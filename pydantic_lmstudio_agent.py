from pydantic_ai import Agent
import os
import asyncio

# Patch: configure OpenAI client via environment vars
os.environ["OPENAI_API_KEY"] = "not-needed"  # LM Studio ignores this
os.environ["OPENAI_BASE_URL"] = "http://localhost:1234/v1"  # LM Studio base URL

async def main():
    agent = Agent(model="openai:mistral-7b-instruct-v0.1")  # Must have "openai:" prefix
    result = await agent.run("What is the capital of France?")
    print(result.output)

asyncio.run(main())