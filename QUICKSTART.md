# Quick Reference - AI Scan PDF Project

## 🚀 Quick Start

```bash
# 1. Start GPT4All v3.9.0 with API Server enabled
# 2. Parse PDFs to chunks
python parse_and_chunk.py

# 3. Generate embeddings
python embed_local.py

# 4. Query documents
python main.py
```

## 📁 Directory Structure

```
ai_scan_pdf/
├── PDF_Input/           [IGNORED] Place your PDFs here
├── Temp_Output/         [IGNORED] Chunks & intermediate files
├── LearningDb_Output/   [IGNORED] Vector database
├── MDFile/              Documentation (safe to upload)
├── HTMLFile/            User guides (safe to upload)
├── chunks/              [IGNORED] Text chunks (legacy)
├── .gitignore           Git ignore rules
├── security_agent.py    Security scanner
├── pre_commit_hook.py   Pre-commit check
└── *.py                 Main scripts
```

## 🔒 Security Commands

```bash
# Scan for data leaks
python security_agent.py

# Install pre-commit hook
copy pre_commit_hook.py .git\hooks\pre-commit

# Check before commit
python pre_commit_hook.py
```

## 📊 GPT4All Setup

**Models Required:**
- LLM: `deepseek-r1-distill-qwen-14b` (or similar 14B)
- Embedding: `all-MiniLM-L6-v2`

**API Server:** `http://localhost:4891`

## ✅ Safe to Upload to GitHub

- ✅ Source code (`*.py`)
- ✅ Documentation (`*.md`, `HTMLFile/`)
- ✅ Configuration (`.gitignore`, `LICENSE`)
- ✅ Security tools (`security_agent.py`)

## ❌ Never Upload

- ❌ PDF files (`PDF_Input/`, `*.pdf`)
- ❌ Vector databases (`vector_db.json`, `LearningDb_Output/`)
- ❌ Chunks (`chunks/`, `Temp_Output/`)
- ❌ Model files (`*.gguf`, `*.bin`)
- ❌ Secrets (`.env`, `credentials.json`)

## 🛠️ Troubleshooting

| Issue | Solution |
|-------|----------|
| GPT4All API not connecting | Ensure GPT4All app is running with API server enabled |
| Model not found | Download models in GPT4All app settings |
| Embedding fails | Check `all-MiniLM-L6-v2` is loaded |
| Security scan fails | Run `python security_agent.py` and fix issues |

## 📞 Support Files

- `SECURITY.md` - Detailed security guide
- `README.md` - Project overview
- `MDFile/AI.MD` - AI coding standards
- `MDFile/Requirement.md` - Requirements
- `MDFile/TeamDevQA.MD` - Workflow documentation

---
**Version:** 1.0.0 | **Updated:** 2026-03-19
