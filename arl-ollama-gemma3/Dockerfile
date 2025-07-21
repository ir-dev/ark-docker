## Use the official Ollama base image
#FROM ollama/ollama:latest
#
#RUN ollama pull gemma3:latest
#
#RUN ollama run gemma3
#
## Expose the Ollama port
#EXPOSE 11434

#FROM ubuntu:22.04
#
## Install dependencies
#RUN apt-get update && apt-get install -y curl gnupg
#
## Add Ollama package source
#RUN curl -fsSL https://ollama.com/install.sh | sh
#
## Pull model (can also be done at runtime)
#RUN /bin/bash -c "source ~/.bashrc && ollama serve & sleep 5 && ollama pull gemma3:latest"
#
## Expose Ollama API port
#EXPOSE 11434
#
## Start the Ollama server
#CMD ["ollama", "serve"]
#

FROM ubuntu:22.04

# Install dependencies
RUN apt-get update && \
    apt-get install -y curl && \
    rm -rf /var/lib/apt/lists/*

# Install Ollama
RUN curl -fsSL https://ollama.com/install.sh | sh

# Add Ollama to PATH
ENV PATH=$PATH:/usr/local/bin

# Pre-download model (optional - can be done at runtime instead)
#RUN ollama pull gemma3:latest && \
#    ollama rm gemma3:latest  # Remove to save space, will redownload on first run

# Create startup script
RUN echo '#!/bin/bash\n\
ollama serve &\n\
sleep 5\n\
if ! ollama list | grep -q gemma; then\n\
  echo "Downloading Gemma model..."\n\
  ollama pull gemma3:latest\n\
fi\n\
tail -f /dev/null' > /start.sh && \
    chmod +x /start.sh

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=30s --retries=3 \
    CMD curl -f http://localhost:11434/api/tags || exit 1

# Expose Ollama API port
EXPOSE 11434

# Start the container
CMD ["/start.sh"]