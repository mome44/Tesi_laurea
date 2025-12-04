import requests
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time
from tqdm import tqdm
import re

header = {"User-Agent": "TesimagistraleMNLP/1.0 (mailto:lagana.1946083@studenti.uniroma1.it)"}
language ="scn"
URL = f"https://{language}.wikipedia.org/w/api.php"
#URL = f"https://{language}.wikisource.org/w/api.php"
input_file_path = "scnwiki-latest-all-titles"

NAME = "sicilian_wikitext"
FOLDER = "corpus_tesi/siciliano/wikipedia"


def parse_text_wiki(html_text):
    soup = BeautifulSoup(html_text, 'html.parser')
    paragraphs= soup.select("p")
    text = ""
    paragraph_text_list =[]
    #getting the text from all the paragraphs
    for p in paragraphs:
        paragraph_text = p.get_text()
        if paragraph_text not in paragraph_text_list:   
            paragraph_text_list.append(paragraph_text)
    for t in paragraph_text_list:
        text = text + t
    text = re.sub(r"\{\s*\\displaystyle\s+[^}]+\}", "", text)
    return text


def safe_request(Req_session, WIKI_URL, header, params):
    for attempt in range(1,6):
        #RESPONSE OF THE SECOND REQUEST
        response = Req_session.get(WIKI_URL, headers=header, params=params, timeout=30)
        if response.status_code in (429, 503):
            wait = 4 * attempt
            print(f"Tentativo {attempt} fallito ({response.status_code}), attendo {wait}s...")
            time.sleep(wait)
            continue
        if response.status_code == 403:
            time.sleep(4 * attempt)
            continue
        response.raise_for_status()
        return response

def get_wikidata(url,title, language):
    Req_session = requests.Session()

    #This query gets the physical html content of the pages
    wiki_page_structure = {
        "action": "parse",
        "format": "json",
        "page": title,
        "prop": "text",
        "redirects": "1",     
        "maxlag": "5",
    }
    
    response = safe_request(Req_session, url, header, wiki_page_structure)
    data = response.json().get("parse", {})
    html_text = data.get("text", {}).get("*", "")
    
    text = parse_text_wiki(html_text)
    #print(text)
    return text

if __name__ == "__main__":
    df = pd.read_csv(input_file_path, sep="\t")

    corpus_dictionary = []

    futures = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for idx, row in df.iterrows():
            title = row["page_title"]
            fut = executor.submit(get_wikidata, URL, title, language)
            futures.append((idx, title, fut))
        with tqdm(total=len(futures), desc="Processing Wikipedia pages", dynamic_ncols=True, miniters=1, disable=False) as pbar:

            for fut in as_completed([f for (_, _, f) in futures]):
                for idx, title, f_check in futures:
                    if f_check == fut:
                        break
                try:
                    text = fut.result()
                except Exception:
                    text = ""
                if len(text.strip())>3:
                    corpus_dictionary.append({
                        "text": text.strip()
                    })
                pbar.update(1)
                
                if pbar.n % 200 == 0:
                    with open(f"{FOLDER}/{NAME}_index_{pbar.n}.json", "w", encoding="utf-8") as f:
                        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)

                time.sleep(0.05)

    # SALVATAGGIO FINALE CORRETTO
    with open(f"{FOLDER}/{NAME}.json", "w", encoding="utf-8") as f:
        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)

    print("FINITO!")