# 🚀 How to Run - AI Scan PDF

## 📋 Quick Start Checklist

- [ ] GPT4All v3.9.0+ installed
- [ ] Models downloaded in GPT4All
- [ ] PDF files in `PDF_Input/` folder
- [ ] Python dependencies installed

---

## Step 1: Install GPT4All

### Download
1. Go to: https://gpt4all.io/index.html
2. Click **"Download"** for Windows
3. Run installer and follow prompts

### First Launch
1. Open GPT4All from Start Menu
2. Accept terms of service
3. Wait for initial setup

---

## Step 2: Download Required Models

In GPT4All application:

### Model 1: LLM (Main AI)
1. Click **"Settings"** (gear icon) or **"Download Models"**
2. Search for: `unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF`
3. Click **Download**
4. Wait for download (~6 GB, 10-30 minutes depending on internet)

### Model 2: Embedding
1. Search for: `Qwen/Qwen3-Embedding-0.6B-GGUF`
2. Click **Download**
3. Wait for download (~1.5 GB, 5-15 minutes)

### Verify Downloads
- Go to main screen
- Both models should appear in model list
- Status should show **"Downloaded"**

---

## Step 3: Enable API Server

1. In GPT4All, click **Settings** (gear icon)
2. Find **"Local API Server"** section
3. Toggle **ON** (enable)
4. Verify port is **4891**
5. Click **Save**

### Test API Server

Open browser and go to: `http://localhost:4891/v1/models`

If you see a JSON list of models, API server is running ✅

Example response:
```json
{"data":[{"id":"qwen3-8b",...},{"id":"Qwen/Qwen3-Embedding-0.6B-GGUF",...}]}
```

---

## Step 4: Load Models

### In GPT4All App:
1. Go to main screen (chat interface)
2. Click on model dropdown at top
3. Select **`unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF`**
4. Wait for it to load (30-60 seconds)
5. Status should show **"Loaded"** or **"Ready"**

### Keep GPT4All Running
- **DO NOT close GPT4All** while running the pipeline
- Minimize it and let it run in background
- API server must stay on

---

## Step 5: Install Python Dependencies

Open PowerShell or Command Prompt:

```bash
pip install pdfplumber pythainlp tqdm requests numpy fitz easyocr Pillow
```

Wait for installation to complete.

---

## Step 6: Prepare PDF Files

### Create Input Folder
```
D:\dev\ai_scan_pdf\PDF_Input\
```

### Add Your PDFs
Place your Thai PDF documents in this folder:
- `DOL_FSS_Index.1เอกสารสรุปความต้องการของผู้ใช้งาน_20260131_v2.5.pdf`
- `DOL_FSS_Index.2เอกสารSRS_202600202_2.6.pdf`

Or any other Thai/English PDF documents you want to analyze.

---

## Step 7: Run the Pipeline

### 7.1 Parse PDFs to Chunks

```bash
cd D:\dev\ai_scan_pdf
python parse_and_chunk.py
```

**Expected Output:**
```
[*] Parsing PDF: PDF_Input\DOL_FSS_Index.1....pdf
Extracting pages: 100%|████████| 220/220 [02:07<00:00,  1.73it/s]
[+] Saved 59 chunks to Temp_Output\chunks\...
[*] Parsing PDF: PDF_Input\DOL_FSS_Index.2....pdf
Extracting pages: 100%|████████| 464/464 [05:27<00:00,  1.42it/s]
[+] Saved 147 chunks to Temp_Output\chunks\...
```

**Time:** ~8 minutes for 684 pages (2 PDFs)

**Output Location:** `Temp_Output/chunks/`

---

### 7.2 Generate Embeddings

```bash
python embed_local.py
```

**Expected Output:**
```
[*] Generating Embeddings with GPT4All API (Qwen/Qwen3-Embedding-0.6B-GGUF)...
[*] API Server: http://localhost:4891
[*] Processing 206 chunks...
Vectorizing PDF Chunks: 100%|████████| 206/206 [03:45<00:00,  1.09s/chunk]
[+] Successfully saved 206 embedded chunks to LearningDb_Output\vector_db.json
```

**Time:** ~3-5 minutes for 206 chunks

**Output Location:** `LearningDb_Output/vector_db.json`

---

### 7.3 Query Your Documents

```bash
python main.py
```

**Expected Output:**
```
=== GPT4All Spec Analyzer (Powered by unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF) ===
[*] Embedding Model: Qwen/Qwen3-Embedding-0.6B-GGUF
[*] API Server: http://localhost:4891
[*] Knowledge Base: 206 PDF Chunks Loaded.

[?] Question for the document (exit/quit to stop):
```

**Ask Questions:**
```
[?] Question: ระบบสามารถเบิกจ่ายงบประมาณได้อย่างไร
[*] Retrieving relevant knowledge...
[*] Performing Deep Vector Search with Embeddings...
[*] Analyzing with unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF...

==================================================
AI ANALYSIS:
[Answer in Thai based on document content]
==================================================
```

**Exit:**
Type `exit` or `quit` to stop.

---

## 📊 Expected Processing Times

### Dell Optiplex 3070 (i5-8500, 8GB RAM)

| Operation | Time | Output |
|-----------|------|--------|
| Parse PDF (220 pages) | ~2-3 min | 59 chunks |
| Parse PDF (464 pages) | ~5-6 min | 147 chunks |
| Generate Embeddings (206 chunks) | ~3-5 min | vector_db.json |
| Query + Answer | ~10-20 sec | Thai response |

**Total for 684 pages:** ~8-14 minutes (one-time processing)

---

## 🔧 Troubleshooting

### Error: Cannot connect to GPT4All

**Solution:**
1. Check GPT4All app is open
2. Check API Server is enabled (Settings → Local API Server → ON)
3. Check port is 4891
4. Restart GPT4All app

### Error: 404 Model not found

**Solution:**
1. In GPT4All, click model dropdown
2. Make sure model is loaded (not just downloaded)
3. Wait for "Loaded" status
4. Try again

### Error: MemoryError or system slow

**Solution:**
1. Close all other applications (browser, Office, etc.)
2. Restart computer to free RAM
3. Use smaller model if available
4. Consider upgrading to 16GB RAM

### Error: PDF not found

**Solution:**
1. Check PDF files are in `PDF_Input/` folder
2. Check file names match exactly in `parse_and_chunk.py`
3. Use full path if needed

### Error: Thai characters display as ???

**Solution:**
```bash
# In CMD/PowerShell, run:
chcp 65001

# Then run Python script
python main.py
```

Or use **Windows Terminal** instead of CMD.

---

## ✅ Success Indicators

### After Step 7.1 (Parse PDFs):
- ✅ See "[+] Saved XX chunks to Temp_Output\chunks\..."
- ✅ No error messages
- ✅ `Temp_Output/chunks/` folder has `.md` files

### After Step 7.2 (Embeddings):
- ✅ See "[+] Successfully saved XX embedded chunks to LearningDb_Output\vector_db.json"
- ✅ `LearningDb_Output/vector_db.json` exists
- ✅ File size is several MB

### After Step 7.3 (Query):
- ✅ See "=== GPT4All Spec Analyzer ==="
- ✅ Can type questions
- ✅ Gets Thai language responses
- ✅ Responses reference document content

---

## 🛑 Before Uploading to GitHub

### Run Security Check
```bash
python security_agent.py
```

**Expected:**
```
✅ No security issues found! Safe to commit.
```

### Verify .gitignore
Check these folders are NOT in git:
- `PDF_Input/` ✅
- `Temp_Output/` ✅
- `LearningDb_Output/` ✅
- `chunks/` ✅
- `*.pdf` ✅
- `vector_db.json` ✅

### Safe to Upload:
- ✅ `*.py` files (source code)
- ✅ `README.md`, `*.md` (documentation)
- ✅ `HTMLFile/` (user guides)
- ✅ `MDFile/` (technical specs)
- ✅ `.gitignore`

---

## 📞 Support

- **Security Guide:** See `SECURITY.md`
- **Quick Reference:** See `QUICKSTART.md`
- **GPT4All Setup:** See `HTMLFile/คู่มือการติดตั้ง_GPT4All.md`
- **Thai Guide:** See `HTMLFile/คู่มือการใช้งาน_AI_Scan_PDF.html`

---

*Last Updated: 2026-03-19*
*Version: 1.0.0*
