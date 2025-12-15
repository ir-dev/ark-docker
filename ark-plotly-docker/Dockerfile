# Use an official Python runtime as a parent image
FROM python:3.10-slim-bullseye

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for headless Chrome for Kaleido
# This list is crucial and based on our previous troubleshooting
RUN apt update && apt install -y --no-install-recommends \
    wget \
    gnupg \
    libnss3 \
    libatk-bridge2.0-0 \
    libcups2 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    libxkbcommon0 \
    libpango-1.0-0 \
    libcairo2 \
    libasound2 \
    fonts-liberation \
    xdg-utils \
    lsb-release \
    # Clean up apt cache to keep image size small
    && rm -rf /var/lib/apt/lists/*

# Download and install Google Chrome (required for Kaleido)
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list \
    && apt update \
    && apt install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Copy the requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Expose the port your Gunicorn server will listen on
EXPOSE 5000

# Command to run the application using Gunicorn
CMD ["python", "app.py"]
# For a Flask app named 'app' in 'app.py':
# CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "app:app"]
# For a Dash app where `server = app.server` in `app.py`:
# CMD ["gunicorn", "--workers", "3", "--bind", "0.0.0.0:8000", "app:server"]