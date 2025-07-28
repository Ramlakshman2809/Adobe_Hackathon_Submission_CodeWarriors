# Adobe Hackathon PDF Document Processing Projects

This repository contains two distinct PDF document processing projects submitted for Adobe hackathon challenges, each designed for different use cases and requirements.

##  Project Structure

```
├── Challenge-1/          # Simple PDF outline extractor
│   ├── prg1.py           # Initial implementation
│   ├── prg2.py           # Refined implementation
│   ├── requirements.txt
│   ├── dockerfile
│   ├── app/
│   │   ├── input/         # PDF input directory
│   │   └── output/        # JSON output directory
│   └── README.md
└── Challenge-2/          # Advanced document processor with NLP capabilities
    ├── app/
    │   ├── document_processor.py
    │   ├── run_tests.py
    │   ├── requirements.txt
    │   ├── Dockerfile
    │   ├── input/         # PDF input directory
    │   └── output/        # JSON output directory
    └── README.md
```

##  Challenge-2: Advanced Document Processor

A sophisticated Python-based tool for extracting, ranking, and analyzing sections and subsections from PDF documents using state-of-the-art NLP models.

### Features

- **Intelligent Section Extraction**: Extracts sections and subsections from PDFs using advanced heading detection
- **NLP-Powered Ranking**: Ranks sections by relevance to user-defined personas and job tasks
- **Advanced NLP Models**: Uses Sentence Transformers and KeyBERT for semantic analysis
- **Structured Output**: Generates comprehensive JSON with metadata, ranked sections, and refined text chunks
- **Flexible Use Cases**: Designed for research, business analysis, and educational content extraction
- **Docker Support**: Containerized deployment with Docker

### Technology Stack

- **Python 3.7+**
- **NLP Libraries**: sentence-transformers, keybert, transformers
- **PDF Processing**: pdfplumber
- **Machine Learning**: torch, numpy
- **Model Hub**: huggingface-hub

### Installation & Usage

1. **Clone and Setup**:

   ```bash
   cd Challenge-2
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r app/requirements.txt
   ```

2. **Prepare Input**:

   - Place PDF files in `app/input/` subdirectories (e.g., `app/input/academic_research/`)

3. **Run Processing**:

   ```bash
   # Direct execution
   python app/document_processor.py

   # With test cases
   python app/run_tests.py
   ```

4. **Docker Usage**:
   ```bash
   docker build -t document-processor ./app
   docker run --rm -v $(pwd)/app/input:/app/input -v $(pwd)/app/output:/app/output document-processor
   ```

### Output Structure

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

---

## ️ Challenge-1: PDF Outline Extractor

A lightweight, efficient tool for extracting document outlines and titles from PDF files by analyzing text formatting and structure.

### Features

- **Fast Processing**: Lightweight implementation with minimal dependencies
- **Font Analysis**: Analyzes font usage to identify headings vs. body text
- **Heading Detection**: Identifies headings based on formatting, position, and patterns
- **Hierarchical Output**: Generates structured outline with heading levels (H1, H2, H3)
- **Batch Processing**: Processes multiple PDFs in a directory
- **Simple JSON Output**: Clean, readable output format

### Technology Stack

- **Python 3.7+**
- **PDF Processing**: pdfminer.six, pdfplumber
- **Text Analysis**: Built-in regex and string processing

### Installation & Usage

1. **Setup**:

   ```bash
   cd Challenge-1
   pip install -r requirements.txt
   ```

2. **Run Processing**:

   ```bash
   # Process all PDFs in input directory
   python prg2.py

   # With custom input/output directories
   python prg2.py ./app/input ./app/output
   ```

### Output Structure

```json
{
  "title": "Document Title",
  "outline": [
    {
      "level": "H1",
      "text": "Main Heading",
      "page": 1
    },
    {
      "level": "H2",
      "text": "Sub Heading",
      "page": 2
    }
  ]
}
```

### Implementation Versions

- **prg1.py**: Initial implementation with basic heading detection
- **prg2.py**: Refined implementation with improved font analysis and better heading detection logic

---

##  Comparison

| Feature              | Challenge-2                    | Challenge-1             |
| -------------------- | ------------------------------ | ----------------------- |
| **Complexity**       | Advanced (NLP-powered)         | Simple (rule-based)     |
| **Dependencies**     | Heavy (ML models)              | Light (minimal)         |
| **Processing Speed** | Slower (NLP inference)         | Fast (text analysis)    |
| **Use Case**         | Content analysis & ranking     | Structure extraction    |
| **Output**           | Rich metadata + ranked content | Clean outline structure |
| **Resource Usage**   | High (GPU recommended)         | Low (CPU only)          |

##  Requirements

### Challenge-2

- Python 3.7+
- 4GB+ RAM (8GB+ recommended)
- Internet connection (for model downloads)
- GPU optional but recommended for large documents

### Challenge-1

- Python 3.7+
- 1GB+ RAM
- No internet connection required
- CPU only

##  Quick Start

### For Advanced Analysis (Challenge-2):

```bash
cd Challenge-2
pip install -r app/requirements.txt
python app/run_tests.py
```

### For Simple Outline Extraction (Challenge-1):

```bash
cd Challenge-1
pip install -r requirements.txt
python prg2.py
```

##  License

MIT License - See individual project directories for specific license information.

## 欄 Contributing

Both projects are open to contributions. Please ensure to:

1. Test your changes thoroughly
2. Update documentation as needed
3. Follow the existing code style
4. Add appropriate error handling

---

**Note**: The first run of Challenge-2 may take longer as it downloads NLP models. Workspace is ready to use immediately after installation.
