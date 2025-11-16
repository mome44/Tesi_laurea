import os
import json
from transformers import AutoTokenizer

LINGUA = "siciliano"

cartella = f"corpus_tesi/{LINGUA}"

#tokenizer
tokenizer = AutoTokenizer.from_pretrained("sapienzanlp/Minerva-7B-base-v1.0", use_fast=True)


sottocartelle = ["commedia", "parafrasi", "prosa", "poesia"]

result = {}
totale = 0
totale_prosa = 0
for cart in sottocartelle:
    total_text_num = []
    cartelladet = cartella + "/" + cart
    for filename in os.listdir(cartelladet):
        if filename.endswith(".json"):
            percorso_file = os.path.join(cartelladet, filename)
            with open(percorso_file, "r", encoding="utf-8") as f:
                try:
                    data = json.load(f)

                    for item in data:
                        if "text" in item:
                            tokens = tokenizer.encode(
                                item["text"],
                                add_special_tokens=False
                            )
                            total_text_num.append(len(tokens))
                except json.JSONDecodeError:
                    print(f"The file is not a JSON")
    num_tokens = sum(total_text_num)
    
    result[cart] = num_tokens  # <-- salva nel dict
    print(f"Numero totale di token {cart}: {num_tokens}")

    totale+=num_tokens

    if cart ==  "parafrasi" or cart == "prosa":
        totale_prosa+=num_tokens
#tokens = tokenizer.encode(testo_completo)



with open (f"{cartella}/token_{LINGUA}.txt", "w", encoding="utf-8") as f:
    for categoria, count in result.items():
        f.write(f"{categoria} : {count}\n")
    
    f.write(f"totale : {totale}\n")

    f.write(f"totale prosa : {totale_prosa}\n")



