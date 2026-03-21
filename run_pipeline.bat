@echo off
REM Batch file to run the data processing pipeline: parsing and embedding.

echo Activating virtual environment...
call .\.venv\Scripts\activate.bat

IF %ERRORLEVEL% NEQ 0 (
    echo Error: Failed to activate virtual environment.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo --- Starting PDF Parsing and Chunking (parse_and_chunk.py) ---
python parse_and_chunk.py

IF %ERRORLEVEL% NEQ 0 (
    echo Error: PDF parsing and chunking failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo --- Starting Embedding Vector Generation (embed_local.py) ---
python embed_local.py

IF %ERRORLEVEL% NEQ 0 (
    echo Error: Embedding vector generation failed.
    pause
    exit /b %ERRORLEVEL%
)

echo.
echo --- Data Processing Pipeline Complete ---
pause
