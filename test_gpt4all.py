"""
Test GPT4All API Connection

This script tests if GPT4All API server is running and models are loaded.
"""

import requests
import json

API_BASE = "http://localhost:4891"

def test_connection():
    """Test if GPT4All API is accessible"""
    try:
        response = requests.get(API_BASE, timeout=5)
        print(f"✅ GPT4All API is running at {API_BASE}")
        return True
    except Exception as e:
        print(f"❌ Cannot connect to GPT4All at {API_BASE}")
        print(f"   Error: {e}")
        print("\n📋 Steps to fix:")
        print("   1. Open GPT4All application")
        print("   2. Go to Settings → Enable 'Local API Server'")
        print("   3. Make sure port is 4891")
        return False

def list_models():
    """List available models"""
    try:
        # Try v1 API first (OpenAI-compatible)
        response = requests.get(f"{API_BASE}/v1/models", timeout=5)
        if response.status_code == 200:
            data = response.json()
            models = [m['id'] for m in data.get('data', [])]
            print(f"\n📦 Available Models ({len(models)} found):")
            for model in models:
                print(f"   • {model}")
            return models
        else:
            # Fallback to old endpoint
            response = requests.get(f"{API_BASE}/api/models", timeout=5)
            if response.status_code == 200:
                models = response.json()
                print(f"\n📦 Available Models ({len(models)} found):")
                for model in models:
                    print(f"   • {model}")
                return models
            else:
                print("⚠️  No models endpoint or empty response")
                return []
    except Exception as e:
        print(f"⚠️  Could not retrieve models: {e}")
        return []

def test_embedding():
    """Test embedding generation"""
    # Try multiple endpoint patterns
    endpoints = [
        ("/v1/embeddings", "input"),
        ("/api/embedding", "prompt"),
        ("/v1/embeddings", "input"),
    ]
    
    for endpoint, input_key in endpoints:
        try:
            response = requests.post(
                f"{API_BASE}{endpoint}",
                json={"model": "Qwen/Qwen3-Embedding-0.6B-GGUF", input_key: "test"},
                timeout=10
            )
            if response.status_code == 200:
                data = response.json()
                # Handle different response formats
                embedding = data.get("embedding") or data.get("data", [{}])[0].get("embedding", [])
                if embedding:
                    print(f"\n✅ Embedding model working!")
                    print(f"   Endpoint: {endpoint}")
                    print(f"   Vector size: {len(embedding)} dimensions")
                    return True
        except Exception as e:
            pass
    
    print(f"\n❌ Embedding test failed: All endpoints returned errors")
    print("   Make sure 'Qwen/Qwen3-Embedding-0.6B-GGUF' model is loaded in GPT4All")
    print("   Note: In GPT4All app, click on the model to load it (not just downloaded)")
    return False

def test_llm(model_name="qwen3-8b"):
    """Test LLM generation"""
    # Try multiple endpoint patterns
    endpoints = [
        ("/v1/chat/completions", {"messages": [{"role": "user", "content": "สวัสดี"}]}),
        ("/api/generate", {"prompt": "สวัสดี"}),
        ("/api/chat", {"messages": [{"role": "user", "content": "สวัสดี"}]}),
    ]
    
    for endpoint, body_template in endpoints:
        try:
            body = {"model": model_name, **body_template, "stream": False}
            response = requests.post(
                f"{API_BASE}{endpoint}",
                json=body,
                timeout=30
            )
            if response.status_code == 200:
                result = response.json()
                print(f"\n✅ LLM '{model_name}' is working!")
                print(f"   Endpoint: {endpoint}")
                # Handle different response formats
                response_text = result.get("response") or result.get("choices", [{}])[0].get("message", {}).get("content", "")
                if response_text:
                    print(f"   Test response: {response_text[:50]}...")
                return True
        except Exception as e:
            pass
    
    print(f"\n❌ LLM test failed: All endpoints returned errors")
    print(f"   Make sure '{model_name}' is loaded in GPT4All")
    return False

def main():
    print("\n" + "="*60)
    print("🔍 GPT4All Connection Test")
    print("="*60 + "\n")
    
    # Test 1: Connection
    if not test_connection():
        return
    
    # Test 2: List models
    models = list_models()
    
    # Test 3: Embedding
    test_embedding()
    
    # Test 4: LLM (try common model names)
    llm_models = [
        "qwen3-8b",
        "unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF",
        "deepseek-r1:8b",
        "deepseek-r1-distill-qwen-14b"
    ]
    
    for model in llm_models:
        if any(model.lower() in m.lower() for m in models) or len(models) == 0:
            print(f"\n🧪 Testing LLM: {model}...")
            if test_llm(model):
                break
    
    print("\n" + "="*60)
    print("📋 Next Steps:")
    print("="*60)
    print("1. In GPT4All app, make sure these models are loaded:")
    print("   • Qwen/Qwen3-Embedding-0.6B-GGUF (for embeddings)")
    print("   • qwen3-8b (unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF)")
    print("\n2. Run: python embed_local.py")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
