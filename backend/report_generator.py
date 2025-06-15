from fpdf import FPDF
import os, uuid
from datetime import datetime
import unicodedata

REPORTS_DIR = "generated_reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def strip_unicode(text: str) -> str:
    return unicodedata.normalize("NFKD", text).encode("latin-1", "ignore").decode("latin-1")

class SessionTranscript:
    def __init__(self):
        self.entries = []

    def add(self, prompt: str, response: str):
        self.entries.append((datetime.now(), prompt, response))

    def clear(self):
        self.entries = []

    def generate_pdf(self, session_title: str, metrics: dict = None):
        fn = f"{uuid.uuid4().hex}_session.pdf"
        path = os.path.join(REPORTS_DIR, fn)

        pdf = FPDF()
        pdf.add_page()
        pdf.set_auto_page_break(True, 15)
        pdf.set_font("Arial", "B", 16)
        pdf.cell(0, 10, strip_unicode(session_title), ln=1, align="C")
        pdf.ln(5)

        pdf.set_font("Arial", "", 12)
        for i, (ts, q, a) in enumerate(self.entries, 1):
            pdf.set_font("Arial", "B", 12)
            pdf.cell(0, 8, f"{i}. {ts.strftime('%Y-%m-%d %H:%M:%S')}", ln=1)
            pdf.set_font("Arial", "", 12)
            pdf.multi_cell(0, 6, strip_unicode(f"Q: {q}"))
            pdf.multi_cell(0, 6, strip_unicode(f"A: {a}"))
            pdf.ln(3)

        # Optional metrics footer
        if metrics:
            avg_latency = (
                round(sum(metrics["latency_history"]) / len(metrics["latency_history"]), 3)
                if metrics.get("latency_history") else "N/A"
            )
            pdf.set_font("Arial", "I", 10)
            pdf.ln(5)
            pdf.multi_cell(0, 6, strip_unicode(
                f"--- Server metrics at export ---\n"
                f"Total requests: {metrics.get('requests', 'N/A')}\n"
                f"Average latency: {avg_latency}s\n"
                f"Last latency: {metrics.get('last_latency_sec', 'N/A')}s"
            ))

        pdf.output(path)
        return fn
