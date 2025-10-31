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

product_description = {
    "name": "The Cymbal Pod",
    "description": "a single person, urban transport vehicle that hovers silently and moves quietly through the world.",
    "aesthetics": "Neo-Minimalism & Organic Futurism. The design is defined by smooth, pebble-like forms and a low-profile silhouette that minimizes visual clutter. Surfaces utilize matte, non-reflective finishes (e.g., recycled polymers) for a muted, sophisticated look. Integrated, subtle lighting systems are used instead of harsh external lights.",
    "mood_color_palette": "Calm, serene, focused, and sophisticated. The feeling is one of being centered and undisturbed amidst urban chaos. Color Palette: Muted & Earthy. Mist Gray (Primary body color, matte finish), Deep Jade (Accent for integrated system lighting and UI), Terra Cotta Accent (Subtle interior touch for fabric piping or controls), Soft Linen (Main interior fabric).",
}

# Create a detailed prompt for the product
product_prompt = f"A photorealistic image of {product_description['name']}, {product_description['description']}. The design is {product_description['aesthetics']}. The mood and color palette are {product_description['mood_color_palette']}. The background is white."

# Create a directory for the images
output_dir = "images"
os.makedirs(output_dir, exist_ok=True)

# Define the output path for the product image
product_output_path = os.path.join(output_dir, "product_cymbal_pod.png")

print(f"Generating image for product: {product_description['name']}")
print(f"Prompt: {product_prompt}")

# Generate the product image
generate(product_prompt, None, product_output_path)
print(f"Image saved to {os.path.abspath(product_output_path)}")

reference_image = product_output_path


angle = ["front-facing", "side profile", "three-quarter view", "close-up"]

for angle_option in angle:
  prompt = f"A photorealistic with {angle_option} The background is white."

  # Define the output path
  output_path = os.path.join(output_dir, f"product_cymbal_pod-{angle_option}.png")

  print(f"Generating image for product: {output_path}")
  print(f"Prompt: {prompt}")

  # Generate the image

  generate(prompt, reference_image, output_path)
  print(f"Image saved to {os.path.abspath(output_path)}")
