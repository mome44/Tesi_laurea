import re
import json
import random



NAME = "reddit_romano_processed"
DIALECT = "rom"
TYPE = "book"
MAX_PAROLE = 130
OUTPUT_PATH = f"../corpus/samples"

with open(f"../corpus/{DIALECT}_{TYPE}_refined.json", "r", encoding="utf-8") as f:
    data = json.load(f)

def visualizza_testo(data, filler):
    total_text = ""
    i=0
    data_2 = []
    for item in data:
        
        testo = item["text"]
        if i==0:
            total_text +=testo
        else:
            total_text += filler+ testo
        i+=1
    
    print(total_text)
    data_2.append({"text": total_text.strip()})
    #parts = re.split(r"(?=(?:^|\n)[A-ZÀ-Ù][A-ZÀ-Ù0-9'’\-\s]{3,})", total_text)
    #for j in parts:
    #    if len(j.strip()) > 3:
    #        data_2.append({"text": j.strip()})
    return data_2


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

def estrai_qa_sample(data):
    data_2 = []
    for item in data:
        testo = item["text"]
        risultato = dividi_testo_per_frase(testo, MAX_PAROLE)

        print("\n ", len(risultato))
        if len(risultato)>= 5:
            numeri = random.sample(range(0, len(risultato)), 2)
            a, b = numeri
            data_2.append({
                "text": risultato[a]
            })
            if len(risultato)>= 10:
                data_2.append({
                    "text": risultato[b]
                })
        #print(risultato[0])
    return data_2


data = estrai_qa_sample(data)

with open(f"{OUTPUT_PATH}/{DIALECT}_{TYPE}.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)
    
    
    