# AI-Powered Legal Document Summarization

## Overview
This project is an advanced AI-based tool that leverages Legal BERT and transformer-based models to generate concise, accurate, and readable summaries of legal documents. The system provides comprehensive legal document analysis with specialized models trained on legal text.

## Features

### 🤖 Legal BERT Integration
- **Legal BERT Summarization**: Specialized BERT model fine-tuned for legal clause classification
- **Unified Extractive/Abstractive**: Single interface for both summarization methods
- **Legal Context Awareness**: Prioritizes legally relevant sentences and clauses
- **Clause Classification**: Automatic identification and categorization of legal clauses

### 📊 Advanced Analysis
- **Extractive and Abstractive Summarization** using Legal BERT and BART models
- **Jurisdiction Detection** to tailor suggestions and summaries based on locale-specific laws
- **Risk Assessment** with automated clause risk categorization (High/Medium/Low)
- **Legal Insights Extraction** with importance level classification
- **Comprehensive Document Statistics** including entity recognition and party identification

### 🎯 Smart Features
- **Multi-tab Interface**: Organized workflow with Summarization, Legal Analysis, Insights, and Statistics
- **Entity Recognition**: Automatic extraction of parties, dates, and legal entities
- **Legal Section Identification**: Detection of standard legal document sections
- **Recommendation Engine**: AI-powered suggestions for document improvements

### 💻 User Interface
- **Streamlit-Based Web Interface** with intuitive design
- **File Upload Support**: PDF, DOCX, and TXT format compatibility
- **Real-time Processing**: Instant analysis and summarization
- **Interactive Tabs**: Organized feature access with visual feedback

## Setup

### Prerequisites
- Python 3.8+
- pip (Python package installer)
- 4GB+ RAM (recommended for transformer models)
- Internet connection (for initial model downloads)

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/Sane219/Ai-Powered-Legal-Summarizer.git
   cd Ai-Powered-Legal-Summarizer
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv legal_ai_env
   source legal_ai_env/bin/activate   # On Windows use: legal_ai_env\Scripts\activate
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy language model** (required for entity recognition)
   ```bash
   python -m spacy download en_core_web_sm
   ```

## Running the Application

### Quick Start
1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```
   Access the app at `http://localhost:8501`

2. **Run comprehensive tests** (optional)
   ```bash
   python test_project.py
   ```

## Usage Guide

### Document Upload
- Upload legal documents in **PDF**, **DOCX**, or **TXT** format
- Supported document types: contracts, agreements, NDAs, employment documents, etc.

### Feature Tabs

#### 📝 Summarization Tab
- **Legal BERT Extractive**: Select number of key sentences (1-10)
- **Legal BERT Abstractive**: Choose summary length (50-300 words)
- Real-time processing with legal context awareness

#### ⚖️ Legal Analysis Tab
- **Jurisdiction Detection**: Automatic identification of applicable legal systems
- **Risk Assessment**: Clause-level risk categorization with recommendations
- **Party Identification**: Extraction of involved parties and entities

#### 🔍 Insights Tab
- **Legal BERT Insights**: AI-powered clause importance classification
- **Clause Type Detection**: Automatic categorization of legal provisions
- **High-Priority Clauses**: Focus on most critical document sections

#### 📊 Statistics Tab
- **Document Metrics**: Word count, character count, entity statistics
- **Legal Sections**: Identification of standard legal document structures
- **Entity Analysis**: Comprehensive breakdown of extracted information

## Architecture

### Core Components
- **Legal BERT Summarizer** (`src/legal_bert_summarizer.py`): Unified summarization engine
- **Document Processor** (`src/document_processor.py`): Text extraction and preprocessing
- **Legal Analyzer** (`src/legal_analyzer.py`): Jurisdiction detection and risk assessment
- **Extractive Summarizer** (`src/extractive_summarizer.py`): Traditional extractive methods
- **Abstractive Summarizer** (`src/abstractive_summarizer.py`): Neural abstractive summarization

### Models Used
- **Legal BERT**: `mauro/bert-base-uncased-finetuned-clause-type` for legal clause classification
- **BART**: `facebook/bart-large-cnn` for abstractive summarization
- **spaCy**: `en_core_web_sm` for entity recognition and text processing

## Testing
The project includes comprehensive testing via `test_project.py`:
- Configuration validation
- Document processing pipeline
- Summarization engines (extractive & abstractive)
- Legal analysis components
- File processing capabilities

## Project Structure
```
Ai-Powered-Legal-Summarizer/
├── app.py                          # Main Streamlit application
├── requirements.txt                # Python dependencies
├── test_project.py                 # Comprehensive test suite
├── data/                          # Sample documents and uploads
│   ├── sample_contract.txt
│   └── Sample_NDA_Legal_Document.pdf
└── src/                           # Core modules
    ├── config.py                  # Configuration and constants
    ├── document_processor.py      # Document processing pipeline
    ├── legal_bert_summarizer.py   # Legal BERT integration
    ├── extractive_summarizer.py   # Extractive summarization
    ├── abstractive_summarizer.py  # Abstractive summarization
    └── legal_analyzer.py          # Legal analysis and risk assessment
```

## Performance Notes
- **First Run**: Initial model downloads may take 2-5 minutes
- **Processing Time**: Varies by document length (typically 5-30 seconds)
- **Memory Usage**: 2-4GB RAM during processing
- **GPU Support**: Automatically utilizes CUDA if available

## Troubleshooting

### Common Issues
1. **Model Download Errors**: Ensure stable internet connection for initial setup
2. **Memory Issues**: Close other applications if running on limited RAM
3. **PDF Processing**: Some complex PDFs may require manual text extraction
4. **Slow Performance**: Consider using GPU acceleration for faster processing

### Dependencies
If you encounter import errors, ensure all dependencies are installed:
```bash
pip install --upgrade -r requirements.txt
python -m spacy download en_core_web_sm
```

## Contributing
Pull requests are welcome! For major changes, please open an issue first to discuss the proposed changes.

### Development Setup
1. Fork the rep
ity** tech communegalhe l❤️ for tith **Built w
---


ce frameworkterfa the web intreamlit for
- Sacebook AIodel by Frization mBART summae)
- ypclause-tned--finetuasedrt-base-uncuro/begface.co/mas://huggin-type](httpuned-clauseetcased-finase-unro/bert-bel by [mauBERT mod
- Legal gmentsowledckn

## Ase](LICENSE)[MIT Licen
nseice

## L Requestpen a Pull6. Ofeature`)
re/amazing-in featuush origanch (`git pbr. Push to 
5feature'`)Add amazing it -m 'comm(`git  changes ommit.py`)
4. Ctest_projectython un tests (`pe`)
3. Raturing-feamazfeature/kout -b (`git checch re brante a featu2. Creaository
