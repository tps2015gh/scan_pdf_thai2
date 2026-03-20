import fitz  # PyMuPDF
import os
import gc
import json
import easyocr
import numpy as np
from PIL import Image
from tqdm import tqdm

def ocr_pdf_page(page, reader):
    # Render page to image (pixmap)
    pix = page.get_pixmap(matrix=fitz.Matrix(2, 2)) # 2x zoom for better OCR
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Run OCR (Thai and English)
    result = reader.readtext(np.array(img), detail=0)
    return " ".join(result)

def main():
    pdf_path = os.path.join("PDF_Input", "your_scanned_document.pdf")
    # Replace "your_scanned_document.pdf" with the actual filename of your scanned PDF.
    # Ensure this file is placed in the 'PDF_Input' directory.
    if not os.path.exists(pdf_path):
        print(f"[!] File not found: {pdf_path}")
        return

    # Output to Temp_Output
    output_dir = "Temp_Output"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    output_file = os.path.join(output_dir, "ocr_test_output.txt")

    print("[*] Initializing EasyOCR (Thai, English)...")
    # This might take time and memory on 32-bit
    try:
        reader = easyocr.Reader(['th', 'en'], gpu=False)
    except Exception as e:
        print(f"[!] Error initializing OCR: {e}")
        return

    doc = fitz.open(pdf_path)
    # Just process first 2 pages for proof of concept due to 32-bit limits
    limit = min(2, len(doc))
    print(f"[*] Processing first {limit} pages with OCR...")

    all_text = ""
    for i in range(limit):
        print(f"[*] OCR-ing Page {i+1}...")
        page_text = ocr_pdf_page(doc[i], reader)
        all_text += f"\n--- Page {i+1} ---\n{page_text}\n"
        gc.collect()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(all_text)

    print(f"[+] OCR results saved to {output_file}")

if __name__ == "__main__":
    main()
