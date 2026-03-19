import json
import os
import sys
import numpy as np
import requests

# Load configuration from config.json
def load_config():
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

CONFIG = load_config()

# Get backend configuration
BACKEND_TYPE = CONFIG.get('backend', {}).get('type', 'gpt4all')
API_BASE_URL = CONFIG.get('backend', {}).get('api_base_url', 'http://localhost:4891')
LLM_MODEL = CONFIG.get('models', {}).get('llm_model', 'qwen3-8b')
EMBED_MODEL = CONFIG.get('models', {}).get('embedding_model', 'Qwen/Qwen3-Embedding-0.6B-GGUF')

# Generation settings
MAX_TOKENS = CONFIG.get('generation', {}).get('max_tokens', 2000)
TEMPERATURE = CONFIG.get('generation', {}).get('temperature', 0.2)

# Search settings
TOP_K = CONFIG.get('search', {}).get('top_k_chunks', 3)

# Show backend info on startup
print(f"\n[ℹ] Using backend: {BACKEND_TYPE.upper()}")

def get_embedding(text):
    """Generate embedding using GPT4All API or fallback to hash"""
    try:
        response = requests.post(
            f"{API_BASE_URL}/v1/embeddings",
            json={"model": EMBED_MODEL, "input": text},
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data["data"][0]["embedding"]
    except Exception as e:
        # Fallback to hash-based embedding
        return generate_semantic_hash(text)

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
    query_emb = get_embedding(query)

    if query_emb and len(vector_db) > 0 and "embedding" in vector_db[0]:
        print("[*] Performing Deep Vector Search with Embeddings...")
        results = []
        for chunk in vector_db:
            sim = cosine_similarity(query_emb, chunk["embedding"])
            results.append((sim, chunk))
        results.sort(key=lambda x: x[0], reverse=True)
        return [x[1] for x in results[:top_k]]
    else:
        print("[!] Warning: Could not generate query embedding or vector_db empty. Falling back to Keyword Search.")
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

def query_llm(prompt):
    """Query the LLM using configured backend API"""
    try:
        # Different backends use different endpoints
        if BACKEND_TYPE == 'ollama':
            # Ollama uses /api/generate with 'prompt' instead of 'messages'
            response = requests.post(
                f"{API_BASE_URL}/api/generate",
                json={
                    "model": LLM_MODEL,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "num_predict": MAX_TOKENS,
                        "temperature": TEMPERATURE
                    }
                },
                timeout=300
            )
            response.raise_for_status()
            data = response.json()
            return data.get("response", "")
        
        else:
            # OpenAI-compatible (GPT4All, LM Studio, etc.)
            response = requests.post(
                f"{API_BASE_URL}/v1/chat/completions",
                json={
                    "model": LLM_MODEL,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream": False,
                    "max_tokens": MAX_TOKENS,
                    "temperature": TEMPERATURE
                },
                timeout=300
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
    
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 500:
            return f"[ERROR] Model is not loaded or busy. Please check {BACKEND_TYPE.upper()} app and ensure the model is loaded."
        return f"Error: HTTP {e.response.status_code}"
    except requests.exceptions.ConnectionError:
        return f"[ERROR] Cannot connect to {BACKEND_TYPE.upper()}. Make sure the server is running on {API_BASE_URL}."
    except Exception as e:
        return f"Error: {str(e)}"

def check_backend_status():
    """Check if API backend is accessible"""
    try:
        # Try to get models list
        if BACKEND_TYPE == 'ollama':
            response = requests.get(f"{API_BASE_URL}/api/tags", timeout=5)
        else:
            response = requests.get(f"{API_BASE_URL}/v1/models", timeout=5)
        
        if response.status_code == 200:
            return True, "API Server is running"
        return False, f"API returned {response.status_code}"
    except:
        return False, "Cannot connect to API Server"

def main():
    # Step 0: Check backend connection
    print(f"\n{'='*70}")
    print("🔍 Checking API Status...")
    print(f"{'='*70}")
    
    api_ok, status_msg = check_backend_status()
    if api_ok:
        print(f"[✓] {BACKEND_TYPE.upper()} API: {status_msg}")
    else:
        print(f"[!] {BACKEND_TYPE.upper()} API: {status_msg}")
        print(f"\n⚠️  WARNING: {BACKEND_TYPE.upper()} may not be running properly!")
        print(f"\n📋 Troubleshooting Steps:")
        
        if BACKEND_TYPE == 'gpt4all':
            print(f"   1. Open GPT4All application")
            print(f"   2. Go to Settings → Enable 'Local API Server'")
            print(f"   3. Make sure port is 4891")
            print(f"   4. Load the model: {LLM_MODEL}")
        elif BACKEND_TYPE == 'ollama':
            print(f"   1. Start Ollama: ollama serve")
            print(f"   2. Pull a model: ollama pull {LLM_MODEL}")
            print(f"   3. Check: ollama list")
        elif BACKEND_TYPE == 'lmstudio':
            print(f"   1. Open LM Studio")
            print(f"   2. Start Local Server")
            print(f"   3. Load a model")
        else:
            print(f"   1. Check your {BACKEND_TYPE} server is running")
            print(f"   2. Verify API URL: {API_BASE_URL}")
        
        print(f"   5. Try again\n")
    
    vector_db_path = os.path.join("LearningDb_Output", "vector_db.json")
    
    if not os.path.exists(vector_db_path):
        print(f"[!] ERROR: {vector_db_path} not found.")
        print("[!] Run these steps first:")
        print("[!]   Step 1: python parse_and_chunk.py")
        print("[!]   Step 2: python embed_local.py")
        return

    with open(vector_db_path, "r", encoding="utf-8") as f:
        vector_db = json.load(f)

    print(f"\n{'='*70}")
    print(f"=== AI Scan PDF - Spec Analyzer ===")
    print(f"{'='*70}")
    print(f"[*] Backend: {BACKEND_TYPE.upper()}")
    print(f"[*] API Server: {API_BASE_URL}")
    print(f"[*] LLM Model: {LLM_MODEL}")
    print(f"[*] Embedding: {EMBED_MODEL}")
    print(f"[*] Knowledge Base: {len(vector_db)} PDF Chunks Loaded.")
    print(f"\n📋 Quick Help:")
    print(f"   - Type your question in Thai or English")
    print(f"   - Type 'exit' or 'quit' to stop")
    print(f"   - Type 'help' for more options")
    print(f"{'='*70}\n")

    while True:
        try:
            query = input("[?] Your question: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\n[!] Exiting...")
            break
            
        if query.lower() in ['exit', 'quit', 'q']:
            print("\n[+] Goodbye!\n")
            break
        
        if query.lower() in ['help', 'h', '?']:
            print("\n" + "="*50)
            print("HELP - How to use:")
            print("="*50)
            print("1. Ask questions about your PDF documents")
            print("2. The system will search relevant chunks")
            print("3. AI will answer based on document content")
            print("\nExamples:")
            print("  - ระบบเบิกจ่ายงบประมาณทำอย่างไร")
            print("  - What is the budget approval process?")
            print("  - ขั้นตอนการตรวจสอบใบสำคัญ")
            print("\nCommands:")
            print("  - exit, quit, q : Exit the program")
            print("  - help, h      : Show this help")
            print("  - info, i      : Show system information")
            print("="*50 + "\n")
            continue
        
        if query.lower() in ['info', 'i']:
            print("\n" + "="*50)
            print("SYSTEM INFORMATION")
            print("="*50)
            print(f"LLM Model: {LLM_MODEL}")
            print(f"Embedding: {EMBED_MODEL}")
            print(f"API Server: {API_BASE_URL}")
            print(f"Chunks: {len(vector_db)}")
            print(f"Status: Ready")
            print("="*50 + "\n")
            continue

        print("[*] Searching documents...", end=" ", flush=True)
        relevant_chunks = search_chunks(query, vector_db, top_k=TOP_K)
        
        if not relevant_chunks:
            print("[!] No relevant documents found.\n")
            continue
        
        print(f"Found {len(relevant_chunks)} relevant chunk(s)")

        context = "\n---\n".join([c["content"] for c in relevant_chunks])
        full_prompt = f"""You are an AI assistant analyzing Thai PDF documents.
Using ONLY the context below, answer the question. 
- Respond in Thai if the question is in Thai
- Respond in English if the question is in English
- Be concise and accurate
- If the answer is not in the context, say "ไม่พบข้อมูลในเอกสาร" (Information not found in documents)

CONTEXT:
{context}

QUESTION: {query}

ANSWER:"""

        print(f"[*] Analyzing with {LLM_MODEL}...")
        answer = query_llm(full_prompt)

        print(f"\n{'='*70}")
        print(f"📄 AI ANALYSIS:")
        print(f"{'='*70}")
        print(answer)
        print(f"{'='*70}\n")

if __name__ == "__main__":
    main()
