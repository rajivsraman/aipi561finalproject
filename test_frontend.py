import unittest
from unittest.mock import patch, MagicMock
import streamlit as st
import sys

class TestFrontendStreamlit(unittest.TestCase):
    @patch("requests.post")
    @patch.dict("sys.modules", {
        "matplotlib": MagicMock(),
        "matplotlib.pyplot": MagicMock(),
        "numpy": MagicMock(),
        "numpy.linalg": MagicMock(),
    })
    def test_login_successful(self, mock_post):
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = {"access_token": "fake_token"}

        def mock_text_input(label, **kwargs):
            if "Username" in label:
                return "test_user"
            if "Password" in label:
                return "test_pass"
            return ""

        if "token" in st.session_state:
            del st.session_state["token"]
        if "username" in st.session_state:
            del st.session_state["username"]

        with patch("streamlit.text_input", side_effect=mock_text_input), \
            patch("streamlit.radio", return_value="Login"), \
            patch("streamlit.button", return_value=True), \
            patch("streamlit.subheader"), \
            patch("streamlit.columns", return_value=[MagicMock(), MagicMock()]), \
            patch("streamlit.success"), \
            patch("streamlit.error"):

            import importlib
            import frontend.streamlit_app
            importlib.reload(frontend.streamlit_app)

            assert st.session_state["token"] == "fake_token"
            assert st.session_state["username"] == "test_user"

    @patch("requests.get")
    def test_metrics_graph_render(self, mock_get):
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = {
            "latency_history": [0.1, 0.15, 0.12],
            "requests": 3,
            "last_latency_sec": 0.12
        }

        response = mock_get("http://localhost:8000/metrics")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()["latency_history"]), 3)


if __name__ == "__main__":
    unittest.main()
