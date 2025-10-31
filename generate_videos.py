"Generates videos from scene images using the Veo model."

import logging
import os
import time
import glob
import subprocess
from google import genai
from google.genai import types
import io

import config

def download_video(gcs_uri: str, local_path: str, scene_name: str) -> str | None:
    """Downloads a video from GCS to a local path and returns the local file path."""
    local_file_path = os.path.join(local_path, f"{scene_name}.mp4")
    logging.info(f"Downloading video from {gcs_uri} to {local_file_path}...")
    try:
        subprocess.run(["gsutil", "cp", gcs_uri, local_file_path], check=True, capture_output=True, text=True)
        logging.info(f"Video downloaded successfully to {local_file_path}")
        return local_file_path
    except FileNotFoundError:
        logging.error("gsutil command not found. Please ensure the Google Cloud SDK is installed and in your PATH.")
        return None
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to download video from GCS: {e}\n{e.stderr}")
        return None

def generate_video_for_scene(client, scene_dir, output_gcs_path, local_video_path):
    """Generates a video for a single scene and returns the local file path."""
    scene_name = os.path.basename(scene_dir)
    logging.info(f"Processing scene: {scene_name}")

    image_path = os.path.join(scene_dir, "image-1.png")
    if not os.path.exists(image_path):
        logging.warning(f"image-1.png not found in {scene_dir}. Skipping.")
        return None

    output_gcs_uri = f"{output_gcs_path}/{scene_name}.mp4"

    logging.info(f"Generating video for {scene_name}...")
    
    try:
        img = types.Image.from_file(location=image_path)

        operation = client.models.generate_videos(
            model=config.VIDEO_MODEL,
            image=types.Image(
                image_bytes=img.image_bytes,
                mime_type="image/png",
            ),
            config=types.GenerateVideosConfig(
                output_gcs_uri=output_gcs_uri,
                aspect_ratio="16:9",
                number_of_videos=1,
                person_generation="allow_adult",
            ),
        )

        logging.info(f"Video generation started. Operation: {operation.operation.name}")
        logging.info("Waiting for operation to complete...")

        while not operation.done:
            time.sleep(30)
            operation = client.operations.get(operation)
            logging.info(f"Operation status: {operation.state}")

        if operation.response:
            generated_video_uri = operation.result.generated_videos[0].video.uri
            logging.info(f"Video generated successfully: {generated_video_uri}")
            return download_video(generated_video_uri, local_video_path, scene_name)
        else:
            logging.error("Video generation failed or returned no response.")
            return None

    except Exception as e:
        logging.error(f"An unexpected error occurred during video generation for scene {scene_name}: {e}")
        return None

def run_video_generation(project_id, location, gcs_bucket):
    """Main function to generate videos for all scenes."""
    log_stream = io.StringIO()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=log_stream)

    if not project_id or project_id == "[your-project-id]":
        logging.error("Please set your Google Cloud Project ID.")
        return [], log_stream.getvalue()

    if not gcs_bucket or gcs_bucket == "gs://[your-gcs-bucket]/videos":
        logging.error("Please set your GCS bucket.")
        return [], log_stream.getvalue()

    video_paths = []
    try:
        client = genai.Client(vertexai=True, project=project_id, location=location)

        os.makedirs(config.VIDEOS_DIR, exist_ok=True)

        scene_dirs = [d for d in glob.glob(f"{config.PROMPTS_IMAGES_DIR}/*") if os.path.isdir(d)]

        for scene_dir in scene_dirs:
            video_path = generate_video_for_scene(client, scene_dir, gcs_bucket, config.VIDEOS_DIR)
            if video_path:
                video_paths.append(video_path)

        logging.info("All scenes processed.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
    
    return video_paths, log_stream.getvalue()

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate videos for scenes.")
    parser.add_argument("--project_id", type=str, default=config.PROJECT_ID, help="Google Cloud Project ID.")
    parser.add_argument("--location", type=str, default=config.LOCATION, help="Google Cloud Location.")
    parser.add_argument("--gcs_bucket", type=str, default=config.OUTPUT_GCS_BUCKET, help="GCS bucket for video output.")
    args = parser.parse_args()

    video_files, logs = run_video_generation(args.project_id, args.location, args.gcs_bucket)
    print("--- LOGS ---")
    print(logs)
    print("--- GENERATED VIDEOS ---")
    for video_file in video_files:
        print(video_file)
