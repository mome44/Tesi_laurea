import os
import json


def unifica_json(cartella_input, file_output):
    testi_unificati = []
    data=[]
    #loop per i file in una cartella
    for nome_file in sorted(os.listdir(cartella_input)):

        if not nome_file.lower().endswith(".json"):
            continue

        percorso = os.path.join(cartella_input, nome_file)

        with open(percorso, "r", encoding="utf-8") as f:
            contenuto = json.load(f)

        for item in contenuto:
            
        
            testo = item["text"]

            data.append({
                "text": testo
            })

    with open(file_output, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ====== USO ======
cartella = "../corpus_tesi/romanesco/parafrasi_refined"
output = "rom_par_refined.json"

unifica_json(cartella, output)