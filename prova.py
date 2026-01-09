import pandas as pd
import glob

path = "results/minerva_answers/*.csv"   # cartella + pattern
files = glob.glob(path)


df = pd.concat(
    (pd.read_csv(f) for f in files),
    ignore_index=True
)

print(df)

df.to_csv(f"results/eval/total.csv", index=False)

