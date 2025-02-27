import fitz  # Using PyMuPDF as it's faster and would be better if there are thousand+ resumes to be ranked
import pytesseract  # If the resume is scanned image
from pdf2image import convert_from_path
from docx import Document  #using python-docs because extracts with proper formatting and maintains the text order
import pdfplumber
from pathlib import Path
import re
import nltk
from nltk.corpus import stopwords
from spellchecker import SpellChecker
from sentence_transformers import SentenceTransformer


def extract_text_from_resume(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join([page.get_text("text") for page in doc])
    return text

def extract_text_from_image_pdf(pdf_path):
    images = convert_from_path(pdf_path)
    text = "\n".join([pytesseract.image_to_string(img) for img in images])
    return text

def extract_text_from_docx(docx_path):
    doc = Document(docx_path)
    text = "\n".join([para.text for para in doc.paragraphs])
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
        
# Download stopwords if not already downloaded
nltk.download("stopwords")
stop_words = set(stopwords.words("english"))

def preprocess_text(text, remove_stopwords=True):

    # Convert to lowercase
    text = text.lower()

    # Remove special characters, punctuation, and extra spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Remove stopwords if enabled
    if remove_stopwords:
        text = " ".join(word for word in text.split() if word not in stop_words)

    return text

# Initialize spell checker
spell = SpellChecker()

def correct_text(text):

    # Convert to lowercase
    text = text.lower()

    # Remove special characters and extra spaces
    text = re.sub(r"[^a-zA-Z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize text into words
    words = text.split()

    # Correct misspelled words
    corrected_words = [spell.correction(word) if word in spell.unknown(words) and spell.correction(word) is not None else word for     word in words]

    # Join corrected words back into a sentence
    corrected_text = " ".join(corrected_words)

    return corrected_text

# Load SBERT model
model = SentenceTransformer('all-MiniLM-L6-v2')  # Lightweight and efficient

def rank_resumes(resume_files, job_description):
    """Ranks multiple resumes based on similarity to job description."""
    job_embedding = model.encode([job_description])

    ranked_resumes = []
    
    for file in resume_files:
        resume_text = extract_text(file)
        resume_text = preprocess_text(resume_text)
        resume_text = correct_text(resume_text)
        
        resume_embedding = model.encode([resume_text])
        similarity_score = cosine_similarity(resume_embedding, job_embedding)[0][0]
        
        ranked_resumes.append((file.name, similarity_score))

    # Sort resumes by similarity score in descending order
    ranked_resumes.sort(key=lambda x: x[1], reverse=True)
    

print("jai_hind") # Debug step
