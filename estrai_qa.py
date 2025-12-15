import re

# Il formato stringa da analizzare (parsed)
testo_siciliano = "[La vecchietta, dopo che pensò che il vecchio volesse fare del male, cosa fece e iniziò a dire?]#Gli fece una faccia stordita e cominciò a recitare una filastrocca:#"
testo_drago = "[Dove arrivò il vecchio Drago dopo che si allontanò brontolando?]#Accanto alla Chiesa#"

# Espressione regolare
regex = r"\[(.*?)\]#(.*?)#"

def estrai_domanda_risposta(testo):
    """Estrae la domanda e la risposta da una stringa formattata."""
    
    # Tentativo di trovare la corrispondenza all'inizio della stringa
    match = re.match(regex, testo)
    
    if match:
        # Il gruppo 1 (index 1) è la Domanda
        domanda = match.group(1)
        # Il gruppo 2 (index 2) è la Risposta
        risposta = match.group(2)
        
        print(f"Testo Originale: {testo}")
        print("--- Risultato dell'Estrazione ---")
        print(f"Domanda (Gruppo 1): {domanda}")
        print(f"Risposta (Gruppo 2): {risposta}\n")
    else:
        print(f"Nessuna corrispondenza trovata per: {testo}\n")

# Applicazione dell'estrazione
estrai_domanda_risposta(testo_siciliano)
estrai_domanda_risposta(testo_drago)