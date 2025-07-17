from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
from app.llm import ask_question

app = FastAPI(title="LLM FAQ API", description="A FAQ API powered by LLM and Stack Overflow data")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

class FAQRequest(BaseModel):
    question: str
    context: str = ""

@app.get("/")
def root():
    return {"message": "LLM FAQ API is running", "status": "healthy"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "message": "API is operational"}

@app.get("/stackoverflow/search")
def search_stackoverflow(query: str):
    """Search Stack Overflow for questions and answers."""
    try:
        # Use Stack Exchange API
        url = "https://api.stackexchange.com/2.3/search"
        params = {
            "order": "desc",
            "sort": "relevance",
            "intitle": query,
            "site": "stackoverflow"
        }
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching Stack Overflow: {str(e)}")

@app.post("/faq/ask")
def faq_ask(request: FAQRequest):
    """Ask a question and get an AI-powered answer."""
    try:
        # Combine question and context
        full_context = f"Context: {request.context}\nQuestion: {request.question}" if request.context else request.question
        answer = ask_question(full_context)
        return {"answer": answer, "question": request.question}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating answer: {str(e)}")