# agent_print_files.py

import os
from langchain.agents import initialize_agent, Tool
from langchain.agents.agent_types import AgentType
from langchain_community.chat_models import ChatOllama
from langchain.tools import tool

# Set up the LLM
llm = ChatOllama(base_url="http://localhost:11434", model="mistral")

# Define a tool with a clear name for the agent
@tool(name="print_all_files", description="Returns the full contents of all .txt, .md, .py, or .json files in ./data directory.")
def print_all_files(dummy: str = "") -> str:
    """
    Returns the full contents of all .txt, .md, .py, or .json files in ./data directory.
    """
    directory = "./data"
    if not os.path.exists(directory):
        return f"Directory '{directory}' not found."

    results = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith((".txt", ".md", ".py", ".json")):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                        results.append(f"\n--- {path} ---\n{content.strip()}\n")
                except Exception as e:
                    results.append(f"Error reading {path}: {e}")
    return "\n".join(results) if results else "No files found."

# Register tool
# Use the new Tool class for better compatibility
from langchain.tools import Tool as ToolClass

print_all_files_tool = ToolClass(
    name="print_all_files",
    func=print_all_files,
    description="Returns the full contents of all .txt, .md, .py, or .json files in ./data directory."
)

tools = [print_all_files_tool]

# Initialize agent
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    handle_parsing_errors=True,
)

# Use invoke instead of run (avoids deprecation warning)
response = agent.invoke({"input": "Print out the contents of all local files."})
print("\n🧠 Agent Response:\n", response)
