import streamlit as st
import os
import tempfile
import sys
# To import the source module from src
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
from src.source import extract_text, preprocess_text, correct_text, rank_resumes

st.title("AI Resume Ranking System")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
MAX_FILE_SIZE_MB = 5  # Example: 5MB limit
if any(uploaded_file.size > MAX_FILE_SIZE_MB * 1024 * 1024 for uploaded_file in uploaded_files):
    st.error(f"❌ One or more files exceed {MAX_FILE_SIZE_MB}MB. Please upload smaller files.")

job_description = st.text_area("Enter Job Description")

if uploaded_files and job_description:
    try:
    temp_files = []
    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp:
            temp.write(uploaded_file.read())
            temp_files.append(temp.name)

    try:
        with st.spinner("🔍 Ranking resumes..."):
            ranked_results = rank_resumes(temp_files, job_description)
    
        st.subheader("🏆 Ranked Resumes:")
        for rank, (resume_name, score) in enumerate(ranked_results, start=1):
            st.write(f"**{rank}. {resume_name}** - Similarity Score: {score:.2f}")

except Exception as e:
    st.error(f"⚠️ Error processing resumes: {e}")

finally:
    for temp_path in temp_files:
        os.remove(temp_path)
