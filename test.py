import requests

url = "http://localhost:8000/v1/chat/completions"

payload = {
    "model": "mistral",
    "messages": [
        {"role": "user", "content": "What is the capital of France?"}
    ]
}

response = requests.post(url, json=payload)
print(response.json())
