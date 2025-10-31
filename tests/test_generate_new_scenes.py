
import unittest
import os
import shutil

from generate_new_scenes import run_scene_generation
import config

class TestGenerateNewScenes(unittest.TestCase):

    def setUp(self):
        """Set up the test environment."""
        self.output_dir = config.GENERATED_SCENES_DIR
        # Clean up the output directory before each test
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def tearDown(self):
        """Clean up the test environment."""
        if os.path.exists(self.output_dir):
            shutil.rmtree(self.output_dir)

    def test_run_scene_generation(self):
        """Test the run_scene_generation function."""
        generated_files, logs = run_scene_generation()

        # Check if the output directory was created
        self.assertTrue(os.path.exists(self.output_dir))

        # Check if the expected number of files were generated
        self.assertEqual(len(generated_files), 2)

        # Check if the generated files exist and are not empty
        for file_path in generated_files:
            self.assertTrue(os.path.exists(file_path))
            self.assertGreater(os.path.getsize(file_path), 0)

if __name__ == '__main__':
    unittest.main()
