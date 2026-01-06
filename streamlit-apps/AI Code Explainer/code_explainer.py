import streamlit as st
from llm_engine import explain_code

st.set_page_config(page_title="Local AI Code Explainer", layout="wide")

st.title("📂 Local AI Code Explainer")
st.markdown("Analyze your code privately using local LLMs (Ollama).")

# Sidebar for configuration
with st.sidebar:
    st.header("Settings")
    model_choice = st.selectbox("Select Model", ["llama3.2", "qwen", "gemma3"])
    clear_btn = st.button("Clear History")

# Main Interface
col1, col2 = st.columns(2)

with col1:
    st.subheader("Input Code")
    code_input = st.text_area("Paste your code here:", height=400, placeholder="def hello_world(): ...")
    
    uploaded_file = st.file_uploader("Or upload a file", type=["py", "js", "cpp", "java"])
    if uploaded_file:
        code_input = uploaded_file.read().decode("utf-8")

with col2:
    st.subheader("Explanation")
    if st.button("Explain Code") and code_input:
        with st.spinner("Analyzing..."):
            response_container = st.empty()
            full_response = ""
            
            # Stream the response to the UI
            for chunk in explain_code(code_input, model_choice):
                full_response += chunk['message']['content']
                response_container.markdown(full_response + "▌")
            
            response_container.markdown(full_response)
    else:
        st.info("Enter code and click 'Explain' to see results.")