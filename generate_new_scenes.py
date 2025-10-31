"Generates new image prompts for scenes based on ad copy concepts."

import os
import logging
import io

import config

# Scene data based on ad-copy.md concepts
SCENES_TO_GENERATE = {
    "11-pain-point-ad-scene": [
        {
            "title": "Scene 1: The Daily Struggle",
            "setting": "A person's messy home office, cluttered with papers and coffee cups.",
            "action": "The person looks overwhelmed, staring at a complex spreadsheet on their computer screen with a look of frustration."
        },
        {
            "title": "Scene 2: A Moment of Clarity",
            "setting": "The same home office, but now the person is using a new, sleek software interface on their screen.",
            "action": "The person's expression changes to one of relief and focus as they easily navigate the software. The clutter around them seems less daunting."
        },
        {
            "title": "Scene 3: The Successful Outcome",
            "setting": "A clean, organized home office. The sun is shining through the window.",
            "action": "The person is leaning back in their chair, smiling with satisfaction at a completed project on their screen. They take a relaxed sip of coffee."
        }
    ],
    "12-testimonial-ad-scene": [
        {
            "title": "Scene 1: The Skeptic",
            "setting": "A person is on their laptop, looking at a product page with a skeptical expression.",
            "action": "They are reading customer reviews, with a mix of positive and negative comments visible on the screen. They seem unsure whether to trust the product."
        },
        {
            "title": "Scene 2: The Leap of Faith",
            "setting": "The person is unboxing the product in their living room.",
            "action": "They open the box with a sense of curiosity. The product is revealed, looking just as advertised. A small, hopeful smile appears on their face."
        },
        {
            "title": "Scene 3: The Enthusiastic Advocate",
            "setting": "The person is now talking to a friend over video call, enthusiastically showing them the product.",
            "action": "They are passionately explaining how great the product is, pointing to its features. The friend on the screen looks impressed and intrigued."
        }
    ]
}

def generate_prompts_from_scene_data(scene_name, scene_data):
    """Generates image prompts from structured scene data."""
    prompts = []
    file_name = f"{scene_name}.md"
    
    for i, scene_part in enumerate(scene_data):
        scene_title = scene_part["title"]
        setting = scene_part["setting"]
        action_visual = scene_part["action"]
        
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

def run_scene_generation():
    """Main function to generate new scenes and prompts."""
    log_stream = io.StringIO()
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s', stream=log_stream)

    generated_files = []
    try:
        output_dir = config.GENERATED_SCENES_DIR
        os.makedirs(output_dir, exist_ok=True)

        for scene_name, scene_data in SCENES_TO_GENERATE.items():
            scene_dir = os.path.join(output_dir, scene_name)
            os.makedirs(scene_dir, exist_ok=True)
                
            prompts = generate_prompts_from_scene_data(scene_name, scene_data)
            
            prompt_file_path = os.path.join(scene_dir, "prompts.md")
            with open(prompt_file_path, "w") as prompt_file:
                for i, prompt in enumerate(prompts):
                    prompt_file.write(f"--- Prompt {i+1} ---\n")
                    prompt_file.write(prompt)
                    prompt_file.write("\n")
            logging.info(f"Generated prompts for scene: {scene_name}")
            generated_files.append(prompt_file_path)

    except IOError as e:
        logging.error(f"Error writing prompts: {e}")
    
    return generated_files, log_stream.getvalue()

if __name__ == "__main__":
    files, logs = run_scene_generation()
    print("--- LOGS ---")
    print(logs)
    print("--- GENERATED FILES ---")
    for f in files:
        print(f)
