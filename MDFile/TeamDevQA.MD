# Workflow: Local-First AI Pipeline

## 1. Data Ingestion (Python-Led)
- **Script A:** `parse_and_chunk.py` -> อ่าน PDF และแบ่งข้อมูลเป็นชิ้นเล็กๆ (Chunks).
- **Script B:** `embed_local.py` -> แปลงข้อความเป็น Vector โดยใช้โมเดลขนาดเล็ก (เช่น `all-MiniLM-L6-v2`) รันบน CPU 3070 ได้สบาย.

## 2. The Inference Loop (Cost = $0)
- **Step 1:** เมื่อ User ถามคำถาม, Python จะค้นหา Chunk ที่เกี่ยวข้องจาก Local Vector DB.
- **Step 2:** สร้าง Prompt ที่มีเฉพาะเนื้อหาที่จำเป็น (Context Injection).
- **Step 3:** ส่งให้ **Qwen-CLI** หรือ **Ollama** ประมวลผลในเครื่อง.

## 3. High-Level Analysis (Optional Cloud)
- หาก Local LLM วิเคราะห์โครงสร้างระบบที่ซับซ้อนไม่ได้ (Low Confidence), Python Script จะส่ง "เฉพาะก้อนเนื้อหาที่ติดปัญหา" ไปที่ **Gemini-CLI** เพื่อประหยัด Token สูงสุด.

## 4. Quality Control
- **Output Validation:** ตรวจสอบว่า Code ที่ AI เจนออกมาจาก Spec มี Syntax ที่ถูกต้อง (Auto-linting).