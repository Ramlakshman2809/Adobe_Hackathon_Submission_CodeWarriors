# Document Processor

A Python-based tool for extracting, ranking, and analyzing sections and subsections from PDF documents using NLP models. Designed for flexible use cases such as research, business analysis, and educational content extraction.

## Features

- Extracts sections and subsections from PDFs using heading detection
- Ranks sections by relevance to a user-defined persona and job/task
- Uses state-of-the-art NLP models (Sentence Transformers, KeyBERT)
- Outputs structured JSON with metadata, ranked sections, and refined text chunks
- CLI and Docker support

## Requirements

- Python 3.7+
- See `app/requirements.txt` for Python dependencies:
  - pdfplumber
  - sentence-transformers
  - keybert
  - numpy
  - huggingface-hub
  - torch
  - transformers

## Installation

1. Clone the repository and navigate to the project directory.
2. (Optional) Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r app/requirements.txt
   ```

## Usage

### 1. Prepare Input

- Place your PDF files in the appropriate subdirectory under `app/input/` (e.g., `app/input/academic_research/`).

### 2. Run the Processor

You can run the processor directly or use the provided test runner:

#### Directly (example):

```bash
python document_processor.py
```

This runs a sample job for a travel planner persona.

#### With Test Cases:

```bash
python run_tests.py
```

This will process all test cases defined in `run_tests.py` and output results to `app/output/`.

### 3. Output

- Results are saved as JSON files in `app/output/`.
- Example output structure:

```json
{
  "metadata": {
    "input_documents": ["doc1.pdf", "doc2.pdf"],
    "persona": "Travel Planner",
    "job_to_be_done": "Plan a trip...",
    "processing_timestamp": "2025-07-28T18:48:12.587404"
  },
  "extracted_sections": [
    {
      "document": "doc1.pdf",
      "section_title": "Introduction",
      "importance_rank": 1.0,
      "page_number": 1
    }
  ],
  "subsection_analysis": [
    { "document": "doc1.pdf", "refined_text": "...", "page_number": 2 }
  ]
}
```

## Docker

Build and run the application in a container:

```bash
docker build -t document-processor .
# Run (ensure your PDFs are mounted to /app/input/)
docker run --rm -v $(pwd)/app/input:/app/input -v $(pwd)/app/output:/app/output document-processor
```

## Customization

- Edit `run_tests.py` to add or modify test cases (personas, jobs, input folders).
- The main processing logic is in `document_processor.py`.

## Notes

- The first run may download NLP models (requires internet access).
- Ensure your input PDFs are text-based (not scanned images) for best results.

## License

MIT License
