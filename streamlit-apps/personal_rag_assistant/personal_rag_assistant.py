import streamlit as st
import os
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
from rag_system import RAGEngine

st.set_page_config(page_title="Personal RAG Assistant", layout="wide")

# --- Authentication ---
with open('auth.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# Login widget
authenticator.login()

if st.session_state["authentication_status"]:
    # --- Main Application ---
    with st.sidebar:
        st.write(f'Welcome *{st.session_state["name"]}*')
        authenticator.logout('Logout', 'main')
        st.divider()
    
    st.title("Personal RAG Assistant")

    # Initialize engine once per session
    if "engine" not in st.session_state:
        st.session_state.engine = RAGEngine()

    engine = st.session_state.engine

    with st.sidebar:
        st.header("Settings")
        uploaded_file = st.file_uploader("Upload PDF", type="pdf")
        
        if st.button("Index Document") and uploaded_file:
            with st.spinner("Processing..."):
                temp_path = f"temp_{uploaded_file.name}"
                with open(temp_path, "wb") as f:
                    f.write(uploaded_file.getvalue())
                
                engine.process_pdf(temp_path)
                os.remove(temp_path)
                st.success("Document added to local storage!")

        st.divider()

        if st.button("Clear Collection", type="primary"):
            if engine.clear_all_data():
                st.session_state.messages = []
                st.success("Collection cleared!")
                st.rerun()

    # --- Chat Interface ---
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask about your document..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            chain = engine.get_qa_chain()
            if chain:
                with st.spinner("Analyzing..."):
                    response = chain.invoke(prompt)
                    st.markdown(response["result"])
                    st.session_state.messages.append({"role": "assistant", "content": response["result"]})
            else:
                st.warning("The database is empty. Please upload a document.")

elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
elif st.session_state["authentication_status"] is None:
    st.warning('Please enter your username and password')