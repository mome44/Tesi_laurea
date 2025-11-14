import requests
from urllib.parse import quote
BASE_URL = "https://nap.wikisource.org/wiki/"
API_URL = "https://nap.wikisource.org/w/api.php"
header = {"User-Agent": "TesimagistraleMNLP/1.0 (mailto:lagana.1946083@studenti.uniroma1.it)"}
params = {
    "action": "query",
    "list": "allpages",
    "aplimit": "max",
    "format": "json",
    "apnamespace": 0      # solo namespace principale (i testi)
}

pages = []

while True:
    data = requests.get(API_URL, params=params, headers=header).json()

    # Aggiunge gli URL completi
    for p in data["query"]["allpages"]:
        raw_title = p["title"]
        # 1. Sostituisce gli spazi con _ come fa MediaWiki
        normalized = raw_title.replace(" ", "_")

        # 2. Codifica i caratteri speciali per URL
        encoded = quote(normalized, safe="_")

        full_url = BASE_URL + encoded
        pages.append(full_url)

    # Gestione della paginazione
    if "continue" in data:
        params.update(data["continue"])
    else:
        break

# Salvataggio su file
with open("pagine_wikisource.txt", "w", encoding="utf-8") as f:
    for url in pages:
        f.write(url + "\n")

print(f"Totale pagine trovate: {len(pages)}")
print("File salvato come pagine_wikisource.txt")
