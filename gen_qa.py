from google import genai
from google.genai.errors import APIError
import time
import random
import json
import os

API_KEY_LIST = [
    "AIzaSyDAM3VU2O7RClzARfcjVr-WFtO-oEWsZTE", #prima
    "AIzaSyCKynyTujWmvIYiOaLxnpuuvUevgFUx5fQ", #Seconda
    "AIzaSyA5aGoN_UAs6QznnGP8Jpa4bh3vqEV8XYk", #TERZA
    "AIzaSyAay0PJStTeZxxcuTn97RwmJzifefQEHS8", #QUARTA CAR
    "AIzaSyAf8vqpLY1mvNf03gvNQ8NDyP8drwXTP6s", #mich
    "AIzaSyAyS0Or4He8_ByQpINlDWXNKw6yMpdpJ7o", #p1
    "AIzaSyC9fknqBf7ogCScgSDNRsW0VDGH91PNFLg", #p2
    "AIzaSyDa0mJS5Bcx-qF3pYQ9mvb2ICTu0BsoPiU", #p3
    "AIzaSyDMyQo3NAh0DYKEparoxSxtuFO17-kJoZc", #p4
    "AIzaSyCJQZiXj85Ti3JJOdNHKTQbeURaknnVVqA"  #fedoe
]

# --- Configurazioni ---
MODEL_NAME = "gemini-2.5-flash"

DIALECT = "nap"

SPLITTING = {"nap_wiki":20, "nap_par":0, "rom_par":0, "nap_book":5, "scn_wiki":20, "scn_book":5, "rom_book":25}

PATH = f"corpus/evaluation/samples"
OUTPUT_PATH = f"corpus/evaluation/q_a"
LAST_FILE = 0
api_idx = 0

with open(f"prompt/prompt_gen_{DIALECT}.txt", "r", encoding = "utf-8") as p:
    prompt = p.read()
    print(prompt)


def gemini_api_call(prompt, model_name, API_KEY):
    max_retries = 5
    response = None
    for attempt in range(1, max_retries):
        try:
            time.sleep(random.uniform(8, 12))  #controling our request rate
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
                print(f"  Token di input (prompt): {usage.prompt_token_count}")
                print(f"  Token di output (risposta): {usage.candidates_token_count}")
                print(f"  Token totali consumati: {usage.total_token_count}")
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
    if ".json" in filename:
        name = filename.split(".")[0]
    else:
        continue
    num = SPLITTING[name]
    if num == 0:
        continue
    
    full_path = os.path.join(PATH,filename)
    if os.path.isfile(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    #data_sample = data[:num]
    data_sample =data
    LAST_FILE = num

    result_data = []
    index = 0
    increase = 1
    num = len(data)
    while index < num:
        api_key = API_KEY_LIST[api_idx]
        if index < LAST_FILE:
            index=LAST_FILE
            continue
        
        sentence_sample = data_sample[index]
        sentence = sentence_sample["text"]
        #question_1 = sentence_sample["Domanda"]
        #answer_1 = sentence_sample["Risposta"]
        #sentence_sample = data_sample[index + 1]
        #question_2 = sentence_sample["Domanda"]
        #answer_2 = sentence_sample["Risposta"]
        
        print(f"processing {num_api_call} api {api_idx} - {name}: file index {index}/{num}")
        
        prompt_input = prompt + '\"' + sentence + '\"'
        #prompt_input = prompt + '\nDomanda: ' + question_1 + '\nRisposta:' + answer_1 + '\nDomanda: ' + question_2 + '\nRisposta:' + answer_2 

        print(prompt_input)

        response = gemini_api_call(prompt_input, MODEL_NAME, API_KEY=api_key)
        if response == 0:
            print("Retrying due to server issues")
            continue
        if response:
            result_data.append({
                "text": response.strip()
            })
            index +=increase
        if response is None:
            print(f"Errore a step {num_api_call}")
            with open(f"{OUTPUT_PATH}/{name}_qa_g2_{index-increase}.json", "w", encoding="utf-8") as out:
                json.dump(result_data, out, ensure_ascii=False, indent=2)
            api_idx +=increase
            continue
        num_api_call+=1
        print("saving checkpoint")
        with open(f"{OUTPUT_PATH}/{name}_qa_g2_{index}.json", "w", encoding="utf-8") as out:
            json.dump(result_data, out, ensure_ascii=False, indent=2)
        
    if errore:
        break
    if num_api_call == 20:
        break
    print(f"finished with {name}\n")
    
    #saving the paraphrasis
    with open(f"{OUTPUT_PATH}/{name}_qa_g2.json", "w", encoding="utf-8") as out:
        json.dump(result_data, out, ensure_ascii=False, indent=2)
    
    
    


    
