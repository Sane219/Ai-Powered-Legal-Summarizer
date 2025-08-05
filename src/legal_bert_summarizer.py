"""
Legal BERT-based unified summarizer for both extractive and abstractive summarization
"""
from transformers import AutoTokenizer, AutoModel, pipeline
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import List, Dict
import re

logger = logging.getLogger(__name__)

class LegalBertSummarizer:
    """Unified Legal BERT summarizer for both extractive and abstractive summarization"""
    
    def __init__(self, model_name="mauro/bert-base-uncased-finetuned-clause-type"):
        """Initialize the Legal BERT summarizer"""
        self.model_name = model_name
        
        try:
            # Load Legal BERT model and tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModel.from_pretrained(model_name)
            
            # Legal clause classifier
            self.classifier = pipeline("text-classification", model=model_name)
            
            # Fallback summarizer for abstractive tasks
            self.abstractive_model = pipeline("summarization", model="facebook/bart-large-cnn")
            
            logger.info(f"Initialized Legal BERT unified summarizer with {model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Legal BERT: {e}")
            raise
    
    def get_sentence_embeddings(self, sentences: List[str]) -> np.ndarray:
        """Get BERT embeddings for sentences using Legal BERT"""
        embeddings = []
        
        for sentence in sentences:
            # Tokenize and get embeddings
            inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
            
            with torch.no_grad():
                outputs = self.model(**inputs)
                # Use CLS token embedding
                sentence_embedding = outputs.last_hidden_state[:, 0, :].numpy()
                embeddings.append(sentence_embedding[0])
        
        return np.array(embeddings)
    
    def extractive_summarize(self, text: str, num_sentences: int = 3) -> str:
        """Perform extractive summarization using Legal BERT embeddings"""
        try:
            # Split text into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text.strip())
            sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
            
            if len(sentences) <= num_sentences:
                return " ".join(sentences)
            
            # Get Legal BERT embeddings for all sentences
            sentence_embeddings = self.get_sentence_embeddings(sentences)
            
            # Get document embedding (average of all sentence embeddings)
            doc_embedding = np.mean(sentence_embeddings, axis=0)
            
            # Calculate similarity scores
            similarities = cosine_similarity([doc_embedding], sentence_embeddings)[0]
            
            # Classify each sentence for legal importance
            legal_scores = []
            for sentence in sentences:
                try:
                    classification = self.classifier(sentence)
                    # Use the confidence score as legal importance
                    score = classification[0]['score'] if classification else 0.5
                    legal_scores.append(score)
                except:
                    legal_scores.append(0.5)
            
            # Combine similarity and legal importance scores
            combined_scores = []
            for i in range(len(sentences)):
                # Weight: 60% Legal BERT similarity + 40% Legal classification score
                combined_score = 0.6 * similarities[i] + 0.4 * legal_scores[i]
                combined_scores.append((combined_score, i, sentences[i]))
            
            # Sort by combined score and select top sentences
            combined_scores.sort(reverse=True, key=lambda x: x[0])
            
            # Select top sentences and maintain original order
            selected_indices = sorted([item[1] for item in combined_scores[:num_sentences]])
            summary_sentences = [sentences[i] for i in selected_indices]
            
            summary = " ".join(summary_sentences)
            logger.info(f"Legal BERT extractive summarization successful: {len(summary_sentences)} sentences")
            return summary
            
        except Exception as e:
            logger.error(f"Legal BERT extractive summarization failed: {e}")
            return ""
    
    def abstractive_summarize(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """Perform abstractive summarization with legal context awareness"""
        try:
            # First, use Legal BERT to identify important legal clauses
            sentences = re.split(r'(?<=[.!?])\s+', text.strip())
            legal_sentences = []
            
            for sentence in sentences:
                try:
                    classification = self.classifier(sentence)
                    # Keep sentences with high legal relevance
                    if classification and classification[0]['score'] > 0.6:
                        legal_sentences.append(sentence)
                except:
                    continue
            
            # If we found legally relevant sentences, prioritize them
            if legal_sentences:
                prioritized_text = " ".join(legal_sentences) + " " + text
            else:
                prioritized_text = text
            
            # Use the abstractive model with legal context
            summary = self.abstractive_model(
                prioritized_text,
                max_length=max_length,
                min_length=min_length,
                do_sample=False
            )
            
            result = summary[0]["summary_text"]
            logger.info("Legal BERT-enhanced abstractive summarization successful")
            return result
            
        except Exception as e:
            logger.error(f"Legal BERT abstractive summarization failed: {e}")
            return ""
    
    def get_legal_insights(self, text: str) -> Dict:
        """Extract legal insights using Legal BERT classification"""
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        insights = {
            "high_importance": [],
            "medium_importance": [],
            "low_importance": [],
            "clause_types": {}
        }
        
        for sentence in sentences:
            if len(sentence.strip()) < 10:
                continue
                
            try:
                classification = self.classifier(sentence)
                if classification:
                    score = classification[0]['score']
                    label = classification[0]['label']
                    
                    # Categorize by importance
                    if score > 0.8:
                        insights["high_importance"].append(sentence)
                    elif score > 0.6:
                        insights["medium_importance"].append(sentence)
                    else:
                        insights["low_importance"].append(sentence)
                    
                    # Track clause types
                    if label not in insights["clause_types"]:
                        insights["clause_types"][label] = []
                    insights["clause_types"][label].append({
                        "sentence": sentence,
                        "confidence": score
                    })
                        
            except Exception as e:
                logger.warning(f"Failed to classify sentence: {e}")
                continue
        
        return insights

def main():
    """Test the Legal BERT unified summarizer"""
    print("Testing Legal BERT Unified Summarizer...")
    
    summarizer = LegalBertSummarizer()
    
    sample_text = """
    EMPLOYMENT AGREEMENT
    
    This Employment Agreement is entered into between TechCorp Inc., a Delaware corporation ("Company"), 
    and Jane Smith ("Employee") on January 15, 2024. The term of employment shall commence on February 1, 2024, 
    and continue for a period of 2 years, unless terminated earlier.
    
    CONFIDENTIALITY: Employee acknowledges that during employment, Employee may have access to confidential 
    and proprietary information of the Company. Employee agrees to maintain strict confidentiality.
    
    TERMINATION: Either party may terminate this Agreement with 30 days written notice. Upon termination, 
    Employee shall return all company property and confidential materials.
    
    COMPENSATION: Company shall pay Employee a base salary of $120,000 per year, payable monthly.
    """
    
    print("\n1. Legal BERT Extractive Summary:")
    extractive_summary = summarizer.extractive_summarize(sample_text, num_sentences=3)
    print(extractive_summary)
    
    print("\n2. Legal BERT-Enhanced Abstractive Summary:")
    abstractive_summary = summarizer.abstractive_summarize(sample_text, max_length=100)
    print(abstractive_summary)
    
    print("\n3. Legal Insights:")
    insights = summarizer.get_legal_insights(sample_text)
    print(f"High importance clauses: {len(insights['high_importance'])}")
    print(f"Clause types found: {list(insights['clause_types'].keys())}")

if __name__ == "__main__":
    main()
