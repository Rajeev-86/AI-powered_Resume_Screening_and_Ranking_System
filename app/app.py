import streamlit as st
import os
import sys
import io
# Import the source module
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(BASE_DIR)
from src.source import extract_text, preprocess_text, rank_resumes

# Custom CSS to add a background image
st.markdown(
    """
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), 
                    url("https://images4.alphacoders.com/133/thumb-1920-1336369.jpeg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("📄 AI Resume Screening & Ranking System")

# Upload Resumes
uploaded_files = st.file_uploader("Upload Resumes", type=["pdf", "docx"], accept_multiple_files=True)

# Input Job Description
job_description = st.text_area("Enter Job Description", placeholder="Paste the job description here...")

if uploaded_files and job_description:
    # Convert uploaded files into {filename: BytesIO} dictionary
    resume_data = {file.name: io.BytesIO(file.read()) for file in uploaded_files}

    # Rank resumes
    with st.spinner("🔍 Ranking resumes..."):
        ranked_results = rank_resumes(resume_data, job_description)

    # Display results
    st.subheader("🏆 Ranked Resumes:")
    for rank, (filename, score) in enumerate(ranked_results, start=1):
        st.write(f"**{rank}. {filename}** - Similarity Score: {score:.2f}")
