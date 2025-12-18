
Natural language processing for dialects of a language a survey

There are two main tasks in this paper

**Natural language understanding**  (NLU)
This a very common task in this field it includes dialect identification, sentiment analysis and other classification tasks.
The paper lists several methods but the most important to us is fine tuning LLMs where it lists a paper

**Natural language generation** (NLG)
Here it appears that the metrics for text generation may penalize the output inc ertain dialects in the paper 
Dialect-robust Evaluation of Generated Text. In ACL. Toronto, Canada, 6010–6028. https://doi.org/10.18653/v1/2023.acl-long.331

They introduce a new metric called Nano, which allows perturbations in the general output. 

----

#### Low-Resource Dialect Adaptation of Large Language Models: A French Dialect Case-Study

It states that Continual pre-training is one of the most common way to adapt dialect to LLM models.

They considered the limitation of CPT but also a good way of doing that.

It is based on french dialects especially quebecois a regional dialect of french spoken in Canada. 

Used LoRA for adaptation and gradient-check pointing as parameter efficient strategies.

-> what is gradient check pointing?
Durante il forward pass, che consiste nel calcolare le attivazioni delle matrici di tutti i layers, quindi Wx, come abbiamo visto già a neural networks. Questa tecnica consiste nel salvare alcune delle attivazioni intermedie, perché se si calcolano tutte specialmente in modelli molto grandi questo può occupare molta memoria. Le attivazioni mancanti 
sono calcolate al momento del backward pass. 


The corpus isa total of 86M tokens in our experiments, the result was evaluated on the COLE benchmark.

Difference between Continual learning and CPT 

CL uses such as regularization, replay, and gradient orthogonalization to mitigate catastrophic forgetting across many tasks.

This is field is called:
domain-adaptive pre-training (DAPT) or language-adaptive pre-training (LAPT)

The dataset is divided into different fields, for the sake of my thesis let's look and analyze the smaller ones, for exampe the Youtube comments 2.15 M tokens, and reddit 1.76 M tokens.

Training

All matrices in the transformer LLAMA 3.2 1B, LLama 3.1-8B so 4 for attention layers and 3 for fnn.
R=16 alpha=32, dropout = 0.1

Sequences of 1024 tokens with stride of 512 (due to computational constraints)
Three to six epochs, with AdamW, weight decay = 0.01,
learning rate 1x 10^-5. with cosine decay and a warm-up ration of 0.1

Gradients were clipped at a norm of 1.0.

Evaluation:
- QFrCoLA: There are 25k  sentences classified as grammatical and ungrammatical.
- QFrBLiMP: the same
- QFrCORT: definition matching task, there are french multi word expression and 10 possible definitions.
- Sentiment analysis.
It is evaluated on a number of datasets, mainly for classification, like choosing the correct sentences. Identifying if a sentence is paraphrased or not. But these cases required the existance of testing datasets structured in a specific way in the dialect, so I don't think that they can be relevant.

The results showed significant improvements on 




----
Don’t Teach Minerva”: Guiding LLMs Through Complex Syntax  for Faithful Latin Translation with RAG

This paper teaches latin translation to minerva, there are two stages in this process.
Latin is a low resource language

----
SemiAdapt and SemiLoRA: Efficient Domain Adaptation for Transformer-based Low-Resource Language Translation with a Case Study on Irish

Working on a relatively small corpus for the irish language with a total of 17 milion tokens for the Irish gaelic, and roughly the same for english. Since their aim is to perform better in the task of translation it might be useful to see what they created.

They proposed two models Semi Adapt and SemiLoRA, which use zero shot domain assignment to training data. What is domain assignment, is where we try to categorize data into different knowledge domain according to the kind of data.
This is followed by either full fine tuning or the training of LoRA adapters.

DATA
They used data from the OPUS platform, there are also 813k sentence pairs from alternate sources like school exams,bringing the total parallel value to 17 M token for 1.32M sentences.

The model uses is NLLB-200   VEDERE DOMAIN SINGOLI LOR

---

Mixture-of-LoRAs: An Efficient Multitask Tuning for Large Language Models

This paper introduce a method for dealing with multiple taks using lora, since there is the problem of which LoRa to use accordin to the prompt and the task. 
The most simple method is to mix the data in input and simply add just one lora module for all the tasks combined. 
The second method (their) consists of combining two separated approac, the first part consists in training the LoRA modules individually and then introduce a domain classifier to select the correct lora model. The domain classifier refers to the domain of the tasks, since one important aspect in continuous fine tuning is to choose some tasks which can regard different fields of the language corpus.

This domain classifier is a routing mecanism, they only used it on decoder only architectures. 

To improve the efficiency of training and inference they used a parallel processing strategy to train different lora domains at the same time.

MoA architecture  (Mixture of Lora)
They train N different Lora modules for N different tasks, obtaining the optimal parameter for each task scenario and data. This means that each lora module has to be optimized individually.

In the second stage it combines the set of N LoRAs. as usually with lora we keep the llm parameters theta fixed, and introduce router parameters R. 
The trainable router and the parameters of lora are combine to optimize the autoregressive modeling tasks. 
In this stage the training data is sampled from the original data of each task, the final loss of MoA is the sum of the language model loss and the MoE loss.  L = LLM (x) + ηLcls
So they change of cours the router with the LclS loss and also it includes the loss for slightly upgrading the Lora modules in order to increase the balance in the model.
The routing strategy
Typical routing strategies focuses on learning token level weighting fuctions, assigning one or two experts per token. the experts are lora modules.
This is complex to implement.
They adopt another method sequence-level routing strategy, during training each tranformer layer employs a separate router to assign the training data with its domain, ofc the training data is labelled since we know the domain from the dataset. 
... continuare






