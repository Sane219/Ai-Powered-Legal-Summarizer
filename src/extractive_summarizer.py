"""
Extractive summarization module for legal documents
Leverages a transformer model for summarization
"""
from transformers import pipeline
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExtractiveSummarizer:
    """Summarizes legal documents using extractive summarization with Legal BERT"""
    
    def __init__(self, model_name="mauro/bert-base-uncased-finetuned-clause-type"):
        """Initialize the summarizer with a legal-specific BERT model"""
        self.model_name = model_name
        try:
            # Import additional libraries for Legal BERT-based summarization
            from transformers import AutoTokenizer, AutoModel
            import torch
            
            # Load Legal BERT model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.legal_model = AutoModel.from_pretrained(model_name)
            
            # For clause classification
            self.classifier = pipeline("text-classification", model=model_name)
            
            # For summarization fallback, use legal-oriented model
            self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
            
            logger.info(f"Initialized Legal BERT extractive summarizer with model {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize Legal BERT model {model_name}: {e}")
            # Fallback to a lighter model
            self.model_name = "sshleifer/distilbart-cnn-12-6"
            self.summarizer = pipeline("summarization", model=self.model_name)
            self.classifier = None
            self.legal_model = None
            self.tokenizer = None
            logger.info(f"Fallback to model {self.model_name}")

    def summarize(self, text, max_length=130, min_length=30) -> str:
        """Summarize the input text using the model"""
        try:
            summary = self.summarizer(
                text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            summarized_text = summary[0]["summary_text"]
            logger.info("Summarization successful")
            return summarized_text
        except Exception as e:
            logger.error(f"Summarization failed: {e}")
            return ""

def main():
    """Test the extractive summarizer"""
    summarizer = ExtractiveSummarizer()
    
    # Test text
    sample_text = """
    This Agreement is entered into between ABC Corporation, a Delaware corporation ("Company"), 
    and John Doe ("Employee") on January 1, 2024. The term of this agreement shall be 2 years.
    CONFIDENTIALITY: Employee agrees to maintain confidentiality of all proprietary information.
    TERMINATION: This agreement may be terminated by either party with 30 days notice.
    """
    
    # Summarize text
    summary = summarizer.summarize(sample_text)
    print("Summary:\n", summary)

if __name__ == "__main__":
    main()

