FROM python:3.9-slim

# Install system dependencies
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    curl ca-certificates && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama (official method)
RUN curl -fsSL https://ollama.com/install.sh | sh

# Create non-root user
RUN useradd -m ollama_user && \
    mkdir -p /home/ollama_user/.ollama && \
    chown ollama_user:ollama_user /home/ollama_user/.ollama

WORKDIR /app
COPY --chown=ollama_user:ollama_user . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Environment variables
ENV FLASK_APP=app.py
ENV OLLAMA_HOST=0.0.0.0
ENV MODEL_NAME=gemma2

USER ollama_user

EXPOSE 5000 11434

# Startup script
CMD ["sh", "-c", \
     "ollama serve & \
     while ! curl -s http://localhost:11434 >/dev/null; do sleep 1; done && \
     echo 'Downloading model...' && \
     ollama pull gemma2 && \
     echo 'Starting Flask...' && \
     flask run --host=0.0.0.0 --port=5000"]