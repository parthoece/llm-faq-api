#!/usr/bin/env python3
"""
Final verification test - simplified version
"""

import sys
import time
import subprocess
import requests

def test_all():
    print("=== LLM FAQ API - Final Verification ===\n")
    
    # 1. Test Python environment
    print(f"✓ Python version: {sys.version.split()[0]}")
    
    # 2. Test Ollama
    try:
        result = subprocess.run(['ollama', 'list'], capture_output=True, text=True, timeout=5)
        if 'llama3.2:1b' in result.stdout:
            print("✓ Ollama service and model available")
        else:
            print("⚠ Ollama model might not be available")
    except:
        print("✗ Ollama not available")
    
    # 3. Test API endpoints
    try:
        # Health check
        response = requests.get('http://localhost:8000/health', timeout=5)
        if response.status_code == 200:
            print("✓ Health endpoint working")
        else:
            print(f"⚠ Health endpoint returned {response.status_code}")
            
        # FAQ endpoint
        payload = {"question": "What is Python?", "context": "Programming"}
        response = requests.post('http://localhost:8000/faq/ask', json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            answer = data.get('answer', '')
            if answer and len(answer) > 10:
                print("✓ FAQ endpoint working")
                print(f"  Sample answer: {answer[:80]}...")
            else:
                print("⚠ FAQ endpoint returned empty answer")
        else:
            print(f"⚠ FAQ endpoint returned {response.status_code}")
            
    except requests.exceptions.ConnectionError:
        print("✗ API server not reachable")
    except Exception as e:
        print(f"✗ API test error: {e}")
    
    print("\n=== Test Complete ===")
    print("\nTo use the API:")
    print("1. Visit http://localhost:8000/docs for interactive documentation")
    print("2. Test with: curl -X POST 'http://localhost:8000/faq/ask' -H 'Content-Type: application/json' -d '{\"question\": \"What is Python?\"}'")

if __name__ == "__main__":
    test_all()
