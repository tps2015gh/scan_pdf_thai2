#!/usr/bin/env python3
"""
Create a sample Thai text PDF for testing the AI Scan PDF system.
This creates a text-based PDF (not scanned) for accurate Thai text extraction.
"""

from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.units import cm
import os

# Sample Thai content (HR/Policy document style)
THAI_CONTENT = """
เอกสารนโยบายบริษัท
====================

1. วัตถุประสงค์
เอกสารนี้จัดทำขึ้นเพื่อกำหนดนโยบายและแนวปฏิบัติสำหรับพนักงานทุกคนในองค์กร

2. ขอบเขตการบังคับใช้
นโยบายนี้ใช้กับพนักงานทุกคน ตั้งแต่ระดับปฏิบัติการจนถึงผู้บริหาร

3. เวลาทำงาน
- วันทำงาน: วันจันทร์ ถึง วันศุกร์
- เวลาทำงาน: 09:00 - 18:00 น.
- พักกลางวัน: 12:00 - 13:00 น.

4. การลา
พนักงานมีสิทธิ์ลาได้ดังนี้:
- ลากิจ: ไม่เกิน 6 วันทำการต่อปี
- ลาป่วย: ไม่เกิน 30 วันทำการต่อปี
- ลาพักร้อน: 10 วันทำการต่อปี (หลังจากทำงานครบ 1 ปี)

5. สวัสดิการ
- ประกันสุขภาพกลุ่ม
- กองทุนสำรองเลี้ยงชีพ
- โบนัสประจำปี (ตามผลการดำเนินงาน)

6. การประเมินผล
พนักงานจะได้รับการประเมินผลปีละ 2 ครั้ง:
- ครึ่งปีแรก (มกราคม - มิถุนายน)
- ครึ่งปีหลัง (กรกฎาคม - ธันวาคม)

7. ข้อควรปฏิบัติ
- แต่งกายสุภาพเรียบร้อย
- มาทำงานตรงเวลา
- เคารพกฎระเบียบของบริษัท

8. ติดต่อสอบถาม
หากมีข้อสงสัย ติดต่อแผนกทรัพยากรบุคคล
อีเมล: hr@company.co.th
โทรศัพท์: 02-XXX-XXXX

---
เอกสารนี้เผยแพร่เมื่อ: มีนาคม 2569
"""

def create_thai_pdf(output_path):
    """Create a simple Thai text PDF using built-in fonts."""
    
    print(f"[*] Creating Thai PDF: {output_path}")
    
    # Create PDF
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    
    # Since we don't have Thai fonts installed, we'll create a simple PDF
    # with English description that simulates a Thai document structure
    # This is for testing the extraction pipeline
    
    y = height - 2*cm
    
    # Title
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width/2, y, "Company Policy Document")
    y -= 1*cm
    
    # Subtitle (Thai transliteration for testing)
    c.setFont("Helvetica", 12)
    c.drawCentredString(width/2, y, "(Ekkasan NAYOBAY BORISAT - Policy Document)")
    y -= 1.5*cm
    
    # Content sections
    c.setFont("Helvetica", 11)
    
    sections = [
        "1. OBJECTIVE (WATTHU PRASONG)",
        "This document establishes policies and guidelines for all employees.",
        "",
        "2. SCOPE (KHOB KHET)",
        "This policy applies to all employees from operational to executive levels.",
        "",
        "3. WORKING HOURS (WELA THAMNGAN)",
        "- Work days: Monday to Friday",
        "- Working hours: 09:00 - 18:00",
        "- Lunch break: 12:00 - 13:00",
        "",
        "4. LEAVE ENTITLEMENT (KAN LA)",
        "- Personal leave: Up to 6 days per year",
        "- Sick leave: Up to 30 days per year", 
        "- Annual leave: 10 days per year (after 1 year)",
        "",
        "5. BENEFITS (SAWATDIKAN)",
        "- Group health insurance",
        "- Provident fund",
        "- Annual bonus (based on performance)",
        "",
        "6. PERFORMANCE REVIEW (KAN PRAMEIN PHON)",
        "Employees will be reviewed twice a year:",
        "- First half (January - June)",
        "- Second half (July - December)",
        "",
        "7. CODE OF CONDUCT (KHO KHUAN PRACTI)",
        "- Dress professionally",
        "- Arrive on time",
        "- Respect company rules",
        "",
        "8. CONTACT (TID TOR THAMTHAM)",
        "For inquiries, contact Human Resources Department",
        "Email: hr@company.co.th",
        "Phone: 02-XXX-XXXX",
        "",
        "---",
        "Document published: March 2026 (MINAKHOM 2569)",
    ]
    
    for line in sections:
        if y < 2*cm:  # New page if needed
            c.showPage()
            y = height - 2*cm
            c.setFont("Helvetica", 11)
        
        if line == "":
            y -= 0.3*cm
        elif line.startswith("---"):
            y -= 0.5*cm
            c.setFont("Helvetica-Oblique", 10)
            c.drawString(2*cm, y, line)
            c.setFont("Helvetica", 11)
        else:
            c.drawString(2*cm, y, line)
            y -= 0.6*cm
    
    # Save PDF
    c.save()
    print(f"[+] Created: {output_path}")
    print(f"[+] Pages: 1")
    return True

def create_thai_pdf_with_unicode(output_path):
    """
    Create a PDF with actual Thai Unicode text.
    Requires a Thai font file (e.g., sarabun.ttf, freeserif.ttf)
    """
    # Search for Thai fonts on the system
    thai_fonts = [
        "fonts/THSarabunNew.ttf",
        "fonts/Sarabun-Regular.ttf", 
        "C:/Windows/Fonts/tahoma.ttf",  # Tahoma supports Thai
        "C:/Windows/Fonts/leelawadee.ttf",  # Leelawadee (Windows Thai font)
    ]
    
    font_path = None
    for fp in thai_fonts:
        if os.path.exists(fp):
            font_path = fp
            break
    
    if not font_path:
        print("[!] No Thai font found. Creating English version instead.")
        return create_thai_pdf(output_path)
    
    print(f"[*] Using Thai font: {font_path}")
    
    # Register the font
    try:
        pdfmetrics.registerFont(TTFont('ThaiFont', font_path))
    except Exception as e:
        print(f"[!] Font registration failed: {e}")
        return create_thai_pdf(output_path)
    
    # Create PDF with Thai text
    c = canvas.Canvas(output_path, pagesize=A4)
    width, height = A4
    y = height - 2*cm
    
    c.setFont("ThaiFont", 16)
    c.drawCentredString(width/2, y, "เอกสารนโยบายบริษัท")
    y -= 1.5*cm
    
    c.setFont("ThaiFont", 12)
    
    for line in THAI_CONTENT.strip().split('\n'):
        if y < 2*cm:
            c.showPage()
            y = height - 2*cm
            c.setFont("ThaiFont", 12)
        
        if line.strip() == "":
            y -= 0.5*cm
        elif line.startswith("="):
            y -= 0.5*cm
        else:
            c.drawString(2*cm, y, line.strip())
            y -= 0.7*cm
    
    c.save()
    print(f"[+] Created with Thai Unicode: {output_path}")
    return True

if __name__ == "__main__":
    output_dir = "PDF_Input"
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, "thai_policy_sample.pdf")
    
    # Try to create with Thai Unicode, fallback to English
    create_thai_pdf_with_unicode(output_path)
    
    print("\n[+] Sample PDF created successfully!")
    print("[+] Run 'python parse_and_chunk.py' to test extraction")
