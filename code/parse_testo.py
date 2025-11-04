import re
import json
pattern = r"[A-Za-z]+\. [A-Za-z]+"

NAME = "Come_ve_va_de_ingarellavve_su_sta_cosa_il_romanesc"

with open(f"{NAME}.txt", "r", encoding="utf-8") as f:
    testo = f.read()

def process_testo_parentesi(testo):

    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)
    data = process_testo_generico(testo)
    return data

def process_testo_dialoghi(testo):
    testo = testo.replace("...", "")
    chunks = re.split(r'(?:[<‹]\s*)?«(.*?)»', testo, flags=re.DOTALL)
    data = []
    for i, chunk in enumerate(chunks):
        if len(chunk.strip())>1:
            data.append({'text': chunk.strip()})
    return data

def process_testo_semplice(testo):
    testo= testo.split('\n')
    data = []
    for t in testo:
        data.append({"text": t.strip()})
    return data


def process_testo_zanazzo(testo):
    pattern = r'(?m)(?:\n|\f)+(?=\s*[IVXLCDM]{1,7}\.\s)'
    testo = testo.replace("\r\n", "\n").replace("\r", "\n")
    #removes the pages number
    testo = re.sub(r'(?m)^\s*\d+\s*\n', '', testo)
    data = []
    blocchi = re.split(pattern, testo)
    for racconto in blocchi:
        racconto=racconto.strip()
        print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        
        #split the title according to the roman numerals and string
        m = re.match(r'^\s*([IVXLCDM]{1,7}\.\s*[^\.\n]*)\.?\s*(.*)$', racconto, re.DOTALL)
        if m:
            titolo = m.group(1).strip()
            testo_racconto = m.group(2).strip()
        else:
            titolo = "unknown"
            testo_racconto = racconto
        #remove the \n and the - characters, as well as \n\n and double/triple spaces
        testo_racconto = re.sub(r'-\s*\n\s*', '', testo_racconto)
        testo_racconto = re.sub(r'\n+', ' ', testo_racconto)
        testo_racconto = re.sub(r'\s{2,}', ' ', testo_racconto)
        print(titolo, " --- \n", testo_racconto)

        testo_racconto = testo_racconto.split(". ")

        for l in testo_racconto:

            ls =l.split("—")
            for i in ls:
                if len(i) != 0:
                    data.append({
                        "text": i.strip(),
                        "title": titolo.strip(),
                    })
    return data

def process_poesie_liber(testo):
    testo = re.sub(r'7474\s*$', '', testo).strip()

    parts = re.split(r'\n\s*\b\d{1,3}\b\s*\n', testo)
    data =[]

    for p in parts:

        data.append({
            'text': p.strip()
        })
        
    return data

def process_poesie(testo):
    testo = testo.replace("Pier Paolo Pasolini   - Il vantone di Plauto \n\n", "")
    parts = testo.split("HTTP://COPIONI.CORRIERESPETTACOLO.IT")

    data =[]
    for p in parts:
        if len(p.strip()) > 0:
                data.append({
                    "text": p.strip()
                })
        
    return data

def process_testo_generico(testo):
    testo = re.sub(r'\n+', ' ', testo)
    testo = re.sub(r'\.{2,}', '.', testo)

    data=[]

    testo = testo.split(". ")

    for l in testo:
        ls =l.split("–")
        for i in ls:
            if len(i.strip()) > 0:
                data.append({
                    "text": i.strip()
                })
    return data

def process_testo_virgolette(testo):
    matches = re.findall(r'“([^”]+)”', testo)
    data =[]
    for l in matches:
        if len(l.strip()) > 3:
            data.append({
                "text": l.strip()
            })
    return data

def process_altro(testo):
    testo = testo.split("\n")
    data =[]
    for i in testo:
        i = i.strip('\"')
        if len(i.strip()) > 3:
                data.append({
                    "text": i.strip()
                })
    return data

def process_testo_wikisource(testo):
    #print(testo)
    testo = testo.split(". ")

    data = []
    for l in testo:

        ls =l.split("—")
        for i in ls:
            if len(i.strip()) > 0:
                data.append({
                    "text": i.strip()
                })
    return data

data =process_testo_virgolette(testo)
#data = process_testo_zanazzo(testo)

with open(f"../corpus_tesi/romanesco/{NAME}_processed.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)
    
    
    