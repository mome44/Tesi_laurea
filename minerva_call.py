import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
#from huggingface_hub import snapshot_download
#
#snapshot_download(
#    repo_id="sapienzanlp/Minerva-7B-instruct-v1.0",
#    local_dir="minerva-7b-instruct",
#    local_dir_use_symlinks=False
#)
#token = "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"

MODEL_PATH = "minerva-7b-instruct"  # path locale

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float16,
    device_map="auto"
)

model.eval()

df = pd.read_csv("Q&A dialect thesis - Q&A.csv")
print(df.columns)

df_grouped = df.groupby("Full text")
results = []

for full_text, dfs in df_grouped:
    rows = dfs[["testo", "label"]].to_dict("records")

    row1, row2 = rows

    #question_1 = row1["Dialectal question"]
    #question_2 = row2["Dialectal question"]

    ai_model = row1["AI model"]
    dialect = row1["Dialect"]
    domain = row1["Domain"]

    question_1 = row1["Italian question"]
    question_2 = row2["Italian question"]

    answer_1 = row1["Italian answer"]
    answer_2 = row2["Italian answer"]

    prompt = f"Dato questo testo: \n \"{full_text}\" \n rispondi a queste domande: \n {question_1} \n {question_2}"

    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)

    # generazione
    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            do_sample=True
        )
    
    response = tokenizer.decode(
        outputs[0][inputs["input_ids"].shape[-1]:],
        skip_special_tokens=True
    )

    results.append({
        "model":ai_model,
        "dialect":dialect,
        "domain":domain,
        "full_text": full_text,
        "q_1": question_1,
        "a_1": answer_1,
        "q_2": question_2,
        "a_2": answer_2,
        "minerva_response": response
    })

out_df = pd.DataFrame(results)
out_df.to_csv("minerva_answers.csv", index=False)