import json
import os
import re
from collections import defaultdict
from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer, LTChar, LTTextBoxHorizontal


class PDFOutlineExtractor:
    """Extracts document outline/title from PDF files by analyzing text formatting and structure."""
    
    def __init__(self):
        """Initialize the extractor with empty title and outline."""
        self.title = ""
        self.outline = []
        self.font_stats = defaultdict(int)
    
    def extract_from_pdf(self, pdf_path):
        """Main method to extract outline from PDF file.
        
        Args:
            pdf_path: Path to the PDF file to process
            
        Returns:
            Dictionary containing title and outline structure
        """
        self._analyze_fonts(pdf_path)
        self._extract_headings(pdf_path)
        return self._generate_output()
    
    def _analyze_fonts(self, pdf_path):
        """Analyze font usage statistics across the document to identify common body text."""
        for page_layout in extract_pages(pdf_path):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    first_char = self._get_first_character(element)
                    if first_char:
                        font_key = (first_char.size, first_char.fontname)
                        self.font_stats[font_key] += 1
    
    def _get_first_character(self, text_container):
        """Helper to safely get the first character from a text container."""
        if not hasattr(text_container, '_objs') or not text_container._objs:
            return None
            
        first_obj = text_container._objs[0]
        if hasattr(first_obj, '_objs') and first_obj._objs:
            first_char = first_obj._objs[0]
            if isinstance(first_char, LTChar):
                return first_char
        return None
    
    def _extract_headings(self, pdf_path):
        """Extract potential headings from the document based on formatting."""
        if not self.font_stats:
            self._analyze_fonts(pdf_path)
            
        common_body_font = self._get_most_common_font()
        
        for page_num, page_layout in enumerate(extract_pages(pdf_path), start=1):
            for element in page_layout:
                if isinstance(element, LTTextBoxHorizontal):
                    text = element.get_text().strip()
                    if not text:
                        continue
                    
                    first_char = self._get_first_character(element)
                    if not first_char:
                        continue
                        
                    font_key = (first_char.size, first_char.fontname)
                    is_bold = "bold" in first_char.fontname.lower()
                    
                    if self._is_heading(element, text, font_key, is_bold, page_layout):
                        level = self._determine_heading_level(first_char.size, is_bold)
                        self._add_heading(level, text, page_num)
    
    def _get_most_common_font(self):
        """Get the most common font in the document (assumed to be body text)."""
        if not self.font_stats:
            return None
        return sorted(self.font_stats.items(), key=lambda x: -x[1])[0][0]
    
    def _is_heading(self, element, text, font_key, is_bold, page_layout):
        """Determine if an element should be considered a heading."""
        common_body_font = self._get_most_common_font()
        return (
            font_key != common_body_font
            or self._is_heading_by_format(text)
            or self._is_heading_by_position(element, page_layout)
        )
    
    def _is_heading_by_format(self, text):
        """Check if text matches common heading patterns."""
        # Numbered headings (e.g., "1. Introduction", "Section 2")
        if re.match(r'^(?:\d+\.\s+|[A-Z]\.\s+|Section\s+\d+|Chapter\s+\d+)', text):
            return True
        
        # All caps headings (minimum 3 chars, max 6 words)
        if text.isupper() and len(text) >= 3 and len(text.split()) <= 6:
            return True
            
        # Title case headings (max 6 words with at least one title case word)
        words = text.split()
        return (len(words) <= 6 
                and all(w.istitle() or w.islower() for w in words) 
                and any(w.istitle() for w in words))
    
    def _is_heading_by_position(self, element, page_layout):
        """Check if text position suggests a heading (centered or with whitespace)."""
        # Check if centered (within 20pt tolerance)
        page_center = page_layout.width / 2
        element_center = (element.x0 + element.x1) / 2
        if abs(element_center - page_center) < 20:
            return True
            
        # Check for sufficient whitespace above (not at very top)
        return element.y1 < page_layout.height - 30
    
    def _determine_heading_level(self, size, is_bold):
        """Determine heading level based on font size and style."""
        if size > 14 or is_bold:
            return "H1"
        elif size > 12:
            return "H2"
        return "H3"
    
    def _add_heading(self, level, text, page_num):
        """Add a heading to the outline structure."""
        self.outline.append({
            "level": level,
            "text": text,
            "page": page_num
        })
    
    def _generate_output(self):
        """Generate the output JSON structure with title and outline."""
        if not self.title:
            self._determine_title()
        return {
            "title": self.title,
            "outline": self.outline
        }
    
    def _determine_title(self):
        """Determine the document title from the outline."""
        if not self.outline:
            self.title = "Untitled"
            return
            
        for heading in self.outline:
            if heading["level"] == "H1":
                self.title = heading["text"]
                return
                
        self.title = self.outline[0]["text"]


def process_pdfs(input_dir, output_dir):
    """Process all PDFs in input directory and save JSONs to output directory.
    
    Args:
        input_dir: Directory containing PDF files to process
        output_dir: Directory where JSON results will be saved
    """
    os.makedirs(output_dir, exist_ok=True)
    
    for filename in os.listdir(input_dir):
        if filename.lower().endswith('.pdf'):
            pdf_path = os.path.join(input_dir, filename)
            json_filename = f"{os.path.splitext(filename)[0]}.json"
            json_path = os.path.join(output_dir, json_filename)
            
            extractor = PDFOutlineExtractor()
            result = extractor.extract_from_pdf(pdf_path)
            
            with open(json_path, 'w') as f:
                json.dump(result, f, indent=2)


if __name__ == "__main__":
    import sys
    input_dir = sys.argv[1] if len(sys.argv) > 1 else "/app/input"
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "/app/output"
    process_pdfs(input_dir, output_dir)