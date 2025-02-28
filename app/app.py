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
    temp_files = []  # List to store tuples (original_name, temp_file_path)

    for uploaded_file in uploaded_files:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp:
            temp.write(uploaded_file.read())  # Write uploaded content to temp file
            temp_files.append((uploaded_file.name, temp.name))  # Store tuple (original_name, temp_path)

    # Run ranking
    with st.spinner("🔍 Ranking resumes..."):
        ranked_results = rank_resumes(temp_files, job_description)  # Pass tuples

    # Display ranked resumes using original names
    st.subheader("🏆 Ranked Resumes:")
    for rank, (original_name, score) in enumerate(ranked_results, start=1):
        st.write(f"**{rank}. {original_name}** - Similarity Score: {score:.2f}")

    # Cleanup temp files
    for _, temp_path in temp_files:
        os.remove(temp_path)
