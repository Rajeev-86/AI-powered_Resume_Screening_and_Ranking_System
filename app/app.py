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
job_description = st.text_area("Enter Job Description")

if uploaded_files and job_description:
    temp_files = []  # List to store temp file paths
    file_name_mapping = {}  # Dictionary to map temp file paths to original names

    for uploaded_file in uploaded_files:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp:
            temp.write(uploaded_file.read())  # Write uploaded content to temp file
            temp_files.append(temp.name)  # Store temp file path
            file_name_mapping[temp.name] = uploaded_file.name  # Map temp file to original name

    # Run ranking
    with st.spinner("🔍 Ranking resumes..."):
        ranked_results = rank_resumes(temp_files, job_description)

    # Display ranked resumes with original file names
    st.subheader("🏆 Ranked Resumes:")
    for rank, (resume_path, score) in enumerate(ranked_results, start=1):
        original_name = file_name_mapping.get(resume_path, "Unknown File")  # Get original name
        st.write(f"**{rank}. {original_name}** - Similarity Score: {score:.2f}")

    # Cleanup temp files
    for temp_path in temp_files:
        os.remove(temp_path)
