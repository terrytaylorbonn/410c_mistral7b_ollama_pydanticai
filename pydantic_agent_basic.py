# pydantic_agent_basic.py

#GPT7

import asyncio
from pydantic import BaseModel
from pydantic_ai import Agent
from pydantic_ai.models import OllamaModel

# Define a structured task schema
class Task(BaseModel):
    title: str
    priority: str
    due: str

# Use the local Ollama server
agent = Agent(
    model=OllamaModel(model_name="mistral", base_url="http://localhost:11434")
)

async def main():
    task = await agent.run(
        schema=Task,
        input="Schedule a task to review documents tomorrow. Make it high priority.",
    )
    print(task)

if __name__ == "__main__":
    asyncio.run(main())

# #GPT5

# import asyncio
# from pydantic import BaseModel
# from pydantic_ai import Agent
# from pydantic_ai.providers.openai import OpenAIProvider

# # Define the structured schema
# class Task(BaseModel):
#     title: str
#     priority: str
#     due: str

# # Create the agent
# agent = Agent(
#     model="openai:mistral",  # Pydantic AI uses this format for Ollama
#     provider=OpenAIProvider(
#         api_key="ollama",
#         base_url="http://localhost:11434/v1"
#     )
# )

# # Async entry point
# async def main():
#     task = await agent.run(
#         schema=Task,
#         input="Create a high-priority task to review documents, due tomorrow."
#     )
#     print(task)

# # Run the agent
# if __name__ == "__main__":
#     asyncio.run(main())


# # GPT3
# import asyncio
# from pydantic_ai import Agent
# from schemas import Task

# agent = Agent(model="openai:mistral")  # Ollama compatible

# async def main():
#     task = await agent.run(
#         Task,
#         "Create a high-priority task to review documents, due tomorrow."
#     )
#     print(task)

# asyncio.run(main())


# from pydantic_ai import Agent
# from pydantic_ai.providers.openai import OpenAIProvider
# from schemas import Task

# agent = Agent(
#     model="openai:mistral",
#     provider=OpenAIProvider(
#         api_key="ollama",
#         base_url="http://localhost:8000/v1"
#     )
# )

# task = agent.complete(
#     Task,
#     "Create a high-priority task to review documents, due tomorrow."
# )

# print(task)
