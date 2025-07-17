#!/bin/bash

# Setup script for Codespaces
echo "🚀 Setting up LLM FAQ API development environment..."

# Remove any existing corrupted virtual environment
if [ -d ".venv" ]; then
    echo "🧹 Cleaning up existing virtual environment..."
    rm -rf .venv
fi

# Create fresh virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip to latest version
echo "⬆️ Upgrading pip..."
python -m pip install --upgrade pip

# Install requirements
if [ -f "requirements.txt" ]; then
    echo "📋 Installing requirements from requirements.txt..."
    pip install -r requirements.txt
    echo "✅ Requirements installed successfully!"
else
    echo "⚠️ requirements.txt not found, skipping package installation"
fi

# Verify installation
echo "🔍 Verifying installations..."
pip list

echo "🎉 Setup complete! Virtual environment is ready."
echo "💡 Your Python packages are installed and ready to use."
echo "🚀 You can now run: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload"
