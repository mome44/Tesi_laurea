import requests
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time
from tqdm import tqdm
import re
import os

header = {"User-Agent": "TesimagistraleMNLP/1.0 (mailto:lagana.1946083@studenti.uniroma1.it)"}
language ="nap"
URL = f"https://{language}.wikisource.org/w/api.php"
input_file_path = "wikisourc.txt"

NAME = "nap_wikisource"
FOLDER = "corpus_tesi/napoletano/wikipedia/source"


def extract_title_from_url(url):
    # Esempio URL: https://it.wikisource.org/wiki/La_Divina_Commedia/Inferno/I
    match = re.search(r'/wiki/(.+)$', url)
    return match.group(1) if match else None

def fetch_wikisource_text(title):

    params = {
        "action": "parse",
        "page": title,
        "prop": "wikitext",
        "format": "json"
    }

    r = requests.get(URL, headers=header, params=params, timeout=30)
    data = r.json()

    if "parse" not in data:
        return ""

    return data["parse"]["wikitext"]["*"]

def save_text(text, filename):
    with open(filename, "w", encoding="utf-8") as f:
        f.write(text)

def process_wikisource_links(links):
    for url in links:
        title = extract_title_from_url(url)
        if not title:
            print(f"URL non valido: {url}")
            continue

        print(f"Scarico: {title} ...")
        text = fetch_wikisource_text(title)
        print(text)
        if not text.strip():
            print(f"⚠ Nessun testo trovato per {title}")
            continue

        filename = os.path.join(FOLDER, f"{NAME}.txt")
        save_text(text, filename)
        print(f"Salvato in: {filename}")


# ──────────────────────────────────────────

with open(input_file_path, "r", encoding="utf-8") as f:
    testo=f.read()

lista = testo.split("\n")
print(lista)

process_wikisource_links(lista)
