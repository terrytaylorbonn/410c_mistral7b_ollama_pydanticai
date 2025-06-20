"""
Ultra-minimal Gradio app for Render deployment
Just the essentials - nothing fancy
"""

import gradio as gr
import os
from pathlib import Path

def simple_query(question):
    """Ultra-simple document search"""
    if not question.strip():
        return "Please enter a question."
    
    # Look for documents in data directory
    data_dir = Path("./data")
    if not data_dir.exists():
        return "No documents found. Add some .txt files to the data directory."
    
    # Find text files
    txt_files = list(data_dir.glob("*.txt"))
    if not txt_files:
        return "No .txt files found in data directory."
    
    # Simple search - just look for query words in files
    results = []
    query_words = question.lower().split()
    
    for txt_file in txt_files:
        try:
            content = txt_file.read_text(encoding='utf-8')
            content_lower = content.lower()
            
            # Count matches
            matches = sum(1 for word in query_words if word in content_lower)
            if matches > 0:
                # Get first 200 chars
                preview = content[:200] + "..." if len(content) > 200 else content
                results.append(f"**{txt_file.name}** (matches: {matches})\n{preview}\n")
        except Exception as e:
            continue
    
    if results:
        return f"Found {len(results)} relevant document(s):\n\n" + "\n".join(results[:3])
    else:
        return f"No matches found for '{question}' in {len(txt_files)} documents."

def main():
    """Create the simplest possible Gradio interface"""
    
    # Create interface
    demo = gr.Interface(
        fn=simple_query,
        inputs=gr.Textbox(
            label="Ask a question about your documents",
            placeholder="What would you like to know?",
            lines=2
        ),
        outputs=gr.Textbox(
            label="Answer",
            lines=10
        ),
        title="🤖 Simple Document Search",
        description="Upload .txt files to the data/ directory and ask questions about them.",
        examples=[
            ["What is this about?"],
            ["Tell me about quantum computing"],
            ["What are the main features?"]
        ]
    )
    
    # Launch
    port = int(os.getenv("PORT", 7860))
    demo.launch(
        server_name="0.0.0.0",
        server_port=port,
        share=False
    )

if __name__ == "__main__":
    main()
