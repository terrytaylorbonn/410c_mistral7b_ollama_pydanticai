#mistral_ollama_fastapi.py

#GPT72

from fastapi import FastAPI, Request
from pydantic import BaseModel
import httpx
import traceback

app = FastAPI()

class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    model: str
    messages: list[Message]

@app.post("/v1/chat/completions")
async def chat_completions(request: ChatRequest):
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "http://localhost:11434/api/chat",
                json={
                    "model": request.model,
                    "messages": [msg.dict() for msg in request.messages],
                    "stream": False
                }
            )
            response.raise_for_status()
            return {
                "id": "chatcmpl-244",
                "object": "chat.completion",
                "created": 1750005646,
                "model": request.model,
                "system_fingerprint": "fp_ollama",
                "choices": [{
                    "index": 0,
                    "message": response.json()["message"],
                    "finish_reason": "stop"
                }],
                "usage": {
                    "prompt_tokens": 12,
                    "completion_tokens": 8,
                    "total_tokens": 20
                }
            }
    except Exception as e:
        print("Exception occurred:")
        traceback.print_exc()
        return {
            "error": str(e),
            "trace": traceback.format_exc()
        }



#GPT 71

# from fastapi import FastAPI
# from pydantic import BaseModel
# import httpx

# app = FastAPI()

# class Message(BaseModel):
#     role: str
#     content: str

# class ChatRequest(BaseModel):
#     model: str
#     messages: list[Message]

# @app.post("/v1/chat/completions")
# async def chat_completions(request: ChatRequest):
#     try:
#         async with httpx.AsyncClient() as client:
#             response = await client.post(
#                 "http://localhost:11434/api/chat",
#                 json={
#                     "model": request.model,
#                     "messages": [msg.dict() for msg in request.messages],
#                     "stream": False   # 🔥 KEY FIX: disable streaming
#                 }
#             )
#             response.raise_for_status()
#             return response.json()
#     except httpx.HTTPError as e:
#         return {"error": str(e), "details": e.response.text if e.response else None}


# from fastapi import FastAPI, Request
# from fastapi.responses import JSONResponse
# import httpx

# app = FastAPI()

# OLLAMA_API_URL = "http://localhost:11434/v1/chat/completions"

# @app.get("/")
# def root():
#     return {"message": "Ollama proxy running (OpenAI-compatible style)"}

# @app.post("/v1/chat/completions")
# async def proxy_chat(request: Request):
#     try:
#         payload = await request.json()

#         async with httpx.AsyncClient() as client:
#             response = await client.post(OLLAMA_API_URL, json=payload)

#         return JSONResponse(status_code=response.status_code, content=response.json())

#     except Exception as e:
#         return JSONResponse(status_code=500, content={"error": str(e)})
