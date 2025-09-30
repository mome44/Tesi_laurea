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
#URL = f"https://{language}.wikipedia.org/w/api.php"
URL = f"https://{language}.wikisource.org/w/api.php"
input_file_path = "scnwiki-latest-all-titles"

NAME = "sicilian_wikisource"
FOLDER = "sicilian"


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

def parse_text_sicilian_wikisource(html_text):

    return text


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
    
    if language == "scn":
        text = parse_text_sicilian_wiki(html_text)
    
    return text


if __name__ == "__main__":
    df = pd.read_csv(input_file_path, sep="\t")

    i = 0
    result_list=[]
    corpus_dictionary = dict()
    with ThreadPoolExecutor(max_workers=12) as executor:
        #I do a loop throughout all the rows
        for idx, row in df.iterrows():
            title = row['page_title']
            #I compute the result
            result= executor.submit(get_wikidata, title, language)
            #I append it in the list
            result_list.append(result)

        with tqdm(total=len(result_list),
                  desc="Processing Wikipedia pages",
                  dynamic_ncols=True,
                  miniters=1,
                  disable=False) as pbar:         # forza la visualizzazione
            for fut in as_completed(result_list):
                try:
                    r = fut.result()
                except Exception:
                    r = ""

                if pbar.n not in corpus_dictionary:
                    corpus_dictionary[pbar.n] = r

                pbar.update(1)                    

                # checkpoint ogni 100 completamenti
                if pbar.n % 500 == 0:
                    with open(f'{FOLDER}/{NAME}_index_{pbar.n}.json', "w", encoding="utf-8") as f:
                        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)

                time.sleep(0.25)  


    with open(f'{FOLDER}/{NAME}.json', "w", encoding="utf-8") as file:
        json.dump(corpus_dictionary, f, ensure_ascii=False, indent=2)
    