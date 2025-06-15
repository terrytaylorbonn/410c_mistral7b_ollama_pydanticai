# langchain_ollama_agent222.py (v2, clean)

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
