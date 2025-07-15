import os
import requests
from app.stackoverflow import fetch_stackoverflow_posts

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

def ask_question(query: str):
    so_posts = fetch_stackoverflow_posts(query)

    prompt = f"""Use the following Stack Overflow posts to answer the user's question.

Stack Overflow:
{chr(10).join(so_posts)}

User Question:
{query}
"""

    response = requests.post(
        f"{OLLAMA_HOST}/api/generate",
        json={"model": OLLAMA_MODEL, "prompt": prompt}
    )

    if response.status_code != 200:
        return {"error": "Failed to generate response from LLaMA."}

    result = response.json()
    return {"answer": result.get("response", "[No output]")}