"""
Simple Gradio UI for the Local RAG System
Provides a web interface for querying documents and comparing with OpenAI
"""

import gradio as gr
import os
import sys
import time
from pathlib import Path

# Add current directory to path for imports
sys.path.append(str(Path(__file__).parent))

# Import our RAG functions with fallback
try:
    # Try to use the original RAG system first
    from rag_file_loader import load_and_query_documents
    print("Using original RAG system with Ollama")
except ImportError:
    try:
        # Fallback to simple deployment-friendly version
        from simple_rag_deploy import load_and_query_documents
        print("Using simple RAG system (deployment mode)")
    except ImportError as e:
        print(f"Import error: {e}")
        print("Neither RAG system available")
        
        # Create a dummy function as last resort
        def load_and_query_documents(query, data_dir="./data", top_k=3):
            return {
                "answer": "RAG system not available. Please check the setup.",
                "sources": [],
                "processing_time": 0
            }

# Import OpenAI functionality with fallback
try:
    from openai_rag_demo import query_openai_rag
except ImportError:
    print("OpenAI RAG demo not available")
    
    def query_openai_rag(query):
        return {
            "answer": "OpenAI integration not available in this deployment",
            "model_used": "none",
            "tokens_used": 0,
            "cost_estimate": 0
        }

def query_local_rag(query: str, top_k: int = 3):
    """Query the local RAG system"""
    if not query.strip():
        return "Please enter a query."
    
    try:
        start_time = time.time()
        result = load_and_query_documents(
            query=query,
            data_dir="./data",
            top_k=top_k
        )
        end_time = time.time()
        
        # Format the response
        response = f"**Answer:** {result['answer']}\n\n"
        response += f"**Processing Time:** {end_time - start_time:.2f} seconds\n\n"
        response += f"**Sources Found:** {len(result['sources'])}\n\n"
        
        for i, source in enumerate(result['sources'][:top_k], 1):
            response += f"**Source {i}:** {source.get('metadata', {}).get('source', 'Unknown')} "
            response += f"(Score: {source.get('score', 0):.2f})\n"
            response += f"Content: {source.get('content', '')[:200]}...\n\n"
        
        return response
        
    except Exception as e:
        return f"Error querying local RAG: {str(e)}"

def query_openai_comparison(query: str):
    """Query OpenAI for comparison (if API key is available)"""
    if not query.strip():
        return "Please enter a query."
    
    # Check if OpenAI API key is available
    if not os.getenv("OPENAI_API_KEY"):
        return "OpenAI API key not found. Set OPENAI_API_KEY environment variable to use this feature."
    
    try:
        start_time = time.time()
        result = query_openai_rag(query)
        end_time = time.time()
        
        response = f"**OpenAI Answer:** {result.get('answer', 'No answer provided')}\n\n"
        response += f"**Processing Time:** {end_time - start_time:.2f} seconds\n\n"
        response += f"**Model Used:** {result.get('model_used', 'Unknown')}\n"
        response += f"**Tokens Used:** {result.get('tokens_used', 'Unknown')}\n"
        response += f"**Estimated Cost:** ${result.get('cost_estimate', 'Unknown')}\n"
        
        return response
        
    except Exception as e:
        return f"Error querying OpenAI: {str(e)}"

def query_both_systems(query: str, top_k: int = 3):
    """Query both local and OpenAI systems for comparison"""
    if not query.strip():
        return "Please enter a query.", "Please enter a query."
    
    local_result = query_local_rag(query, top_k)
    openai_result = query_openai_comparison(query)
    
    return local_result, openai_result

def check_system_status():
    """Check the status of various system components"""
    status = "## System Status\n\n"
    
    # Check data directory
    data_dir = Path("./data")
    if data_dir.exists():
        txt_files = list(data_dir.glob("*.txt"))
        md_files = list(data_dir.glob("*.md"))
        total_files = len(txt_files) + len(md_files)
        status += f"✅ Data directory: {total_files} documents found\n"
    else:
        status += "❌ Data directory not found\n"
    
    # Check OpenAI API key
    if os.getenv("OPENAI_API_KEY"):
        status += "✅ OpenAI API key configured\n"
    else:
        status += "⚠️ OpenAI API key not configured\n"
    
    # Check Ollama (this would require testing connection)
    status += "ℹ️ Ollama status: Check manually with `ollama list`\n"
    
    return status

# Create the Gradio interface
def create_interface():
    """Create and configure the Gradio interface"""
    
    with gr.Blocks(
        title="Local RAG + Multi-Agent System",
        theme=gr.themes.Soft(),
    ) as app:
        
        gr.Markdown("""
        # 🤖 Local RAG + Multi-Agent System
        
        Query your local documents using AI models and compare with OpenAI results.
        
        **Features:**
        - 🏠 Local RAG with Mistral 7B/Phi-3 via Ollama
        - 🌐 OpenAI comparison (requires API key)
        - 📊 Side-by-side result comparison
        - 📁 Automatic document indexing from `data/` directory
        """)
        
        with gr.Tab("RAG Query"):
            with gr.Row():
                with gr.Column():
                    query_input = gr.Textbox(
                        label="Enter your query",
                        placeholder="What would you like to know about your documents?",
                        lines=3
                    )
                    top_k_slider = gr.Slider(
                        minimum=1,
                        maximum=10,
                        value=3,
                        step=1,
                        label="Number of sources to retrieve"
                    )
                    
                    with gr.Row():
                        local_btn = gr.Button("Query Local RAG", variant="primary")
                        openai_btn = gr.Button("Query OpenAI", variant="secondary")
                        both_btn = gr.Button("Compare Both", variant="stop")
            
            with gr.Row():
                with gr.Column():
                    gr.Markdown("### Local RAG Results")
                    local_output = gr.Markdown(label="Local Results")
                
                with gr.Column():
                    gr.Markdown("### OpenAI Results")
                    openai_output = gr.Markdown(label="OpenAI Results")
        
        with gr.Tab("System Status"):
            status_btn = gr.Button("Check System Status")
            status_output = gr.Markdown()
        
        with gr.Tab("About"):
            gr.Markdown("""
            ## About This System
            
            This is a local RAG (Retrieval-Augmented Generation) system that allows you to:
            
            1. **Query Local Documents**: Uses ChromaDB for vector storage and local AI models via Ollama
            2. **Compare with OpenAI**: Side-by-side comparison with cloud AI models
            3. **Multi-Agent Architecture**: Research and Writer agents for complex tasks
            4. **GitIngest Integration**: Process GitHub repositories for analysis
            
            ### Setup Requirements
            - Ollama installed with Mistral 7B or Phi-3 Mini models
            - Documents in the `data/` directory
            - Optional: OpenAI API key for comparison features
            
            ### Models Used
            - **Local**: Mistral 7B, Phi-3 Mini (via Ollama)
            - **Cloud**: GPT-3.5-turbo, GPT-4 (via OpenAI API)
            
            ### Data Sources
            The system automatically indexes documents from the `data/` directory including:
            - Text files (.txt)
            - Markdown files (.md)
            - JSON files (.json)
            
            For more information, see the project documentation.
            """)
        
        # Set up event handlers
        local_btn.click(
            fn=query_local_rag,
            inputs=[query_input, top_k_slider],
            outputs=local_output
        )
        
        openai_btn.click(
            fn=query_openai_comparison,
            inputs=query_input,
            outputs=openai_output
        )
        
        both_btn.click(
            fn=query_both_systems,
            inputs=[query_input, top_k_slider],
            outputs=[local_output, openai_output]
        )
        
        status_btn.click(
            fn=check_system_status,
            outputs=status_output
        )
        
        # Add example queries
        gr.Examples(
            examples=[
                ["What is quantum computing?"],
                ["Explain machine learning algorithms"],
                ["How does the repository structure work?"],
                ["What are the main features of this project?"],
            ],
            inputs=query_input
        )
    
    return app

if __name__ == "__main__":
    # Create and launch the interface
    app = create_interface()
    
    # Launch with public access for potential deployment
    app.launch(
        server_name="0.0.0.0",  # Allow external access
        server_port=7860,        # Standard Gradio port
        share=False,             # Set to True for temporary public link
        debug=True               # Enable debug mode
    )
