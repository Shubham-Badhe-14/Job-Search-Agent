#!/bin/bash

# Check if venv exists
if [ -d "agent_env" ]; then
    source agent_env/bin/activate
else
    echo "⚠️  Virtual environment 'agent_env' not found!"
    exit 1
fi

echo "=================================================="
echo "🚀 Starting CareerAgent AI Frontend"
echo "=================================================="

streamlit run streamlit_app.py --server.port 8501 --server.headless true --browser.gatherUsageStats false --server.headless true --browser.gatherUsageStats false
