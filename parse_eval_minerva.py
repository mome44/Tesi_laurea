import nltk
from nltk.translate.meteor_score import meteor_score
from nltk.tokenize import word_tokenize
#nltk.download('punkt_tab')
#nltk.download('wordnet')
#nltk.download("punkt")
import sacrebleu
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch
import json
#from peft import LoraConfig, get_peft_model, TaskType, PeftModel

from datetime import datetime
from datasets import load_dataset

import pandas as pd
import re

MODEL_PATH = "minerva-350M"
FILENAME = "minerva_answers_partial_93"
path_folder = ""    #change this when using cineca   has to end in /
path_corpus = "corpus/refined/"
training_name = "rom_book"
output_path = "results/"
model_name = "minerva-350M"

df = pd.read_csv(f"results/minerva_answers/{FILENAME}.csv")

#base_model = AutoModelForCausalLM.from_pretrained(
#    MODEL_PATH,
#    dtype=torch.float16,
#    device_map="auto"
#)
#
#model = PeftModel.from_pretrained(
#    base_model,
#    "./minerva-lora"
#)
#
#model.eval()

def parse_response(text):
    #pattern = r'\d\)\s.*?(?=\n\d\)|$)'
    
    #pattern = r'(\d\)\s.*?)(?=\n\d\)|$)'
    #pattern = r'\d\)\s.*?(?=\r?\n\d\)|$)'
    #pattern = r'(\d\)\s.*?)(?=(?:\r?\n\d\)|$))'
    pattern = r"\d[.)]\s*(.*?)(?=\r?\n\d[.)]|$)"


    risposte = re.findall(pattern, text, flags=re.S)
    risposte = [r.strip() for r in risposte]
    
    answer_1 = risposte[0].lower().strip()
    if len(risposte) == 1:
        answer_2 = "null"
        if "\r" in answer_1:
            answer_2 = answer_1.split("\r")[1].strip()
            answer_1 = answer_1.split("\r")[0]
    else:
        answer_2 = risposte[1].lower().strip()
        answer_2 = answer_2.split("\r")[0]

    #print(answer_1.split("."))
    #print(f"{answer_1} \n\n{answer_2}")
    return answer_1, answer_2

for idx, row in df.iterrows():

    italiano_ref_1 = row["a_1"]
    italiano_ref_2 = row["a_2"]

    response_raw = row["minerva_response"]
    print("index -----------", idx)
    print(response_raw)
    answer_1, answer_2 = parse_response(response_raw)

    df.at[idx, "min_answer_1"] = answer_1
    df.at[idx, "min_answer_2"] = answer_2

    ref_1_tokens = [word_tokenize(italiano_ref_1, language="italian")]
    ref_2_tokens = [word_tokenize(italiano_ref_2, language="italian")]

    ans_1_tokens = word_tokenize(answer_1, language="italian")
    ans_2_tokens = word_tokenize(answer_2, language="italian")

    # METEOR
    meteor_1 = meteor_score(ref_1_tokens, ans_1_tokens)
    meteor_2 = meteor_score(ref_2_tokens, ans_2_tokens)
    print(meteor_1, meteor_2)

    chrf_1 = sacrebleu.sentence_chrf(answer_1, [italiano_ref_1])
    chrf_2 = sacrebleu.sentence_chrf(answer_2, [italiano_ref_2])

    print(chrf_1, chrf_2)

    df.at[idx, "meteor_1"] = meteor_1
    df.at[idx, "meteor_2"] = meteor_2

    df.at[idx, "chrf_1"] = chrf_1
    df.at[idx, "chrf_2"] = chrf_2

df.to_csv(f"results/eval/{FILENAME}.csv", index=False)





