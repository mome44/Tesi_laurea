import re
import json
pattern = r"[A-Za-z]+\. [A-Za-z]+"

NAME = "Meo_Patacca_er_Greve_e_Marco_Pepe_la_Cra"

with open(f"{NAME}.txt", "r", encoding="utf-8") as f:
    testo = f.read()

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

with open(f"../code_e_corpus_tesi/romanesco/{NAME}_processed.json", "w", encoding="utf-8") as out:
    json.dump(data, out, ensure_ascii=False, indent=2)
    
    
    