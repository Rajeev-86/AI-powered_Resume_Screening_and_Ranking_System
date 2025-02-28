import streamlit as st
import os
import sys
import io

# Import the source module
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
from src.source import extract_text, preprocess_text, correct_text, rank_resumes

st.title("AI Resume Ranking System")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_description = st.text_area("Enter Job Description")
if uploaded_files:
    resume_data = {file.name: io.BytesIO(file.read()) for file in uploaded_files}

    # Now pass `resume_data` (dictionary of {filename: file_content}) to `rank_resumes`
    ranked_results = rank_resumes(resume_data, job_description)

    # Display results
    st.subheader("🏆 Ranked Resumes:")
    for rank, (filename, score) in enumerate(ranked_results, start=1):
        st.write(f"**{rank}. {filename}** - Similarity Score: {score:.2f}")
