#!/bin/bash
# start_agents.sh - Start both agents

echo "Starting Multi-Agent System..."

# Start Agent1 in background
echo "Starting Agent1 (Research Assistant) on port 8001..."
python3 agent1_research.py &
AGENT1_PID=$!

# Wait a moment for Agent1 to start
sleep 3

# Start Agent2 in background  
echo "Starting Agent2 (Report Writer) on port 8002..."
python3 agent2_writer.py &
AGENT2_PID=$!

echo "Both agents started!"
echo "Agent1 PID: $AGENT1_PID"
echo "Agent2 PID: $AGENT2_PID"
echo ""
echo "Agent1 API: http://localhost:8001/docs"
echo "Agent2 API: http://localhost:8002/docs"
echo ""
echo "Press Ctrl+C to stop all agents"

# Wait for interrupt
trap 'kill $AGENT1_PID $AGENT2_PID; echo "Stopping agents..."; exit' INT
wait
