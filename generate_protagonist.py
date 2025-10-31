import os
from google import genai
from google.genai import types
from dotenv import load_dotenv

load_dotenv()

PROJECT_ID = os.environ.get("PROJECT_ID")
LOCATION = os.environ.get("LOCATION")

def generate(prompt, reference_image, output_path):
  client = genai.Client(
      vertexai=True,
      project=PROJECT_ID,
      location=LOCATION,
  )

  msg1_text1 = genai.types.Part.from_text(text=prompt)

  model_name = "gemini-2.5-flash-image"
  contents = [
    genai.types.Content(
      role="user",
      parts=[
        msg1_text1
      ]
    ),
  ]

  model = "gemini-2.5-flash-image"
  if reference_image:
    contents = [
      types.Content(
        role="user",
        parts=[
          msg1_text1,
          types.Part.from_bytes(data=open(reference_image, "rb").read(), mime_type="image/png")
        ]
      ),
    ]
  else:
    if reference_image:
      contents = [
        types.Content(
          role="user",
          parts=[
            msg1_text1            
          ]
        ),
      ]
  generate_content_config = types.GenerateContentConfig(
    temperature = 1,
    top_p = 0.95,
    max_output_tokens = 32768,
    response_modalities = ["IMAGE"],
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

protagonist_description = {
    "name": "Anya Sharma",
    "age": 32,
    "occupation": "Architect specializing in sustainable urban development",
    "appearance": "Medium height, athletic build, with sharp, intelligent eyes. She often wears practical yet stylish clothing in muted tones, reflecting her appreciation for functional design. Her hair is usually tied back in a neat bun, emphasizing her focused demeanor.",
}

# Create a detailed prompt
appearance = protagonist_description['appearance']
occupation = protagonist_description['occupation']
name = protagonist_description['name']
age = protagonist_description['age']

prompt = f"A photorealistic portrait of {name}, a {age}-year-old {occupation}. {appearance}. She has a focused and thoughtful expression. The background is white."

# Create a directory for the images
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

# Define the output path
output_path = os.path.join(output_dir, f"protagonist_anya_sharma.png")

print(f"Generating image for protagonist: {name}")
print(f"Prompt: {prompt}")

# Generate the image
generate(prompt, None, output_path)
print(f"Image saved to {os.path.abspath(output_path)}")
reference_image = output_path


angle = ["front-facing", "side profile", "three-quarter view", "over-the-shoulder", "close-up"]

for angle_option in angle:
  prompt = f"A photorealistic portrait with {angle_option} of {name}, a {age}-year-old {occupation}. {appearance}. She has a focused and thoughtful expression. The background is white."

  # Define the output path
  output_path = os.path.join(output_dir, f"protagonist_anya_sharma-{angle_option}.png")

  print(f"Generating image for protagonist: {name}")
  print(f"Prompt: {prompt}")

  # Generate the image

  generate(prompt, reference_image, output_path)
  print(f"Image saved to {os.path.abspath(output_path)}")
