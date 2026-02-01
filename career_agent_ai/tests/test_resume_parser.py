import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent dir to path to import modules
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from career_agent_ai.tools.resume_parser import parse_resume

class TestResumeParser(unittest.TestCase):
    
    @patch('career_agent_ai.tools.resume_parser.pdfplumber.open')
    @patch('os.path.exists')
    def test_parse_resume_success_pdfplumber(self, mock_exists, mock_pdf_open):
        """Test successful parsing with pdfplumber"""
        mock_exists.return_value = True
        
        # Mock PDF page and text
        mock_page = MagicMock()
        mock_page.extract_text.return_value = "Candidate Name\\\nSkills: Python, AI"
        
        mock_pdf = MagicMock()
        mock_pdf.pages = [mock_page]
        mock_pdf_open.return_value.__enter__.return_value = mock_pdf
        
        result = parse_resume("fake_resume.pdf")
        
        self.assertIn("Candidate Name", result)
        self.assertIn("Skills: Python, AI", result)

    @patch('career_agent_ai.tools.resume_parser.os.path.exists')
    def test_resume_not_found(self, mock_exists):
        """Test file not found error"""
        mock_exists.return_value = False
        result = parse_resume("nonexistent.pdf")
        self.assertTrue(result.startswith("Error: Resume file not found"))

if __name__ == '__main__':
    unittest.main()
