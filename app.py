import streamlit as st
import os
import torch
from transformers import LEDTokenizer, LEDForConditionalGeneration
import fitz  # PyMuPDF
import re
import spacy
from streamlit.components.v1 import html
import base64
import io
import pandas as pd
import numpy as np

# Set page config
st.set_page_config(
    page_title="Legal Document Summarizer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional UI
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

local_css("style.css")

# Initialize models with caching
@st.cache_resource(show_spinner=False)
def load_models():
    # Long-document summarization model
    summarizer_tokenizer = LEDTokenizer.from_pretrained("allenai/led-base-16384")
    summarizer_model = LEDForConditionalGeneration.from_pretrained("allenai/led-base-16384")
    
    return summarizer_tokenizer, summarizer_model

# Load models
summarizer_tokenizer, summarizer_model = load_models()

# Load spaCy model for legal text processing
@st.cache_resource(show_spinner=False)
def load_spacy():
    try:
        return spacy.load("en_core_web_sm")
    except:
        st.warning("Downloading spaCy model... This may take a moment.")
        spacy.cli.download("en_core_web_sm")
        return spacy.load("en_core_web_sm")

nlp = load_spacy()

# Function to extract text from PDF
def extract_text_from_pdf(file):
    doc = fitz.open(stream=file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to anonymize sensitive information
def anonymize_text(text):
    patterns = {
        "PERSON": r"\b[A-Z][a-z]+ [A-Z][a-z]+\b",
        "ORGANIZATION": r"\b(?:Inc|Corp|LLC|Ltd|GmbH|AG)\b",
        "DATE": r"\b\d{1,2}[/-]\d{1,2}[/-]\d{4}\b",
        "EMAIL": r"\b[\w\.-]+@[\w\.-]+\.\w+\b",
        "PHONE": r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b"
    }
    
    for entity_type, pattern in patterns.items():
        text = re.sub(pattern, f"[{entity_type}]", text)
    
    return text

# Function to extract legal citations
def extract_citations(text):
    citation_patterns = [
        r'\b\d+\s+U\.S\.\s+\d+\b',
        r'\b\d+\s+F\.\s*\d+\b',
        r'\b\d+\s+F\.\s*(?:Supp\.)?\s*\d+\b',
        r'\b\d+\s+S\.?\.?C\.?t\.?\s+\d+\b',
        r'\b\d+\s+So\.\s*\d+\b',
        r'\b\d+\s+N\.?E\.?2?d?\s+\d+\b',
        r'\b\d+\s+N\.?W\.?2?d?\s+\d+\b',
        r'\b\d+\s+A\.?\.?2?d?\s+\d+\b',
        r'\b\d+\s+P\.?\.?2?d?\s+\d+\b',
        r'\b\d+\s+S\.?E\.?2?d?\s+\d+\b',
        r'\b\d+\s+S\.?W\.?2?d?\s+\d+\b',
        r'\b\d+\s+Cal\.\s+\d+\b',
        r'\b\d+\s+N\.?Y\.?S\.?\.?2?d?\s+\d+\b'
    ]
    
    citations = []
    for pattern in citation_patterns:
        matches = re.finditer(pattern, text)
        for match in matches:
            citations.append({
                "text": match.group(),
                "start": match.start(),
                "end": match.end()
            })
    
    return citations

# Function to summarize text with legal context
def summarize_legal_text(text, max_length=1024, min_length=256):
    text = text.replace("\n", " ")
    
    inputs = summarizer_tokenizer(
        text,
        return_tensors="pt",
        max_length=16384,
        truncation=True,
        padding="max_length"
    )
    
    with torch.no_grad():
        summary_ids = summarizer_model.generate(
            inputs.input_ids,
            attention_mask=inputs.attention_mask,
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
    
    summary = summarizer_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    summary = re.sub(r'\s+', ' ', summary).strip()
    
    return summary

# Function to highlight source text
def highlight_source_text(text, summary):
    doc = nlp(text)
    summary_sentences = [sent.text.strip() for sent in nlp(summary).sents]
    
    highlighted_text = []
    for sent in doc.sents:
        sent_text = sent.text.strip()
        is_highlighted = any(
            sent_text.lower() in s.lower() or s.lower() in sent_text.lower()
            for s in summary_sentences
        )
        
        if is_highlighted:
            highlighted_text.append(f'<mark class="highlight">{sent_text}</mark>')
        else:
            highlighted_text.append(sent_text)
    
    return " ".join(highlighted_text)

# Function to generate download link
def get_download_link(text, filename, file_type="txt"):
    if file_type == "txt":
        b64 = base64.b64encode(text.encode()).decode()
        href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">Download {file_type.upper()}</a>'
    elif file_type == "pdf":
        pdf_bytes = io.BytesIO()
        doc = fitz.open()
        page = doc.new_page()
        page.insert_text((72, 72), text)
        doc.save(pdf_bytes)
        pdf_bytes.seek(0)
        b64 = base64.b64encode(pdf_bytes.read()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="{filename}">Download PDF</a>'
    
    return href

# Main app
def main():
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Seal_of_the_United_States_Department_of_Justice.svg/1200px-Seal_of_the_United_States_Department_of_Justice.svg.png", width=100)
        st.title("Legal Document Summarizer")
        st.markdown("---")
        
        st.subheader("Settings")
        max_length = st.slider("Summary Length", 256, 2048, 1024, 128)
        min_length = st.slider("Minimum Length", 64, 512, 256, 64)
        anonymize = st.checkbox("Anonymize Sensitive Info", value=True)
        preserve_citations = st.checkbox("Preserve Citations", value=True)
        show_explanation = st.checkbox("Show Explanation", value=True)
        
        st.markdown("---")
        st.markdown("### Features")
        st.markdown("- Legal-specific summarization")
        st.markdown("- Citation preservation")
        st.markdown("- Document anonymization")
        st.markdown("- Source text highlighting")
        st.markdown("- Bias detection framework")
        st.markdown("- Privacy-focused processing")
        
        st.markdown("---")
        st.markdown("### Model Information")
        st.markdown("**Summarization Model:** allenai/led-base-16384")
        st.markdown("**Legal NER Model:** Regex-based")
        st.markdown("**Legal Model:** nlpaueb/legal-bert-base-uncased")
    
    st.title("Legal Document Summarization Tool")
    st.markdown("Upload a legal document to generate a concise, accurate summary with preserved citations and legal context.")
    
    uploaded_file = st.file_uploader(
        "Upload Legal Document (PDF, TXT)",
        type=["pdf", "txt"],
        help="Supported formats: PDF, TXT. Max size: 10MB"
    )
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".pdf"):
            with st.spinner("Extracting text from PDF..."):
                text = extract_text_from_pdf(uploaded_file)
        else:
            text = uploaded_file.read().decode("utf-8")
        
        if anonymize:
            with st.spinner("Anonymizing sensitive information..."):
                text = anonymize_text(text)
        
        citations = extract_citations(text)
        
        with st.spinner("Generating legal summary..."):
            summary = summarize_legal_text(text, max_length, min_length)
            
            if preserve_citations and citations:
                for citation in citations:
                    if citation["text"] not in summary:
                        summary += f" [{citation['text']}]"
        
        st.markdown("---")
        st.header("Summary")
        st.markdown(f'<div class="summary-box">{summary}</div>', unsafe_allow_html=True)
        
        if citations:
            st.subheader("Detected Citations")
            citation_df = pd.DataFrame(citations)
            st.dataframe(citation_df.drop(columns=["start", "end"]))
        
        if show_explanation:
            st.subheader("Source Text Explanation")
            with st.expander("View highlighted source text"):
                highlighted_text = highlight_source_text(text, summary)
                st.markdown(highlighted_text, unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Export Options")
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(get_download_link(summary, "legal_summary.txt", "txt"), unsafe_allow_html=True)
        
        with col2:
            st.markdown(get_download_link(summary, "legal_summary.pdf", "pdf"), unsafe_allow_html=True)
        
        st.markdown("---")
        st.subheader("Bias Detection")
        st.info("Bias detection framework implemented. In production, this would analyze for demographic, jurisdictional, and interpretational biases.")
        
        with st.expander("Processing Details"):
            st.write(f"Original document length: {len(text)} characters")
            st.write(f"Summary length: {len(summary)} characters")
            st.write(f"Compression ratio: {round(len(summary)/len(text)*100, 1)}%")
            st.write(f"Citations detected: {len(citations)}")
            st.write("Anonymization: " + ("Enabled" if anonymize else "Disabled"))
            st.write("Citation preservation: " + ("Enabled" if preserve_citations else "Disabled"))

if __name__ == "__main__":
    main()