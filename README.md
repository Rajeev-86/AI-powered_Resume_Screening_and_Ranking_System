# AI Resume Screening and Ranking System

## Overview
The **AI Resume Screening and Ranking System** is an automated solution that leverages Natural Language Processing (NLP) and machine learning techniques to rank resumes based on their relevance to a given job description. This system improves efficiency in recruitment by reducing manual effort and bias while ensuring accurate candidate evaluation.

## Features
- **Automated Resume Parsing**: Extracts text from PDF and DOCX files.
- **Preprocessing and Text Cleaning**: Removes special characters, stopwords, and normalizes text.
- **Semantic Similarity Matching**: Uses SBERT embeddings to compute similarity scores between resumes and job descriptions.
- **User-Friendly Web Interface**: Built with Streamlit for easy resume uploads and ranking visualization.

## Installation
### Prerequisites
Ensure you have Python 3.8+ installed.

### Steps
1. Clone the repository:
   ```sh
   git clone https://github.com/Rajeev-86/AI-powered_Resume_Screening_and_Ranking_System.git
   cd AI-powered_Resume_Screening_and_Ranking_System
   ```
2. Install dependencies:
   ```sh
   pip install -r src/requirements.txt
   ```
3. Run the application:
   ```sh
   streamlit run app/app.py
   ```

## Usage
1. Upload multiple resumes (PDF/DOCX) via the web interface.
2. Provide a job description.
3. The system processes the resumes, ranks them based on similarity, and displays the results.

## Technologies Used
- **Python** (Core programming language)
- **Streamlit** (Web application framework)
- **PyMuPDF, pdfplumber, python-docx** (Resume text extraction)
- **NLTK** (Text preprocessing)
- **SBERT (Sentence-BERT)** (Semantic similarity computation)

## Future Enhancements
- Improve OCR for scanned PDFs.
- Integrate support for additional file formats (TXT, JSON, etc.).
- Enhance the ranking algorithm with deep learning models.

## Acknowledgments
Special thanks to the open-source NLP community for providing valuable tools and frameworks that made this project possible.

