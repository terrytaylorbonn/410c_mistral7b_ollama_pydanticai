# test_ollama.py
"""
Simple test to check Ollama response times
"""

import requests
import time

def test_ollama_simple():
    """Test a very simple prompt to Ollama"""
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": "Say hello in one word.",
                "stream": False,
                "options": {
                    "num_predict": 10
                }
            },
            timeout=15
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Success! Response time: {end_time - start_time:.2f}s")
            print(f"Answer: {result['response']}")
            return True
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(response.text)
            return False
            
    except requests.exceptions.Timeout:
        print(f"❌ Timeout after {time.time() - start_time:.2f}s")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def test_embedding():
    """Test embedding generation"""
    start_time = time.time()
    
    try:
        response = requests.post(
            "http://localhost:11434/api/embeddings",
            json={
                "model": "nomic-embed-text",
                "prompt": "test text"
            },
            timeout=10
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            print(f"✅ Embedding success! Response time: {end_time - start_time:.2f}s")
            return True
        else:
            print(f"❌ Embedding error: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return False

if __name__ == "__main__":
    print("Testing Ollama performance...")
    print("\n1. Testing simple text generation:")
    test_ollama_simple()
    
    print("\n2. Testing embeddings:")
    test_embedding()
    
    print("\n3. Testing with different options:")
    start_time = time.time()
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "mistral",
                "prompt": "What is quantum computing? Answer in 2 sentences.",
                "stream": False,
                "options": {
                    "temperature": 0.1,
                    "num_predict": 50,
                    "top_p": 0.5
                }
            },
            timeout=20
        )
        
        end_time = time.time()
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Longer prompt success! Response time: {end_time - start_time:.2f}s")
            print(f"Answer: {result['response']}")
        else:
            print(f"❌ Longer prompt failed: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Longer prompt error: {e}")
