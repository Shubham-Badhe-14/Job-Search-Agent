#!/bin/bash
set -e

# Trap Ctrl+C to kill both background processes
cleanup() {
    echo "Shutting down services..."
    kill $(jobs -p)
    wait
}
trap cleanup SIGINT SIGTERM EXIT

# Ensure we are in the project root
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
cd "$PROJECT_ROOT"

./scripts/run_backend.sh &
./scripts/run_frontend.sh &

wait
