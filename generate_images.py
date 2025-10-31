from google import genai
from google.genai import types
import base64
import os
import re

from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")



def generate(prompt, output_path, images_references=[]):
  client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location=LOCATION,
  )
  
  msg1_text1 = types.Part.from_text(text=prompt)


  model = "gemini-2.5-flash-image"
  contents = [
    types.Content(
      role="user",
      parts=[
        msg1_text1
      ]
    ),
  ]
  for reference_image in images_references:
      contents[0].parts.append(
        types.Part.from_bytes(data=open(reference_image, "rb").read(), mime_type="image/png"))

  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 32768,
    response_modalities = ["TEXT", "IMAGE"],
    safety_settings = [types.SafetySetting(
      category="HARM_CATEGORY_HATE_SPEECH",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_DANGEROUS_CONTENT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
      threshold="OFF"
    ),types.SafetySetting(
      category="HARM_CATEGORY_HARASSMENT",
      threshold="OFF"
    )],
  )

  for chunk in client.models.generate_content_stream(
    model = model,
    contents = contents,
    config = generate_content_config,
    ):
    if chunk.parts and chunk.parts[0].inline_data:
        with open(output_path, 'wb') as f:
            f.write(chunk.parts[0].inline_data.data)

if __name__ == '__main__':
    script_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(script_dir, "prompts-images")
    images_dir = os.path.join(script_dir, "images")
    
    images_references = []
    # Collect all generated protagonist and product images as references
    if os.path.exists(images_dir):
        for image_file in os.listdir(images_dir):
            if image_file.startswith("protagonist_") or image_file.startswith("product_"):
                images_references.append(os.path.join(images_dir, image_file))
    
    if not images_references:
        print("Warning: No reference images found for protagonist or product. Consistency may be affected.")
    
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
                            generate(prompt.strip(), output_path, images_references)
                            print(f"Image saved to {output_path}")
                        except Exception as e:
                            print(f"Error generating image for prompt {i+1} in {scene_dir_name}: {e}")
