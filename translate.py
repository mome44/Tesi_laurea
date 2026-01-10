from google import genai
from google.genai.errors import APIError
import pandas as pd
import time
import random
import json
import os
from dotenv import load_dotenv
import os

load_dotenv()
k1 = os.getenv("GEM_API_1")
k2 = os.getenv("GEM_API_2")
k3 = os.getenv("GEM_API_3")
k4 = os.getenv("GEM_API_4")
k5 = os.getenv("GEM_API_5")
k6 = os.getenv("GEM_API_6")
k7 = os.getenv("GEM_API_7")
k8 = os.getenv("GEM_API_8")
k9 = os.getenv("GEM_API_9")
k10 = os.getenv("GEM_API_10")
k11 = os.getenv("GEM_API_11")

PATH = f"corpus/evaluation/parsed/tre"
OUTPUT_PATH = f"corpus/evaluation/parsed/transl"
API_KEY_LIST = [k1,k2,k3,k4,k5,k6,k7,k8,k9,k10,k11]
MODEL_NAME = "gemini-2.5-flash"
df = pd.read_csv("Q&A dialect thesis - Q&A.csv")

LAST_FILE = 0
api_idx = 1

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

i = 126
total_length = len(df) #dataset delle domande

df["Translation"] = None
print(df.columns)

results=[]

total_length = len(df)

while i < total_length:
    api_key = API_KEY_LIST[api_idx]

    row = df.iloc[i] 
    print(f"Question ------ {i+1}/{total_length} -------")
    dialect = row["Dialect"]
    full_text = row["Full text"]

    with open(f"prompt/prompt_trad_{dialect}.txt", "r", encoding = "utf-8") as p:
        prompt = p.read()

    prompt_input = prompt + "\n\n" + full_text
    print(prompt_input)
    response = gemini_api_call(prompt_input, MODEL_NAME, API_KEY=api_key)
    if response == 0:
        print("Retrying due to server issues")
        continue
    if response:
        df.at[i, "Translation"] = response.strip()
        df.at[i+1, "Translation"] = response.strip()
        i +=2
        num_api_call+=1
    
    if response is None:
        print(f"Errore a step {num_api_call}")
        df.to_csv(f"results/transl/Q&A dialect thesis translated - Q&A_partial_{i}.csv", index=False)
        api_idx +=1
        continue
    
    print("saving checkpoint")
    df.to_csv(f"results/transl/Q&A dialect thesis translated - Q&A_partial_{i}.csv", index=False)
    
#saving the translation
df.to_csv("Q&A dialect thesis translated - Q&A.csv", index=False)
