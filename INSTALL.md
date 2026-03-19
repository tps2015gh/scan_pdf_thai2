# 📦 Installation & Requirements

## 🎯 Quick Install (3 Steps)

### 1. Install GPT4All Desktop App
**Download:** https://gpt4all.io/index.html

- Download for Windows
- Install and run
- Download models:
  - `unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF` (~6 GB)
  - `Qwen/Qwen3-Embedding-0.6B-GGUF` (~1.5 GB)

### 2. Install Python Dependencies
```bash
pip install pdfplumber pythainlp tqdm requests numpy fitz easyocr Pillow
```

### 3. Configure GPT4All
1. Open GPT4All app
2. Settings → Enable "Local API Server"
3. Port: **4891**
4. Load model: **qwen3-8b**

---

## 📋 Full Requirements

### System Requirements

| Component | Minimum | Recommended |
|-----------|---------|-------------|
| **OS** | Windows 10 | Windows 11 |
| **CPU** | Intel i5-8500 | Intel i7-8700+ |
| **RAM** | 8 GB | 16 GB |
| **Storage** | 256 GB SSD | 512 GB NVMe |
| **Python** | 3.8+ | 3.10+ 64-bit |

### Python Version Note

**Current Setup:** Python 3.8.5 (32-bit)
- ✅ Works with GPT4All Desktop App
- ⚠️ Limited gpt4all Python library support
- ✅ Uses API-based approach

**If Upgrading:** Python 3.10+ (64-bit)
- ✅ Full gpt4all library support
- ✅ Better performance
- ✅ More embedding options

---

## 🔧 Python Packages

### Core Dependencies
```bash
# PDF Processing
pdfplumber        # PDF text extraction
fitz              # PDF manipulation (PyMuPDF)
pythainlp         # Thai language processing

# AI/ML
requests          # HTTP API calls to GPT4All
numpy             # Vector operations
tqdm              # Progress bars

# OCR (Optional)
easyocr           # Thai/English OCR
Pillow            # Image processing
```

### Install Command
```bash
pip install pdfplumber pythainlp tqdm requests numpy fitz easyocr Pillow
```

### Optional: Better Embeddings
```bash
# For improved semantic search (requires Python 3.10+ 64-bit)
pip install sentence-transformers

# Or use GPT4All Python library (if available for your Python version)
pip install gpt4all
```

---

## 📁 Project Structure

```
ai_scan_pdf/
├── PDF_Input/              # Place your PDF files here
├── Temp_Output/            # Intermediate chunks (auto-created)
├── LearningDb_Output/      # Vector database (auto-created)
│
├── parse_and_chunk.py      # Step 1: Parse PDFs
├── embed_local.py          # Step 2: Generate embeddings
├── main.py                 # Step 3: Query documents
├── ocr_test.py             # Optional: OCR for scanned PDFs
│
├── security_agent.py       # Security scanner
├── pre_commit_hook.py      # Git pre-commit hook
│
├── README.md               # Main documentation
├── QUICK_START.md          # Step-by-step guide
├── HOW_TO_RUN.md           # Detailed setup guide
├── GPT4ALL_EMBEDDING_SETUP.md  # Embedding options
└── requirements.txt        # This file (create if needed)
```

---

## 🚀 Quick Test

After installation, test each component:

### Test 1: GPT4All Connection
```bash
python test_gpt4all.py
```

Expected: ✅ for API and LLM

### Test 2: Parse PDFs
```bash
python parse_and_chunk.py
```

Expected: Chunks saved to `Temp_Output/chunks/`

### Test 3: Generate Embeddings
```bash
python embed_local.py
```

Expected: `LearningDb_Output/vector_db.json` created

### Test 4: Query System
```bash
python main.py
```

Expected: Interactive prompt appears

---

## 🔒 Security

Before uploading to GitHub:

```bash
python security_agent.py
```

**Expected:** ✅ No security issues found

**Auto-ignored folders:**
- `PDF_Input/` - Your documents
- `Temp_Output/` - Processing output
- `LearningDb_Output/` - Vector database
- `chunks/` - Text chunks
- `*.pdf`, `*.json`, `*.gguf` - Data files

---

## 🆘 Troubleshooting Installation

### Problem: pip install fails

**Solution:**
```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Then install packages
pip install pdfplumber pythainlp tqdm requests numpy
```

### Problem: GPT4All model download fails

**Solution:**
1. Check internet connection
2. Try downloading GGUF directly from HuggingFace
3. Place in GPT4All models folder:
   - Windows: `C:\Users\<YourName>\gpt4all\`

### Problem: Thai text not displaying

**Solution:**
```bash
# Set console to UTF-8
chcp 65001

# Use Windows Terminal instead of CMD
wt
```

### Problem: Import Error

**Solution:**
```bash
# Check installed packages
pip list

# Reinstall if needed
pip install --force-reinstall pdfplumber pythainlp
```

---

## 📞 Additional Resources

- **GPT4All Docs:** https://docs.gpt4all.io/
- **PyThaiNLP:** https://pythainlp.org/
- **PDFPlumber:** https://github.com/jsvine/pdfplumber
- **EasyOCR:** https://github.com/JaidedAI/EasyOCR

---

## 📝 Version Information

**Current Setup:**
- GPT4All Desktop: v3.9.0
- Python: 3.8.5 (32-bit)
- LLM Model: unsloth/DeepSeek-R1-0528-Qwen3-8B-GGUF
- Embedding: Qwen/Qwen3-Embedding-0.6B-GGUF

**Last Updated:** 2026-03-19

---

## ✅ Installation Checklist

- [ ] GPT4All Desktop App installed
- [ ] Models downloaded (qwen3-8b, Qwen3-Embedding-0.6B)
- [ ] API Server enabled in GPT4All
- [ ] Python packages installed
- [ ] PDF files in `PDF_Input/` folder
- [ ] Tested with `python test_gpt4all.py`
- [ ] Security check passed

**Ready to use!** Run `python main.py` to start querying your documents.
