from pdfminer.high_level import extract_text

NAME ="saint_exupery_il_piccolo_principe"

pdf_path = f"{NAME}.pdf"
text = extract_text(pdf_path)
 
with open(f"{NAME}.txt", "w", encoding="utf-8") as f:
    f.write(text or "")
