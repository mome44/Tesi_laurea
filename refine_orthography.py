import json
import pandas as pd
import os
import re

DIALECT = "romanesco"
TIPO = "parafrasi"
PATH = f"corpus_tesi/{DIALECT}/{TIPO}"
OUTPUT_PATH = f"corpus_tesi/{DIALECT}/parafrasi_standard"

def refine_siciliano(testo):
    testo_standardizzato = testo
    return testo_standardizzato

def refine_romano(testo):
    testo = re.sub(r"\b(del)\b", "der", testo)
    testo = re.sub(r"\b(della)\b", "de la", testo)
    testo = re.sub(r"\b(delle)\b", "de le", testo)
    testo = re.sub(r"\b(degli|dei)\b", "de li", testo)

    testo = re.sub(r"\b(il|el)\b", "er", testo)
    testo = re.sub(r"\b(i)\b", "li", testo)

    testo = re.sub(r"\bdi\b", "de", testo)
    testo = re.sub(r"\bmi\b", "me", testo)
    testo = re.sub(r"\bti\b", "te", testo)

    testo = re.sub(r"gli", "jj", testo)
    testo = re.sub(r"\bcaldo\b", "callo", testo)
    testo = re.sub(r"\b([A-Za-z]+)are\b", r"\1à", testo)
    testo = re.sub(r"\b([A-Za-z]+)ere\b", r"\1e'", testo)
    testo = re.sub(r"\b([A-Za-z]+)ire\b", r"\1ì", testo)

    testo_standardizzato = testo
    return testo_standardizzato

def refine_napoletano(testo):
    
    #preposizioni articolate
    testo = re.sub(r"\b(de lo|delo|del|di lo)\b", "d''o", testo)
    testo = re.sub(r"\b(de la|della|dela|di la)\b", "d''a", testo)
    testo = re.sub(r"\b(de le|delle|dele|di le|de li|delli|deli|di li|dei)\b", "d''e", testo)
    testo = re.sub(r"\b(de ll'|dell'|de l'|degli)\b", "'e ll'", testo)
    testo = re.sub(r"\b(de|di)\b", "'e", testo)

    testo = re.sub(r"\b(a lo|al|allo|a il)\b", "a'o", testo)
    testo = re.sub(r"\b(a la|alla)\b", "a'a", testo)
    #continuare

    #articoli
    testo = re.sub(r"\b(lo|il|el|er|lu|'o|’o|u)\b", "'o", testo)
    testo = re.sub(r"\b(Lo|Il|El|Er|Lu|'O|’O|u)\b", "'O", testo)
    testo = re.sub(r"\b(la|’a)\b", "'a", testo)
    testo = re.sub(r"\b(La|’A)\b", "'A", testo)

    testo = re.sub(r"\b(uno|un|nu|'no|'nu|’no|’nu)\b", "nu")
    testo = re.sub(r"\b(Uno|Un|Nu|'No|'Nu|’No|’Nu)\b", "Nu")
    testo = re.sub(r"\b(una|na|'na|’na)\b", "na")
    testo = re.sub(r"\b(Una|Na|'Na|’Na)\b", "Na")

    testo = re.sub(r"\b(li|le|'e|’e|’i)\b", "'e", testo)
    testo = re.sub(r"\b(Li|Le|'E|’E|’I)\b", "'e", testo)

    testo = re.sub(r"\bcinque", "cinche", testo)
    testo = re.sub(r"\bdisse\b", "dicette", testo)
    testo = re.sub(r"\bdissero\b", "dicettero", testo)
    testo = re.sub(r"(?!q)ue(?!\b)", "uo", testo)

    # C. Infinito italiano → napoletano (are→à, ere→é, ire→ì)
    testo = re.sub(r"\b([A-Za-z]+)are\b", r"\1à", testo)
    testo = re.sub(r"\b([A-Za-z]+)ere\b", r"\1e'", testo)
    testo = re.sub(r"\b([A-Za-z]+)ire\b", r"\1ì", testo)
    print(testo)
    # D. Convertire apostrofo standard
    testo_standardizzato = testo
    return testo_standardizzato

def refine(Dialetto, testo):
    if Dialetto == "napoletano":
        return refine_napoletano(testo)
    elif Dialetto == "siciliano":
        return refine_siciliano(testo)
    elif Dialetto == "romanesco":
        return refine_romano(testo)
    else:
        return ""
    

for filename in os.listdir(PATH):
    full_path = os.path.join(PATH,filename)
    print("processing ", filename)

    if os.path.isfile(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    errore = False
    data_refined = []
    for item in data:
        testo = item["text"]
        testo_nuovo = refine(Dialetto = DIALECT, testo=testo)
        if testo_nuovo == "":
            print("errore dialetto non trovato o altro")
            errore = True
            break
        data_refined.append({
            "text": testo_nuovo
        })
    if not errore:
        with open(f"{OUTPUT_PATH}/{filename}_refined.json", "w", encoding="utf-8") as out:
            json.dump(data_refined, out, ensure_ascii=False, indent=2)
#
#
#with open("sicilian/wiki_index_55500.json", "r", encoding="utf-8") as f:
#    data = json.load(f)
#
#df = pd.DataFrame(list(data.items()), columns=["chiave", "valore"])
#
#col = "valore"  # o "valore", se è quella che ti interessa
#
#tmp = df.copy()
#tmp["_norm"] = (
#    tmp[col]
#    .astype(str)          # uniforma tipi misti
#    .str.strip()          # toglie spazi
#    .str.casefold()       # confronto case-insensitive (meglio di lower())
#)
#
#df_no_dup = tmp[~tmp["_norm"].duplicated(keep="first")].drop(columns="_norm")
#df_no_dup["valore"] = df_no_dup["valore"].str.replace(r"\S*Pi favuri, agghiunci na lijami a sta pàggina e scancella st'abbisu.\nPâ lista cumpleta dî pàggini òrfani, vidi a pàggina dâ catigurìa.\S*", "", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()
#
#df_no_dup = df_no_dup[df_no_dup["valore"].str.len() >= 4]
#
#patterns = [r"^Lu\s+\d+\s*\([IVXLCDM]+\s+a nùmmaru rumanu\)\s+è n'annu\b", r"^L'\d+\s*\([IVXLCDM]+\s+a nùmmaru rumanu\)\s+è n'annu", 
#            r"Pì arrìpurtari cchìu immediatamenti i diffìrenzi tra li diversi ordini di grannizza, chista paggina cunteni",
#            r"Pì arrìpurtari cchìu immediatamenti i diffìrenzi tra li diversi ordini di grannizza, chista pàggina cunteni",
#            r"^\.[a-z]{2}\s+è lu duminiu di Internet assignatu"]
#
#for p in patterns:
#    to_drop = df_no_dup["valore"].astype(str).str.contains(p, na=False, regex=True)
#    df_no_dup = df_no_dup.loc[~to_drop].reset_index(drop=True)
#
#
#
#print(df_no_dup,len(df_no_dup))
#
#testo_unico = "\n".join(df_no_dup["valore"].astype(str))
#
#print(len(testo_unico))
## se preferisci con newline tra una riga e l'altra:
## testo_unico = "\n".join(df_clean["valore"].astype(str))
#
## salva su file di testo
#with open("output.txt", "w", encoding="utf-8") as f:
#    f.write(testo_unico)