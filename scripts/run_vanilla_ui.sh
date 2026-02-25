#!/bin/bash
# scripts/run_vanilla_ui.sh

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

# Navigate to the vanilla-ui directory
cd "$PROJECT_ROOT/frontend/vanilla-ui"

echo "Starting Vanilla JS UI at http://localhost:8080..."
python3 -m http.server 8080
