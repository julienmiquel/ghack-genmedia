
# Gemini Interaction Guidelines for Cymbal Pod Media Generation Project

This document provides context and guidelines for the Gemini model when interacting with the Cymbal Pod media generation project.

## Project Context

The primary goal of this project is to leverage generative AI to create various media assets (ad copy, image prompts, videos) for the Cymbal Pod, a silent, hovering single-person urban transport vehicle. The project aims to maintain a consistent brand identity and messaging across all generated content.

## Key Files and Directories

Gemini should be aware of the following important files and directories:

- `brand.md`: Contains the core brand guidelines, aesthetics, values, mood, color palette, and target audience for the Cymbal Pod. This document is crucial for all content generation.
- `prompts/ad-copy.md`: Provides templates and guidance for generating effective ad copy.
- `prompts/story-telling.md`: Offers principles and insights into effective storytelling for marketing.
- `scenes/`: Contains markdown files describing various scenes, which are used to generate image prompts.
- `prompts-images/`: Stores generated image prompts and associated images for existing scenes.
- `generated-scenes/`: A directory where newly generated image prompts for scenes are stored.
- `generate_videos.py`: Script for generating videos from images.
- `generate_new_scenes.py`: Script for generating new image prompts based on ad copy concepts.
- `generate_ad_copy.py`: Script for generating ad copy using the Gemini model.
- `requirements.txt`: Lists all Python dependencies for the project.
- `README.md`: General project documentation and usage instructions.

## Gemini's Role

Gemini's role in this project includes, but is not limited to:
- Assisting with the development and refinement of generative programs.
- Generating new content (ad copy, image prompts, etc.) based on project guidelines.
- Providing explanations and documentation for the codebase.
- Troubleshooting and debugging scripts.

## Guidelines for Interaction

1.  **Adherence to Brand Guidelines:** Always refer to `brand.md` for all content generation tasks. Ensure that generated ad copy, scene descriptions, and any other creative output align with the Cymbal Pod's aesthetics, values, mood, color palette, and target audience.
2.  **Leverage Provided Resources:** Utilize the principles and templates outlined in `prompts/ad-copy.md` and `prompts/story-telling.md` when generating ad copy or developing narrative-driven content.
3.  **Tool Usage:** Make effective use of the available tools (e.g., `read_file`, `write_file`, `run_shell_command`, `run_gcloud_command`) to perform tasks efficiently.
4.  **Clarity and Specificity:** If a request is ambiguous or lacks sufficient detail, ask clarifying questions to ensure the generated output meets the user's expectations.
5.  **Code Consistency:** When modifying or creating new Python scripts, adhere to the existing coding style and conventions found in the project.
6.  **Documentation:** Keep documentation up-to-date, especially for new scripts or significant changes to existing ones.
