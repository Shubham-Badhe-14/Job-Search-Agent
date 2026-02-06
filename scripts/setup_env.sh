#!/bin/bash
set -e

# Ensure we are in the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

# Verify we are in the project root
if [ ! -f "requirements.txt" ]; then
    echo "Error: requirements.txt not found. Please run this script from the project root."
    exit 1
fi

if [ ! -d "agent_env" ]; then
    echo "Creating virtual environment..."
    python3 -m venv agent_env
fi

source agent_env/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

if [ ! -f ".env" ]; then
    if [ -f "configs/.env.example" ]; then
        echo "Creating .env from example..."
        cp configs/.env.example .env
        echo "Created .env. Please update it with your API keys."
    else
        echo "Warning: No .env or configs/.env.example found."
    fi
fi

echo "Setup complete."
