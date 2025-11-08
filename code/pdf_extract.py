from pdfminer.high_level import extract_text

NAME ="MARTOGLIO Nino__Voculanzicula__null__U(10)-D(2)__Commedia__3a"

pdf_path = f"{NAME}.pdf"
text = extract_text(pdf_path)
 
with open(f"{NAME}.txt", "w", encoding="utf-8") as f:
    f.write(text or "")
