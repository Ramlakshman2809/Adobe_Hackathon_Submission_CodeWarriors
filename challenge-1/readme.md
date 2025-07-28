# PDF Outline Extractor

A Dockerized solution that extracts hierarchical document outlines (titles and headings) from PDF files and outputs them in structured JSON format.

## Approach

### Core Methodology
1. **PDF Analysis**:
   - Uses font attributes (size, style) and text positioning to identify headings
   - Analyzes document structure to determine heading hierarchy (H1, H2, H3)

2. **Hierarchy Detection**:
   - Larger/bolder text → Higher level headings (H1)
   - Progressively smaller text → Lower level headings (H2, H3)
   - Considers text formatting (bold, italics) and positioning (centering)

3. **Title Extraction**:
   - Identifies the largest text on the first page as the document title
   - Falls back to first heading if no clear title is found

## Technical Stack

### Libraries Used
| Library | Version | Purpose |
|---------|---------|---------|
| pdfminer.six | 20221105 | PDF text extraction and layout analysis |
| Python | 3.9+ | Core processing logic |

### System Requirements
- Docker (for containerized execution)
- 8 CPU cores, 16GB RAM
- 200MB disk space

## Installation & Execution

### 1. Build the Docker Image
```bash
docker build --platform linux/amd64 -t pdf-outline-extractor:latest .
```

### 2. Run the Container
```bash
docker run --rm -v "/path/to/your/input:/app/input" -v "/path/to/your/output:/app/output" --network none pdf-outline-extractor
```

### 3. Expected Output
For each input.pdf in /app/input, creates output.json in /app/output with structure:
```json
{
  "title": "Document Title",
  "outline": [
    {"level": "H1", "text": "Main Heading", "page": 1},
    {"level": "H2", "text": "Subheading", "page": 2}
  ]
}
```






