import os
from dotenv import load_dotenv

load_dotenv()

# Google Cloud Project Configuration
PROJECT_ID = os.environ.get("PROJECT_ID", "[your-project-id]")
LOCATION = os.environ.get("LOCATION", "us-central1")

# Google Cloud Storage Configuration
OUTPUT_GCS_BUCKET = os.environ.get("OUTPUT_GCS_BUCKET", "gs://[your-gcs-bucket]/videos")

# Generative Model Configuration
GEMINI_MODEL = "gemini-2.5-flash-preview-09-2025"
VIDEO_MODEL = "veo-3.1-generate-preview"

# Local Directory Configuration
VIDEOS_DIR = "videos"
GENERATED_SCENES_DIR = "generated-scenes"
PROMPTS_IMAGES_DIR = "prompts-images"