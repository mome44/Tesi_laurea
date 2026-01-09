import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM, Trainer, TrainingArguments, DataCollatorForLanguageModeling
import torch
import json
from peft import LoraConfig, get_peft_model, TaskType
from datetime import datetime
from datasets import load_dataset
from peft import LoraConfig, get_peft_model, TaskType, PeftModel
from itertools import product

#per scaricare minerva 350M o altro modello
#from huggingface_hub import snapshot_download
#
#snapshot_download(
#    repo_id="sapienzanlp/Minerva-350M-base-v1.0",
#    local_dir="minerva-350M",
#    local_dir_use_symlinks=False
#)

#global variables
path_folder = ""    #change this when using cineca   has to end in /
path_corpus = "corpus/refined/"
training_name = "rom_book"
output_path = "results/"
model_name = "minerva-350M"


#r = 8
#alpha = 16
#lora_drop = 0.05
#dev_batch_size=1
#grad_acc_steps=1
#num_epochs=1
#lr_list = [1e-3, 1e-4]
#batch_list = [16, 32]
#epochs_list = [5, 10]

#Put here the loop for iterating the combination of hyperparameters
#for lr, batch, epochs in product(lrs, batches, epochs_list):

#hyperparameters
token_max_length = 128
r = 8 #lora rank
alpha = 16
lora_drop = 0.05
dev_batch_size=1
grad_acc_steps=1
lr=2e-4
num_epochs=1

hyper_name = f"r_{r}_alpha_{alpha}_lr_{lr}_ep_{num_epochs}"
 
print(f"starting to train {training_name} with {hyper_name}")

tokenizer = AutoTokenizer.from_pretrained(f"{path_folder}{model_name}")
tokenizer.pad_token = tokenizer.eos_token

#create the dataset by loading the json file
dataset = load_dataset(
    "json",
    data_files=f"{path_folder}{path_corpus}{training_name}_refined.json",
    split="train"
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

def tokenize(batch):
    return tokenizer(
        batch["text"],
        truncation=True,
        max_length=token_max_length
    )

tokenized_dataset = dataset.map(
    tokenize,
    batched=True,
    remove_columns=["text"]
)
tokenized_dataset = tokenized_dataset.select(range(5))

model = AutoModelForCausalLM.from_pretrained(
    f"{path_folder}{model_name}",
    torch_dtype=torch.float16 
#    device_map="auto"
)


lora_config = LoraConfig(
    r=r,                       
    lora_alpha=alpha,
    lora_dropout=lora_drop,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
    target_modules=["q_proj","k_proj","v_proj","o_proj","gate_proj","up_proj","down_proj"]
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
#trainable params: 20,971,520 || all params: 7,420,514,304 || trainable%: 0.2826

model.config.pad_token_id = tokenizer.pad_token_id
model.config.eos_token_id = tokenizer.eos_token_id
model.config.bos_token_id = tokenizer.bos_token_id

training_args = TrainingArguments(
    output_dir=f"{output_path}{training_name}/lora_{hyper_name}",
    per_device_train_batch_size=dev_batch_size,
    gradient_accumulation_steps=grad_acc_steps,
    learning_rate=lr,
    num_train_epochs=num_epochs,
    fp16=True,
    logging_steps=50,
    save_strategy="epoch",
    report_to="none",
    dataloader_pin_memory=False
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    data_collator=data_collator
)


trainer.train()

model.save_pretrained(f"{output_path}{training_name}/lora_{hyper_name}")
tokenizer.save_pretrained(f"{output_path}{training_name}/lora_{hyper_name}")