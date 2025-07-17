#!/bin/bash
# Auto-activate virtual environment for all terminal sessions
echo "Setting up automatic virtual environment activation..."

# Add activation to bashrc if not already present
if ! grep -q "source .venv/bin/activate" ~/.bashrc; then
    echo 'if [ -d "/workspaces/llm-faq-api/.venv" ]; then' >> ~/.bashrc
    echo '    source /workspaces/llm-faq-api/.venv/bin/activate' >> ~/.bashrc
    echo '    echo "🐍 Virtual environment activated!"' >> ~/.bashrc
    echo 'fi' >> ~/.bashrc
fi
