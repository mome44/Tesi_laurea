import re
import json
pattern = r"[A-Za-z]+\. [A-Za-z]+"

NAME = "GORINI Lucia Rosa__Ieri oggi… romani__null__null__Musical__7q"

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


def parse_commedia_teatro_romano_2(testo):
    testo = re.sub(r"\[.*?\]|\(.*?\)", "", testo, flags=re.DOTALL)

    testo = re.sub(r"https://\S*", "", testo)

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



data = parse_commedia_teatro_romano_3(testo)
#data = parse_commedia_simple(testo)
with open(f"../code_e_corpus_tesi/romanesco/{NAME}_processed.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)
    
    
    