# a01_test_ai.py
# Script to test the LLM model using Ollama API.

import json
import os
import requests
import sys
import numpy as np # Keep numpy import
from tqdm import tqdm # Keep tqdm import

# Set UTF-8 encoding for Windows console
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load configuration from config.json
def load_config():
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

CONFIG = load_config()

# Get backend configuration
BACKEND_TYPE = CONFIG.get('backend', {}).get('type', 'ollama')
API_BASE_URL = CONFIG.get('backend', {}).get('api_base_url', 'http://localhost:11434')
LLM_MODEL = CONFIG.get('models', {}).get('llm_model', 'qwen3.5:0.8b')

# Generation settings
MAX_TOKENS = CONFIG.get('generation', {}).get('max_tokens', 500) # Reduced tokens for quick test
TEMPERATURE = CONFIG.get('generation', {}).get('temperature', 0.7)

def check_ollama_api_status(base_url):
    """Checks if Ollama API is accessible at the given base URL."""
    try:
        response = requests.get(base_url + "/api/tags", timeout=5)
        if response.status_code == 200:
            return True, "Ollama API is accessible."
        else:
            return False, "Ollama API returned status code " + str(response.status_code) + "."
    except requests.exceptions.ConnectionError:
        return False, "Could not connect to Ollama API. Is Ollama running?"
    except Exception as e:
        return False, "An unexpected error occurred: " + str(e)

def test_llm_model(model_name, api_base_url, backend_type, prompt, max_tokens, temperature):
    """Tests the LLM model by sending a prompt and printing the response."""
    print("\n" + "="*60)
    print("Testing LLM Model: {}".format(model_name)) # Simplified print
    print("======================================================================")

    api_available = False
    if backend_type == 'ollama':
        is_running, msg = check_ollama_api_status(api_base_url)
        if is_running:
            api_available = True
            print("[OK] Ollama API is running.")
        else:
            print("[!] Ollama API check failed: " + msg)
            print("[WARN] Ollama API may not be running properly!")
    else: # Assume OpenAI-compatible
        try:
            response = requests.get(api_base_url + "/v1/models", timeout=5)
            if response.status_code == 200:
                print("[OK] API Server is running (OpenAI-compatible).")
                api_available = True
            else:
                print("[!] API: Cannot connect to API Server (Status: " + str(response.status_code) + ")")
                print("[WARN] API server may not be running properly!")
        except requests.exceptions.RequestException as e:
            print("[!] API: Cannot connect to API Server")
            print("[!] Error details: " + str(e))
            print("[WARN] API server may not be running properly!")

    if not api_available:
        print("\n[ERROR] Essential API services are not available. Exiting LLM test.")
        return False

    try:
        if backend_type == 'ollama':
            response = requests.post(
                api_base_url + "/api/generate",
                json={
                    "model": model_name,
                    "prompt": prompt,
                    "stream": False,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=120 # Increased timeout for model loading/generation
            )
        else: # Assume OpenAI-compatible
            response = requests.post(
                api_base_url + "/v1/chat/completions",
                json={
                    "model": model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "stream": False
                },
                timeout=120 # Increased timeout for model loading/generation
            )
        
        response.raise_for_status()
        data = response.json()

        # Handle different response formats
        if BACKEND_TYPE == 'ollama':
            content = data.get("response", "Error: No content received.")
        else: # OpenAI-compatible
            content = data.get("choices", [{}])[0].get("message", {}).get("content", "Error: No content received.")
        
        print("\n--- LLM Response ---")
        print(content)
        print("--------------------")
        print("[SUCCESS] LLM model test completed.")
        return True

    except requests.exceptions.RequestException as e:
        print("[ERROR] API Request Failed: " + str(e))
        print("Error: Could not connect to the LLM API. Ensure Ollama is running and the model is loaded.")
        return False
    except Exception as e:
        print("[ERROR] Unexpected error during LLM response generation: " + str(e))
        return False

if __name__ == "__main__":
    print("Starting LLM model test...")
    
    # Test the LLM model
    prompt_text = "สวัสดีครับ! คุณคือใคร?" # "Hello! Who are you?" in Thai
    if test_llm_model(LLM_MODEL, API_BASE_URL, BACKEND_TYPE, prompt_text, MAX_TOKENS, TEMPERATURE):
        print("\nLLM model test finished successfully.")
    else:
        print("\nLLM model test failed. Please check the error messages above.")
        sys.exit(1)
