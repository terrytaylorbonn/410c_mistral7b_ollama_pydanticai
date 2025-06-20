"""
FastAPI wrapper for Render deployment
Combines the RAG system with Gradio UI in a production-ready FastAPI application
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import gradio as gr
import os
import sys
import uvicorn
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

# Import our modules with fallback
try:
    # Try original RAG system first
    from rag_file_loader import load_and_query_documents
    print("Using original RAG system")
except ImportError:
    try:
        # Fallback to deployment-friendly version
        from simple_rag_deploy import load_and_query_documents
        print("Using simple RAG system for deployment")
    except ImportError as e:
        logger.error(f"Import error: {e}")
        # Create dummy function
        def load_and_query_documents(query, data_dir="./data", top_k=3):
            return {
                "answer": "RAG system not available",
                "sources": [],
                "processing_time": 0
            }

try:
    from gradio_ui import create_interface
except ImportError as e:
    logger.error(f"Gradio UI import error: {e}")
    # Create minimal interface
    import gradio as gr
    
    def create_interface():
        def simple_query(query):
            result = load_and_query_documents(query)
            return result["answer"]
        
        return gr.Interface(
            fn=simple_query,
            inputs=gr.Textbox(label="Query"),
            outputs=gr.Textbox(label="Answer"),
            title="Local RAG System"
        )

# Create FastAPI app
app = FastAPI(
    title="Local RAG + Multi-Agent System",
    description="A local RAG system with multi-agent architecture and Gradio UI",
    version="1.0.0",
    docs_url="/api/docs",
    redoc_url="/api/redoc"
)

# Pydantic models for API
class QueryRequest(BaseModel):
    query: str
    top_k: int = 3

class QueryResponse(BaseModel):
    answer: str
    sources: list
    processing_time: float
    model_used: str = "local"

class HealthResponse(BaseModel):
    status: str
    message: str
    components: dict

# Create Gradio interface
gradio_app = create_interface()

# Mount Gradio app
app = gr.mount_gradio_app(app, gradio_app, path="/")

# API Routes
@app.get("/api/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint for deployment monitoring"""
    try:
        # Check data directory
        data_dir = Path("./data")
        data_status = "healthy" if data_dir.exists() else "warning"
        
        # Check environment
        openai_status = "configured" if os.getenv("OPENAI_API_KEY") else "not_configured"
        
        components = {
            "data_directory": data_status,
            "openai_api": openai_status,
            "gradio_ui": "healthy"
        }
        
        overall_status = "healthy" if data_status == "healthy" else "degraded"
        
        return HealthResponse(
            status=overall_status,
            message="RAG system is operational",
            components=components
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/query", response_model=QueryResponse)
async def api_query(request: QueryRequest):
    """API endpoint for RAG queries"""
    try:
        import time
        start_time = time.time()
        
        result = load_and_query_documents(
            query=request.query,
            data_dir="./data",
            top_k=request.top_k
        )
        
        processing_time = time.time() - start_time
        
        return QueryResponse(
            answer=result["answer"],
            sources=result["sources"],
            processing_time=processing_time,
            model_used="local_rag"
        )
    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/status")
async def system_status():
    """Detailed system status endpoint"""
    try:
        data_dir = Path("./data")
        
        if data_dir.exists():
            txt_files = list(data_dir.glob("*.txt"))
            md_files = list(data_dir.glob("*.md"))
            total_files = len(txt_files) + len(md_files)
        else:
            total_files = 0
        
        return {
            "data_directory": {
                "exists": data_dir.exists(),
                "total_files": total_files,
                "txt_files": len(txt_files) if data_dir.exists() else 0,
                "md_files": len(md_files) if data_dir.exists() else 0
            },
            "environment": {
                "openai_api_key": bool(os.getenv("OPENAI_API_KEY")),
                "python_version": sys.version,
                "working_directory": str(Path.cwd())
            },
            "deployment": {
                "platform": os.getenv("RENDER", "local"),
                "port": os.getenv("PORT", "10000")
            }
        }
    except Exception as e:
        logger.error(f"Status check failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Background task for initialization
@app.on_event("startup")
async def startup_event():
    """Initialize the application"""
    logger.info("Starting RAG system...")
    
    # Check if data directory exists
    data_dir = Path("./data")
    if not data_dir.exists():
        logger.warning("Data directory not found, creating...")
        data_dir.mkdir(exist_ok=True)
        
        # Create a sample file
        sample_file = data_dir / "sample.txt"
        sample_file.write_text("""
        Welcome to the Local RAG + Multi-Agent System!
        
        This is a sample document to demonstrate the RAG functionality.
        You can add your own documents to the data directory.
        
        Features:
        - Local AI models via Ollama
        - Vector search with ChromaDB
        - Multi-agent architecture
        - OpenAI comparison
        - GitIngest integration
        """)
        logger.info("Created sample document")
    
    logger.info("RAG system initialized successfully")

# Redirect root to Gradio UI
@app.get("/api")
async def api_root():
    """API root endpoint"""
    return {
        "message": "Local RAG + Multi-Agent System API",
        "docs": "/api/docs",
        "gradio_ui": "/",
        "health": "/api/health"
    }

if __name__ == "__main__":
    # Get port from environment (for Render deployment)
    port = int(os.getenv("PORT", 10000))
    
    # Configure for deployment
    uvicorn.run(
        "fastapi_app:app",
        host="0.0.0.0",
        port=port,
        reload=False,  # Disable reload in production
        access_log=True,
        log_level="info"
    )
