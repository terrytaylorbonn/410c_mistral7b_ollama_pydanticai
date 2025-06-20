# API Documentation

This document describes the APIs and endpoints available in the project.

## Multi-Agent System APIs

### Research Agent (Port 8001)

#### POST /research
Research and gather information on a given topic.

**Request:**
```json
{
    "query": "string",
    "max_sources": 5,
    "include_technical": true
}
```

**Response:**
```json
{
    "results": [
        {
            "source": "string",
            "content": "string",
            "relevance_score": 0.95,
            "timestamp": "2024-01-01T00:00:00Z"
        }
    ],
    "summary": "string",
    "confidence": 0.85
}
```

#### GET /health
Check agent health status.

**Response:**
```json
{
    "status": "healthy",
    "model": "mistral:7b",
    "uptime": "2h 30m"
}
```

### Writer Agent (Port 8002)

#### POST /write
Generate written content based on research data.

**Request:**
```json
{
    "topic": "string",
    "research_data": [
        {
            "source": "string",
            "content": "string"
        }
    ],
    "style": "technical|academic|casual",
    "length": "short|medium|long"
}
```

**Response:**
```json
{
    "content": "string",
    "word_count": 500,
    "style_score": 0.9,
    "citations": ["source1", "source2"]
}
```

#### POST /edit
Edit and improve existing content.

**Request:**
```json
{
    "content": "string",
    "instructions": "string",
    "preserve_style": true
}
```

**Response:**
```json
{
    "edited_content": "string",
    "changes_made": ["grammar", "clarity", "structure"],
    "improvement_score": 0.15
}
```

## RAG System APIs

### Simple RAG

#### Function: `query_documents(query: str, top_k: int = 5)`
Query the local document collection.

**Parameters:**
- `query`: Search query string
- `top_k`: Number of top results to return

**Returns:**
```python
{
    "answer": "string",
    "sources": [
        {
            "content": "string",
            "score": 0.95,
            "metadata": {}
        }
    ],
    "processing_time": 1.5
}
```

### OpenAI RAG

#### Function: `openai_rag_query(query: str, model: str = "gpt-3.5-turbo")`
Query using OpenAI models for comparison.

**Parameters:**
- `query`: Search query string
- `model`: OpenAI model to use

**Returns:**
```python
{
    "answer": "string",
    "model_used": "gpt-3.5-turbo",
    "tokens_used": 150,
    "cost_estimate": 0.0003
}
```

## GitIngest Integration APIs

### Basic GitIngest

#### Function: `get_repo_summary(repo_url: str)`
Get repository summary from GitIngest.

**Parameters:**
- `repo_url`: GitHub repository URL

**Returns:**
```python
{
    "success": True,
    "summary": "string",
    "file_count": 25,
    "total_lines": 1500,
    "languages": ["Python", "JavaScript"]
}
```

### Advanced GitIngest

#### Function: `process_and_ingest(repo_url: str, save_to_rag: bool = True)`
Process repository and optionally add to RAG system.

**Parameters:**
- `repo_url`: GitHub repository URL
- `save_to_rag`: Whether to add to RAG database

**Returns:**
```python
{
    "processed": True,
    "filename": "repo-summary.txt",
    "added_to_rag": True,
    "chunk_count": 12
}
```

## Model Configuration APIs

### Ollama Integration

#### Function: `test_ollama_connection(model: str = "mistral:7b")`
Test connection to Ollama service.

**Parameters:**
- `model`: Model name to test

**Returns:**
```python
{
    "connected": True,
    "model": "mistral:7b",
    "version": "0.1.25",
    "available_models": ["mistral:7b", "phi3:mini"]
}
```

## Error Handling

All APIs use consistent error response format:

```json
{
    "error": {
        "code": "ERROR_CODE",
        "message": "Human readable error message",
        "details": "Additional technical details",
        "timestamp": "2024-01-01T00:00:00Z"
    }
}
```

### Common Error Codes

- `MODEL_UNAVAILABLE`: AI model is not accessible
- `INVALID_INPUT`: Request validation failed
- `PROCESSING_ERROR`: Internal processing error
- `TIMEOUT`: Request timed out
- `RATE_LIMITED`: Too many requests

## Authentication

Currently, the system uses:
- **OpenAI API**: Requires `OPENAI_API_KEY` environment variable
- **Local APIs**: No authentication (intended for local development)
- **GitIngest**: No authentication required

## Rate Limits

- **Local Ollama**: Limited by hardware capability
- **OpenAI API**: Subject to OpenAI's rate limits
- **GitIngest**: Public API limits apply

## Response Times

Typical response times:
- Local RAG queries: 1-5 seconds
- OpenAI queries: 2-10 seconds
- Agent communication: 0.5-2 seconds
- GitIngest processing: 5-30 seconds (depending on repo size)

## WebSocket Support

Currently not implemented, but architecture supports:
- Real-time agent communication
- Streaming responses
- Live collaboration features

## Batch Operations

For processing multiple requests:
- Use individual API calls in sequence
- Implement client-side batching
- Consider rate limits and timeouts
