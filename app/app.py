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
    temp_files = {}  # Dictionary to store temp file paths mapped to original names

    for uploaded_file in uploaded_files:
        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp:
            temp.write(uploaded_file.read())  # Write uploaded content to temp file
            temp_files[temp.name] = uploaded_file.name  # Store temp file path with original name

    # Run ranking
    with st.spinner("🔍 Ranking resumes..."):
        ranked_results = rank_resumes(list(temp_files.keys()), job_description)

    # Display ranked resumes using original names
    st.subheader("🏆 Ranked Resumes:")
    for rank, (temp_path, score) in enumerate(ranked_results, start=1):
        original_name = temp_files[temp_path]  # Get original filename
        st.write(f"**{rank}. {original_name}** - Similarity Score: {score:.2f}")

    # Cleanup temp files
    for temp_path in temp_files.keys():
        os.remove(temp_path)
