
import unittest
from unittest.mock import patch, MagicMock
import os

from generate_videos import run_video_generation

class TestGenerateVideos(unittest.TestCase):

    @patch('generate_videos.subprocess.run')
    @patch('generate_videos.time.sleep')
    @patch('generate_videos.genai.Client')
    def test_run_video_generation_success(self, mock_genai_client, mock_sleep, mock_subprocess_run):
        """Test successful video generation."""
        # Arrange
        mock_operation = MagicMock()
        mock_operation.done = False

        # Make the operation complete after the first check
        def get_operation_side_effect(op):
            mock_op = MagicMock()
            mock_op.done = True
            mock_op.response = True
            mock_op.result.generated_videos[0].video.uri = "gs://fake-bucket/fake-video.mp4"
            return mock_op
        
        mock_client_instance = mock_genai_client.return_value
        mock_client_instance.models.generate_videos.return_value = mock_operation
        mock_client_instance.operations.get.side_effect = get_operation_side_effect

        # Create a dummy scene directory and image
        scene_dir = "prompts-images/test-scene"
        os.makedirs(scene_dir, exist_ok=True)
        with open(os.path.join(scene_dir, "image-1.png"), "w") as f:
            f.write("fake image data")

        # Act
        video_paths, logs = run_video_generation("test-project", "test-location", "gs://test-bucket")

        # Assert
        self.assertIn("test-scene.mp4", video_paths[0])
        self.assertIn("Video downloaded successfully", logs)
        mock_subprocess_run.assert_called_once()

        # Clean up
        os.remove(os.path.join(scene_dir, "image-1.png"))
        os.rmdir(scene_dir)

if __name__ == '__main__':
    unittest.main()
