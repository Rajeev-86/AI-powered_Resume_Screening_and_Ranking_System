import fitz  # Using PyMuPDF as it's faster and would be better if there are thousand+ resumes to be ranked
import pytesseract  # If the resume is a scanned image
from pdf2image import convert_from_path
from docx import Document  # Using python-docx because it extracts with proper formatting and maintains text order
import pdfplumber
from pathlib import Path
import re
import nltk
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import os

# Check if stopwords are already downloaded
try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

stop_words = set(stopwords.words("english"))

def extract_text_from_resume(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc]).strip()
    return text

def extract_text_from_image_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = "\n".join([pytesseract.image_to_string(img).strip() for img in images])
    text = re.sub(r"\s+", " ", text).strip()  # Normalize spaces
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text.strip() for para in doc.paragraphs]).strip()
    return text

def is_pdf_scanned(pdf_path):
    """Returns True if the PDF is scanned (image-based), False if it's text-based."""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            if page.extract_text():
                return False  # Found text, so it's not scanned
    return True  # No text found, it's a scanned PDF

def extract_text(file_path):
    ext = Path(file_path).suffix.lower()

    if ext == ".pdf":
        if is_pdf_scanned(file_path):
            return extract_text_from_image_pdf(file_path)  # Use OCR
        else:
            return extract_text_from_resume(file_path)  # Use PyMuPDF
    elif ext == ".docx":
        return extract_text_from_docx(file_path)
    else:
        raise ValueError("Unsupported file format. Only PDF and DOCX are supported.")
        
def preprocess_text(text, remove_stopwords=True):
    """Lowercases text, removes special characters, and optionally removes stopwords."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    
    if remove_stopwords:
        text = " ".join(word for word in text.split() if word not in stop_words)

    return text

# Initialize spell checker
spell = SpellChecker()

def correct_text(text):
    """Corrects spelling errors in the text."""
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    words = text.split()
    unknown_words = spell.unknown(words)
    corrected_words = [spell.correction(word) if word in unknown_words and spell.correction(word) else word for word in words]

    return " ".join(corrected_words)

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight and efficient

def rank_resumes(resume_files, job_description):
    """Ranks multiple resumes based on similarity to job description."""
    job_embedding = model.encode([job_description], normalize_embeddings=True)

    ranked_resumes = []
    
    for original_name, file_path in resume_files:  # Unpacking tuple (original_name, temp_path)
        try:
            resume_text = extract_text(file_path)  # Corrected variable name
        except Exception as e:
            print(f"Error processing {original_name}: {e}")
            continue  # Skip this resume
            
        resume_text = preprocess_text(resume_text)
        resume_text = correct_text(resume_text)
        
        resume_embedding = model.encode([resume_text], normalize_embeddings=True)
        similarity_score = float(resume_embedding @ job_embedding.T)  # Dot product instead of cosine similarity 
        
        ranked_resumes.append((original_name, similarity_score))  # Store original name, not temp file name

    # Sort resumes by similarity score in descending order
    ranked_resumes.sort(key=lambda x: x[1], reverse=True)

    return ranked_resumes  # Return ranked results

# Debugging Step
print("jai_hind")
