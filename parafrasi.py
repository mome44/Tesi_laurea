from google import genai
from google.genai.errors import APIError
import time
import random
import json
def format_input_sonetti(data):
    
    return data

def format_input_commedie(data):
    num_righe = 5
    i = 0
    result = []
    formatted_text = ""
    for item in data:
        if i == num_righe:
            i = 0
            result.append(formatted_text)
            formatted_text = ""
        character = item["character"]
        text = item["text"].replace("\n", " ").strip()
        formatted_text += f"{character} : {text} \n"
        i+=1
    return result


API_KEY = "AIzaSyDAM3VU2O7RClzARfcjVr-WFtO-oEWsZTE"

# --- Configurazioni ---
MODEL_NAME = "gemini-2.5-flash"
PROMPT_incipit = "Spiegami in due paragrafi il concetto di MLOps, evidenziando il ruolo dell'automazione."
PROMPT_request = "aok "
def gemini_api_call(prompt, model_name):
    try:
        client = genai.Client(api_key=API_KEY)
    except Exception as e:
        print("ERRORE: Impossibile inizializzare il client.")
        print(f"Dettagli: {e}")
        return None
    max_retries = 5
    response = None
    for attempt in range(max_retries):
        try:
            time.sleep(random.uniform(6, 8))  #controling our request rate
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

            print(response.text)
            return response.text
        except APIError as e:
            wait_time = 2 ** attempt  # Esponezially più lungo
            print(f"ERRORE: {e}. Riprovo in {wait_time} secondi...")
            if attempt < max_retries - 1:
                time.sleep(wait_time)
            else:
                print("Raggiunto il numero massimo di tentativi. Impossibile completare la richiesta.")
                print("Controlla i tuoi limiti di utilizzo sulla dashboard di Google AI Studio.")
                return None
        
        except Exception as e:
            print(f"ERRORE API (Potrebbe essere una limitazione di quota): {e}")
            print("Verifica l'utilizzo della tua API in Google AI Studio per non eccedere il piano gratuito.")
            return None


#response = chiama_gemini_con_controllo_token(PROMPT, MODEL_NAME)


FILE_NAME = "Meo_Patacca_er_Greve_e_Marco_Pepe_la_Cra_processed"
DIALECT = "romanesco"
with open(f"code_e_corpus_tesi/{DIALECT}/{FILE_NAME}.json", "r", encoding="utf-8") as f:
    data = json.load(f)

result = format_input_commedie(data)
print(result[0])
for part in result:
    prompt = PROMPT_incipit + part + PROMPT_request

    #response = gemini_api_call(prompt, MODEL_NAME)

#
## evaluation loop
#for idx, row in df.iterrows():
#    #if(idx + 1) < 67:
#    #    continue
#    print(f"\nEvaluating sentence {idx}")
#    original = row['Sentence']
#
#    
#    translation = row[model_name]
#    prompt = f"""You are an expert evaluating modern Italian translations of an archaic sentence.
#        Original: {original}
#        Translation: {translation}
#        Please evaluate your translation exactly in this format, following the rubric:
#        Overall Score: <number from 1 to 5>
#        Feedback: <short explanation>
#        """
#    try:
#        max_retries = 5
#        response = None
#        for attempt in range(max_retries):
#            try:
#                time.sleep(random.uniform(6, 8))  #controling our request rate
#                response_obj = chat.send_message(prompt)
#                response = response_obj.text.strip()
#                break  #exit loop if success
#            except Exception as e:
#                wait_time = 2 ** attempt
#                print(f"Gemini error at row {idx}, model {model_name} (attempt {attempt+1}): {e}")
#                if attempt == max_retries - 1:
#                    response = "Gemini failed after retries. Score = 1"
#                else:
#                    time.sleep(wait_time)
#        print(f"Gemini response for {model_name}, row {idx}:\n{response}\n---")
#        overall_score = None
#        feedback = ""
#        #debug option: store raw response in the dataframe
#        df.at[idx, f'{model_name}_RawResponse'] = response
#        #parse line by line
#        for line in response.split('\n'):
#            line = line.strip()
#            if line.startswith("Overall Score:"):
#                score_text = line.split(':')[1].strip()
#                overall_score = safe_parse_score(score_text)
#            if line.startswith("Feedback:"):
#                feedback = line.split('Feedback:', 1)[1].strip()
#        if overall_score is None:
#            overall_score = 1
#            feedback += " (Score not found, defaulted to 1)"
#        # save to df
#        df.at[idx, f'{model_name}_Score'] = overall_score
#        df.at[idx, f'{model_name}_Feedback'] = feedback
#    except Exception as e:
#        print(f"Error at row {idx}, model {model_name}: {e}")
#        df.at[idx, f'{model_name}_Score'] = 1
#        df.at[idx, f'{model_name}_Feedback'] = "Error"
#
#    # save results parthially since we faced so many API problems
#    output_path = f'{path_to_shared_folder}ev_partial/gemini/gemini_evaluation_results_line{idx +1}.jsonl'
#    df.to_json(output_path, orient='records', lines=True, force_ascii=False)
#    print(f"Partial results saved to to {output_path}")
#
#
#print(f"\nDone evaluating all sentences.")
#