import re
import json


NAME = "sicilian_wikitext"

#with open(f"{NAME}.txt", "r", encoding="utf-8") as f:
#    testo = f.read()

with open(f"../corpus_tesi/siciliano/wikipedia/originale/{NAME}.json", "r", encoding="utf-8") as f:
    testo = json.load(f)

def process_opus(testo):
    data =[]
    #removes emojis special characters and other symbols
    emoji_pattern = re.compile(
    r"[\U0001F600-\U0001F64F", r"\U0001F300-\U0001F5FF" , r"\U0001F680-\U0001F6FF" , r"\U0001F700-\U0001F77F"  , r"\U0001F780-\U0001F7FF" ,r"\U0001F800-\U0001F8FF"   
    r"\U0001F900-\U0001F9FF" , r"\U0001FA00-\U0001FA6F" , r"\U0001FA70-\U0001FAFF", r"\U00002700-\U000027BF", r"\U0001F1E0-\U0001F1FF" ,r"]+",
    flags=re.UNICODE)
    testo = re.sub(emoji_pattern, "", testo)
    testo = re.sub(r"[:;%•●▪►◄■□◆◇…–—|*$£&]", " ", testo)
    testo = re.sub(r"[^\S\r\n]+", " ", testo)
    testo = re.sub(r"\[[\s\d]+\]", "", testo)
    testo = re.sub(r"\{.*?\}", "", testo, flags=re.DOTALL)
    #testo = re.sub(r"\[.*?\]", "", testo, flags=re.DOTALL)
    testo = re.sub(r"\{|\}", "", testo, flags=re.DOTALL)
    testo = re.sub(r"\[|\]", "", testo, flags=re.DOTALL)
    testo = re.sub(r" +", " ", testo)
    testo = re.sub(r"\n{3,}", "\n\n", testo)

    
    lines = testo.split("\n")
    for line in lines:
        lunghezza = len(line.strip().split())
        if lunghezza >= 4:
            data.append({
                "text": line.strip()
            })
        else:
            print(line)
    return data

def parse_wikipedia_sic(data):
    data_2 =[]
    visti = set() #make sure that duplicate articles are not considered
    for item in data:
        testo = item["text"]
        #removes wikipedia citations and also not useful lists of names
        testo = re.sub(r"\[.*?\]!|·.*?·|•.*?•", "", testo, flags=re.DOTALL)
        #removing the most common phrases
        patterns = [r"^Lu\s+\d+\s*\([IVXLCDM]+\s+a nùmmaru rumanu\)\s+è n'annu\b", r"^L'\d+\s*\([IVXLCDM]+\s+a nùmmaru rumanu\)\s+è n'annu", 
            r"Pì arrìpurtari cchìu immediatamenti i diffìrenzi tra li diversi ordini di grannizza, chista paggina cunteni",
            r"Pì arrìpurtari cchìu immediatamenti i diffìrenzi tra li diversi ordini di grannizza, chista pàggina cunteni",
            r"^\.[a-z]{2}\s+è lu duminiu di Internet assignatu",
            r"è un cumuni talianu dâ pruvincia di",
            r"è nu cumuni talianu dâ pruvincia di",
            r"Pi favuri, agghiunci na lijami a sta pàggina e scancella st'abbisu.\nPâ lista cumpleta dî pàggini òrfani, vidi a pàggina dâ catigurìa.",
            r'Elencu in òrdini (alfabbèticu|crunulòggicu) di li pirsunalità (?:ca foru )?primiati cu lu Nobel pi',
            r"{{Coord}}Categoria:P37 differente su WikidataCategoria:P38 (differente|uguale) su WikidataCategoria:P78 (differente|uguale) su WikidataCategoria:P85 (uguale|differente) su WikidataCategoria:P395 letta da WikidataCategoria:P474 differente su Wikidata",
            r"{{Coord}}Categoria:P37 letta da WikidataCategoria:P38 letta da WikidataCategoria:P78 letta da WikidataCategoria:P85 letta da WikidataCategoria:P395 letta da WikidataCategoria:P474 letta da Wikidata"
            r"uguale su WikidataCategoria:P474 uguale su Wikidata\n",
            r"((un|nu) elencu di distanzi maggiuri di 10[-−]\d+[^:]*:|" \
            r"Distanzi 'nfiriuri a 10[-−]\d+[^ \n]*|" \
            r"Distanzi supiriuri a 10[-−]\d+[^ \n]*)",
            r"^(.*?) è nu cumuni dâ pruvincia di (.*?)."
            r"Havi na pupulazzioni di\s*([\d' ]+)\s*abbitanti.",
            r"^(Distanzi|Accilirazzioni)\s+[^\n]*?(nfiriuri|infiriuri|supiriuri|supìriuri|superiuri|supiriori)\s+a\s+[0-9' ]+(?:m(?:/s²?|/s)?)?\s*$"
            ]
        for p in patterns:
            testo = re.sub(p, "", testo, flags=re.MULTILINE)
        if " ete " in testo or " quidd" in testo:
            #we don't want the texts in salentino
            continue
        lunghezza = testo.split()
        if len(lunghezza) > 5 and testo not in visti:
            data_2.append({
                "text": testo
            })
            visti.add(testo)
    return data_2

def parse_wikipedia_nap(data):
    data_2 =[]
    visti = set() #makes sure that duplicate articles are not found
    for item in data:
        testo = item["text"]
        #removes wiki citations, and most repeated senteces
        testo = re.sub(r"\[.*?\]", "", testo, flags=re.DOTALL)
        patterns = [r"Chist'articulo è sulo na bozza \(stub\). Si ce puó ddà na mano, p’’o fà addeventà nu poco meglio, spriemme ccà. Pe' ssapé comm’’e 'a fà, guarda ncopp’’e ccunvenziune 'e Wikipedia.\n",
                    r"Pe' ssapé quale so' tutte quant’’e stub, vaje a vedé 'a categoria stub.\n",
                    r"Elenco aggiornato alla stagione agonistica 2024/2025\n\nReal Puglianello", r'\n.*?\|', r'\d{1,3}°\d{1,2}(\'|′)\d{1,2}(\.\d{1,2})?(\"|″)[NSECW](,)? \d{1,3}°\d{1,2}(\'|′)\d{1,2}(\.\d{1,2})?(\"|″)[NSECW]',r"Mustra 'int' 'a mappa",
                    r"'O\s\d{1,2}\s'e\s[\wàèéìòù'’\s]+\sè\s'o\s\d+°\sjuorno\s'e\sll'anno\ssecunno\s'o\scalannario\sgreguriano(\s\('o\s\d+°\sint’’e\sl'anne\sbisestile\))?(\.\s*Ammancano\s\d+\sjourne\sp’’a\sfine\s'e\sll'anno(\s\('o\s\d+\s'int’’e\sl'anne\sbisestile\))?)?",
                    r"(?:'O\s\d{1,2}\s'e\s[\wàèéìòù'’\s]+\sè\s'o\s\d+°\sjuorno\s'e\sll'anno\ssecunno\s'o\scalannario\sgreguriano(\s\('o\s\d+°\sint’’e\sll'anne\sbisestile\))?\.)?\s*Ammancano\s\d+\sjourne\sp’’a\sfine\s'e\sll'anno\s*(?:\s\(('o|o)\s\d+\s'int’’e\sll'anne\sbisestile\))?",
                    r"· Comune d''a pruvincia 'e", 
                    r"^[A-ZÀ-Üa-zà-ü'’ \-]+ è nu comune\b.*?pruvincia\b.*\n?",
                    ]
        for p in patterns:
            testo = re.sub(p, "", testo, flags=re.MULTILINE)

        lunghezza = testo.split()
        if len(lunghezza) > 5 and testo not in visti:
            data_2.append({
                "text": testo
            })
            visti.add(testo)
    return data_2

def remove_numbered_notes(testo):
    #this function was used find the notes from the bottom of a page in a text, which were very inconsistent
    text = testo
    lines = text.splitlines(keepends=True)

    def is_note_start(line):
        #a line is the start of a note only if it starts with a number
        return re.match(r'^\s*\d{1,4}\b', line) is not None

    out_lines = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        if is_note_start(line):
            #we keep track of the last line which is a note
            last_note_line = line
            i += 1
            blank_count = 0
            while i < n:
                nxt = lines[i]
                #if a new number starts it means that this note has ended
                if is_note_start(nxt):
                    break
                # se riga vuota -> potenzialmente parte dei blank dopo nota
                if nxt.strip() == '':
                    blank_count += 1
                    if blank_count > 2:
                        break
                    i += 1
                    continue
                if blank_count > 0:
                    #here we check the case where the note had an incomplete word "accapo"
                    if last_note_line.rstrip().endswith('-'):
                        #in this case we continue
                        last_note_line = nxt
                        i += 1
                        blank_count = 0
                        continue
                    else:
                        break
                else:
                    #if there are no blanks we consume the line
                    last_note_line = nxt
                    i += 1
                    continue
            continue
        else:
            #since we excluded all the notes we simply append the lines that remain
            out_lines.append(line)
            i += 1

    cleaned = ''.join(out_lines)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    return cleaned

def process_testo_parentesi(testo):
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)
    data = process_testo_generico(testo)
    return data

def process_testo_dialoghi(testo):
    testo = testo.replace("...", "")
    #split the text according to the start/end of dialogue symbols
    chunks = re.split(r'(?:[<‹]\s*)?«(.*?)»', testo, flags=re.DOTALL)
    data = []
    for i, chunk in enumerate(chunks):
        if len(chunk.strip())>1:
            data.append({'text': chunk.strip()})
    return data

def process_testo_semplice(testo):
    testo= testo.split('---')
    data = []
    for t in testo:
        if len(t.strip())> 2:
            data.append({"text": t.strip()})
    return data

def process_testo_arbasicula(testo):
    #remove these strings
    testo = re.sub(r'^(?=.*(?:Arba\s*Sicula|AsbaSicula|AtbaSicula|iso\s*\d+\s*PM|sso\s*\d+\s*PM|Eugene\s+Mirabelli|Macpherson\s*&\s*Company|pp\.|[Ee]\s*%.*[A-Za-z]{2,}.*V)).*$', '', testo, flags=re.M)
    testo = re.sub(r'(?m)^\s*\d+\s*\n', '', testo)
    testo = re.sub(r'[©@]', '', testo)
    return process_testo_generico(testo)

def process_testo_dialettando(testo):
    data = []

    parti = testo.split("---")
    for racconto in parti:
        racconto=racconto.lstrip("\n\n")
        sezioni = racconto.split("\n\n",1)
        titolo = sezioni[0]
        testo = sezioni[1]
        if len(testo.strip()) > 2:
            data.append({
                "text": testo.strip(),
                "title": titolo.strip(),
            })
    return data

def process_testo_zanazzo(testo):
    #split according to the chapters which are indicated through roman numerals
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
        #split the text into dialogues
        for l in testo_racconto:

            ls =l.split("—")
            for i in ls:
                if len(i) != 0:
                    data.append({
                        "text": i.strip(),
                        "title": titolo.strip(),
                    })
    return data

def process_testo_liber(testo):
    testo = testo.replace('\x0c', '\n')
    pattern = (
        r'(?m)^\s*\d{1,3}\s*$'   #lines with the page number            
        r'(?:\n(?:Letteratura italiana Einaudi\s)\s*'
        r'\n\s*Giovan Battista Basile - Lo cunto de li cunti*)?' 
    )
    #pattern = (
    #    r'(?m)^\s*\d{1,3}\s*$'
    #    r'(?:\n(?:Fiabe novelle e racconti popolari siciliani\s*[–-]\s*Vol\. IV)\s*'
    #    r'\n\s*Giuseppe Pitrè\s*)?'              
    #)
    testo = re.sub(pattern, '\n', testo, flags=re.IGNORECASE)
    testo = remove_numbered_notes(testo)
    pattern = r'(?m)(?:\r?\n|\f)+\s*[IVXLCDM]{1,7}\.\s*(?:\r?\n|\f)+'
    testo = testo.replace("\r\n", "\n").replace("\r", "\n")
    #removes the pages number
    testo = re.sub(r'(?m)^\s*\d+\s*\n', '', testo)
    data = []
    blocchi = re.split(pattern, testo)
    for racconto in blocchi:
        racconto=racconto.strip()
        racconto = re.sub(r'\d+', '', racconto)
        racconto = re.split(r'\bVARIANTI\s+E\s+RISCONTRI', racconto, flags=re.IGNORECASE)[0].strip()
        
        print("--------------------------------------")
        
        #split to the first sentence
        parts = re.split(r'[.!?]|\n{1,2}', racconto, maxsplit=1)

        titolo = parts[0].strip()
        testo_racconto = parts[1].strip() if len(parts) > 1 else ""
        #remove the \n and the - characters, as well as \n\n and double/triple spaces
        testo_racconto = re.sub(r'-\s*\n\s*', '', testo_racconto)
        testo_racconto = re.sub(r'\n+', ' ', testo_racconto)
        testo_racconto = re.sub(r'\s{2,}', ' ', testo_racconto)
        print(testo_racconto)

        if len(testo_racconto.strip())>2:
            data.append({
                "text": testo_racconto.strip(),
                "title": titolo.strip(),
            })
    return data

def dividi_testo_per_frase(testo, max_parole):
    sentence_pattern = r'(?<=[.?!])\s+'
    frasi = re.split(sentence_pattern, testo)
    
    frasi = [f.strip() for f in frasi if f.strip()]

    blocchi = []
    blocco_corrente = []
    conteggio_parole = 0
    
    for frase in frasi:
        parole_frase = len(frase.split())
        if conteggio_parole + parole_frase > max_parole and blocco_corrente:
            # if the old block + the new sentence exceeds the limit we consider the current block
            blocchi.append(" ".join(blocco_corrente))
            
            #start the new block
            blocco_corrente = [frase]
            conteggio_parole = parole_frase
            
        else:
            blocco_corrente.append(frase)
            conteggio_parole += parole_frase
    if blocco_corrente:
        blocchi.append(" ".join(blocco_corrente))
        
    return blocchi

def process_pasolini(testo):
    testo = testo.replace('\x0c', '')

    pattern = (
        r'(?m)^\s*\d{1,3}\s*$'                   
        r'(?:\n(?:Letteratura italiana Einaudi\s)\s*'
        r'\n\s*Pier Paolo Pasolini - Ragazzi di vita*)?'              
    )
    testo = re.sub(pattern, '\n', testo, flags=re.IGNORECASE)

    pattern = r'(?m)(?:\r?\n|\f)+\s*[IVXLCDM]{1,7}\.\s*(?:\r?\n|\f)+'

    capitoli = re.split(pattern, testo)
    data = []

    for capitolo in capitoli:
        if "CAPITOLO" in capitolo:
            continue
        lungh = []
        capitolo=capitolo.strip()
        #remove the \n and the - characters, as well as \n\n and double/triple spaces
        testo_racconto = re.sub(r'-\s*\n\s*', '', capitolo)
        testo_racconto = re.sub(r'\n+', ' ', testo_racconto)
        testo_racconto = re.sub(r'\s{2,}', ' ', testo_racconto)

        LIMITE_MASSIMO_PAROLE = 130

        risultato = dividi_testo_per_frase(testo_racconto, LIMITE_MASSIMO_PAROLE)
        #frasi_racconto = testo_racconto.split(". ")
        for f in risultato:
            print(f)
            print("\n---------------------------------------------------\n")
            
            if len(testo_racconto) > 2:
                data.append({
                    "text":f,
                })
        
    return data

def process_pascarella(testo):
    testo = testo.replace('\x0c', '')
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)
    pattern = (
        r'(?m)^\s*\d{1,3}\s*$'                    
        r'(?:\n(?:Novelle napoletane\s)\s*'
        r'\n\s*Marco Monnier*)?'
        r"\[.*?\]|\(.*?\)" 
        r"\*"         
    )
    testo = re.sub(pattern, '', testo, flags=re.IGNORECASE)

    pattern = r'(?m)(?:\r?\n|\f)+\s*[IVXLCDM]{1,7}\.\s*(?:\r?\n|\f)+'

    capitoli = re.split(pattern, testo)
    data = []

    for capitolo in capitoli:
        if "CAPITOLO" in capitolo:
            continue
        lungh = []
        capitolo=capitolo.strip()
        #remove the \n and the - characters, as well as \n\n and double/triple spaces
        testo_racconto = re.sub(r'-\s*\n\s*', '', capitolo)
        testo_racconto = re.sub(r'\n+', ' ', testo_racconto)
        testo_racconto = re.sub(r'\s{2,}', ' ', testo_racconto)

        LIMITE_MASSIMO_PAROLE = 150

        risultato = dividi_testo_per_frase(testo_racconto, LIMITE_MASSIMO_PAROLE)
        #frasi_racconto = testo_racconto.split(". ")
        for f in risultato:
            print(f)
            print("\n---------------------------------------------------\n")
            
            if len(testo_racconto) > 2:
                data.append({
                    "text":f,
                })
        
    return data

def process_malavoglia(testo):
    testo = testo.replace('\x0c', '')
    pattern = (r'(?m)^\s*\d{1,3}\s*$')
    testo = re.sub(pattern, '\n', testo, flags=re.IGNORECASE)

    pattern = r'(\s*CAPITOLO\s+[IVXLCDM]+)'

    capitoli = re.split(pattern, testo)
    data = []

    for capitolo in capitoli:
        if "CAPITOLO" in capitolo:
            continue
        lungh = []
        capitolo=capitolo.strip()
        testo_racconto = re.sub(r'-\s*\n\s*', '', capitolo)
        testo_racconto = re.sub(r'\n+', ' ', testo_racconto)
        testo_racconto = re.sub(r'\s{2,}', ' ', testo_racconto)

        LIMITE_MASSIMO_PAROLE = 150

        risultato = dividi_testo_per_frase(testo_racconto, LIMITE_MASSIMO_PAROLE)
        #frasi_racconto = testo_racconto.split(". ")
        for f in risultato:
            print(f)
            print("\n\n\n---------------------------------------------------\n\n\n")
            if len(testo_racconto) > 2:
                data.append({
                    "text":f,
                })
        
    return data

def process_testo_liber_nap(testo):
    testo = testo.replace('\x0c', '')
    pattern = r'(?m)^\s*\d{1,3}\s*$'               # riga con solo il numero di pagina            
    
    data=[]
    testo = re.sub(pattern, '', testo, flags=re.IGNORECASE)

    frase = "Letteratura italiana Einaudi"
    pattern = rf".*{re.escape(frase)}.*\n?"
    testo = re.sub(pattern, '', testo, flags=re.IGNORECASE)
    frase = "Giovan Battista Basile - Lo cunto de li cunti"
    pattern = rf".*{re.escape(frase)}.*\n?"
    testo = re.sub(pattern, '', testo, flags=re.IGNORECASE)


    blocchi = testo.split("\n\n\n")
    
    for racconto in blocchi:
        racconto=racconto.strip()
        testo_racconto = re.sub(r'-\s*\n\s*', '', racconto)
        testo_racconto = re.sub(r'\n+', ' ', testo_racconto)
        testo_racconto = re.sub(r'\s{2,}', ' ', testo_racconto)
        
        if len(testo_racconto) > 2:
            data.append({
                "text": testo_racconto,
            })
    return data

def process_testo_liber_2(testo):
    testo = testo.replace('\x0c', '\n')
    pattern = (
        r'(?m)^\s*\d{1,3}\s*$'                   
        r'(?:\n(?:Fiabe novelle e racconti popolari siciliani\s*[–-]\s*Vol\. (II|I|III|IV|V)\s*' 
        r'\n\s*Giuseppe Pitrè\s*)?'                
    )
    testo = re.sub(pattern, '\n', testo, flags=re.IGNORECASE)
    testo = remove_numbered_notes(testo)
    pattern = r'(?m)(?:\r?\n|\f)+\s*[IVXLCDM]{1,7}\.\s*(?:\r?\n|\f)+'
    testo = testo.replace("\r\n", "\n").replace("\r", "\n")
    #removes the pages number
    testo = re.sub(r'(?m)^\s*\d+\s*\n', '', testo)
    fulltext = ""
    blocchi = re.split(pattern, testo)
    for racconto in blocchi:
        racconto=racconto.strip()
        racconto = re.sub(r'\d+', '', racconto)
        
        
        racconto = re.split(r'\bVARIANTI\s+E\s+RISCONTRI', racconto, flags=re.IGNORECASE)[0].strip()
        racconto = "\n--------------------------------------\n" + racconto
        fulltext += racconto
        print("--------------------------------------")
        

    with open("pitre_fiabe_novelle_e_racconti_1_nuovo.txt", "w", encoding="utf-8") as f:
        f.write(fulltext)

def process_poesie_liber(testo):
    testo = testo.replace('\x0c', '')
    testo = re.sub(r'7474\s*$', '', testo).strip()

    parts = re.split(r'\n\s*\b\d{1,3}\b\s*\n', testo)
    data =[]

    for p in parts:
        #this is important to exclude whether we have only the title of the poem, since they all are uppercase
        if re.search(r"[a-zàèéìòóù]", p.strip()):
            data.append({
                'text': p.strip()
            })
        
    return data

def process_poesie_copioni(testo):
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
    testo= re.sub(r'\d+', '', testo)

    data=[]

    testo = testo.split(". ")

    for l in testo:
        ls =l.split("—")
        for i in ls:
            if len(i.strip()) > 4:
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

def pulisci_blocco(blocco):
    righe = blocco.splitlines()
    pulite = []

    for r in righe:
        linea = r.strip()

        #removes the lines like   String:
        if re.match(r"^[A-Za-zÀ-ÿ'\-]+:$", linea):
            continue
        
        # removes the SIGLE and other dotted characters
        if re.match(r"^(s\.\s*[fm]\.|v\.\s*(tr|intr)\.)", linea):
            continue
        pulite.append(r)

    return "\n".join(pulite)

def process_testo_torrese(testo):
    data =[]
    pattern = r"\*\*\*.*?(?=(?:\*\*\*)|$)"

    blocchi = re.findall(pattern, testo, flags=re.S)

    for i, b in enumerate(blocchi, 1):
        blocco = pulisci_blocco(b) 
        pulito = re.sub(r'\n\n.*$', '', blocco, flags=re.DOTALL)
        pulito = re.sub(r'^\*\*\*[A-Z]{1,4}\.\s*', '', pulito)
        pulito = pulito.strip("***")
        if len(pulito.strip()) > 2:
            data.append({
                "text": pulito.strip()
            })
    return data

def process_poesie(testo):
    testo = testo.replace('\x0c', '')
    data =[]
    parts = re.split(r'\b[IVXLCDM]{1,7}\b', testo)
    for p in parts:
        if len(p.strip()) >2:
            data.append({
                "text": p.strip()
            })
    return data

def process_poesie_tre(testo):
    testo = testo.replace('\x0c', '')
    data =[]
    pattern = r"^(?=[A-ZÀ-Ý0-9 '’.,;:!?()-]+$).*$"
    #splitting for the title
    parts = re.split(pattern, testo)
    for p in parts:
        p=p.strip(".\n\n\n\n\n\n")
        if len(p.strip()) >2:
            data.append({
                "text": p.strip()
            })
    return data

data =parse_wikipedia_sic(testo)

with open(f"../corpus_tesi/siciliano/wikipedia/{NAME}_processed.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)
    
    
    