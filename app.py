"""
Streamlit app for AI-Powered Legal Document Summarization
"""
import streamlit as st
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from document_processor import DocumentProcessor
from legal_bert_summarizer import LegalBertSummarizer
from legal_analyzer import LegalAnalyzer

# Initialize components
processor = DocumentProcessor()
legal_summarizer = LegalBertSummarizer()
legal_analyzer = LegalAnalyzer()

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

        # Create tabs for different features
        tab1, tab2, tab3, tab4 = st.tabs(["📝 Summarization", "⚖️ Legal Analysis", "🔍 Insights", "📊 Statistics"])
        
        with tab1:
            st.header("Legal BERT Summarization")
            
            # Summarization options
            col1, col2 = st.columns(2)
            
            with col1:
                summarization_type = st.selectbox("Summarization Type", ["Extractive", "Abstractive"])
            
            with col2:
                if summarization_type == "Extractive":
                    num_sentences = st.slider("Number of sentences", 1, 10, 3)
                else:
                    max_length = st.slider("Max length", 50, 300, 150)
            
            if st.button("Generate Summary"):
                with st.spinner("Generating Legal BERT summary..."):
                    if summarization_type == "Extractive":
                        summary = legal_summarizer.extractive_summarize(
                            document_info["clean_text"], 
                            num_sentences=num_sentences
                        )
                        st.success("✅ Legal BERT Extractive Summary")
                    else:
                        summary = legal_summarizer.abstractive_summarize(
                            document_info["clean_text"], 
                            max_length=max_length
                        )
                        st.success("✅ Legal BERT-Enhanced Abstractive Summary")
                    
                    st.write(summary)
        
        with tab2:
            st.header("Legal Document Analysis")
            
            if st.button("Analyze Document"):
                with st.spinner("Analyzing legal document..."):
                    analysis = legal_analyzer.comprehensive_analysis(document_info["clean_text"])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("🌍 Jurisdiction Detection")
                        jurisdiction = analysis["jurisdiction"]
                        for country, score in jurisdiction.items():
                            if score > 0:
                                st.write(f"{country}: {score:.2%}")
                    
                    with col2:
                        st.subheader("⚠️ Risk Assessment")
                        risk_dist = analysis["risk_report"]["risk_distribution"]
                        st.write(f"🔴 High Risk: {risk_dist['high']} clauses")
                        st.write(f"🟡 Medium Risk: {risk_dist['medium']} clauses")
                        st.write(f"🟢 Low Risk: {risk_dist['low']} clauses")
                    
                    if analysis["risk_report"]["recommendations"]:
                        st.subheader("💡 Recommendations")
                        for rec in analysis["risk_report"]["recommendations"]:
                            st.write(f"• {rec}")
        
        with tab3:
            st.header("Legal BERT Insights")
            
            if st.button("Extract Legal Insights"):
                with st.spinner("Extracting insights with Legal BERT..."):
                    insights = legal_summarizer.get_legal_insights(document_info["clean_text"])
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.subheader("📈 Importance Levels")
                        st.write(f"High: {len(insights['high_importance'])} clauses")
                        st.write(f"Medium: {len(insights['medium_importance'])} clauses")
                        st.write(f"Low: {len(insights['low_importance'])} clauses")
                    
                    with col2:
                        st.subheader("📋 Clause Types Detected")
                        for clause_type, clauses in insights["clause_types"].items():
                            st.write(f"• {clause_type}: {len(clauses)} instances")
                    
                    if insights["high_importance"]:
                        st.subheader("🔥 High Importance Clauses")
                        for i, clause in enumerate(insights["high_importance"][:3], 1):
                            st.write(f"{i}. {clause[:200]}...")
        
        with tab4:
            st.header("📊 Document Statistics")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Word Count", document_info["word_count"])
                st.metric("Character Count", document_info["char_count"])
            
            with col2:
                st.metric("Entities Found", document_info["entities"].get("total_count", 0))
                st.metric("Parties Identified", len(document_info["parties"]))
            
            with col3:
                st.metric("Dates Found", len(document_info["dates_and_deadlines"]))
                legal_sections = sum(1 for v in document_info["legal_sections"].values() if v)
                st.metric("Legal Sections", legal_sections)
