#!/bin/bash
# Ultra-simple build script

echo "Installing minimal dependencies..."
pip install gradio

echo "Creating data directory..."
mkdir -p data

echo "Creating sample document..."
cat > data/sample.txt << 'EOF'
Welcome to the Simple Document Search System!

This is a basic document search tool that can help you find information in your text files.

Key features:
- Simple text search
- Works with .txt files
- Fast and lightweight
- Easy to use

How to use:
1. Add your .txt files to the data directory
2. Ask questions about your documents
3. Get instant answers

This system uses basic word matching to find relevant information in your documents.
EOF

echo "Build completed successfully!"
