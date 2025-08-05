# AI-Powered Legal Document Summarization

## Overview
This project aims to create an AI-based tool that leverages transformer-based models to generate concise, accurate, and readable summaries of legal documents.

## Features
- **Extractive and Abstractive Summarization** using models like BERT and GPT-based architectures.
- **Jurisdiction Detection** to tailor suggestions and summaries based on locale-specific laws.
- **Clause-by-Clause Analysis** for a detailed examination of specific document sections.
- **Streamlit-Based User Interface** providing easy upload and summary generation.

## Setup

### Prerequisites
- Python 3.7+
- pip (Python package installer)

### Installation
1. **Clone the repository**
   ```bash
   git clone https://github.com/your-repo/legal-summarizer.git
   cd legal-summarizer
   ```

2. **Set up a virtual environment**
   ```bash
   python -m venv legal_ai_env
   source legal_ai_env/bin/activate   # On Windows use: legal_ai_env\Scripts\Activate.ps1
   ```

3. **Install required dependencies**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application
1. **Start the Streamlit app**
   ```bash
   streamlit run app.py
   ```
   Access the app at `http://localhost:8501`

## Usage
- Upload legal documents in PDF, DOCX, or TXT format to generate summaries.
- Choose between extractive and abstractive summarization methods.

## Model Training
- The existing summarization models are pre-trained and fine-tuned for processing legal documents.

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss the proposed changes.

## License
[MIT License](LICENSE)

---
