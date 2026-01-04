import json
import pandas as pd
import os
import re
import unicodedata
DIALECT = "romanesco"
#, "nap_w", "rom_b", "scn_b", "scn_w"
List_TIPO = ["scn_b"]

OUTPUT_PATH = f"corpus/refined"

segnali = [
        "traduzion", "narrativa", "parafras", " il "
        "ho tradotto", "di seguito", "mi dispiace", "mi scus", "Mi scus",
        "testo",  "fornit", "Mi dispiace", "sono pronto", "trasformare", "trasformà", "mi darai"
    ]

def refine_siciliano(testo):
    testo = re.sub(r"[`´‘’‚‛ʾʼʻ᾿ʹˊˋ＇]", "'", testo)
    testo = re.sub(r"ʃ(?=[bcdfghjklmnpqrstvwxyz])", "s", testo)
    testo = re.sub(r"š(?=[bcdfghjklmnpqrstvwxyz])", "s", testo)
    testo = re.sub(r"ʃ|š", "ç", testo)
    testo = re.sub(r"ç(?=[aou])", "ci", testo)
    testo = re.sub(r"ç", "c", testo)

    testo = re.sub(r"ä", "a", testo)
    testo = re.sub(r"ö", "o", testo)
    testo = re.sub(r"ï", "i", testo)
    testo = re.sub(r"ü", "u", testo)

    #preposizioni articolate
    testo = re.sub(r"\b(de lo|delo|del|di lo)\b", "di lu", testo)
    testo = re.sub(r"\b(de la|della|dela|di la)\b", "di la", testo)
    testo = re.sub(r"\b(de le|delle|dele|di le|de li|delli|deli|di li|dei)\b", "di li", testo)
    testo = re.sub(r"\b(de ll'|dell'|de l'|degli)\b", "dill'", testo)
    testo = re.sub(r"\b(de|di)\b", "di", testo)

    testo = re.sub(r"\b(a lo|al|allo|a il)\b", "a lu", testo)
    testo = re.sub(r"\b(a la|alla)\b", "a la", testo)
    testo = re.sub(r"\b(alle|a le|alli|ai|a i)\b", "a li", testo)
    testo = re.sub(r"\b(agli|all')\b", "all'", testo)

    testo = re.sub(r"\b(con il|col)\b", "cu lu", testo)
    testo = re.sub(r"\b(coll'|cogli)", "cull'", testo)
    testo = re.sub(r"\b(co|cu|con)\b", "cu", testo)

    testo = re.sub(r"\b(nel|ne lo)\b", "ni lu", testo)
    testo = re.sub(r"\b(nella|ne la)\b", "ni la", testo)
    testo = re.sub(r"\b(nelle|ne le|ne li|nei)\b", "ni li", testo)
    testo = re.sub(r"\b(negli|nell')", "ni ll'", testo)

    #continuare

    #articoli
    testo = re.sub(r"\b(lo|il|el|er|lu|'o|u|'u)\b", "lu", testo)
    testo = re.sub(r"\b(Lo|Il|El|Er|Lu|'O|U|'U)\b", "Lu", testo)
    testo = re.sub(r"\b(la)\b", "la", testo)
    testo = re.sub(r"\b(La)\b", "La", testo)

    testo = re.sub(r"\b(uno|un|nu|'no|'nu)\b", "un", testo)
    testo = re.sub(r"\b(Uno|Un|Nu|'No|'Nu)\b", "Un", testo)
    testo = re.sub(r"\b(una|na|'na)\b", "na", testo)
    testo = re.sub(r"\b(Una|Na|'Na)\b", "Na", testo)

    testo = re.sub(r"\b(li|le|'e)\b", "li", testo)
    testo = re.sub(r"\b(Li|Le|'E)\b", "Li", testo)

    testo = re.sub(r"nd(?!r)", "nn", testo)
    testo = re.sub(r"(mb|nv)(?!r)", "mm", testo)

    testo = re.sub(r"(ddh|ddr|ddhr|ḍḍ)", "ddh", testo)

    testo = re.sub(r"\b(haju|aiu|ho|haiu|aju)\b", "aiu", testo)
    testo = re.sub(r"\b(havi|avi|ha)\b", "avi", testo)

    testo = re.sub(r"gli(?=[aeou])", "gghi", testo)


    testo = re.sub(r"\bcinque", "cincu", testo)
    testo = re.sub(r"qu(?=[e,i])", "ch", testo)

    testo = re.sub(r"\b([A-Za-z]{3,})are\b", r"\1ari", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})ere\b", r"\1iri", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})ire\b", r"\1iri", testo)
    
    testo_standardizzato = testo
    return testo_standardizzato

def refine_romano(testo):
    testo = re.sub(r"[`´‘’‚‛ʾʼʻ᾿ʹˊˋ＇]", "'", testo)

    testo = re.sub(r"\b(del|di er|di el|de er|de il)\b", "der", testo)
    testo = re.sub(r"\b(della|di la|dela)\b", "de la", testo)
    testo = re.sub(r"\b(delle|di le|dele)\b", "de le", testo)
    testo = re.sub(r"\b(dei|deli|di li)\b", "de li", testo)
    testo = re.sub(r"\b(degli|dell')", "dell'", testo)
    testo = re.sub(r"\bdi\b", "de", testo)

    testo = re.sub(r"\b(allo)\b", "a lo", testo)
    testo = re.sub(r"\b(alla)\b", "a la", testo)
    testo = re.sub(r"\b(alle)\b", "a le", testo)
    testo = re.sub(r"\b(agli|all')\b", "all'", testo)
    testo = re.sub(r"\b(al)\b", "ar", testo)
    testo = re.sub(r"\b(ai)\b", "a li", testo)  
    testo = re.sub(r"\b(coll'|cogli)", "coll'", testo)
    testo = re.sub(r"\b(con il|col)\b", "cor", testo)
    testo = re.sub(r"\b(co|cu|con)\b", "co", testo)
    testo = re.sub(r"\b(nello)\b", "ne lo", testo)
    testo = re.sub(r"\b(nella)\b", "ne la", testo)
    testo = re.sub(r"\b(nelle)\b", "ne le", testo)
    testo = re.sub(r"\b(nel)\b", "ner", testo)
    testo = re.sub(r"\b(nei)\b", "ne li", testo)
    testo = re.sub(r"\b(negli|nell')", "nell'", testo)    
    testo = re.sub(r"\b(il|el)\b", "er", testo)
    testo = re.sub(r"\b(i)\b", "li", testo)
    #testo = re.sub(r"l\b", "r", testo)

    testo = re.sub(r"\bdi\b", "de", testo)
    #testo = re.sub(r"\bmi\b", "me", testo)
    testo = re.sub(r"\bti\b", "te", testo)
    testo = re.sub(r"\b(quel)\b", "quer", testo)
    testo = re.sub(r"\b(quer')", "quell'", testo)
    testo = re.sub(r"\b(egli|esso)\b", "lui", testo)
    testo = re.sub(r"\b(Egli|Esso)\b", "Lui", testo)
    testo = re.sub(r"\b(ella|essa)\b", "lei", testo)
    testo = re.sub(r"\b(Ella|Essa)\b", "Lei", testo)
    testo = re.sub(r"\b(essi)\b", "loro", testo)
    testo = re.sub(r"\b(Essi)\b", "Loro", testo)
    testo = re.sub(r"\bper\b", "pe'", testo)
    testo = re.sub(r"\bsul\b", "sur", testo)
    testo = re.sub(r"\b(bel)\b", "ber", testo)

    testo = re.sub(r"\bcald([aeio])\b", r"call\1", testo)
    testo = re.sub(r"\bartr([aeio])\b", r"antr\1", testo)
    testo = re.sub(r"gli(?=[aeou])", "j", testo)
    testo = re.sub(r"\br'(?=[aeoiu])", "l'", testo)

    testo = re.sub(r"ngi(?=[aou])", "gn", testo)
    testo = re.sub(r"ng(?=[ie])", "gn", testo)

    testo = re.sub(r"l(?=[bcdfghjkmnpqrstvwxyz])", "r", testo)
    testo = re.sub(r"nd(?!r)", "nn", testo)

    testo = re.sub(r"\b([A-Za-z]{3,})(rsi|rse|rci)\b", r"\1sse", testo)
    testo = re.sub(r"(rgli|rle)\b", "je", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})armi\b", r"\1amme", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})ermi\b", r"\1emme", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})irmi\b", r"\1imme", testo)

    testo = re.sub(r"\b([A-Za-z]{3,})arti\b", r"\1atte", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})erti\b", r"\1ette", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})irti\b", r"\1itte", testo)

    testo = re.sub(r"\b([A-Za-z]{3,})arvi\b", r"\1avve", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})ervi\b", r"\1evve", testo)
    testo = re.sub(r"\b([A-Za-z]{3,})irvi\b", r"\1ivve", testo)
    testo = re.sub(r"\bsono\b", "so'", testo)

    testo = re.sub(r"\buo", "o", testo)
    testo = re.sub(r"(?<!\b[qts])uo", "o", testo)

    testo = re.sub(r"\b(UO|Uo)", "O", testo)
    testo = re.sub(r"(?<!\b[tsq])(UO|Uo)", "O", testo) 

    #print(testo)
    testo_standardizzato = testo
    return testo_standardizzato

def refine_napoletano(testo):
    testo = re.sub(r"[`´‘’‚‛ʾʼʻ᾿ʹˊˋ＇]", "'", testo)

    #vedere le vocali con il cappelletto 
    #vocali
    testo = re.sub(r"ə|ë", "e", testo)
    testo = re.sub(r"ʃ(?=[bcdfghjklmnpqrstvwxyz])", "s", testo)
    testo = re.sub(r"š(?=[bcdfghjklmnpqrstvwxyz])", "s", testo)
    testo = re.sub(r"ʃ|š", "ç", testo)
    testo = re.sub(r"ç(?=[aou])", "ci", testo)
    testo = re.sub(r"ç", "c", testo)

    testo = re.sub(r"ä", "a", testo)
    testo = re.sub(r"ö", "o", testo)
    testo = re.sub(r"ï", "i", testo)
    testo = re.sub(r"ü", "u", testo)

    #preposizioni articolate
    testo = re.sub(r"\b(de lo|delo|del|di lo|d'o|d' o)\b", "d''o", testo)
    testo = re.sub(r"\b(de la|della|dela|di la|d'a|d' a)\b", "d''a", testo)
    testo = re.sub(r"\b(de le|delle|dele|di le|de li|delli|deli|di li|dei|d'e|d' e)\b", "d''e", testo)
    testo = re.sub(r"\b(de ll'|dell'|de l'|degli)\b", "'e ll'", testo)
    testo = re.sub(r"\b(de|di)\b", "'e", testo)

    testo = re.sub(r"\b(a lo|al|allo|a il)\b", "a 'o", testo)
    testo = re.sub(r"\b(a la|alla)\b", "a 'a", testo)
    testo = re.sub(r"\b(alle|a le|alli|ai|a i)\b", "a 'e", testo)
    testo = re.sub(r"\b(agli|all')\b", "a ll'", testo)

    testo = re.sub(r"\b(con il|col)\b", "cu 'o", testo)
    testo = re.sub(r"\b(coll'|cogli)", "cu ll'", testo)
    testo = re.sub(r'\b(c"(?=[aouei])\b)', "cu '", testo)
    testo = re.sub(r"\b(co|cu|con)\b", "cu", testo)

    testo = re.sub(r"\b(Dint|'Ind'|Ind|Ind'|Int'|Int|'Int')\b", "'Int'", testo)
    testo = re.sub(r"\b(dint|'ind'|ind|ind'|int'|int|'int')\b", "'int'", testo)
    testo = re.sub(r"\b(nel|ne lo)\b", "'int''o", testo)
    testo = re.sub(r"\b(nella|ne la)\b", "'int''a", testo)
    testo = re.sub(r"\b(nelle|ne le|ne li|nei)\b", "'int''e", testo)
    testo = re.sub(r"\b(negli|nell')", "'int'a ll'", testo)

    testo = re.sub(r"\bsopra\b", "'ncoppa", testo)
    testo = re.sub(r'copp"(?=[aeiou])', "copp''", testo)


    #continuare

    #articoli
    testo = re.sub(r"\b(lo|il|el|er|lu|'o|u)\b", "'o", testo)
    testo = re.sub(r"\b(Lo|Il|El|Er|Lu|'O|u)\b", "'O", testo)
    testo = re.sub(r"\b(la)\b", "'a", testo)
    testo = re.sub(r"\b(La)\b", "'A", testo)

    testo = re.sub(r"\b(uno|un|nu|'no|'nu)\b", "nu", testo)
    testo = re.sub(r"\b(Uno|Un|Nu|'No|'Nu)\b", "Nu", testo)
    testo = re.sub(r"\b(una|na|'na)\b", "na", testo)
    testo = re.sub(r"\b(Una|Na|'Na)\b", "Na", testo)

    testo = re.sub(r"\b(li|le|'i)\b", "'e", testo)
    testo = re.sub(r"\b(Li|Le|'I)\b", "'E", testo)

    testo = re.sub(r"nd(?!r)", "nn", testo)
    testo = re.sub(r"mb(?!r)", "mm", testo)

    testo = re.sub(r"\bcinque", "cinche", testo)
    testo = re.sub(r"\bdisse\b", "dicette", testo)
    testo = re.sub(r"\bdissero\b", "dicettero", testo)
    testo = re.sub(r"qu(?=[e,i])", "ch", testo)
    testo = re.sub(r"(?<!(q|g))ue(?!\b)", "uo", testo)

    testo = re.sub(r"ngi(?=[aou])", "gn", testo)
    testo = re.sub(r"ng(?=[ie])", "gn", testo)
    testo = re.sub(r"([ctvmpds])\"([aeiou]\b)", r"\1''\2", testo)

    testo = re.sub(r"'{3,}", "''", testo)
    testo = re.sub(r"('\"|\"')", "''", testo)
    # D. Convertire apostrofo standard
    testo_standardizzato = testo
    return testo_standardizzato

def general_refine(testo):
    testo = unicodedata.normalize("NFC", testo)
    emoji_pattern = re.compile(
    r"[\U0001F600-\U0001F64F"  # emoticon
    r"\U0001F300-\U0001F5FF"   # simboli e pittogrammi
    r"\U0001F680-\U0001F6FF"   # trasporti e simboli vari
    r"\U0001F700-\U0001F77F"   # simboli alchemici
    r"\U0001F780-\U0001F7FF"   # simboli geometrici estesi
    r"\U0001F800-\U0001F8FF"   # frecce supplementari
    r"\U0001F900-\U0001F9FF"   # emoji supplementari
    r"\U0001FA00-\U0001FA6F"   # simboli estesi A
    r"\U0001FA70-\U0001FAFF"   # simboli estesi B
    r"\U00002700-\U000027BF"   # dingbats
    r"\U0001F1E0-\U0001F1FF"   # bandiere
    r"]+",
    flags=re.UNICODE
    )
    testo = re.sub(emoji_pattern, "", testo)
    testo = re.sub(r"[•●▪►◄■□◆◇…–—|*$£&]", " ", testo)
    testo = re.sub(r"[^\S\r\n]+", " ", testo)

    testo = re.sub(r" +", " ", testo)
    testo = re.sub(r"\n{3,}", "\n\n", testo)
    return testo

def refine(Dialetto, testo):
    testo = general_refine(testo)
    if Dialetto == "napoletano":
        return refine_napoletano(testo)
    elif Dialetto == "siciliano":
        return refine_siciliano(testo)
    elif Dialetto == "romanesco":
        return refine_romano(testo)
    else:
        return ""

def process_fulltext(full_text):
    lines = full_text.split("\n")

    singe_lines = set()

    full_text_processed =""
    for line in lines:
        lunghezza = len(line.strip().split())
        if lunghezza >= 3 and line not in singe_lines:
            full_text_processed += "\n" + line
            singe_lines.add(line)
    return full_text_processed

frasesos = ""
full_text = ""

with open(f"corpus/raw/rom_book.json", "r", encoding="utf-8") as f:
    data = json.load(f)
errore = False
data_refined = []
suspect_sentences = []
for item in data:
    testo = item["text"]
    prima_frase = testo.split(".",1)
    if any(s in prima_frase for s in segnali) and "trilussa" in filename:
        suspect_sentences.append(prima_frase)
        testo = testo.replace(prima_frase, "")
    #testo_nuovo = testo
    testo_nuovo = refine(Dialetto = "romanesco", testo=testo)
    full_text += "\n" + testo_nuovo
    if testo_nuovo == "":
        print("errore dialetto non trovato o altro")
        errore = True
        break
    data_refined.append({
        "text": testo_nuovo
    })
for f in suspect_sentences:
    frasesos += f +"\n\n"    
if not errore:
    with open(f"{OUTPUT_PATH}/rom_book_refined.json", "w", encoding="utf-8") as out:
        json.dump(data_refined, out, ensure_ascii=False, indent=2)


#for tipe in List_TIPO:
#    if DIALECT == "romanesco" and (tipe == "opus" or tipe == "wikipedia"):
#        continue
#    TIPO = tipe
#    PATH = f"corpus_tesi/{DIALECT}/{TIPO}"
#
#    for filename in os.listdir(PATH):
#        if ".json" not in filename:
#            continue
#        full_path = os.path.join(PATH,filename)
#
#        filename = filename.split(".")[0]
#        print("processing ", filename)
#
#        frasesos += "\n" + filename + "\n\n\n"
#
#        if os.path.isfile(full_path):
#            with open(full_path, "r", encoding="utf-8") as f:
#                data = json.load(f)
#        errore = False
#        data_refined = []
#
#
#        suspect_sentences = []
#        for item in data:
#            testo = item["text"]
#            prima_frase = testo.split(".",1)
#            if any(s in prima_frase for s in segnali) and "trilussa" in filename:
#                suspect_sentences.append(prima_frase)
#                testo = testo.replace(prima_frase, "")
#            #testo_nuovo = testo
#            testo_nuovo = refine(Dialetto = DIALECT, testo=testo)
#            full_text += "\n" + testo_nuovo
#            if testo_nuovo == "":
#                print("errore dialetto non trovato o altro")
#                errore = True
#                break
#            data_refined.append({
#                "text": testo_nuovo
#            })
#
#        for f in suspect_sentences:
#            frasesos += f +"\n\n"    
#        if not errore:
#            with open(f"{OUTPUT_PATH}/{filename}_refined.json", "w", encoding="utf-8") as out:
#                json.dump(data_refined, out, ensure_ascii=False, indent=2)
#
#print("processing fulltext")
#full_text=process_fulltext(full_text)
#print("finished")

#with open(f"corpus_tesi/{DIALECT}/full_text.txt", "w", encoding="utf-8") as file:
#    file.write(full_text)

