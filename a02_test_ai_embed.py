# a02_test_ai_embed.py
# Script to test the embedding model using Ollama API.

import json
import os
import requests
import sys
import numpy as np

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
EMBEDDING_MODEL = CONFIG.get('models', {}).get('embedding_model', 'nomic-embed-text:latest')

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

def test_embedding_model(model_name, api_base_url, backend_type, text_to_embed):
    """Tests the embedding model by sending text and printing embedding details."""
    print("\n" + "="*60)
    print("Testing Embedding Model: {}".format(model_name)) # Simplified print
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
        print("\n[ERROR] Essential API services are not available. Exiting embedding test.")
        return False

    try:
        if backend_type == 'ollama':
            response = requests.post(
                api_base_url + "/api/embeddings",
                json={"model": model_name, "prompt": text_to_embed},
                timeout=30
            )
        else: # Assume OpenAI-compatible
            response = requests.post(
                api_base_url + "/v1/embeddings",
                json={"model": model_name, "input": text_to_embed},
                timeout=30
            )
        
        response.raise_for_status() # Raise an exception for bad status codes
        data = response.json()
        
        # Handle different response formats
        embedding = data.get("embedding") or data.get("data", [{}])[0].get("embedding", [])

        if embedding:
            print("\n--- Embedding Result ---")
            print("  - Dimensions: {}".format(len(embedding)))
            print("  - First 5 values: {}".format(embedding[:5]))
            print("------------------------")
            print("[SUCCESS] Embedding model test completed.")
            return True
        else:
            print("[!] API Error: Could not extract embedding from response.")
            print("[!] Response content: " + response.text[:500]) # Print some response text for debugging
            return False

    except requests.exceptions.RequestException as e:
        print("[ERROR] API Request Failed: " + str(e))
        print("Error: Could not connect to the Embedding API. Ensure Ollama is running and the model is loaded.")
        return False
    except Exception as e:
        print("[ERROR] Unexpected error during embedding generation: " + str(e))
        return False

if __name__ == "__main__":
    print("Starting Embedding model test...")
    
    sample_text = "This is a test sentence to generate an embedding."
    if test_embedding_model(EMBEDDING_MODEL, API_BASE_URL, BACKEND_TYPE, sample_text):
        print("\nEmbedding model test finished successfully.")
    else:
        print("\nEmbedding model test failed. Please check the error messages above.")
        sys.exit(1)
