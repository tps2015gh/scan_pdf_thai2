# ⚙️ Configuration Manager Guide

## Quick Start

### View Current Configuration
```bash
python config_manager.py --show
```

### Change LLM Model
```bash
# Change to a different model
python config_manager.py --model qwen2.5-7b-instruct

# Or use interactive mode
python config_manager.py
# Select option 2
```

### List Available Models
```bash
python config_manager.py --list
```

---

## Configuration File: `config.json`

### Key Settings You Can Change

#### 1. LLM Model
```json
"models": {
  "llm_model": "qwen3-8b"
}
```

**Available Options:**
- `qwen3-8b` (your current: unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF)
- `qwen2.5-7b-instruct`
- `bartowski/DeepSeek-R1-Distill-Qwen-14B-GGUF`
- `Llama-3.2-1B-Instruct-Q4_0.gguf`

**How to Change:**
```bash
python config_manager.py --model qwen2.5-7b-instruct
```

#### 2. Embedding Model
```json
"models": {
  "embedding_model": "Qwen/Qwen3-Embedding-0.6B-GGUF"
}
```

**Available Options:**
- `Qwen/Qwen3-Embedding-0.6B-GGUF` (current)
- `all-MiniLM-L6-v2`
- `paraphrase-multilingual-MiniLM-L12-v2`

**How to Change:**
```bash
python config_manager.py --embedding all-MiniLM-L6-v2
```

#### 3. Generation Settings
```json
"generation": {
  "max_tokens": 2000,
  "temperature": 0.2
}
```

**Parameters:**
- `max_tokens`: Maximum response length (default: 2000)
- `temperature`: Creativity vs accuracy (0.0 = factual, 1.0 = creative)

**How to Change:**
```bash
python config_manager.py --max-tokens 3000 --temp 0.3
```

#### 4. Search Settings
```json
"search": {
  "top_k_chunks": 3
}
```

**What it does:** Number of chunks to retrieve for each query

**How to Change:**
Edit `config.json` directly, or use interactive mode

---

## Interactive Mode

```bash
python config_manager.py
```

### Menu Options:

1. **Show current configuration** - View all settings
2. **Change LLM model** - Select a different LLM
3. **Change embedding model** - Select different embedding
4. **List available models** - See what GPT4All has loaded
5. **Change generation settings** - Adjust temperature, max tokens
6. **Exit** - Save and exit

### Example Session:
```
Select an option:
  1. Show current configuration
  2. Change LLM model
  3. Change embedding model
  4. List available models
  5. Change generation settings
  6. Exit

Your choice (1-6): 2
Enter LLM model name: qwen2.5-7b-instruct
[+] LLM model changed to: qwen2.5-7b-instruct
```

---

## Common Configurations

### Fast Response (Lower Quality)
```bash
python config_manager.py --max-tokens 1000 --temp 0.1
```

Edit `config.json`:
```json
{
  "generation": {
    "max_tokens": 1000,
    "temperature": 0.1
  },
  "search": {
    "top_k_chunks": 2
  }
}
```

### High Quality (Slower)
```bash
python config_manager.py --max-tokens 4000 --temp 0.2
```

Edit `config.json`:
```json
{
  "generation": {
    "max_tokens": 4000,
    "temperature": 0.2
  },
  "search": {
    "top_k_chunks": 5
  }
}
```

### Better Thai Support
Use Qwen models:
```bash
python config_manager.py --model qwen2.5-7b-instruct
```

### Better English Support
Use Llama models:
```bash
python config_manager.py --model Llama-3.2-1B-Instruct-Q4_0.gguf
```

---

## Troubleshooting

### Config File Not Found
```
[!] Config file not found: config.json
[!] Creating default config...
```

**Solution:** The file will be auto-created. Or restore from git:
```bash
git checkout config.json
```

### Model Not Working After Change
```
[ERROR] Model is not loaded or busy
```

**Solution:**
1. Check model name matches GPT4All exactly
2. Load the model in GPT4All app
3. Run: `python config_manager.py --list` to see available models

### Invalid Model Name
```
Error: HTTP 404
```

**Solution:**
1. List available models: `python config_manager.py --list`
2. Copy exact model name
3. Update config: `python config_manager.py --model <exact_name>`

---

## Backup & Restore

### Backup Configuration
```bash
copy config.json config.json.backup
```

### Restore Default
```bash
git checkout config.json
```

### Share Configuration
```bash
# Copy config.json to another project
copy config.json ..\another_project\
```

---

## Advanced: Manual Editing

You can edit `config.json` directly in a text editor:

```json
{
  "gpt4all": {
    "api_base_url": "http://localhost:4891",
    "api_timeout": 30
  },
  "models": {
    "llm_model": "qwen3-8b",
    "embedding_model": "Qwen/Qwen3-Embedding-0.6B-GGUF"
  },
  "generation": {
    "max_tokens": 2000,
    "temperature": 0.2,
    "stream": false
  }
}
```

**⚠️ Important:**
- Keep JSON format valid
- Don't change key names
- Use double quotes `"`
- No trailing commas

---

## Command Reference

| Command | Description |
|---------|-------------|
| `python config_manager.py` | Interactive mode |
| `python config_manager.py --show` | Show current config |
| `python config_manager.py --model <name>` | Set LLM model |
| `python config_manager.py --embedding <name>` | Set embedding model |
| `python config_manager.py --list` | List available models |
| `python config_manager.py --temp <value>` | Set temperature |
| `python config_manager.py --max-tokens <value>` | Set max tokens |

---

## Integration

### How It Works

1. **On Startup:** `main.py`, `embed_local.py` load `config.json`
2. **Settings Applied:** Models, API URLs, generation params
3. **No Code Changes:** Edit config, not Python files

### Files That Use Config

- `main.py` - LLM model, generation settings, search
- `embed_local.py` - Embedding model, API URL
- `config_manager.py` - Configuration UI

---

**Last Updated:** 2026-03-19
**Version:** 1.0.0
