
import streamlit as st

import config
from generate_ad_copy import run_ad_copy_generation
from generate_videos import run_video_generation
from generate_new_scenes import run_scene_generation

st.set_page_config(layout="wide")

st.title("Cymbal Pod Media Generation Workflow")

st.markdown("""
This application automates the generation of media assets for the Cymbal Pod brand.
Follow the steps below to generate ad copy, image prompts, and videos.
""")

# --- Configuration ---
st.header("Configuration")
st.markdown("Please provide your Google Cloud project details.")

project_id = st.text_input("Google Cloud Project ID", value=config.PROJECT_ID)
location = st.text_input("Google Cloud Location", value=config.LOCATION)
gcs_bucket = st.text_input("GCS Bucket for Video Output", value=config.OUTPUT_GCS_BUCKET)

# --- Workflow Steps ---
st.header("Workflow")

# 1. Generate Ad Copy
st.subheader("Step 1: Generate Ad Copy")
if st.button("Generate Ad Copy"):
    with st.spinner("Generating ad copy... This may take a moment."):
        ad_copy = run_ad_copy_generation(project_id, location)
        st.markdown("### Generated Ad Copy")
        st.markdown(ad_copy)

# 2. Generate New Image Prompts
st.subheader("Step 2: Generate New Image Prompts")
if st.button("Generate Image Prompts"):
    with st.spinner("Generating new scene prompts..."):
        generated_files, logs = run_scene_generation()
        st.markdown("### Logs")
        st.text(logs)
        st.markdown("### Generated Prompt Files")
        for file_path in generated_files:
            st.success(f"Generated: {file_path}")

# 3. Generate Videos
st.subheader("Step 3: Generate Videos")
st.markdown("This step will generate videos from the images in the `prompts-images` directory.")
if st.button("Generate Videos"):
    with st.spinner("Generating videos... This can take several minutes per video."):
        video_paths, logs = run_video_generation(project_id, location, gcs_bucket)
        st.markdown("### Logs")
        st.text(logs)
        st.markdown("### Generated Videos")
        if video_paths:
            for video_path in video_paths:
                st.video(video_path)
        else:
            st.warning("No videos were generated. Check the logs for details.")
