"""
Enhanced legal analyzer with jurisdiction support and clause-by-clause breakdown
"""
import re
import json
from typing import Dict, List, Optional, Tuple
import logging
from pathlib import Path

from config import LEGAL_SECTIONS, CLAUSE_KEYWORDS

logger = logging.getLogger(__name__)

class LegalAnalyzer:
    """Advanced legal document analyzer with jurisdiction and clause analysis"""
    
    def __init__(self):
        """Initialize the legal analyzer"""
        self.jurisdictions = {
            "US": {
                "keywords": ["United States", "U.S.", "federal", "state law"],
                "date_formats": [r"\d{1,2}/\d{1,2}/\d{4}", r"\d{1,2}-\d{1,2}-\d{4}"],
                "contract_types": ["employment", "service", "purchase", "lease", "NDA"]
            },
            "UK": {
                "keywords": ["United Kingdom", "UK", "English law", "British"],
                "date_formats": [r"\d{1,2}/\d{1,2}/\d{4}", r"\d{1,2}.\d{1,2}.\d{4}"],
                "contract_types": ["employment", "service", "sale", "tenancy", "confidentiality"]
            },
            "EU": {
                "keywords": ["European Union", "EU", "GDPR", "European law"],
                "date_formats": [r"\d{1,2}.\d{1,2}.\d{4}", r"\d{1,2}/\d{1,2}/\d{4}"],
                "contract_types": ["employment", "service", "supply", "lease", "data protection"]
            },
            "INDIA": {
                "keywords": ["India", "Indian law", "Supreme Court", "High Court"],
                "date_formats": [r"\d{1,2}/\d{1,2}/\d{4}", r"\d{1,2}-\d{1,2}-\d{4}"],
                "contract_types": ["employment", "service", "sale", "lease", "partnership"]
            }
        }
        
        self.risk_indicators = {
            "high": ["indemnify", "liable", "penalty", "breach", "damages", "liquidated damages"],
            "medium": ["terminate", "confidential", "non-compete", "exclusive", "warranty"],
            "low": ["notice", "amendment", "assignment", "governing law", "severability"]
        }
        
        self.compliance_keywords = {
            "GDPR": ["personal data", "data subject", "data controller", "consent", "privacy"],
            "SOX": ["financial reporting", "internal controls", "audit", "disclosure"],
            "HIPAA": ["protected health information", "PHI", "healthcare", "medical records"],
            "PCI": ["payment card", "cardholder data", "PCI DSS", "credit card"]
        }
    
    def detect_jurisdiction(self, text: str) -> Dict[str, float]:
        """Detect the likely jurisdiction(s) of the document"""
        jurisdiction_scores = {}
        text_lower = text.lower()
        
        for jurisdiction, data in self.jurisdictions.items():
            score = 0
            for keyword in data["keywords"]:
                score += text_lower.count(keyword.lower()) * 2
            
            # Check for jurisdiction-specific date formats
            for date_format in data["date_formats"]:
                matches = re.findall(date_format, text)
                score += len(matches) * 0.5
            
            jurisdiction_scores[jurisdiction] = score
        
        # Normalize scores
        total_score = sum(jurisdiction_scores.values())
        if total_score > 0:
            jurisdiction_scores = {k: v/total_score for k, v in jurisdiction_scores.items()}
        
        return jurisdiction_scores
    
    def analyze_clauses(self, text: str) -> Dict[str, Dict]:
        """Perform detailed clause-by-clause analysis"""
        clauses = {}
        
        # Split text into sections/clauses
        sections = re.split(r'\n\s*\d+\.?\s+', text)
        
        for i, section in enumerate(sections):
            if len(section.strip()) < 50:  # Skip very short sections
                continue
                
            clause_name = f"clause_{i+1}"
            clause_analysis = {
                "text": section.strip(),
                "type": self._classify_clause_type(section),
                "risk_level": self._assess_risk_level(section),
                "key_terms": self._extract_key_terms(section),
                "obligations": self._extract_obligations(section),
                "dates": self._extract_clause_dates(section),
                "parties_mentioned": self._extract_clause_parties(section)
            }
            clauses[clause_name] = clause_analysis
        
        return clauses
    
    def _classify_clause_type(self, clause_text: str) -> str:
        """Classify the type of legal clause"""
        clause_lower = clause_text.lower()
        
        for clause_type, keywords in CLAUSE_KEYWORDS.items():
            for keyword in keywords:
                if keyword.lower() in clause_lower:
                    return clause_type
        
        # Additional classification logic
        if any(word in clause_lower for word in ["payment", "compensation", "salary", "fee"]):
            return "payment_terms"
        elif any(word in clause_lower for word in ["intellectual property", "copyright", "patent"]):
            return "intellectual_property"
        elif any(word in clause_lower for word in ["dispute", "arbitration", "litigation"]):
            return "dispute_resolution"
        else:
            return "general"
    
    def _assess_risk_level(self, clause_text: str) -> str:
        """Assess the risk level of a clause"""
        clause_lower = clause_text.lower()
        
        high_risk_count = sum(1 for keyword in self.risk_indicators["high"] 
                             if keyword in clause_lower)
        medium_risk_count = sum(1 for keyword in self.risk_indicators["medium"] 
                               if keyword in clause_lower)
        low_risk_count = sum(1 for keyword in self.risk_indicators["low"] 
                            if keyword in clause_lower)
        
        if high_risk_count >= 2:
            return "high"
        elif high_risk_count >= 1 or medium_risk_count >= 2:
            return "medium"
        else:
            return "low"
    
    def _extract_key_terms(self, clause_text: str) -> List[str]:
        """Extract key legal terms from a clause"""
        # Common legal terms pattern
        legal_terms_pattern = r'\b(?:shall|must|may|will|agree[sd]?|require[sd]?|obligated?|responsible|liable|indemnif[iy]|warrant[sy]?)\b'
        matches = re.findall(legal_terms_pattern, clause_text, re.IGNORECASE)
        return list(set(matches))
    
    def _extract_obligations(self, clause_text: str) -> List[str]:
        """Extract obligations from a clause"""
        obligations = []
        
        # Pattern for obligations (shall/must + verb)
        obligation_patterns = [
            r'(?:shall|must|will|agree to)\s+([^.;]+)',
            r'(?:is|are)\s+(?:required|obligated)\s+to\s+([^.;]+)',
            r'(?:employee|party|company)\s+(?:shall|must|will)\s+([^.;]+)'
        ]
        
        for pattern in obligation_patterns:
            matches = re.findall(pattern, clause_text, re.IGNORECASE)
            obligations.extend([match.strip() for match in matches])
        
        return obligations[:5]  # Limit to 5 most relevant
    
    def _extract_clause_dates(self, clause_text: str) -> List[str]:
        """Extract dates from a specific clause"""
        date_patterns = [
            r'\b\d{1,2}[\/\-]\d{1,2}[\/\-]\d{2,4}\b',
            r'\b(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{2,4}\b',
            r'\b\d{1,2}\s+(?:days?|months?|years?)\b'
        ]
        
        dates = []
        for pattern in date_patterns:
            matches = re.findall(pattern, clause_text, re.IGNORECASE)
            dates.extend(matches)
        
        return dates
    
    def _extract_clause_parties(self, clause_text: str) -> List[str]:
        """Extract parties mentioned in a specific clause"""
        party_patterns = [
            r'\b(?:company|corporation|employer|employee|contractor|client|customer|vendor|supplier)\b',
            r'\b[A-Z][a-z]+ [A-Z][a-z]+\b',  # Proper names
            r'\b[A-Z][a-z]+ (?:Inc|Corp|LLC|Ltd)\.?\b'  # Company names
        ]
        
        parties = []
        for pattern in party_patterns:
            matches = re.findall(pattern, clause_text, re.IGNORECASE)
            parties.extend(matches)
        
        return list(set(parties))[:3]  # Limit to 3 most relevant
    
    def check_compliance(self, text: str) -> Dict[str, List[str]]:
        """Check for compliance-related keywords and requirements"""
        compliance_results = {}
        text_lower = text.lower()
        
        for compliance_type, keywords in self.compliance_keywords.items():
            found_keywords = []
            for keyword in keywords:
                if keyword.lower() in text_lower:
                    found_keywords.append(keyword)
            
            if found_keywords:
                compliance_results[compliance_type] = found_keywords
        
        return compliance_results
    
    def generate_risk_report(self, clauses: Dict) -> Dict:
        """Generate a comprehensive risk report"""
        risk_summary = {"high": [], "medium": [], "low": []}
        total_clauses = len(clauses)
        
        for clause_name, clause_data in clauses.items():
            risk_level = clause_data.get("risk_level", "low")
            risk_summary[risk_level].append({
                "clause": clause_name,
                "type": clause_data.get("type", "unknown"),
                "key_terms": clause_data.get("key_terms", [])
            })
        
        risk_report = {
            "total_clauses": total_clauses,
            "risk_distribution": {
                "high": len(risk_summary["high"]),
                "medium": len(risk_summary["medium"]),
                "low": len(risk_summary["low"])
            },
            "risk_details": risk_summary,
            "recommendations": self._generate_recommendations(risk_summary)
        }
        
        return risk_report
    
    def _generate_recommendations(self, risk_summary: Dict) -> List[str]:
        """Generate recommendations based on risk analysis"""
        recommendations = []
        
        if len(risk_summary["high"]) > 0:
            recommendations.append("⚠️ High-risk clauses detected. Consider legal review before signing.")
        
        if len(risk_summary["medium"]) > 3:
            recommendations.append("📋 Multiple medium-risk clauses present. Review carefully.")
        
        if len(risk_summary["high"]) == 0 and len(risk_summary["medium"]) <= 2:
            recommendations.append("✅ Overall risk level appears manageable.")
        
        return recommendations
    
    def comprehensive_analysis(self, text: str) -> Dict:
        """Perform comprehensive legal document analysis"""
        return {
            "jurisdiction": self.detect_jurisdiction(text),
            "clauses": self.analyze_clauses(text),
            "compliance": self.check_compliance(text),
            "risk_report": self.generate_risk_report(self.analyze_clauses(text))
        }

def main():
    """Test the legal analyzer"""
    analyzer = LegalAnalyzer()
    
    sample_text = """
    EMPLOYMENT AGREEMENT
    
    This Employment Agreement is governed by the laws of Delaware, United States.
    
    1. CONFIDENTIALITY: Employee shall maintain strict confidentiality of all proprietary information.
    
    2. TERMINATION: Company may terminate this agreement with 30 days notice. Employee shall be liable for any damages.
    
    3. INDEMNIFICATION: Employee agrees to indemnify the Company against all claims.
    
    4. PAYMENT: Company shall pay Employee $120,000 annually, payable monthly.
    """
    
    analysis = analyzer.comprehensive_analysis(sample_text)
    
    print("=== Legal Document Analysis ===")
    print(f"Jurisdiction: {analysis['jurisdiction']}")
    print(f"Number of clauses analyzed: {len(analysis['clauses'])}")
    print(f"Risk distribution: {analysis['risk_report']['risk_distribution']}")
    print(f"Compliance areas: {list(analysis['compliance'].keys())}")

if __name__ == "__main__":
    main()
