# LLM-Powered FAQ API (StackOverflow + LLaMA)

This project uses FastAPI + MongoDB + StackOverflow live data + Ollama-based LLaMA model.

##  Usage (on GitHub Codespaces or locally)

### Setup

1. Copy `.env.example` → `.env`
2. Run locally:
```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Or use Docker:

```bash
docker-compose up --build
```

### Visit Swagger UI:
http://localhost:8000/docs
