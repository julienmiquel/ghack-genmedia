import os
import re
from google.cloud import aiplatform

def generate_image(prompt, output_path):
  # Ensure GOOGLE_CLOUD_PROJECT is set
  project_id = os.environ.get("GOOGLE_CLOUD_PROJECT")
  if not project_id:
      raise ValueError("GOOGLE_CLOUD_PROJECT environment variable is not set.")

  aiplatform.init(project=project_id)
  model = aiplatform.ImageGenerationModel.from_pretrained("imagegeneration@006")

  response = model.generate_images(
      prompt=prompt,
      number_of_images=1,
      seed=1,
      guidance_scale=10,
      width=1920,
      height=1080,
  )

  for i, image_bytes in enumerate(response.images):
      with open(output_path, 'wb') as f:
          f.write(image_bytes._image_bytes)


prompts_dir = "/Users/julienmiquel/dev/ghack-genmedia/prompts-images"

for scene_dir_name in os.listdir(prompts_dir):
    scene_dir_path = os.path.join(prompts_dir, scene_dir_name)
    if os.path.isdir(scene_dir_path):
        prompts_file_path = os.path.join(scene_dir_path, "prompts.md")
        if os.path.exists(prompts_file_path):
            with open(prompts_file_path, 'r') as f:
                content = f.read()
                prompts = re.findall(r"--- Prompt \d+ ---\n(.*?)(?=\n--- Prompt \d+ ---|\Z)", content, re.DOTALL)
                for i, prompt in enumerate(prompts):
                    output_path = os.path.join(scene_dir_path, f"image-{i+1}.png")
                    print(f"Generating image for prompt {i+1} in {scene_dir_name}...")
                    try:
                        generate_image(prompt.strip(), output_path)
                        print(f"Image saved to {output_path}")
                    except Exception as e:
                        print(f"Error generating image for prompt {i+1} in {scene_dir_name}: {e}")
