# setup_project.ps1
# Script to set up the Python virtual environment and install dependencies for AI-Scan-PDF.

param()

$ProjectDir = Get-Location
$VenvDir = Join-Path $ProjectDir ".venv"
$ActivateScript = Join-Path $VenvDir "Scripts\Activate.ps1"

# --- 1. Create Virtual Environment if it doesn't exist ---
if (-not (Test-Path $VenvDir)) {
    Write-Host "[INFO] Creating virtual environment in '$VenvDir'..."
    python -m venv $VenvDir
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment. Ensure Python is installed and in your PATH."
        exit 1
    }
    Write-Host "[SUCCESS] Virtual environment created."
} else {
    Write-Host "[INFO] Virtual environment already exists at '$VenvDir'."
}

# --- 2. Activate Virtual Environment ---
Write-Host "[INFO] Activating virtual environment..."
# Check if the activation script exists
if (-not (Test-Path $ActivateScript)) {
    Write-Error "Activation script not found at '$ActivateScript'. Please check your virtual environment setup."
    exit 1
}

# Attempt to activate. Note: Execution policy might require admin rights for the first time.
# If activation fails due to policy, refer to previous instructions (Run PowerShell as Admin).
try {
    . $ActivateScript
    Write-Host "[SUCCESS] Virtual environment activated."
} catch {
    Write-Error "Failed to activate virtual environment. Error: $($_.Exception.Message)"
    Write-Host "Try running PowerShell as Administrator and executing 'Set-ExecutionPolicy RemoteSigned -Scope CurrentUser' if you haven't already."
    exit 1
}

# --- 3. Install Project Dependencies ---
Write-Host "`n[INFO] Installing project dependencies..."
# List of core dependencies for AI-Scan-PDF
$Dependencies = @(
    "pdfplumber",
    "pythainlp",
    "tqdm",
    "requests",
    "numpy",
    "fitz", # PyMuPDF
    "easyocr",
    "Pillow",
    "markdown"
)

# Install dependencies
foreach ($dep in $Dependencies) {
    Write-Host "  - Installing $dep..."
    pip install $dep
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to install $dep. Please check the output for errors."
        # Optionally exit here or try to continue
    }
}

Write-Host "[SUCCESS] Project dependencies installed successfully."

# --- 4. Final Verification and Instructions ---
Write-Host "`n======================================================================"
Write-Host "🚀 Project Setup Complete!"
Write-Host "======================================================================"
Write-Host "Virtual environment is active and dependencies are installed."
Write-Host "You can now run the project scripts."
Write-Host ""
Write-Host "To run the main application, use:"
Write-Host "  python main.py"
Write-Host ""
Write-Host "To run the HTML server, use:"
Write-Host "  python serve_html.py"
Write-Host ""
Write-Host "[IMPORTANT] To deactivate the virtual environment, simply close this PowerShell window or run: deactivate"
Write-Host "======================================================================"
