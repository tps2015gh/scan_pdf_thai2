# 🚀 How to Run - AI Scan PDF (Ollama Edition)

## 📋 Quick Start Checklist

- [ ] **Ollama** installed and running
- [ ] Models pulled in Ollama (`qwen3.5:0.8b`, `nomic-embed-text`)
- [ ] Python virtual environment (`.venv`) created and activated
- [ ] PDF files in `PDF_Input/` folder
- [ ] Python dependencies installed within the virtual environment

---

## Step 1: Set up Python Environment (Virtual Environment)

Using a virtual environment (`venv`) is highly recommended to isolate project dependencies and avoid conflicts.

### 1.1 Create Virtual Environment
Open your **PowerShell terminal** (you might need to run it as Administrator for the first-time activation, as per previous instructions) in your project directory (`C:\dev\scan_pdf_thai\`).
```powershell
# Navigate to project directory if you're not already there
# cd C:\dev\scan_pdf_thai\

# Create the virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "[SUCCESS] Virtual environment '.venv' created."
} else {
    Write-Host "[INFO] Virtual environment '.venv' already exists."
}
```

### 1.2 Activate Virtual Environment
```powershell
.\.venv\Scripts\Activate.ps1
```
*   If you encounter an error related to script execution policy, you may need to run PowerShell as Administrator and execute `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser`, then try activating again in your regular terminal.
*   Once activated, your terminal prompt will change to `(.venv) PS C:\dev\scan_pdf_thai>`.

---

## Step 2: Install & Setup Ollama

### 2.1 Download
1.  Go to: https://ollama.com/
2.  Download and install Ollama for Windows.

### 2.2 Pull Models
Open your **activated** PowerShell terminal (it should show `(.venv)` in the prompt) and run:
```powershell
ollama pull qwen3.5:0.8b
ollama pull nomic-embed-text
```

### 2.3 Keep Ollama Running
Ollama typically runs in the background as a system service or tray icon. Ensure it is active before running the Python scripts.

---

## Step 3: Install Project Dependencies

**Ensure your virtual environment is active** (prompt starts with `(.venv)`).
```powershell
pip install pdfplumber pythainlp tqdm requests numpy fitz easyocr Pillow markdown
```
This installs all necessary libraries for the project within the isolated environment.

---

## Step 4: Configure Backend (Optional)

Check `config.json` to ensure it points to Ollama:
```json
"backend": {
  "type": "ollama",
  "api_base_url": "http://localhost:11434"
}
```
*(This should already be set correctly from previous steps.)*

---

## Step 5: Run the Pipeline

**Ensure your virtual environment is active** (`(.venv)` prompt).

### 5.1 Parse PDFs to Chunks
```powershell
python parse_and_chunk.py
```
This breaks your PDFs into manageable text pieces. Place your PDF files in the `PDF_Input/` folder before running this.

### 5.2 Generate Embeddings
```powershell
python embed_local.py
```
This uses `nomic-embed-text` via Ollama to create a searchable vector database.

### 5.3 Query Your Documents
```powershell
python main.py
```
Ask questions about your documents in Thai or English.

---

## 💻 Hardware Optimization (4GB RAM)

If you are using a 4GB RAM notebook:
1.  **Close all other apps:** Chrome, Edge, and Office consume a lot of RAM.
2.  **Use Small Models:** `qwen3.5:0.8b` is specifically chosen for low RAM usage.
3.  **Patience:** The first query might take a few seconds as the model loads into RAM.

---

## 🔧 Troubleshooting

### Error: Cannot activate virtual environment (`.\.venv\Scripts\Activate.ps1`)
**Solution:** Ensure you have run `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` in an Administrator PowerShell at least once. Then try activating again in a regular PowerShell terminal.

### Error: Ollama Connection refused
**Solution:** Ensure Ollama is running. Check `http://localhost:11434` in your browser.

### Error: Model not found
**Solution:** Run `ollama pull qwen3.5:0.8b` and `ollama pull nomic-embed-text` again in your terminal.

### Error: Out of memory
**Solution:** Close all browsers and other applications. Use the recommended `qwen3.5:0.8b` model.

---

*Last Updated: 2026-03-20*
