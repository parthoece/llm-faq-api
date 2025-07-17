#!/usr/bin/env python3
"""
Quick API test script
"""
import requests
import json

print("Testing LLM FAQ API...")

# Test health endpoint
try:
    response = requests.get('http://localhost:8000/health', timeout=5)
    print(f"Health: {response.status_code} - {response.json()}")
except Exception as e:
    print(f"Health error: {e}")

# Test FAQ endpoint
try:
    payload = {'question': 'What is Python?', 'context': 'Programming'}
    response = requests.post('http://localhost:8000/faq/ask', json=payload, timeout=60)
    print(f"FAQ: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Answer: {result.get('answer', 'No answer')[:100]}...")
    else:
        print(f"Error: {response.text}")
except Exception as e:
    print(f"FAQ error: {e}")

print("Test complete.")
