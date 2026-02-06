#!/bin/bash
set -e

# Ensure we are in the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

if [ -f "agent_env/bin/activate" ]; then
    source agent_env/bin/activate
fi

export PYTHONPATH=$PYTHONPATH:$(pwd)

echo "Starting Frontend..."
streamlit run frontend/streamlit_app.py --server.port 8501
