from pdfminer.high_level import extract_text

NAME ="pitre_fiabe_novelle_e_racconti_2"

pdf_path = f"{NAME}.pdf"
text = extract_text(pdf_path)
 
with open(f"{NAME}.txt", "w", encoding="utf-8") as f:
    f.write(text or "")
