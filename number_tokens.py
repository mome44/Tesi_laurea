import os
import json
from transformers import AutoTokenizer

LISTA_LINGUE = ["romanesco", "napoletano", "siciliano"]
#tokenizer
tokenizer = AutoTokenizer.from_pretrained("sapienzanlp/Minerva-7B-base-v1.0", use_fast=True)
sottocartelle = ["battute", "biografia","citazioni", "descrittiva", "incipit_opere", "narrativa_favole", "narrativa_storie", "notizie", "parafrasi_commedia", "parafrasi_poesia", "parafrasi_prosa", "poesia_formale", "poesia_sonetti","commedia", "wikipedia", "opus"]
 
for lingua in LISTA_LINGUE:
    LINGUA = lingua
    cartella = f"corpus_tesi/{LINGUA}"
    result = {}
    totale = 0
    totale_prosa_pura = 0
    totale_prosa = 0
    totale_parafrasi = 0
    totale_poesia = 0

    for cart in sottocartelle:
        total_text_num = []
        cartelladet = cartella + "/" + cart

        if not os.path.isdir(cartelladet):
            continue

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

        if cart in ["battute", "biografia", "citazioni", "descrittiva", "narrativa_favole", "narrativa_storie", "notizie"]:
            totale_prosa_pura+=num_tokens
        
        if cart in ["battute", "biografia", "citazioni", "descrittiva", "narrativa_favole", "narrativa_storie", "notizie", "parafrasi_commedia", "parafrasi_poesia", "parafrasi_prosa"]:
            totale_prosa +=  num_tokens
        
        if cart in ["poesia_sonetti", "poesia_formale"]:
            totale_poesia += num_tokens

        if cart in ["parafrasi_commedia", "parafrasi_poesia", "parafrasi_prosa"]:
            totale_parafrasi += num_tokens


    with open (f"{cartella}/token_{LINGUA}.txt", "w", encoding="utf-8") as f:
        for categoria, count in result.items():
            f.write(f"{categoria} : {count}\n")
        
        f.write("\n\n")

        f.write(f"totale prosa pura : {totale_prosa_pura}\n\n")
        
        f.write(f"totale prosa: {totale_prosa}\n\n")

        f.write(f"totale poesia: {totale_poesia}\n\n")

        f.write(f"totale parafrasi: {totale_parafrasi}\n\n")
        
        f.write("-----------------------------\n\n")

        f.write(f"totale : {totale}\n\n")

        



