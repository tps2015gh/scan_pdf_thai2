# ⚠️ START HERE - AI Scan PDF Troubleshooting

## ❌ If You See This Error:
```
[ERROR] Model is not loaded or busy. Please check GPT4All app and ensure the model is loaded.
```

## ✅ QUICK FIX (3 Steps)

### Step 1: Open GPT4All App
- Find **GPT4All** in Start Menu
- Launch the application
- **Keep it open**

### Step 2: Load the Model
1. In GPT4All, click **Settings** (gear icon ⚙️)
2. Enable **"Local API Server"** (toggle ON)
3. Go back to **main screen** (chat)
4. Click model dropdown at top
5. Select: **`qwen3-8b`** or **`unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF`**
6. **Wait 30-60 seconds** until it says "Loaded"

### Step 3: Test and Run
```bash
# Test connection
python setup_model_api.py --test

# If test passes, run main program
python main.py
```

---

## 🎯 Alternative: Use Different Backend

### Use Ollama Instead:
```bash
# 1. Install Ollama: https://ollama.ai
# 2. Pull model
ollama pull qwen2.5:7b

# 3. Switch backend
python setup_model_api.py --backend ollama

# 4. Test
python setup_model_api.py --test

# 5. Run
python main.py
```

### Use LM Studio Instead:
```bash
# 1. Open LM Studio
# 2. Start Local Server
# 3. Load a model

# 4. Switch backend
python setup_model_api.py --backend lmstudio

# 5. Test
python setup_model_api.py --test

# 6. Run
python main.py
```

---

## 📚 Full Documentation

| File | What It's For |
|------|---------------|
| **KNOWN_ISSUES.md** | ⭐ Start here for troubleshooting |
| QUICK_START.md | Step-by-step setup guide |
| INSTALL.md | Installation instructions |
| CONFIG_GUIDE.md | How to change models/settings |
| setup_model_api.py | Switch between backends |

---

## 🆘 Still Not Working?

### Run Diagnostic:
```bash
python test_agent.py
```

### Check Configuration:
```bash
python config_manager.py --show
```

### List Available Models:
```bash
python setup_model_api.py --list
```

### Get Help:
Read **KNOWN_ISSUES.md** for detailed troubleshooting.

---

## ✅ Success Indicators

You're ready when you see:
```
[✓] GPT4ALL API: API Server is running
=== AI Scan PDF - Spec Analyzer ===
[*] Backend: GPT4ALL
[*] LLM Model: qwen3-8b
```

Then you can type your question!

---

**Last Updated:** 2026-03-19
