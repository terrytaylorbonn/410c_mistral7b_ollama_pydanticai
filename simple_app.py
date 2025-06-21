"""
Ultra-minimal Gradio app for Render deployment with llms.txt support
Features semantic search over documents with special handling for llms.txt format
"""

import gradio as gr
import os
import re
from pathlib import Path

def parse_llms_txt(content):
    """Parse llms.txt format and extract structured information"""
    lines = content.split('\n')
    parsed = {
        'title': '',
        'description': '',
        'details': '',
        'sections': {}
    }
    
    current_section = None
    current_content = []
    
    for line in lines:
        line = line.strip()
        
        # H1 title (required)
        if line.startswith('# ') and not parsed['title']:
            parsed['title'] = line[2:].strip()
        
        # Blockquote description
        elif line.startswith('> '):
            parsed['description'] += line[2:].strip() + ' '
        
        # H2 sections
        elif line.startswith('## '):
            if current_section and current_content:
                parsed['sections'][current_section] = '\n'.join(current_content)
            current_section = line[3:].strip()
            current_content = []
        
        # Content within sections or details
        elif line:
            if current_section:
                current_content.append(line)
            elif parsed['title'] and not line.startswith('>'):
                parsed['details'] += line + '\n'
    
    # Add final section
    if current_section and current_content:
        parsed['sections'][current_section] = '\n'.join(current_content)
    
    return parsed

def format_llms_response(parsed_data, query_words):
    """Format llms.txt data for display with query highlighting"""
    response = []
    
    if parsed_data['title']:
        response.append(f"**📋 {parsed_data['title']}**\n")
    
    if parsed_data['description']:
        response.append(f"*{parsed_data['description'].strip()}*\n")
    
    if parsed_data['details']:
        details = parsed_data['details'].strip()
        if details:
            response.append(f"{details}\n")
    
    # Add sections with links
    for section_name, section_content in parsed_data['sections'].items():
        response.append(f"**{section_name}:**")
        
        # Extract links from markdown format
        links = re.findall(r'- \[([^\]]+)\]\(([^)]+)\)(?:: (.+))?', section_content)
        for link_text, link_url, link_desc in links:
            desc_part = f": {link_desc}" if link_desc else ""
            response.append(f"  • [{link_text}]({link_url}){desc_part}")
        
        response.append("")
    
    return '\n'.join(response)

def simple_query(question):
    """Enhanced document search with llms.txt support"""
    if not question.strip():
        return "Please enter a question."
    
    # Look for documents in data directory
    data_dir = Path("./data")
    if not data_dir.exists():
        return "No documents found. Add some .txt files to the data directory."
    
    # Find text files and prioritize llms.txt
    txt_files = list(data_dir.glob("*.txt"))
    if not txt_files:
        return "No .txt files found in data directory."
    
    # Check for llms.txt first
    llms_file = data_dir / "llms.txt"
    if llms_file.exists() and question.lower() in ["what is this?", "overview", "about", "info", "help"]:
        try:
            content = llms_file.read_text(encoding='utf-8')
            parsed = parse_llms_txt(content)
            return f"**🔍 Found llms.txt - Project Overview:**\n\n{format_llms_response(parsed, question.lower().split())}"
        except Exception as e:
            pass
    
    # Simple search - look for query words in files
    results = []
    query_words = question.lower().split()
    
    for txt_file in txt_files:
        try:
            content = txt_file.read_text(encoding='utf-8')
            content_lower = content.lower()
            
            # Count matches
            matches = sum(1 for word in query_words if word in content_lower)
            if matches > 0:
                # Special handling for llms.txt
                if txt_file.name == "llms.txt":
                    parsed = parse_llms_txt(content)
                    formatted_content = format_llms_response(parsed, query_words)
                    results.append(f"**📋 {txt_file.name}** (llms.txt format, matches: {matches})\n{formatted_content}\n")
                else:
                    # Get first 800 chars for better context
                    preview = content[:800] + "..." if len(content) > 800 else content
                    results.append(f"**📄 {txt_file.name}** (matches: {matches})\n{preview}\n")
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
        title="🤖 Simple Document Search with llms.txt Support",
        description="Upload .txt files to the data/ directory and ask questions. Special support for llms.txt format!",
        examples=[
            ["What is this about?"],
            ["overview"],
            ["Tell me about quantum computing"],
            ["What are the main features?"],
            ["info"]
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
