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
    temp_files = {}  # Store {temp_path: original_filename}

    for uploaded_file in uploaded_files:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as temp:
            temp.write(uploaded_file.read())
            temp_files[os.path.basename(temp.name)] = uploaded_file.name  # Store only the basename

    
    try:
        with st.spinner("🔍 Ranking resumes..."):
            ranked_results = rank_resumes(list(temp_files.keys()), job_description)  # Pass list of temp filenames
    
        st.subheader("🏆 Ranked Resumes:")
        for rank, (temp_path, score) in enumerate(ranked_results, start=1):
            temp_basename = os.path.basename(temp_path)  # Extract filename only
            original_name = temp_files.get(temp_basename, "Unknown")  # Match with stored filenames
            st.write(f"**{rank}. {original_name}** - Similarity Score: {score:.2f}")

    
    except Exception as e:
        st.error(f"⚠️ Error processing resumes: {e}")
    
    finally:
        for temp_path in temp_files.keys():
            os.remove(temp_path)  # Cleanup temp files
