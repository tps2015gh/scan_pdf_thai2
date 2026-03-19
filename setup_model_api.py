"""
Setup Model & API - AI Scan PDF

Configure which API backend to use: GPT4All, Ollama, LM Studio, or any OpenAI-compatible API.

Usage:
    python setup_model_api.py                    # Interactive setup
    python setup_model_api.py --backend gpt4all  # Set backend directly
    python setup_model_api.py --list             # List available backends
    python setup_model_api.py --test             # Test connection
"""

import json
import os
import sys
import requests

CONFIG_FILE = "config.json"

# Pre-configured backend presets
BACKENDS = {
    "gpt4all": {
        "name": "GPT4All",
        "api_base_url": "http://localhost:4891",
        "api_type": "openai-compatible",
        "endpoint": "/v1/chat/completions",
        "embedding_endpoint": "/v1/embeddings",
        "models_endpoint": "/v1/models",
        "default_llm": "qwen3-8b",
        "default_embedding": "Qwen/Qwen3-Embedding-0.6B-GGUF",
        "description": "GPT4All Desktop App (Local)"
    },
    "ollama": {
        "name": "Ollama",
        "api_base_url": "http://localhost:11434",
        "api_type": "ollama",
        "endpoint": "/api/generate",
        "embedding_endpoint": "/api/embeddings",
        "models_endpoint": "/api/tags",
        "default_llm": "qwen2.5:7b",
        "default_embedding": "nomic-embed-text",
        "description": "Ollama Local (ollama.ai)"
    },
    "lmstudio": {
        "name": "LM Studio",
        "api_base_url": "http://localhost:1234",
        "api_type": "openai-compatible",
        "endpoint": "/v1/chat/completions",
        "embedding_endpoint": "/v1/embeddings",
        "models_endpoint": "/v1/models",
        "default_llm": "local-model",
        "default_embedding": "local-model",
        "description": "LM Studio (Local)"
    },
    "openai": {
        "name": "OpenAI API",
        "api_base_url": "https://api.openai.com/v1",
        "api_type": "openai",
        "endpoint": "/chat/completions",
        "embedding_endpoint": "/embeddings",
        "models_endpoint": "/models",
        "default_llm": "gpt-3.5-turbo",
        "default_embedding": "text-embedding-ada-002",
        "requires_api_key": True,
        "description": "OpenAI Cloud API (Paid)"
    },
    "custom": {
        "name": "Custom API",
        "api_base_url": "http://localhost:8080",
        "api_type": "openai-compatible",
        "endpoint": "/v1/chat/completions",
        "embedding_endpoint": "/v1/embeddings",
        "models_endpoint": "/v1/models",
        "default_llm": "model-name",
        "default_embedding": "model-name",
        "description": "Custom OpenAI-compatible API"
    }
}


class APISetup:
    def __init__(self):
        self.config = self.load_config()
    
    def load_config(self):
        """Load configuration from file"""
        if not os.path.exists(CONFIG_FILE):
            return self.create_default_config()
        
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"[!] Error loading config: {e}")
            return self.create_default_config()
    
    def save_config(self):
        """Save configuration to file"""
        try:
            with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, ensure_ascii=False, indent=2)
            print(f"[+] Configuration saved to {CONFIG_FILE}")
            return True
        except Exception as e:
            print(f"[!] Error saving config: {e}")
            return False
    
    def create_default_config(self):
        """Create default configuration"""
        default_config = {
            "_comment": "AI Scan PDF - Configuration File",
            "_description": "Edit this file to change models and settings without modifying code",
            
            "backend": {
                "_comment": "API Backend Configuration",
                "type": "gpt4all",
                "api_base_url": "http://localhost:4891",
                "api_key": None
            },
            
            "gpt4all": {
                "_comment": "GPT4All API Server Settings",
                "api_base_url": "http://localhost:4891",
                "api_timeout": 30
            },
            
            "models": {
                "_comment": "Model Configuration - Change these to use different models",
                "_note": "Model names must match what's loaded in your API backend",
                
                "llm_model": "qwen3-8b",
                "llm_model_full": "unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF",
                "llm_description": "Main LLM for Thai/English chat",
                
                "embedding_model": "Qwen/Qwen3-Embedding-0.6B-GGUF",
                "embedding_description": "Embedding model for vector search"
            },
            
            "generation": {
                "_comment": "LLM Generation Settings",
                "max_tokens": 2000,
                "temperature": 0.2,
                "top_p": 0.9,
                "stream": False
            },
            
            "embedding": {
                "_comment": "Embedding Settings",
                "dimensions": 384,
                "use_fallback": True,
                "fallback_method": "semantic_hash"
            },
            
            "search": {
                "_comment": "Vector Search Settings",
                "top_k_chunks": 3,
                "min_similarity": 0.1,
                "use_keyword_fallback": True
            },
            
            "paths": {
                "_comment": "File Path Configuration",
                "pdf_input": "PDF_Input",
                "temp_output": "Temp_Output",
                "learning_db_output": "LearningDb_Output",
                "chunks": "Temp_Output/chunks",
                "vector_db": "LearningDb_Output/vector_db.json"
            },
            
            "parsing": {
                "_comment": "PDF Parsing Settings",
                "chunk_size": 4000,
                "chunk_overlap": 500,
                "normalize_thai": True
            },
            
            "ui": {
                "_comment": "User Interface Settings",
                "show_welcome": True,
                "show_help_on_start": True,
                "color_output": True,
                "language": "th"
            }
        }
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        return default_config
    
    def set_backend(self, backend_name):
        """Set API backend"""
        if backend_name not in BACKENDS:
            print(f"[!] Unknown backend: {backend_name}")
            print(f"    Available: {', '.join(BACKENDS.keys())}")
            return False
        
        backend = BACKENDS[backend_name]
        
        # Update config
        if 'backend' not in self.config:
            self.config['backend'] = {}
        
        self.config['backend']['type'] = backend_name
        self.config['backend']['api_base_url'] = backend['api_base_url']
        
        # Update models
        if 'models' not in self.config:
            self.config['models'] = {}
        
        self.config['models']['llm_model'] = backend['default_llm']
        self.config['models']['embedding_model'] = backend['default_embedding']
        
        # Update gpt4all section for backwards compatibility
        if backend_name == 'gpt4all':
            if 'gpt4all' not in self.config:
                self.config['gpt4all'] = {}
            self.config['gpt4all']['api_base_url'] = backend['api_base_url']
        
        if self.save_config():
            print(f"[+] Backend set to: {backend['name']}")
            print(f"[+] API URL: {backend['api_base_url']}")
            print(f"[+] Default LLM: {backend['default_llm']}")
            print(f"[+] Default Embedding: {backend['default_embedding']}")
            
            if backend.get('requires_api_key'):
                print(f"[!] API Key required - edit config.json to add your key")
            
            return True
        return False
    
    def list_backends(self):
        """List available backends"""
        print("\n" + "="*70)
        print("🔌 Available API Backends")
        print("="*70)
        
        for key, backend in BACKENDS.items():
            print(f"\n{backend['name']} ({key})")
            print(f"  {backend['description']}")
            print(f"  URL: {backend['api_base_url']}")
            print(f"  Default LLM: {backend['default_llm']}")
            print(f"  Default Embedding: {backend['default_embedding']}")
            if backend.get('requires_api_key'):
                print(f"  🔑 Requires API Key")
        
        print("\n" + "="*70)
        print("\nTo change backend:")
        print(f"  python setup_model_api.py --backend <name>")
        print("\nExamples:")
        print(f"  python setup_model_api.py --backend gpt4all")
        print(f"  python setup_model_api.py --backend ollama")
        print(f"  python setup_model_api.py --backend lmstudio")
        print("="*70 + "\n")
    
    def test_connection(self):
        """Test API connection"""
        if 'backend' not in self.config:
            print("[!] No backend configured")
            return False
        
        backend_type = self.config['backend'].get('type', 'gpt4all')
        api_base = self.config['backend'].get('api_base_url', 'http://localhost:4891')
        
        print("\n" + "="*70)
        print(f"🧪 Testing Connection: {backend_type.upper()}")
        print("="*70)
        print(f"API URL: {api_base}\n")
        
        # Test models endpoint
        backend = BACKENDS.get(backend_type, BACKENDS['gpt4all'])
        models_endpoint = backend['models_endpoint']
        
        try:
            print(f"[*] Testing models endpoint: {models_endpoint}")
            response = requests.get(f"{api_base}{models_endpoint}", timeout=5)
            
            if response.status_code == 200:
                print(f"[✓] Connection successful!")
                
                # Try to parse models
                try:
                    if backend_type == 'ollama':
                        data = response.json()
                        models = data.get('models', [])
                    else:
                        data = response.json()
                        models = data.get('data', [])
                    
                    print(f"[✓] Found {len(models)} models")
                    
                    if len(models) > 0:
                        print("\nAvailable models:")
                        for model in models[:5]:  # Show first 5
                            if isinstance(model, dict):
                                print(f"  • {model.get('name', model.get('id', 'Unknown'))}")
                            else:
                                print(f"  • {model}")
                        if len(models) > 5:
                            print(f"  ... and {len(models) - 5} more")
                except:
                    print("[!] Could not parse models list")
                
                # Test chat endpoint
                chat_endpoint = backend['endpoint']
                print(f"\n[*] Testing chat endpoint: {chat_endpoint}")
                
                if backend_type == 'ollama':
                    test_response = requests.post(
                        f"{api_base}{chat_endpoint}",
                        json={
                            "model": backend['default_llm'],
                            "prompt": "Hi",
                            "stream": False
                        },
                        timeout=10
                    )
                else:
                    test_response = requests.post(
                        f"{api_base}{chat_endpoint}",
                        json={
                            "model": backend['default_llm'],
                            "messages": [{"role": "user", "content": "Hi"}],
                            "stream": False,
                            "max_tokens": 10
                        },
                        timeout=10
                    )
                
                if test_response.status_code == 200:
                    print(f"[✓] Chat endpoint working!")
                elif test_response.status_code == 500:
                    print(f"[!] Model not loaded (500 error)")
                else:
                    print(f"[!] Chat endpoint error: {test_response.status_code}")
                
                print("\n" + "="*70)
                print("✅ Backend is working!")
                print("="*70 + "\n")
                return True
            else:
                print(f"[!] Connection failed: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("[!] Cannot connect - API server may not be running")
        except Exception as e:
            print(f"[!] Error: {e}")
        
        print("\n" + "="*70)
        print("❌ Backend is NOT working")
        print("="*70)
        print("\nTroubleshooting:")
        if backend_type == 'gpt4all':
            print("1. Open GPT4All application")
            print("2. Settings → Enable 'Local API Server'")
            print("3. Make sure port is 4891")
            print("4. Load a model in GPT4All")
        elif backend_type == 'ollama':
            print("1. Start Ollama: ollama serve")
            print("2. Pull a model: ollama pull qwen2.5:7b")
            print("3. Check: ollama list")
        elif backend_type == 'lmstudio':
            print("1. Open LM Studio")
            print("2. Start Local Server")
            print("3. Load a model")
            print("4. Check port is 1234")
        
        print("\n")
        return False
    
    def interactive_setup(self):
        """Interactive setup wizard"""
        print("\n" + "="*70)
        print("⚙️  API Backend Setup Wizard")
        print("="*70)
        
        print("\nSelect your API backend:")
        for i, (key, backend) in enumerate(BACKENDS.items(), 1):
            print(f"  {i}. {backend['name']} - {backend['description']}")
        
        try:
            choice = input("\nYour choice (1-5): ").strip()
            choice_num = int(choice)
            
            if 1 <= choice_num <= len(BACKENDS):
                backend_keys = list(BACKENDS.keys())
                backend_name = backend_keys[choice_num - 1]
                self.set_backend(backend_name)
                
                print("\n[+] Setup complete!")
                print("\nNext steps:")
                print("1. Make sure your API server is running")
                print("2. Load the required models")
                print("3. Test connection: python setup_model_api.py --test")
                print("4. Run main program: python main.py")
            else:
                print("[!] Invalid choice")
        except ValueError:
            print("[!] Invalid input")
        except KeyboardInterrupt:
            print("\n\n[!] Setup cancelled")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Scan PDF - API Backend Setup')
    parser.add_argument('--backend', type=str, help='Set backend (gpt4all, ollama, lmstudio, openai, custom)')
    parser.add_argument('--list', action='store_true', help='List available backends')
    parser.add_argument('--test', action='store_true', help='Test API connection')
    parser.add_argument('--url', type=str, help='Custom API URL (for custom backend)')
    
    args = parser.parse_args()
    
    setup = APISetup()
    
    if args.list:
        setup.list_backends()
    
    elif args.backend:
        setup.set_backend(args.backend)
        
        # If custom URL provided
        if args.url and args.backend == 'custom':
            setup.config['backend']['api_base_url'] = args.url
            setup.save_config()
    
    elif args.test:
        setup.test_connection()
    
    else:
        setup.interactive_setup()


if __name__ == "__main__":
    main()
