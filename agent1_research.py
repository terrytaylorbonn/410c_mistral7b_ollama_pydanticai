# agent1_research.py
"""
Agent1: Research Assistant
- Uses your existing RAG system
- Provides factual information from documents
- Runs as FastAPI service on port 8001
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import chromadb
import requests
from pathlib import Path
from typing import List, Dict

app = FastAPI(title="Agent1 - Research Assistant", version="1.0.0")

# Request/Response models
class ResearchRequest(BaseModel):
    question: str
    max_sources: int = 2

class ResearchResponse(BaseModel):
    question: str
    answer: str
    sources: List[str]
    agent: str = "Agent1-Research"

# RAG System (simplified from your rag_file_loader.py)
class SimpleRAG:
    def __init__(self, data_folder="./data", ollama_url="http://localhost:11434"):
        self.data_folder = Path(data_folder)
        self.ollama_url = ollama_url
        self.client = chromadb.Client()
        self.collection = None
        self.setup_knowledge_base()
    
    def setup_knowledge_base(self):
        """Load documents and create vector database"""
        print("Setting up Agent1 knowledge base...")
        
        self.collection = self.client.get_or_create_collection(
            name="agent1_docs",
            metadata={"description": "Agent1 Research Assistant"}
        )
        
        # Load documents
        documents = []
        for file_path in self.data_folder.glob("*.txt"):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Simple chunking
                    words = content.split()
                    chunk_size = 300
                    for i in range(0, len(words), chunk_size):
                        chunk = " ".join(words[i:i + chunk_size])
                        documents.append({
                            "id": f"{file_path.stem}_chunk_{i//chunk_size}",
                            "text": chunk,
                            "source": str(file_path)
                        })
                print(f"Loaded {file_path.name}")
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
        
        if not documents:
            print("No documents found!")
            return
        
        # Get embeddings and add to ChromaDB
        embeddings = []
        texts = []
        ids = []
        metadatas = []
        
        for doc in documents:
            try:
                response = requests.post(
                    f"{self.ollama_url}/api/embeddings",
                    json={"model": "nomic-embed-text", "prompt": doc["text"]},
                    timeout=60
                )
                if response.status_code == 200:
                    embedding = response.json()["embedding"]
                    embeddings.append(embedding)
                    texts.append(doc["text"])
                    ids.append(doc["id"])
                    metadatas.append({"source": doc["source"]})
            except Exception as e:
                print(f"Error processing document: {e}")
                continue
        
        if embeddings:
            self.collection.add(
                embeddings=embeddings,
                documents=texts,
                ids=ids,
                metadatas=metadatas
            )
            print(f"Agent1 knowledge base ready with {len(embeddings)} documents")
    
    def research(self, question: str, max_sources: int = 2) -> Dict:
        """Research a question using RAG"""
        try:
            # Get query embedding
            response = requests.post(
                f"{self.ollama_url}/api/embeddings",
                json={"model": "nomic-embed-text", "prompt": question},
                timeout=60
            )
            
            if response.status_code != 200:
                raise Exception("Failed to get query embedding")
                
            query_embedding = response.json()["embedding"]
            
            # Search documents
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=max_sources,
                include=["documents", "metadatas"]
            )
            
            # Prepare context
            context = "\n\n".join([
                f"{doc[:400]}..." if len(doc) > 400 else doc
                for doc in results["documents"][0]
            ])
            
            # Generate answer
            prompt = f"""Answer this research question based on the provided context. Be factual and concise.

Context: {context}

Question: {question}

Answer:"""

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": prompt,
                    "stream": False,
                    "options": {"num_predict": 80}
                },
                timeout=120
            )
            
            if response.status_code == 200:
                answer = response.json()["response"]
            else:
                answer = "Error generating answer"
            
            return {
                "question": question,
                "answer": answer,
                "sources": [meta["source"] for meta in results["metadatas"][0]]
            }
            
        except Exception as e:
            return {
                "question": question,
                "answer": f"Research error: {str(e)}",
                "sources": []
            }

# Initialize RAG system
rag = SimpleRAG()

@app.get("/")
async def root():
    return {"message": "Agent1 - Research Assistant", "status": "ready"}

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "Agent1-Research"}

@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest):
    """Research a question using RAG system"""
    print(f"Agent1 received research request: {request.question}")
    
    result = rag.research(request.question, request.max_sources)
    
    return ResearchResponse(
        question=result["question"],
        answer=result["answer"],
        sources=result["sources"]
    )

if __name__ == "__main__":
    print("Starting Agent1 - Research Assistant on port 8001...")
    uvicorn.run(app, host="0.0.0.0", port=8001)
