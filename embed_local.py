import os
import json
import requests
from tqdm import tqdm
import numpy as np

# Set UTF-8 encoding for Windows console
import sys
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

# Load configuration
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
EMBEDDING_MODEL = CONFIG.get('models', {}).get('embedding_model', 'Qwen/Qwen3-Embedding-0.6B-GGUF')

print(f"\n[ℹ] Using backend: {BACKEND_TYPE.upper()}")

def get_embedding_with_api(text):
    """
    Get embedding using configured backend API.
    Supports GPT4All, Ollama, LM Studio, and other OpenAI-compatible APIs.
    """
    try:
        # Different backends use different endpoints
        if BACKEND_TYPE == 'ollama':
            # Ollama uses /api/embeddings with 'prompt'
            response = requests.post(
                f"{API_BASE_URL}/api/embeddings",
                json={"model": EMBEDDING_MODEL, "prompt": text},
                timeout=30
            )
        else:
            # OpenAI-compatible (GPT4All, LM Studio, etc.) use /v1/embeddings with 'input'
            response = requests.post(
                f"{API_BASE_URL}/v1/embeddings",
                json={"model": EMBEDDING_MODEL, "input": text},
                timeout=30
            )
        
        if response.status_code == 200:
            data = response.json()
            # Handle different response formats
            embedding = data.get("embedding") or data.get("data", [{}])[0].get("embedding", [])
            if embedding:
                return embedding
    
    except Exception as e:
        pass
    
    return None

def generate_semantic_hash(text, dimensions=384):
    """
    Generate a deterministic semantic-like hash for text.
    This is a FALLBACK when no embedding model is available.
    Uses text features to create a pseudo-embedding.
    """
    # Normalize text
    text = text.lower().strip()
    
    # Create feature vector from text
    features = []
    
    # 1. Character-level features (first 100 chars)
    for i in range(min(100, len(text))):
        features.append(ord(text[i]) / 256.0)
    
    # 2. Word count features
    words = text.split()
    features.append(len(words) / 100.0)  # Normalized word count
    
    # 3. Average word length
    if words:
        avg_len = sum(len(w) for w in words) / len(words)
        features.append(avg_len / 20.0)
    else:
        features.append(0.0)
    
    # 4. Thai/English detection
    thai_chars = sum(1 for c in text if '\u0E00' <= c <= '\u0E7F')
    features.append(thai_chars / max(len(text), 1))
    
    # 5. Hash-based features for semantic similarity
    import hashlib
    for i in range(0, dimensions - len(features)):
        hash_input = f"{text}:{i}".encode('utf-8')
        hash_val = int(hashlib.md5(hash_input).hexdigest()[:8], 16)
        features.append((hash_val % 1000) / 1000.0)
    
    # Trim or pad to exact dimensions
    features = features[:dimensions]
    while len(features) < dimensions:
        features.append(0.0)
    
    # Convert to range [-1, 1] for cosine similarity
    features = [(f * 2 - 1) for f in features]
    
    return features

def main():
    # Input: Chunks from Temp_Output
    chunks_dir = os.path.join("Temp_Output", "chunks")
    if not os.path.exists(chunks_dir):
        print(f"[!] Chunks directory not found: {chunks_dir}")
        print("[!] Tip: Run parse_and_chunk.py first to create chunks.")
        return

    # Output: Vector DB in LearningDb_Output
    output_dir = "LearningDb_Output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "vector_db.json")

    # Collect all chunks
    all_chunks = []
    for root, dirs, files in os.walk(chunks_dir):
        for file in files:
            if file.endswith(".md"):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                    all_chunks.append({"path": file_path, "content": content})

    print(f"="*60)
    print(f"🔮 GPT4All Embedding Generator")
    print(f"="*60)
    print(f"[*] Model: {EMBEDDING_MODEL}")
    print(f"[*] API Server: {API_BASE_URL}")
    print(f"[*] Processing {len(all_chunks)} chunks...\n")
    
    # Test API connection first
    print("[*] Testing embedding API endpoint...")
    test_emb = get_embedding_with_api("ทดสอบ")

    if test_emb and len(test_emb) > 10:
        print("[OK] GPT4All API embedding endpoint is working!")
        use_api = True
        print(f"[OK] Vector dimensions: {len(test_emb)}\n")
    else:
        print("[!] GPT4All API embedding endpoint not available")
        print("[!] Using semantic hash fallback (deterministic pseudo-embeddings)")
        print("[!]")
        print("[!] NOTE: For REAL embeddings, install gpt4all Python library:")
        print("[!]   pip install gpt4all")
        print("[!]")
        print("[!] The fallback allows the system to work for testing,")
        print("[!] but semantic search quality will be limited.")
        print()
        use_api = False

    print(f"[*] Generating Embeddings ({len(all_chunks)} chunks)...\n")

    embedded_data = []
    for chunk in tqdm(all_chunks, desc="Vectorizing PDF Chunks"):
        if use_api:
            emb = get_embedding_with_api(chunk["content"])
        else:
            emb = generate_semantic_hash(chunk["content"])
        
        if emb:
            chunk["embedding"] = emb
            embedded_data.append(chunk)

    if not embedded_data:
        print(f"[!] Failed to generate embeddings")
    else:
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(embedded_data, f, ensure_ascii=False, indent=2)
        print(f"\n{'='*60}")
        print(f"[+] Successfully saved {len(embedded_data)} embedded chunks")
        print(f"[+] Output: {output_file}")
        print(f"[+] Done! You can now run: python main.py")
        print(f"{'='*60}")

if __name__ == "__main__":
    main()
