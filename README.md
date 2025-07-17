# LLM FAQ API

A FastAPI-based service that provides an intelligent FAQ system powered by Large Language Models (LLM) through Ollama, with integration capabilities for Stack Overflow data.

## Project Summary

This project creates a RESTful API that can answer user questions using a locally-hosted LLM via Ollama. The API is designed to be lightweight, fast, and easily deployable in development environments like GitHub Codespaces or local Docker containers.

### Key Features

- **FastAPI Framework**: Modern, fast web framework for building APIs with automatic interactive documentation
- **Ollama Integration**: Local LLM inference using the popular Ollama platform
- **Stack Overflow Integration**: Capability to search and integrate Stack Overflow data for enhanced answers
- **Containerized Development**: Full dev container support for GitHub Codespaces and local development
- **Health Monitoring**: Built-in health check endpoints for monitoring service status
- **CORS Support**: Cross-origin resource sharing enabled for web applications

### Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Client/Web    │───▶│   FastAPI App   │───▶│   Ollama LLM    │
│   Application   │    │  (app/main.py)  │    │  (llama3.2:1b)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Stack Overflow  │
                       │  API (Optional) │
                       └─────────────────┘
```

## Quick Start

### Prerequisites

- Python 3.10+ 
- 4GB+ RAM (for LLM model)
- Internet connection (for initial setup)

### Option 1: GitHub Codespaces (Recommended)

1. **Fork or clone this repository**
2. **Open in Codespaces**: Click "Code" → "Create codespace on main"
3. **Wait for setup**: The devcontainer will automatically:
   - Install Python dependencies
   - Install and configure Ollama
   - Pull the LLM model (llama3.2:1b)
   - Set up the development environment

4. **Start the API**:
   ```bash
   # The environment should be ready, just start the server
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Test the API**:
   ```bash
   # Health check
   curl http://localhost:8000/health
   
   # Ask a question
   curl -X POST "http://localhost:8000/faq/ask" \
        -H "Content-Type: application/json" \
        -d '{"question": "What is Python?", "context": "Programming language"}'
   ```

### Option 2: Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd llm-faq-api
   ```

2. **Set up Python environment**:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. **Install and configure Ollama**:
   ```bash
   # Install Ollama (Linux/macOS)
   curl -fsSL https://ollama.ai/install.sh | sh
   
   # Start Ollama service
   ollama serve &
   
   # Pull the LLM model
   ollama pull llama3.2:1b
   ```

4. **Start the FastAPI server**:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

5. **Verify the setup**:
   ```bash
   python test_api.py
   ```

## API Documentation

Once the server is running, visit:
- **Interactive API docs**: http://localhost:8000/docs
- **Alternative docs**: http://localhost:8000/redoc

### Endpoints

#### Health Check
```http
GET /health
```
Returns the service health status.

**Response**:
```json
{
  "status": "healthy",
  "message": "API is operational"
}
```

#### Ask Question
```http
POST /faq/ask
```
Submit a question to get an AI-powered answer.

**Request Body**:
```json
{
  "question": "What is Python?",
  "context": "Programming language basics"
}
```

**Response**:
```json
{
  "answer": "Python is a high-level, interpreted programming language...",
  "question": "What is Python?"
}
```

#### Search Stack Overflow
```http
GET /stackoverflow/search?query=python+list
```
Search Stack Overflow for relevant questions and answers.

**Response**:
```json
{
  "items": [
    {
      "title": "How to create a list in Python",
      "link": "https://stackoverflow.com/questions/...",
      "score": 15
    }
  ]
}
```

## Development Setup

### File Structure

```
llm-faq-api/
├── .devcontainer/
│   ├── devcontainer.json      # Dev container configuration
│   ├── setup.sh              # Automated setup script
│   └── profile.sh            # Shell profile setup
├── .vscode/
│   └── settings.json         # VS Code workspace settings
├── app/
│   ├── __init__.py          # Python package marker
│   ├── main.py              # FastAPI application
│   ├── llm.py               # LLM integration logic
│   └── stackoverflow.py     # Stack Overflow API client
├── requirements.txt          # Python dependencies
├── test_api.py              # Comprehensive test suite
├── .env.example             # Environment variables template
└── README.md                # This file
```

### Environment Variables

Copy `.env.example` to `.env` and customize:

```bash
# Ollama Configuration
OLLAMA_HOST=http://localhost:11434
OLLAMA_MODEL=llama3.2:1b

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000

# Stack Overflow API (optional)
STACKOVERFLOW_API_KEY=your_key_here
```

### Running Tests

The project includes a comprehensive test suite:

```bash
# Run all tests
python test_api.py

# Or run individual components
python -c "
import requests
response = requests.get('http://localhost:8000/health')
print(response.json())
"
```

### Development Commands

```bash
# Start with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Install new dependencies
pip install package_name
pip freeze > requirements.txt

# Check Ollama status
ollama list
ollama ps

# Pull different models
ollama pull llama3.2:3b  # Larger model for better responses
```

## Troubleshooting

### Common Issues

#### 1. Ollama Service Not Running
**Error**: `Cannot connect to Ollama service`

**Solution**:
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start Ollama service
ollama serve &

# Verify it's working
curl http://localhost:11434/api/tags
```

#### 2. Model Not Available
**Error**: `model not found`

**Solution**:
```bash
# List available models
ollama list

# Pull the required model
ollama pull llama3.2:1b

# Or try a different model
ollama pull llama3.2:3b
```

#### 3. Python Virtual Environment Issues
**Error**: `ModuleNotFoundError`

**Solution**:
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### 4. FastAPI Server Won't Start
**Error**: `Port already in use`

**Solution**:
```bash
# Find and kill existing process
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn app.main:app --host 0.0.0.0 --port 8001
```

#### 5. Slow LLM Responses
**Issue**: API timeouts or very slow responses

**Solutions**:
- Use a smaller model: `ollama pull llama3.2:1b`
- Increase timeout values in the code
- Ensure sufficient RAM (4GB+ recommended)
- Check system resources: `htop` or `top`

### Development Environment Issues

#### GitHub Codespaces
- **Issue**: Dev container setup fails
- **Solution**: Rebuild container: Command Palette → "Codespaces: Rebuild Container"

#### VS Code
- **Issue**: Python interpreter not found
- **Solution**: Command Palette → "Python: Select Interpreter" → Choose `.venv/bin/python`

### Logging and Debugging

Enable detailed logging:

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

Check FastAPI logs:
```bash
# Run with debug output
uvicorn app.main:app --reload --log-level debug
```

## Performance Considerations

### Resource Requirements

- **Minimum**: 2 CPU cores, 4GB RAM
- **Recommended**: 4 CPU cores, 8GB RAM
- **Storage**: 2GB for model files

### Optimization Tips

1. **Model Selection**:
   - `llama3.2:1b` - Fast, basic responses
   - `llama3.2:3b` - Better quality, slower
   - `llama3.2:7b` - Best quality, requires more resources

2. **Caching**:
   - Implement response caching for frequently asked questions
   - Cache Stack Overflow search results

3. **Concurrent Requests**:
   - Ollama handles concurrent requests but may be slower
   - Consider implementing request queuing for high load

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Submit a pull request with a clear description

### Development Guidelines

- Follow PEP 8 style guide
- Add type hints to functions
- Include docstrings for public functions
- Update tests when adding features
- Update this README for significant changes

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Support

- **Issues**: Open an issue on GitHub
- **Documentation**: Check the `/docs` endpoint when server is running
- **Community**: Join discussions in GitHub Issues

## Changelog

### v1.0.0 (Current)
- Initial release
- FastAPI integration
- Ollama LLM support
- Stack Overflow API integration
- GitHub Codespaces support
- Comprehensive testing suite
- Full documentation

---

**Quick Test Command**:
```bash
curl -X POST "http://localhost:8000/faq/ask" \
     -H "Content-Type: application/json" \
     -d '{"question": "How do I create a Python list?", "context": "Python basics"}'
```

This should return an AI-generated answer about creating Python lists!
