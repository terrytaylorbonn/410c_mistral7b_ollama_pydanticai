# agent_print_files_langgraph_new.py
"""
LangGraph version of the agent that prints all local file contents.
"""
import os
from langchain_ollama import ChatOllama
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import create_react_agent
from langchain.tools import Tool
from langchain.prompts import ChatPromptTemplate

# Set up the LLM
llm = ChatOllama(base_url="http://localhost:11434", model="mistral")

# Define the tool function
def print_all_files(dummy: str = "") -> str:
    print("[DEBUG] print_all_files tool called")
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

# Register the tool
print_all_files_tool = Tool(
    name="print_all_files",
    func=print_all_files,
    description="Returns the full contents of all .txt, .md, .py, or .json files in ./data directory."
)

tools = [print_all_files_tool]

# Remove custom prompt and use default for create_react_agent
react_agent = create_react_agent(llm, tools)

# Build the graph
workflow = StateGraph(input=dict, output=dict)
workflow.add_node("agent", react_agent)
workflow.set_entry_point("agent")
workflow.add_edge("agent", END)
app = workflow.compile()

# Run the graph
if __name__ == "__main__":
    # Directly call the tool and print its output
    print("\n[DIRECT TOOL CALL] Contents of ./data:")
    print(print_all_files())
    # Optionally, still run the agent for future debugging
    # result = app.invoke({"input": "Print out the contents of all local files."})
    # print("\n[DEBUG] Full agent result:", result)
    # if isinstance(result, dict):
    #     final_output = result.get("output") or result.get("result") or str(result)
    # else:
    #     final_output = str(result)
    # print("\n🧠 Agent Response (LangGraph):\n", final_output)
