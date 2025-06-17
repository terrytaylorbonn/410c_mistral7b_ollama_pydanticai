# agent_local.py

from langchain_community.chat_models import ChatOllama
from langchain.schema import SystemMessage, HumanMessage

# Use local Ollama model
llm = ChatOllama(base_url="http://localhost:11434", model="mistral")

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?")
]

response = llm(messages)
print(response.content)
