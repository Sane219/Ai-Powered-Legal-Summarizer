"""
Abstractive summarization module for legal documents
Uses GPT-based models for generating abstractive summaries
"""
from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
import logging
from typing import Dict, List

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AbstractiveSummarizer:
    """Generates abstractive summaries of legal documents"""
    
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """Initialize the abstractive summarizer"""
        self.model_name = model_name
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
            self.summarizer = pipeline(
                "summarization", 
                model=self.model, 
                tokenizer=self.tokenizer,
                framework="pt"
            )
            logger.info(f"Initialized abstractive summarizer with model {model_name}")
        except Exception as e:
            logger.error(f"Failed to initialize model {model_name}: {e}")
            # Fallback to a lighter model
            self.model_name = "sshleifer/distilbart-cnn-12-6"
            self.summarizer = pipeline("summarization", model=self.model_name)
            logger.info(f"Fallback to model {self.model_name}")
    
    def chunk_text(self, text: str, max_chunk_length: int = 1024) -> List[str]:
        """Split text into chunks for processing"""
        words = text.split()
        chunks = []
        current_chunk = []
        current_length = 0
        
        for word in words:
            if current_length + len(word) + 1 > max_chunk_length and current_chunk:
                chunks.append(" ".join(current_chunk))
                current_chunk = [word]
                current_length = len(word)
            else:
                current_chunk.append(word)
                current_length += len(word) + 1
        
        if current_chunk:
            chunks.append(" ".join(current_chunk))
        
        return chunks
    
    def summarize(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """Generate abstractive summary of the input text"""
        try:
            # Handle long texts by chunking
            if len(text.split()) > 1024:
                chunks = self.chunk_text(text)
                summaries = []
                
                for chunk in chunks:
                    summary = self.summarizer(
                        chunk,
                        max_length=max_length // len(chunks) + 50,
                        min_length=min_length // len(chunks),
                        do_sample=False
                    )
                    summaries.append(summary[0]["summary_text"])
                
                # Combine chunk summaries
                combined_summary = " ".join(summaries)
                
                # Generate final summary from combined summaries
                if len(combined_summary.split()) > 200:
                    final_summary = self.summarizer(
                        combined_summary,
                        max_length=max_length,
                        min_length=min_length,
                        do_sample=False
                    )
                    return final_summary[0]["summary_text"]
                else:
                    return combined_summary
            else:
                summary = self.summarizer(
                    text,
                    max_length=max_length,
                    min_length=min_length,
                    do_sample=False
                )
                return summary[0]["summary_text"]
                
        except Exception as e:
            logger.error(f"Abstractive summarization failed: {e}")
            return ""
    
    def legal_focused_summary(self, text: str, focus_areas: List[str] = None) -> Dict[str, str]:
        """Generate summary focused on specific legal areas"""
        if focus_areas is None:
            focus_areas = ["parties", "obligations", "terms", "conditions", "dates"]
        
        # Create focused prompts for each area
        focused_summaries = {}
        
        for area in focus_areas:
            prompt = f"Summarize the {area} mentioned in this legal document: {text}"
            try:
                summary = self.summarizer(
                    prompt,
                    max_length=100,
                    min_length=20,
                    do_sample=False
                )
                focused_summaries[area] = summary[0]["summary_text"]
            except Exception as e:
                logger.error(f"Failed to generate {area} summary: {e}")
                focused_summaries[area] = ""
        
        return focused_summaries

def main():
    """Test the abstractive summarizer"""
    summarizer = AbstractiveSummarizer()
    
    # Test with longer legal text
    sample_text = """
    EMPLOYMENT AGREEMENT
    
    This Employment Agreement ("Agreement") is entered into on January 15, 2024, 
    between TechCorp Inc., a Delaware corporation ("Company"), and Jane Smith ("Employee").
    
    1. TERM: The term of employment shall commence on February 1, 2024, and continue 
    for a period of 2 years, unless terminated earlier in accordance with this Agreement.
    
    2. POSITION AND DUTIES: Employee shall serve as Senior Software Engineer and shall 
    perform such duties as may be assigned by the Company. Employee agrees to devote 
    full time and attention to the business of the Company.
    
    3. COMPENSATION: Company shall pay Employee a base salary of $120,000 per year, 
    payable in equal monthly installments. Employee shall also be eligible for 
    annual performance bonuses at the discretion of the Company.
    
    4. CONFIDENTIALITY: Employee acknowledges that during employment, Employee may have 
    access to confidential and proprietary information of the Company. Employee agrees 
    to maintain strict confidentiality of all such information during and after employment.
    
    5. TERMINATION: Either party may terminate this Agreement with 30 days written notice.
    Upon termination, Employee shall return all company property and confidential materials.
    Company may terminate Employee immediately for cause, including breach of this Agreement.
    
    6. NON-COMPETE: For a period of 12 months following termination, Employee agrees not 
    to engage in any business that competes with the Company within a 50-mile radius.
    
    7. GOVERNING LAW: This Agreement shall be governed by the laws of the State of Delaware.
    
    IN WITNESS WHEREOF, the parties have executed this Agreement on the date first written above.
    """
    
    print("=== Testing Abstractive Summarizer ===")
    
    # Test general summary
    print("\n1. General Summary:")
    general_summary = summarizer.summarize(sample_text, max_length=200, min_length=50)
    print(general_summary)
    
    # Test focused summaries
    print("\n2. Focused Summaries:")
    focused_summaries = summarizer.legal_focused_summary(sample_text)
    for area, summary in focused_summaries.items():
        if summary:
            print(f"{area.capitalize()}: {summary}")

if __name__ == "__main__":
    main()
