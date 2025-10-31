from google import genai
from google.genai import types
import os

# --- User Configuration ---
# Please fill in your Google Cloud Project ID and Location.
PROJECT_ID = "[your-project-id]"  # Replace with your Project ID
LOCATION = "us-central1"

def generate():
    """Generates ad copy using the Gemini model."""

    if not PROJECT_ID or PROJECT_ID == "[your-project-id]":
        print("Please set your PROJECT_ID in the script.")
        return

    client = genai.Client(
        vertexai=True,
        project=PROJECT_ID,
        location=LOCATION,
    )

    # Read context files
    with open("brand.md", "r") as f:
        brand_context = f.read()
    with open("prompts/ad-copy.md", "r") as f:
        ad_copy_context = f.read()
    with open("prompts/story-telling.md", "r") as f:
        story_telling_context = f.read()

    # Construct the prompt
    prompt = f"""
You are a world-class marketing expert specializing in creating compelling ad copy for innovative tech products.

Your task is to generate a variety of ad copy for the Cymbal Pod, a new personal urban transport vehicle. You must strictly adhere to the brand identity and target audience defined below.

**1. Brand and Product Context:**

{brand_context}

**2. Ad Copy and Storytelling Principles:**

Use the following guides on ad copy and storytelling to inform your writing style and strategy. Do not simply repeat the templates, but apply the core principles to the Cymbal Pod brand.

{ad_copy_context}

{story_telling_context}

**3. Your Assignment:**

Now, generate a comprehensive set of ad copy for the Cymbal Pod. The copy should be ready for a marketing campaign targeting the 'Conscious Urban Professional'.

Create ad copy for the following categories, providing 2-3 variations for each:

a. **Pain Point Ad Copy:** Focus on the stress, noise, and wasted time of urban commuting.

b. **Feature-Benefit Ad Copy:** Translate features like 'silent, hovering' and 'personal sanctuary' into tangible benefits for the target audience.

c. **Testimonial Ad Copy:** Write a believable testimonial from our protagonist, Lena Chen, that reflects her values and experience.

d. **Storytelling Ad Copy:** Create a short, narrative-driven ad that tells a story about how the Cymbal Pod transforms a person's day.

Ensure all copy is sophisticated, calm, and focused, aligning with the brand's mood. The call-to-action should be subtle and refined, such as "Reserve your sanctuary" or "Begin your journey."

Format the output clearly with markdown headings for each category and variation.
"""

    model = "gemini-2.5-flash-preview-09-2025"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=prompt)
            ]
        )
    ]
    tools = [
        types.Tool(google_search=types.GoogleSearch()),
    ]

    generate_content_config = types.GenerateContentConfig(
        temperature=1,
        top_p=0.95,
        max_output_tokens=65535,
        safety_settings=[
            types.SafetySetting(
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="BLOCK_NONE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="BLOCK_NONE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="BLOCK_NONE"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="BLOCK_NONE"
            )
        ],
        tools=tools,
        thinking_config=types.ThinkingConfig(
            thinking_budget=-1,
        ),
    )

    print("--- Generating Ad Copy ---\
")

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if not chunk.candidates or not chunk.candidates[0].content or not chunk.candidates[0].content.parts:
            continue
        print(chunk.text, end="")

    print("\n--- End of Ad Copy Generation ---")

if __name__ == "__main__":
    generate()
