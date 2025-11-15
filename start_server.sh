#!/bin/bash

# Start the Financial Advisory System Web UI
echo "Starting Financial Advisory System Web Server..."
echo ""

# Get the directory where this script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "Activating virtual environment..."
    source venv/bin/activate
else
    echo "Creating virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Check if uvicorn is installed
if ! python -c "import uvicorn" 2>/dev/null; then
    echo "uvicorn not found. Installing dependencies..."
    pip install fastapi uvicorn
fi

# Start the server
echo ""
echo "=========================================="
echo "Server starting on http://localhost:8000"
echo "=========================================="
echo "Press Ctrl+C to stop the server"
echo ""
uvicorn api:app --reload --host 0.0.0.0 --port 8000

