"""
Ultra-simplified RAG loader for deployment environments
Uses only basic Python libraries - no heavy ML dependencies
Compatible with any Python 3.8+ environment
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
import re
import math
from collections import Counter

class UltraSimpleRAGSystem:
    """Ultra-simple RAG system using only basic Python libraries"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.documents = []
        self.is_initialized = False
        
    def load_documents(self) -> List[Dict[str, Any]]:
        """Load documents from the data directory"""
        documents = []
        
        if not self.data_dir.exists():
            print(f"Data directory {self.data_dir} not found")
            return documents
            
        # Load text files
        for file_path in self.data_dir.glob("*.txt"):
            try:
                content = file_path.read_text(encoding='utf-8')
                documents.append({
                    "content": content,
                    "metadata": {
                        "source": file_path.name,
                        "path": str(file_path),
                        "type": "text"
                    }
                })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
        # Load markdown files
        for file_path in self.data_dir.glob("*.md"):
            try:
                content = file_path.read_text(encoding='utf-8')
                documents.append({
                    "content": content,
                    "metadata": {
                        "source": file_path.name,
                        "path": str(file_path),
                        "type": "markdown"
                    }
                })
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
        print(f"Loaded {len(documents)} documents")
        return documents
    
    def simple_tokenize(self, text: str) -> List[str]:
        """Simple tokenization using regex"""
        # Convert to lowercase and extract words
        words = re.findall(r'\b\w+\b', text.lower())
        # Remove common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should', 'could', 'can', 'may', 'might', 'must', 'shall', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'}
        return [word for word in words if word not in stop_words and len(word) > 2]
    
    def calculate_similarity(self, query_words: List[str], doc_words: List[str]) -> float:
        """Calculate simple word overlap similarity"""
        if not query_words or not doc_words:
            return 0.0
        
        query_set = set(query_words)
        doc_set = set(doc_words)
        
        # Calculate Jaccard similarity
        intersection = len(query_set.intersection(doc_set))
        union = len(query_set.union(doc_set))
        
        if union == 0:
            return 0.0
        
        jaccard = intersection / union
        
        # Boost score for documents with more query word occurrences
        doc_counter = Counter(doc_words)
        query_matches = sum(doc_counter[word] for word in query_words if word in doc_counter)
        boost = min(query_matches / len(query_words), 2.0)  # Cap boost at 2x
        
        return jaccard * boost
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search documents using simple word matching"""
        if not self.documents:
            self.documents = self.load_documents()
            
        if not self.documents:
            return []
            
        query_words = self.simple_tokenize(query)
        if not query_words:
            return []
        
        results = []
        
        for doc in self.documents:
            doc_words = self.simple_tokenize(doc["content"])
            similarity = self.calculate_similarity(query_words, doc_words)
            
            if similarity > 0:
                results.append({
                    "content": doc["content"],
                    "metadata": doc["metadata"],
                    "score": similarity
                })
        
        # Sort by similarity score
        results.sort(key=lambda x: x["score"], reverse=True)
        
        # Return top-k results
        return results[:top_k]
    
    def generate_answer(self, query: str, relevant_docs: List[Dict[str, Any]]) -> str:
        """Generate a simple answer based on relevant documents"""
        if not relevant_docs:
            return "I couldn't find any relevant information in the documents to answer your query."
        
        # Simple answer generation - combine relevant snippets
        answer_parts = []
        query_words = self.simple_tokenize(query)
        
        for doc in relevant_docs[:3]:  # Use top 3 documents
            content = doc["content"]
            source = doc["metadata"]["source"]
            
            # Find sentences containing query words
            sentences = re.split(r'[.!?]+', content)
            relevant_sentences = []
            
            for sentence in sentences:
                sentence = sentence.strip()
                if len(sentence) > 20:  # Skip very short sentences
                    sentence_words = self.simple_tokenize(sentence)
                    if any(word in sentence_words for word in query_words):
                        relevant_sentences.append(sentence)
            
            # Take the best sentence(s)
            if relevant_sentences:
                best_sentence = relevant_sentences[0]  # First matching sentence
                answer_parts.append(f"From {source}: {best_sentence}")
        
        if answer_parts:
            answer = "Based on the available documents:\n\n" + "\n\n".join(answer_parts)
        else:
            # Fallback to first part of most relevant document
            doc = relevant_docs[0]
            content_preview = doc["content"][:300] + "..." if len(doc["content"]) > 300 else doc["content"]
            answer = f"From {doc['metadata']['source']}: {content_preview}"
        
        return answer

# Global instance for the RAG system
_rag_system = None

def get_rag_system() -> UltraSimpleRAGSystem:
    """Get or create the global RAG system instance"""
    global _rag_system
    if _rag_system is None:
        _rag_system = UltraSimpleRAGSystem()
    return _rag_system

def load_and_query_documents(query: str, data_dir: str = "./data", top_k: int = 3) -> Dict[str, Any]:
    """
    Main function compatible with existing code
    Load documents and query them using ultra-simple RAG
    """
    start_time = time.time()
    
    rag_system = get_rag_system()
    
    # Update data directory if different
    if str(rag_system.data_dir) != data_dir:
        rag_system.data_dir = Path(data_dir)
    
    # Search for relevant documents
    relevant_docs = rag_system.search_documents(query, top_k)
    
    # Generate answer
    answer = rag_system.generate_answer(query, relevant_docs)
    
    processing_time = time.time() - start_time
    
    return {
        "answer": answer,
        "sources": relevant_docs,
        "processing_time": processing_time,
        "model_used": "ultra_simple_word_matching",
        "query": query
    }

# Fallback function that tries to use the original RAG system first
def load_and_query_documents_with_fallback(query: str, data_dir: str = "./data", top_k: int = 3) -> Dict[str, Any]:
    """
    Try to use the original RAG system, fallback to simple version
    """
    try:
        # Try to import and use the original system
        from rag_file_loader import load_and_query_documents as original_query
        return original_query(query, data_dir, top_k)
    except Exception as e:
        print(f"Original RAG system not available ({e}), using simple fallback")
        return load_and_query_documents(query, data_dir, top_k)

if __name__ == "__main__":
    # Test the simple RAG system
    test_query = "What is this system about?"
    result = load_and_query_documents(test_query)
    
    print(f"Query: {test_query}")
    print(f"Answer: {result['answer']}")
    print(f"Sources found: {len(result['sources'])}")
    print(f"Processing time: {result['processing_time']:.2f} seconds")
