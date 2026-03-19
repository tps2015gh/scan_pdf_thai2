# 🧪 Test Agent Guide

## Quick Start

```bash
# Run basic tests
python test_agent.py

# Run full tests (including pipeline)
python test_agent.py --full

# Verbose output
python test_agent.py --verbose
```

---

## What It Tests

### Test 1: File Structure ✓
- All required Python scripts exist
- All required directories exist
- `.gitignore` properly configured

### Test 2: Python Dependencies ✓
- `requests` - HTTP library
- `numpy` - Math operations
- `tqdm` - Progress bars
- `pdfplumber` - PDF parsing
- `pythainlp` - Thai language
- GPT4All API connection

### Test 3: GPT4All API ✓
- Models endpoint (`/v1/models`)
- LLM model availability
- Chat completions (`/v1/chat/completions`)
- Embeddings API (`/v1/embeddings`) - Expected to use fallback

### Test 4: Vector Database ✓
- `vector_db.json` exists
- Valid JSON format
- Chunks loaded
- Embeddings present
- Embedding dimensions

### Test 5: Security Scan ✓
- No sensitive data exposed
- No API keys in code
- No passwords detected
- `.gitignore` comprehensive

### Test 6: Full Pipeline (Optional) ✓
- PDF files present
- Chunks generated
- Embeddings created

---

## Test Results

### Output Example
```
======================================================================
🤖 AI Scan PDF - Test Agent
======================================================================

[Test 1/6] Checking File Structure...
  ✓ File: main.py
  ✓ File: embed_local.py
  ...

[Test 3/6] Testing GPT4All API...
  ✓ GET /v1/models
  ✓ LLM model available
  ✓ POST /v1/chat/completions
  ✓ POST /v1/embeddings (using fallback)

======================================================================
📊 Test Summary
======================================================================

Total Tests: 32
✓ Passed: 31
✗ Failed: 0
⊘ Skipped: 1

✅ All tests passed! System is ready.
```

### Result Colors

- **✓ Green** - Test passed
- **✗ Red** - Test failed
- **⊘ Yellow** - Test skipped

---

## When to Run Tests

### Before First Use
```bash
python test_agent.py --full
```

### After Installation
```bash
python test_agent.py
```

### Before Committing to GitHub
```bash
python security_agent.py
python test_agent.py
```

### When Something Breaks
```bash
python test_agent.py --verbose
```

---

## Understanding Results

### All Tests Passed ✅
```
✅ All tests passed! System is ready.
```
**Meaning:** Everything is working correctly. You can proceed to use the system.

### Some Tests Failed ⚠️
```
⚠️  1 test(s) failed. Please fix issues above.
```
**Meaning:** There's an issue that needs attention. Check the failed test and fix it.

### Common Failures & Fixes

#### 1. GPT4All API Not Accessible
```
✗ GPT4All API accessible: Cannot connect
```
**Fix:**
1. Open GPT4All app
2. Enable API Server (Settings → Local API Server)
3. Make sure port is 4891

#### 2. Model Not Loaded
```
✗ POST /v1/chat/completions: Model not loaded (500)
```
**Fix:**
1. In GPT4All app, click on model
2. Wait for "Loaded" status
3. Try again

#### 3. Vector DB Not Found
```
✗ vector_db.json exists: Not found
```
**Fix:**
```bash
python embed_local.py
```

#### 4. Missing Python Package
```
✗ pdfplumber (PDF parsing): Not installed
```
**Fix:**
```bash
pip install pdfplumber
```

---

## Test Results File

Test results are saved to:
```
Temp_Output/test_results.json
```

**Contents:**
- Timestamp
- Summary (passed/failed/skipped)
- Detailed results for each test

**Example:**
```json
{
  "timestamp": "2026-03-19T18:38:51",
  "summary": {
    "passed": 31,
    "failed": 0,
    "skipped": 1
  },
  "results": [
    {
      "name": "File: main.py",
      "passed": true,
      "message": ""
    },
    ...
  ]
}
```

---

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Tests
on: [push, pull_request]

jobs:
  test:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.8
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
      
      - name: Run tests
        run: |
          python test_agent.py
```

### Pre-commit Hook
```bash
# Add to .git/hooks/pre-commit
#!/bin/bash
python test_agent.py || exit 1
python security_agent.py || exit 1
```

---

## Troubleshooting

### Test Agent Won't Run
```bash
# Check Python version
python --version

# Check if file exists
dir test_agent.py

# Try with full path
python C:\path\to\test_agent.py
```

### Tests Hang
```bash
# Add timeout
timeout 60 python test_agent.py

# Run with verbose to see where it hangs
python test_agent.py --verbose
```

### False Positives
If a test fails but shouldn't have:
1. Check the error message
2. Verify the requirement is actually met
3. Update the test if needed (in `test_agent.py`)

---

## Performance Benchmarks

### Expected Test Duration

| Test | Time |
|------|------|
| File Structure | < 1 second |
| Dependencies | < 2 seconds |
| GPT4All API | 5-10 seconds |
| Vector DB | < 1 second |
| Security Scan | 5-10 seconds |
| Full Pipeline | 30-60 seconds |

**Total (without --full):** ~15-25 seconds

---

## Related Tools

- **`security_agent.py`** - Security scanner (run before committing)
- **`test_gpt4all.py`** - GPT4All connection tester (quick check)
- **`main.py`** - Main query interface

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-03-19 | Initial release |

---

**Last Updated:** 2026-03-19
**Author:** AI Test Agent
