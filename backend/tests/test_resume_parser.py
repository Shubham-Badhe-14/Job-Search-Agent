import pytest
from unittest.mock import patch, MagicMock
from backend.tools.resume_parser import parse_resume

def test_resume_parser_not_found():
    result = parse_resume.invoke({"file_path": "non_existent.pdf"})
    assert "Error: Resume file not found" in result

@patch("backend.tools.resume_parser.pdfplumber.open")
def test_resume_parser_success(mock_pdf_open):
    # Mock context manager
    mock_pdf = MagicMock()
    mock_pdf_open.return_value.__enter__.return_value = mock_pdf
    
    mock_page = MagicMock()
    mock_page.extract_text.return_value = "Sample Resume Text"
    mock_pdf.pages = [mock_page]
    
    # Create a dummy file to bypass exists check
    with patch("os.path.exists", return_value=True):
         result = parse_resume.invoke({"file_path": "dummy.pdf"})
    
    assert "Resume parsed successfully" in result
    assert "Sample Resume Text" in result
