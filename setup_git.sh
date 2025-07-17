#!/bin/bash

echo "🚀 Git Repository Setup Script"
echo "=============================="

# Check if we're in a git repository
if [ ! -d ".git" ]; then
    echo "📁 Initializing git repository..."
    git init
    echo "✅ Git repository initialized"
else
    echo "✅ Git repository already exists"
fi

# Add all files
echo "📦 Adding all files to git..."
git add .

# Commit changes
echo "💾 Committing changes..."
git commit -m "feat: Complete LLM FAQ API with comprehensive README

- 📝 Complete README.md with project summary and setup guides
- 🚀 FastAPI application with health check and FAQ endpoints  
- 🤖 Ollama LLM integration with error handling
- 🐳 Dev container setup for GitHub Codespaces
- 🧪 Comprehensive test suite
- 📁 Complete project structure and documentation
- 🔧 VS Code workspace configuration
- 🛠️ Environment setup and troubleshooting guides"

# Check status
echo "📊 Git status:"
git status

echo ""
echo "🎉 Local git repository is ready!"
echo ""
echo "To push to GitHub:"
echo "1. Create a new repository on GitHub"
echo "2. Run: git remote add origin https://github.com/yourusername/llm-faq-api.git"
echo "3. Run: git branch -M main"
echo "4. Run: git push -u origin main"
echo ""
echo "Your README and all files are now in git! 🎊"
