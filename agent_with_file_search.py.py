# agent_with_file_search.py

#GPT21


#GPT19

import os
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOllama
from langchain.tools import tool

# Set up the LLM
llm = ChatOllama(base_url="http://localhost:11434", model="mistral")

# Define the tool

#GPT22

from langchain.tools import tool
import os
import json

@tool
def search_files(input_str: str) -> str:
    """
    Search for a keyword in files within a directory. 
    `input_str` should be a JSON string like:
    {"query": "quantum", "directory": "./data"}
    Returns full contents of matching files.
    """
    try:
        params = json.loads(input_str)
        query = params.get("query")
        directory = params.get("directory", "./data")
    except Exception as e:
        return f"Invalid input format. Expected JSON string. Error: {e}"

    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".txt", ".md", ".py", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        if query.lower() in content.lower():
                            results.append(f"\n--- {path} ---\n{content.strip()}\n")
                except Exception as e:
                    results.append(f"Error reading {path}: {e}")
    return "\n".join(results) if results else "No matches found."


#GPT21
# from langchain.tools import tool
# import os

# @tool
# def search_files(query: str, directory: str = "./data") -> str:
#     """
#     Search for a keyword in text, markdown, python, or json files in a directory.
#     If found, print the full contents of those files.
#     """
#     results = []
#     for root, _, files in os.walk(directory):
#         for file in files:
#             if file.endswith((".txt", ".md", ".py", ".json")):
#                 path = os.path.join(root, file)
#                 try:
#                     with open(path, "r", encoding="utf-8") as f:
#                         content = f.read()
#                         if query.lower() in content.lower():
#                             results.append(f"\n--- {path} ---\n{content.strip()}\n")
#                 except Exception as e:
#                     results.append(f"Error reading {path}: {e}")
#     return "\n".join(results) if results else "No matches found."


# @tool
# def search_files(query: str) -> str:
#     """Searches for a keyword in all text, markdown, python, or json files in the ./data directory."""
#     target_dir = "./data"
#     if not os.path.exists(target_dir):
#         return f"Directory '{target_dir}' not found."

#     matches = []
#     for root, _, files in os.walk(target_dir):
#         for file in files:
#             if file.endswith((".txt", ".md", ".py", ".json")):
#                 try:
#                     path = os.path.join(root, file)
#                     with open(path, "r", encoding="utf-8") as f:
#                         for i, line in enumerate(f, start=1):
#                             if query.lower() in line.lower():
#                                 matches.append(f"{file}:{i}: {line.strip()}")
#                 except Exception as e:
#                     matches.append(f"Error reading {file}: {e}")
#     return "\n".join(matches) if matches else "No matches found."

# Define tools
tools = [search_files]

# Initialize agent with parsing error handling
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True  # This line is essential!
)

# Run the agent
# response = agent.run("Search for the word 'quantum' in local files.")
# print("\n🧠 Agent Response:\n", response)
response = agent.run('{"query": "quantum", "directory": "./data"}')
print(response)

# #GPT18
# from langchain.agents import initialize_agent, Tool
# from langchain.agents.agent_types import AgentType
# from langchain_community.chat_models import ChatOllama
# from langchain.tools import tool
# from langchain.schema import SystemMessage, HumanMessage

# import os

# # === STEP 1: LLM Setup ===
# llm = ChatOllama(base_url="http://localhost:11434", model="mistral")

# # === STEP 2: Tool Definition ===
# @tool
# def search_files(query: str) -> str:
#     """Search local .txt, .md, .py, or .json files in ./data/ for a keyword."""
#     matches = []
#     for root, _, files in os.walk("./data"):
#         for file in files:
#             if not file.lower().endswith((".txt", ".md", ".py", ".json")):
#                 continue
#             file_path = os.path.join(root, file)
#             try:
#                 with open(file_path, "r", encoding="utf-8") as f:
#                     for i, line in enumerate(f):
#                         if query.lower() in line.lower():
#                             matches.append(f"{file} (line {i+1}): {line.strip()}")
#             except Exception as e:
#                 matches.append(f"{file}: ERROR - {e}")
#     return "\n".join(matches) if matches else "No matches found."

# tools = [search_files]

# # === STEP 3: Agent Setup ===
# agent = initialize_agent(
#     tools,
#     llm,
#     agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
#     verbose=True
# )

# # === STEP 4: Optional Sample Files ===
# os.makedirs("data", exist_ok=True)
# with open("data/sample.txt", "w", encoding="utf-8") as f:
#     f.write("This is a test file.\nIt talks about quantum physics.\nEnd of file.")
# with open("data/example.md", "w", encoding="utf-8") as f:
#     f.write("# Example Markdown\nSearching for quantum entanglement.\n")

# # === STEP 5: Ask the Agent ===
# response = agent.run("Search for the word 'quantum' in local files.")
# print("\n🧠 Agent Response:\n", response)
