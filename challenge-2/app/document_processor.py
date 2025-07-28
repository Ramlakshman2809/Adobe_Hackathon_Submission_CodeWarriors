import os
import json
import time
import pdfplumber
import re
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
import numpy as np
from typing import List, Dict, Any
from datetime import datetime
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Initialize models
sentence_model = SentenceTransformer("all-MiniLM-L6-v2")
kw_model = KeyBERT(model="paraphrase-MiniLM-L6-v2")

class DocumentProcessor:
    def __init__(self, input_dir: str = None):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_dir = input_dir or os.path.join(self.base_dir, "input")
        os.makedirs(self.input_dir, exist_ok=True)
        print(f"Input directory: {self.input_dir}")

    def get_pdf_paths(self) -> List[str]:
        try:
            pdfs = [
                os.path.join(self.input_dir, f)
                for f in os.listdir(self.input_dir)
                if f.lower().endswith('.pdf')
            ]
            print(f"Found {len(pdfs)} PDF files")
            return pdfs
        except Exception as e:
            print(f"Error finding PDFs: {str(e)}")
            return []

    def extract_sections(self, pdf_path: str) -> List[Dict[str, Any]]:
        sections = []
        try:
            with pdfplumber.open(pdf_path) as pdf:
                current_section = None
                for page_num, page in enumerate(pdf.pages, 1):
                    text = page.extract_text() or ""
                    if not text.strip():
                        continue

                    lines = text.split('\n')
                    for line in lines:
                        line = line.strip()
                        if self._is_heading(line):
                            if current_section and current_section['text'].strip():
                                sections.append(current_section)
                            current_section = {
                                "title": line,
                                "text": "",
                                "page": page_num,
                                "document": os.path.basename(pdf_path)
                            }
                        elif current_section:
                            current_section['text'] += line + "\n"

                    if current_section and current_section['text'].strip():
                        sections.append(current_section)
                        current_section = None

            return sections
        except Exception as e:
            print(f"Error processing {pdf_path}: {str(e)}")
            return []

    def _is_heading(self, line: str) -> bool:
        if not line.strip():
            return False
        patterns = [
            r'^[A-Z][A-Z0-9\s,:;-]+$',
            r'^\d+\.\s+[A-Z]',
            r'^[A-Z][a-z]+:',
            r'^##\s+.+',
            r'^(Introduction|Conclusion|References|Abstract)\b',
            r'^(Activities|Attractions|Dining|Accommodation|Transport|Tips)\b'
        ]
        return (len(line.split()) <= 10 and any(re.match(pattern, line) for pattern in patterns))

    def process_documents(self, persona: str, job: str) -> Dict[str, Any]:
        pdf_paths = self.get_pdf_paths()
        if not pdf_paths:
            return {"error": f"No PDF files found in {self.input_dir}"}

        context = f"Persona: {persona}. Task: {job}"
        context_embedding = sentence_model.encode(context)

        extracted_sections = []
        subsection_candidates = []

        for pdf_path in pdf_paths:
            sections = self.extract_sections(pdf_path)
            for section in sections:
                try:
                    section_text = section["text"][:2000]

                    section_embedding = sentence_model.encode(section_text)
                    section_score = np.dot(context_embedding, section_embedding) / (
                        np.linalg.norm(context_embedding) * np.linalg.norm(section_embedding))

                    extracted_sections.append({
                        "document": section["document"],
                        "section_title": section["title"],
                        "importance_rank": float(np.clip(section_score, 0, 1)),
                        "page_number": section["page"]
                    })

                    # Improved chunking and filtering
                    chunks = self._split_into_chunks(section_text)
                    for chunk in chunks:
                        chunk_len = len(chunk)
                        if chunk_len < 50 or chunk_len > 1000:
                            print(f"[SKIP] Chunk length out of range ({chunk_len}): {chunk[:80]}...")
                            continue

                        chunk_embedding = sentence_model.encode(chunk)
                        chunk_score = np.dot(context_embedding, chunk_embedding) / (
                            np.linalg.norm(context_embedding) * np.linalg.norm(chunk_embedding))

                        print(f"[DEBUG] Score: {chunk_score:.3f} | Chunk: {chunk[:80]}...")

                        if chunk_score > 0.20:
                            subsection_candidates.append({
                                "document": section["document"],
                                "refined_text": chunk,
                                "page_number": section["page"],
                                "score": chunk_score
                            })
                        else:
                            print(f"[SKIP] Low score ({chunk_score:.3f}) for chunk from {section['document']} page {section['page']}")

                except Exception as e:
                    print(f"Error processing section: {str(e)}")

        # Normalize and sort
        extracted_sections.sort(key=lambda x: x["importance_rank"], reverse=True)
        if extracted_sections:
            max_score = extracted_sections[0]["importance_rank"]
            for section in extracted_sections:
                section["importance_rank"] = round(section["importance_rank"] / max_score, 2)

        # Top 1-2 chunks per document, up to 5
        subsections_by_doc = {}
        for sub in sorted(subsection_candidates, key=lambda x: x["score"], reverse=True):
            doc = sub["document"]
            if doc not in subsections_by_doc:
                subsections_by_doc[doc] = []
            if len(subsections_by_doc[doc]) < 2:
                subsections_by_doc[doc].append(sub)

        subsection_analysis = [
            {
                "document": sub["document"],
                "refined_text": sub["refined_text"],
                "page_number": sub["page_number"]
            }
            for subs in subsections_by_doc.values() for sub in subs
        ][:5]

        return {
            "metadata": {
                "input_documents": [os.path.basename(p) for p in pdf_paths],
                "persona": persona,
                "job_to_be_done": job,
                "processing_timestamp": datetime.now().isoformat()
            },
            "extracted_sections": extracted_sections[:5],
            "subsection_analysis": subsection_analysis
        }

    def _split_into_chunks(self, text: str, chunk_size: int = 3) -> List[str]:
        # Sliding window of sentences
        sentences = [s.strip() for s in re.split(r'(?<=[.!?]) +', text) if s.strip()]
        chunks = []
        for i in range(0, len(sentences), chunk_size):
            chunk = " ".join(sentences[i:i + chunk_size])
            if chunk:
                chunks.append(chunk)
        return chunks

if __name__ == "__main__":
    processor = DocumentProcessor()
    result = processor.process_documents(
        persona="Travel Planner",
        job="Plan a trip of 4 days for a group of 10 college friends."
    )

    print(json.dumps(result, indent=2))

    with open("./output/challenge1b_output.json", "w") as f:
        json.dump(result, f, indent=2)
    print("Output saved to output.json")
