import streamlit as st
import os
import sys
from io import BytesIO

# Import functions from src
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
from src.source import extract_text, preprocess_text, correct_text, rank_resumes

st.title("AI Resume Ranking System")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_description = st.text_area("Enter Job Description")

if uploaded_files and job_description:
    resumes = []  # Store extracted text for ranking

    for uploaded_file in uploaded_files:
        file_bytes = uploaded_file.read()  # Read file into memory
        file_stream = BytesIO(file_bytes)  # Convert to BytesIO object

        # Extract text directly from file stream
        extracted_text = extract_text(file_stream, file_type=uploaded_file.type)  
        resumes.append((uploaded_file.name, extracted_text))  

    # Run ranking
    with st.spinner("🔍 Ranking resumes..."):
        ranked_results = rank_resumes(resumes, job_description)  # Process in-memory data

    # Display ranked resumes
    st.subheader("🏆 Ranked Resumes:")
    for rank, (resume_name, score) in enumerate(ranked_results, start=1):
        st.write(f"**{rank}. {resume_name}** - Similarity Score: {score:.2f}")
