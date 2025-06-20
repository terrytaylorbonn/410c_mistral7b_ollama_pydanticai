#!/bin/bash

# Render.com build script
# This script is executed during the build phase

echo "Starting build process..."
echo "Current directory: $(pwd)"
echo "Files available: $(ls -la)"

# Install Python dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements_deploy.txt

# Create data directory if it doesn't exist
echo "Setting up data directory..."
mkdir -p data

# Create a default sample file for demo purposes
if [ ! -f "data/sample.txt" ]; then
    echo "Creating sample data file..."
    cat > data/sample.txt << 'EOF'
# Local RAG + Multi-Agent System

Welcome to the Local RAG + Multi-Agent System!

## What is this system?

This is a Retrieval-Augmented Generation (RAG) system that combines:

1. **Local AI Models**: Using Ollama with Mistral 7B and Phi-3 Mini
2. **Vector Search**: ChromaDB for document embeddings and similarity search  
3. **Multi-Agent Architecture**: Specialized agents for research and writing
4. **Web Interface**: Gradio UI for easy interaction
5. **API Access**: FastAPI endpoints for programmatic access

## Key Features

- **Local Processing**: No data leaves your system (except for OpenAI comparison)
- **Document Analysis**: Automatically indexes documents from the data directory
- **Multi-Model Support**: Compare local models with OpenAI models
- **GitIngest Integration**: Process GitHub repositories for analysis
- **Real-time Queries**: Interactive web interface for document queries

## Use Cases

- Research assistance and document analysis
- Code repository understanding
- Knowledge base querying
- Content generation with fact-checking
- Educational and learning applications

## Getting Started

1. Add your documents to the data directory
2. Use the web interface to query your documents
3. Compare results between local and cloud models
4. Explore the API endpoints for integration

This system is designed to be your personal AI assistant for document analysis and knowledge extraction!
EOF
    echo "Sample data file created successfully"
fi

echo "Build completed successfully!"
