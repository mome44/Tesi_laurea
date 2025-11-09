import re
import json
pattern = r"[A-Za-z]+\. [A-Za-z]+"

NAME = "leggiri_e_capiri_sicilianu_commedia_1"

with open(f"{NAME}.txt", "r", encoding="utf-8") as f:
    testo = f.read()

def parse_commedia_simple(testo):
    #print(testo)
    testo = testo.split("\n\n")

    data = []
    for l in testo:
        if re.search(pattern, l):
            l= re.sub(r'\d+', '', l)
            print(l)

            parti = re.split(r"\.\s*", l, maxsplit=1)
            print(parti)

            data.append({
                "character": parti[0].strip(),
                "text": parti[1].strip()
            })
    return data

def parse_commedia_teatro_romano(testo):
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)

    testo = re.sub(r"https://\S*", "", testo)

    testo = re.sub(r"(?m)^\s*[0-9][0-9\s/:,.\-]*\s*$", "", testo)

    # 4) Pulisci spazi doppi e righe vuote multiple
    testo = re.sub(r"[ \t]+", " ", testo)
    testo = re.sub(r"\n{3,}", "", testo).strip()
    data=[]

    print(testo)

    matches = re.finditer(r"(?ms)^(?P<attore>[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ' \-]*)\s*:\s*(?P<battuta>.*?(?=\n[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ' \-]*\s*:|$))",testo)
    for m in matches:
        speaker = m.group("attore").strip()
        line = " ".join(m.group("battuta").split())
        print(f"{speaker}: {line}")
        data.append({
                "character": speaker,
                "text": line,
            })
    return data

def parse_commedia_romana_multiline(testo):
    # 1) pulizie iniziali (come nella tua funzione)
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)
    testo = re.sub(r"HTTP://\S+", "", testo, flags=re.IGNORECASE)
    testo = re.sub(r"(?m)^\s*[0-9][0-9\s/:,.\-]*\s*$", "", testo)
    testo = re.sub(r"[ \t]+", " ", testo)
    # normalizziamo le interruzioni multiple ma lasciamo singole newline
    testo = re.sub(r"\n{3,}", "\n\n", testo).strip()

    data = []
    current_speaker = None
    current_parts = []

    # regex che riconosce una linea-inizio battuta:
    # es. "NANDO:" oppure "NANDO - testo" o "VECCHIO:    Testo iniziale"
    header_re = re.compile(r'^\s*(?P<attore>[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ0-9\'\.\(\) \-]+?)\s*[:\-]\s*(?P<rest>.*)$')

    for raw_line in testo.splitlines():
        line = raw_line.rstrip()
        if not line:
            # linea vuota: considerala come separatore logico ma mantieni se siamo in una battuta
            if current_speaker is not None:
                # aggiungiamo una linea vuota come separatore interno (opzionale)
                current_parts.append("") 
            continue

        m = header_re.match(line)
        if m:
            # flush precedente
            if current_speaker is not None:
                utterance = " ".join(p.strip() for p in current_parts if p is not None)
                utterance = re.sub(r'\s+', ' ', utterance).strip()
                data.append({"character": current_speaker, "text": utterance})
            # nuova battuta
            current_speaker = m.group("attore").strip()
            rest = m.group("rest").strip()
            current_parts = []
            if rest:
                current_parts.append(rest)
        else:
            # linea di continuazione: la prendiamo tutta (rimuovendo solo spazi estremi)
            # se la linea è indentata, la consideriamo comunque parte della battuta
            if current_speaker is None:
                # se non abbiamo speaker, tratto la riga come "UNKNOWN"
                current_speaker = "UNKNOWN"
                current_parts = [line.strip()]
            else:
                current_parts.append(line.strip())

    # flush finale
    if current_speaker is not None:
        utterance = " ".join(p.strip() for p in current_parts if p is not None)
        utterance = re.sub(r'\s+', ' ', utterance).strip()
        if len(utterance.strip()) > 2:
            data.append({"character": current_speaker, "text": utterance})

    return data

def parse_commedia_teatro_romano_2(testo):
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)

    testo = re.sub(r"HTTP://COPIONI.CORRIERESPETTACOLO.IT", "", testo)

    testo = re.sub(r"(?m)^\s*[0-9][0-9\s/:,.\-]*\s*$", "", testo)

    #Pulisci spazi doppi e righe vuote multiple
    testo = re.sub(r"[ \t]+", " ", testo)
    testo = re.sub(r"\n{3,}", "", testo).strip()
    data=[]

    print(testo)

    matches = re.finditer(
    r'(?ms)^(?P<attore>[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ\' \.\(\)]+?)\s*[–-]\s*[“"](?P<battuta>.*?)(?:[”"]\s*[-–]*\s*)?(?=\n[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ\' \.\(\)]+?\s*[–-]\s*[“"]|$)', testo)
    for m in matches:
        speaker = m.group("attore").strip()
        line = " ".join(m.group("battuta").split())
        print(f"{speaker}: {line}")
        data.append({
                "character": speaker,
                "text": line,
            })
    return data

def parse_commedia_teatro_romano_3(testo):
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)

    testo = re.sub(r"HTTP://\S*", "", testo)

    testo = re.sub(r"(?m)^\s*[0-9][0-9\s/:,.\-]*\s*$", "", testo)

    testo = re.sub(r'-\s*\n\s*', '', testo)
    testo = re.sub(r'\n+', ' ', testo)

    #Pulisci spazi doppi e righe vuote multiple
    testo = re.sub(r"[ \t]+", " ", testo)
    testo = re.sub(r"\n{3,}", "", testo).strip()
    data=[]

    print(testo)

    pattern = (
        r"(?s)(?<!\S)"
        r"(?P<attore>[0-9°ºA-ZÀ-ÖØ-Þ][0-9°ºA-ZÀ-ÖØ-Þ'’ .()]*)"
        r"\s*[–—-]\s*"
        r"(?P<battuta>.*?)"
        r"(?=(?<!\S)[0-9°ºA-ZÀ-ÖØ-Þ][0-9°ºA-ZÀ-ÖØ-Þ'’ .()]*\s*[–—-]\s|$)"
    )

    data = []
    for m in re.finditer(pattern, testo):
        speaker = m.group("attore").strip()
        line = " ".join(m.group("battuta").split())
        data.append({"character": speaker, "text": line})
    return data

def parse_commedia_semplice(testo):
    data =[]
    pattern = re.compile(r'^\s*([A-Za-zÀ-ÖØ-öø-ÿ]{3})\.\s*(.+)$', flags=re.M)

    for m in pattern.finditer(testo):
        personaggio = m.group(1)
        battuta = m.group(2)

        if len(battuta.strip()) > 2:
            data.append({
                "text": battuta.strip(),
                "character": personaggio.strip(),
            })
    return data

data = parse_commedia_semplice(testo)
#data = parse_commedia_simple(testo)
with open(f"../corpus_tesi/siciliano/commedia/{NAME}_processed.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)
    
    
    