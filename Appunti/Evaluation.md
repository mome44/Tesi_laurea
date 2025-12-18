## LLM as judge

_Exploring the Use of Large Language Models for Reference-Free Text Quality Evaluation: An Empirical Study

They use:
- individual score
- Pairwise comparison
### Individual score

This consists of explicit score, where the prompt specifies to measure the quality of a specific performance. Like assigning a score from [0-100].
The other is implicit score so YES-NO question, since often it is hard to assign good scores.

### Pairwise comparison
Needs an initial part of text for example a story line and it compares to two generated outputs and the model has to tell which one is better.

### Tasks
Text summarization, Dialogue response generation, Story generation and Paraphrase generation.

Story generation is the tsak of generating a story based on a given beginning. 
They used openMEVA-ROC (Guan et al., 2021) for evaluation, which contains 200 story beginnings and 5 corresponding machine-generated storylines for each beginning. Each storyline is manually annotated in terms of overall quality.”


----
Silvia lilli

Ha 5 domande in Romanesco e 5 in Siciliano su dei testi dati a cui non si ha accesso.


Una repo dove si trova un codice che traduce dall'italiano a un dialetto della campania.
https://github.com/Tommaso-Sgroi/VojoLe-LM

----
## Other kinds of evaluation

_GRDD+: An Extended Greek Dialectal Dataset with  Cross-Architecture Fine-tuning Evaluation_

Dataset:
they propose an extended version of the GRDD+ dataset that includes texts from different greek dialects. The dataset size is a total of 6M words, for all the dialects combined, so the dimensions are pretty comparable.

Task:
As task they do instruction fine tuning (but the only instruction is generate text in dialect), by creating instruction prompts example by using sliding windows on plain texts. 

Method:
Used three models Llama 3 - 8B, llama 3.1- 8B and Krikri-8B a models for greek. They used **LoRA**. The results on these models were compared to chat gpt gemini and claude.

Evaluation:
Generate 7 generation per model, so 63 per dialect. They used native speakers to evaluate the results 
![[Pasted image 20251218001815.png]]
They did mean and standard deviation, comapring the base model, and the fine tuned one. 
Cretan 16 rater, cypriot 19 ratern, northern 9 and pontic 5, they scaled the results.

Results:
There is an improvement in both llama, so it is useful, the metrics are the one described above.

----

_Dialetto, ma Quanto Dialetto?  Transcribing and Evaluating Dialects on a Continuum_

In general some of the metrics that are used specifically for dialects in the case of translation are BLUE and ChrF, which rely on n gram similarity.



----
_AL-QASIDA: Analyzing LLM Quality and Accuracy Systematically in  Dialectal Arabic_

They want to evaluate the text generation and understanding of arabic dialect.

Dataset:
To create the questions they used an existing english question dataset, and replaced the language name with the arabic variety. Es. can you give me a text in \__ ?
They used a monolingual dialectal text to create prompt, turning sentences into realistic instructions.

Task:
They did instruction tuning using different prompts.
The dialects have to satisfy the following criteria:
- Fidelity: can llm identify and produce the correct DA variety, when asked?
- Understanding: Can it understand prompts in the DA variety?
- Quality: this encompass the fluency and also the semantic accuracy.
- Diglossia: translating between msa and dialects.
Evaluation:

For fidelity they did classification

For understanding they did this, if the model is able to translate the generated text into english then it can understand it and the problem becomes evaluating the translation.  (sp BLEU, chrF)

For the quality they asked for translation from english to dialect. They used human evaluation, they judged adherence of the response to the requeste, the adequacy of translation, also the fluency and dialectal fidelity. 
50 responses in random order.

![[Pasted image 20251218100128.png]]

----
_Assessing Thai Dialect Performance in LLMs with Automatic Benchmarks and Human Evaluation_

They created a new benchmark for evaluating dialects, by translating a gold reference for different tasks, into separate dialects thanks to native speaker.

Una cosa comune è che gemini, chat e così via mostrano sempre un certo standard di fluenza che è spesso superiore a quello che si ottiene con altri modelli open. 

----
_Dialect bench_

Hanno fatto varie task in dialetto su benchmark differenti, tra cui sono presenti anche quelli relativi a Natural language inference, e anche topic classification come per il siciliano. 

Per il napoletano è presente lo stesso dataset per POS, dove hanno testato la parsing evaluation, e anche parse of speech evaluation in zero shot scores, con mBERT e XLM-R, con risultati di 0.30 e 0.50 f1 score.
Potenzialmente potremmo vedere come migliora in caso di fine tuning, magari il valore base aumenta.

Qui ancora non hanno scoperto il golden dataset del siciliano quindi potrebbe essere un aspetto interessante.

----
## Measurable metrics

### Perplexity

### LLM-based scoring

Use chatgpt, gemini or other llms to evaluate if the generated text is good

### Human evaluation

Ask native speakers to rate the quality of the text, or other metrics (but I think it is better to give a simpler task without getting into grammatical stuff.) Like yes/no questions or scoring from 1 to 5.


### Part of speech tagging, dependency parsing

Since the gramamtical structure of italian and the dialect are similar, we can try to use an italian parser on the dialects. For example we can compare the distribution to the original corpus.

I have found a set of annotated examples of POS of sicilian sentences, the idea is to analyze the differences between the distribution of the POS of these sentences to the generated ones. 

Arbuli sunnu: Sicilian3bank 2025

They have used italian parsers like ISDT and POSTWITA on sicilian text and then they have produced manually the golden standard, correcting these annotations. 
So we can check if the difference between our generated text and the gold standard is the same as the one between the training text and it, taking into account the fact that we are going to parse it as italian text.

For neapolitan there exists a small (20) annotated set of sentences, so we can do the same, however the number is significantly small here, so we have to take it into account.

UD_Neapolitan-RB
We can see the difference and the accuracy of an italian parser on neapolitan texts.

For the Roman dialect it is fine if we apply the normal italian parser, since it is the most similar to standard italian, the grammar is basically the same. 
### Lexical coverage

Quello che abbiamo fatto l'altra volta, si misura la percentuale di parole generate che risiede nel vocabolario e anche e parole che non sono nel vocabolario.

### N-gram overlap

Metrics like self-bleu, but I in this case of dialects, in order to compute the similarity we have to take into account orthographical and morphlogical variation in inflections. So it is better to use character based n gram similarity. 

Self-ChRF: it is character based so it can give a more accurate representation. Es. casa and cas are very similar. How much the generated text are similar to each other. 

Corpus-ChRF: it says the overlap of the generated text with the training corpus.

### Mauve
It represents real text and generated text as embeddings, usually on pretrained model like gpt or roberta. 
It extimates the joint distribution of the two collection, computing the divergence metrics in these two distributions. Giving a score between 0 and 1.
 
### Cluster based metrics
Checks if generated texts  belong to the same cluster as the other training texts.

----

Similarity between dialects and standard italian  


In the sicilian paper Arbuli sunni: they tried to parse sicilian in a similar way to italian, using italian parsers. Discovering tha ISDT outperforms postwita in dealing with sicilian texts. 

E. Di Nuovo, Introducing Valico-UD: A Parallel, Learner Italian Treebank for Language Learning Research, Pàtron, 2023.

This paper is cited, to prove that this italian parser was evaluated also on non standard language..

When manually correcting the language it is clear that there were some issues in dealing with that.
Tokenization, especially with the apostrophes, the differences in orthography and the only noticeable sintactical problem is the eventual presence of reduplication. 



_Language Varieties of Italy: Technology Challenges and Opportunities

è presente il dataset sid4lr per la traduzione da napoletano a italiano con 800 frasi parallele.
potenzialmente si potrebbero usare queste frasi per fare il parser.

