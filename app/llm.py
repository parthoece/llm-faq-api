import os
import requests
import json
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2:1b")

def ask_question(query: str):
    """Ask a question to the LLM and get an answer."""
    try:
        # For now, we'll just use the LLM directly without Stack Overflow integration
        # to keep it simple and ensure it works
        
        prompt = f"""Please answer the following question clearly and concisely:

Question: {query}

Answer:"""

        logger.info(f"Sending request to Ollama at {OLLAMA_HOST}")
        logger.info(f"Using model: {OLLAMA_MODEL}")
        
        response = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": OLLAMA_MODEL, 
                "prompt": prompt,
                "stream": False  # Important: disable streaming for simpler response
            },
            timeout=60  # Increase timeout for LLM response
        )

        logger.info(f"Ollama response status: {response.status_code}")
        
        if response.status_code != 200:
            logger.error(f"Ollama error: {response.text}")
            return f"Error: Failed to generate response from Ollama (status {response.status_code})"

        result = response.json()
        logger.info(f"Ollama response keys: {list(result.keys())}")
        
        answer = result.get("response", "[No output generated]")
        if not answer or answer.strip() == "":
            return "Sorry, I couldn't generate a meaningful response."
            
        return answer.strip()

    except requests.exceptions.RequestException as e:
        logger.error(f"Request error: {e}")
        return f"Error: Could not connect to Ollama service - {str(e)}"
    except json.JSONDecodeError as e:
        logger.error(f"JSON decode error: {e}")
        return "Error: Invalid response from Ollama service"
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return f"Error: {str(e)}"