import streamlit as st
from source import extract_text, preprocess_text, correct_text, rank_resumes

st.title("AI Resume Ranking System")

uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)
job_description = st.text_area("Enter Job Description")

if uploaded_files and job_description:
    ranked_results = rank_resumes(uploaded_files, job_description)
    
    st.subheader("Ranked Resumes:")
    for rank, (resume_name, score) in enumerate(ranked_results, start=1):
        st.write(f"**{rank}. {resume_name}** - Similarity Score: {score:.2f}")
