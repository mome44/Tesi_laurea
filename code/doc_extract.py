from docx import Document

NAME = "MASTRO TITTA PìA MOJE"
doc = Document(f"{NAME}.docx")

testo = "\n".join([par.text for par in doc.paragraphs])

with open(f"{NAME}.txt", "w", encoding="utf-8") as f:
    f.write(testo)