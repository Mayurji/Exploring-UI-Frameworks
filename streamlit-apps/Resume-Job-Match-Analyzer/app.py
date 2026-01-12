import streamlit as st
import pandas as pd
from embeddings import EmbeddingManager
from database import JobDatabase
from llm_handler import LLMHandler
import uuid

# Page configuration
st.set_page_config(
    page_title="AI Resume Matcher (LLM Powered)",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for premium look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    .stTextInput>div>div>input {
        background-color: #31333F;
        color: white;
    }
    .stTextArea>div>div>textarea {
        background-color: #31333F;
        color: white;
        border: 1px solid #4a4d5e;
    }
    .stTextArea textarea:disabled {
        background-color: #4a4d5e !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }
    .job-card {
        background-color: #1e1e1e;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
        border: 1px solid #333;
    }
    .match-score {
        font-size: 24px;
        font-weight: bold;
        color: #4CAF50;
    }
    .extracted-info {
        background-color: #3d4051;
        padding: 15px;
        border-radius: 8px;
        font-family: 'Source Code Pro', monospace;
        font-size: 0.95em;
        margin-top: 10px;
        border: 1px solid #5a5e7a;
        color: #e0e0e0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize managers
@st.cache_resource
def get_managers():
    return EmbeddingManager(), JobDatabase(), LLMHandler()

embedding_manager, db, llm_handler = get_managers()

# Sidebar - Job Posting Management
with st.sidebar:
    st.title("💼 Job Management")
    st.subheader("Add New Job Posting")
    
    with st.form("job_form", clear_on_submit=True):
        job_title = st.text_input("Job Title")
        company_name = st.text_input("Company Name")
        job_desc = st.text_area("Job Description", height=200)
        submit_job = st.form_submit_button("Add Job Posting")
        
        if submit_job and job_title and job_desc:
            with st.spinner("Extracting skills/exp and generating embeddings..."):
                job_id = str(uuid.uuid4())
                # Extract skills and experience using LLM
                extracted_info = llm_handler.extract_skills_and_experience(job_desc)
                # Generate embedding for the extracted info
                embedding = embedding_manager.get_embeddings(extracted_info)[0]
                db.add_job_posting(job_id, job_title, company_name or "N/A", job_desc, extracted_info, embedding)
                st.success(f"Added: {job_title}")
                st.info(f"Extracted: {extracted_info}")

# Main Area - Resume Analysis
st.title("🎯 AI Resume Job Match Analyzer (LLM Powered)")
st.markdown("---")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📄 Upload Resume")
    uploaded_file = st.file_uploader("Choose a resume (PDF or Text)", type=["pdf", "txt"])
    
    resume_text = ""
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            resume_text = embedding_manager.extract_text_from_pdf(uploaded_file)
        else:
            resume_text = str(uploaded_file.read(), "utf-8")
        
        st.text_area("Extracted Text (Preview)", resume_text[:1000] + "...", height=300, disabled=True)

with col2:
    st.subheader("🔍 Match Results")
    if resume_text:
        if st.button("Analyze Match"):
            with st.spinner("Extracting skills/exp from resume..."):
                # Extract skills and experience from resume using LLM
                resume_extracted_info = llm_handler.extract_skills_and_experience(resume_text)
                st.markdown("**Extracted from Resume:**")
                st.markdown(f'<div class="extracted-info">{resume_extracted_info}</div>', unsafe_allow_html=True)
                
                with st.spinner("Analyzing match..."):
                    # Generate embedding for the resume's extracted info
                    resume_embedding = embedding_manager.get_embeddings(resume_extracted_info)[0]
                    results = db.query_jobs(resume_embedding, n_results=5)
                    
                    if results and results['ids'] and results['ids'][0]:
                        # Format results for display
                        match_data = []
                        for i in range(len(results['ids'][0])):
                            score = 1 - results['distances'][0][i]
                            job_title = results['metadatas'][0][i]['title']
                            company = results['metadatas'][0][i].get('company', 'N/A')
                            job_desc = results['metadatas'][0][i]['description']
                            
                            # Extract experience for the top match or all matches (limit to top 5)
                            with st.spinner(f"Extracting experience for {job_title}..."):
                                experience = llm_handler.extract_experience(job_desc)
                            
                            match_data.append({
                                "Job Title": job_title,
                                "Company": company,
                                "Match Score": f"{score:.2%}",
                                "Experience Required": experience
                            })
                        
                        df = pd.DataFrame(match_data)
                        st.table(df)
                        
                        # Highlight the best match
                        best_match = results['metadatas'][0][0]['title']
                        best_company = results['metadatas'][0][0].get('company', 'N/A')
                        best_score = 1 - results['distances'][0][0]
                        st.success(f"**Best Match:** {best_match} at **{best_company}** with a {best_score:.2%} similarity!")
                    else:
                        st.warning("No job postings found to match against. Please add some in the sidebar.")
    else:
        st.info("Please upload a resume to see matching job postings.")

st.markdown("---")
st.caption("Built with Streamlit, ChromaDB, and Sentence Transformers")
