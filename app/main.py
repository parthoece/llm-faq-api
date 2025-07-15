from fastapi import FastAPI
from app.llm import ask_question
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

@app.get("/")
def root():
    return {"msg": "LLM FAQ API"}

@app.post("/faq/ask")
def faq_ask(q: str):
    return ask_question(q)