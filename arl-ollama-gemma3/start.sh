#!/bin/bash

echo "Reacehd server."

# Start Ollama server in background
ollama serve &

# Wait until server is responsive
until curl -s http://localhost:11434 > /dev/null; do
  echo "Waiting for Ollama server to start..."
  sleep 2
done

# Pull model
ollama pull gemma:3b

# Wait to keep container running
wait
