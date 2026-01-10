import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from datetime import datetime

#hyperparameters

#path locale per minerva 7b instruct se usi un'altro path puoi cambiare questa variabile
#ho scaricato minerva 7b instruct con huggingface e l'ho salvata nella cartella con questo nome
MODEL_PATH = "minerva-350M"

MAX_NEW_TOKENS = 250
TEMPERATURE = 0.7
TOP_P = 0.9

#codice che ho usato per scaricare minerva 7b instruct

#from huggingface_hub import snapshot_download
#snapshot_download(
#    repo_id="sapienzanlp/Minerva-7B-instruct-v1.0",
#    local_dir="minerva-7b-instruct",
#    local_dir_use_symlinks=False
#)

 
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, device_map="auto")

model.eval()

#dataset delle domande
df = pd.read_csv("Q&A_transl.csv")
print(df.columns)

results=[]

i = 0
total_length = len(df)
for idx, row in df.iterrows():
    print(f"Question ------ {i+1}/{total_length} -------")

    ai_model = row["AI model"]
    dialect = row["Dialect"]
    domain = row["Domain"]
    gemini_question = row["Italian question"]
    gemini_answer = row["Italian answer"]
    full_text = row["Full text"]
    italian_text = row["Translation"]

    #low baseline call --- just the italian question
    prompt_low_baseline = "Rispondi brevemente a questa domanda in italiano\n\n" + gemini_question
    print("prompt_low_baseline\n", prompt_low_baseline)
    
    input_low_baseline = tokenizer(prompt_low_baseline, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output_low_baseline = model.generate(**input_low_baseline, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE, top_p=TOP_P, do_sample=True)
    
    low_bs_response = tokenizer.decode(output_low_baseline[0][input_low_baseline["input_ids"].shape[-1]:], skip_special_tokens=True)


    #experiment call --- dialect text + italian question
    prompt_experiment = "Dato questo testo:\n" + full_text + "\n\nRispondi brevemente a questa domanda in italiano\n\n" + gemini_question
    print("prompt experiment\n", prompt_experiment)
    
    input_experiment = tokenizer(prompt_experiment, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        output_experiment = model.generate(**input_experiment, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE, top_p=TOP_P, do_sample=True)
    
    experiment_response = tokenizer.decode(output_experiment[0][input_experiment["input_ids"].shape[-1]:], skip_special_tokens=True)
    

    #upper baseline call --- italian text + italian question
    prompt_upper_baseline = "Dato questo testo:\n" + italian_text + "\n\nRispondi brevemente a questa domanda in italiano\n\n" + gemini_question
    print("prompt upper baseline\n", prompt_upper_baseline)
    
    input_upper_baseline = tokenizer(prompt_upper_baseline, return_tensors="pt").to(model.device)
    
    with torch.no_grad():
        output_upper_baseline = model.generate(**input_upper_baseline, max_new_tokens=MAX_NEW_TOKENS, temperature=TEMPERATURE, top_p=TOP_P, do_sample=True)
    
    upper_baseline_response = tokenizer.decode(output_upper_baseline[0][input_upper_baseline["input_ids"].shape[-1]:], skip_special_tokens=True)


    results.append({
        "Dialect":dialect,
        "Model":ai_model,
        "Domain":domain,
        "Dialect text": full_text,
        "Italian text": italian_text,
        "Gemini question": gemini_question,
        "Gemini answer": gemini_answer,
        "Lower bs answer": low_bs_response,
        "Experiment answer": experiment_response,
        "Upper bs answer": upper_baseline_response,
    })
    i+=1
    #checkpoint
    if i%5 == 0:
        out_df = pd.DataFrame(results)
        out_df.to_csv(f"checkpoint/minerva_answers_partial_{i}.csv", index=False)


out_df = pd.DataFrame(results)
out_df.to_csv("minerva_answers.csv", index=False)
