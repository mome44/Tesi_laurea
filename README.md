# Tesi_laurea
Tesi di laurea magistrale in Engineering in computer science
Strumenti utili:
- Zotero (e estensione per il browser) per salvare paper
- asta.allen.ai: chatGPT ma specifico per fare ricerche sulla letteratura di un argomento in modo veloce, ti genera dei summary con references, comodo ma ovviamente va rivisto 
- connectedpapers.com sito web che ti trova paper collegati ad uno di partenza, hai 3 chiamate al giorno ma sono sufficienti di solito, molto comodo

## Categorie corpus
Io ho diviso i dati in questo modo
 - Commedia: Contiene commedie dal tono popolare
 - Poesia_sonetti: Poesie popolari
 - Poesia_formale: Poesie liriche più formali (es. divina commedia)
 - Narrativa_favole: Contiene storie popolari/leggende, favole (comunque racconti inventati)
 - Narrativa_storie: Contiene racconti non fiction, come esperienze personali ricordi o storie di fatti accaduti realmente, raccontate in prima persona.
 - Incipit_opere: Prologo/introduzione di opere importanti
 - Descrittiva: Contiene descrizioni di vari campi come cucina, linguistica, definizioni di parole
 - Notizie: descrizione di fatti che accadono/accaduti in stile giornalistico
 - Battute: battute umoristiche
 - Biografie: storie della vita di persone
 - Citazioni
 - Wikipedia
 - Opus
 - Parafrasi_commedia: commedie parafrasate in prosa AI
 - Parafrasi_poesia: poesie parafrasate in prosa AI
 - Parafrasi_prosa: testi TRADOTTI in dialetto AI

 - Totale prosa pura: battute + biografia + citazioni + descrittiva + narrativa_favole + narrativa_storie +notizie
 - Totale parafrasi: parafrasi_commedia + parafrasi_prosa + parafrasi_poesia
 - Totale poesia: poesia_sonetti + poesia_formale
 - Totale prosa: totale prosa pura + totale parafrasi

Dato che hai detto di dividere tutto in tre domini principali, LIBRI, WIKI, NEWS.
Andando un po' a logica ho notato che alcune delle mie categorie più specifiche si potevano accorpare perché corrispondevano allo stesso dominio.

Ho fatto questo ragionamento:
LIBRI = Narrativa_favole + Narrativa_storie + Incipit_opere
LIBRI + par = LIBRI + (parafrasi_commedia, parafrasi_poesia, parafrasi_prosa)
LIBRI + par + opus = LIBRI + (parafrasi_commedia, parafrasi_poesia, parafrasi_prosa) + opus
WIKI = Wikipedia + Descrittiva
NEWS = Notizie

Solo due domini non hanno corrispondenze, anche perché sono molto piccoli.
Battute, Citazioni

Domanda
Le poesie e le commedie (non parafrasate) dove vanno? diventano task a parte oppure finiscono in LIBRI essendo comunque letteratura?

Ti mando l'immagine dove sono presenti tutti i token, catalogati, con anche i raggruppamenti per i tre domini, ho messo in grassetto quelli con i token più elevati.



## COSE DA FARE
### Generazione evaluation samples.

Prendere le prime frasi di un documento qui dice 5 ma secondo me anche meno forse 3/2. 
Fare una chiamata a Gemini - 3/2.5 dove gli chiediamo di fare due domande su questo estratto di testo. Ci devono essere 4 coppie domanda risposta, meglio prima fare le due domande e le due risposte in dialetto, successivamente si può chiedere di tradurre in italiano.

Fare stratified sampling per capire quanti Q-A generare
- Fare una funzione che salva le prima righe 150/200 parole del numero di sample che si deve scegliere per fare q&a in una serie di file json. 
- Ristrutturare i testi in prosa visto che sono scritti per righe
- Scrivere il prompt e testarlo
- Fare standardizzazione dell'ortografia e cercare di cambiare anche da solo lo cunto de li cunti. 
- Fare una copia del file della API
- Capire quale API usare e se conviene pagare oppure no

### da fare
- Scrivere i progressi fino ad adesso
- trovare altre poesie per il siciliano in caso, e vedere se si riesce a scaricare lo cunto de li cunti in napoletano più moderno

Literature Review
- LoRA: come funziona tecnicamente il training (requisiti di token, parametri, etc)
   - TADA ?
- Language/Dialect adaptation (in generale e con LoRA), cerca anche come lo fanno per i low-resource languages (basco, finlandese, latino, catalano ...) 
- Language Model automatic evaluation (soprattutto base models) oltre a perplexity -- vedi Minerva, OLMo (1 e 2 e 3) 
- Esiste qualcosa in Italiano del genere? Forse sì ma vecchia, senza Minerva probabilmente (probabilmente solo per comparazione)

Prossima volta:
- LitReview su quello (quello che riesci) slides 


## CORPUS

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






