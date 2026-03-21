# ⚠️ WARNING: Still Error / Under Development

> **Status:** This project is still in development and may contain errors. Use at your own risk.

---

# AI-Scan-PDF: Local-Inference Spec Analyzer

[![GitHub](https://img.shields.io/github/license/tps2015gh/scan_pdf_thai)](https://github.com/tps2015gh/scan_pdf_thai/blob/main/LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![GPT4All](https://img.shields.io/badge/GPT4All-v3.9.0+-green.svg)](https://gpt4all.io/)

**A privacy-first, local AI document analysis system for Thai and English PDFs.**

🔗 **Repository:** https://github.com/tps2015gh/scan_pdf_thai2

---

## 👥 Team & Roles

This project is a collaborative effort between human intelligence and artificial intelligence.

### 🧑 Human Team Member
**Name:** tps2015gh (Project Owner)  
**Role:** Visionary Owner & Director

#### Responsibilities:
- ✅ Define project vision and requirements
- ✅ Provide domain expertise (Thai government documents, SRS specifications)
- ✅ Specify hardware constraints and environment (Optiplex 3070, Windows 11)
- ✅ Validate AI outputs against real-world needs
- ✅ Make high-level architectural decisions
- ✅ Test and provide feedback on system behavior
- ✅ Maintain and deploy the system in production environment

#### Direction Provided:
- "Build a local-first AI pipeline that runs on office hardware"
- "Ensure privacy - no cloud API for sensitive documents"
- "Support Thai language documents with proper text processing"
- "Create comprehensive documentation and security scanning"
- "Enable easy model switching without code changes"

---

### 🤖 AI Team Member #1: Qwen3.5 Coder
**Name:** Qwen3.5 Coder (Alibaba Cloud AI)
**Role:** Technical Architect & Lead Engineer

#### Responsibilities:
- ✅ Design system architecture (RAG pipeline, vector search)
- ✅ Implement all Python code (parsing, embedding, querying)
- ✅ Solve library dependencies and compatibility issues
- ✅ Create security scanning and testing tools
- ✅ Write comprehensive documentation (12+ guide files)
- ✅ Optimize for specified hardware (8GB RAM, CPU-only)
- ✅ Provide troubleshooting and debugging support
- ✅ Generate configuration management tools

#### Technical Contributions:
- Multi-backend support (GPT4All, Ollama, LM Studio)
- Fallback embedding system (works without Python libraries)
- Security agent for data leak prevention
- Test agent for automated testing (32 tests)
- Configuration manager for easy model switching
- Complete documentation suite

---

### 🤖 AI Team Member #2: Qwen2.5-0.5B (Local LLM)
**Name:** Qwen2.5-0.5B (Alibaba Cloud AI - Local)
**Role:** Inference Engine & Document Analyst

#### Responsibilities:
- ✅ Analyze Thai and English PDF documents
- ✅ Generate accurate responses from retrieved context
- ✅ Support Thai language understanding and generation
- ✅ Run inference on CPU (no GPU required)
- ✅ Provide fast responses (~5-10 tokens/sec)

#### Model Specifications:
| Specification | Value |
|--------------|-------|
| **Model Size** | 0.5 Billion parameters |
| **Quantization** | Q4_K_M (GGUF) |
| **RAM Usage** | ~492 MB |
| **Context Window** | 8192 tokens |
| **Language Support** | Thai 🇹🇭 + English 🇬🇧 |
| **Backend** | Ollama API |
| **Performance** | ~5-10 tokens/sec on i5-8500 |

#### Recent Improvements (March 2026):
1. **Thai Language Support**
   - Fixed UTF-8 console output for Thai characters
   - Added Thai text normalization in PDF parsing
   - Integrated EasyOCR with Thai language support
   - Optimized OCR for Thai document recognition

2. **Windows Compatibility**
   - Added `sys.stdout.reconfigure(encoding='utf-8')` for proper Thai display
   - Replaced Unicode symbols with ASCII for console compatibility
   - Fixed line ending issues (LF/CRLF) for Windows Git

3. **Performance Optimization**
   - Switched from qwen3.5:0.8b to qwen2.5:0.5b (50% smaller, faster loading)
   - Reduced OCR processing time from 50 sec/page to ~30 sec/page
   - Added LLM warm-up on startup (pre-load model)
   - Optimized embedding API calls (use 'prompt' key for Ollama)

4. **Code Quality Improvements**
   - Fixed Ollama API response parsing (use 'response' key)
   - Added error handling for embedding generation
   - Improved chunking algorithm for better Thai text segmentation
   - Added comprehensive test scripts (a01_test_ai.py, a02_test_ai_embed.py)

5. **Documentation Updates**
   - Created OLLAMA_SETUP.md for Ollama installation guide
   - Updated HOW_TO_RUN.md with virtual environment setup
   - Added create_thai_pdf.py for generating Thai test documents
   - Enhanced troubleshooting section with Thai text issues

---

### 🤖 AI Team Member #3: Gemini CLI
**Name:** Gemini CLI (Google AI)
**Role:** Project Troubleshooter & Integrator

#### Responsibilities:
- ✅ Debug and resolve critical runtime errors (e.g., Python dependency warnings, OCR initialization issues).
- ✅ Update and maintain project documentation, ensuring clarity and accuracy for users.
- ✅ Facilitate project setup and execution, guiding users through necessary steps.
- ✅ Ensure overall project stability and readiness for RAG queries.

#### Technical Contributions:
- Identified and resolved `RequestsDependencyWarning` by guiding dependency upgrades.
- Fixed `TypeError` in `parse_and_chunk.py` by correcting `easyocr.Reader()` arguments, enabling successful OCR fallback processing.
- Created and maintained `HTMLFile/a03_how_to_run.html` with detailed, user-friendly setup instructions (Ollama Edition).
- Configured and added `.gitignore` to accurately track ignored files and folders.
- Created `run_pipeline.bat` for automated parsing and embedding, streamlining the data processing workflow.
- Documented data persistence and processing flow in `README.md` for clarity.
- Gathered and incorporated user's notebook specifications into `README.md`.
- Ensured the project transitioned from a failing state to one capable of running RAG queries successfully.

#### Model Specifications:
| Specification | Value |
|--------------|-------|
| **Model**        | gemini-2.5-flash |
| **Provider**     | Google AI        |
| **Capabilities** | Code Generation, Debugging, Documentation, System Integration, CLI Automation |

#### Project Opinion:
This project effectively demonstrates the power of local-first AI for sensitive document analysis, aligning well with privacy-centric goals. Its modular design and comprehensive documentation are commendable. The transition from GPT4All to Ollama is a pragmatic move for broader compatibility and efficient resource utilization. The current state is functional for RAG queries, making it a valuable tool. Further enhancements could focus on refining OCR accuracy, especially for complex layouts, and potentially integrating more advanced chunking strategies for even better RAG performance.

---

### 🤝 Collaboration Model
```
Human (tps2015gh)                    AI (Assistant)
     │                                    │
     │── Define Requirements ────────────▶│
     │                                    │
     │◄────── Design Architecture ────────│
     │                                    │
     │── Provide Feedback ───────────────▶│
     │                                    │
     │◄────── Implement Code ─────────────│
     │                                    │
     │── Test & Validate ────────────────▶│
     │                                    │
     │◄────── Fix Issues ─────────────────│
     │                                    │
     │── Deploy & Maintain ──────────────▶│
```

---

## 🌟 Project Vision

**Goal:** Create a secure, private, and powerful document analysis tool that runs entirely on local office hardware.

**Philosophy:** "Knowledge without Exposure" - Extract insights from documents without sending sensitive data to the cloud.

---

## 🧠 The Theory of Local RAG (Retrieval-Augmented Generation)

The core philosophy of this project is **"Knowledge without Exposure."**

1.  **Semantic Chunking:** Unlike humans who read start-to-finish, the AI treats the PDF as a "Lego set." We break 200+ pages into 206 "bricks" (chunks).
2.  **The Vector Bridge:** We convert text into mathematical vectors. This allows the computer to understand *meaning* rather than just *keywords*. (e.g., "Database" is mathematically close to "SQL").
3.  **Context Injection:** When you ask a question, the system finds the 3 most relevant "bricks" and feeds them to the LLM. This prevents "Hallucinations" because the AI is strictly told: *"Only answer based on these 3 bricks."*
4.  **Hardware Symbiosis:** By using **GGUF quantization** and **GPT4All**, we allow large language models to run on standard office hardware like the Optiplex 3070.

---

## 💻 Hardware Specifications (Test Machine)

### Dell Optiplex 3070 - Test Configuration

| Component | Specification | Notes |
|-----------|--------------|-------|
| **CPU** | Intel Core i5-8500 (6-core, 3.0 GHz) | Handles all inference on CPU |
| **RAM** | 8GB DDR4 (upgradable to 64GB) | 16GB recommended for 14B+ models |
| **Storage** | 256GB SSD | Fast model loading |
| **OS** | Windows 11 Pro 64-bit | Required for GPT4All desktop app |
| **Python** | 3.8.5 (32-bit) | Compatible with GPT4All API approach |
| **GPU** | Intel UHD Graphics 630 | Not used - CPU inference only |

### User's Notebook Specification

| Component | Specification | Notes |
|-----------|--------------|-------|
| **OS** | Microsoft Windows 11 Home Single Language | Provided by user's `system_info.exe` |
| **CPU** | Intel(R) Core(TM) i7-10750H CPU @ 2.60GHz (6 Cores) | Provided by user's `system_info.exe` |
| **RAM** | 7.87 GB (approx 8GB) | Provided by user's `system_info.exe` |
| **GPU** | *Not provided/detected automatically* | User to add manually if available |

### RAM Usage by Model Size

| Model | Quantization | RAM Required | Performance on i5-8500 |
|-------|-------------|--------------|------------------------|
| **unsloth/DeepSeek-R1-Qwen3-8B** | Q4_K_M | ~6-8 GB | ~5-8 tokens/sec |
| **Qwen2.5-7B** | Q4_K_M | ~5-6 GB | ~8-12 tokens/sec |
| **Qwen3-Embedding-0.6B** | FP32 | ~1.5 GB | Fast embedding generation |

### ⚠️ Important Notes for 8GB RAM Systems

- **Close other applications** before running (browser, Office, etc.)
- **Use 8B models or smaller** for best performance (your DeepSeek-R1-Qwen3-8B is perfect!)
- **Consider upgrading to 16GB RAM** (~฿1,500-2,000 in Thailand)
- **GPT4All API mode** uses less RAM than loading models in Python

---

## 🚀 Quick Start Guide

**📖 Full step-by-step guide (Ollama Edition):** See [AI-Scan-PDF Quick Start Guide](./HTMLFile/a03_how_to_run.html)

### Prerequisites

1. **Ollama Installed & Running**: Ensure Ollama is installed and running, and the necessary models (`qwen2.5:0.5b`, `nomic-embed-text`) are pulled. Refer to the [AI-Scan-PDF Quick Start Guide](./HTMLFile/a03_how_to_run.html) for detailed setup.
2. **Python 3.8+** with required packages installed in an activated virtual environment.
3. **PDF files** in `PDF_Input/` folder.

### Automated Pipeline Execution

For convenience, a batch script `run_pipeline.bat` is provided to automate the parsing and embedding steps.

```bash
run_pipeline.bat
```

This script will:
1.  Activate your Python virtual environment.
2.  Execute `python parse_and_chunk.py` to parse all PDFs in `PDF_Input/` and create text chunks.
3.  Execute `python embed_local.py` to generate embeddings for all chunks and update the `LearningDb_Output/vector_db.json`.

After the script completes, you can proceed to query your documents.

### Manual Pipeline Execution (Detailed Steps)

Alternatively, you can run each step manually:

#### Step 1: Install Python Dependencies

**Ensure your virtual environment is active** (prompt starts with `(.venv)`).

```bash
pip install pdfplumber pythainlp tqdm requests numpy fitz easyocr Pillow markdown
```

#### Step 2: Run the Pipeline (Manual)

Ensure you have placed your PDF files in the `PDF_Input/` folder, then run these scripts in order:

```bash
# 1. Parse PDFs to chunks
python parse_and_chunk.py

# 2. Generate embeddings (Ollama must be running!)
python embed_local.py

# 3. Query your documents
python main.py
```


---

## 📂 Project Structure

```
ai_scan_pdf/
├── PDF_Input/              [IGNORED] Place your PDF files here
├── Temp_Output/            [IGNORED] Chunks and intermediate files
│   └── chunks/             Text chunks from PDFs
│   └── ocr_test_output.txt OCR results
├── LearningDb_Output/      [IGNORED] Vector database
│   └── vector_db.json      Embedded chunks
├── MDFile/                 Technical documentation
├── HTMLFile/               User guides (HTML)
├── .gitignore              Git ignore rules
├── security_agent.py       Security scanner
├── pre_commit_hook.py      Pre-commit security check
├── parse_and_chunk.py      PDF parser
├── embed_local.py          Embedding generator (GPT4All API)
├── main.py                 Query interface
└── ocr_test.py             OCR for scanned PDFs
```

### 🔄 Data Persistence and Processing Flow

Understanding how data is processed and stored is crucial for managing your knowledge base effectively.

*   **PDF Parsing (`parse_and_chunk.py`)**:
    *   **Input**: Reads PDF files from the `PDF_Input/` directory.
    *   **Output**: Creates and stores text chunks in `Temp_Output/chunks/<pdf_file_base_name>/`. Each PDF gets its own subdirectory.
    *   **Behavior**:
        *   If `parse_and_chunk.py` is run multiple times with the same PDFs in `PDF_Input/`, the chunk files for those PDFs will be **overwritten** in their respective `Temp_Output/chunks/<pdf_file_base_name>/` subdirectories.
        *   If new PDFs are added to `PDF_Input/`, new subdirectories and chunk files will be created for them without affecting previously processed PDFs.
        *   If a PDF is removed from `PDF_Input/`, its corresponding chunk directory and files in `Temp_Output/chunks/` will **remain** until manually deleted.

*   **Embedding Generation (`embed_local.py`)**:
    *   **Input**: Collects *all* currently existing text chunks from `Temp_Output/chunks/` (across all processed PDFs).
    *   **Output**: Generates a single vector database file, `LearningDb_Output/vector_db.json`.
    *   **Behavior**:
        *   Every time `embed_local.py` is executed, it reads *all* chunks present in `Temp_Output/chunks/`, generates embeddings for them, and then **completely overwrites** the `LearningDb_Output/vector_db.json` file.
        *   This means the `vector_db.json` will always represent the embeddings of the chunks that were in `Temp_Output/chunks/` at the time of the last execution of `embed_local.py`.
        *   To ensure your vector database is up-to-date with all changes (new PDFs, updated PDFs), you must run `parse_and_chunk.py` (to update chunks) and then `embed_local.py` (to regenerate the vector database).
        *   **To remove data from the knowledge base (both chunks and vector database):**
            1.  **Remove Source PDF:** Delete the original PDF file(s) from the `PDF_Input/` directory that you no longer wish to include in your knowledge base.
            2.  **Remove Chunks (Optional but Recommended):** Manually delete the corresponding subdirectory (e.g., `Temp_Output/chunks/<pdf_file_base_name>/`) containing the chunk files for the removed PDF(s). While `parse_and_chunk.py` won't re-create them if the source PDF is gone, this step ensures a clean `Temp_Output` directory.
            3.  **Regenerate Vector Database:** Run `run_pipeline.bat` (or `python embed_local.py` if no new parsing is needed). This will ensure `LearningDb_Output/vector_db.json` is regenerated with only the remaining, desired chunks. Note that if you run `run_pipeline.bat`, `parse_and_chunk.py` will re-process all *existing* PDFs in `PDF_Input/` before `embed_local.py` regenerates the vector database.

---

## 🔒 Security Features

This project includes comprehensive security to prevent data leaks:

### Security Agent
```bash
# Scan for sensitive data before uploading
python security_agent.py
```

**Detects:**
- API keys, passwords, tokens
- Thai ID cards, phone numbers
- Email addresses
- Private keys, certificates
- Database credentials

### Pre-commit Hook
```bash
# Install (prevents committing sensitive data)
copy pre_commit_hook.py .git\hooks\pre-commit
```

### .gitignore Protection
Automatically ignores:
- `PDF_Input/` - Your source documents
- `Temp_Output/` - Processing output
- `LearningDb_Output/` - Vector embeddings
- `*.pdf`, `*.json`, `*.gguf` - Data files

---

## 📖 Documentation

### Technical Specs
- [AI Role & Coding Standards](./MDFile/AI.MD)
- [Project Requirements](./MDFile/Requirement.md)
- [QA & Pipeline Workflow](./MDFile/TeamDevQA.MD)

### User Guides
- [**How to Run (English)**](./HTMLFile/howtorun.html)
- [**คู่มือการใช้งาน (Thai)**](./HTMLFile/คู่มือการใช้งาน_AI_Scan_PDF.html)
- [**Security Guide**](./SECURITY.md)
- [**Quick Reference**](./QUICKSTART.md)

---

## 🤖 Model Comparison for Thai Language

### Large Language Models (LLM)

| Model | Thai Support | Speed (i5-8500) | RAM | Accuracy |
|-------|-------------|-----------------|-----|----------|
| **unsloth/DeepSeek-R1-Qwen3-8B** | ⭐⭐⭐⭐⭐ Excellent | ~5-8 tok/s | 6-8GB | Best for technical Thai (Your current model) |
| **Qwen2.5-7B** | ⭐⭐⭐⭐ Very Good | ~8-12 tok/s | 5-6GB | Good balance |
| **Llama-3-8B** | ⭐⭐⭐ Limited | ~6-8 tok/s | 6-8GB | Better for English |

### Embedding Models

| Model | Thai Support | Use Case |
|-------|-------------|----------|
| **Qwen/Qwen3-Embedding-0.6B-GGUF** | ⭐⭐⭐⭐⭐ Excellent | Thai + English documents |
| **paraphrase-multilingual** | ⭐⭐⭐⭐ Good | Multi-language support |

**Recommendation for Thai Documents:**
- Use **Qwen3-Embedding-0.6B** for best Thai + English embedding

---

## 🔧 Troubleshooting

### GPT4All API Not Connecting

**Error:** `Error connecting to GPT4All: Connection refused`

**Solution:**
1. Open GPT4All application
2. Go to Settings → Enable "Local API Server"
3. Check port is 4891
4. Restart GPT4All app

### Model Download Fails

**Error:** Model not found in GPT4All

**Solution:**
1. Open GPT4All app
2. Click "Download Models"
3. Search for exact model name
4. If not found, download GGUF manually from HuggingFace

### Out of Memory Error

**Error:** `MemoryError` or system freezes

**Solution:**
1. Close all other applications (browser, Office)
2. Use smaller model (7B instead of 14B)
3. Upgrade RAM to 16GB
4. Restart computer to free memory

### Slow Processing

**Expected Speed on i5-8500:**
- PDF Parsing: ~2 pages/second
- Embedding: ~1-2 chunks/second
- LLM Response: ~3-5 tokens/second (14B model)

**To Improve:**
- Upgrade to 16GB RAM
- Use 7B model instead of 14B
- Close background applications

### Thai Text Display Issues

**Problem:** Thai characters show as ??? or boxes

**Solution:**
1. Ensure terminal supports UTF-8:
   ```bash
   chcp 65001
   ```
2. Use Windows Terminal instead of CMD
3. Install Thai fonts on Windows

---

## 📊 Performance Benchmarks (Optiplex 3070)

### PDF Processing (684 pages total)

| Operation | Time | Output |
|-----------|------|--------|
| Parse PDFs | ~8 minutes | 206 chunks |
| Generate Embeddings | ~3-5 minutes | vector_db.json |
| Query + Response | ~10-20 seconds | Answer |

### Memory Usage

| State | RAM Usage |
|-------|-----------|
| Idle | ~2 GB |
| GPT4All App | ~1 GB |
| GPT4All + 8B Model | ~7-9 GB |
| Full Pipeline Running | ~10-12 GB |

---

## 🌐 GPT4All API Reference

### Endpoints (GPT4All v3.9.0+ - OpenAI Compatible)

**Chat Completions (LLM):**
```bash
POST http://localhost:4891/v1/chat/completions
{
  "model": "qwen3-8b",
  "messages": [{"role": "user", "content": "Your question"}],
  "stream": false,
  "max_tokens": 2000,
  "temperature": 0.2
}
```

**Embeddings:**
```bash
POST http://localhost:4891/v1/embeddings
{
  "model": "Qwen/Qwen3-Embedding-0.6B-GGUF",
  "input": "Text to embed"
}
```

**List Models:**
```bash
GET http://localhost:4891/v1/models
```

### Python Example

```python
import requests

API_BASE = "http://localhost:4891"

# Generate text (Chat Completions)
response = requests.post(
    f"{API_BASE}/v1/chat/completions",
    json={
        "model": "qwen3-8b",
        "messages": [{"role": "user", "content": "สวัสดีครับ"}],
        "stream": False
    }
)
print(response.json()["choices"][0]["message"]["content"])

# Generate embedding
response = requests.post(
    f"{API_BASE}/v1/embeddings",
    json={
        "model": "Qwen/Qwen3-Embedding-0.6B-GGUF",
        "input": "Hello world"
    }
)
print(response.json()["data"][0]["embedding"])
```

---

## 📞 Support & Resources

- **GPT4All Official:** https://gpt4all.io/
- **GPT4All Docs:** https://docs.gpt4all.io/
- **HuggingFace Models:** https://huggingface.co/models?library=gguf
- **Thai NLP (PyThaiNLP):** https://pythainlp.org/

---

## 📝 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.1.0 | 2026-03-20 | **Qwen2.5-0.5B Integration**: Thai language fixes, Windows UTF-8 support, OCR optimization, Ollama backend migration |
| 1.0.0 | 2026-03-19 | GPT4All migration, security agent, enhanced docs |
| 0.9.0 | 2026-01-31 | Initial Ollama-based version |

---

*Created by Qwen3.5 Coder (AI Architect) and Qwen2.5-0.5B (Local LLM) under the direction of Human Owner tps2015gh.*
*Last Updated: 2026-03-20*
*Team: Human Vision + AI Engineering = Local-First Thai PDF Analysis*
