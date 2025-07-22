# Use official Python image as base (required for Azure App Service)
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama - PROPER METHOD
RUN curl -fsSL https://ollama.com/install.sh | sh

# Verify Ollama installation
RUN test -f /usr/bin/ollama && echo "Ollama installed successfully" || echo "Ollama installation failed"

# Set environment variables
ENV OLLAMA_HOST=0.0.0.0
ENV PATH="${PATH}:/usr/local/bin"

# Create non-root user
RUN useradd -m -d /home/ollama_user ollama_user && \
    mkdir -p /home/ollama_user/.ollama && \
    chown ollama_user:ollama_user /home/ollama_user/.ollama

# Switch to non-root user
USER ollama_user
WORKDIR /home/ollama_user

# Create minimal Flask app for Azure health checks
RUN mkdir -p app && \
    echo "from flask import Flask\napp = Flask(__name__)\n\n@app.route('/')\ndef health():\n    return 'OK', 200\n\nif __name__ == '__main__':\n    app.run(host='0.0.0.0', port=8000)" > app/app.py && \
    echo "flask==2.0.1" > app/requirements.txt && \
    pip install --user -r app/requirements.txt

# Create startup script
RUN echo '#!/bin/bash\n\
set -e\n\
\n\
# Verify Ollama is installed\n\
if ! command -v ollama &> /dev/null; then\n\
    echo "ERROR: Ollama not found in PATH!"\n\
    exit 1\n\
fi\n\
\n\
# Start Ollama server\n\
echo "Starting Ollama server..."\n\
ollama serve &\n\
\n\
# Wait for server to start\n\
echo "Waiting for server to initialize..."\n\
while ! curl -s http://localhost:11434 >/dev/null; do\n\
    sleep 1\n\
done\n\
\n\
# Download Gemma model if not present\n\
if ! ollama list | grep -q gemma; then\n\
    echo "Downloading Gemma 2B model..."\n\
    ollama pull gemma:2b\n\
fi\n\
\n\
# Start Flask health check endpoint\n\
echo "Starting health check endpoint..."\n\
python -m flask run --app app/app.py --host=0.0.0.0 --port=8000 &\n\
\n\
echo "Service is ready"\n\
echo "Ollama API: http://localhost:11434"\n\
echo "Health check: http://localhost:8000"\n\
\n\
# Keep container running\n\
tail -f /dev/null' > entrypoint.sh && \
    chmod +x entrypoint.sh

# Expose ports
EXPOSE 8000
EXPOSE 11434

# Start the service
ENTRYPOINT ["./entrypoint.sh"]