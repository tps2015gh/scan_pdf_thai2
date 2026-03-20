import pdfplumber
import os
import re
import gc
from pythainlp.util import normalize
from pythainlp.tokenize import word_tokenize
from tqdm import tqdm

def normalize_thai(text):
    if not text:
        return ""
    return normalize(text)

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    chunks = []
    # Simple split by newline or sentences
    # For better chunking, we could use LangChain's RecursiveCharacterTextSplitter
    # But let's do a simple one first to avoid extra dependencies if possible
    
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - chunk_overlap)
        
    return chunks

def parse_pdf(pdf_path):
    print(f"[*] Parsing PDF: {pdf_path}")
    all_text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in tqdm(pdf.pages, desc="Extracting pages"):
            text = page.extract_text()
            if text:
                all_text += normalize_thai(text) + "\n"
            
            # Memory safety as per AI.MD
            del page
            gc.collect()
            
    return all_text

def save_chunks(chunks, output_dir, base_name):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, chunk in enumerate(chunks):
        file_path = os.path.join(output_dir, f"{base_name}_chunk_{i+1}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk)

    print(f"[+] Saved {len(chunks)} chunks to {output_dir}")

import pdfplumber
import os
import re
import gc
from pythainlp.util import normalize
from pythainlp.tokenize import word_tokenize
from tqdm import tqdm
import json

# Try PyMuPDF for OCR fallback (import as pymupdf to avoid conflicts)
try:
    import pymupdf as fitz
    HAS_PYMUPDF = True
except ImportError:
    HAS_PYMUPDF = False

try:
    import easyocr
    import numpy as np
    from PIL import Image
    HAS_EASYOCR = True
except ImportError:
    HAS_EASYOCR = False

# Global OCR reader (lazy loaded)
ocr_reader = None

def get_ocr_reader():
    global ocr_reader
    if ocr_reader is None:
        print("[*] Initializing EasyOCR (Thai only, optimized for speed)...")
        # Optimized for CPU speed
        ocr_reader = easyocr.Reader(
            ['th'],  # Thai only (faster than ['th', 'en'])
            gpu=False,
            quantized=True  # Use quantized models if available
        )
    return ocr_reader

def load_config():
    config_file = "config.json"
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {}

CONFIG = load_config()

def normalize_thai(text):
    if not text:
        return ""
    return normalize(text)

def chunk_text(text, chunk_size=1000, chunk_overlap=200):
    chunks = []
    start = 0
    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]
        chunks.append(chunk)
        start += (chunk_size - chunk_overlap)
        
    return chunks

def ocr_page_with_pymupdf(page, reader):
    """Extract text from a page using OCR (for scanned PDFs)."""
    if not HAS_PYMUPDF:
        return ""
    # Use 1.5x zoom instead of 2x (faster, slight quality trade-off)
    pix = page.get_pixmap(matrix=fitz.Matrix(1.5, 1.5))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    # batch_size=1 for memory efficiency on CPU
    result = reader.readtext(np.array(img), detail=0, batch_size=1)
    return " ".join(result)

def parse_pdf(pdf_path):
    print(f"[*] Parsing PDF: {pdf_path}")
    all_text = ""
    use_ocr_fallback = False
    
    # First try normal text extraction
    with pdfplumber.open(pdf_path) as pdf:
        for page in tqdm(pdf.pages, desc="Extracting pages"):
            text = page.extract_text()
            if text:
                all_text += normalize_thai(text) + "\n"
            else:
                use_ocr_fallback = True
            
            del page
            gc.collect()
    
    # If no text extracted, use OCR
    if use_ocr_fallback or len(all_text.strip()) < 100:
        print("[!] Little/no text extracted. Trying OCR fallback...")
        if not HAS_PYMUPDF or not HAS_EASYOCR:
            print("[!] OCR libraries not available. Install with: pip install pymupdf easyocr")
            return all_text
            
        all_text = ""
        reader = get_ocr_reader()
        
        doc = fitz.open(pdf_path)
        for i, page in enumerate(tqdm(doc, desc="OCR pages")):
            page_text = ocr_page_with_pymupdf(page, reader)
            all_text += f"\n--- Page {i+1} ---\n{normalize_thai(page_text)}\n"
            gc.collect()
        doc.close()

    return all_text

def save_chunks(chunks, output_dir, base_name):
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    for i, chunk in enumerate(chunks):
        file_path = os.path.join(output_dir, f"{base_name}_chunk_{i+1}.md")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(chunk)

    print(f"[+] Saved {len(chunks)} chunks to {output_dir}")

def main():
    input_dir = CONFIG.get('paths', {}).get('pdf_input', 'PDF_Input')
    output_base_dir = CONFIG.get('paths', {}).get('chunks', os.path.join('Temp_Output', 'chunks'))

    # Ensure input directory exists
    if not os.path.exists(input_dir):
        print(f"[!] Input directory not found: {input_dir}. Please create it and add PDFs.")
        return

    pdf_files = [f for f in os.listdir(input_dir) if f.lower().endswith('.pdf')]
    if not pdf_files:
        print(f"[!] No PDF files found in {input_dir}. Please add PDFs to process.")
        return

    for pdf_file_name in pdf_files:
        pdf_path = os.path.join(input_dir, pdf_file_name)
        print(f"[*] Processing {pdf_file_name}...")
        
        text = parse_pdf(pdf_path)
        chunk_size = CONFIG.get('parsing', {}).get('chunk_size', 4000)
        chunk_overlap = CONFIG.get('parsing', {}).get('chunk_overlap', 500)
        chunks = chunk_text(text, chunk_size=chunk_size, chunk_overlap=chunk_overlap)

        base_name = os.path.splitext(pdf_file_name)[0]
        save_chunks(chunks, os.path.join(output_base_dir, base_name), base_name)
    
    print("\n[+] PDF parsing and chunking complete.")

if __name__ == "__main__":
    main()
