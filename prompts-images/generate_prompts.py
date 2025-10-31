
"""Generates image prompts from scene descriptions in the 'scenes' directory."""

import os
import re
import glob
import logging

import config

SCENES_DIR = "scenes"

def generate_prompts(file_content, file_name):
    """Generates image prompts from the content of a scene file."""
    scenes = re.findall(r"### \*\*(Scene \d+:.*?)\*\*\n\n\*\*Setting:\*\*(.*?)\n\n\*\*Action/Visual:\*\*(.*?)\n\n", file_content, re.DOTALL)
    
    prompts = []
    for i, (scene_title, setting, action_visual) in enumerate(scenes):
        # Beginning of the scene
        prompt_start = f"""
A photorealistic shot of the beginning of {scene_title.strip()} from {file_name}.
The setting is {setting.strip()}.
The scene shows {action_visual.strip()}.
The image should be in a 16:9 format.
"""
        prompts.append(prompt_start)
        
        # End of the scene
        prompt_end = f"""
A photorealistic shot of the end of {scene_title.strip()} from {file_name}.
The setting is {setting.strip()}.
The scene shows the conclusion of {action_visual.strip()}.
The image should be in a 16:9 format.
"""
        prompts.append(prompt_end)
        
    return prompts

def main():
    """Main function to generate prompts for all scenes."""
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

    file_paths = glob.glob(os.path.join(SCENES_DIR, "*.md"))

    if not file_paths:
        logging.warning(f"No scene files found in the '{SCENES_DIR}' directory.")
        return

    output_dir = config.PROMPTS_IMAGES_DIR
    os.makedirs(output_dir, exist_ok=True)

    for file_path in file_paths:
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                file_name = os.path.basename(file_path)
                scene_name = os.path.splitext(file_name)[0]
                scene_dir = os.path.join(output_dir, scene_name)
                
                os.makedirs(scene_dir, exist_ok=True)
                    
                prompts = generate_prompts(content, file_name)
                
                with open(os.path.join(scene_dir, "prompts.md"), "w") as prompt_file:
                    for i, prompt in enumerate(prompts):
                        prompt_file.write(f"--- Prompt {i+1} ---\n")
                        prompt_file.write(prompt)
                        prompt_file.write("\n")
                logging.info(f"Generated prompts for scene: {scene_name}")

        except IOError as e:
            logging.error(f"Error processing file {file_path}: {e}")

if __name__ == "__main__":
    main()
