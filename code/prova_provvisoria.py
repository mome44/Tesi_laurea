import os
import re
import json
PATH =  "../corpus_tesi/napoletano/wikipedia/source"
OUTPUT_PATH = "../corpus_tesi/napoletano/poesia"

for filename in os.listdir(PATH):
    full_path = os.path.join(PATH,filename)

    filename = filename.split(".")[0]
    print("processing ", filename)

    with open(full_path, "r", encoding="utf-8") as f:
        testo = f.read()
    
    data = []
    parts = re.split(r"\[p\.\s*\d+[\s\S]*?\]", testo)

    for p in parts:
        print("\n\n ------- \n\n",p)
        if len(p.strip())>4:
            data.append({
                "text":p.strip()
            })
    
    with open(f"{OUTPUT_PATH}/{filename}_processed.json", "w", encoding="utf-8") as out:
        json.dump(data, out, ensure_ascii=False, indent=2)


