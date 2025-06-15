import unittest
from unittest.mock import patch, MagicMock
from backend import titan_client
import json

class TestTitanClient(unittest.TestCase):

    @patch("backend.titan_client.bedrock")
    def test_query_titan_success(self, mock_bedrock):
        # Mocked response body structure
        mock_response = MagicMock()
        mock_response["body"].read.return_value = b'{"results": [{"outputText": "Mock Titan output"}]}'
        mock_bedrock.invoke_model.return_value = mock_response

        prompt = "What is the capital of France?"
        result = titan_client.query_titan(prompt)

        self.assertEqual(result, "Mock Titan output")
        mock_bedrock.invoke_model.assert_called_once()
        args, kwargs = mock_bedrock.invoke_model.call_args
        self.assertIn("body", kwargs)
        self.assertIn("inputText", json.loads(kwargs["body"]))

    @patch("backend.titan_client.bedrock")
    def test_query_titan_no_output(self, mock_bedrock):
        mock_response = MagicMock()
        mock_response["body"].read.return_value = b'{"results": [{}]}'
        mock_bedrock.invoke_model.return_value = mock_response

        prompt = "Test fallback"
        result = titan_client.query_titan(prompt)

        self.assertEqual(result, "No output.")

if __name__ == "__main__":
    unittest.main()
