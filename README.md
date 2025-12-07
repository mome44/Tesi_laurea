# Tesi_laurea
Tesi di laurea magistrale in Engineering in computer science
Strumenti utili:
- Zotero (e estensione per il browser) per salvare paper
- asta.allen.ai: chatGPT ma specifico per fare ricerche sulla letteratura di un argomento in modo veloce, ti genera dei summary con references, comodo ma ovviamente va rivisto 
- connectedpapers.com sito web che ti trova paper collegati ad uno di partenza, hai 3 chiamate al giorno ma sono sufficienti di solito, molto comodo

## Categorie corpus
 - Commedia: Contiene commedie dal tono popolare
 - Poesia_sonetti: Poesie popolari
 - Poesia_formale: Poesie liriche più formali (es. divina commedia)
 - Narrativa_favole: Contiene storie popolari/leggende, favole (comunque racconti inventati)
 - Narrativa_storie: Contiene racconti non fiction, come esperienze personali o storie di fatti accaduti realmente.
 - Incipit_opere: Prologo/introduzione di opere importanti
 - Descrittiva: Contiene descrizioni di vari campi come cucina, o imparare la lingua stessa, definizioni di parole
 - Notizie: descrizione di fatti che accadono/accaduti in stile giornalistico
 - Battute: battute umoristiche
 - Biografie: storie della vita di persone
 - Citazioni
 - Wikipedia
 - Opus
 - Parafrasi_commedia: commedie parafrasate in prosa
 - Parafrasi_poesia: poesie parafrasate in prosa
 - Traduzioni_testi: testi tradotti in dialetto


## COSE DA FARE
- categorizzazione dei dati un po' più fine-grained (per la narrativa cerca anche i riassunti)

### fatto

### da fare


Literature Review
- LoRA: come funziona tecnicamente il training (requisiti di token, parametri, etc)
   - TADA ?
- Language/Dialect adaptation (in generale e con LoRA), cerca anche come lo fanno per i low-resource languages (basco, finlandese, latino, catalano ...) 
- Language Model automatic evaluation (soprattutto base models) oltre a perplexity -- vedi Minerva, OLMo (1 e 2 e 3) 
- Esiste qualcosa in Italiano del genere? Forse sì ma vecchia, senza Minerva probabilmente (probabilmente solo per comparazione)

Prossima volta:
- LitReview su quello (quello che riesci) slides 


## CORPUS
 - Vedere quanto corpus serve basandosi su llamantino la versione di llama che ha anche l'italiano
 - Proseguire con la raccolta dei tre corpus e dividere i testi trovati in PROSA PURA, TEATRO, SONETTI, facendo il parsing che già esiste per la prosa pura e il teatro.
 - Vedere se bisogna fare in modo che tutti e tre i corpus siano di dimensioni comparabili
 - Scrivere i progressi fino ad adesso
 - Calcolare le percentuali e statistiche di questi testi "PURI"
 - Vedere se si tratta di un corpus sufficiente utilizzando varie metriche per misurare Quantità e qualità
 - VEDERE SE MANCANO PARTI DELLE TRADUZIONI/PARAFRASI IN ROMANESCO E NAPOLETANO (SONO PARTITE DA UN CERTO NUMERO) 

### ROMANESCO
#### fatto
 - (fatto) rivedere il parsing dei seguenti testi: GORINI lucia rosa ieri oggi .. romani; Hollywood tutta n'antra cosa; La macchinazione 
 - creare la funzione per fare il parsing con le poesie +  prompt
 - creare il prompt e la funzione per tradurre i malavoglia di verga in romanesco
 - parafrasare altre poesie e sonetti in romanesco
 - Trovare un modo per togliere le scritte di gemini prima delle risposte quando sono presenti
 - rivedere ortografia e standardizzazione romanesco
#### da fare


### SICILIANO
#### fatto
 - wikipedia
 - testi wikisource
 - reddit 
 - fare il parsing dei testi di wikipedia, come rimuovere [2]
 - vedere il corpus OPUS
 - rivedere estrazione reddit totu44 e salvarli in un file json normale
 - estrarre commedie e poesie in siciliano dal link del sito web
#### da fare

 - vedere ortografia e standardizzazione del siciliano
 - fare parafrasi così come napoletano e romano
 - aggiungere delle poesie in siciliano

### NAPOLETANO
#### fatto
 - Estrarre wikipedia e fare il parsing dei testi
 - Wikisource
 - Estrarre i link e i testi trovati online
 - Parafrasare le commedie in prosa
 - Trovare un modo per parafrasare lo cunto de' li cunti in napoletano moderno
 - Vedere corpus OPUS come il siciliano
 - Parafrasare le poesie in prosa
 - tradurre verga e le novelle napoletane di monnier
 - estrarre le altre poesie di wikisource e parafrasarle
 - dal file di testo completo, bisogna togliere tutte le righe di una parola 
 - togliere le emoji dall'opus
 - tradurre anche altri testi, già in italiano
 - rivedere ortografia e standardizzazione napoletano
#### da fare






