# Setup Guide

This guide provides detailed setup instructions for the Local RAG + Multi-Agent System.

## Prerequisites

### System Requirements
- **OS**: Linux (Ubuntu/WSL2), macOS, or Windows
- **Python**: 3.11 or higher
- **RAM**: 8GB minimum, 16GB+ recommended for Mistral 7B
- **Storage**: 10GB free space for models and data
- **Network**: Internet connection for model downloads

### Required Software

#### 1. Ollama Installation
```bash
# Linux/macOS
curl -fsSL https://ollama.com/install.sh | sh

# Windows (WSL2)
curl -fsSL https://ollama.com/install.sh | sh

# Verify installation
ollama --version
```

#### 2. Python Environment
```bash
# Check Python version
python3 --version

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate    # Windows

# Upgrade pip
pip install --upgrade pip
```

## Installation Steps

### 1. Clone and Setup Project
```bash
# Navigate to your projects directory
cd /home/your-username/

# If you don't have the project files, create the directory
mkdir 410_mistral7b_ollama_pydanticai
cd 410_mistral7b_ollama_pydanticai

# Install dependencies
pip install -r requirements.txt
```

### 2. Install and Setup Ollama Models
```bash
# Pull required models (this may take 10-30 minutes)
ollama pull mistral:7b
ollama pull phi3:mini

# Verify models are installed
ollama list

# Test model functionality
ollama run mistral:7b "Hello, how are you?"
```

### 3. Environment Configuration

#### Create Environment Variables
```bash
# For OpenAI integration (optional but recommended)
export OPENAI_API_KEY="your-openai-api-key-here"

# Make it permanent (Linux/macOS)
echo 'export OPENAI_API_KEY="your-openai-api-key-here"' >> ~/.bashrc
source ~/.bashrc

# For WSL2/Windows users
echo 'export OPENAI_API_KEY="your-openai-api-key-here"' >> ~/.bashrc
source ~/.bashrc
```

#### Create .env file (Alternative)
```bash
# Create .env file in project root
cat > .env << EOF
OPENAI_API_KEY=your-openai-api-key-here
OLLAMA_HOST=http://localhost:11434
RAG_DATA_PATH=./data
VECTOR_DB_PATH=./chroma_db
EOF
```

### 4. Initialize Data Directory
```bash
# Create data directory if it doesn't exist
mkdir -p data

# Add sample documents (optional)
echo "This is a sample document for testing RAG functionality." > data/sample.txt
echo "# Sample Markdown\nThis is a markdown document." > data/example.md
```

## Verification Tests

### 1. Test Ollama Connection
```bash
python3 test_ollama.py
```

Expected output:
```
✅ Ollama is running
✅ Model mistral:7b is available
✅ Model phi3:mini is available
✅ Test query successful
```

### 2. Test RAG System
```bash
python3 simple_rag.py
```

Follow the interactive prompts to test document querying.

### 3. Test Multi-Agent System
```bash
# Terminal 1: Start agents
chmod +x start_agents.sh
./start_agents.sh

# Terminal 2: Test client
python3 demo_client.py
```

### 4. Test OpenAI Integration (if configured)
```bash
python3 openai_rag_demo.py
```

## Troubleshooting

### Common Issues

#### 1. Ollama Not Found
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama service
ollama serve &

# Or restart system service
sudo systemctl restart ollama
```

#### 2. Model Loading Errors
```bash
# Check available models
ollama list

# Re-pull models if necessary
ollama pull mistral:7b --force
ollama pull phi3:mini --force
```

#### 3. Memory Issues
```bash
# Check available RAM
free -h

# For low memory systems, use smaller model
ollama pull phi3:mini
# Then modify scripts to use phi3:mini instead of mistral:7b
```

#### 4. Port Conflicts
```bash
# Check if ports are in use
netstat -tlnp | grep :8001
netstat -tlnp | grep :8002

# Kill processes if necessary
pkill -f "agent1_research.py"
pkill -f "agent2_writer.py"
```

#### 5. Python Dependencies
```bash
# If requirements.txt fails, install individually
pip install fastapi uvicorn pydantic requests
pip install scikit-learn numpy chromadb
pip install openai python-dotenv

# For development
pip install --upgrade pip setuptools wheel
```

### Performance Optimization

#### 1. Hardware Recommendations
- **CPU**: Multi-core processor (8+ cores recommended)
- **RAM**: 16GB+ for smooth Mistral 7B operation
- **Storage**: SSD recommended for faster model loading
- **GPU**: Optional, but improves performance significantly

#### 2. Model Selection
```bash
# For faster responses (lower quality)
ollama pull phi3:mini

# For better quality (slower responses)
ollama pull mistral:7b

# For best quality (requires more resources)
ollama pull llama3:8b
```

#### 3. System Tuning
```bash
# Increase file descriptor limits
ulimit -n 4096

# For WSL2 users - allocate more memory
# Edit .wslconfig in Windows user directory:
# [wsl2]
# memory=8GB
# processors=4
```

## Advanced Configuration

### 1. Custom Model Configuration
Edit individual Python files to change models:
```python
# In ollama_pydantic_agent.py, simple_rag.py, etc.
MODEL = "your-preferred-model"  # e.g., "phi3:mini", "llama3:8b"
```

### 2. Vector Database Configuration
```python
# In rag_file_loader.py
CHROMA_DB_PATH = "./custom_chroma_db"
COLLECTION_NAME = "custom_collection"
```

### 3. Agent Port Configuration
```python
# In agent1_research.py
PORT = 8001  # Change if needed

# In agent2_writer.py  
PORT = 8002  # Change if needed
```

## Production Deployment

### 1. Docker Setup (Optional)
```bash
# Build Docker image (if Dockerfile is available)
docker build -t rag-system .

# Run container
docker run -p 8001:8001 -p 8002:8002 rag-system
```

### 2. Systemd Service (Linux)
```bash
# Create service file
sudo tee /etc/systemd/system/rag-agents.service << EOF
[Unit]
Description=RAG Multi-Agent System
After=network.target

[Service]
Type=forking
User=your-username
WorkingDirectory=/path/to/410_mistral7b_ollama_pydanticai
ExecStart=/path/to/410_mistral7b_ollama_pydanticai/start_agents.sh
Restart=always

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
sudo systemctl enable rag-agents
sudo systemctl start rag-agents
```

## Next Steps

After successful setup:
1. Review [EXAMPLES.md](EXAMPLES.md) for usage examples
2. Check [API.md](docs/API.md) for API documentation
3. Explore different models and configurations
4. Add your own documents to the `data/` directory
5. Experiment with GitIngest integration for codebase analysis

## Getting Help

If you encounter issues:
1. Check the logs in terminal outputs
2. Verify all prerequisites are met
3. Test individual components separately
4. Review the troubleshooting section above
5. Check Ollama documentation: https://ollama.com/docs
6. Refer to project README.md for additional context
