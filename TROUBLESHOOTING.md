# 🔧 Quick Troubleshooting Guide

## ❌ Error: Model is not loaded or busy

### Symptom
```
[ERROR] Model is not loaded or busy. Please check GPT4All app and ensure the model is loaded.
```

### ✅ Solution (5 Steps)

#### Step 1: Open GPT4All App
- Find GPT4All in Start Menu
- Launch the application
- Wait for it to fully load

#### Step 2: Check API Server
1. Click **Settings** (gear icon ⚙️)
2. Find **"Local API Server"**
3. Make sure it's **ON** (toggle should be blue/enabled)
4. Verify **Port: 4891**

#### Step 3: Load the Model
1. Go back to **main screen** (chat interface)
2. Look at the **model dropdown** at the top
3. Click and select: **`qwen3-8b`** or **`unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF`**
4. **Wait** for the model to load (30-60 seconds)
5. Status should show: **"Loaded"** or **"Ready"**

#### Step 4: Verify Model is Ready
- The model name should appear at the top
- No loading spinner
- Chat box should be active

#### Step 5: Test Connection
```bash
python test_gpt4all.py
```

Expected output:
```
✅ LLM 'qwen3-8b' is working!
```

Then try again:
```bash
python main.py
```

---

## 🚨 Still Not Working?

### Problem: Can't find model in list

**Solution:**
1. In GPT4All, click **"Download Models"**
2. Search for: `unsloth` or `deepseek`
3. Download: `unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF`
4. Wait for download (~6 GB, 10-30 minutes)
5. Then select and load it

### Problem: Model shows but won't load

**Solution:**
1. Close GPT4All completely
2. Re-open GPT4All
3. Try loading the model again
4. If still failing, restart your computer

### Problem: 500 Server Error

**Solution:**
```
Error: HTTP 500
```

This means the model is busy or crashed.

1. In GPT4All, **unload** the model (if option exists)
2. **Reload** the model
3. Wait 1 minute before querying
4. If persists, restart GPT4All app

### Problem: Connection Refused

**Solution:**
```
Error: Cannot connect to GPT4All
```

1. Check GPT4All app is **actually running** (not minimized to tray)
2. Check **API Server is enabled** in Settings
3. Check **port 4891** is correct
4. Try accessing in browser: `http://localhost:4891`
5. If blank/error, restart GPT4All

---

## 📋 Quick Checklist

Before running `python main.py`:

- [ ] GPT4All app is **open and visible**
- [ ] API Server is **enabled** (Settings → Local API Server → ON)
- [ ] Model `qwen3-8b` is **loaded** (not just downloaded)
- [ ] No loading spinner in GPT4All
- [ ] Test passed: `python test_gpt4all.py`

---

## 🎯 Quick Test Commands

```bash
# Test 1: Check GPT4All connection
curl http://localhost:4891/v1/models

# Test 2: Run test agent
python test_gpt4all.py

# Test 3: Run main program
python main.py
```

---

## 💡 Tips

### Keep GPT4All Running
- Don't close GPT4All while using `main.py`
- Minimize it, don't exit
- Model stays loaded in memory

### Reduce Memory Usage
If your system is slow:
1. Close browser tabs
2. Close Office applications
3. Close other programs
4. Your model uses ~6-8 GB RAM

### Faster Loading Next Time
- Keep GPT4All running in background
- Model stays loaded
- No need to reload every time

---

## 📞 Still Stuck?

Run the test agent for detailed diagnostics:

```bash
python test_agent.py --verbose
```

Check the results:
- If GPT4All API test fails → Fix GPT4All setup
- If model test fails → Load the model
- If all pass → Try `main.py` again

---

## 🔄 Complete Restart Procedure

If nothing works, do a complete restart:

1. **Close** GPT4All app completely
2. **Close** all Python terminals
3. **Wait** 10 seconds
4. **Open** GPT4All app
5. **Enable** API Server (Settings)
6. **Load** model: qwen3-8b
7. **Wait** for "Loaded" status
8. **Open** new terminal
9. **Run**: `python main.py`

---

**Last Updated:** 2026-03-19
**For:** GPT4All v3.9.0 + AI Scan PDF
