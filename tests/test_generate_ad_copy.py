
import unittest
from unittest.mock import patch, MagicMock

from generate_ad_copy import run_ad_copy_generation

class TestGenerateAdCopy(unittest.TestCase):

    @patch('generate_ad_copy.genai.Client')
    def test_run_ad_copy_generation_success(self, mock_genai_client):
        """Test successful ad copy generation."""
        # Arrange
        mock_stream = [
            MagicMock(text="This is "),
            MagicMock(text="a test ad copy."),
        ]
        mock_client_instance = mock_genai_client.return_value
        mock_client_instance.models.generate_content_stream.return_value = mock_stream

        # Act
        result = run_ad_copy_generation("test-project", "test-location")

        # Assert
        self.assertEqual(result, "This is a test ad copy.")
        mock_genai_client.assert_called_once_with(vertexai=True, project="test-project", location="test-location")
        mock_client_instance.models.generate_content_stream.assert_called_once()

    @patch('generate_ad_copy.genai.Client')
    def test_run_ad_copy_generation_file_not_found(self, mock_genai_client):
        """Test ad copy generation with a FileNotFoundError."""
        # Arrange
        mock_genai_client.side_effect = FileNotFoundError("brand.md not found")

        # Act
        result = run_ad_copy_generation("test-project", "test-location")

        # Assert
        self.assertIn("brand.md not found", result)

if __name__ == '__main__':
    unittest.main()
