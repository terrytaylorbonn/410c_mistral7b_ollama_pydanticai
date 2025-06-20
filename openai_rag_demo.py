# openai_rag_demo.py
"""
Simple OpenAI-powered RAG demo
Compare with local model performance
"""

import os
from openai import OpenAI
from pathlib import Path
import json
from typing import List, Dict
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class OpenAIRAG:
    def __init__(self, api_key: str = None):
        """Initialize with OpenAI API key"""
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key required. Set OPENAI_API_KEY environment variable or pass api_key parameter.")
        
        # Set up OpenAI client (new format)
        self.client = OpenAI(api_key=self.api_key)
        
        # Simple document storage
        self.documents = []
        self.vectorizer = TfidfVectorizer(stop_words='english', max_features=1000)
        self.doc_vectors = None
        
    def load_documents(self, data_folder: str = "./data"):
        """Load all text files from data folder"""
        data_path = Path(data_folder)
        self.documents = []
        
        print(f"Loading documents from {data_path}...")
        
        for txt_file in data_path.glob("*.txt"):
            try:
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Simple chunking - split by paragraphs
                chunks = content.split('\n\n')
                
                for i, chunk in enumerate(chunks):
                    if len(chunk.strip()) > 50:  # Skip very short chunks
                        self.documents.append({
                            'content': chunk.strip(),
                            'source': txt_file.name,
                            'chunk_id': f"{txt_file.stem}_{i}"
                        })
                
                print(f"  Loaded {txt_file.name}: {len([c for c in chunks if len(c.strip()) > 50])} chunks")
                
            except Exception as e:
                print(f"  Error loading {txt_file}: {e}")
        
        if self.documents:
            # Create TF-IDF vectors for all documents
            doc_texts = [doc['content'] for doc in self.documents]
            self.doc_vectors = self.vectorizer.fit_transform(doc_texts)
            print(f"\nTotal documents loaded: {len(self.documents)}")
        else:
            print("No documents found!")
    
    def search_documents(self, query: str, top_k: int = 3) -> List[Dict]:
        """Find most relevant documents using TF-IDF similarity"""
        if not self.documents or self.doc_vectors is None:
            return []
        
        # Vectorize the query
        query_vector = self.vectorizer.transform([query])
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, self.doc_vectors).flatten()
        
        # Get top-k most similar documents
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0:  # Only include documents with some similarity
                results.append({
                    'content': self.documents[idx]['content'],
                    'source': self.documents[idx]['source'],
                    'chunk_id': self.documents[idx]['chunk_id'],
                    'similarity': float(similarities[idx])
                })
        
        return results
    
    def ask_openai(self, question: str, context_docs: List[Dict]) -> str:
        """Ask OpenAI using retrieved context"""
        
        # Build context from retrieved documents
        context = ""
        for i, doc in enumerate(context_docs, 1):
            context += f"Source {i} ({doc['source']}):\n{doc['content']}\n\n"
        
        # Create prompt
        prompt = f"""Based on the following context documents, answer the question. Be accurate and cite which sources you're using.

Context:
{context}

Question: {question}

Answer:"""

        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",  # or "gpt-4" if you have access
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that answers questions based on provided context. Always cite your sources."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=300,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"OpenAI API Error: {e}"
    
    def answer_question(self, question: str) -> Dict:
        """Complete RAG pipeline: search + generate answer"""
        print(f"\nQuestion: {question}")
        print("-" * 50)
        
        # Step 1: Retrieve relevant documents
        print("🔍 Searching for relevant documents...")
        relevant_docs = self.search_documents(question, top_k=3)
        
        if not relevant_docs:
            return {
                "question": question,
                "answer": "No relevant documents found.",
                "sources": [],
                "context_used": []
            }
        
        print(f"Found {len(relevant_docs)} relevant documents:")
        for i, doc in enumerate(relevant_docs, 1):
            print(f"  {i}. {doc['source']} (similarity: {doc['similarity']:.3f})")
        
        # Step 2: Generate answer with OpenAI
        print("\n🤖 Generating answer with OpenAI...")
        answer = self.ask_openai(question, relevant_docs)
        
        return {
            "question": question,
            "answer": answer,
            "sources": [doc['source'] for doc in relevant_docs],
            "context_used": relevant_docs
        }

def main():
    """Interactive demo"""
    print("🚀 OPENAI RAG DEMO")
    print("=" * 40)
    
    # Get API key
    api_key = input("Enter your OpenAI API key (or press Enter if set in environment): ").strip()
    if not api_key:
        api_key = os.getenv('OPENAI_API_KEY')
    
    if not api_key:
        print("❌ OpenAI API key required!")
        print("Set OPENAI_API_KEY environment variable or enter it when prompted.")
        return
    
    try:
        # Initialize RAG system
        rag = OpenAIRAG(api_key=api_key)
        
        # Load documents
        rag.load_documents("./data")
        
        if not rag.documents:
            print("❌ No documents found in ./data folder!")
            return
        
        print("\n" + "=" * 50)
        print("OpenAI RAG System Ready!")
        print("Type 'quit' to exit.")
        print("=" * 50)
        
        # Interactive Q&A
        while True:
            question = input("\nYour question: ").strip()
            
            if question.lower() in ['quit', 'exit', 'q']:
                break
                
            if question:
                result = rag.answer_question(question)
                
                print(f"\n✅ Answer:")
                print(result['answer'])
                
                print(f"\n📚 Sources used:")
                for source in set(result['sources']):
                    print(f"  - {source}")
                
                # Show context details
                print(f"\n🔍 Context details:")
                for i, doc in enumerate(result['context_used'], 1):
                    print(f"  {i}. {doc['source']} (similarity: {doc['similarity']:.3f})")
                    print(f"     Preview: {doc['content'][:100]}...")
                    print()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
