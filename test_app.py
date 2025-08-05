"""
Simplified test version of the Streamlit app
"""
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import streamlit as st
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

st.title("AI-Powered Legal Document Summarization - Test")

try:
    from document_processor import DocumentProcessor
    st.success("✅ DocumentProcessor imported successfully")
except Exception as e:
    st.error(f"❌ DocumentProcessor import failed: {e}")

try:
    from legal_bert_summarizer import LegalBertSummarizer
    st.success("✅ LegalBertSummarizer imported successfully")
except Exception as e:
    st.error(f"❌ LegalBertSummarizer import failed: {e}")

try:
    from legal_analyzer import LegalAnalyzer
    st.success("✅ LegalAnalyzer imported successfully")
except Exception as e:
    st.error(f"❌ LegalAnalyzer import failed: {e}")

# Test basic functionality
if st.button("Test Basic Functionality"):
    try:
        processor = DocumentProcessor()
        st.success("✅ DocumentProcessor initialized")
        
        legal_summarizer = LegalBertSummarizer()
        st.success("✅ LegalBertSummarizer initialized")
        
        legal_analyzer = LegalAnalyzer()
        st.success("✅ LegalAnalyzer initialized")
        
        st.success("🎉 All components working!")
        
    except Exception as e:
        st.error(f"❌ Initialization failed: {e}")
        import traceback
        st.code(traceback.format_exc())