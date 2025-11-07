"""
RAG Knowledge Base Module
Handles loading and searching FAQ data from Excel file
"""

import pandas as pd
from typing import List, Dict, Optional
import os


class FAQKnowledgeBase:
    """Manages FAQ knowledge base from Excel file"""
    
    # Common Spanish punctuation to strip from words
    PUNCTUATION = '¿?.,;:'
    
    def __init__(self, excel_file: str = "faq_grupo_lazarus.xlsx"):
        """
        Initialize the knowledge base
        
        Args:
            excel_file: Path to the Excel file containing FAQ data
        """
        self.excel_file = excel_file
        self.faqs: List[Dict[str, str]] = []
        self.load_data()
    
    def load_data(self) -> None:
        """Load FAQ data from Excel file"""
        if not os.path.exists(self.excel_file):
            raise FileNotFoundError(f"Excel file not found: {self.excel_file}")
        
        try:
            df = pd.read_excel(self.excel_file, engine='openpyxl')
            
            # Convert DataFrame to list of dictionaries
            for _, row in df.iterrows():
                self.faqs.append({
                    'pregunta': str(row['Pregunta']),
                    'respuesta': str(row['Respuesta']),
                    'categoria': str(row.get('Categoría', 'General'))
                })
            
            print(f"✓ Loaded {len(self.faqs)} FAQs from {self.excel_file}")
        except Exception as e:
            raise Exception(f"Error loading Excel file: {str(e)}")
    
    def search(self, query: str, threshold: float = 0.2) -> Optional[Dict[str, str]]:
        """
        Enhanced keyword-based search in FAQ database
        
        Args:
            query: User's question
            threshold: Minimum similarity threshold
        
        Returns:
            Best matching FAQ or None if no match found
        """
        query_lower = query.lower()
        best_match = None
        best_score = 0
        
        # Remove common stopwords and punctuation
        stopwords = {'de', 'la', 'el', 'en', 'y', 'a', 'los', 'las', 'del', 'al', 
                     'es', 'un', 'una', 'con', 'por', 'para', 'su', 'sus', 'que', '¿', '?', 
                     'están', 'estan', 'como', 'cual', 'cuales'}
        
        # Word mappings for better matching
        word_mappings = {
            'donde': 'ubicad',
            'ubicacion': 'ubicad',
            'oficina': 'ubicad',
            'direccion': 'ubicad',
        }
        
        # Clean query
        query_words = [w.strip(self.PUNCTUATION) for w in query_lower.split() 
                      if w.strip(self.PUNCTUATION) not in stopwords]
        # Apply mappings
        query_words = [word_mappings.get(w, w) for w in query_words]
        
        for faq in self.faqs:
            pregunta_lower = faq['pregunta'].lower()
            respuesta_lower = faq['respuesta'].lower()
            categoria_lower = faq['categoria'].lower()
            
            # Clean FAQ question
            pregunta_words = [w.strip(self.PUNCTUATION) for w in pregunta_lower.split() 
                            if w.strip(self.PUNCTUATION) not in stopwords]
            
            score = 0
            
            # Check for substring matches (more flexible)
            for query_word in query_words:
                # Check in question
                for pregunta_word in pregunta_words:
                    if query_word in pregunta_word or pregunta_word in query_word:
                        score += 0.4
                    if query_word == pregunta_word:
                        score += 0.2
                
                # Check in category
                if query_word in categoria_lower:
                    score += 0.3
                
                # Check in answer (less weight)
                if query_word in respuesta_lower:
                    score += 0.1
            
            # Normalize score
            if len(query_words) > 0:
                score = score / len(query_words)
                
                # Bonus for exact phrase match
                if query_lower in pregunta_lower or query_lower in respuesta_lower:
                    score += 0.5
                
                if score > best_score and score > threshold:
                    best_score = score
                    best_match = faq
        
        return best_match
    
    def get_all_faqs(self) -> List[Dict[str, str]]:
        """Return all FAQs"""
        return self.faqs
    
    def get_faqs_by_category(self, category: str) -> List[Dict[str, str]]:
        """Get FAQs filtered by category"""
        return [faq for faq in self.faqs if faq['categoria'].lower() == category.lower()]
