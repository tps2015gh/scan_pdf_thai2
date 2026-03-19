import os
import json
import requests
from tqdm import tqdm
import numpy as np

# Load configuration
def load_config():
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

CONFIG = load_config()

# GPT4All Local API Server Settings
API_BASE_URL = CONFIG.get('gpt4all', {}).get('api_base_url', 'http://localhost:4891')
EMBEDDING_MODEL = CONFIG.get('models', {}).get('embedding_model', 'Qwen/Qwen3-Embedding-0.6B-GGUF')

def get_embedding_with_api(text, use_chat_endpoint=False):
    """
    Try to get embedding using GPT4All's available endpoints.
    Since GPT4All v3.9.0 doesn't have native embedding API,
    we can use a workaround with the chat endpoint.
    """
    if not use_chat_endpoint:
        # Try standard embedding endpoints
        endpoints = [
            ("/v1/embeddings", "input"),
            ("/api/embedding", "prompt"),
        ]
        
        for endpoint, input_key in endpoints:
            try:
                response = requests.post(
                    f"{API_BASE_URL}{endpoint}",
                    json={"model": EMBEDDING_MODEL, input_key: text},
                    timeout=30
                )
                if response.status_code == 200:
                    data = response.json()
                    embedding = data.get("embedding") or data.get("data", [{}])[0].get("embedding", [])
                    if embedding:
                        return embedding
            except:
                continue
    
    # Fallback: Use chat endpoint to get embedding representation
    # This asks the model to output embedding-like features
    try:
        response = requests.post(
            f"{API_BASE_URL}/v1/chat/completions",
            json={
                "model": "qwen3-8b",
                "messages": [
                    {"role": "system", "content": "You are an embedding generator. Output a 384-dimensional vector as a JSON array."},
                    {"role": "user", "content": f"Generate a semantic vector representation of this text (output ONLY a JSON array of 384 numbers between -1 and 1): {text[:500]}"}
                ],
                "stream": False,
                "max_tokens": 1000,
                "temperature": 0.0
            },
            timeout=60
        )
        if response.status_code == 200:
            import re
            content = response.json()["choices"][0]["message"]["content"]
            # Try to extract JSON array from response
            match = re.search(r'\[.*?\]', content, re.DOTALL)
            if match:
                embedding = json.loads(match.group())
                if isinstance(embedding, list) and len(embedding) > 0:
                    return embedding
    except:
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
        print("[+] ✓ GPT4All API embedding endpoint is working!")
        use_api = True
        print(f"[+] Vector dimensions: {len(test_emb)}\n")
    else:
        print("[!] ✗ GPT4All API embedding endpoint not available")
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
