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

def main():
    files = [
        "DOL_FSS_Index.1เอกสารสรุปความต้องการของผู้ใช้งาน_20260131_v2.5.pdf",
        "DOL_FSS_Index.2เอกสารSRS_202600202_2.6.pdf"
    ]

    input_dir = "PDF_Input"
    output_base_dir = os.path.join("Temp_Output", "chunks")

    for pdf_file in files:
        pdf_path = os.path.join(input_dir, pdf_file)
        if not os.path.exists(pdf_path):
            print(f"[!] File not found: {pdf_path}")
            continue

        text = parse_pdf(pdf_path)
        # Simple chunking: 2000 tokens roughly ~ 4000-6000 chars
        # The AI.MD says 2,000 tokens for context optimization
        chunks = chunk_text(text, chunk_size=4000, chunk_overlap=500)

        # Get clean filename without path and extension
        base_name = os.path.splitext(pdf_file)[0]
        save_chunks(chunks, os.path.join(output_base_dir, base_name), base_name)

if __name__ == "__main__":
    main()
