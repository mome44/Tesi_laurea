import re
import json

NAME = "VILLA DEGLI OLMI"

with open(f"{NAME}.txt", "r", encoding="utf-8") as f:
    testo = f.read()


def parse_commedia_wikisourcenap(testo, token):
    #token can be whichever character separates the character from their battuta
    parti = testo.split("\n\n")
    data =[]
    for p in parti:
        if token in p:
            sezione = p.split(token)
            character = sezione[0].strip()
            racconto = sezione[1].strip()
            #remove the parenthesis and its content from the text
            #since in comedies the part in parenthesis are in italian
            character = re.sub(r"\[.*?\]|\(.*?\)", "", character, flags=re.DOTALL)
            racconto = re.sub(r"\[.*?\]|\(.*?\)", "", racconto, flags=re.DOTALL)
            print(character, "\n", racconto)
            if len(racconto.strip())>3:
                data.append({
                    "character": character.strip(),
                    "text": racconto.strip()
                })
    return data
 
def parse_commedia_simple(testo):
    #the character is separated from the text by a dot + space
    testo = testo.split("\n\n")
    data = []
    pattern = r"[A-Za-z]+\. [A-Za-z]+"
    for l in testo:
        if re.search(pattern, l):
            #remove all the number (for the page numbers)
            l= re.sub(r'\d+', '', l)
            parti = re.split(r"\.\s*", l, maxsplit=1)
            data.append({
                "character": parti[0].strip(),
                "text": parti[1].strip()
            })
    return data

def parse_commedia_teatro_romano(testo):
    #remove the suggestion from the text
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)

    #remove the html website in the pdf
    testo = re.sub(r"https://\S*", "", testo)
    testo = re.sub(r"HTTP://COPIONI.CORRIERESPETTACOLO.IT", "", testo)

    #remove all the possible numbers including dates and indexes
    testo = re.sub(r"(?m)^\s*[0-9][0-9\s/:,.\-]*\s*$", "", testo)

    testo = re.sub(r"[ \t]+", " ", testo)
    testo = re.sub(r"\n{3,}", "", testo).strip()
    data=[]

    print(testo)
    
    matches = re.finditer(r"(?ms)^(?P<attore>[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ' \-]*)\s*[:–-–—-]\s*(?P<battuta>.*?(?=\n[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ' \-]*\s*:|$))",testo)
    for m in matches:
        character = m.group("attore").strip()
        line = " ".join(m.group("battuta").split())
        print(f"{character}: {line}")
        data.append({
                "character": character,
                "text": line,
            })
    return data

def parse_commedia_romana_multiline(testo):
    #remove the suggestion from the text
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)

    #remove the html website in the pdf
    testo = re.sub(r"https://\S*", "", testo)

    #remove all the possible numbers including dates and indexes
    testo = re.sub(r"(?m)^\s*[0-9][0-9\s/:,.\-]*\s*$", "", testo)

    testo = re.sub(r"[ \t]+", " ", testo)
    testo = re.sub(r"\n{3,}", "", testo).strip()

    data = []
    current_speaker = None
    #the list of the comedy lines
    current_parts = []

    #the actor is defined by only majuscule letters followed by : or - and then the rest
    #this works also in multiline context where the text il longer than a single line

    header_re = re.compile(r'^\s*(?P<attore>[A-ZÀ-ÖØ-Þ][A-ZÀ-ÖØ-Þ0-9\'\.\(\) \-]+?)\s*[:\-]\s*(?P<rest>.*)$')

    for riga in testo.splitlines():
        line = riga.rstrip()
        if not line:
            continue

        #find the matches for our pattern
        m = header_re.match(line)
        if m:
            #if there is a new current speaker we save the current situation
            if current_speaker is not None:
                battuta = ""
                for p in current_parts:
                    if p is not None:
                        battuta + = " " + p.strip()
                battuta = re.sub(r'\s+', ' ', battuta).strip()
                battuta = battuta.strip("—")
                battuta = battuta.strip("-")
                battuta = battuta.strip(".")

                if len(battuta.strip()) > 4:
                    data.append({"character": current_speaker, "text": battuta})
            
            current_speaker = m.group("attore").strip()
            rest = m.group("rest").strip()
            current_parts = []
            if rest:
                current_parts.append(rest)
        else:
            #if there is no match we take the line with character unknown
            if current_speaker is None:
                current_speaker = "UNKNOWN"
                current_parts = [line.strip()]
            else:
                current_parts.append(line.strip())

    battuta = ""
    for p in current_parts:
        if p is not None:
            battuta + = " " + p.strip()
    battuta = re.sub(r'\s+', ' ', battuta).strip()
    battuta = battuta.strip("—")
    battuta = battuta.strip("-")
    battuta = battuta.strip(".")

    if len(battuta.strip()) > 4:
        data.append({"character": current_speaker, "text": battuta})

    return data

def parse_commedia_semplice(testo):
    data =[]
    #three letters followed by a dot and a space
    pattern = re.compile(r'^\s*([A-Za-zÀ-ÖØ-öø-ÿ]{3})\.\s*(.+)$', flags=re.M)

    for m in pattern.finditer(testo):
        personaggio = m.group(1)
        battuta = m.group(2)
        battuta = re.sub(r"\[.*?\]|\(.*?\)", "", battuta, flags=re.DOTALL)
        personaggio = re.sub(r"\[.*?\]|\(.*?\)", "", personaggio, flags=re.DOTALL)
        if len(battuta.strip()) > 2:
            data.append({
                "text": battuta.strip(),
                "character": personaggio.strip(),
            })
    return data

def parse_commedia_semplice_2(testo):
    data =[]
    #majuscule actor name followed by two newlines
    pattern = re.compile(r'^([A-Z .]+)\n\n(.*?)(?=(?:\n[A-Z .]+\n\n)|\Z)', re.S | re.M)

    for m in pattern.finditer(testo):
        personaggio = m.group(1)
        battuta = m.group(2)
        battuta = re.sub(r"\[.*?\]|\(.*?\)", "", battuta, flags=re.DOTALL)

        if len(battuta.strip()) > 2:
            data.append({
                "text": battuta.strip(),
                "character": personaggio.strip(),
            })
    return data

def parse_commedia_semplice_3(testo):
    data =[]
    #new line and space after the actor name
    pattern = re.compile(r'([A-ZÀ-Ü\s]+)\n\s*(.+?)(?=\n[A-ZÀ-Ü\s]+\n|\Z)', re.DOTALL)

    for m in pattern.finditer(testo):
        personaggio = m.group(1)
        battuta = m.group(2)
        battuta = re.sub(r"\[.*?\]|\(.*?\)", "", battuta, flags=re.DOTALL)

        if len(battuta.strip()) > 2:
            data.append({
                "text": battuta.strip(),
                "character": personaggio.strip(),
            })
    return data

def parse_commedia_semplice_5(testo):
    data =[]
    #specific for sicilian comedy, since it has that the name of the actor should contain also apostrophes, which were not 
    #counted before
    pattern = re.compile(
    r"^([A-ZÀ-Ü][\w’'`\-àèéìòùÀÈÉÌÒÙḍḍîûçÇ]+)\s*\n(.+?)(?=\n[A-ZÀ-Ü][\w’'`\-àèéìòùÀÈÉÌÒÙḍḍîûçÇ]+\s*\n|^Scena|^Attu|\Z)",
    re.MULTILINE | re.DOTALL
    )

    for m in pattern.finditer(testo):
        personaggio = m.group(1)
        battuta = m.group(2)
        battuta = re.sub(r"\[.*?\]|\(.*?\)", "", battuta, flags=re.DOTALL)

        if len(battuta.strip()) > 2:
            data.append({
                "text": battuta.strip(),
                "character": personaggio.strip(),
            })
    return data

def parse_commedia_semplice_4(testo):
    #here they are simply separated by a :
    data =[]
    elenco_batt = testo.split("\n\n")

    for batt in elenco_batt:
        if ":" in batt:
            parti = batt.split(":",1)
            personaggio = parti[0]
            battuta = parti[1]
            battuta = re.sub(r"\[.*?\]|\(.*?\)", "", battuta, flags=re.DOTALL)

            if len(battuta.strip()) > 2:
                data.append({
                    "text": battuta.strip(),
                    "character": personaggio.strip(),
                })
    return data

data = parse_commedia_romana_multiline(testo)
#data = parse_commedia_simple(testo)

with open(f"../corpus_tesi/siciliano/commedia/{NAME}_processed.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)
    
    
    