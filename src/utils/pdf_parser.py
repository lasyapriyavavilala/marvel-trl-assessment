import fitz  # PyMuPDF

def extract_text_from_pdf(filepath: str, max_pages: int = 50) -> str:
    """
    Extract text from PDF using PyMuPDF.
    
    Args:
        filepath: Path to PDF file
        max_pages: Maximum pages to parse (limit for speed)
    
    Returns:
        Extracted text
    """
    try:
        doc = fitz.open(filepath)
        text_parts = []
        
        for page_num in range(min(len(doc), max_pages)):
            page = doc[page_num]
            text_parts.append(page.get_text())
        
        return "\n\n".join(text_parts)
    
    except Exception as e:
        print(f"❌ PDF parsing error for {filepath}: {e}")
        return ""