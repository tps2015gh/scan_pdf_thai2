"""
Configuration Manager - AI Scan PDF

Easy model and settings changer without modifying code.

Usage:
    python config_manager.py              # Interactive mode
    python config_manager.py --show       # Show current config
    python config_manager.py --model qwen2.5-7b-instruct  # Change LLM model
    python config_manager.py --list       # List available models
"""

import json
import os
import sys
import requests

CONFIG_FILE = "config.json"

class ConfigManager:
    def __init__(self):
        self.config = self.load_config()
        self.api_base = self.config.get("gpt4all", {}).get("api_base_url", "http://localhost:4891")
    
    def load_config(self):
        """Load configuration from file"""
        if not os.path.exists(CONFIG_FILE):
            print(f"[!] Config file not found: {CONFIG_FILE}")
            print("[!] Creating default config...")
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
            "gpt4all": {
                "api_base_url": "http://localhost:4891",
                "api_timeout": 30
            },
            "models": {
                "llm_model": "qwen3-8b",
                "llm_model_full": "unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF",
                "embedding_model": "Qwen/Qwen3-Embedding-0.6B-GGUF"
            },
            "generation": {
                "max_tokens": 2000,
                "temperature": 0.2,
                "stream": False
            },
            "search": {
                "top_k_chunks": 3
            }
        }
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(default_config, f, ensure_ascii=False, indent=2)
        
        return default_config
    
    def show_config(self):
        """Display current configuration"""
        print("\n" + "="*60)
        print("📋 Current Configuration")
        print("="*60)
        
        print(f"\n🌐 GPT4All API:")
        print(f"   URL: {self.config.get('gpt4all', {}).get('api_base_url', 'N/A')}")
        
        print(f"\n🤖 Models:")
        models = self.config.get('models', {})
        print(f"   LLM: {models.get('llm_model', 'N/A')}")
        print(f"   Embedding: {models.get('embedding_model', 'N/A')}")
        
        print(f"\n⚙️  Generation:")
        gen = self.config.get('generation', {})
        print(f"   Max Tokens: {gen.get('max_tokens', 'N/A')}")
        print(f"   Temperature: {gen.get('temperature', 'N/A')}")
        
        print(f"\n🔍 Search:")
        search = self.config.get('search', {})
        print(f"   Top K Chunks: {search.get('top_k_chunks', 'N/A')}")
        
        print("\n" + "="*60 + "\n")
    
    def list_models(self):
        """List available models from GPT4All"""
        print("\n" + "="*60)
        print("📦 Available Models in GPT4All")
        print("="*60)
        
        try:
            response = requests.get(f"{self.api_base}/v1/models", timeout=5)
            if response.status_code == 200:
                models = response.json().get('data', [])
                print(f"\nFound {len(models)} models:\n")
                for model in models:
                    model_id = model.get('id', 'Unknown')
                    print(f"  • {model_id}")
                
                print("\n" + "="*60)
                print("\nTo change LLM model:")
                print(f"  python config_manager.py --model <model_name>")
                print("\nExample:")
                print(f"  python config_manager.py --model qwen2.5-7b-instruct")
                print("="*60 + "\n")
            else:
                print(f"[!] Cannot connect to GPT4All API (Status {response.status_code})")
                print("[!] Make sure GPT4All is running with API Server enabled")
        except Exception as e:
            print(f"[!] Error: {e}")
            print("[!] Make sure GPT4All is running")
    
    def set_llm_model(self, model_name):
        """Change LLM model"""
        self.config['models']['llm_model'] = model_name
        if self.save_config():
            print(f"[+] LLM model changed to: {model_name}")
            print(f"[!] Remember to load this model in GPT4All app")
            return True
        return False
    
    def set_embedding_model(self, model_name):
        """Change embedding model"""
        self.config['models']['embedding_model'] = model_name
        if self.save_config():
            print(f"[+] Embedding model changed to: {model_name}")
            return True
        return False
    
    def set_generation_params(self, max_tokens=None, temperature=None):
        """Change generation parameters"""
        if 'generation' not in self.config:
            self.config['generation'] = {}
        
        if max_tokens is not None:
            self.config['generation']['max_tokens'] = max_tokens
            print(f"[+] Max tokens set to: {max_tokens}")
        
        if temperature is not None:
            self.config['generation']['temperature'] = temperature
            print(f"[+] Temperature set to: {temperature}")
        
        self.save_config()
    
    def interactive_mode(self):
        """Interactive configuration mode"""
        print("\n" + "="*60)
        print("⚙️  Configuration Manager - Interactive Mode")
        print("="*60)
        
        while True:
            print("\nSelect an option:")
            print("  1. Show current configuration")
            print("  2. Change LLM model")
            print("  3. Change embedding model")
            print("  4. List available models")
            print("  5. Change generation settings")
            print("  6. Exit")
            
            choice = input("\nYour choice (1-6): ").strip()
            
            if choice == '1':
                self.show_config()
            
            elif choice == '2':
                model = input("Enter LLM model name: ").strip()
                if model:
                    self.set_llm_model(model)
            
            elif choice == '3':
                model = input("Enter embedding model name: ").strip()
                if model:
                    self.set_embedding_model(model)
            
            elif choice == '4':
                self.list_models()
            
            elif choice == '5':
                try:
                    max_tokens = input("Max tokens (current: {}): ".format(
                        self.config.get('generation', {}).get('max_tokens', 2000)
                    )).strip()
                    if max_tokens:
                        self.set_generation_params(max_tokens=int(max_tokens))
                    
                    temp = input("Temperature (current: {}): ".format(
                        self.config.get('generation', {}).get('temperature', 0.2)
                    )).strip()
                    if temp:
                        self.set_generation_params(temperature=float(temp))
                except ValueError:
                    print("[!] Invalid number")
            
            elif choice == '6':
                print("\n[+] Exiting configuration manager\n")
                break
            
            else:
                print("[!] Invalid choice")


def main():
    import argparse
    
    parser = argparse.ArgumentParser(description='AI Scan PDF Configuration Manager')
    parser.add_argument('--show', action='store_true', help='Show current configuration')
    parser.add_argument('--model', type=str, help='Set LLM model')
    parser.add_argument('--embedding', type=str, help='Set embedding model')
    parser.add_argument('--list', action='store_true', help='List available models')
    parser.add_argument('--temp', type=float, help='Set temperature')
    parser.add_argument('--max-tokens', type=int, help='Set max tokens')
    
    args = parser.parse_args()
    
    manager = ConfigManager()
    
    if args.show:
        manager.show_config()
    
    elif args.model:
        manager.set_llm_model(args.model)
    
    elif args.embedding:
        manager.set_embedding_model(args.embedding)
    
    elif args.list:
        manager.list_models()
    
    elif args.temp or args.max_tokens:
        manager.set_generation_params(
            max_tokens=args.max_tokens,
            temperature=args.temp
        )
    
    else:
        manager.interactive_mode()


if __name__ == "__main__":
    main()
