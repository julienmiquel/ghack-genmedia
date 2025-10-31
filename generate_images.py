from google import genai
from google.genai import types
import base64
import os
import re

def generate(prompt, output_path, images_references=[]):
  client = genai.Client(
      vertexai=False,
      api_key=os.environ.get("GOOGLE_CLOUD_API_KEY"),
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
    prompts_dir = "/Users/julienmiquel/dev/ghack-genmedia/prompts-images"
    
    images_references = []
    angle = ["front-facing", "side profile", "three-quarter", "over-the-shoulder", "close-up"]

    for angle_option in angle:

      # Define the output path
      if os.path.exists(f"./protagonist_anya_sharma-{angle_option}.png"):
        output_path = f"./protagonist_anya_sharma-{angle_option}.png"
        images_references.append(output_path)

      if os.path.exists(f"product_cymbal_pod-{angle_option}.png"):
        output_path = f"product_cymbal_pod-{angle_option}.png"
        images_references.append(output_path)
       
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
