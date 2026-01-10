import pandas as pd
import re

# carica il csv
df = pd.read_csv("QA translation - Q&A dialect thesis translated - Q&A.csv")

# funzione di parsing
def extract_between_hashes(text):
    if pd.isna(text):
        return None

    text = text.replace("#Testo tradotto#", "")
    text = text.strip("#")
    text = text.rstrip("#")
    text = text.strip()
    return text

# applica il parsing alla colonna
df["Translation"] = df["Translation"].apply(extract_between_hashes)

# salva il risultato
df.to_csv("Q&A_trasl.csv", index=False)
