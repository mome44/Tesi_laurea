from pdf2image import convert_from_path
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
NAME ="er-teatro-de-prosa-13394"


# Converte le pagine del PDF in immagini
pages = convert_from_path(f"{NAME}.pdf")

testo_completo = ""

for page_number, page in enumerate(pages):
    # Applica OCR alla pagina
    text = pytesseract.image_to_string(page, lang='eng')  # usa 'eng' per inglese
    testo_completo += f"\n{text}"

# Salva in un file
with open(f"{NAME}.txt", "w", encoding="utf-8") as f:
    f.write(testo_completo)

print("OCR completato! Testo salvato in output.txt")