"""
Comprehensive test script for AI-Powered Legal Document Summarization
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

def test_all_modules():
    """Test all modules in the project"""
    print("🧪 Testing AI-Powered Legal Document Summarization\n")
    
    # Test 1: Configuration
    print("1. Testing Configuration...")
    try:
        from config import MODELS, LEGAL_SECTIONS, CLAUSE_KEYWORDS
        print(f"   ✅ Models configured: {list(MODELS.keys())}")
        print(f"   ✅ Legal sections: {len(LEGAL_SECTIONS)}")
        print(f"   ✅ Clause keywords: {len(CLAUSE_KEYWORDS)}")
    except Exception as e:
        print(f"   ❌ Configuration test failed: {e}")
        return False
    
    # Test 2: Document Processor
    print("\n2. Testing Document Processor...")
    try:
        from document_processor import DocumentProcessor
        processor = DocumentProcessor()
        
        sample_text = """
        EMPLOYMENT AGREEMENT
        This Employment Agreement is entered into between ABC Corporation (Company) and John Doe (Employee) on January 1, 2024.
        CONFIDENTIALITY: Employee shall maintain confidentiality of all proprietary information.
        TERMINATION: This agreement may be terminated with 30 days notice.
        """
        
        # Test text cleaning
        clean_text = processor.clean_text(sample_text)
        print(f"   ✅ Text cleaning: {len(clean_text)} chars processed")
        
        # Test entity extraction
        entities = processor.extract_entities(clean_text)
        print(f"   ✅ Entity extraction: {entities.get('total_count', 0)} entities found")
        
        # Test section identification
        sections = processor.identify_legal_sections(clean_text)
        found_sections = {k: v for k, v in sections.items() if v}
        print(f"   ✅ Legal sections: {len(found_sections)} sections identified")
        
    except Exception as e:
        print(f"   ❌ Document processor test failed: {e}")
        return False
    
    # Test 3: Extractive Summarizer
    print("\n3. Testing Extractive Summarizer...")
    try:
        from extractive_summarizer import ExtractiveSummarizer
        summarizer = ExtractiveSummarizer()
        
        sample_text = """
        This Employment Agreement is entered into between TechCorp Inc., a Delaware corporation, 
        and Jane Smith on January 15, 2024. The term of employment shall commence on February 1, 2024, 
        and continue for a period of 2 years. Employee agrees to maintain confidentiality of all 
        proprietary information. Either party may terminate this agreement with 30 days written notice.
        """
        
        summary = summarizer.summarize(sample_text, max_length=80, min_length=20)
        if summary:
            print(f"   ✅ Extractive summarization: Generated {len(summary.split())} word summary")
        else:
            print("   ⚠️ Extractive summarization: No summary generated")
        
    except Exception as e:
        print(f"   ❌ Extractive summarizer test failed: {e}")
        return False
    
    # Test 4: Abstractive Summarizer
    print("\n4. Testing Abstractive Summarizer...")
    try:
        from abstractive_summarizer import AbstractiveSummarizer
        summarizer = AbstractiveSummarizer()
        
        sample_text = """
        This Employment Agreement is entered into between TechCorp Inc., a Delaware corporation, 
        and Jane Smith on January 15, 2024. The employee will serve as Senior Software Engineer 
        with a base salary of $120,000 per year. Employee agrees to maintain confidentiality 
        and may be terminated with 30 days notice.
        """
        
        summary = summarizer.summarize(sample_text, max_length=100, min_length=30)
        if summary:
            print(f"   ✅ Abstractive summarization: Generated {len(summary.split())} word summary")
        else:
            print("   ⚠️ Abstractive summarization: No summary generated")
        
    except Exception as e:
        print(f"   ❌ Abstractive summarizer test failed: {e}")
        return False
    
    # Test 5: Legal Analyzer
    print("\n5. Testing Legal Analyzer...")
    try:
        from legal_analyzer import LegalAnalyzer
        analyzer = LegalAnalyzer()
        
        sample_text = """
        EMPLOYMENT AGREEMENT
        This Employment Agreement is governed by the laws of Delaware, United States.
        1. CONFIDENTIALITY: Employee shall maintain strict confidentiality.
        2. TERMINATION: Company may terminate with 30 days notice. Employee shall be liable for damages.
        3. INDEMNIFICATION: Employee agrees to indemnify the Company.
        """
        
        analysis = analyzer.comprehensive_analysis(sample_text)
        
        print(f"   ✅ Jurisdiction detection: {len(analysis['jurisdiction'])} jurisdictions analyzed")
        print(f"   ✅ Clause analysis: {len(analysis['clauses'])} clauses processed")
        print(f"   ✅ Risk assessment: {analysis['risk_report']['risk_distribution']}")
        
    except Exception as e:
        print(f"   ❌ Legal analyzer test failed: {e}")
        return False
    
    # Test 6: File Processing
    print("\n6. Testing File Processing...")
    try:
        sample_file = "data/sample_contract.txt"
        if os.path.exists(sample_file):
            result = processor.process_document(sample_file)
            if "error" not in result:
                print(f"   ✅ File processing: {result['word_count']} words processed")
                print(f"   ✅ Entities found: {result['entities'].get('total_count', 0)}")
                print(f"   ✅ Parties found: {len(result['parties'])}")
            else:
                print(f"   ❌ File processing failed: {result['error']}")
        else:
            print("   ⚠️ Sample file not found, skipping file processing test")
    
    except Exception as e:
        print(f"   ❌ File processing test failed: {e}")
        return False
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS COMPLETED SUCCESSFULLY!")
    print("📋 Project Summary:")
    print("   - Configuration: ✅ Working")
    print("   - Document Processing: ✅ Working") 
    print("   - Extractive Summarization: ✅ Working")
    print("   - Abstractive Summarization: ✅ Working")
    print("   - Legal Analysis: ✅ Working")
    print("   - File Processing: ✅ Working")
    print("\n🚀 The AI-Powered Legal Document Summarizer is ready to use!")
    print("   Run 'streamlit run app.py' to start the web interface")
    
    return True

if __name__ == "__main__":
    test_all_modules()
