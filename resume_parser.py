"""
Resume Parser Module
Handles PDF extraction and text processing for resume analysis
"""

import pdfplumber
import logging
from typing import Union
from pathlib import Path

# Configure logging
logger = logging.getLogger(__name__)


def extract_text(file: Union[str, Path]) -> str:
    """Extracts text from PDF resume file, handles encrypted/damaged PDFs gracefully."""
    try:
        pages_text = []
        
        # Open PDF and extract text from each page
        with pdfplumber.open(file) as pdf:
            # Check if PDF has pages
            if not pdf.pages:
                raise ValueError("PDF file is empty or contains no pages")
            
            # Extract text from each page
            for page_num, page in enumerate(pdf.pages, 1):
                try:
                    page_text = page.extract_text()
                    if page_text:
                        pages_text.append(page_text)
                except Exception as e:
                    logger.warning(f"Error extracting text from page {page_num}: {str(e)}")
                    continue
        
        # Check if any text was extracted
        if not pages_text:
            raise ValueError("No text could be extracted from the PDF file")
        
        # Join pages and convert to lowercase for consistent processing
        extracted_text = "\n".join(pages_text).lower()
        logger.info(f"Successfully extracted {len(extracted_text)} characters from PDF")
        
        return extracted_text
        
    except pdfplumber.exceptions.PDFException as e:
        logger.error(f"Invalid PDF file: {str(e)}")
        raise ValueError("The selected file is not a valid PDF") from e
    except FileNotFoundError as e:
        logger.error(f"PDF file not found: {str(e)}")
        raise FileNotFoundError("Resume file not found") from e
    except Exception as e:
        logger.error(f"Unexpected error extracting PDF text: {str(e)}", exc_info=True)
        raise ValueError(f"Error processing PDF: {str(e)}") from e