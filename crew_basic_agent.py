# crew_basic_agent.py

#GPT14

from langchain_community.chat_models import ChatOllama
from crewai import Agent, Task, Crew

# Define LLM
llm = ChatOllama(base_url="http://localhost:11434", model="mistral")

# Patch: Monkey-patch `.model_name` so CrewAI won't crash
llm.model_name = "ollama/mistral"  # CrewAI expects provider/model format

# Define Agent
agent = Agent(
    role="Research Assistant",
    goal="Answer simple factual questions",
    backstory="You're a helpful and precise assistant.",
    allow_delegation=False,
    llm=llm
)

# Define Task
task = Task(
    description="What is the capital of France?",
    expected_output="A one-sentence answer with the capital.",
    agent=agent
)

# Run Crew
crew = Crew(
    agents=[agent],
    tasks=[task],
    verbose=True
)

crew.kickoff()


# #GPT13
# from crewai import Agent, Task, Crew
# from langchain_community.chat_models import ChatOllama

# # ✅ Use your offline Mistral7B via Ollama
# llm = ChatOllama(base_url="http://localhost:11434", model="mistral")

# # Define a basic agent
# agent = Agent(
#     role="Geography expert",
#     goal="Answer geography-related questions clearly",
#     backstory="You are a world-renowned geography professor helping students.",
#     allow_delegation=False,
#     verbose=True,
#     llm=llm
# )

# # Define a task the agent will perform
# task = Task(
#     description="What is the capital of France?",
#     agent=agent,
# )

# # Assemble the crew and run
# crew = Crew(
#     agents=[agent],
#     tasks=[task],
#     verbose=True
# )

# if __name__ == "__main__":
#     result = crew.run()
#     print("\n🔍 Final Result:\n", result)
