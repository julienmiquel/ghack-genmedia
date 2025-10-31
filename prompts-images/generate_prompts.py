import os
import re

def generate_prompts(file_content, file_name):
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

file_paths = [
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/1-testimonial-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/10-emotional-story-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/2-seasonal-holiday-promotion-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/3-pain-point-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/4-discount-sale-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/5-fomo-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/6-feature-benefit-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/7-social-proof-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/8-authentic-story-ad-copy-scene.md",
    "/Users/julienmiquel/dev/ghack-genmedia/scenes/9-suspenseful-story-ad-copy-scene.md",
]

output_dir = "/Users/julienmiquel/dev/ghack-genmedia/prompts-images"

if not os.path.exists(output_dir):
    os.makedirs(output_dir)

for file_path in file_paths:
    with open(file_path, 'r') as f:
        content = f.read()
        file_name = os.path.basename(file_path)
        scene_name = os.path.splitext(file_name)[0]
        scene_dir = os.path.join(output_dir, scene_name)
        
        if not os.path.exists(scene_dir):
            os.makedirs(scene_dir)
            
        prompts = generate_prompts(content, file_name)
        
        with open(os.path.join(scene_dir, "prompts.md"), "w") as prompt_file:
            for i, prompt in enumerate(prompts):
                prompt_file.write(f"--- Prompt {i+1} ---\n")
                prompt_file.write(prompt)
                prompt_file.write("\n")