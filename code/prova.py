import os

def elimina_righe_pari(nome_file):
    """
    Legge un file, elimina le righe pari (2a, 4a, 6a, ecc.) e risalva il file.

    Args:
        nome_file (str): Il percorso e nome del file di testo.
    """
    try:
        # 1. Legge tutte le righe dal file
        with open(nome_file, 'r') as file:
            righe = file.readlines()
        
        # 2. Filtra le righe per mantenere solo quelle dispari
        # La numerazione delle righe nel file va da 1 in su.
        # La lista 'righe' ha indici che vanno da 0.
        # Indice 0 (riga 1) -> (0 + 1) % 2 = 1 (Dispari) -> Mantieni
        # Indice 1 (riga 2) -> (1 + 1) % 2 = 0 (Pari)   -> Elimina
        # Indice 2 (riga 3) -> (2 + 1) % 2 = 1 (Dispari) -> Mantieni
        
        righe_dispari = [
            riga for indice, riga in enumerate(righe)
            if (indice + 1) % 2 != 0
        ]
        
        # 3. Scrive le righe rimanenti (dispari) nel file, sovrascrivendolo
        with open(nome_file, 'w') as file:
            file.writelines(righe_dispari)
            
        print(f"✅ Le righe pari sono state eliminate con successo dal file '{nome_file}'.")
        print(f"Totale righe salvate (dispari): {len(righe_dispari)}")

    except FileNotFoundError:
        print(f"❌ Errore: Il file '{nome_file}' non è stato trovato.")
    except Exception as e:
        print(f"❌ Si è verificato un errore: {e}")

# --- Utilizzo del programma ---

# Sostituisci 'il_tuo_file.txt' con il nome del tuo file di testo
nome_del_file = 'trilussa_tutte_le_poesie.txt' 

# Esegui la funzione
elimina_righe_pari(nome_del_file)