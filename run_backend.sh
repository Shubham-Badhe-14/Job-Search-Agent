#!/bin/bash

# Check if venv exists
if [ -d "agent_env" ]; then
    source agent_env/bin/activate
else
    echo "⚠️  Virtual environment 'agent_env' not found!"
    echo "   Please make sure you are in the project root."
    exit 1
fi

echo "=================================================="
echo "🚀 Starting CareerAgent AI Backend"
echo "=================================================="
echo "📝 API Documentation: http://127.0.0.1:8000/docs"
echo "🛑 Press Ctrl+C to stop the server"
echo "=================================================="

uvicorn career_agent_ai.app:app --reload --host 0.0.0.0 --port 8000
