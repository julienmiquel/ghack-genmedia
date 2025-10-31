
import os
import time
import glob
from google import genai
from google.genai import types
import mediapy as media
from dotenv import load_dotenv

load_dotenv()

# --- User Configuration ---
# Please fill in your Google Cloud Project ID and a GCS bucket for video output.
PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")
OUTPUT_GCS_BUCKET = os.environ.get("OUTPUT_GCS_BUCKET")

# --- Script ---

def show_video(gcs_uri: str, local_path: str, scene_name: str) -> None:
    """Downloads a video from GCS and displays it."""
    local_file_path = os.path.join(local_path, f"{scene_name}.mp4")
    
    # Using gsutil to copy the file. Make sure gsutil is authenticated.
    os.system(f"gsutil cp {gcs_uri} {local_file_path}")
    
    print(f"Video downloaded to {local_file_path}")
    # The mediapy.show_video function is for notebooks. In a script,
    # we'll just confirm download.
    # media.show_video(media.read_video(local_file_path), height=500)


def generate_video_for_scene(client, scene_dir, output_gcs_path, local_video_path):
    """Generates a video for a single scene."""
    print(f"Processing scene: {os.path.basename(scene_dir)}")
    
    image_path = os.path.join(scene_dir, "image-1.png")
    if not os.path.exists(image_path):
        print(f"  - image-1.png not found in {scene_dir}. Skipping.")
        return

    scene_name = os.path.basename(scene_dir)
    output_gcs_uri = f"{output_gcs_path}/{scene_name}.mp4"

    print(f"  - Generating video for {scene_name}...")
    
    img = types.Image.from_file(location=image_path)

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
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

    print(f"  - Video generation started. Operation: {operation}")
    print("  - Waiting for operation to complete...")

    while not operation.done:
        time.sleep(30)  # Poll every 30 seconds
        operation = client.operations.get(operation)
        print(f"  - Operation status: {operation}")

    if operation.response:
        generated_video_uri = operation.result.generated_videos[0].video.uri
        print(f"  - Video generated successfully: {generated_video_uri}")
        show_video(generated_video_uri, scene_dir, scene_name)
    else:
        print("  - Video generation failed or returned no response.")


def main():
    """Main function to generate videos for all scenes."""
    if not PROJECT_ID or PROJECT_ID == "[your-project-id]":
        print("Please set your PROJECT_ID in the script.")
        return

    if not OUTPUT_GCS_BUCKET or OUTPUT_GCS_BUCKET == "gs://[your-gcs-bucket]/videos":
        print("Please set your OUTPUT_GCS_BUCKET in the script.")
        return

    client = genai.Client(vertexai=True, project=PROJECT_ID, location=LOCATION)

    prompts_images_dir = "prompts-images"
    scene_dirs = [d for d in glob.glob(f"{prompts_images_dir}/*") if os.path.isdir(d)]

    for scene_dir in scene_dirs:
        generate_video_for_scene(client, scene_dir, OUTPUT_GCS_BUCKET, scene_dir)

    print("\nAll scenes processed.")

if __name__ == "__main__":
    main()
