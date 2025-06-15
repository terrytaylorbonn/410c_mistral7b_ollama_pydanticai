# ollama_pydantic_agent.py

#GPT23

from pydantic_ai import Agent
from pydantic_ai.providers.openai import OpenAIProvider
import asyncio

#GPT24
agent = Agent(
    model="openai:mistral",  # No colons or version tag
    provider=OpenAIProvider(
        api_key="ollama",
        base_url="http://localhost:11434/v1"
    )
)


# agent = Agent(
#     model="openai:mistral:7b-instruct",
#     provider=OpenAIProvider(
#         api_key="ollama",  # dummy key (required but not used by Ollama)
#         base_url="http://localhost:11434/v1"
#     )
# )

async def main():
    response = await agent.run("What is the capital of France?")
    print(response.output)

asyncio.run(main())


# #GPT20

# import asyncio
# from pydantic_ai import Agent
# from pydantic_ai.providers.openai import OpenAIProvider

# agent = Agent(
#     model="openai:mistral",  # 'openai:' prefix is needed even for Ollama
#     provider=OpenAIProvider(
#         api_key="ollama",  # Required, even if not used
#         base_url="http://localhost:11434/v1",  # Ollama's OpenAI-compatible endpoint
#     )
# )

# async def main():
#     response = await agent.run("What is the capital of France?")
#     print(response.output)

# asyncio.run(main())



#GPT 18

# from pydantic_ai import Agent
# from pydantic_ai.providers.openai import OpenAIProvider

# agent = Agent(
#     model="openai:mistral",  # Provider prefix required
#     provider=OpenAIProvider(
#         api_key="ollama",  # dummy key
#         base_url="http://localhost:11434/v1"
#     )
# )

# response = agent.run("What is the capital of France?")
# print(response.output)


# response = agent.chat("What is the capital of France?")
# print(response.content)



# GPT17
# from pydantic_ai import Agent
# from pydantic_ai.providers.openai import OpenAIProvider

# # Create the agent
# agent = Agent(
#     model="mistral",  # Name of your model (used by Ollama)
#     provider=OpenAIProvider(
#         api_key="ollama",  # Required but not validated for local Ollama
#         base_url="http://localhost:11434/v1"
#     )
# )

# # Send a prompt
# response = agent.chat("What is the capital of Canada?")
# print(response.content)




# GPT16

# from pydantic_ai import Agent
# from pydantic_ai.providers.openai import OpenAIProvider

# # Define your Ollama-based agent
# agent = Agent(
#     model="mistral",  # Just the model name as a string now
#     provider=OpenAIProvider(
#         api_key="ollama",  # Required field, but not used by Ollama
#         base_url="http://localhost:11434/v1",  # Ollama OpenAI-compatible endpoint
#         model="mistral"
#     )
# )

# # Make a test call
# response = agent.chat("What is the capital of Canada?")
# print(response.content)



# # GPT15

# from pydantic_ai import Agent
# from pydantic_ai.providers.openai import OpenAIProvider
# from pydantic_ai.models import KnownModelName

# # Use Ollama's OpenAI-compatible API
# agent = Agent(
#     model=KnownModelName.OPENAI,  # Required if you want structured output later
#     provider=OpenAIProvider(
#         api_key="ollama",  # Required by OpenAI spec, ignored by Ollama
#         base_url="http://localhost:11434/v1",  # Ollama's OpenAI endpoint
#         model="mistral"  # Ollama model name
#     )
# )

# # Simple chat test
# response = agent.chat("What is the capital of Canada?")
# print(response.content)




### pre GPT15
# from pydantic import BaseModel
# from pydantic_ai import Agent
# # from pydantic_ai.models import OpenAIAgentSettings
# from pydantic_ai.models.openai import OpenAIAgentSettings #GPT5
# import os


# # Pydantic model for structured output
# class CityInfo(BaseModel):
#     city: str
#     country: str
#     population: str | None = None


# # Settings for local Ollama using OpenAI-compatible API
# settings = OpenAIAgentSettings(
#     provider="openai",
#     model="mistral",
#     base_url="http://localhost:11434/v1",
#     api_key="ollama",  # not validated
# )

# agent = Agent(settings=settings)

# # User query
# query = "What is the population of Tokyo and which country is it in?"

# # Run agent with output model
# response = agent.run(query, output_model=CityInfo)

# print("\n🧠 Structured Response:")
# print(response)
