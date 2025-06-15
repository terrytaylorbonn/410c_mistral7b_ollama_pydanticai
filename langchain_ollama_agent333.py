# langchain_ollama_agent333.py

try:
    import torch
    if torch.cuda.is_available():
        print(f"GPU is available: {torch.cuda.get_device_name(torch.cuda.current_device())}")
    else:
        print("GPU is NOT available. Running on CPU.")
except ImportError:
    print("PyTorch is not installed. Cannot check GPU status.")

from langchain_core.messages import HumanMessage
# from langchain_community.chat_models import ChatOpenAI
from langchain_openai import ChatOpenAI

# Connect to Ollama (must be running mistral)
llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model_name="mistral"
)

# Run a prompt
response = llm.invoke([HumanMessage(content="What is the capital of France?")])
print(response.content)


# from langchain.chat_models import ChatOpenAI
# from langchain.schema import HumanMessage

# # ✅ Connect to Ollama (make sure it's running)
# llm = ChatOpenAI(
#     base_url="http://localhost:11434/v1",  # Ollama's OpenAI-compatible endpoint
#     api_key="ollama",                      # Can be anything for Ollama
#     model_name="mistral"                   # Or "mistral:7b-instruct" if applicable
# )

# # 🧪 Run a simple prompt
# response = llm([HumanMessage(content="What is the capital of France?")])
# print(response.content)
