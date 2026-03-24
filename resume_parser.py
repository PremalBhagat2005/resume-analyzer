import pdfplumber
from typing import Union
from pathlib import Path

def extract_text(file: Union[str, Path]) -> str:
    """
    Extract text from a PDF file.
    
    Args:
        file: Path to the PDF file
        
    Returns:
        str: Extracted text converted to lowercase, with pages separated by newlines
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        pdfplumber.exceptions.PDFException: If the file is not a valid PDF
    """
    pages_text = []
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                pages_text.append(page_text)
    
    return "\n".join(pages_text).lower()