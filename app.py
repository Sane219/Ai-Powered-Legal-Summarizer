"""
Streamlit app for AI-Powered Legal Document Summarization
"""
import streamlit as st
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from document_processor import DocumentProcessor
from extractive_summarizer import ExtractiveSummarizer
from abstractive_summarizer import AbstractiveSummarizer

# Initialize components
processor = DocumentProcessor()
extractive_summarizer = ExtractiveSummarizer()
abstractive_summarizer = AbstractiveSummarizer()

# Streamlit UI Configurations
st.set_page_config(page_title="AI Legal Document Summarizer", page_icon="⚖️", layout="wide")

# App Title
st.title("AI-Powered Legal Document Summarization")

# Upload documents
uploaded_file = st.file_uploader("Upload a legal document", type=["pdf", "docx", "txt"])

if uploaded_file is not None:
    # Process file
    file_path = os.path.join("data", uploaded_file.name)
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    # Extract and display text
    st.header("Document Text")
    document_info = processor.process_document(file_path)

    if "error" in document_info:
        st.error(f"Error in processing document: {document_info['error']}")
    else:
        st.text_area("Extracted Text", document_info["clean_text"], height=200)

        # Summarization Options
        summarization_type = st.selectbox("Select Summarization Type", ["Extractive", "Abstractive"])
        
        if summarization_type == "Extractive":
            st.header("Extractive Summary")
            extractive_summary = extractive_summarizer.summarize(document_info["clean_text"])
            st.write(extractive_summary)
        else:
            st.header("Abstractive Summary")
            abstractive_summary = abstractive_summarizer.summarize(document_info["clean_text"])
            st.write(abstractive_summary)
