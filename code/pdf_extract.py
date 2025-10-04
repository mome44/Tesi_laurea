from pdfminer.high_level import extract_text

pdf_path = "Meo_Patacca_er_Greve_e_Marco_Pepe_la_Cra.pdf"
text = extract_text(pdf_path)

with open("Meo_Patacca_er_Greve_e_Marco_Pepe_la_Cra.txt", "w", encoding="utf-8") as f:
    f.write(text or "")
