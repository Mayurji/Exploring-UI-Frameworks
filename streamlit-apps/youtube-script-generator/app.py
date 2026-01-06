import streamlit as st

from tools.generator import generate_script
from tools.generator import generate_titles
from tools.generator import generate_hooks

st.set_page_config(page_title="YouTube Script Generator", layout="wide")

st.title("🎬 YouTube Script Generator (Open Source)")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Select Model", ["llama3.2", "qwen", "gemma3"])
    clear_btn = st.button("Clear History")

topic = st.text_input("Video Topic")
tone = st.selectbox("Tone", ["Educational", "Conversational", "Storytelling", "Technical"])
duration = st.slider("Duration (minutes)", 1, 15, 5)

if st.button("Generate"):
    if not topic:
        st.warning("Please enter a topic")
    else:
        with st.spinner("Generating content..."):
            st.subheader("📌 Titles")
            st.write(generate_titles(topic, model_name=model_choice))

            st.subheader("⚡ Hooks")
            st.write(generate_hooks(topic, model_name=model_choice))

            st.subheader("📝 Full Script")
            st.write(generate_script(topic, tone, duration, model_name=model_choice))
