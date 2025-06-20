# agent2_writer.py
"""
Agent2: Report Writer
- Calls Agent1 for research
- Formats information into reports
- Runs as FastAPI service on port 8002
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
import httpx
import requests
from typing import List, Dict

app = FastAPI(title="Agent2 - Report Writer", version="1.0.0")

# Configuration
AGENT1_URL = "http://localhost:8001"
OLLAMA_URL = "http://localhost:11434"

# Request/Response models
class ReportRequest(BaseModel):
    topic: str
    questions: List[str]
    report_style: str = "executive_summary"  # or "detailed", "bullet_points"

class ReportResponse(BaseModel):
    topic: str
    report: str
    research_used: List[Dict]
    agent: str = "Agent2-Writer"

class Agent2Writer:
    def __init__(self):
        self.agent1_url = AGENT1_URL
        self.ollama_url = OLLAMA_URL
    
    async def call_agent1_research(self, question: str) -> Dict:
        """Call Agent1 for research"""
        try:
            async with httpx.AsyncClient(timeout=180.0) as client:  # 3 minute timeout
                response = await client.post(
                    f"{self.agent1_url}/research",
                    json={"question": question, "max_sources": 2}
                )
                if response.status_code == 200:
                    return response.json()
                else:
                    return {
                        "question": question,
                        "answer": f"Agent1 error: {response.status_code}",
                        "sources": []
                    }
        except Exception as e:
            return {
                "question": question,
                "answer": f"Failed to contact Agent1: {str(e)}",
                "sources": []
            }
    
    async def gather_research(self, questions: List[str]) -> List[Dict]:
        """Gather research from Agent1 for multiple questions"""
        research_results = []
        
        for question in questions:
            print(f"Agent2 asking Agent1: {question}")
            result = await self.call_agent1_research(question)
            research_results.append(result)
        
        return research_results
    
    def format_report(self, topic: str, research_data: List[Dict], style: str = "executive_summary") -> str:
        """Format research into a report using LLM"""
        
        # Prepare research context
        research_context = ""
        for i, research in enumerate(research_data, 1):
            research_context += f"\nQuestion {i}: {research['question']}\n"
            research_context += f"Answer: {research['answer']}\n"
            if research['sources']:
                research_context += f"Sources: {', '.join(research['sources'])}\n"
        
        # Create prompt based on style
        style_instructions = {
            "executive_summary": "Write a concise executive summary (2-3 paragraphs)",
            "detailed": "Write a detailed report with clear sections and explanations",
            "bullet_points": "Organize the information into clear bullet points"
        }
        
        instruction = style_instructions.get(style, style_instructions["executive_summary"])
        
        prompt = f"""Create a {style} report about "{topic}" based on the research below.

Research Data:
{research_context}

{instruction}. Be professional and well-structured.

Report:"""

        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "phi3:mini",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": 200,
                        "temperature": 0.3
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                return response.json()["response"]
            else:
                return f"Error formatting report: {response.status_code}"
                
        except Exception as e:
            return f"Report formatting error: {str(e)}"

# Initialize Agent2
writer = Agent2Writer()

@app.get("/")
async def root():
    return {"message": "Agent2 - Report Writer", "status": "ready"}

@app.get("/health")
async def health():
    return {"status": "healthy", "agent": "Agent2-Writer"}

@app.get("/check_agent1")
async def check_agent1():
    """Check if Agent1 is available"""
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            response = await client.get(f"{AGENT1_URL}/health")
            if response.status_code == 200:
                return {"agent1_status": "available", "response": response.json()}
            else:
                return {"agent1_status": "error", "code": response.status_code}
    except Exception as e:
        return {"agent1_status": "unavailable", "error": str(e)}

@app.post("/create_report", response_model=ReportResponse)
async def create_report(request: ReportRequest):
    """Create a report by gathering research from Agent1"""
    print(f"Agent2 creating report on: {request.topic}")
    
    # Gather research from Agent1
    research_results = await writer.gather_research(request.questions)
    
    # Format into report
    report = writer.format_report(
        request.topic, 
        research_results, 
        request.report_style
    )
    
    return ReportResponse(
        topic=request.topic,
        report=report,
        research_used=research_results
    )

if __name__ == "__main__":
    print("Starting Agent2 - Report Writer on port 8002...")
    uvicorn.run(app, host="0.0.0.0", port=8002)
