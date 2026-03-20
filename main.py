import json
import os
import sys
import requests
from pythainlp.util import normalize
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
EMBEDDING_MODEL = CONFIG.get('models', {}).get('embedding_model', 'nomic-embed-text:latest')

# Generation settings
MAX_TOKENS = CONFIG.get('generation', {}).get('max_tokens', 500) # Reduced tokens for quicker responses
TEMPERATURE = CONFIG.get('generation', {}).get('temperature', 0.2)

# Search settings
TOP_K = CONFIG.get('search', {}).get('top_k_chunks', 3)

# Show backend info on startup
print("\n[INFO] Using backend: " + BACKEND_TYPE.upper())

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

def get_embedding_with_api(text):
    """
    Get embedding using configured backend API.
    Supports Ollama, GPT4All, LM Studio, and other OpenAI-compatible APIs.
    """
    try:
        # --- Ollama specific endpoint ---
        if BACKEND_TYPE == 'ollama':
            try:
                # Check Ollama server status first
                is_running, msg = check_ollama_api_status(API_BASE_URL)
                if not is_running:
                    print("[WARN] Ollama check failed: " + msg)
                    print("[WARN] Falling back to semantic hash.")
                    return None # Fallback if Ollama not running
                
                response = requests.post(
                    API_BASE_URL + "/api/embeddings",
                    json={"model": EMBEDDING_MODEL, "prompt": text},
                    timeout=120 # Increased timeout for embedding generation to 120 seconds
                )
                if response.status_code == 200:
                    data = response.json()
                    embedding = data.get("embedding")
                    if embedding:
                        return embedding
                    else:
                        print("[!] Ollama API Error: Response OK, but 'embedding' key missing or empty.")
                        return None # Fallback if structure is wrong
                else:
                    print("[!] Ollama API Error: Status " + str(response.status_code))
                    print("[!] Response content: " + response.text[:500]) # Print some response text for debugging
                    return None # Fallback
            except requests.exceptions.RequestException as e:
                print("[!] Ollama Connection Error: " + str(e))
                print("[!] Falling back to semantic hash.")
                return None
            except Exception as e: # Catch any other unexpected errors
                print("[ERROR] Unexpected error during Ollama embedding call: " + str(e))
                return None

        # --- OpenAI-compatible API endpoint (GPT4All, LM Studio, etc.) ---
        else: # Assumed to be OpenAI-compatible
            response = requests.post(
                API_BASE_URL + "/v1/embeddings",
                json={"model": EMBEDDING_MODEL, "input": text},
                timeout=120 # Increased timeout for embedding generation to 120 seconds
            )
            response.raise_for_status() # Raise an exception for bad status codes
            data = response.json()
            # Handle different response formats
            embedding = data.get("data", [{}])[0].get("embedding", [])
            if embedding:
                return embedding
            else: # Handle case where 'data' might be empty or missing
                print("[!] API Error: Unexpected response format from /v1/embeddings.")
                return None
    
    except requests.exceptions.Timeout: # Catch specific Timeout error
        print("[ERROR] API Request Timed Out after 120 seconds.")
        print("Error: The embedding model took too long to respond. This might be due to system resources or model loading time.")
        return None
    except requests.exceptions.RequestException as e:
        print("[ERROR] API Request Failed: " + str(e))
        return "Error: Could not connect to the Embedding API. Ensure Ollama is running and the model is loaded."
    except Exception as e:
        print("[ERROR] Unexpected error during API call: " + str(e))
        return "Error: An unexpected issue occurred."

def generate_semantic_hash(text, dimensions=384):
    """Fallback embedding using deterministic hash"""
    import hashlib
    text = text.lower().strip()
    features = []
    for i in range(min(100, len(text))):
        features.append(ord(text[i]) / 256.0)
    words = text.split()
    features.append(len(words) / 100.0)
    if words:
        features.append(sum(len(w) for w in words) / len(words) / 20.0)
    else:
        features.append(0.0)
    thai_chars = sum(1 for c in text if '\u0E00' <= c <= '\u0E7F')
    features.append(thai_chars / max(len(text), 1))
    for i in range(0, dimensions - len(features)):
        hash_input = f"{text}:{i}".encode('utf-8')
        hash_val = int(hashlib.md5(hash_input).hexdigest()[:8], 16)
        features.append((hash_val % 1000) / 1000.0)
    features = features[:dimensions]
    while len(features) < dimensions:
        features.append(0.0)
    return [(f * 2 - 1) for f in features]

def cosine_similarity(a, b):
    a = np.array(a)
    b = np.array(b)
    # Handle zero vectors to prevent NaN
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def search_chunks(query, vector_db, top_k=3):
    query_emb = get_embedding_with_api(query) # Calls the corrected get_embedding_with_api

    if query_emb and len(vector_db) > 0 and "embedding" in vector_db[0]:
        print("[INFO] Performing Deep Vector Search with Embeddings...")
        results = []
        for chunk in vector_db:
            sim = cosine_similarity(query_emb, chunk["embedding"])
            results.append((sim, chunk))
        results.sort(key=lambda x: x[0], reverse=True)
        return [x[1] for x in results[:top_k]]
    else:
        print("[WARN] Could not generate query embedding or vector_db empty. Falling back to Keyword Search.")
        query_words = query.lower().split()
        results = []
        for chunk in vector_db:
            score = 0
            content_lower = chunk["content"].lower()
            for word in query_words:
                if word in content_lower: score += 1
            results.append((score, chunk))
        results.sort(key=lambda x: x[0], reverse=True)
        return [x[1] for x in results[:top_k]]


def get_llm_response(prompt, model, max_tokens, temperature, stream=False):
    """Generate response from LLM using configured backend API."""
    try:
        if BACKEND_TYPE == 'ollama':
            response = requests.post(
                API_BASE_URL + "/api/generate",
                json={
                    "model": model,
                    "prompt": prompt,
                    "stream": stream,
                    "max_tokens": max_tokens,
                    "temperature": temperature
                },
                timeout=240 # Increased timeout for LLM generation
            )
        else: # Assume OpenAI-compatible (GPT4All, LM Studio, etc.)
            response = requests.post(
                API_BASE_URL + "/v1/chat/completions",
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}],
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "stream": stream
                },
                timeout=240 # Increased timeout for LLM generation
            )
        
        response.raise_for_status() # Raise an exception for bad status codes

        data = response.json()

        # Handle different response formats
        if BACKEND_TYPE == 'ollama':
            return data.get("response", "Error: No content received.")
        else: # OpenAI-compatible
            return data.get("choices", [{}])[0].get("message", {}).get("content", "Error: No content received.")

    except requests.exceptions.Timeout: # Catch specific Timeout error
        print("[ERROR] API Request Timed Out after 240 seconds.")
        print("Error: The LLM model took too long to respond. This might be due to system resource limitations (RAM/CPU) or model processing time.")
        return None
    except requests.exceptions.RequestException as e:
        print("[ERROR] API Request Failed: " + str(e))
        return "Error: Could not connect to the LLM API. Ensure Ollama is running and the model is loaded."
    except Exception as e:
        print("[ERROR] Unexpected error during LLM response generation: " + str(e))
        return "Error: An unexpected issue occurred."

def main():
    # Load config
    config = load_config()
    
    # --- API Status Check ---
    print("\n======================================================================")
    print("Checking API Status...")
    print("======================================================================")
    
    api_available = False
    backend_type = CONFIG.get('backend', {}).get('type', 'ollama') # Default to ollama
    api_base_url = CONFIG.get('backend', {}).get('api_base_url', 'http://localhost:11434') # Default to ollama port

    if backend_type == 'ollama':
        try:
            # Use /api/tags for Ollama check
            response = requests.get(api_base_url + "/api/tags", timeout=5)
            if response.status_code == 200:
                print("[OK] OLLAMA API: API Server is running")
                api_available = True
            else:
                print("[!] OLLAMA API: Cannot connect to API Server (Status: " + str(response.status_code) + ")")
                print("[WARN] OLLAMA may not be running properly!")
        except requests.exceptions.RequestException as e:
            print("[!] OLLAMA API: Cannot connect to API Server")
            print("[!] Error details: " + str(e))
            print("[WARN] OLLAMA may not be running properly!")
    else: # Assume OpenAI-compatible for other backends
        try:
            # Use /v1/models to check compatibility
            response = requests.get(api_base_url + "/v1/models", timeout=5)
            if response.status_code == 200:
                print("[OK] Embedding API: API Server is running (OpenAI-compatible)")
                api_available = True
            else:
                print("[!] API: Cannot connect to API Server (Status: " + str(response.status_code) + ")")
                print("[WARN] API server may not be running properly!")
        except requests.exceptions.RequestException as e:
            print("[!] API: Cannot connect to API Server")
            print("[!] Error details: " + str(e))
            print("[WARN] API server may not be running properly!")

    if not api_available:
        print("\n[ERROR] Essential API services are not available. Exiting.")
        sys.exit(1)
    
    # --- Load Vector DB ---
    vector_db_path = config.get('paths', {}).get('vector_db', 'LearningDb_Output/vector_db.json')
    if not os.path.exists(vector_db_path):
        print("[!] Vector database not found: " + vector_db_path)
        print("[!] Please run 'python embed_local.py' first to generate embeddings.")
        sys.exit(1)
        
    try:
        with open(vector_db_path, 'r', encoding='utf-8') as f:
            vector_db = json.load(f)
        print("[*] Knowledge Base: " + str(len(vector_db)) + " PDF Chunks Loaded.")
    except Exception as e:
        print("[!] Error loading vector database: " + str(e))
        sys.exit(1)

    # --- Main Interface ---
    print("\n======================================================================")
    print("=== AI Scan PDF - Spec Analyzer ===")
    print("======================================================================")
    print("Displaying config: Backend={}, API={}, LLM={}, Embedding={}".format(BACKEND_TYPE.upper(), API_BASE_URL, LLM_MODEL, EMBEDDING_MODEL))
    print("Knowledge Base: {} PDF Chunks Loaded.".format(len(vector_db)))

    print("\n📋 Quick Help:")
    print("   - Type your question in Thai or English")
    print("   - Type 'exit' or 'quit' to stop")
    print("   - Type 'help' for more options")
    print("======================================================================")

    # Warm-up: Send initial greeting to load the model
    print("\n[*] Initializing LLM model...")
    warmup_prompt = "สวัสดี! คุณพร้อมช่วยตอบคำถามหรือยัง? ตอบสั้นๆ เป็นภาษาไทย"
    warmup_response = get_llm_response(
        warmup_prompt,
        LLM_MODEL,
        MAX_TOKENS,
        TEMPERATURE,
        stream=False
    )
    if warmup_response:
        print("[OK] LLM initialized: " + warmup_response.strip())
    else:
        print("[WARN] LLM warm-up failed, continuing anyway...")

    while True:
        query = input("\n[?] Your question: ")
        if query.lower() in ['exit', 'quit']:
            break
        elif query.lower() == 'help':
            print("\nAvailable commands:")
            print("  - type your question")
            print("  - exit/quit: stop the program")
            continue
        
        # Search for relevant chunks
        relevant_chunks = search_chunks(query, vector_db, top_k=TOP_K)
        
        # Construct prompt
        context = "\n".join([f"Chunk {i+1}:\n{chunk['content']}\n" for i, chunk in enumerate(relevant_chunks)])
        system_prompt = "You are an AI assistant analyzing technical documents. Answer the user's question based ONLY on the provided context. If the context does not contain the answer, state that you cannot find the information in the provided documents."
        
        final_prompt = "{}\n\nContext:\n{}\n\nUser Question:\n{}".format(system_prompt, context, query)

        # Get response from LLM
        print("\n[*] Analyzing with {}...".format(LLM_MODEL))
        response = get_llm_response(
            final_prompt, 
            LLM_MODEL, 
            MAX_TOKENS, 
            TEMPERATURE, 
            stream=False # Set to True for streaming if implemented
        )
        
        print("\n======================================================================")
        print("AI ANALYSIS:")
        print(response)
        print("======================================================================")

if __name__ == "__main__":
    main()
