import requests
import json
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd
import time
from tqdm import tqdm
import re

header = {"User-Agent": "TesimagistraleMNLP/1.0 (mailto:lagana.1946083@studenti.uniroma1.it)"}
language ="nap"
URL = f"https://{language}.wikipedia.org/w/api.php"
#URL = f"https://{language}.wikisource.org/w/api.php"
input_file_path = "napwiki-latest-all-titles"

NAME = "neapolitan_wikitext"
FOLDER = "corpus_tesi/napoletano/wikipedia"


def parse_text_sicilian_wiki(html_text):

    soup = BeautifulSoup(html_text, 'html.parser')
        
    paragraphs= soup.select("p")
    text = ""
    paragraph_text_list =[]
    for p in paragraphs:
        paragraph_text = p.get_text()
        if paragraph_text not in paragraph_text_list:   
            paragraph_text_list.append(paragraph_text)
    for t in paragraph_text_list:
        text = text + t
    text = re.sub(r"\{\s*\\displaystyle\s+[^}]+\}", "", text)
    return text

#def parse_text_sicilian_wikisource(html_text):
#
#    return text


def safe_get(session, url, params=None, max_retries=5, base_wait=2):
    last = None
    for attempt in range(1, max_retries + 1):
        r = session.get(url, params=params, timeout=30)
        if r.status_code in (429, 503):
            wait = int(r.headers.get("Retry-After", base_wait * attempt))
            time.sleep(wait)
            last = r
            continue
        if r.status_code == 403:
            time.sleep(base_wait * attempt)
            last = r
            continue
        r.raise_for_status()
        return r
    if last is not None:
        last.raise_for_status()
    raise RuntimeError("No valid response")

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
    #The id of some language are not the same as the one found in the
    #url so I had to map them
    #print(WIKI_URL, title)
    Req_session = requests.Session()

    #This query gets the physical content of the pages

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
    
    text = parse_text_sicilian_wiki(html_text)
    #print(text)
    return text
def get_wikipedia_url(title, language):
    # Replace spaces with underscores and URL-encode special characters
    from urllib.parse import quote
    base = f"https://{language}.wikipedia.org/wiki/"
    return base + quote(title.replace(" ", "_"))


if __name__ == "__main__":
    df = pd.read_csv(input_file_path, sep="\t")

    corpus_dictionary = []

    futures = []
    with ThreadPoolExecutor(max_workers=5) as executor:

        # CREO SOLO LA LISTA DEI FUTURE
        for idx, row in df.iterrows():
            title = row["page_title"]
            fut = executor.submit(get_wikidata, URL, title, language)
            # salvo l'indice separatamente, NON dentro la lista dei futuri
            futures.append((idx, title, fut))

        # tqdm funziona SOLO qui, NON durante la creazione dei future
        with tqdm(total=len(futures),
                  desc="Processing Wikipedia pages",
                  dynamic_ncols=True,
                  miniters=1,
                  disable=False) as pbar:

            # Ricorda: as_completed vuole SOLO la lista dei future puri
            for fut in as_completed([f for (_, _, f) in futures]):

                # Trovo l'indice corretto del future
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

                # checkpoint ogni 200
                if pbar.n % 200 == 0:
                    with open(f"{FOLDER}/{NAME}_index_{pbar.n}.json", "w", encoding="utf-8") as f:
                        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)

                time.sleep(0.05)

    # SALVATAGGIO FINALE CORRETTO
    with open(f"{FOLDER}/{NAME}.json", "w", encoding="utf-8") as f:
        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)

    print("FINITO!")
#
#if __name__ == "__main__":
#    df = pd.read_csv(input_file_path, sep="\t")
#
#    i = 0
#    result_list=[]
#    corpus_dictionary = dict()
#    with ThreadPoolExecutor(max_workers=12) as executor:
#        #I do a loop throughout all the rows
#        with tqdm(total=len(df), desc="Processing pages", dynamic_ncols=True) as pbar:
#            for idx, row in df.iterrows():
#                title = row['page_title']
#                page_url = get_wikipedia_url(title, language)
#                #print("Checking:", page_url)
#                #I compute the result
#                result= executor.submit(get_wikidata, URL, title, language)
#                #I append it in the list
#                result_list.append(result)
#
#        with tqdm(total=len(result_list),
#                  desc="Processing Wikipedia pages",
#                  dynamic_ncols=True,
#                  miniters=1,
#                  disable=False) as pbar:         # forza la visualizzazione
#            for fut in as_completed(result_list):
#                try:
#                    r = fut.result()
#                except Exception:
#                    r = ""
#
#                if pbar.n not in corpus_dictionary:
#                    corpus_dictionary[pbar.n] = r
#
#                pbar.update(1)                    
#
#                # checkpoint ogni 100 completamenti
#                if pbar.n % 100 == 0:
#                    with open(f'{FOLDER}/{NAME}_index_{pbar.n}.json', "w", encoding="utf-8") as f:
#                        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)
#
#                time.sleep(0.25)  
#
#    with open(f'{FOLDER}/{NAME}.json', "w", encoding="utf-8") as f:
#        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)
   
#if __name__ == "__main__":
#    df = pd.read_csv(input_file_path, sep="\t")
#
#    corpus_dictionary = dict()
#
#    with tqdm(total=len(df),
#              desc="Processing Wikipedia pages (sequential)",
#              dynamic_ncols=True,
#              miniters=1,
#              disable=False) as pbar:
#        for idx, row in df.iterrows():
#            title = row["page_title"]
#            page_url = get_wikipedia_url(title, language)
#            print("Checking:", page_url)
#            
#            try:
#                text = get_wikidata(URL, title, language)
#            except Exception as e:
#                print(f"Errore nella pagina '{title}': {e}")
#                text = ""
#
#            corpus_dictionary[idx] = text
#            pbar.update(1)
#            
#
#            # checkpoint ogni 500 pagine
#            if (idx + 1) % 500 == 0:
#                with open(f'{FOLDER}/{NAME}_index_{idx+1}.json', "w", encoding="utf-8") as f:
#                    json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)
#            
#            time.sleep(0.5)  # per non sovraccaricare Wikipedia
#
#    # salvataggio finale
#    with open(f'{FOLDER}/{NAME}.json', "w", encoding="utf-8") as f:
#        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)