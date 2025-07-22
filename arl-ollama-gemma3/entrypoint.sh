#!/bin/bash
set -e

# Start Ollama in background
echo "Starting Ollama..."
ollama serve &

# Wait for Ollama to start
sleep 5

# Start the dummy Flask app (required for Azure health checks)
echo "Starting dummy web app..."
python -m flask run --host=0.0.0.0 --port=8000 &

# Keep container running
tail -f /dev/null