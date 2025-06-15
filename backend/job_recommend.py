import fitz
from backend.titan_client import query_titan

async def recommend_jobs_from_resume(resume_file, interests: str) -> str:
    resume_text = extract_text_from_pdf(await resume_file.read())
    prompt = (
        "You are a career advisor. Review this resume and interests, "
        "recommend 3–5 jobs with reasons. Please start with the list of the jobs in your response.\n\n"
        f"Resume:\n{resume_text}\nInterests:\n{interests}"
    )
    return query_titan(prompt)

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    doc = fitz.open("pdf", pdf_bytes)
    return "\n".join(p.get_text() for p in doc)
