
# GenMedia: Cymbal Pod Brand Media Generation

This project contains a suite of Python scripts for generating various media assets for the Cymbal Pod brand, a silent, hovering single-person urban transport vehicle.

## Overview

The scripts leverage generative AI to create:
- **Ad Copy:** High-quality, on-brand advertising copy.
- **Image Prompts:** Detailed prompts for generating scene-based images.
- **Videos:** Short animated videos from images.

## Getting Started

### Prerequisites

- Python 3.7+
- A Google Cloud Platform (GCP) project with the Vertex AI API enabled.
- `gsutil` command-line tool authenticated with your GCP account.

### Installation

1. **Clone the repository (if you haven't already):**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Install the required Python packages:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure your GCP Project ID:**

   You must fill in your Google Cloud Project ID in the following scripts:
   - `generate_videos.py`
   - `generate_ad_copy.py`

   Open each file and replace `"[your-project-id]"` with your actual GCP Project ID.

## Usage

### Generating Ad Copy

This script uses the Gemini model to generate various types of ad copy based on the brand guidelines and marketing principles.

**To run:**
```bash
python3 generate_ad_copy.py
```

The generated ad copy will be printed to the console.

### Generating New Image Prompts

This script creates new sets of image prompts based on predefined scene concepts. The prompts are saved in the `generated-scenes` directory.

**To run:**
```bash
python3 generate_new_scenes.py
```

### Generating Videos

This script generates a short video for each scene defined in the `prompts-images` directory. It uses the first image of each scene as the input for video generation.

**Before running:**

- Make sure you have filled in your `PROJECT_ID` and a valid GCS bucket path in `generate_videos.py`.

**To run:**
```bash
python3 generate_videos.py
```

The generated videos will be saved to your specified GCS bucket and then downloaded to the `videos` directory.

## Workflow

This section outlines a typical workflow for generating media assets using the scripts in this project.

1.  **Generate New Image Prompts (Optional):**
    Use `python3 generate_new_scenes.py` to create new scene descriptions and corresponding image prompts. These will be saved in the `generated-scenes` directory. This step is useful if you want to create new visual narratives.

2.  **Generate Images (External Step):**
    The image prompts generated in the previous step (or existing ones in `prompts-images/`) are designed to be used with an external image generation tool (e.g., Imagen, Midjourney, DALL-E) to create the actual image files (e.g., `image-1.png`, `image-2.png`). These images should then be placed in the appropriate scene directories (e.g., `prompts-images/your-new-scene/`).

3.  **Generate Videos:**
    Once you have a set of images for a scene, use `python3 generate_videos.py` to generate short animated videos. This script takes the first image of each scene as input and animates it. Ensure your `PROJECT_ID` and GCS bucket are configured in the script.

4.  **Generate Ad Copy:**
    Independently, you can use `python3 generate_ad_copy.py` to generate marketing ad copy tailored to the Cymbal Pod brand. This script leverages the brand guidelines and marketing principles to produce compelling text. Ensure your `PROJECT_ID` is configured in the script.

