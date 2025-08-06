"""
Streamlit app for AI-Powered Legal Document Summarization - Clean Professional Version
"""
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)
import streamlit as st
import os
import sys
# MUST be the first Streamlit command
st.set_page_config(
    page_title="AI Legal Document Summarizer",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://github.com/Sane219/Ai-Powered-Legal-Summarizer',
        'Report a bug': "https://github.com/Sane219/Ai-Powered-Legal-Summarizer/issues",
        'About': "AI-Powered Legal Document Summarizer v1.0"
    }
)
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))
try:
    from src.document_processor import DocumentProcessor
    from src.legal_bert_summarizer import LegalBertSummarizer
    from src.legal_analyzer import LegalAnalyzer
except ImportError:
    # Try with src prefix for different deployment environments
    try:
        from src.document_processor import DocumentProcessor
        from src.legal_bert_summarizer import LegalBertSummarizer
        from src.legal_analyzer import LegalAnalyzer
    except ImportError as e:
        st.error(f"Error importing modules: {e}")
        st.info("Please ensure all dependencies are installed correctly.")
        st.stop()
# Clean, Professional CSS
PROFESSIONAL_CSS = """
/* Clean Professional Legal Theme */
/* Main app styling */
.stApp {
    background-color: #f8f9fa;
    color: #2c3e50;
}
/* Remove default streamlit padding */
.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}
/* Professional header styling */
.professional-header {
    background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
    color: white;
    padding: 3rem 2rem;
    border-radius: 12px;
    margin-bottom: 2rem;
    text-align: center;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}
.professional-header h1 {
    font-size: 2.5rem;
    font-weight: 300;
    margin-bottom: 0.5rem;
    letter-spacing: -0.5px;
}
.professional-header p {
    font-size: 1.1rem;
    opacity: 0.9;
    margin-bottom: 1.5rem;
}
/* Feature badges */
.feature-badge {
    background: rgba(255, 255, 255, 0.15);
    color: white;
    padding: 0.5rem 1rem;
    border-radius: 20px;
    margin: 0.25rem;
    display: inline-block;
    font-size: 0.9rem;
    backdrop-filter: blur(10px);
}
/* Clean card styling */
.clean-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border: 1px solid #e9ecef;
    transition: all 0.2s ease;
}
.clean-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    transform: translateY(-1px);
}
/* Card with accent border */
.accent-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border-left: 4px solid #3498db;
}
/* Professional button styling */
.stButton > button {
    background: #3498db;
    color: white;
    border: none;
    border-radius: 6px;
    padding: 0.75rem 1.5rem;
    font-weight: 500;
    font-size: 0.95rem;
    transition: all 0.2s ease;
    box-shadow: 0 2px 4px rgba(52, 152, 219, 0.2);
}
.stButton > button:hover {
    background: #2980b9;
    transform: translateY(-1px);
    box-shadow: 0 4px 8px rgba(52, 152, 219, 0.3);
}
/* Clean upload area */
.upload-area {
    border: 2px dashed #bdc3c7;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    background: #f8f9fa;
    margin-bottom: 1rem;
    transition: all 0.2s ease;
}
.upload-area:hover {
    border-color: #3498db;
    background: #ecf0f1;
}
/* Tab styling */
.stTabs > div > div > div > div {
    background: #f8f9fa;
    color: #2c3e50;
    border-radius: 8px 8px 0 0;
    border: 1px solid #e9ecef;
    border-bottom: none;
    font-weight: 500;
    transition: all 0.2s ease;
}
.stTabs > div > div > div > div:hover {
    background: #e9ecef;
}
.stTabs > div > div > div > div[data-selected="true"] {
    background: white;
    color: #3498db;
    border-bottom: 2px solid #3498db;
}
/* Clean text area */
.stTextArea > div > div > textarea {
    border: 1px solid #e9ecef;
    border-radius: 6px;
    background: #f8f9fa;
    font-family: 'Segoe UI', system-ui, sans-serif;
    transition: all 0.2s ease;
}
.stTextArea > div > div > textarea:focus {
    border-color: #3498db;
    background: white;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}
/* Clean selectbox */
.stSelectbox > div > div > select {
    border: 1px solid #e9ecef;
    border-radius: 6px;
    background: white;
    padding: 0.5rem;
    transition: all 0.2s ease;
}
.stSelectbox > div > div > select:focus {
    border-color: #3498db;
    box-shadow: 0 0 0 3px rgba(52, 152, 219, 0.1);
}
/* Clean slider */
.stSlider > div > div > div > div {
    background: #e9ecef;
    border-radius: 4px;
}
.stSlider > div > div > div > div > div {
    background: #3498db;
    border: 2px solid white;
    border-radius: 50%;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
}
/* Sidebar styling */
.css-1d391kg {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
/* Professional metrics */
.metric-card {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border: 1px solid #e9ecef;
    transition: all 0.2s ease;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
.metric-value {
    font-size: 2rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0.5rem 0;
}
.metric-label {
    color: #7f8c8d;
    font-size: 0.9rem;
    font-weight: 500;
}
/* Risk visualization */
.risk-card {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
    border: 1px solid #e9ecef;
}
.risk-high {
    border-left: 4px solid #e74c3c;
}
.risk-medium {
    border-left: 4px solid #f39c12;
}
.risk-low {
    border-left: 4px solid #27ae60;
}
.risk-bar {
    height: 8px;
    background: #ecf0f1;
    border-radius: 4px;
    margin: 0.5rem 0;
    overflow: hidden;
}
.risk-fill-high {
    height: 100%;
    background: #e74c3c;
    border-radius: 4px;
}
.risk-fill-medium {
    height: 100%;
    background: #f39c12;
    border-radius: 4px;
}
.risk-fill-low {
    height: 100%;
    background: #27ae60;
    border-radius: 4px;
}
/* Success messages */
.success-message {
    background: #d4edda;
    color: #155724;
    border: 1px solid #c3e6cb;
    border-radius: 6px;
    padding: 1rem;
    margin: 1rem 0;
}
.error-message {
    background: #f8d7da;
    color: #721c24;
    border: 1px solid #f5c6cb;
    border-radius: 6px;
    padding: 1rem;
    margin: 1rem 0;
}
.warning-message {
    background: #fff3cd;
    color: #856404;
    border: 1px solid #ffeaa7;
    border-radius: 6px;
    padding: 1rem;
    margin: 1rem 0;
}
/* Clean typography */
h1, h2, h3, h4, h5, h6 {
    color: #2c3e50;
    font-weight: 600;
    line-height: 1.2;
}
h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }
/* Responsive design */
@media (max-width: 768px) {
    .professional-header {
        padding: 2rem 1rem;
    }
    
    .professional-header h1 {
        font-size: 2rem;
    }
    
    .clean-card {
        padding: 1rem;
        margin-bottom: 1rem;
    }
    
    .upload-area {
        padding: 1.5rem;
    }
}
/* Remove default streamlit spacing */
div[data-testid="stVerticalBlock"] > div[style*="flex-direction: column"] > div[data-testid="stVerticalBlock"] {
    gap: 0.5rem;
}
/* Clean spinner */
.stSpinner > div {
    border-color: #3498db;
    border-top-color: transparent;
}
/* Professional table styling */
.stDataFrame {
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
.stDataFrame > div > div > table {
    border-collapse: collapse;
    width: 100%;
}
.stDataFrame > div > div > table th {
    background: #f8f9fa;
    color: #2c3e50;
    padding: 0.75rem;
    text-align: left;
    font-weight: 600;
    border-bottom: 2px solid #e9ecef;
}
.stDataFrame > div > div > table td {
    padding: 0.75rem;
    border-bottom: 1px solid #f1f3f4;
}
.stDataFrame > div > div > table tr:hover {
    background: #f8f9fa;
}
"""
# Load professional CSS
def load_css():
    st.markdown(f'<style>{PROFESSIONAL_CSS}</style>', unsafe_allow_html=True)
# Initialize components with error handling
@st.cache_resource
def initialize_components():
    try:
        processor = DocumentProcessor()
        legal_summarizer = LegalBertSummarizer()
        legal_analyzer = LegalAnalyzer()
        return processor, legal_summarizer, legal_analyzer
    except Exception as e:
        st.error(f"Error initializing components: {e}")
        return None, None, None
# Clean UI Components
def create_professional_header():
    """Create a clean, professional header"""
    st.markdown("""
    <div class="professional-header">
        <h1>⚖️ AI Legal Document Summarizer</h1>
        <p>Transform complex legal documents into clear, actionable insights</p>
        <div>
            <span class="feature-badge">📄 PDF, DOCX, TXT Support</span>
            <span class="feature-badge">🤖 Legal BERT Powered</span>
            <span class="feature-badge">⚡ Real-time Analysis</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
def create_clean_upload():
    """Create a clean file upload section"""
    st.markdown("""
    <div class="upload-area">
        <h3 style="color: #2c3e50; margin-bottom: 1rem;">📁 Upload Your Legal Document</h3>
        <p style="color: #7f8c8d; margin-bottom: 1rem;">
            Supported formats: PDF, DOCX, TXT | Max file size: 10MB
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Choose a file", 
        type=["pdf", "docx", "txt"],
        label_visibility="collapsed",
        key="file_uploader"
    )
    
    if uploaded_file:
        # File info display
        file_size = len(uploaded_file.getvalue()) / 1024 / 1024  # MB
        st.markdown(f"""
        <div class="clean-card">
            <h4 style="color: #2c3e50; margin-bottom: 1rem;">📄 File Information</h4>
            <p><strong>Name:</strong> {uploaded_file.name}</p>
            <p><strong>Size:</strong> {file_size:.2f} MB</p>
            <p><strong>Type:</strong> {uploaded_file.type}</p>
        </div>
        """, unsafe_allow_html=True)
    
    return uploaded_file
def create_clean_tabs():
    """Create clean, professional tabs"""
    tab1, tab2, tab3, tab4 = st.tabs([
        "📝 Summarization", 
        "⚖️ Legal Analysis", 
        "🔍 Insights", 
        "📊 Statistics"
    ])
    return tab1, tab2, tab3, tab4
def create_clean_card(title, content, icon="📄", accent_color="#3498db"):
    """Create a clean, professional card"""
    st.markdown(f"""
    <div class="accent-card" style="border-left-color: {accent_color};">
        <h3 style="color: {accent_color}; margin-bottom: 1rem;">{icon} {title}</h3>
        <div style="background: #f8f9fa; padding: 1rem; border-radius: 6px;">
            {content}
        </div>
    </div>
    """, unsafe_allow_html=True)
def create_clean_metrics(stats):
    """Create clean metric cards"""
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; color: #3498db; margin-bottom: 0.5rem;">📝</div>
            <div class="metric-value">{stats['word_count']}</div>
            <div class="metric-label">Words</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; color: #e74c3c; margin-bottom: 0.5rem;">👥</div>
            <div class="metric-value">{len(stats['parties'])}</div>
            <div class="metric-label">Parties</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div style="font-size: 2.5rem; color: #f39c12; margin-bottom: 0.5rem;">📊</div>
            <div class="metric-value">{stats['entities'].get('total_count', 0)}</div>
            <div class="metric-label">Entities</div>
        </div>
        """, unsafe_allow_html=True)
def create_clean_risk_visualization(risk_data):
    """Create clean risk assessment visualization"""
    st.markdown("""
    <div class="clean-card">
        <h3 style="color: #e74c3c; margin-bottom: 1.5rem;">⚠️ Risk Assessment</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="risk-card risk-high">
            <div style="color: #e74c3c; font-weight: 600; margin-bottom: 0.5rem;">🔴 High Risk</div>
            <div class="risk-bar">
                <div class="risk-fill-high" style="width: {min(risk_data['high'] * 10, 100)}%;"></div>
            </div>
            <div style="font-size: 1.5rem; font-weight: 600; color: #2c3e50;">{risk_data['high']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="risk-card risk-medium">
            <div style="color: #f39c12; font-weight: 600; margin-bottom: 0.5rem;">🟡 Medium Risk</div>
            <div class="risk-bar">
                <div class="risk-fill-medium" style="width: {min(risk_data['medium'] * 10, 100)}%;"></div>
            </div>
            <div style="font-size: 1.5rem; font-weight: 600; color: #2c3e50;">{risk_data['medium']}</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="risk-card risk-low">
            <div style="color: #27ae60; font-weight: 600; margin-bottom: 0.5rem;">🟢 Low Risk</div>
            <div class="risk-bar">
                <div class="risk-fill-low" style="width: {min(risk_data['low'] * 10, 100)}%;"></div>
            </div>
            <div style="font-size: 1.5rem; font-weight: 600; color: #2c3e50;">{risk_data['low']}</div>
        </div>
        """, unsafe_allow_html=True)
def create_professional_sidebar():
    """Create a professional sidebar"""
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 1.5rem; background: linear-gradient(135deg, #2c3e50, #34495e); 
                border-radius: 8px; color: white; margin-bottom: 1.5rem;">
        <h2 style="margin: 0; font-size: 1.5rem;">⚖️ Legal AI</h2>
        <p style="margin: 0.5rem 0 0 0; opacity: 0.9; font-size: 0.9rem;">Powered by Legal BERT</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.sidebar.markdown("### 🚀 Features")
    st.sidebar.markdown("""
    - **Smart Summarization**: Extractive & Abstractive
    - **Legal Analysis**: Risk assessment & jurisdiction
    - **Deep Insights**: Clause importance analysis
    - **Rich Statistics**: Document metrics & entities
    """)
    
    st.sidebar.markdown("### 📋 Supported Formats")
    st.sidebar.markdown("""
    - PDF documents
    - DOCX files  
    - TXT files
    """)
    
    st.sidebar.markdown("### 💡 Tips")
    st.sidebar.markdown("""
    - Use clear, well-formatted documents
    - Larger files may take longer to process
    - Check results for accuracy
    """)
    
    st.sidebar.markdown("---")
    st.sidebar.markdown("### 📞 Support")
    st.sidebar.markdown("""
    [GitHub Issues](https://github.com/Sane219/Ai-Powered-Legal-Summarizer/issues)
    
    **Version**: 1.0.0
    """)
def show_clean_success(message, details=""):
    """Show clean success message"""
    st.markdown(f"""
    <div class="success-message">
        <h4 style="margin: 0 0 0.5rem 0;">✅ {message}</h4>
        {f'<p style="margin: 0;">{details}</p>' if details else ''}
    </div>
    """, unsafe_allow_html=True)
def show_clean_error(message, details=""):
    """Show clean error message"""
    st.markdown(f"""
    <div class="error-message">
        <h4 style="margin: 0 0 0.5rem 0;">❌ {message}</h4>
        {f'<p style="margin: 0;">{details}</p>' if details else ''}
    </div>
    """, unsafe_allow_html=True)
def show_clean_warning(message, details=""):
    """Show clean warning message"""
    st.markdown(f"""
    <div class="warning-message">
        <h4 style="margin: 0 0 0.5rem 0;">⚠️ {message}</h4>
        {f'<p style="margin: 0;">{details}</p>' if details else ''}
    </div>
    """, unsafe_allow_html=True)
# Main application
def main():
    # Load professional CSS
    load_css()
    
    # Create professional sidebar
    create_professional_sidebar()
    
    # Create header
    create_professional_header()
    
    # Initialize components
    processor, legal_summarizer, legal_analyzer = initialize_components()
    if not all([processor, legal_summarizer, legal_analyzer]):
        show_clean_error("Failed to initialize application components", "Please check the logs and ensure all dependencies are installed.")
        st.stop()
    
    # Clean file upload
    uploaded_file = create_clean_upload()
    
    if uploaded_file is not None:
        # Process file
        file_path = os.path.join("data", uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        
        # Extract and display text
        st.markdown("""
        <div class="clean-card">
            <h3 style="color: #3498db; margin-bottom: 1rem;">📄 Document Text</h3>
        </div>
        """, unsafe_allow_html=True)
        
        document_info = processor.process_document(file_path)
        
        if "error" in document_info:
            show_clean_error("Document Processing Error", document_info['error'])
        else:
            # Clean text display
            st.text_area("Extracted Text", document_info["clean_text"], height=200)
            
            # Create clean tabs
            tab1, tab2, tab3, tab4 = create_clean_tabs()
            
            with tab1:
                st.markdown("""
                <div class="clean-card">
                    <h3 style="color: #3498db; margin-bottom: 1rem;">📝 Legal BERT Summarization</h3>
                </div>
                """, unsafe_allow_html=True)
                
                # Clean summarization options
                col1, col2 = st.columns(2)
                with col1:
                    summarization_type = st.selectbox("Summarization Type", ["Extractive", "Abstractive"])
                with col2:
                    if summarization_type == "Extractive":
                        num_sentences = st.slider("Number of sentences", 1, 10, 3)
                    else:
                        max_length = st.slider("Max length", 50, 300, 150)
                
                if st.button("Generate Summary", key="summarize_btn"):
                    with st.spinner("Generating summary..."):
                        try:
                            if summarization_type == "Extractive":
                                summary = legal_summarizer.extractive_summarize(
                                    document_info["clean_text"],
                                    num_sentences=num_sentences
                                )
                                if summary:
                                    show_clean_success("Extractive Summary Generated")
                                    create_clean_card("Extractive Summary", summary, "📝", "#27ae60")
                                else:
                                    show_clean_warning("Summary Generation Failed", "Could not generate extractive summary. Please try with different settings.")
                            else:
                                summary = legal_summarizer.abstractive_summarize(
                                    document_info["clean_text"],
                                    max_length=max_length
                                )
                                if summary:
                                    show_clean_success("Abstractive Summary Generated")
                                    create_clean_card("Abstractive Summary", summary, "🤖", "#3498db")
                                else:
                                    show_clean_warning("Summary Generation Failed", "Could not generate abstractive summary. Please try with different settings.")
                        except Exception as e:
                            show_clean_error("Summary Generation Error", f"Error generating summary: {str(e)}")
            
            with tab2:
                st.markdown("""
                <div class="clean-card">
                    <h3 style="color: #e74c3c; margin-bottom: 1rem;">⚖️ Legal Document Analysis</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Analyze Document", key="analyze_btn"):
                    with st.spinner("Analyzing document..."):
                        try:
                            analysis = legal_analyzer.comprehensive_analysis(document_info["clean_text"])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                jurisdiction_content = "".join([f"{country}: {score:.2%}<br>" for country, score in analysis["jurisdiction"].items() if score > 0])
                                create_clean_card("Jurisdiction Detection", jurisdiction_content, "🌍", "#3498db")
                            
                            with col2:
                                risk_dist = analysis["risk_report"]["risk_distribution"]
                                create_clean_risk_visualization(risk_dist)
                            
                            if analysis["risk_report"]["recommendations"]:
                                rec_content = "".join([f"• {rec}<br>" for rec in analysis["risk_report"]["recommendations"]])
                                create_clean_card("Recommendations", rec_content, "💡", "#f39c12")
                                
                        except Exception as e:
                            show_clean_error("Analysis Error", f"Error analyzing document: {str(e)}")
            
            with tab3:
                st.markdown("""
                <div class="clean-card">
                    <h3 style="color: #9b59b6; margin-bottom: 1rem;">🔍 Legal BERT Insights</h3>
                </div>
                """, unsafe_allow_html=True)
                
                if st.button("Extract Legal Insights", key="insights_btn"):
                    with st.spinner("Extracting insights..."):
                        try:
                            insights = legal_summarizer.get_legal_insights(document_info["clean_text"])
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                importance_content = f"""
                                High: {len(insights['high_importance'])} clauses<br>
                                Medium: {len(insights['medium_importance'])} clauses<br>
                                Low: {len(insights['low_importance'])} clauses
                                """
                                create_clean_card("Importance Levels", importance_content, "📈", "#9b59b6")
                            
                            with col2:
                                clause_content = "".join([f"• {clause_type}: {len(clauses)} instances<br>" 
                                                        for clause_type, clauses in insights["clause_types"].items()])
                                create_clean_card("Clause Types Detected", clause_content, "📋", "#e67e22")
                            
                            if insights["high_importance"]:
                                high_imp_content = "".join([f"{i}. {clause[:200]}...<br>" 
                                                          for i, clause in enumerate(insights["high_importance"][:3], 1)])
                                create_clean_card("High Importance Clauses", high_imp_content, "🔥", "#e74c3c")
                                
                        except Exception as e:
                            show_clean_error("Insights Error", f"Error extracting insights: {str(e)}")
            
            with tab4:
                st.markdown("""
                <div class="clean-card">
                    <h3 style="color: #f39c12; margin-bottom: 1rem;">📊 Document Statistics</h3>
                </div>
                """, unsafe_allow_html=True)
                
                try:
                    create_clean_metrics(document_info)
                    
                    # Additional statistics
                    col1, col2 = st.columns(2)
                    with col1:
                        if document_info["dates"]:
                            dates_content = "".join([f"• {date}<br>" for date in document_info["dates"]])
                            create_clean_card("Dates Found", dates_content, "📅", "#27ae60")
                    
                    with col2:
                        entities_content = f"Total entities: {document_info['entities'].get('total_count', 0)}<br>"
                        entities_content += "".join([f"• {entity_type}: {len(entities)}<br>" 
                                                    for entity_type, entities in document_info["entities"].items() 
                                                    if entity_type != "total_count"])
                        create_clean_card("Entity Breakdown", entities_content, "🏷️", "#3498db")
                        
                except Exception as e:
                    show_clean_error("Statistics Error", f"Error generating statistics: {str(e)}")
    
    else:
        # Clean welcome message
        st.markdown("""
        <div class="clean-card" style="text-align: center;">
            <h3 style="color: #3498db; margin-bottom: 1rem;">👋 Welcome to AI Legal Document Summarizer</h3>
            <p style="color: #7f8c8d; font-size: 1.1rem; margin-bottom: 1.5rem;">
                Upload a legal document to get started with AI-powered analysis, summarization, and insights.
            </p>
            <div>
                <span style="background: #ecf0f1; padding: 0.75rem 1.5rem; 
                             border-radius: 25px; margin: 0.25rem; display: inline-block; color: #2c3e50;">
                    📄 Supports PDF, DOCX, TXT
                </span>
                <span style="background: #ecf0f1; padding: 0.75rem 1.5rem; 
                             border-radius: 25px; margin: 0.25rem; display: inline-block; color: #2c3e50;">
                    ⚡ Fast Processing
                </span>
                <span style="background: #ecf0f1; padding: 0.75rem 1.5rem; 
                             border-radius: 25px; margin: 0.25rem; display: inline-block; color: #2c3e50;">
                    🔒 Secure & Private
                </span>
            </div>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
