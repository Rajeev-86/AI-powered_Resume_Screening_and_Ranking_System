import streamlit as st
import os
import sys
import tempfile

# To import the source module from src
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)

from src.source import extract_text, preprocess_text, correct_text, rank_resumes

st.title("📄 AI Resume Ranking System")

# Upload resumes
uploaded_files = st.file_uploader("📂 Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)

# Job description input
job_description = st.text_area("📝 Enter Job Description")

# Process when both files and job description are provided
if uploaded_files and job_description:
    st.subheader("🔄 Processing Resumes...")
    
    # Save uploaded files temporarily
    temp_files = []
    for uploaded_file in uploaded_files:
        temp_path = os.path.join(tempfile.gettempdir(), uploaded_file.name)
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.read())
        temp_files.append(temp_path)

    # Run ranking with a spinner
    with st.spinner("🔍 Ranking resumes..."):
        ranked_results = rank_resumes(temp_files, job_description)

    # Display ranked resumes
    st.subheader("🏆 Ranked Resumes:")
    for rank, (resume_name, score) in enumerate(ranked_results, start=1):
        st.markdown(f"**{rank}. {resume_name}** - 🎯 Similarity Score: `{score:.2f}`")
