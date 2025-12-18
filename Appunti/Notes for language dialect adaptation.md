Sambalingo paper

They provide some comprehensive methods for adapting languages, since normally one would just pre train a new mode for the specific language, however in most instances this isn't possible or even the best solution, due to the lack of data or also to performances.

They adapted 9 languages using settings of 7B and 70B tokens.
Arabic, Bulgarian, Hungarian, Japanese, Russian, Serbian, Slovenian, Thai, and Turkish

Steps:
- selecting a model
- Extending the model vocabulary, the tokenizer (in their case llama) was extended by adding non overlapping tokens 
- Continual pretraining consisting of 1:3 mixture of the model's language and the target language web data w
- Instruction fine- tuning
- Alignment

The more tokens they added the lower the fertility rate would get, which is good since it indicates the numer of tokens for each word, and the usual behavior in words that are not "known" by the tokenizer is to produce more token than normal. The vocabulary expansion has no useful impact n accuracy, but a good one on inference and sequence.

They also initialize new token embeddings ...

We are interested on the continuos pre-training phase, with the "document attention" as stated in a previous paper.  Iyer et al.
Sequence length 4096
learning rate 1e-4   with cosine decay
warm up ration of 0.01
weight decay 0.1
maximum of 4 epochs.  following Muennighoff et al. Scaling data-constrained language models, 2023.

---

Challenges in Adapting Multilingual LLMs to Low-Resource Languages using LoRA PEFT Tuning

Paper abbastanza inutile hanno fatto fine tuning usando un dataset tradotto con google translate in Marathi, il dataset Alphaca contenente 52000 paia di instruction-response. Per le task di classificazione e di generazione di testo ma si trattava più che altro della capacità di rispondere alle domande quindi non è molto rilevante, poi hanno fatto anche la valutazione manuale boh.

----

Efficiently Adapting Pretrained Language Models to New Languages

LLm reach sub optimal performances on low resource language, since the model is usually dominated by english or another language. 
The adaptation to a new language must be done in a proper way, since misusing it can lead to excessive catastrophic forgetting and also poor token efficiency. 
The two relevant aspect are the Tokenizer, Data input mix during training.

In the paper they are dealing with hungarian and thai.

- **Tokenizer**
Most model as tokenizer use bite pair encoding (BPE) since this allows to base ourselves not on the characters of the alphabet but also on other characters.
The tokenizer has a poor tokenization efficiency if it is not trained on a given language, this creates a much higher amount of tokens, which can be impactful in terms of memory and time during the training phase.

The objective to improve its efficiency is to better its fertility, 

fertility is the average number of tokens per word.

In this paper instead of extending the tokenizer vocabulary like it did the first one, the procedure consists in replacing the least frequent tokens with ones from the new language, in this way we stay with the same vocabulary and embedding size.

Train a BPE tokenizer on the new language with vocabulary size k and check the number of overlapping tokens o, we replace the least important tokens in k - o (so we don't consider the overlapping words ofc.)
The embeddings of the new tokens must be randomized, in this way the new embeddings can be learned.
By doing this we reduce the fertility.

- **Training data mixtures**

The data for continuous pretraining is mixed between english data (the main language) with either hungaria and thai. 
They used a sample of the data from the actual pretraining corpus (the first initial training not this one) to mix with hungarian or thai.

Hungarian pretraining tuning data
- 96 Gbytes, 11M circa documents.
Thai 
- 15 M documents
I ignore for now the instruction tuning.

They tested different percentage of english and hungarian, the training was run for 30k steps. They compared it also with a pure hungarian model. 
The conclusions were that mixing data with english (or the source language of the model) can help mitigate the catastrophic forgetting and improve the performances of hungarian without any significant difference between 25% and 50% of the english data.

Hyperparameters:
batch size 512, LR = 0.000015, weight decay = 0.1.

---
Natural Language Processing for Dialects of a Language: A Survey

The introduction explains why is it necessary to consider dialects UTILE PER LA TESI.

Downstream tasks: tasks that the llm is able to execute after the continual pretraining phase.
----
Optimizing Retrieval-Augmented Generation (RAG) for Colloquial  Cantonese: A LoRA-Based Systematic Review

 Cos'è RAG: 
Retrieval augmented generation is a method which consists of taking the input query to the machine and using it to search for documents or information on the web or a knowledge base, the retrieved information are then added to the input prompt. This allows to generate more precise texts but we have to be careful when designing the processing of the queries and the search, especially for low resource languages it can cause hallucinations, since the online resources and information are limited.

Integrating this with Lora consists of having the structure above, but when the augmented input is given to the model, the lora module is activated to the model.

This paper shows that in the case of low resource languages this shows increasing performances. 


---
Vedere
- Mixture-of-LoRAs: An Efficient Multitask Tuning for Large Language Models
- Efficient Corpus and Graph-Based Adaptation of Small Multilingual Language Models for Low-Resource Languages (scrivere il riassunto anche se è su modelli piccoli)
- Vedere adapters come Tada e dada e quello generico e uno moderno (prendere i riassunti già fatti)
- In the main LoRA paper see the concept of LoRA dropout, and why is it useful for low resource languages.
- Mettere la ricerca che ho fatto a settembre nel powerpoint
- Mettere tutti questi appunti nel powerpoint in modo strutturato

Low resource languages
- datasets and limitations
Continual pre-training for language adaptation
- Tokenizer
- Mixture of data
- Catastrophic forgetting 
- Hyperparameters for LoRA
Multiple tasks
- Different possible tasks, Classification, text generation
- Domain based tasks
- LoRA with multiple Tasks
- How to select which lora module to activate
Evaluation
- Finding a method for evaluating the generated text.





