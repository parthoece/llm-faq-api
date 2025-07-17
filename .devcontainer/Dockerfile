# Base image
FROM mcr.microsoft.com/devcontainers/python:1-3.10

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3-venv \
    curl \
    git \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set work directory
WORKDIR /workspaces/llm-faq-api

# Copy requirements early to leverage cache
COPY requirements.txt .

# Optional: Pre-install packages into global Python (but usually not needed)
# RUN pip install --upgrade pip && pip install -r requirements.txt
