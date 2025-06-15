import pytest
from io import BytesIO
from unittest.mock import patch, AsyncMock
from backend.job_recommend import extract_text_from_pdf, recommend_jobs_from_resume
from fitz import open as fitz_open
from backend.titan_client import query_titan

def test_extract_text_from_pdf_empty():
    # Create a PDF with one blank page
    doc = fitz_open()
    doc.new_page()  # At least one page required
    buffer = BytesIO()
    doc.save(buffer)
    pdf_bytes = buffer.getvalue()

    result = extract_text_from_pdf(pdf_bytes)
    assert isinstance(result, str)
    assert result.strip() == ""

