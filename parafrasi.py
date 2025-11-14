from google import genai
from google.genai.errors import APIError
import time
import random
import json
import os


#API_KEY = "AIzaSyDAM3VU2O7RClzARfcjVr-WFtO-oEWsZTE" #prima
#API_KEY = "AIzaSyCKynyTujWmvIYiOaLxnpuuvUevgFUx5fQ" #Seconda
API_KEY = "AIzaSyA5aGoN_UAs6QznnGP8Jpa4bh3vqEV8XYk" #TERZA
# --- Configurazioni ---
MODEL_NAME = "gemini-2.5-flash"

DIALECT = "romanesco"
TIPO = "poesia"
PATH = f"corpus_tesi/{DIALECT}/{TIPO}"
OUTPUT_PATH = f"corpus_tesi/{DIALECT}/parafrasi"
LAST_FILE = 126

with open(f"prompt_{DIALECT}_{TIPO}.txt", "r", encoding = "utf-8") as p:
    prompt = p.read()

def format_input(data, type):
    if type == "commedia":
        num_righe = 10
        i = 0
        result = []
        formatted_text = ""
        for item in data:
            if i == num_righe:
                i = 0
                result.append(formatted_text)
                formatted_text = ""
            text = item["text"].replace("\n", " ").strip()
            if "character" in item:
                character = item["character"]
                formatted_text += f"{character} : {text} \n"
            else:
                formatted_text += f"{text} \n"
            i+=1
        return result
    else:
        result = []
        for item in data:
            result.append(item["text"])
        return result


def gemini_api_call(prompt, model_name):
    max_retries = 5
    response = None
    for attempt in range(1, max_retries):
        try:
            time.sleep(random.uniform(7, 8))  #controling our request rate
            try:
                client = genai.Client(api_key=API_KEY)
            except Exception as e:
                print("ERRORE: Impossibile inizializzare il client.")
                print(f"Dettagli: {e}")
                return None
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
            )
            # 3. Estrai e stampa il conteggio dei token
            if response.usage_metadata:
                usage = response.usage_metadata
                print("USO DEI TOKEN PER QUESTA CHIAMATA:")
                print(f"  Token di Input (Prompt): {usage.prompt_token_count}")
                print(f"  Token di Output (Risposta): {usage.candidates_token_count}")
                print(f"  Token Totali Consumati: {usage.total_token_count}")
            else:
                print("ATTENZIONE: Metadati d'uso dei token non disponibili nella risposta.")

            
            return response.text
        except APIError as e:
            wait_time = 3 ** attempt  # Esponezially più lungo
            print(f"ERRORE: {e}. Riprovo in {wait_time} secondi...")
            if attempt < max_retries - 1:
                time.sleep(wait_time)
            else:
                if hasattr(e, 'status_code') and e.status_code == 503:
                    # Questo è il codice 503 specifico che vuoi intercettare
                    print("Errore 503 rilevato dopo il max di tentativi.")
                    return 0 
                # 2. SE IL CODICE NON È DISPONIBILE, USA LA RAPPRESENTAZIONE STRINGA CON PRUDENZA
                # Controlla solo se il codice 503 è presente nella stringa dell'errore
                elif "503 UNAVAILABLE" in str(e): 
                    print("Errore 503 rilevato tramite stringa dopo il max di tentativi.")
                    return 0
                print("Raggiunto il numero massimo di tentativi. Impossibile completare la richiesta.")
                print("Controlla i tuoi limiti di utilizzo sulla dashboard di Google AI Studio.")
                return None
        
        except Exception as e:
            print(f"ERRORE API (Potrebbe essere una limitazione di quota): {e}")
            print("Verifica l'utilizzo della tua API in Google AI Studio per non eccedere il piano gratuito.")
            return None

num_api_call=0
errore = False
for filename in os.listdir(PATH):
    full_path = os.path.join(PATH,filename)
    #skipping the paraphrased files
    if "processed.json" in filename:
        nome_file = filename.strip("processed.json")
    else:
        continue
    
    if os.path.isfile(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    
    result = format_input(data, TIPO)
    print(f"starting with {nome_file}\n")

    result_data = []
    index = 0
    while index < len(result):
        if index < LAST_FILE:
            index=LAST_FILE
            continue
        part = result[index]
        print(f"processing {num_api_call} - {nome_file}: file index {index}/{len(result)}")
        prompt_input = prompt + part

        response = gemini_api_call(prompt_input, MODEL_NAME)
        if response == 0:
            print("Retrying due to server issues")
            continue

        if response:
            result_data.append({
                "text": response.strip()
            })
            index +=1

        if response is None:
            print(f"Errore a step {num_api_call}")
            with open(f"{OUTPUT_PATH}/{nome_file}paraphrased_partial_{index-1}.json", "w", encoding="utf-8") as out:
                json.dump(result_data, out, ensure_ascii=False, indent=2)
            errore=True
            break

        num_api_call+=1
    if errore:
        break
    if num_api_call == 250:
        break
    print(f"finished with {nome_file}\n")
    
    #saving the paraphrasis
    with open(f"{OUTPUT_PATH}/{nome_file}paraphrased.json", "w", encoding="utf-8") as out:
        json.dump(result_data, out, ensure_ascii=False, indent=2)
    
    #renaming the old file
    os.rename(full_path, f"{PATH}/{nome_file}finished.json")
    
    
    


    
