# demo_client.py
"""
Demo client to test the multi-agent system
Shows how Agent2 calls Agent1 to create reports
"""

import requests
import json
import time

AGENT1_URL = "http://localhost:8001"
AGENT2_URL = "http://localhost:8002"

def test_agent1_direct():
    """Test Agent1 directly"""
    print("=== Testing Agent1 (Research Assistant) ===")
    
    response = requests.post(
        f"{AGENT1_URL}/research",
        json={"question": "What is quantum computing?"}
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"Question: {result['question']}")
        print(f"Answer: {result['answer']}")
        print(f"Sources: {result['sources']}")
    else:
        print(f"Error: {response.status_code}")

def test_agent2_report():
    """Test Agent2 creating a report (which calls Agent1)"""
    print("\n=== Testing Agent2 (Report Writer) ===")
    
    # Create a report request
    report_request = {
        "topic": "Quantum Computing Overview",
        "questions": [
            "What is quantum computing?",
            "What are qubits?",
            "How does quantum entanglement work?"
        ],
        "report_style": "executive_summary"
    }
    
    print("Agent2 creating report...")
    response = requests.post(
        f"{AGENT2_URL}/create_report",
        json=report_request
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"\nTopic: {result['topic']}")
        print(f"\nReport:\n{result['report']}")
        print(f"\nResearch Used:")
        for i, research in enumerate(result['research_used'], 1):
            print(f"  {i}. {research['question']}")
            print(f"     Sources: {research['sources']}")
    else:
        print(f"Error: {response.status_code}")

def check_agents_health():
    """Check if both agents are running"""
    print("=== Checking Agent Health ===")
    
    try:
        response1 = requests.get(f"{AGENT1_URL}/health", timeout=5)
        print(f"Agent1: {response1.json()}")
    except Exception as e:
        print(f"Agent1: Not available ({e})")
    
    try:
        response2 = requests.get(f"{AGENT2_URL}/health", timeout=5)
        print(f"Agent2: {response2.json()}")
    except Exception as e:
        print(f"Agent2: Not available ({e})")

if __name__ == "__main__":
    print("Multi-Agent System Demo")
    print("=" * 40)
    
    # Check if agents are running
    check_agents_health()
    
    # Test Agent1 directly
    test_agent1_direct()
    
    # Wait a moment
    time.sleep(2)
    
    # Test Agent2 (which calls Agent1)
    test_agent2_report()
