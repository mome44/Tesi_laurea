from pdfminer.high_level import extract_text

NAME ="PASOLINI Pier Paolo__Il vantone di Plauto__null__(13)__Commedia__5a"

pdf_path = f"{NAME}.pdf"
text = extract_text(pdf_path)
 
with open(f"{NAME}.txt", "w", encoding="utf-8") as f:
    f.write(text or "")
