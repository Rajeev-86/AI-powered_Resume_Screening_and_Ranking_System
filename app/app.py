import streamlit as st
import os
import tempfile
import sys

# Import the source module
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
from src.source import extract_text, preprocess_text, correct_text, rank_resumes

st.title("AI Resume Ranking System")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_description = st.text_area("Enter Job Description")

if uploaded_files and job_description:
    resume_files = []  # List to store (original_name, temp_path) tuples

    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp:
            temp.write(uploaded_file.read())  # Save uploaded file to temp storage
            resume_files.append((uploaded_file.name, temp.name))  # Store original name and temp file path

    # Run ranking
    with st.spinner("🔍 Ranking resumes..."):
        ranked_results = rank_resumes(resume_files, job_description)  # Passing list of (name, path)

    # Display ranked resumes
    st.subheader("🏆 Ranked Resumes:")
    for rank, (original_name, score) in enumerate(ranked_results, start=1):
        st.write(f"**{rank}. {original_name}** - Similarity Score: {score:.2f}")

    # Cleanup temp files
    for _, temp_path in resume_files:
        os.remove(temp_path)
