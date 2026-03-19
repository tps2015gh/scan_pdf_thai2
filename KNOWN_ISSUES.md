# ⚠️ Known Issues & Troubleshooting

## ❌ ERROR: Model is not loaded or busy

### Symptom
When running `python main.py`, you see:
```
[ERROR] Model is not loaded or busy. Please check GPT4All app and ensure the model is loaded.
```

### ✅ ROOT CAUSE
The AI model is **NOT loaded** in your API backend (GPT4All, Ollama, LM Studio, etc.).

The system can connect to the API server, but no model is ready to process requests.

---

## 🔧 Solution (By Backend)

### If Using GPT4All (Default)

#### Step-by-Step Fix:

1. **Open GPT4All Application**
   - Find it in Start Menu
   - Launch the application

2. **Enable API Server**
   - Click **Settings** (gear icon ⚙️)
   - Find **"Local API Server"**
   - Toggle **ON** (should be blue/enabled)
   - Verify **Port: 4891**

3. **Load the Model**
   - Go back to **main screen** (chat interface)
   - Look at **model dropdown** at top
   - Click and select: **`qwen3-8b`** or search for **`unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF`**
   - **Wait 30-60 seconds** for model to load
   - Status should show: **"Loaded"** or **"Ready"**

4. **Verify Model is Ready**
   - Model name appears at top
   - No loading spinner
   - Chat box is active

5. **Test Connection**
   ```bash
   python test_gpt4all.py
   ```
   Expected: ✅ LLM working

6. **Try Again**
   ```bash
   python main.py
   ```

---

### If Using Ollama

#### Step-by-Step Fix:

1. **Start Ollama**
   ```bash
   ollama serve
   ```

2. **Pull Model** (first time only)
   ```bash
   ollama pull qwen2.5:7b
   ```

3. **Verify Model**
   ```bash
   ollama list
   ```
   You should see your model listed.

4. **Configure Backend**
   ```bash
   python setup_model_api.py --backend ollama
   ```

5. **Test Connection**
   ```bash
   python setup_model_api.py --test
   ```

6. **Run Main Program**
   ```bash
   python main.py
   ```

---

### If Using LM Studio

#### Step-by-Step Fix:

1. **Open LM Studio**
   - Launch the application

2. **Start Local Server**
   - Click **"Local Server"** tab
   - Click **"Start Server"**
   - Verify port is **1234**

3. **Load a Model**
   - Click **"Load Model"**
   - Select a model from the list
   - Wait for loading to complete

4. **Configure Backend**
   ```bash
   python setup_model_api.py --backend lmstudio
   ```

5. **Test Connection**
   ```bash
   python setup_model_api.py --test
   ```

6. **Run Main Program**
   ```bash
   python main.py
   ```

---

## 🎯 Quick Diagnostic

Run this to check what's wrong:

```bash
python setup_model_api.py --test
```

### Possible Results:

#### ✅ Backend is working
```
✅ Backend is working!
```
**Next:** Run `python main.py`

#### ❌ Cannot connect
```
[!] Cannot connect - API server may not be running
```
**Fix:** Start your API server (GPT4All/Ollama/LM Studio)

#### ❌ Model not loaded (500)
```
[!] Model not loaded (500 error)
```
**Fix:** Load a model in your API backend

---

## 🔄 Switch Between Backends

### Available Backends:
- **gpt4all** - GPT4All Desktop App (default)
- **ollama** - Ollama (ollama.ai)
- **lmstudio** - LM Studio
- **custom** - Any OpenAI-compatible API

### How to Switch:

```bash
# List available backends
python setup_model_api.py --list

# Switch to GPT4All (default)
python setup_model_api.py --backend gpt4all

# Switch to Ollama
python setup_model_api.py --backend ollama

# Switch to LM Studio
python setup_model_api.py --backend lmstudio

# Test connection
python setup_model_api.py --test
```

---

## 📋 Common Issues

### Issue 1: "Connection refused"
```
Error: Cannot connect to GPT4ALL
```

**Cause:** API server not running

**Fix:**
1. Open GPT4All app
2. Enable API Server in Settings
3. Make sure port is 4891

---

### Issue 2: "500 Server Error"
```
Error: HTTP 500
```

**Cause:** Model not loaded or busy

**Fix:**
1. Load model in GPT4All/Ollama/LM Studio
2. Wait for "Loaded" status
3. Wait 1 minute before querying

---

### Issue 3: "404 Not Found"
```
Error: HTTP 404
```

**Cause:** Wrong model name or endpoint

**Fix:**
1. Check model name matches exactly
2. List available models: `python setup_model_api.py --list`
3. Update config: `python setup_model_api.py --model <exact_name>`

---

### Issue 4: "Model not found in config"
```
[!] Model name not found
```

**Cause:** Model name in config doesn't match loaded model

**Fix:**
```bash
# See what's loaded
python setup_model_api.py --list

# Update config
python config_manager.py --model <model_name_from_list>
```

---

## 🛠️ Manual Configuration

Edit `config.json` directly:

### For GPT4All:
```json
{
  "backend": {
    "type": "gpt4all",
    "api_base_url": "http://localhost:4891"
  },
  "models": {
    "llm_model": "qwen3-8b",
    "embedding_model": "Qwen/Qwen3-Embedding-0.6B-GGUF"
  }
}
```

### For Ollama:
```json
{
  "backend": {
    "type": "ollama",
    "api_base_url": "http://localhost:11434"
  },
  "models": {
    "llm_model": "qwen2.5:7b",
    "embedding_model": "nomic-embed-text"
  }
}
```

### For LM Studio:
```json
{
  "backend": {
    "type": "lmstudio",
    "api_base_url": "http://localhost:1234"
  },
  "models": {
    "llm_model": "local-model",
    "embedding_model": "local-model"
  }
}
```

---

## 📞 Still Having Issues?

### Run Full Diagnostic:
```bash
python test_agent.py --verbose
```

### Check Logs:
- GPT4All: Check app console/output
- Ollama: Check terminal where `ollama serve` is running
- LM Studio: Check Server tab logs

### Get Help:
1. Run: `python setup_model_api.py --list`
2. Screenshot the output
3. Check which backend you're using: `python config_manager.py --show`
4. Verify model is loaded in your backend app

---

## ✅ Success Checklist

Before `python main.py` will work:

- [ ] API backend is running (GPT4All/Ollama/LM Studio)
- [ ] API Server is enabled (for GPT4All: Settings → Local API Server)
- [ ] Model is loaded (not just downloaded)
- [ ] Test passes: `python setup_model_api.py --test`
- [ ] Correct backend configured: `python config_manager.py --show`

---

**Last Updated:** 2026-03-19
**Version:** 1.0.0
