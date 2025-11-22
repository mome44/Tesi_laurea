import requests
from bs4 import BeautifulSoup
import re
import os
from urllib.parse import unquote, urlparse

header = {"User-Agent": "TesimagistraleMNLP/1.0 (mailto:lagana.1946083@studenti.uniroma1.it)"}
input_file_path = "wikisourc.txt"

NAME = "nap_wikisource"
FOLDER = "corpus_tesi/napoletano/wikipedia/source"


def extract_title_from_url(url):
    m = re.search(r'/wiki/(.+)$', url)
    return m.group(1) if m else None


def safe_filename(title):
    title = unquote(title)
    title = re.sub(r'[\\/*?:"<>|]', "_", title)
    return title + ".txt"


def fetch_html_text(url):
    r = requests.get(url, headers=header, timeout=20)
    soup = BeautifulSoup(r.text, "html.parser")

    main = soup.select_one("div.mw-parser-output")
    if not main:
        return ""

    # Rimuovi elementi non testuali
    for sel in ["table", "style", "script", ".references", ".toc"]:
        for el in main.select(sel):
            el.decompose()

    # Estrai testo
    text = main.get_text("\n", strip=True)
    text = re.sub(r'\n{3,}', "\n\n", text)
    return text


def process_wikisource_links(links):
    os.makedirs(FOLDER, exist_ok=True)

    for url in links:
        title = extract_title_from_url(url)
        if not title:
            print(f"URL non valido: {url}")
            continue

        print(f"Scarico {title} ...")

        text = fetch_html_text(url)

        if not text.strip():
            print(f"⚠ Nessun testo estratto da {title}")
            continue

        filename = os.path.join(FOLDER, safe_filename(title))

        with open(filename, "w", encoding="utf-8") as f:
            f.write(text)

        print(f"✔ Salvato in: {filename} ({len(text)} caratteri)")


# ---- MAIN ----

with open(input_file_path, "r", encoding="utf-8") as f:
    links = [line.strip() for line in f if line.strip()]

process_wikisource_links(links)
