"""
Simplified RAG loader for deployment environments without Ollama
Uses basic text similarity and TF-IDF for document matching
"""

import os
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SimpleRAGSystem:
    """Simplified RAG system that works without heavy ML dependencies"""
    
    def __init__(self, data_dir: str = "./data"):
        self.data_dir = Path(data_dir)
        self.documents = []
        self.vectorizer = None
        self.tfidf_matrix = None
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
    
    def initialize_vectorizer(self):
        """Initialize the TF-IDF vectorizer with documents"""
        if not self.documents:
            self.documents = self.load_documents()
            
        if not self.documents:
            print("No documents found to initialize vectorizer")
            return
            
        # Extract text content for vectorization
        texts = [doc["content"] for doc in self.documents]
        
        # Initialize and fit TF-IDF vectorizer
        self.vectorizer = TfidfVectorizer(
            max_features=1000,  # Limit features for deployment
            stop_words='english',
            ngram_range=(1, 2),  # Include bigrams
            max_df=0.95,  # Ignore very common terms
            min_df=1  # Include all terms that appear at least once
        )
        
        try:
            self.tfidf_matrix = self.vectorizer.fit_transform(texts)
            self.is_initialized = True
            print(f"Vectorizer initialized with {len(texts)} documents")
        except Exception as e:
            print(f"Error initializing vectorizer: {e}")
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        """Search documents using TF-IDF similarity"""
        if not self.is_initialized:
            self.initialize_vectorizer()
            
        if not self.is_initialized:
            return []
            
        try:
            # Transform query using the same vectorizer
            query_vector = self.vectorizer.transform([query])
            
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vector, self.tfidf_matrix).flatten()
            
            # Get top-k most similar documents (lower threshold)
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            results = []
            for idx in top_indices:
                # Lower threshold to include more results
                if similarities[idx] > 0.001:  # Very low threshold
                    results.append({
                        "content": self.documents[idx]["content"],
                        "metadata": self.documents[idx]["metadata"],
                        "score": float(similarities[idx])
                    })
            
            # If no results, try with the top document regardless of score
            if not results and len(self.documents) > 0:
                best_idx = np.argmax(similarities)
                results.append({
                    "content": self.documents[best_idx]["content"],
                    "metadata": self.documents[best_idx]["metadata"],
                    "score": float(similarities[best_idx])
                })
            
            return results
            
        except Exception as e:
            print(f"Error searching documents: {e}")
            return []
    
    def generate_answer(self, query: str, relevant_docs: List[Dict[str, Any]]) -> str:
        """Generate a simple answer based on relevant documents"""
        if not relevant_docs:
            return "I couldn't find any relevant information in the documents to answer your query."
        
        # Simple answer generation - combine relevant snippets
        answer_parts = []
        
        for doc in relevant_docs[:3]:  # Use top 3 documents
            content = doc["content"]
            source = doc["metadata"]["source"]
            
            # Extract relevant snippet (first 200 characters around query terms)
            query_words = query.lower().split()
            content_lower = content.lower()
            
            # Find best position in content
            best_pos = 0
            best_score = 0
            
            for word in query_words:
                pos = content_lower.find(word)
                if pos != -1:
                    # Count query words in surrounding context
                    start = max(0, pos - 100)
                    end = min(len(content), pos + 100)
                    context = content_lower[start:end]
                    score = sum(1 for w in query_words if w in context)
                    if score > best_score:
                        best_score = score
                        best_pos = pos
            
            # Extract snippet
            start = max(0, best_pos - 100)
            end = min(len(content), best_pos + 200)
            snippet = content[start:end].strip()
            
            if snippet:
                answer_parts.append(f"From {source}: {snippet}")
        
        if answer_parts:
            answer = "Based on the available documents:\n\n" + "\n\n".join(answer_parts)
        else:
            answer = "I found some relevant documents but couldn't extract specific information to answer your query."
        
        return answer

# Global instance for the RAG system
_rag_system = None

def get_rag_system() -> SimpleRAGSystem:
    """Get or create the global RAG system instance"""
    global _rag_system
    if _rag_system is None:
        _rag_system = SimpleRAGSystem()
    return _rag_system

def load_and_query_documents(query: str, data_dir: str = "./data", top_k: int = 3) -> Dict[str, Any]:
    """
    Main function compatible with existing code
    Load documents and query them using simple RAG
    """
    start_time = time.time()
    
    rag_system = get_rag_system()
    
    # Update data directory if different
    if str(rag_system.data_dir) != data_dir:
        rag_system.data_dir = Path(data_dir)
        rag_system.is_initialized = False
    
    # Search for relevant documents
    relevant_docs = rag_system.search_documents(query, top_k)
    
    # Generate answer
    answer = rag_system.generate_answer(query, relevant_docs)
    
    processing_time = time.time() - start_time
    
    return {
        "answer": answer,
        "sources": relevant_docs,
        "processing_time": processing_time,
        "model_used": "simple_tfidf",
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
