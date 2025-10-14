import os
import json
from transformers import AutoTokenizer

cartella = "code_e_corpus_tesi/romanesco"

#tokenizer
MODEL_NAME = "roberta-base"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, use_fast=True)

total_text = []


for filename in os.listdir(cartella):
    if filename.endswith(".json"):
        percorso_file = os.path.join(cartella, filename)
        with open(percorso_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                
                for item in data:
                    if "text" in item:
                        total_text.append(item["text"])
            except json.JSONDecodeError:
                print(f"The file is not a JSON")


testo_completo = "\n".join(total_text)

token_ids_corpus = tokenizer.encode(
    testo_completo,
    add_special_tokens=False
)
tot_token_corpus = len(token_ids_corpus)

print(f"Numero totale di token: {tot_token_corpus}")
