import requests
import json
import subprocess
from bs4 import BeautifulSoup
from urllib.parse import unquote
import sys
import os

DUMP_LIST = ["scnwiki-latest-pages-articles-multistream.xml.bz2", "scnwiki-latest-pages-meta-current.xml.bz2"]
for zipped_dump in DUMP_LIST:

    # Directory di output (verrà creata se non esiste)
    output_dir = "parsed_text"

    #execute the call of wikiextractor
    command = [
        "python3", "-m", "wikiextractor.WikiExtractor",
        "--json",
        "--no-templates",
        "--processes", "4",
        "-o", output_dir,
        zipped_dump
    ]

    subprocess.run(command, check=True)

for file_path in os.folders():
    with open(file_path, "r", encoding="utf-8") as file:
        file = json.load(file)

    for line in file:
        url = line['url']
        url = unquote(url)
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            paragraphs= soup.select("p")
            text = ""
            for p in paragraphs:
                text = text.join(p)
            print(text)
        except Exception as e:
            print(f"Error fetching {url}: {e}")
