# 🚀 Quick Start - AI Scan PDF

## 📋 Step-by-Step Guide

### **Step 1: Start GPT4All** ⏳
```
1. Open GPT4All application
2. Go to Settings (gear icon)
3. Enable "Local API Server" (port 4891)
4. Load model: qwen3-8b (or unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF)
5. Keep GPT4All running in background
```

**✅ Verify:** Open browser → http://localhost:4891/v1/models

---

### **Step 2: Parse PDFs** 📄
```bash
python parse_and_chunk.py
```

**What it does:**
- Reads PDF files from `PDF_Input/` folder
- Extracts text from each page
- Splits into chunks (4000 chars each)
- Saves to `Temp_Output/chunks/`

**Expected Output:**
```
[*] Parsing PDF: PDF_Input\document.pdf
Extracting pages: 100%|████████| 220/220 [02:07<00:00]
[+] Saved 59 chunks to Temp_Output\chunks\...
```

**Time:** ~2-3 minutes per 200 pages

---

### **Step 3: Generate Embeddings** 🔮
```bash
python embed_local.py
```

**What it does:**
- Reads chunks from `Temp_Output/chunks/`
- Creates vector embeddings for each chunk
- Saves to `LearningDb_Output/vector_db.json`

**Expected Output:**
```
[*] Processing 206 chunks...
Vectorizing PDF Chunks: 100%|████████| 206/206 [00:01<00:00]
[+] Successfully saved 206 embedded chunks
```

**Time:** ~1-2 minutes for 200 chunks

**Note:** Currently uses semantic hash fallback (GPT4All embedding API not available in v3.9.0)

---

### **Step 4: Query Documents** ❓
```bash
python main.py
```

**What it does:**
- Loads vector database
- Lets you ask questions about your PDFs
- Searches relevant chunks
- AI generates answers based on document content

**Expected Output:**
```
======================================================================
🔍 Checking GPT4All Status...
======================================================================
[✓] GPT4All API: API Server is running
======================================================================
=== GPT4All Spec Analyzer (Powered by qwen3-8b) ===
======================================================================
[*] Knowledge Base: 206 PDF Chunks Loaded.

📋 Quick Help:
   - Type your question in Thai or English
   - Type 'help' for more options
   - Type 'exit' to stop
======================================================================

[?] Your question:
```

**Example Questions:**
- `ระบบเบิกจ่ายงบประมาณทำอย่างไร`
- `What is the budget approval process?`
- `ขั้นตอนการตรวจสอบใบสำคัญ`
- `help` - Show help
- `info` - Show system info
- `exit` - Exit program

---

## 🎯 Complete Workflow

```
┌─────────────────┐
│  Step 1: Start  │
│  GPT4All App    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Step 2: Parse  │◄── Run once per new PDF
│  PDFs           │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Step 3: Generate│◄── Run once per new/changed PDF
│  Embeddings     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  Step 4: Query  │◄── Run anytime to ask questions
│  Documents      │
└─────────────────┘
```

---

## 🔧 Troubleshooting

### Problem: "Cannot connect to GPT4All"

**Solution:**
1. Check GPT4All app is open
2. Check API Server is enabled (Settings → Local API Server → ON)
3. Check port is 4891
4. Restart GPT4All app

### Problem: "500 Server Error"

**Solution:**
1. In GPT4All app, make sure model is **loaded** (not just downloaded)
2. Click on model name to load it
3. Wait for "Loaded" status
4. Try again

### Problem: "vector_db.json not found"

**Solution:**
1. Run Step 2: `python parse_and_chunk.py`
2. Run Step 3: `python embed_local.py`
3. Then run Step 4

### Problem: Thai characters display as ???

**Solution:**
```bash
# In CMD/PowerShell:
chcp 65001
python main.py

# Or use Windows Terminal instead
```

---

## 📊 When to Re-run Each Step

| Step | When to Re-run |
|------|----------------|
| **Step 1** | Every time (start GPT4All) |
| **Step 2** | When you add/change PDF files |
| **Step 3** | After running Step 2 |
| **Step 4** | Anytime you want to query |

---

## 🎓 Tips for Better Results

### Writing Good Questions:
- ✅ Be specific: `ขั้นตอนการเบิกค่ารักษาพยาบาล`
- ✅ Use keywords from documents
- ✅ Ask one thing at a time
- ❌ Too vague: `บอกทุกอย่าง` (tell everything)

### Example Questions:
```
✅ Good:
- ระบบตรวจสอบใบสำคัญมีขั้นตอนอย่างไร
- ใครเป็นผู้อนุมัติการเบิกจ่ายงบประมาณ
- เงินนอกงบประมาณประเภทใดบ้าง

❌ Bad:
- everything
- all info
- tell me about budget (too broad)
```

---

## 📞 Need Help?

1. Run `python main.py` and type `help`
2. Check `HOW_TO_RUN.md` for detailed guide
3. Check `GPT4ALL_EMBEDDING_SETUP.md` for embedding issues
4. Run `python security_agent.py` to check for problems

---

**Last Updated:** 2026-03-19
**Version:** 1.0.0
