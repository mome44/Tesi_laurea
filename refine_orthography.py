import json
import pandas as pd
import os


DIALECT = "romanesco"
TIPO = "parafrasi"
PATH = f"corpus_tesi/{DIALECT}/{TIPO}"
OUTPUT_PATH = f"corpus_tesi/{DIALECT}/parafrasi_standard"

def refine_siciliano(testo):
    testo_standardizzato = testo
    return testo_standardizzato

def refine_romano(testo):
    testo_standardizzato = testo
    return testo_standardizzato

def refine_napoletano(testo):
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


with open("sicilian/wiki_index_55500.json", "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(list(data.items()), columns=["chiave", "valore"])

col = "valore"  # o "valore", se è quella che ti interessa

tmp = df.copy()
tmp["_norm"] = (
    tmp[col]
    .astype(str)          # uniforma tipi misti
    .str.strip()          # toglie spazi
    .str.casefold()       # confronto case-insensitive (meglio di lower())
)

df_no_dup = tmp[~tmp["_norm"].duplicated(keep="first")].drop(columns="_norm")
df_no_dup["valore"] = df_no_dup["valore"].str.replace(r"\S*Pi favuri, agghiunci na lijami a sta pàggina e scancella st'abbisu.\nPâ lista cumpleta dî pàggini òrfani, vidi a pàggina dâ catigurìa.\S*", "", regex=True).str.replace(r"\s+", " ", regex=True).str.strip()

df_no_dup = df_no_dup[df_no_dup["valore"].str.len() >= 4]

patterns = [r"^Lu\s+\d+\s*\([IVXLCDM]+\s+a nùmmaru rumanu\)\s+è n'annu\b", r"^L'\d+\s*\([IVXLCDM]+\s+a nùmmaru rumanu\)\s+è n'annu", 
            r"Pì arrìpurtari cchìu immediatamenti i diffìrenzi tra li diversi ordini di grannizza, chista paggina cunteni",
            r"Pì arrìpurtari cchìu immediatamenti i diffìrenzi tra li diversi ordini di grannizza, chista pàggina cunteni",
            r"^\.[a-z]{2}\s+è lu duminiu di Internet assignatu"]

for p in patterns:
    to_drop = df_no_dup["valore"].astype(str).str.contains(p, na=False, regex=True)
    df_no_dup = df_no_dup.loc[~to_drop].reset_index(drop=True)



print(df_no_dup,len(df_no_dup))

testo_unico = "\n".join(df_no_dup["valore"].astype(str))

print(len(testo_unico))
# se preferisci con newline tra una riga e l'altra:
# testo_unico = "\n".join(df_clean["valore"].astype(str))

# salva su file di testo
with open("output.txt", "w", encoding="utf-8") as f:
    f.write(testo_unico)