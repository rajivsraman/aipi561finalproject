import fitz  # PyMuPDF
from backend.titan_client import query_titan

async def score_resume_pdf(resume_file) -> str:
    content = await resume_file.read()
    text = extract_text_from_pdf(content)

    prompt = (
        "You are a resume evaluator. Given the following resume text, score the resume out of 20 and start your response with the score, and "
        "provide professional feedback on strengths, weaknesses, and career fit:\n\n"
        f"{text}"
    )

    return query_titan(prompt)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open("pdf", pdf_bytes)
    return "\n".join([page.get_text() for page in doc])
