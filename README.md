# 410c Mistral 7B Ollama PydanticAI

## Overview
Local AI development environment using Mistral 7B, Ollama, and PydanticAI for RAG (Retrieval-Augmented Generation) and multi-agent systems. This project demonstrates how to build a complete AI pipeline running entirely offline with local models, plus cloud model integration for comparison.

## What This Repository Contains
- **Local RAG System** with ChromaDB vector storage for document querying
- **Multi-Agent Architecture** with specialized Research and Report Writer agents
- **OpenAI Integration** for model comparison and performance benchmarking
- **GitIngest Integration** for automated GitHub repository analysis
- **Audio Processing** with transcription and summarization capabilities
- **Streaming Responses** optimized for slower hardware (USB SSD setups)

## Key Features
- 🤖 **Multiple AI Models**: Mistral 7B, Phi3:mini, OpenAI GPT-3.5-turbo
- 🔍 **RAG Implementation**: Query your own documents with semantic search
- 👥 **Multi-Agent System**: Collaborative AI agents with RESTful APIs
- 🎯 **Performance Optimized**: Works on USB SSDs with appropriate timeouts
- 🔄 **Streaming Support**: Real-time response generation
- 📊 **Model Comparison**: Local vs cloud model performance analysis

## Core Components

### RAG System
- **`rag_file_loader.py`** - Interactive RAG system with document indexing
- **`simple_rag.py`** - Lightweight streaming RAG implementation
- **`openai_rag_demo.py`** - OpenAI-powered RAG for comparison

### Multi-Agent System  
- **`agent1_research.py`** - Research agent using RAG for factual answers
- **`agent2_writer.py`** - Report writer that calls Agent1 for information
- **`demo_client.py`** - Client demonstrating agent interaction
- **`start_agents.sh`** - Startup script for both agents

### Repository Analysis
- **`gitingest_demo.py`** - Full-featured GitHub repository analyzer
- **`gitingest_agent_integration.py`** - Integration with multi-agent system
- **`simple_gitingest_examples.py`** - Basic GitIngest usage patterns

### Utilities
- **`audio_transcribe_summarize.py`** - Audio transcription with Whisper
- **`test_ollama.py`** - Ollama performance testing
- **`clean_requirements.py`** - Dependency management

## Quick Start

### Prerequisites
- WSL2 or Linux environment
- Python 3.11+
- Ollama installed
- 6GB+ free space for models

### Installation
1. **Clone and setup:**
   ```bash
   git clone https://github.com/terrytaylorbonn/410c_mistral7b_ollama_pydanticai
   cd 410c_mistral7b_ollama_pydanticai
   python -m venv .venvUV
   source .venvUV/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Install Ollama models:**
   ```bash
   ollama pull mistral
   ollama pull phi3:mini  
   ollama pull nomic-embed-text
   ```

### Usage Examples

#### RAG System
```bash
# Interactive document querying
python3 rag_file_loader.py

# Ask questions like:
# "What is quantum computing?"
# "Tell me about entanglement"
```

#### Multi-Agent System
```bash
# Terminal 1: Start agents
./start_agents.sh

# Terminal 2: Test interaction
python3 demo_client.py
```

#### OpenAI Comparison
```bash
# Set API key
export OPENAI_API_KEY="your-key-here"

# Compare with cloud models
python3 openai_rag_demo.py
```

#### Repository Analysis
```bash
# Analyze any GitHub repo
python3 gitingest_demo.py
```

## API Endpoints

### Agent1 (Research Assistant) - Port 8001
- **GET** `/health` - Health check
- **POST** `/research` - Answer questions using RAG
  ```json
  {"question": "What is quantum computing?", "max_sources": 2}
  ```

### Agent2 (Report Writer) - Port 8002  
- **GET** `/health` - Health check
- **POST** `/create_report` - Generate comprehensive reports
  ```json
  {
    "topic": "Quantum Computing Overview",
    "questions": ["What is quantum computing?", "What are qubits?"],
    "report_style": "executive_summary"
  }
  ```

- **Interactive Documentation:**
  - Agent1: http://localhost:8001/docs
  - Agent2: http://localhost:8002/docs

## Performance Notes

### USB SSD Optimization
This project is optimized for USB SSD setups (like WSL2 on external drives):
- Extended timeouts (120s for generation)
- Reduced retry attempts
- Shorter response limits
- Streaming support for better UX

### Model Performance
- **Mistral 7B**: ~1.7 tokens/second on USB SSD
- **Phi3:mini**: Faster alternative for testing
- **OpenAI**: Cloud comparison baseline

## Data Sources
Add documents to the `data/` folder for RAG queries:
- `quantum_computing.txt` - Quantum computing concepts
- `quantum_mechanics.txt` - Physics fundamentals  
- Your own documents (.txt files)

## Development Workflow
1. **Add Knowledge**: Place documents in `data/` folder
2. **Query Locally**: Use `rag_file_loader.py` for testing
3. **Generate Reports**: Use multi-agent system for comprehensive analysis
4. **Compare Models**: Test with OpenAI for quality benchmarking
5. **Analyze Repos**: Use GitIngest for codebase understanding

## Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Documents     │    │   ChromaDB      │    │   Local LLM     │
│   (data/*.txt)  │───▶│   (Vectors)     │───▶│   (Ollama)      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                                        │
┌─────────────────┐    ┌─────────────────┐             │
│   Agent2        │◀───│   Agent1        │◀────────────┘
│   (Writer)      │    │   (Research)    │
└─────────────────┘    └─────────────────┘
        │                       │
        └───────────────────────┴─────────▶ Reports & Answers
```

## Contributing
This is a learning and experimentation repository. Feel free to:
- Add new document sources
- Experiment with different models
- Optimize for your hardware setup
- Create new agent types

## License
MIT License - See LICENSE file for details

## Acknowledgments
- **Ollama** for local LLM serving
- **ChromaDB** for vector storage
- **FastAPI** for agent APIs
- **OpenAI** for model comparison
- **GitIngest** for repository analysis
