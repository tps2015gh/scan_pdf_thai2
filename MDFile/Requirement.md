# Project: Local-Inference PDF Spec Analyzer
## Hardware Constraints (Optiplex 3070)
- **Target:** 7B-Parameter Models (Qwen2.5-Coder-7B or Llama-3-8B).
- **Optimization:** Use **GGUF Format** with `llama-cpp-python` for CPU/iGPU acceleration.
- **Inference Library:** `llama-cpp-python` or `Ollama API` via Python.

## Functional Requirements
1. **Dynamic Prompting:** Python script must merge `System_Prompt`, `Context_Chunk`, and `User_Query`.
2. **Context Window Management:** Implement a sliding window or summary-based attention to prevent RAM overflow.
3. **Extraction Engine:** `pdfplumber` for text/tables; `EasyOCR` for Thai image-text.

เทคนิคพิเศษสำหรับ Optiplex 3070 (Windows 11)
เนื่องจากคุณใช้ Windows 11 ผมแนะนำให้ติดตั้ง WSL2 (Ubuntu) ครับ เพราะจะรันเครื่องมือจำพวก marker (สำหรับแปลง PDF เป็น Markdown) และ Ollama ได้เสถียรกว่าในฝั่ง Windows เปล่าๆ

ตัวอย่างการใช้งานผ่าน CLI แบบประหยัด Token:
เขียน Python Script สำหรับ "ตัดแบ่ง PDF ออกเป็นไฟล์ Markdown ย่อยๆ (Chunking)" เพื่อเตรียมไว้ใช้กับ CLI เหล่านี้เลยไหมครับ? (วิธีนี้จะช่วยให้คุณเลือกส่งเฉพาะส่วนที่ต้องการเข้า AI ได้แม่นยำมาก)

โปรแกรมจะต้อง แสดงสถานะให้ดูด้วยตลอดการทำงาน