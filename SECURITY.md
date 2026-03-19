# 🔒 Security Guide - AI Scan PDF Project

## Overview

This project includes a comprehensive security system to prevent accidental data leaks when uploading to GitHub.

## 🛡️ Security Components

### 1. `.gitignore` - First Line of Defense

Automatically ignores:
- **Input Data**: `PDF_Input/`, `*.pdf`
- **Output Data**: `Temp_Output/`, `LearningDb_Output/`, `chunks/`
- **Databases**: `vector_db.json`, `*.embeddings.json`
- **Models**: `*.gguf`, `*.bin`
- **Secrets**: `.env`, `*.key`, `credentials.json`
- **Python**: `__pycache__/`, `*.pyc`, `venv/`

### 2. `security_agent.py` - AI Security Scanner

Scans for potential data leaks:

**Detects:**
- API keys and tokens
- Passwords and secrets
- Private keys and certificates
- Database connection strings
- Email addresses
- Thai phone numbers
- Thai ID card numbers
- AWS credentials
- Internal IP addresses

**Usage:**
```bash
# Basic scan
python security_agent.py

# Strict mode (more aggressive)
python security_agent.py --strict

# Scan specific path
python security_agent.py --path /path/to/project
```

**Severity Levels:**
- 🔴 **CRITICAL**: Private keys, AWS credentials
- 🟠 **HIGH**: API keys, passwords, Thai ID cards
- 🟡 **MEDIUM**: Emails, phone numbers
- 🔵 **LOW**: Internal IP addresses

### 3. `pre_commit_hook.py` - Pre-commit Protection

Runs security check before every git commit.

**Installation:**
```bash
# Copy to git hooks directory
copy pre_commit_hook.py .git\hooks\pre-commit

# Or create a symlink (Git Bash)
ln -s ../../pre_commit_hook.py .git/hooks/pre-commit
```

**Manual bypass (NOT recommended):**
```bash
git commit --no-verify
```

## 📋 Security Checklist Before Upload

- [ ] Run `python security_agent.py` - should show ✅
- [ ] Verify `.gitignore` exists
- [ ] Check `PDF_Input/` is empty or ignored
- [ ] Confirm no `vector_db.json` in root
- [ ] Ensure no `.env` files with secrets
- [ ] Review any HIGH/CRITICAL issues

## 🔧 Fixing Security Issues

### Issue: Files not in .gitignore
**Solution:** Add to `.gitignore`:
```
# Example
sensitive_folder/
*.pdf
```

### Issue: API keys in code
**Solution:** Use environment variables:
```python
# ❌ Bad
api_key = "sk-1234567890abcdef"

# ✅ Good
import os
api_key = os.getenv("API_KEY")
```

### Issue: Database credentials
**Solution:** Use `.env` file (ignored):
```bash
# .env (add to .gitignore!)
DATABASE_URL=mongodb://localhost:27017
```

```python
# Code
import os
db_url = os.getenv("DATABASE_URL")
```

## 📊 Security Scan Report Example

```
============================================================
🔒 AI Security Agent - Data Leak Checker
============================================================

[*] Checking for critical files...
[*] Checking for critical directories...
  ✓ PDF_Input/ is properly ignored
  ✓ Temp_Output/ is properly ignored
[*] Scanning code for secrets...
[*] Checking .gitignore configuration...
  ✓ .gitignore is properly configured

============================================================
📊 Security Scan Report
============================================================

Files scanned: 428
Issues found: 0

✅ No security issues found! Safe to commit.
```

## 🚨 What To Do If You Find a Leak

1. **DO NOT COMMIT** - Stop immediately
2. Run `python security_agent.py` to identify the issue
3. Remove or mask the sensitive data
4. If already committed:
   ```bash
   # Remove from git history (careful!)
   git filter-branch --force --index-filter \
     "git rm --cached --ignore-unmatch PATH_TO_FILE" \
     --prune-empty --tag-name-filter cat -- --all
   
   # Force push (rewrites history)
   git push origin --force --all
   ```
5. Rotate any exposed credentials immediately

## 📁 Safe Files for GitHub

These files are **safe** to upload:
- ✅ `*.py` (source code without secrets)
- ✅ `README.md`, `*.md` (documentation)
- ✅ `HTMLFile/` (user guides)
- ✅ `MDFile/` (technical specs)
- ✅ `.gitignore`
- ✅ `LICENSE`
- ✅ `security_agent.py`, `pre_commit_hook.py`

## 📁 Never Upload These

These files are **never** safe to upload:
- ❌ `PDF_Input/*.pdf` (source documents)
- ❌ `LearningDb_Output/` (embeddings)
- ❌ `Temp_Output/` (processed data)
- ❌ `vector_db.json` (vector database)
- ❌ `*.gguf` (model files)
- ❌ `.env` (environment secrets)
- ❌ `credentials.json` (authentication)

## 🔄 Continuous Security

Run security checks:
- **Before every commit**: `python pre_commit_hook.py`
- **Before pushing**: `python security_agent.py --strict`
- **Weekly audit**: Full scan with manual review

---

**Created by:** AI Security Agent
**Version:** 1.0.0
**Last Updated:** 2026-03-19
