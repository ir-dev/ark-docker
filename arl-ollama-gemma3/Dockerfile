# Use official Python image as base (required for Azure App Service)
FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama using official method
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

# Copy local app folder (must contain app.py and requirements.txt)
COPY --chown=ollama_user:ollama_user . .

# Install Python dependencies
RUN pip install --user -r requirements.txt

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
# Start Python application\n\
echo "Starting Python application..."\n\
python app.py &\n\
\n\
echo "Service is ready"\n\
echo "Ollama API: http://localhost:11434"\n\
echo "Web app: http://localhost:5000"\n\
\n\
# Keep container running\n\
tail -f /dev/null' > entrypoint.sh && \
    chmod +x entrypoint.sh

# Expose ports
EXPOSE 5000 11434

# Start the service
ENTRYPOINT ["./entrypoint.sh"]