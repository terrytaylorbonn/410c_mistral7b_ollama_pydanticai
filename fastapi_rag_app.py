#!/usr/bin/env python3
"""
FastAPI wrapper for RAG system - Render deployment ready
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import os
from typing import List, Dict, Any
import json
import traceback

# Import our deployment-ready RAG system
from simple_rag_deploy import DeploymentRAG

app = FastAPI(
    title="Local RAG System API",
    description="RAG system with local embeddings for deployment",
    version="1.0.0"
)

# Enable CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize RAG system
rag_system = None

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5

class QueryResponse(BaseModel):
    answer: str
    sources: List[Dict[str, Any]]
    processing_time: float
    success: bool
    error: str = None

@app.on_event("startup")
async def startup_event():
    """Initialize RAG system on startup"""
    global rag_system
    try:
        print("🚀 Initializing RAG system...")
        rag_system = DeploymentRAG()
        print("✅ RAG system initialized successfully")
    except Exception as e:
        print(f"❌ Failed to initialize RAG system: {e}")
        traceback.print_exc()

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "RAG System API is running",
        "status": "healthy",
        "version": "1.0.0",
        "rag_initialized": rag_system is not None
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    try:
        if rag_system is None:
            return {
                "status": "unhealthy",
                "message": "RAG system not initialized",
                "rag_initialized": False
            }
        
        # Test a simple query
        test_result = rag_system.query("test", top_k=1)
        
        return {
            "status": "healthy",
            "message": "All systems operational",
            "rag_initialized": True,
            "document_count": len(rag_system.documents) if hasattr(rag_system, 'documents') else 0,
            "test_query_success": test_result.get('success', False)
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "message": f"Health check failed: {str(e)}",
            "rag_initialized": rag_system is not None
        }

@app.post("/query", response_model=QueryResponse)
async def query_documents(request: QueryRequest):
    """Query the RAG system"""
    try:
        if rag_system is None:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        print(f"📝 Processing query: {request.query}")
        
        result = rag_system.query(request.query, top_k=request.top_k)
        
        if not result.get('success', False):
            raise HTTPException(status_code=500, detail=result.get('error', 'Query processing failed'))
        
        return QueryResponse(
            answer=result['answer'],
            sources=result['sources'],
            processing_time=result.get('processing_time', 0.0),
            success=True
        )
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"❌ Query error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

@app.get("/documents")
async def list_documents():
    """List available documents"""
    try:
        if rag_system is None:
            raise HTTPException(status_code=503, detail="RAG system not initialized")
        
        documents = []
        if hasattr(rag_system, 'documents'):
            for i, doc in enumerate(rag_system.documents):
                documents.append({
                    "index": i,
                    "preview": doc[:100] + "..." if len(doc) > 100 else doc,
                    "length": len(doc)
                })
        
        return {
            "total_documents": len(documents),
            "documents": documents
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing documents: {str(e)}")

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        if rag_system is None:
            return {"error": "RAG system not initialized"}
        
        stats = {
            "system_status": "operational",
            "document_count": len(rag_system.documents) if hasattr(rag_system, 'documents') else 0,
            "embedding_model": "TF-IDF (local)",
            "deployment_mode": "cloud_ready"
        }
        
        return stats
        
    except Exception as e:
        return {"error": f"Error getting stats: {str(e)}"}

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(
        "fastapi_rag_app:app",
        host="0.0.0.0",
        port=port,
        reload=True
    )
