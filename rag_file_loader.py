# rag_file_loader.py
"""
RAG system that loads documents from your data/ folder
Works with your existing Mistral 7B setup

NOTE: Optimized for USB SSD setup - responses may take 1-2 minutes
For faster responses, consider using simple_rag.py with streaming
"""

import os
import requests
import chromadb
from pathlib import Path
from typing import List, Dict
import re

class DocumentRAG:
    def __init__(self, data_folder="./data", ollama_url="http://localhost:11434"):
        self.data_folder = Path(data_folder)
        self.ollama_url = ollama_url
        self.client = chromadb.Client()
        self.collection = None
        
    def load_documents_from_folder(self) -> List[Dict]:
        """Load all text files from data folder"""
        documents = []
        
        for file_path in self.data_folder.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                # Split into chunks (simple approach)
                chunks = self.chunk_text(content, chunk_size=500)
                
                for i, chunk in enumerate(chunks):
                    documents.append({
                        "id": f"{file_path.stem}_chunk_{i}",
                        "text": chunk,
                        "source": str(file_path),
                        "chunk_index": i
                    })
                    
                print(f"Loaded {len(chunks)} chunks from {file_path.name}")
                
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                
        return documents
    
    def chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> List[str]:
        """Split text into overlapping chunks"""
        words = text.split()
        chunks = []
        
        for i in range(0, len(words), chunk_size - overlap):
            chunk_words = words[i:i + chunk_size]
            chunk = " ".join(chunk_words)
            chunks.append(chunk)
            
        return chunks
    
    def get_embedding(self, text: str, model="nomic-embed-text") -> List[float]:
        """Get embeddings from Ollama"""
        try:
            response = requests.post(
                f"{self.ollama_url}/api/embeddings",
                json={"model": model, "prompt": text},
                timeout=60  # Longer timeout for USB SSD
            )
            if response.status_code == 200:
                return response.json()["embedding"]
            else:
                raise Exception(f"Embedding failed: {response.text}")
        except Exception as e:
            print(f"Embedding error: {e}")
            raise
    
    def setup_knowledge_base(self, collection_name="file_documents"):
        """Load documents and create vector database"""
        print("Setting up knowledge base...")
        
        # Create collection
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "File-based RAG system"}
        )
        
        # Load documents
        documents = self.load_documents_from_folder()
        
        if not documents:
            print("No documents found in data folder!")
            return
            
        print(f"Processing {len(documents)} document chunks...")
        
        # Prepare data for ChromaDB
        embeddings = []
        texts = []
        ids = []
        metadatas = []
        
        for doc in documents:
            try:
                embedding = self.get_embedding(doc["text"])
                embeddings.append(embedding)
                texts.append(doc["text"])
                ids.append(doc["id"])
                metadatas.append({
                    "source": doc["source"],
                    "chunk_index": doc["chunk_index"]
                })
            except Exception as e:
                print(f"Error processing document {doc['id']}: {e}")
                continue
        
        # Add to ChromaDB
        if embeddings:
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                ids=ids,
                metadatas=metadatas
            )
            print(f"Successfully added {len(embeddings)} documents to knowledge base!")
        
    def search(self, query: str, n_results: int = 3) -> List[Dict]:
        """Search for relevant documents"""
        if not self.collection:
            raise Exception("Knowledge base not set up. Run setup_knowledge_base() first.")
            
        query_embedding = self.get_embedding(query)
        
        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        search_results = []
        for i in range(len(results["documents"][0])):
            search_results.append({
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "distance": results["distances"][0][i]
            })
            
        return search_results
    
    def ask_question(self, question: str, model="mistral") -> Dict:
        """Ask a question and get an answer based on your documents"""
        print(f"\nQuestion: {question}")
        
        # Search for relevant documents
        relevant_docs = self.search(question, n_results=2)  # Reduce to 2 for shorter context
        
        # Create shorter context
        context = "\n\n".join([
            f"{doc['text'][:300]}..." if len(doc['text']) > 300 else doc['text']
            for doc in relevant_docs
        ])
        
        # Shorter, more focused prompt
        prompt = f"""Answer this question using the provided context. Be concise.

Context: {context}

Question: {question}

Answer:"""

        # Try with retries and much longer timeout for USB SSD setup
        answer = None
        for attempt in range(2):  # Reduce to 2 attempts since each takes so long
            try:
                print(f"Generating answer (attempt {attempt + 1})... This may take 1-2 minutes on USB SSD...")
                response = requests.post(
                    f"{self.ollama_url}/api/generate",
                    json={
                        "model": model,
                        "prompt": prompt,
                        "stream": False,
                        "options": {
                            "temperature": 0.3,
                            "top_p": 0.9,
                            "num_predict": 100  # Shorter responses for faster completion
                        }
                    },
                    timeout=120  # 2 minutes timeout for USB SSD setup
                )
                
                if response.status_code == 200:
                    answer = response.json()["response"]
                    break
                else:
                    print(f"HTTP Error: {response.status_code}")
                    if attempt == 1:  # Last attempt
                        answer = f"Error generating answer: {response.text}"
                    
            except requests.exceptions.Timeout:
                print(f"Timeout on attempt {attempt + 1} (this is normal on USB SSD)")
                if attempt == 1:  # Last attempt
                    answer = "Response took longer than 2 minutes. Consider using the streaming version (simple_rag.py) for better experience on USB SSD."
                continue
            except Exception as e:
                print(f"Error on attempt {attempt + 1}: {e}")
                if attempt == 1:  # Last attempt
                    answer = f"Error: {e}"
                break
        
        return {
            "question": question,
            "answer": answer,
            "sources": [doc["source"] for doc in relevant_docs],
            "relevant_chunks": len(relevant_docs)
        }

# Example usage
if __name__ == "__main__":
    print("Setting up RAG system with your documents...")
    
    # Initialize RAG with your data folder
    rag = DocumentRAG(data_folder="./data")
    
    # Set up knowledge base (this will process all .txt files in data/)
    rag.setup_knowledge_base()
    
    # Interactive Q&A
    print("\n" + "="*50)
    print("RAG System Ready! Ask questions about your documents.")
    print("Type 'quit' to exit.")
    print("="*50)
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
            
        if question:
            # Try with phi3:mini first (faster), fallback to mistral
            try:
                result = rag.ask_question(question, model="phi3:mini")
            except:
                print("Trying with mistral model...")
                result = rag.ask_question(question, model="mistral")
                
            print(f"\nAnswer: {result['answer']}")
            print(f"\nSources used: {', '.join(set(result['sources']))}")
