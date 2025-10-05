from pdfminer.high_level import extract_text

NAME ="Benedetto-fra-le-donne-Copioni"

pdf_path = f"{NAME}.pdf"
text = extract_text(pdf_path)
 
with open(f"{NAME}.txt", "w", encoding="utf-8") as f:
    f.write(text or "")
