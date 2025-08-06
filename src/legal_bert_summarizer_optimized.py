"""
Memory-optimized Legal BERT-based unified summarizer for both extractive and abstractive summarization
"""
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from transformers import AutoTokenizer, AutoModel, pipeline
import torch
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import logging
from typing import List, Dict
import re
import gc

logger = logging.getLogger(__name__)

class LegalBertSummarizer:
    """Memory-optimized unified Legal BERT summarizer for both extractive and abstractive summarization"""
    
    def __init__(self, model_name="mauro/bert-base-uncased-finetuned-clause-type"):
        """Initialize the Legal BERT summarizer with memory optimization"""
        self.model_name = model_name
        self.tokenizer = None
        self.model = None
        self.classifier = None
        self.abstractive_model = None
        
        try:
            # Load models with memory-efficient settings
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_name, 
                trust_remote_code=True,
                use_fast=True  # Use fast tokenizer for better performance
            )
            
            # Load model with reduced precision if available
            self.model = AutoModel.from_pretrained(
                model_name, 
                trust_remote_code=True,
                torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
                low_cpu_mem_usage=True
            )
            
            # Legal clause classifier with fallback
            try:
                self.classifier = pipeline(
                    "text-classification", 
                    model=model_name, 
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
            except Exception as e:
                logger.warning(f"Could not load legal classifier: {e}, using fallback")
                self.classifier = None
            
            # Lazy load abstractive model only when needed
            logger.info(f"Initialized Legal BERT unified summarizer with {model_name}")
            
        except Exception as e:
            logger.error(f"Failed to initialize Legal BERT: {e}")
            # Don't raise, allow fallback methods to work
            logger.info("Will use fallback methods for summarization")
    
    def get_sentence_embeddings(self, sentences: List[str]) -> np.ndarray:
        """Get BERT embeddings for sentences using Legal BERT with memory optimization"""
        embeddings = []
        
        # Process sentences in batches to manage memory
        batch_size = 5
        for i in range(0, len(sentences), batch_size):
            batch = sentences[i:i+batch_size]
            
            for sentence in batch:
                try:
                    # Truncate long sentences
                    if len(sentence) > 500:
                        sentence = sentence[:500]
                    
                    # Tokenize and get embeddings
                    inputs = self.tokenizer(sentence, return_tensors="pt", truncation=True, padding=True, max_length=512)
                    
                    with torch.no_grad():
                        outputs = self.model(**inputs)
                        # Use CLS token embedding
                        sentence_embedding = outputs.last_hidden_state[:, 0, :].numpy()
                        embeddings.append(sentence_embedding[0])
                except Exception as e:
                    logger.warning(f"Failed to get embedding for sentence: {e}")
                    # Use zero embedding as fallback
                    embeddings.append(np.zeros(768))  # BERT base dimension
            
            # Clear memory after each batch
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            gc.collect()
        
        return np.array(embeddings)
    
    def extractive_summarize(self, text: str, num_sentences: int = 3) -> str:
        """Perform extractive summarization using Legal BERT embeddings with memory optimization"""
        try:
            # Truncate very long texts
            if len(text) > 20000:
                text = text[:20000]
                logger.info("Truncated text for extractive summarization")
            
            # Split text into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text.strip())
            sentences = [s.strip() for s in sentences if len(s.strip()) > 10]
            
            if len(sentences) <= num_sentences:
                return " ".join(sentences)
            
            # Limit number of sentences to process
            if len(sentences) > 50:
                sentences = sentences[:50]
                logger.info("Limited to first 50 sentences for processing")
            
            # Get Legal BERT embeddings for all sentences
            if self.model and self.tokenizer:
                sentence_embeddings = self.get_sentence_embeddings(sentences)
                
                # Get document embedding (average of all sentence embeddings)
                doc_embedding = np.mean(sentence_embeddings, axis=0)
                
                # Calculate similarity scores
                similarities = cosine_similarity([doc_embedding], sentence_embeddings)[0]
            else:
                # Fallback: use random scores
                similarities = np.random.random(len(sentences))
            
            # Classify each sentence for legal importance
            legal_scores = []
            for sentence in sentences:
                try:
                    if self.classifier:
                        # Truncate sentence for classification
                        truncated_sentence = sentence[:512]
                        classification = self.classifier(truncated_sentence)
                        # Use the confidence score as legal importance
                        score = classification[0]['score'] if classification else 0.5
                    else:
                        # Fallback scoring based on legal keywords
                        score = self._get_legal_score_fallback(sentence)
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
            
            # Clear memory
            gc.collect()
            return summary
            
        except Exception as e:
            logger.error(f"Legal BERT extractive summarization failed: {e}")
            # Fallback to simple text truncation
            sentences = re.split(r'(?<=[.!?])\s+', text.strip())
            return " ".join(sentences[:num_sentences])
    
    def _load_abstractive_model(self):
        """Lazy load abstractive model only when needed"""
        if self.abstractive_model is None:
            try:
                self.abstractive_model = pipeline(
                    "summarization", 
                    model="facebook/bart-large-cnn", 
                    trust_remote_code=True,
                    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
                )
                logger.info("Loaded abstractive summarization model")
            except Exception as e:
                logger.warning(f"Could not load abstractive model: {e}")
                self.abstractive_model = False  # Mark as failed to avoid retrying
    
    def abstractive_summarize(self, text: str, max_length: int = 150, min_length: int = 50) -> str:
        """Perform abstractive summarization with legal context awareness and memory optimization"""
        try:
            # Truncate very long texts to prevent memory issues
            if len(text) > 10000:
                text = text[:10000]
                logger.info("Truncated text for abstractive summarization")
            
            # First, use Legal BERT to identify important legal clauses
            sentences = re.split(r'(?<=[.!?])\s+', text.strip())
            legal_sentences = []
            
            for sentence in sentences[:50]:  # Limit to first 50 sentences
                try:
                    if self.classifier:
                        classification = self.classifier(sentence[:512])  # Truncate sentence
                        # Keep sentences with high legal relevance
                        if classification and classification[0]['score'] > 0.6:
                            legal_sentences.append(sentence)
                    else:
                        # Fallback: use keyword-based legal relevance
                        if self._get_legal_score_fallback(sentence) > 0.6:
                            legal_sentences.append(sentence)
                except:
                    continue
            
            # If we found legally relevant sentences, prioritize them
            if legal_sentences:
                prioritized_text = " ".join(legal_sentences[:10])  # Limit to 10 sentences
            else:
                prioritized_text = text[:5000]  # Use first 5000 chars
            
            # Load abstractive model if needed
            self._load_abstractive_model()
            
            # Use the abstractive model with legal context
            if self.abstractive_model and self.abstractive_model is not False:
                summary = self.abstractive_model(
                    prioritized_text,
                    max_length=min(max_length, 200),  # Cap max length
                    min_length=min(min_length, 30),
                    do_sample=False
                )
                result = summary[0]["summary_text"]
                logger.info("Legal BERT-enhanced abstractive summarization successful")
                
                # Clear memory
                gc.collect()
                return result
            else:
                # Fallback to extractive if abstractive model not available
                logger.info("Using extractive fallback for abstractive summarization")
                return self.extractive_summarize(text, num_sentences=3)
            
        except Exception as e:
            logger.error(f"Legal BERT abstractive summarization failed: {e}")
            # Fallback to extractive
            try:
                return self.extractive_summarize(text, num_sentences=3)
            except:
                return "Unable to generate summary due to processing error."
    
    def get_legal_insights(self, text: str) -> Dict:
        """Extract legal insights using Legal BERT classification with memory optimization"""
        # Truncate text if too long
        if len(text) > 15000:
            text = text[:15000]
            
        sentences = re.split(r'(?<=[.!?])\s+', text.strip())
        insights = {
            "high_importance": [],
            "medium_importance": [],
            "low_importance": [],
            "clause_types": {}
        }
        
        # Limit number of sentences to process
        sentences = sentences[:100]
        
        for sentence in sentences:
            if len(sentence.strip()) < 10:
                continue
                
            try:
                if self.classifier:
                    # Truncate sentence for classification
                    truncated_sentence = sentence[:512]
                    classification = self.classifier(truncated_sentence)
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
                else:
                    # Fallback classification
                    score = self._get_legal_score_fallback(sentence)
                    if score > 0.7:
                        insights["high_importance"].append(sentence)
                    elif score > 0.5:
                        insights["medium_importance"].append(sentence)
                    else:
                        insights["low_importance"].append(sentence)
                        
            except Exception as e:
                logger.warning(f"Failed to classify sentence: {e}")
                continue
        
        # Clear memory
        gc.collect()
        return insights
    
    def _get_legal_score_fallback(self, sentence: str) -> float:
        """Fallback method to score legal importance using keywords"""
        legal_keywords = [
            'agreement', 'contract', 'party', 'parties', 'shall', 'hereby', 'whereas',
            'confidentiality', 'termination', 'liability', 'indemnification', 'property',
            'intellectual', 'disclosure', 'non-disclosure', 'employment', 'compensation',
            'damages', 'breach', 'arbitration', 'jurisdiction', 'governing law',
            'force majeure', 'amendment'
        ]
        
        sentence_lower = sentence.lower()
        matches = sum(1 for keyword in legal_keywords if keyword in sentence_lower)
        
        # Normalize score between 0 and 1
        max_possible_matches = min(len(legal_keywords), len(sentence.split()))
        score = matches / max_possible_matches if max_possible_matches > 0 else 0.5
        
        return min(score, 1.0)

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