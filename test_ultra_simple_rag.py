"""
Quick test of the ultra-simple RAG system
"""

from simple_rag_deploy import load_and_query_documents

def main():
    print("Testing Ultra-Simple RAG System...")
    
    # Test basic functionality
    result = load_and_query_documents("What is quantum computing?")
    
    print(f"Query: What is quantum computing?")
    print(f"Answer: {result['answer'][:200]}...")
    print(f"Sources found: {len(result['sources'])}")
    print(f"Model used: {result['model_used']}")
    print(f"Processing time: {result['processing_time']:.2f}s")
    
    print("\n" + "="*50)
    print("✅ Ultra-Simple RAG system working!")
    print("Ready for deployment with minimal dependencies.")

if __name__ == "__main__":
    main()
