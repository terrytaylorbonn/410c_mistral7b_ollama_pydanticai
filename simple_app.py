"""
Ultra-minimal Gradio app for Render deployment with llms.txt support
Features intelligent answers using OpenAI with document context
"""

import gradio as gr
import os
import re
from pathlib import Path
from openai import OpenAI

# Load environment variables from .env file if it exists
env_file = Path(".env")
if env_file.exists():
    for line in env_file.read_text().strip().split('\n'):
        if line and not line.startswith('#') and '=' in line:
            key, value = line.split('=', 1)
            os.environ[key.strip()] = value.strip()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

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

def generate_intelligent_answer(question, relevant_docs):
    """Use OpenAI to generate an intelligent answer based on retrieved documents"""
    if not client.api_key:
        return "⚠️ OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
    
    # Prepare context from relevant documents
    context = "\n\n".join([doc for doc in relevant_docs[:3]])  # Limit to top 3 docs
    
    print(f"DEBUG: Context length: {len(context)} characters")  # Debug output
    print(f"DEBUG: Context preview: {context[:500]}...")  # Debug output
    
    # Create prompt
    prompt = f"""Based on the following documents, please answer the user's question. 
If the documents don't contain relevant information, say so honestly.

Documents:
{context}

Question: {question}

Please provide a helpful, accurate answer based on the information in the documents."""

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that answers questions based on provided documents. Be concise but thorough."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=500,
            temperature=0.1
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"❌ Error generating answer: {str(e)}"

def simple_query(question):
    """Enhanced document search with OpenAI-powered intelligent answers"""
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
    
    # Collect relevant documents based on keyword matching
    relevant_docs = []
    query_words = question.lower().split()
    
    print(f"DEBUG: Searching for words: {query_words}")  # Debug output
    
    for txt_file in txt_files:
        try:
            content = txt_file.read_text(encoding='utf-8')
            content_lower = content.lower()
            
            # Count matches (improved matching - include partial matches)
            matches = 0
            for word in query_words:
                if len(word) > 2:  # Only count meaningful words
                    if word in content_lower:
                        matches += content_lower.count(word)
                    # Also check for partial matches in compound words
                    elif any(word in token for token in content_lower.split()):
                        matches += 1
            
            print(f"DEBUG: {txt_file.name} - matches: {matches}")  # Debug output
            
            if matches > 0:
                # Special handling for llms.txt
                if txt_file.name == "llms.txt":
                    parsed = parse_llms_txt(content)
                    formatted_content = format_llms_response(parsed, query_words)
                    relevant_docs.append(f"From {txt_file.name} (llms.txt format):\n{formatted_content}")
                else:
                    # For large files, try to extract relevant sections
                    if len(content) > 10000:
                        # Try to find sections containing query words
                        relevant_sections = []
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            line_lower = line.lower()
                            if any(word in line_lower for word in query_words if len(word) > 2):
                                # Include context around matching lines
                                start = max(0, i-5)
                                end = min(len(lines), i+6)
                                section = '\n'.join(lines[start:end])
                                relevant_sections.append(section)
                        
                        if relevant_sections:
                            content = '\n\n---\n\n'.join(relevant_sections[:5])  # Top 5 sections
                        else:
                            content = content[:10000] + "\n...[truncated for length]"
                    
                    relevant_docs.append(f"From {txt_file.name}:\n{content}")
                    
        except Exception as e:
            print(f"DEBUG: Error reading {txt_file.name}: {e}")  # Debug output
            continue
    
    if not relevant_docs:
        return f"No relevant documents found for '{question}' in {len(txt_files)} files."
    
    # Use OpenAI to generate intelligent answer
    answer = generate_intelligent_answer(question, relevant_docs)
    
    # Add source information
    source_files = [doc.split('\n')[0].replace('From ', '').replace(':', '') for doc in relevant_docs]
    sources = f"\n\n📚 **Sources:** {', '.join(source_files[:3])}"
    
    return f"🤖 **AI Answer:**\n\n{answer}{sources}"

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
        title="🤖 AI-Powered Document Search with llms.txt Support",
        description="Ask questions about your documents and get intelligent AI-powered answers using OpenAI!",
        examples=[
            ["What is this project about?"],
            ["How does quantum computing work?"],
            ["What are the main features of this system?"],
            ["Can you explain the deployment process?"],
            ["Tell me about the llms.txt format"]
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
