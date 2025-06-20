# Project Structure

This document provides an overview of the project structure and key components.

## Directory Structure

```
410_mistral7b_ollama_pydanticai/
├── docs/                          # Documentation
│   ├── PROJECT_STRUCTURE.md      # This file
│   └── API.md                     # API documentation
├── data/                          # Data files for RAG
│   ├── cyclotruc-gitingest.txt   # GitIngest outputs
│   ├── octocat-hello-world.txt   
│   ├── quantum_computing.txt     
│   ├── quantum_mechanics.txt     
│   ├── sample.txt                
│   └── example.md                
├── __pycache__/                   # Python cache files
├── README.md                      # Main project documentation
├── requirements.txt               # Python dependencies
├── SETUP.md                       # Detailed setup instructions
├── EXAMPLES.md                    # Usage examples
├── CHANGELOG.md                   # Version history
├── .gitignore                     # Git ignore rules
└── LICENSE                        # Project license
```

## Core Components

### RAG System
- **`rag_file_loader.py`** - Document loading and vector database management
- **`simple_rag.py`** - Basic RAG query interface
- **`openai_rag_demo.py`** - OpenAI-powered RAG for comparison

### Multi-Agent System
- **`agent1_research.py`** - Research agent (port 8001)
- **`agent2_writer.py`** - Writer agent (port 8002)
- **`demo_client.py`** - Client for testing agents
- **`start_agents.sh`** - Script to start all agents

### GitIngest Integration
- **`gitingest_demo.py`** - Basic GitIngest API demonstration
- **`simple_gitingest_examples.py`** - Simple usage examples
- **`gitingest_agent_integration.py`** - Advanced agent integration

### Local Ollama Integration
- **`ollama_pydantic_agent.py`** - Pydantic AI with Ollama
- **`pydantic_agent_basic.py`** - Basic Pydantic AI examples
- **`test_ollama.py`** - Ollama connectivity tests
- **`mistral_ollama_fastapi.py`** - FastAPI with Mistral/Ollama

### Utility Scripts
- **`schemas.py`** - Pydantic schemas and data models
- **`clean_requirements.py`** - Dependency management
- **`find_files_with_phrase.py`** - Text search utilities
- **`selenium1.py`**, **`selenium2.py`** - Web scraping tools
- **`audio_transcribe_summarize.py`** - Audio processing

## Data Flow

1. **Document Ingestion**: Files from `data/` directory are loaded and vectorized
2. **Vector Storage**: ChromaDB stores document embeddings locally
3. **Query Processing**: User queries are vectorized and matched against documents
4. **Response Generation**: Local Ollama models or OpenAI generate responses
5. **Multi-Agent Coordination**: Research and Writer agents collaborate on complex tasks

## Key Features

### Local AI Models
- Mistral 7B via Ollama
- phi3:mini for lightweight operations
- ChromaDB for vector storage
- Local embeddings using scikit-learn

### External Integrations
- OpenAI API for quality comparison
- GitIngest.com for codebase summarization
- FastAPI for REST endpoints

### Agent Architecture
- Modular agent design
- RESTful communication between agents
- Configurable model backends
- Error handling and retry logic

## Configuration

### Environment Variables
- `OPENAI_API_KEY` - Required for OpenAI comparison features
- Model configurations in individual scripts

### Model Settings
- Default local model: `mistral:7b`
- Fallback model: `phi3:mini`
- Embedding model: TF-IDF (local) or OpenAI
- Vector database: ChromaDB (persistent)

## Extension Points

The architecture supports easy extension for:
- Additional AI models (Ollama, LM Studio, etc.)
- New agent types and capabilities
- Different vector databases
- Custom document processors
- Alternative embedding methods
