# GitIngest Getting Started Guide

## What is GitIngest?

GitIngest (https://gitingest.com/) analyzes GitHub repositories and creates comprehensive summaries perfect for AI analysis. It extracts:
- Project structure
- Key file contents  
- Repository metadata
- Code snippets

## Quick Start (3 Methods)

### Method 1: Web Interface (Easiest)
1. Go to https://gitingest.com/
2. Paste GitHub URL (e.g., `https://github.com/python/requests`)
3. Click "Ingest Repository"
4. Copy the generated summary
5. Paste into your AI chat

### Method 2: Direct URL
```
https://gitingest.com/api/ingest?url=https://github.com/owner/repo
```

### Method 3: API Call (Python)
```python
import requests

response = requests.post(
    "https://gitingest.com/api/ingest",
    json={"url": "https://github.com/fastapi/fastapi"}
)

analysis = response.json()
```

## Common Filter Patterns

### Python Projects
```python
{
    "url": "https://github.com/owner/repo",
    "include_patterns": ["*.py", "*.md", "*.txt", "requirements.txt"],
    "exclude_patterns": ["*.pyc", "__pycache__/*", ".env", "venv/*"]
}
```

### JavaScript/Node.js
```python
{
    "url": "https://github.com/owner/repo", 
    "include_patterns": ["*.js", "*.ts", "*.json", "*.md"],
    "exclude_patterns": ["node_modules/*", "*.min.js", "dist/*"]
}
```

### Documentation Only
```python
{
    "url": "https://github.com/owner/repo",
    "include_patterns": ["*.md", "*.rst", "*.txt"],
    "exclude_patterns": [".git/*", "node_modules/*"]
}
```

## Integration with Your Multi-Agent System

1. **Run GitIngest** on a repository
2. **Save output** to your `data/` folder  
3. **Query with RAG** using your existing system
4. **Generate reports** with Agent2

## Example Workflow

```bash
# 1. Analyze repository and add to knowledge base
python3 gitingest_agent_integration.py

# 2. Query the repository using your RAG system
python3 rag_file_loader.py

# 3. Ask questions like:
# "What does this repository do?"
# "How is the code structured?" 
# "What are the main components?"
```

## Use Cases

- **Code Review**: Understand unfamiliar codebases
- **Learning**: Study how popular projects are structured
- **Documentation**: Generate project overviews
- **AI Analysis**: Prepare repositories for LLM analysis
- **Research**: Compare different implementations

## Best Practices

1. **Filter appropriately** - Don't include huge files or binaries
2. **Focus on key files** - README, main source files, configs
3. **Exclude noise** - Tests, logs, build artifacts
4. **Save for reuse** - Cache analyses locally
5. **Combine with AI** - Use output as context for deeper analysis

## Example Questions to Ask Your RAG System After GitIngest

- "What is the architecture of this project?"
- "How do I get started with this codebase?"
- "What are the main dependencies?"
- "How is error handling implemented?"
- "What are the key design patterns used?"

## Files Created by This Demo

- `gitingest_demo.py` - Full-featured demo with interactive examples
- `simple_gitingest_examples.py` - Basic usage patterns
- `gitingest_agent_integration.py` - Integration with your multi-agent system

## Try It Now!

```bash
# Simple example
python3 simple_gitingest_examples.py

# Full demo
python3 gitingest_demo.py

# Multi-agent integration
python3 gitingest_agent_integration.py
```
