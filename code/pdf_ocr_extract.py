from pdf2image import convert_from_path
import pytesseract

from PIL import Image

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
NAME ="favole_nap"


# Converte le pagine del PDF in immagini
#pages = convert_from_path(f"{NAME}.pdf")

testo_completo = ""

for i in range(1, 6):
    page = Image.open(f"nap{i}.png")

#for page_number, page in enumerate(pages):
    # Applica OCR alla pagina
    text = pytesseract.image_to_string(page, lang='ita')  # usa 'eng' per inglese
    testo_completo += f"\n{text}"

# Salva in un file
with open(f"{NAME}.txt", "w", encoding="utf-8") as f:
    f.write(testo_completo)

print("OCR completato! Testo salvato in output.txt")