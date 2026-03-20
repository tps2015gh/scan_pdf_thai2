# Ollama Setup Guide (Recommended)

## 🌟 Why Ollama?

Ollama is now the recommended backend for this project because:
- ✅ **Full API Support:** Includes both Chat and Embedding APIs out of the box.
- ✅ **Low Resource:** Highly optimized for CPU and low RAM (perfect for 4GB notebooks).
- ✅ **Thai Support:** Excellent support for Thai language models like Qwen.
- ✅ **Easy Management:** Simple CLI for pulling and running models.

---

## 🔧 Installation

1. **Download Ollama:** https://ollama.com/
2. **Install:** Run the installer and follow the instructions.
3. **Verify:** Open a terminal and run `ollama --version`.

---

## 📦 Required Models

Pull the lightweight models optimized for 4GB RAM:

### 1. Main LLM (Chat/Analysis)
```bash
ollama pull qwen3.5:0.8b
```
*Size: ~0.5 GB | RAM: ~1.0 GB*

### 2. Embedding Model (Vector Search)
```bash
ollama pull nomic-embed-text
```
*Size: ~0.3 GB | RAM: ~0.5 GB*

---

## ⚙️ Configuration

Ensure your `config.json` is set to use Ollama:

```json
"backend": {
  "type": "ollama",
  "api_base_url": "http://localhost:11434",
  "api_timeout": 60
},
"models": {
  "llm_model": "qwen3.5:0.8b",
  "embedding_model": "nomic-embed-text:latest"
}
```

---

## 🚀 Running the Pipeline

1. **Parse:** `python parse_and_chunk.py`
2. **Embed:** `python embed_local.py`
3. **Query:** `python main.py`

---

## 📊 Performance on 4GB RAM

| Model | Load Time | Inference Speed | RAM Usage |
|-------|-----------|-----------------|-----------|
| **qwen3.5:0.8b** | ~2-3 sec | ~15-20 tok/s | ~0.8 GB |
| **nomic-embed** | ~1 sec | Fast | ~0.3 GB |

**Total System RAM Usage:** ~2.5 GB (Leaving ~1.5 GB for OS/Python).

---

## 📝 Troubleshooting

- **Connection Error:** Ensure Ollama is running in the tray.
- **Model Not Found:** Pull the models using `ollama pull`.
- **Sluggishness:** Close Chrome/Edge and other high-RAM applications.

---
**Last Updated:** 2026-03-20
**Ollama Version:** Latest
**Status:** Recommended Backend
