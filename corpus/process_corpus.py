import os
import json
import re
import csv
# ====== USO ======
cartella = "evaluation/translated"
output = "evaluation/csv_final"


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

def parse_qa(cartella_input, file_output):
    #loop per i file in una cartella
    for nome_file in sorted(os.listdir(cartella_input)):

        if not nome_file.lower().endswith(".json"):
            continue

        if "nap" in nome_file:
            dialect = "Neapolitan"
        elif "rom" in nome_file:
            dialect = "Roman"
        elif "scn" in nome_file:
            dialect = "Sicilian"
        else:
            dialect = "_"

        percorso = os.path.join(cartella_input, nome_file)

        with open(percorso, "r", encoding="utf-8") as f:
            contenuto = json.load(f)
        data = []
        for item in contenuto:
            
        
            testo = item["text"]

            pattern = r"(?:\[(.*?)\]|([^#\n]+?))#(.*?)#"

            coppie=[]
            for g1, g2, risposta in re.findall(pattern, testo, flags=re.DOTALL):
                domanda = g1 if g1 else g2
                coppie.append((domanda.strip(), risposta.strip()))


            for domanda, risposta in coppie:
                print("Domanda:", domanda)
                print("Risposta:", risposta)

                data.append({
                    "Dialect" : "italian",
                    "Domanda": domanda,
                    "Risposta": risposta
                })
        with open(f"{file_output}/{nome_file}", "w", encoding="utf-8") as f:
           json.dump(data, f, ensure_ascii=False, indent=2)
        
def convert_csv(cartella_input, file_output):
    for nome_file in sorted(os.listdir(cartella_input)):

        if not nome_file.lower().endswith(".json"):
            continue


        if "nap" in nome_file:
            dialect = "Neapolitan"
        elif "rom" in nome_file:
            dialect = "Roman"
        elif "scn" in nome_file:
            dialect = "Sicilian"
        else:
            dialect = "_"

        percorso = os.path.join(cartella_input, nome_file)

        with open(percorso, "r", encoding="utf-8") as f:
            data = json.load(f)

        nome_file = nome_file.replace(".json", ".csv")
        # Apri CSV per scrivere
        with open(f"{file_output}/{nome_file}", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)

            # Scrivi intestazioni (colonne)
            writer.writerow(["Dialect", "Domanda", "Risposta"])

            # Scrivi le righe
            for item in data:
                writer.writerow([item["Dialect"],item["Domanda"],item["Risposta"]])

def compute_token(cartella_input, file_output):
    vocabulary = dict()
    for nome_file in sorted(os.listdir(cartella_input)):

        if not nome_file.lower().endswith(".json"):
            continue

        nome = nome_file.split(".")[0].replace("_refined", "_qa")
        percorso = os.path.join(cartella_input, nome_file)

        with open(percorso, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        if nome not in vocabulary:
            vocabulary[nome] = set()

        for item in data:
            #testo = item["text"]
            testo = item["Domanda"] + " " + item["Risposta"]
            testo = re.sub(r"[!?.,:;]", "", testo)
            
            testo = testo.lower()
            
            wordset = set(testo.split(" "))
            vocabulary[nome].update(wordset)
    
    vocabulary_json = {
        nome: sorted(list(words))
        for nome, words in vocabulary.items()
    }
    with open(f"{file_output}/generated_word_dictionary.json", "w", encoding="utf-8") as f:
        json.dump(vocabulary_json, f, ensure_ascii=False, indent=2)

def compute_token_similarity():
    with open("tok_dict/generated_word_dictionary.json", "r", encoding="utf-8") as f:
        gen_word_data = json.load(f)
    with open("tok_dict/word_dictionary.json", "r", encoding="utf-8") as f:
        word_data = json.load(f)
    total_nap_gen_word = set()
    total_scn_gen_word = set()
    total_rom_gen_word = set()
    total_nap_word = set()
    total_scn_word = set()
    total_rom_word = set()
    for domain, gen_word_list in gen_word_data.items():
        word_list = word_data[domain]
        gen_word_set = set(gen_word_list)
        word_set = set(word_list)
        intersezione = gen_word_set.intersection(word_set)

        if "nap" in domain:
            total_nap_gen_word.update(gen_word_set)
            total_nap_word.update(word_set)
        if "scn" in domain:
            total_scn_gen_word.update(gen_word_set)
            total_scn_word.update(word_set)
        if "rom" in domain:
            total_rom_gen_word.update(gen_word_set)
            total_rom_word.update(word_set)
        
        not_in_word_vocabulary = gen_word_set - intersezione
        #print(not_in_word_vocabulary)
        s=""
        for i in not_in_word_vocabulary:
            s+=i + " "
        
        #print(s)
        percentuale = (len(intersezione) / len(gen_word_set)) * 100 if word_set else 0
        print(f"Percentuale di tokens generati in comune per {domain} : {percentuale:.2f}%")
    
    intersezione_nap = total_nap_gen_word.intersection(total_nap_word)
    percentuale_nap = (len(intersezione_nap) / len(total_nap_gen_word)) * 100 if total_nap_word else 0
    
    print(f"\nTotale nap: {percentuale_nap:.2f}%")
    not_in_word_vocabulary = total_nap_gen_word - intersezione_nap
    s=""
    for i in not_in_word_vocabulary:
        s+=i + " | "
    
    print("Nap not in dictionary\n", s)
    
    intersezione_rom = total_rom_gen_word.intersection(total_rom_word)
    percentuale_rom = (len(intersezione_rom) / len(total_rom_gen_word)) * 100 if total_rom_word else 0

    print(f"\nTotale rom: {percentuale_rom:.2f}%")
    not_in_word_vocabulary = total_rom_gen_word - intersezione_rom
    s=""
    for i in not_in_word_vocabulary:
        s+=i + " | "
    
    print("Rom not in dictionary\n", s)
    
    intersezione_scn = total_scn_gen_word.intersection(total_scn_word)
    percentuale_scn = (len(intersezione_scn) / len(total_scn_gen_word)) * 100 if total_scn_word else 0

    print(f"\nTotale scn: {percentuale_scn:.2f}%")
    not_in_word_vocabulary = total_scn_gen_word - intersezione_scn
    s=""
    for i in not_in_word_vocabulary:
        s+=i + " | "
    
    print("Scn not in dictionary\n", s)

#compute_token(cartella, output)
#compute_token_similarity()

convert_csv(cartella, output)

#parse_qa(cartella, output)

#with open(file_output, "w", encoding="utf-8") as f:
#    json.dump(data, f, ensure_ascii=False, indent=2)

