import re
import json
pattern = r"[A-Za-z]+\. [A-Za-z]+"

NAME = "177750.PL1-Ragazzi-di-vita-di-Pier-Paolo-Pasolini-1955-Letteratura-italiana-Einaudi"

with open(f"{NAME}.txt", "r", encoding="utf-8") as f:
    testo = f.read()

#with open(f"{NAME}.json", "r", encoding="utf-8") as f:
#    testo = json.load(f)

def parse_wikipedia_sic(data):
    data_2 =[]
    for item in data:
        testo = item["text"]
        #rimuove le citazioni di wikipedia
        testo = re.sub(r"\[.*?\]|", "", testo, flags=re.DOTALL)
        #rimuove le frasi che sono presenti moltissime volte
        patterns = [r"^Lu\s+\d+\s*\([IVXLCDM]+\s+a nùmmaru rumanu\)\s+è n'annu\b", r"^L'\d+\s*\([IVXLCDM]+\s+a nùmmaru rumanu\)\s+è n'annu", 
            r"Pì arrìpurtari cchìu immediatamenti i diffìrenzi tra li diversi ordini di grannizza, chista paggina cunteni",
            r"Pì arrìpurtari cchìu immediatamenti i diffìrenzi tra li diversi ordini di grannizza, chista pàggina cunteni",
            r"^\.[a-z]{2}\s+è lu duminiu di Internet assignatu",
            r"è un cumuni talianu dâ pruvincia",
            r"è nu cumuni talianu dâ pruvincia",
            r"Pi favuri, agghiunci na lijami a sta pàggina e scancella st'abbisu.\nPâ lista cumpleta dî pàggini òrfani, vidi a pàggina dâ catigurìa."]
        
        for p in patterns:
            testo = re.sub(p, "", testo)
        lunghezza = testo.split(" ")
        if len(lunghezza) > 5:
            data_2.append({
                "text": testo
            })
    return data_2

def parse_wikipedia_nap(data):
    data_2 =[]
    for item in data:
        testo = item["text"]
        #rimuove le citazioni di wikipedia
        testo = re.sub(r"\[.*?\]|", "", testo, flags=re.DOTALL)
        patterns = [r"Chist'articulo è sulo na bozza (stub). Si ce puó ddà na mano, p’’o fà addeventà nu poco meglio, spriemme ccà. Pe' ssapé comm’’e 'a fà, guarda ncopp’’e ccunvenziune 'e Wikipedia.\n",
                    r"Pe' ssapé quale so' tutte quant’’e stub, vaje a vedé 'a categoria stub.\n"]
        
        for p in patterns:
            testo = re.sub(p, "", testo)
        lunghezza = testo.split(" ")
        if len(lunghezza) > 5:
            data_2.append({
                "text": testo
            })
    return data_2


def remove_numbered_notes(testo, max_blank_after_note=2):
    """
    Rimuove blocchi di note che iniziano con un numero all'inizio di riga.
    Se la riga finale della nota termina con '-' (sillabazione), rimuove anche
    la riga successiva non vuota come continuazione, anche se separata da
    fino a `max_blank_after_note` righe vuote.
    """
    text = testo
    lines = text.splitlines(keepends=True)

    def is_note_start(line):
        # una riga è inizio nota se comincia con 1-4 cifre
        return re.match(r'^\s*\d{1,4}\b', line) is not None

    out_lines = []
    i = 0
    n = len(lines)

    while i < n:
        line = lines[i]
        if is_note_start(line):
            # siamo all'inizio di una nota: salta la riga numerata
            last_note_line = line
            i += 1

            # scarta le righe successive della nota finché non troviamo
            # una nuova riga che inizia con numero (nuova nota) o
            # finché non decidiamo di fermarci
            blank_count = 0
            while i < n:
                nxt = lines[i]
                # se inizia un nuovo numero -> fine nota
                if is_note_start(nxt):
                    break
                # se riga vuota -> potenzialmente parte dei blank dopo nota
                if nxt.strip() == '':
                    blank_count += 1
                    # non superare il massimo di blank da consumare qui (ma li saltiamo)
                    if blank_count > max_blank_after_note:
                        # non vogliamo saltare più di max_blank_after_note;
                        # quindi ci fermiamo lasciando il resto del testo intatto
                        break
                    i += 1
                    continue
                # riga non vuota
                # se c'erano blank lines prima di questa riga non vuota,
                # la consideriamo continuazione SOLO se la nota precedente
                # terminava con una sillabazione (es. endswith('-'))
                if blank_count > 0:
                    if last_note_line.rstrip().endswith('-'):
                        # è continuazione: consumala e continua a cercare eventuali altre righe
                        last_note_line = nxt
                        i += 1
                        blank_count = 0
                        continue
                    else:
                        # non è continuazione, fermati QUI (mantieni la riga non vuota)
                        break
                else:
                    # nessun blank tra le righe: riga non vuota immediata dopo la numerata
                    # la consideriamo come parte della nota; consumala
                    last_note_line = nxt
                    i += 1
                    continue
            # fine: abbiamo saltato la nota (e al massimo max_blank_after_note blank lines e
            # possibili continuazioni dovute a sillabazione)
            continue
        else:
            out_lines.append(line)
            i += 1

    # ricostruisci testo
    cleaned = ''.join(out_lines)
    # evita troppi newline consecutivi residui (>2 -> 2)
    cleaned = re.sub(r'\n{3,}', '\n\n', cleaned)
    
    return cleaned

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
        if len(t.strip())> 2:
            data.append({"text": t.strip()})
    return data

def process_testo_arbasicula(testo):
    testo = re.sub(r'^(?=.*(?:Arba\s*Sicula|AsbaSicula|AtbaSicula|iso\s*\d+\s*PM|sso\s*\d+\s*PM|Eugene\s+Mirabelli|Macpherson\s*&\s*Company|pp\.|[Ee]\s*%.*[A-Za-z]{2,}.*V)).*$', '', testo, flags=re.M)
    testo = re.sub(r'(?m)^\s*\d+\s*\n', '', testo)
    testo = re.sub(r'[©@]', '', testo)
    print(testo.strip())
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

def process_testo_liber(testo):
    testo = testo.replace('\x0c', '\n')
    pattern = (
        r'(?m)^\s*\d{1,3}\s*$'                    # riga con solo il numero di pagina
        r'(?:\n(?:Letteratura italiana Einaudi\s)\s*' # titolo (– o -)
        r'\n\s*Giovan Battista Basile - Lo cunto de li cunti*)?'                # autore (opzionale)
    )
    #pattern = (
    #    r'(?m)^\s*\d{1,3}\s*$'                    # riga con solo il numero di pagina
    #    r'(?:\n(?:Fiabe novelle e racconti popolari siciliani\s*[–-]\s*Vol\. IV)\s*' # titolo (– o -)
    #    r'\n\s*Giuseppe Pitrè\s*)?'                # autore (opzionale)
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
        
        # divide alla prima frase (terminata da . ! o ?)
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

def dividi_testo_per_frase(testo: str, max_parole: int) -> list[str]:
    """
    Divide un testo in blocchi più piccoli.
    
    Ogni blocco non supera il numero massimo di parole e il taglio avviene
    sempre alla fine dell'ultima frase completa inclusa.

    Args:
        testo: La stringa di testo completa da dividere.
        max_parole: La lunghezza massima (in parole) desiderata per ogni blocco.

    Returns:
        Una lista di stringhe (i blocchi di testo).
    """
    
    # 1. Definizione della punteggiatura che segna la fine di una frase.
    # Pattern per: punto, punto interrogativo o punto esclamativo, seguiti da spazio
    delimitatori_frase = r'(?<=[.?!])\s+'
    
    # 2. Dividere il testo in una lista di frasi complete
    frasi = re.split(delimitatori_frase, testo)
    
    # Pulizia: rimuove spazi iniziali/finali e frasi vuote
    frasi = [f.strip() for f in frasi if f.strip()]

    blocchi = []
    blocco_corrente = []
    conteggio_parole = 0
    
    for frase in frasi:
        # Contiamo le parole della frase corrente.
        parole_frase = len(frase.split())
        
        # Se includendo questa frase si supera il limite E il blocco corrente non è vuoto...
        if conteggio_parole + parole_frase > max_parole and blocco_corrente:
            # 1. Chiudiamo il blocco precedente.
            blocchi.append(" ".join(blocco_corrente))
            
            # 2. Iniziamo un nuovo blocco con la frase corrente.
            blocco_corrente = [frase]
            conteggio_parole = parole_frase
            
        # Altrimenti, aggiungiamo la frase al blocco corrente.
        else:
            blocco_corrente.append(frase)
            conteggio_parole += parole_frase

    # 3. Aggiungere l'ultimo blocco rimanente (se non è vuoto)
    if blocco_corrente:
        blocchi.append(" ".join(blocco_corrente))
        
    return blocchi

def process_pasolini(testo):
    testo = testo.replace('\x0c', '')

    pattern = (
        r'(?m)^\s*\d{1,3}\s*$'                    # riga con solo il numero di pagina
        r'(?:\n(?:Letteratura italiana Einaudi\s)\s*' # titolo (– o -)
        r'\n\s*Pier Paolo Pasolini - Ragazzi di vita*)?'                # autore (opzionale)
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

        LIMITE_MASSIMO_PAROLE = 150

        risultato = dividi_testo_per_frase(testo_racconto, LIMITE_MASSIMO_PAROLE)
        #frasi_racconto = testo_racconto.split(". ")
        for f in risultato:
            print(len(f))
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
        r'(?m)^\s*\d{1,3}\s*$'                    # riga con solo il numero di pagina
        r'(?:\n(?:Letteratura italiana Einaudi\s)\s*' # titolo (– o -)
        r'\n\s*Pier Paolo Pasolini - Ragazzi di vita*)?'
        r"\[.*?\]|\(.*?\)" 
        r"\*"            # autore (opzionale)
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
            print(len(f))
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
    lunghezza_frasi = 200

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
            print("\n\n\n---------------------------------------------------\n\n\n")
            if len(testo_racconto) > 2:
                data.append({
                    "text":f,
                })
        
    return data

def process_testo_liber_nap(testo):
    testo = testo.replace('\x0c', '')
    pattern = (
        r'(?m)^\s*\d{1,3}\s*$'                    # riga con solo il numero di pagina               # autore (opzionale)
    )
    data=[]
    testo = re.sub(pattern, '', testo, flags=re.IGNORECASE)

    frase = "Letteratura italiana Einaudi"  # <-- sostituisci con la frase che vuoi
    pattern = rf".*{re.escape(frase)}.*\n?"
    testo = re.sub(pattern, '', testo, flags=re.IGNORECASE)
    frase = "Giovan Battista Basile - Lo cunto de li cunti"  # <-- sostituisci con la frase che vuoi
    pattern = rf".*{re.escape(frase)}.*\n?"
    testo = re.sub(pattern, '', testo, flags=re.IGNORECASE)


    blocchi = testo.split("\n\n\n")
    
    for racconto in blocchi:
        racconto=racconto.strip()
        #remove the \n and the - characters, as well as \n\n and double/triple spaces
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
        r'(?m)^\s*\d{1,3}\s*$'                    # riga con solo il numero di pagina
        r'(?:\n(?:Fiabe novelle e racconti popolari siciliani\s*[–-]\s*Vol\. II)\s*' # titolo (– o -)
        r'\n\s*Giuseppe Pitrè\s*)?'                # autore (opzionale)
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

        # 1. elimina righe tipo "parola:"
        if re.match(r"^[A-Za-zÀ-ÿ'\-]+:$", linea):
            continue
        
        # 2. elimina righe di definizioni tipo "s. f.", "s. m.", "v. tr.", "v. intr."
        if re.match(r"^(s\.\s*[fm]\.|v\.\s*(tr|intr)\.)", linea):
            continue

        # 3. elimina righe vuote multiple (opzionale)
        # if linea == "":
        #     continue

        pulite.append(r)

    return "\n".join(pulite)

def process_testo_torrese(testo):
    data =[]
    pattern = r"\*\*\*.*?(?=(?:\*\*\*)|$)"

    # re.S makes . match newlines
    blocchi = re.findall(pattern, testo, flags=re.S)

    # Stampa per controllo
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

data =process_pasolini(testo)

with open(f"../corpus_tesi/romanesco/verga/{NAME}_processed.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)
    
    
    