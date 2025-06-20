# simple_rag.py
"""
Ultra-simple RAG that works around timeout issues
Uses streaming responses and minimal context
"""

import requests
import chromadb
import json
from pathlib import Path

class SimpleRAG:
    def __init__(self):
        self.client = chromadb.Client()
        self.collection = None
        self.ollama_url = "http://localhost:11434"
        
    def setup_documents(self):
        """Load and index documents"""
        self.collection = self.client.get_or_create_collection("simple_docs")
        
        # Load your data files
        data_folder = Path("./data")
        docs = []
        
        for txt_file in data_folder.glob("*.txt"):
            with open(txt_file, 'r') as f:
                content = f.read()
                # Simple chunking - split by sentences
                sentences = content.split('. ')
                for i, sentence in enumerate(sentences):
                    if len(sentence.strip()) > 20:  # Skip very short sentences
                        docs.append({
                            "id": f"{txt_file.stem}_{i}",
                            "text": sentence.strip(),
                            "source": txt_file.name
                        })
        
        print(f"Loaded {len(docs)} document chunks")
        
        # Get embeddings and add to ChromaDB
        embeddings = []
        texts = []
        ids = []
        metadatas = []
        
        for doc in docs:
            try:
                # Get embedding
                response = requests.post(
                    f"{self.ollama_url}/api/embeddings",
                    json={"model": "nomic-embed-text", "prompt": doc["text"]},
                    timeout=10
                )
                if response.status_code == 200:
                    embedding = response.json()["embedding"]
                    embeddings.append(embedding)
                    texts.append(doc["text"])
                    ids.append(doc["id"])
                    metadatas.append({"source": doc["source"]})
            except Exception as e:
                print(f"Error processing: {e}")
                continue
        
        if embeddings:
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                ids=ids,
                metadatas=metadatas
            )
            print(f"Added {len(embeddings)} documents to knowledge base")
    
    def search(self, query, n_results=2):
        """Search for relevant documents"""
        # Get query embedding
        response = requests.post(
            f"{self.ollama_url}/api/embeddings",
            json={"model": "nomic-embed-text", "prompt": query},
            timeout=10
        )
        
        if response.status_code == 200:
            query_embedding = response.json()["embedding"]
            
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results
            )
            
            return results["documents"][0]
        return []
    
    def ask_streaming(self, question, model="phi3:mini"):
        """Ask question with streaming response"""
        print(f"\nQuestion: {question}")
        
        # Get relevant documents
        relevant_docs = self.search(question)
        
        if not relevant_docs:
            print("No relevant documents found.")
            return
        
        # Create simple context (just the most relevant sentence)
        context = relevant_docs[0][:200]  # Use only first 200 chars
        
        # Simple prompt
        prompt = f"Based on this: '{context}' Answer: {question}"
        
        # Streaming request
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": True,
                    "options": {"num_predict": 50}  # Very short response
                },
                stream=True,
                timeout=5
            )
            
            print("Answer: ", end="", flush=True)
            for line in response.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            print(data["response"], end="", flush=True)
                        if data.get("done", False):
                            break
                    except:
                        continue
            print()  # New line
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    print("Setting up Simple RAG...")
    rag = SimpleRAG()
    rag.setup_documents()
    
    print("\nReady! Ask short questions:")
    while True:
        question = input("\nQ: ").strip()
        if question.lower() in ['quit', 'q', 'exit']:
            break
        if question:
            rag.ask_streaming(question)
