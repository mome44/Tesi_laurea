import os
import json
from transformers import AutoTokenizer


cartella = "code_e_corpus_tesi/romanesco"

#tokenizer
tokenizer = AutoTokenizer.from_pretrained("sapienzanlp/Minerva-7B-base-v1.0", use_fast=True)

total_text_num = []


for filename in os.listdir(cartella):
    if filename.endswith(".json"):
        percorso_file = os.path.join(cartella, filename)
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

print(total_text_num)
#tokens = tokenizer.encode(testo_completo)
num_tokens = sum(total_text_num)

print(f"Numero totale di token: {num_tokens}")
