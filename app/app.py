import streamlit as st
import os
import pandas as pd
import sys
# To import the source module from src
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
from src.source import extract_text, preprocess_text, correct_text, rank_resumes

st.title("AI Resume Ranking System")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_description = st.text_area("Enter Job Description")
        
if uploaded_files and job_description:
    st.header("Ranking Resumes")

    resumes = []
    for file in uploaded_files:
        resumes.append(file)

    # Rank resumes
    scores = rank_resumes(job_description, resumes)

    # Display scores
    results = pd.DataFrame({"Resume": [file.name for file in uploaded_files], "Score": score })
    results = results.sort_values(by="Score", ascending=False)

    st.write(results)
