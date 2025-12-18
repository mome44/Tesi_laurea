## Introduction
*definition of corpus*
Extracting the corpus is one of the most important aspects that have to be considered when dealing with LLMs. Since the quality of the corpus is related also to the performance of the model.

In our case, the one of “teaching” Minerva some Italian regional languages, we have to understand that there are some limitations, that wouldn’t be there when considering widespread and official languages.

The first thing is the lack of huge quantities of corpus. Usually regional languages do not have a rich literary history that can be compared to modern standard languages such as Italian or English. Moreover this problem becomes more prevalent on the internet, where only a small percentage of the production can be found digitalized or even scanned.

The other aspect is the orthography and standardization, since regional languages often do not have a standardized spelling and orthography, neither an organization that regulates them. The way of representing the language is left to the individual speakers. So there is a lot more variations when it comes to even writing a single word, this depends on the structure of the language itself and also on the official language in which it coexists with. E.g the way in which italian dialects are usually written will tend to resemble italian orthography.

## Corpus subdivision
Kinds of corpus

When extracting the corpus for language fine tuning we have different kinds of texts online. The main categorization divides them based on two criteria:
- Format
- Domain

### Format
This indicates the way in which the text is written, in literature the most common styles are, prose poetry and comedy. 

*definition of prose, poetry and comedy*

#### Prose texts

They are found on the web, especially on free website, like the gutenberg project and the manuzio/liber liber website.

Other than digitalized books other sources include websites that contain information and news e.g. Wikipedia, wikisource and also different local websites written in the language.

In order to grasp the more lively and used language, also extracting text from social networks, such as facebook posts and reddit is useful.

These prose texts are then extracted and parsed, the parsing of texts follows the standard conventions, so first they are converted into a single block of text, then they are divided into sentences.

One must also take into account the presence of certain part in Italian or quotes and page numbers and so on.

This process is done using parsing with specific rules.

Prose text according to standard practince in large llm fine tuning techniques can be divided into different _domains_. Each domain has its own characteristics, in this scenario two main domains can be identified.

#### Comedies

They are texts made by a continuos dialogue, where each speaker is identified and there are also brief description of the scenario and the action that the actor is performing. The Italian “dialectal” comedies and theater, contains usually funny or comical language, the description of the scenario is usually in Italian.

In order to parse them is necessary to consider only the “battute”, so excluding the indentation and the description.

The results are saved in a json file containing “actor” and “text”.

However there is a problem with this kind of texts because they contain battute so they cannot be directly used for language training, so there needs to be paraphrasing.

#### Poetry and lyrics

These were extracted from popular local authors and they still represent the majority of the texts in these regional languages. The major problem here is that they rime and the words are not rearranged in the natural way in which people speak. So also here we need to paraphrasize the text, while maintaining the same language.

### Domain

#### Literature

#### Encyclopedical

#### News

## Methods

### Parsing

#### Image extraction

#### Comedy parsing

#### Prose and poetry parsing

### Generating more text
Paraphrasis

*cite papers about paraphrasis and data augmentation using llms*
This important step was implemented by first creating a prompt to perform this paraphrasis, I tried different API and the best open LLM to do this was __

The structure of the prompt was this:

And with this I was able to obtain more text than originally expected.

It is important that the paraphrasis maintains the same meaning as the original text and also maintain the same language, this is essential for my task since the prompt is in Italian there is always the risk of getting a more italianized text than expected.

Generating more texts

Once created all the “original” text in prose, there is the problem of determining the amount of tokens to train the model to speak the language. Here there are two factors:

-         The model size: the bigger the model, the more parameters are needed to do fine tuning.

-         The quality of the corpus: It is not recommended to do too many paraphrases of the same text otherwise the model could be biased towards the same sentence

This is done in a similar way to the paraphrasis, of course these text are put aside.

API calls and a little glimpse about prompt engineering

[Talk about llms and the utility of structuring prompts with few shot examples to get better results especially with tasks about paraphrasing and translation.

The prompt was structured this way,
#### Parafrasis
#### Translation




## Standardization

*describe the problem of finding a standardized version of these languages*
### Roman
### Neapolitan
### Sicilian

## Analysis

Here we can show the composition of the corpus that I have gathered for the three languages, it is expressed in total number of tokens, according to the tokenization for Minerva.

Tokens are important but we should also care about quality, since tokens only consider the subwords that are present, it is not always necessary to add large quantities of texts. It is important that all of the tokens cover the language and allow the model to generate it correctly, of course this depends on the structure of the language, in my case the Romanesco dialect is very similar to standard Italian and this will cause that Minerva already knows a lot of tokens, so the required one to generate a text will be fewer, vice versa with Neapolitan and sicilian which are quite different (they still share a percentage) but it is better to add more.

Also when adding more text we should measure the amount of new tokens that are added so

[insert here graphs that show the composition for the corpus together respect to the three langs]

Romanesco 250k original tokens

Which


