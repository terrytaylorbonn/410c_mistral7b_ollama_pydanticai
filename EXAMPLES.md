# Usage Examples

This document provides comprehensive examples of how to use the Local RAG + Multi-Agent System.

## Table of Contents
1. [Basic RAG Queries](#basic-rag-queries)
2. [Multi-Agent Workflows](#multi-agent-workflows)
3. [GitIngest Integration](#gitingest-integration)
4. [OpenAI Comparison](#openai-comparison)
5. [Advanced Use Cases](#advanced-use-cases)

## Basic RAG Queries

### Simple Document Query
```python
# Run the simple RAG interface
python3 simple_rag.py

# Example interaction:
# Enter your query (or 'quit' to exit): What is quantum computing?
# Processing query...
# Answer: Quantum computing is a revolutionary approach to computation...
# Sources: quantum_computing.txt (Score: 0.85)
```

### Programmatic RAG Usage
```python
from rag_file_loader import load_and_query_documents

# Query documents programmatically
result = load_and_query_documents(
    query="Explain machine learning algorithms",
    data_dir="./data",
    top_k=3
)

print(f"Answer: {result['answer']}")
print(f"Sources found: {len(result['sources'])}")
for i, source in enumerate(result['sources']):
    print(f"{i+1}. {source['metadata']['source']} (Score: {source['score']:.2f})")
```

### Adding New Documents
```bash
# Add a new document to the RAG system
echo "Machine learning is a subset of artificial intelligence..." > data/ml_basics.txt

# The system will automatically index it on next query
python3 simple_rag.py
# Query: "What is machine learning?"
```

## Multi-Agent Workflows

### Starting the Agent System
```bash
# Start all agents
chmod +x start_agents.sh
./start_agents.sh

# You should see:
# Starting Research Agent on port 8001...
# Starting Writer Agent on port 8002...
# Both agents are now running!
```

### Research Agent Examples

#### Basic Research Query
```python
import requests

# Query the research agent
response = requests.post("http://localhost:8001/research", json={
    "query": "latest developments in quantum computing",
    "max_sources": 5,
    "include_technical": True
})

result = response.json()
print(f"Research Summary: {result['summary']}")
print(f"Confidence: {result['confidence']}")
```

#### Health Check
```bash
# Check agent status
curl http://localhost:8001/health

# Expected response:
# {"status": "healthy", "model": "mistral:7b", "uptime": "1h 23m"}
```

### Writer Agent Examples

#### Content Generation
```python
import requests

# Generate content based on research
response = requests.post("http://localhost:8002/write", json={
    "topic": "Quantum Computing Applications",
    "research_data": [
        {
            "source": "research_paper.pdf",
            "content": "Quantum computing shows promise in cryptography..."
        }
    ],
    "style": "technical",
    "length": "medium"
})

result = response.json()
print(f"Generated content ({result['word_count']} words):")
print(result['content'])
```

#### Content Editing
```python
# Edit existing content
response = requests.post("http://localhost:8002/edit", json={
    "content": "Quantum computing is good for stuff.",
    "instructions": "Make this more technical and detailed",
    "preserve_style": False
})

result = response.json()
print("Improved content:")
print(result['edited_content'])
print(f"Changes made: {result['changes_made']}")
```

### Complete Multi-Agent Workflow
```python
# demo_client.py example usage
python3 demo_client.py

# Follow the interactive prompts:
# 1. Enter research topic
# 2. System researches the topic
# 3. Writer generates content based on research
# 4. View final result
```

## GitIngest Integration

### Basic Repository Analysis
```python
# Use gitingest_demo.py
python3 gitingest_demo.py

# Example interaction:
# Enter GitHub repository URL: https://github.com/octocat/Hello-World
# Processing repository...
# Summary saved to: data/octocat-hello-world.txt
```

### Manual GitIngest Workflow
```bash
# 1. Visit GitIngest.com web interface
# 2. Enter repository URL: https://github.com/username/repo
# 3. Copy the generated summary
# 4. Save to data directory
echo "Repository summary content..." > data/my-repo-summary.txt

# 5. Query the RAG system about the repository
python3 simple_rag.py
# Query: "What is the main purpose of this repository?"
```

### Advanced GitIngest with Agent Integration
```python
# Use the advanced integration
python3 gitingest_agent_integration.py

# Features:
# - Automatic repository processing
# - Integration with RAG system
# - Agent-based analysis
# - Structured output
```

### Batch Repository Processing
```python
# Process multiple repositories
repositories = [
    "https://github.com/microsoft/vscode",
    "https://github.com/python/cpython",
    "https://github.com/tensorflow/tensorflow"
]

for repo_url in repositories:
    # Process each repository
    # Save to data/ directory
    # Add to RAG system
    pass
```

## OpenAI Comparison

### Basic OpenAI RAG Query
```python
# Ensure OPENAI_API_KEY is set
export OPENAI_API_KEY="your-api-key"

# Run OpenAI comparison
python3 openai_rag_demo.py

# Compare responses:
# Local Model: [Response from Mistral/Ollama]
# OpenAI Model: [Response from GPT-3.5/4]
# Cost: $0.0023
```

### Quality Comparison
```python
# Test the same query on both systems
query = "Explain the differences between classical and quantum algorithms"

# Local RAG
local_result = query_local_rag(query)

# OpenAI RAG  
openai_result = query_openai_rag(query)

# Compare results
print("Local Response:")
print(local_result['answer'])
print(f"Processing time: {local_result.get('processing_time', 'N/A')}")

print("\nOpenAI Response:")
print(openai_result['answer'])
print(f"Tokens used: {openai_result.get('tokens_used', 'N/A')}")
print(f"Estimated cost: ${openai_result.get('cost_estimate', 'N/A')}")
```

## Advanced Use Cases

### 1. Custom Document Processing
```python
# Add custom document processor
def process_code_files(directory):
    """Process programming files for RAG"""
    code_extensions = ['.py', '.js', '.java', '.cpp']
    
    for file_path in Path(directory).rglob('*'):
        if file_path.suffix in code_extensions:
            # Extract functions, classes, comments
            # Add to RAG system with metadata
            pass

# Usage
process_code_files("./my_project")
```

### 2. Domain-Specific RAG
```python
# Create domain-specific knowledge base
domains = {
    "medical": ["medical_papers.txt", "drug_interactions.txt"],
    "legal": ["contracts.txt", "case_law.txt"],
    "technical": ["api_docs.txt", "specifications.txt"]
}

# Query specific domain
result = query_domain_rag("medical", "What are the side effects of aspirin?")
```

### 3. Multi-Modal RAG
```python
# Process different file types
file_processors = {
    '.pdf': extract_pdf_text,
    '.docx': extract_word_text,
    '.md': extract_markdown,
    '.html': extract_html_text,
    '.json': extract_json_content
}

for file_path in data_directory:
    processor = file_processors.get(file_path.suffix)
    if processor:
        content = processor(file_path)
        add_to_rag_system(content, metadata={'source': file_path})
```

### 4. Real-time Data Integration
```python
# Integrate with live data sources
import schedule
import time

def update_rag_with_news():
    """Update RAG system with latest news"""
    # Fetch from news API
    # Process and add to RAG
    pass

def update_rag_with_docs():
    """Update with latest documentation"""
    # Check for new documents
    # Process and index
    pass

# Schedule updates
schedule.every(1).hours.do(update_rag_with_news)
schedule.every(24).hours.do(update_rag_with_docs)

while True:
    schedule.run_pending()
    time.sleep(1)
```

### 5. Agent Chain Workflows
```python
# Create complex multi-agent workflows
workflow = [
    ("research", {"query": "AI trends 2024", "depth": "comprehensive"}),
    ("analyze", {"focus": "business_impact", "metrics": ["adoption", "roi"]}),
    ("write", {"format": "executive_summary", "length": "2_pages"}),
    ("review", {"criteria": ["accuracy", "clarity", "completeness"]})
]

# Execute workflow
results = execute_agent_workflow(workflow)
```

### 6. Custom Evaluation Metrics
```python
def evaluate_rag_performance(test_queries, ground_truth):
    """Evaluate RAG system performance"""
    metrics = {
        'accuracy': [],
        'relevance': [],
        'response_time': [],
        'source_quality': []
    }
    
    for query, expected in zip(test_queries, ground_truth):
        result = query_rag_system(query)
        
        # Calculate metrics
        accuracy = calculate_accuracy(result, expected)
        relevance = calculate_relevance(result['sources'])
        
        metrics['accuracy'].append(accuracy)
        metrics['relevance'].append(relevance)
    
    return metrics

# Usage
test_queries = ["What is quantum computing?", "How does ML work?"]
ground_truth = ["Expected answer 1", "Expected answer 2"]
performance = evaluate_rag_performance(test_queries, ground_truth)
```

## Best Practices

### 1. Document Preparation
```bash
# Clean and organize documents
mkdir -p data/categories/{technical,business,research}

# Use descriptive filenames
mv document1.txt data/technical/api_documentation.txt
mv document2.txt data/business/market_analysis.txt
```

### 2. Query Optimization
```python
# Use specific, well-formed queries
good_query = "What are the key differences between supervised and unsupervised machine learning algorithms?"
poor_query = "ML stuff"

# Include context when needed
contextual_query = "In the context of natural language processing, how do transformer models work?"
```

### 3. Performance Monitoring
```python
# Monitor system performance
import time
import psutil

def monitor_query_performance(query):
    start_time = time.time()
    start_memory = psutil.Process().memory_info().rss
    
    result = query_rag_system(query)
    
    end_time = time.time()
    end_memory = psutil.Process().memory_info().rss
    
    metrics = {
        'query_time': end_time - start_time,
        'memory_used': end_memory - start_memory,
        'result_quality': evaluate_result_quality(result)
    }
    
    return result, metrics
```

### 4. Error Handling
```python
# Robust error handling
def safe_rag_query(query, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = query_rag_system(query)
            return result
        except ModelUnavailableError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)  # Exponential backoff
                continue
            else:
                return {"error": "Model unavailable after retries"}
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}
```

## Common Workflows

### Research Paper Analysis
1. Upload research papers to `data/papers/`
2. Query specific concepts: "What are the main findings about X?"
3. Use multi-agent system to generate summaries
4. Compare with OpenAI for quality assessment

### Codebase Documentation
1. Use GitIngest to process repository
2. Save output to `data/codebases/`
3. Query architecture: "How is the authentication system implemented?"
4. Generate documentation with writer agent

### Competitive Analysis
1. Process competitor websites/docs
2. Research market trends
3. Generate comparative analysis
4. Create strategic recommendations

These examples should help you get started with the various features and capabilities of the system. Remember to check the API documentation in `docs/API.md` for detailed parameter information.
