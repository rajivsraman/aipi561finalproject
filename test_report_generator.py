import os
import unittest
from backend.report_generator import SessionTranscript, strip_unicode, REPORTS_DIR

class TestReportGenerator(unittest.TestCase):

    def setUp(self):
        self.transcript = SessionTranscript()

    def tearDown(self):
        # Clean up generated PDF files
        for f in os.listdir(REPORTS_DIR):
            if f.endswith("_session.pdf"):
                os.remove(os.path.join(REPORTS_DIR, f))

    def test_strip_unicode(self):
        input_str = "Résumé – naïve façade"
        stripped = strip_unicode(input_str)
        self.assertNotIn("é", stripped)
        self.assertIn("e", stripped)

    def test_add_and_clear_entries(self):
        self.transcript.add("Hi", "Hello back")
        self.assertEqual(len(self.transcript.entries), 1)
        self.transcript.clear()
        self.assertEqual(len(self.transcript.entries), 0)

    def test_generate_pdf_without_metrics(self):
        self.transcript.add("Q1", "A1")
        self.transcript.add("Q2", "A2")
        filename = self.transcript.generate_pdf("Test Session")
        full_path = os.path.join(REPORTS_DIR, filename)

        self.assertTrue(os.path.exists(full_path))
        self.assertTrue(filename.endswith("_session.pdf"))

    def test_generate_pdf_with_metrics(self):
        self.transcript.add("Prompt", "Response")
        metrics = {
            "requests": 10,
            "last_latency_sec": 0.423,
            "latency_history": [0.5, 0.3, 0.47]
        }
        filename = self.transcript.generate_pdf("Metrics Test", metrics)
        path = os.path.join(REPORTS_DIR, filename)

        self.assertTrue(os.path.exists(path))
        self.assertGreater(os.path.getsize(path), 100)  # Ensure content is written

if __name__ == '__main__':
    unittest.main()
