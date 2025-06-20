#!/usr/bin/env python3
"""
Gradio UI for deployed RAG system - can connect to local or remote FastAPI
"""

import gradio as gr
import requests
import json
import os
from typing import List, Tuple
import time

# Configuration
API_BASE_URL = os.environ.get("RAG_API_URL", "http://localhost:8000")

def query_rag_api(query: str, top_k: int = 5) -> Tuple[str, str]:
    """Query the RAG API and return formatted response"""
    if not query.strip():
        return "Please enter a question.", ""
    
    try:
        # Show loading message
        loading_msg = f"🔍 Searching documents for: '{query}'"
        
        # Make API request
        response = requests.post(
            f"{API_BASE_URL}/query",
            json={"query": query, "top_k": top_k},
            timeout=30
        )
        
        if response.status_code != 200:
            error_detail = response.json().get("detail", "Unknown error")
            return f"❌ Error: {error_detail}", ""
        
        result = response.json()
        
        # Format the answer
        answer = result.get("answer", "No answer generated")
        processing_time = result.get("processing_time", 0.0)
        
        # Format sources
        sources = result.get("sources", [])
        sources_text = ""
        if sources:
            sources_text = "📚 **Sources:**\n\n"
            for i, source in enumerate(sources[:3], 1):  # Show top 3 sources
                content = source.get("content", "")
                score = source.get("score", 0.0)
                preview = content[:200] + "..." if len(content) > 200 else content
                sources_text += f"**Source {i}** (Score: {score:.2f}):\n{preview}\n\n"
        
        # Format final response
        formatted_answer = f"""
## 🤖 RAG System Response

{answer}

*Processing time: {processing_time:.2f} seconds*

---

{sources_text}
        """.strip()
        
        return formatted_answer, f"✅ Found {len(sources)} relevant sources"
        
    except requests.exceptions.ConnectionError:
        return f"❌ Connection Error: Could not connect to RAG API at {API_BASE_URL}", "Connection failed"
    except requests.exceptions.Timeout:
        return "❌ Timeout: The request took too long to process", "Request timeout"
    except Exception as e:
        return f"❌ Error: {str(e)}", "Processing error"

def check_api_health() -> str:
    """Check if the API is healthy"""
    try:
        response = requests.get(f"{API_BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            health_data = response.json()
            status = health_data.get("status", "unknown")
            if status == "healthy":
                doc_count = health_data.get("document_count", 0)
                return f"✅ API Status: Healthy | Documents: {doc_count}"
            else:
                return f"⚠️ API Status: {status}"
        else:
            return f"❌ API Status: Error ({response.status_code})"
    except Exception as e:
        return f"❌ API Status: Unavailable ({str(e)})"

def get_system_info() -> str:
    """Get system information"""
    try:
        response = requests.get(f"{API_BASE_URL}/stats", timeout=10)
        if response.status_code == 200:
            stats = response.json()
            info = f"""
**System Information:**
- Document Count: {stats.get('document_count', 'Unknown')}
- Embedding Model: {stats.get('embedding_model', 'Unknown')}
- Deployment Mode: {stats.get('deployment_mode', 'Unknown')}
- API URL: {API_BASE_URL}
            """.strip()
            return info
        else:
            return "Could not retrieve system information"
    except Exception as e:
        return f"Error getting system info: {str(e)}"

# Create Gradio interface
def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(
        title="RAG System - Document Q&A",
        theme=gr.themes.Soft(),
        css="""
        .gradio-container {
            max-width: 900px !important;
        }
        """
    ) as interface:
        
        gr.Markdown("""
        # 📚 RAG System - Document Q&A
        
        Ask questions about the documents in the system and get AI-powered answers with source references.
        """)
        
        # Status section
        with gr.Row():
            with gr.Column(scale=2):
                status_text = gr.Textbox(
                    label="System Status",
                    value=check_api_health(),
                    interactive=False,
                    lines=1
                )
            with gr.Column(scale=1):
                refresh_btn = gr.Button("🔄 Refresh Status", size="sm")
        
        # Main query interface
        with gr.Row():
            with gr.Column():
                query_input = gr.Textbox(
                    label="Your Question",
                    placeholder="Ask anything about the documents... (e.g., 'What is quantum computing?')",
                    lines=2
                )
                
                with gr.Row():
                    submit_btn = gr.Button("🔍 Search Documents", variant="primary")
                    clear_btn = gr.Button("🗑️ Clear", variant="secondary")
                
                top_k_slider = gr.Slider(
                    minimum=1,
                    maximum=10,
                    value=5,
                    step=1,
                    label="Number of sources to retrieve"
                )
        
        # Results section
        with gr.Row():
            with gr.Column():
                answer_output = gr.Markdown(
                    label="Answer",
                    value="*Enter a question above to get started...*"
                )
                
                result_status = gr.Textbox(
                    label="Status",
                    value="Ready to search",
                    interactive=False,
                    lines=1
                )
        
        # System info section
        with gr.Accordion("System Information", open=False):
            system_info = gr.Markdown(value=get_system_info())
            info_refresh_btn = gr.Button("🔄 Refresh Info")
        
        # Example queries
        with gr.Accordion("Example Queries", open=False):
            gr.Markdown("""
            **Try these example questions:**
            - What is quantum computing?
            - How does machine learning work?
            - What are the main topics in the documents?
            - Explain artificial intelligence
            - What is mentioned about algorithms?
            """)
            
            example_buttons = [
                gr.Button("What is quantum computing?", size="sm"),
                gr.Button("How does machine learning work?", size="sm"),
                gr.Button("What are the main topics?", size="sm")
            ]
        
        # Event handlers
        submit_btn.click(
            fn=query_rag_api,
            inputs=[query_input, top_k_slider],
            outputs=[answer_output, result_status]
        )
        
        query_input.submit(  # Enter key submission
            fn=query_rag_api,
            inputs=[query_input, top_k_slider],
            outputs=[answer_output, result_status]
        )
        
        clear_btn.click(
            fn=lambda: ("", "*Enter a question above to get started...*", "Ready to search"),
            outputs=[query_input, answer_output, result_status]
        )
        
        refresh_btn.click(
            fn=check_api_health,
            outputs=[status_text]
        )
        
        info_refresh_btn.click(
            fn=get_system_info,
            outputs=[system_info]
        )
        
        # Example button handlers
        for i, btn in enumerate(example_buttons):
            example_queries = [
                "What is quantum computing?",
                "How does machine learning work?",
                "What are the main topics in the documents?"
            ]
            btn.click(
                fn=lambda q=example_queries[i]: q,
                outputs=[query_input]
            )
    
    return interface

if __name__ == "__main__":
    print(f"🚀 Starting Gradio UI...")
    print(f"📡 Connecting to RAG API at: {API_BASE_URL}")
    
    # Check API health on startup
    health_status = check_api_health()
    print(f"🏥 API Health: {health_status}")
    
    # Create and launch interface
    interface = create_interface()
    interface.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        debug=True
    )
