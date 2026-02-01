import os
import PyPDF2
import pdfplumber
from crewai.tools import tool

@tool("Resume Parser Tool")
def parse_resume(file_path: str) -> str:
    """
    Parse resume PDF and extract text content.
    
    Args:
        file_path: Path to the resume PDF file
    
    Returns:
        Extracted text content from the resume or error message.
    """
    if not os.path.exists(file_path):
        return f"Error: Resume file not found at {file_path}. Please check the file path."
    
    try:
        # Try using pdfplumber first (better text extraction)
        with pdfplumber.open(file_path) as pdf:
            text = ""
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text + "\n"
            
            if text.strip():
                return text.strip()
    except Exception as e:
        print(f"pdfplumber failed: {e}, trying PyPDF2...")
    
    try:
        # Fallback to PyPDF2
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            
            if text.strip():
                return text.strip()
            else:
                return "Error: Could not extract text from PDF. The file might be image-based or corrupted."
    
    except Exception as e:
        return f"Error: Failed to parse resume PDF. {str(e)}"
