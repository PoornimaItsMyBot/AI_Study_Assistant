
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import unittest
from unittest.mock import patch, MagicMock
from ai.gemini_client import GeminiClient


class TestGeminiClient(unittest.TestCase):

    @patch("ai.gemini_client.genai.Client")
    @patch("ai.gemini_client.os.getenv")
    def test_raises_error_if_api_key_missing(self, mock_getenv, mock_genai_client):
        mock_getenv.return_value = None
        with self.assertRaises(ValueError):
            GeminiClient()

    @patch("ai.gemini_client.genai.Client")
    @patch("ai.gemini_client.os.getenv")
    def test_generate_text_returns_stripped_response(self, mock_getenv, mock_genai_client):
        mock_getenv.return_value = "fake-api-key"

        mock_response = MagicMock()
        mock_response.text = "  Hello, student!  "
        mock_instance = mock_genai_client.return_value
        mock_instance.models.generate_content.return_value = mock_response

        client = GeminiClient()
        result = client.generate_text("Say hello")

        self.assertEqual(result, "Hello, student!")


if __name__ == "__main__":
    unittest.main()