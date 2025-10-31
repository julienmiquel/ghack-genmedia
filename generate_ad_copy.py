
"""Generates ad copy using the Gemini model based on brand and marketing principles."""

import logging
import os
from google import genai
from google.genai import types

import config

def run_ad_copy_generation(project_id, location):
    """Generates ad copy and returns it as a string."""

    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    if not project_id or project_id == "[your-project-id]":
        error_msg = "Please set your Google Cloud Project ID."
        logging.error(error_msg)
        return error_msg

    try:
        client = genai.Client(
            vertexai=True,
            project=project_id,
            location=location,
        )

        # Read context files
        logging.info("Reading context files...")
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

        logging.info("--- Generating Ad Copy ---")
        response_chunks = []
        for chunk in client.models.generate_content_stream(
            model=config.GEMINI_MODEL,
            contents=contents,
            config=generate_content_config,
        ):
            if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
                response_chunks.append(chunk.text)
        
        logging.info("--- End of Ad Copy Generation ---")
        return "".join(response_chunks)

    except FileNotFoundError as e:
        error_msg = f"Error: {e}. Make sure the context files (brand.md, prompts/ad-copy.md, prompts/story-telling.md) are in the correct location."
        logging.error(error_msg)
        return error_msg
    except Exception as e:
        error_msg = f"An unexpected error occurred: {e}"
        logging.error(error_msg)
        return error_msg

if __name__ == "__main__":
    # This part is for direct execution of the script, not used by the Streamlit app.
    import argparse
    parser = argparse.ArgumentParser(description="Generate ad copy for the Cymbal Pod brand.")
    parser.add_argument("--project_id", type=str, default=config.PROJECT_ID, help="Google Cloud Project ID.")
    parser.add_argument("--location", type=str, default=config.LOCATION, help="Google Cloud Location.")
    args = parser.parse_args()

    generated_copy = run_ad_copy_generation(args.project_id, args.location)
    print(generated_copy)
