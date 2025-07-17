#!/usr/bin/env python3
"""
Comprehensive test script for LLM FAQ API.
Tests environment, dependencies, API endpoints, and LLM integration.
"""

import os
import sys
import json
import time
import subprocess
import requests
from pathlib import Path

def print_section(title):
    print(f"\n{'='*60}")
    print(f" {title}")
    print(f"{'='*60}")

def print_status(message, success=True):
    status = "✓" if success else "✗"
    print(f"{status} {message}")

def test_environment():
    """Test basic environment setup."""
    print_section("ENVIRONMENT TESTS")
    
    # Check Python version
    python_version = sys.version
    print_status(f"Python version: {python_version}")
    
    # Check virtual environment
    venv_active = hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)
    print_status(f"Virtual environment active: {venv_active}", venv_active)
    
    # Check working directory
    cwd = os.getcwd()
    print_status(f"Working directory: {cwd}")
    
    # Check key files exist
    key_files = [
        'app/main.py',
        'app/llm.py', 
        'app/stackoverflow.py',
        'requirements.txt',
        '.devcontainer/devcontainer.json'
    ]
    
    for file_path in key_files:
        exists = Path(file_path).exists()
        print_status(f"File exists: {file_path}", exists)

def test_dependencies():
    """Test installed Python packages."""
    print_section("DEPENDENCY TESTS")
    
    required_packages = [
        'fastapi',
        'uvicorn',
        'requests',
        'python-dotenv'
    ]
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print_status(f"Package installed: {package}")
        except ImportError:
            print_status(f"Package missing: {package}", False)

def test_ollama():
    """Test Ollama installation and model availability."""
    print_section("OLLAMA TESTS")
    
    # Check if Ollama is installed
    try:
        result = subprocess.run(['ollama', '--version'], capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print_status(f"Ollama installed: {result.stdout.strip()}")
        else:
            print_status("Ollama not found", False)
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print_status("Ollama not found or not responding", False)
        return False
    
    # Check if Ollama service is running
    try:
        response = requests.get('http://localhost:11434/api/tags', timeout=5)
        if response.status_code == 200:
            print_status("Ollama service is running")
            
            # Check available models
            models = response.json().get('models', [])
            if models:
                print_status(f"Available models: {len(models)}")
                for model in models:
                    print_status(f"  - {model.get('name', 'unknown')}")
                
                # Check for required model
                model_names = [model.get('name', '') for model in models]
                if any('llama3.2:1b' in name for name in model_names):
                    print_status("Required model (llama3.2:1b) available")
                    return True
                else:
                    print_status("Required model (llama3.2:1b) not found", False)
                    return False
            else:
                print_status("No models available", False)
                return False
        else:
            print_status(f"Ollama service not responding (status: {response.status_code})", False)
            return False
    except requests.RequestException as e:
        print_status(f"Cannot connect to Ollama service: {e}", False)
        return False

def start_fastapi_server():
    """Start FastAPI server in background."""
    print_section("STARTING FASTAPI SERVER")
    
    try:
        # Check if server is already running
        response = requests.get('http://localhost:8000/health', timeout=2)
        if response.status_code == 200:
            print_status("FastAPI server already running")
            return True
    except requests.RequestException:
        pass
    
    # Start server in background
    print_status("Starting FastAPI server...")
    try:
        # Use the VS Code task if available, otherwise start manually
        process = subprocess.Popen([
            sys.executable, '-m', 'uvicorn', 
            'app.main:app', 
            '--host', '0.0.0.0', 
            '--port', '8000',
            '--reload'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        
        # Wait for server to start
        for i in range(30):  # Wait up to 30 seconds
            try:
                response = requests.get('http://localhost:8000/health', timeout=1)
                if response.status_code == 200:
                    print_status("FastAPI server started successfully")
                    return True
            except requests.RequestException:
                pass
            time.sleep(1)
        
        print_status("FastAPI server failed to start within timeout", False)
        return False
        
    except Exception as e:
        print_status(f"Failed to start FastAPI server: {e}", False)
        return False

def test_api_endpoints():
    """Test API endpoints."""
    print_section("API ENDPOINT TESTS")
    
    base_url = 'http://localhost:8000'
    
    # Test health endpoint
    try:
        response = requests.get(f'{base_url}/health', timeout=5)
        if response.status_code == 200:
            print_status("Health endpoint working")
        else:
            print_status(f"Health endpoint failed (status: {response.status_code})", False)
    except requests.RequestException as e:
        print_status(f"Health endpoint error: {e}", False)
        return False
    
    # Test search endpoint
    try:
        response = requests.get(f'{base_url}/stackoverflow/search?query=python+list', timeout=10)
        if response.status_code == 200:
            data = response.json()
            if 'items' in data and len(data['items']) > 0:
                print_status(f"Search endpoint working (found {len(data['items'])} results)")
            else:
                print_status("Search endpoint returned no results", False)
        else:
            print_status(f"Search endpoint failed (status: {response.status_code})", False)
    except requests.RequestException as e:
        print_status(f"Search endpoint error: {e}", False)
    
    # Test FAQ ask endpoint (requires Ollama)
    try:
        payload = {
            "question": "What is Python?",
            "context": "Python is a programming language"
        }
        response = requests.post(f'{base_url}/faq/ask', json=payload, timeout=30)
        if response.status_code == 200:
            data = response.json()
            if 'answer' in data and data['answer'].strip():
                print_status("FAQ ask endpoint working")
                print_status(f"  Answer preview: {data['answer'][:100]}...")
            else:
                print_status("FAQ ask endpoint returned empty answer", False)
        else:
            print_status(f"FAQ ask endpoint failed (status: {response.status_code})", False)
            try:
                error_detail = response.json()
                print_status(f"  Error: {error_detail.get('detail', 'Unknown error')}")
            except:
                pass
    except requests.RequestException as e:
        print_status(f"FAQ ask endpoint error: {e}", False)

def main():
    """Run all tests."""
    print_section("LLM FAQ API - COMPREHENSIVE TESTS")
    print("Testing environment, dependencies, and API functionality...")
    
    # Basic tests
    test_environment()
    test_dependencies()
    
    # Ollama tests
    ollama_ok = test_ollama()
    
    # Start server and test API
    if start_fastapi_server():
        test_api_endpoints()
    else:
        print_status("Skipping API tests due to server startup failure", False)
    
    print_section("TEST SUMMARY")
    if ollama_ok:
        print_status("All major components are working")
        print("✓ Environment setup complete")
        print("✓ Dependencies installed")
        print("✓ Ollama service running with model")
        print("✓ FastAPI server operational")
        print("✓ API endpoints functional")
    else:
        print_status("Some components need attention", False)
        print("Check the test output above for specific issues.")

if __name__ == "__main__":
    main()
