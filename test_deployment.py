"""
Test script for the FastAPI + Gradio deployment
Tests both the API endpoints and Gradio interface functionality
"""

import requests
import json
import time

def test_gradio_interface():
    """Test if Gradio interface is accessible"""
    try:
        response = requests.get("http://localhost:10000/")
        if response.status_code == 200:
            print("✅ Gradio interface is accessible")
            return True
        else:
            print(f"❌ Gradio interface returned status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error accessing Gradio interface: {e}")
        return False

def test_api_endpoints():
    """Test the FastAPI endpoints"""
    base_url = "http://localhost:10000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{base_url}/api/health")
        if response.status_code == 200:
            health_data = response.json()
            print("✅ Health endpoint working")
            print(f"   Status: {health_data.get('status', 'unknown')}")
            print(f"   Message: {health_data.get('message', 'none')}")
        else:
            print(f"❌ Health endpoint returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint error: {e}")
    
    # Test query endpoint
    try:
        query_data = {
            "query": "What is this system about?",
            "top_k": 3
        }
        response = requests.post(f"{base_url}/api/query", json=query_data)
        if response.status_code == 200:
            result = response.json()
            print("✅ Query endpoint working")
            print(f"   Answer: {result.get('answer', 'No answer')[:100]}...")
            print(f"   Sources found: {len(result.get('sources', []))}")
            print(f"   Processing time: {result.get('processing_time', 0):.2f}s")
        else:
            print(f"❌ Query endpoint returned status: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Query endpoint error: {e}")
    
    # Test status endpoint
    try:
        response = requests.get(f"{base_url}/api/status")
        if response.status_code == 200:
            status_data = response.json()
            print("✅ Status endpoint working")
            print(f"   Total files: {status_data.get('data_directory', {}).get('total_files', 0)}")
            print(f"   OpenAI configured: {status_data.get('environment', {}).get('openai_api_key', False)}")
        else:
            print(f"❌ Status endpoint returned status: {response.status_code}")
    except Exception as e:
        print(f"❌ Status endpoint error: {e}")

def test_simple_rag_system():
    """Test the simple RAG system directly"""
    try:
        from simple_rag_deploy import load_and_query_documents
        
        print("\n🧪 Testing Simple RAG System:")
        result = load_and_query_documents("What is quantum computing?")
        
        print(f"✅ RAG system working")
        print(f"   Answer: {result['answer'][:150]}...")
        print(f"   Sources: {len(result['sources'])}")
        print(f"   Time: {result['processing_time']:.2f}s")
        
    except Exception as e:
        print(f"❌ RAG system error: {e}")

def main():
    """Run all tests"""
    print("🚀 Testing FastAPI + Gradio Deployment\n")
    
    print("1. Testing Gradio Interface:")
    gradio_ok = test_gradio_interface()
    
    print("\n2. Testing API Endpoints:")
    test_api_endpoints()
    
    print("\n3. Testing RAG System:")
    test_simple_rag_system()
    
    print("\n📋 Summary:")
    if gradio_ok:
        print("✅ System is ready for deployment!")
        print("🌐 Gradio UI: http://localhost:10000")
        print("📚 API Docs: http://localhost:10000/docs")
        print("🔍 API Status: http://localhost:10000/api/status")
    else:
        print("❌ System needs troubleshooting")
    
    print("\n📝 Next Steps for Render Deployment:")
    print("1. Push code to GitHub repository")
    print("2. Create Render web service")
    print("3. Set environment variables (PORT=10000)")
    print("4. Configure build command: ./build.sh")
    print("5. Configure start command: python fastapi_app.py")

if __name__ == "__main__":
    main()
