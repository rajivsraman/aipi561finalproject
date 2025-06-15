import unittest
from unittest.mock import patch, AsyncMock
from backend import resume_scoring

class TestResumeScoring(unittest.TestCase):

    def test_extract_text_from_pdf(self):
        # Create a simple PDF in memory with 1 page of text
        import fitz
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), "Test resume content")
        pdf_bytes = doc.write()
        doc.close()

        result = resume_scoring.extract_text_from_pdf(pdf_bytes)
        self.assertIn("Test resume content", result)


if __name__ == "__main__":
    unittest.main()
