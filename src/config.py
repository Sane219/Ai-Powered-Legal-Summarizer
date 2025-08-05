"""
Configuration settings for Legal Document Summarization Tool
"""
import os
from pathlib import Path

# Base paths
BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"

# Model configurations
MODELS = {
    "extractive": {
        "name": "facebook/bart-large-cnn",
        "max_length": 1024,
        "min_length": 50,
        "do_sample": False
    },
    "abstractive": {
        "name": "microsoft/DialoGPT-large",
        "max_length": 512,
        "min_length": 100,
        "temperature": 0.7
    },
    "legal_bert": {
        "name": "nlpaueb/legal-bert-base-uncased",
        "max_length": 512
    }
}

# Legal document processing settings
LEGAL_SECTIONS = [
    "parties",
    "obligations",
    "termination",
    "indemnity", 
    "confidentiality",
    "intellectual_property",
    "governing_law",
    "dispute_resolution",
    "payment_terms",
    "liability",
    "force_majeure",
    "definitions"
]

# NER settings for legal entities
LEGAL_ENTITIES = [
    "PERSON",
    "ORG", 
    "DATE",
    "MONEY",
    "PERCENT",
    "LAW",
    "LEGAL_ROLE",
    "CONTRACT_TERM"
]

# Summarization levels
SUMMARY_LEVELS = {
    "brief": {
        "max_sentences": 3,
        "max_words": 150,
        "focus": ["parties", "key_obligations", "important_dates"]
    },
    "standard": {
        "max_sentences": 8,
        "max_words": 400,
        "focus": ["parties", "obligations", "termination", "key_terms", "dates"]
    },
    "detailed": {
        "max_sentences": 15,
        "max_words": 800,
        "focus": "all_sections"
    }
}

# File processing settings
SUPPORTED_FORMATS = [".pdf", ".docx", ".txt"]
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

# Streamlit UI settings
UI_CONFIG = {
    "page_title": "AI Legal Document Summarizer",
    "page_icon": "⚖️",
    "layout": "wide",
    "sidebar_state": "expanded"
}

# Legal clause keywords for detection
CLAUSE_KEYWORDS = {
    "indemnity": ["indemnify", "indemnification", "hold harmless", "defend"],
    "termination": ["terminate", "termination", "end", "expire", "dissolution"],
    "confidentiality": ["confidential", "non-disclosure", "proprietary", "trade secret"],
    "liability": ["liable", "liability", "damages", "loss", "responsible"],
    "intellectual_property": ["copyright", "trademark", "patent", "intellectual property", "IP"],
    "governing_law": ["governing law", "jurisdiction", "applicable law"],
    "force_majeure": ["force majeure", "act of god", "unforeseeable circumstances"]
}

# Environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
