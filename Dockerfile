# F3V3R DR34M DOCKER RUNTIME - ULTIMATE KEYGEN STYLE
# ================================================
# Yo dawg, we're bout to drop some SICK infrastructure! 

# Base image that works on both Windows and Linux
FROM python:3.11-slim

# 1337 METADATA
LABEL maintainer="F3V3R DR34M CREW"
LABEL version="1.337"
LABEL description="ULTIMATE CROSS-PLATFORM DOCKER RUNTIME"

# Set environment variables for maximum SWAG
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV OLLAMA_HOST=0.0.0.0
ENV OLLAMA_PORT=11434

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Create our elite workspace
WORKDIR /f3v3r_dr34m

# Copy configuration and requirements
COPY requirements.txt config.yml ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Expose ports for Ollama and potential services
EXPOSE 11434
EXPOSE 7860

# Ultimate runtime command
CMD ["python", "main.py"]
