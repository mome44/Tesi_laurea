## Introduction

_A corpus can be defined as a collection of machine-readable authentic texts (including transcripts of spoken data) that is sampled to be representative of a particular natural language or language variety.’_     (McEnery et al. 2006: 5)

[https://www.lancaster.ac.uk/fass/projects/corpus/ZJU/xpapers/Xiao_corpus_creation.pdf]

Creating, and extracting the corpus is crucial wen dealing with LLMs, since the quality of the corpus is related to model's performance.

In this matter, when dealing with regional languages and dialect, there are some limitations, that wouldn’t be there when considering widespread and official languages.

The first aspect is the lack of available texts online. Usually regional languages do not have a rich literary history that can be compared to modern standard languages such as Italian or English. Moreover this problem becomes more prevalent on the internet, where only a small percentage of the production is digitalized or even scanned. In fact the problem of dealing with low resource languages is still studied in modern day literature and research.

The other aspect is orthography and standardization, since regional languages often do not have a standardized spelling and orthography, neither an organization that regulates them. The way of representing the language is left to the individual speakers. So there is are numerous variations when it comes to spelling even a single word, it is clear that this depends on the structure of the language itself and also on the official language in which it coexists with. E.g the way in which italian dialects are usually written will tend to resemble italian orthography.

## Corpus subdivision

When extracting the corpus for language fine tuning we have different kinds of texts online. The main categorization divides them based on two criteria:
- Format
- Domain
### Format
This indicates the way in which the text is written, in order to convey a certain meaning in this matter. This subdivision was made according to the way that these texts are useful for the task of text generation. common styles are, prose poetry and comedy. 

#### Non dialogue prose
_Prose texts are literary medium distinguished from poetry especially by its greater irregularity and variety of rhythm and its closer correspondence to the patterns of everyday speech_

These kind of texts are perfect for training LLms models, they provide a natural flow in providing or explaining information. 

#### Poetry

https://www.merriam-webster.com/dictionary/prose

_Poetry is a writing style that formulates a concentrated imaginative awareness of experience in language chosen and arranged to create a specific emotional response through meaning, sound, and rhythm_

The most important difference when selecting the corpus, since poetry is structured in an artistic and selected way, thus the word order, choice of word and also rhyme does not reflect everyday conversation like prose does.
These characteristics of poetry becomes an issue when used for training LLms since they can produce un natural results, at least for my task.
#### Theater plays

Prose is better in this matter, but inside the realm of prose there can also be some issues. One of the genres of prose are theater plays.
_A **theatrical play** is a **dramatic text written for performance on stage**, characterized by **direct dialogue between characters**, a structured division into **acts and scenes**, and the inclusion of **stage directions** that guide performance._

Dialogue based theater genres like comedy/drama, are often structured in direct dialogues. So for the purpose of being able to generate continual text this setting is not suitable either, the model will learn to generate dialogues which is perceived as unnatural.

For all the reasons above, it was made the decision to differentiate between non dialogue prose, theater and poetry.

### Domain
The other subdivision is more semantic, the reason is related to the specific task that the model has to execute. It is common procedure of dividing texts (mainly non dialogical prose texts) into domains each one has its own register and style and way of displaying information.

Their definition is not strictly defined since it is all common practice.
#### Literature
It includes fictional stories and events narrated usually through third/first person, they were written for entertaining so they use specific vocabulary and style.

*vedere se si devono includere le commedie e e le poesie*

Examples of this include: Narrative, Stories, Fiction.

#### Encyclopedical
Text for explaining and teaching information by providing descriptions and using technical and scientific terms. They are more formal and precise.

Examples of this include: Wikipedia, descriptive texts
#### News
Texts produced by journalistic media that deal with current events, using a clear and objective language style, they provide reasons that support their theory. 

Ex. newspapers.
## Methods

The general procedure adopted when building the corpus was this:
- searching for the text online
- extracting the source data into txt format
- Parsing it and saving it into json files.

### Searching

This corpus was built by scraping texts from websites and partially extracting text from pictures. The main sources for regional languages in the realm of italian web, were these:
- the wiki environment: including wikipedia, wikisource and wikiquote. In recent years wikipedia has been expanded with pages and entire domains in regional/minority languages from all over the world. In this case there exist wikipedia in sicilian and neapolitan.
- Manuzio liber liber project: It is a free organization that publishes free books and promotes free access to culture on the web. It is the main source for italian and dialectal literature.
- Archive.org: This website contains data and snapshot of websites on the past, this includes also metadata such as pdf, or scanned images of texts. 
- Dialectal italian websites: They contains information about specific dialects together with other cultural informations, they are usually written in a very low register language.
- Social networks: This includes comments or posts on social media such as reddit or facebook.
- OPUS: Open parallel corpus it is a collection of parallel and monolingual text corpora used for Machine translation and MNLP research. There were some parallel texts of sicilian and neapolitan.


Regarding all these sources there is the question about privacy and fair use
#### Open source texts
This is one of the main issue that comes with NLP and AI in general, since these models need training data, it is not uncommon that copyrighted data is unknowingly used to train these models. In the european union there is an ongoing debate asking for clearer rules about AI generated content and 

The European Parliament’s July 2025 study highlights a **legal mismatch** between current copyright exceptions—such as text and data mining—and the realities of AI training practices, which were not foreseen by earlier legislation
https://www.europarl.europa.eu/RegData/etudes/STUD/2025/774095/IUST_STU(2025)774095_EN.pdf

### Extraction

#### Wikipedia

The aim is to extract all the textual content from wikipedia pages in a certain language, the most efficient way to do so is by doing API calls. 

Wiki has an efficient api system where it could be specificed in the call the kind of data you want to get. In order to do that it is neccessary to provide the URL api endpoint and the title of the page you want to download. 

In my case, i found the wikipedia dump pages for neapolitan and sicilian, since wiki has it's own domain in these matter 

https://dumps.wikimedia.org/scnwiki/latest/

https://dumps.wikimedia.org/napwiki/latest/

There is the file that specifies the list of all the titles of each page in that language. 

These requests used the requests library and it required the full html text of the wikipedia page with that name. 

[]

The text is then extracted and parsed using the beautiful soup library, which extracts all the text that appears between paragraphs. Using this function.

The resulting texts for each page are put into a json file, so that each json element corresponds to a page if it is not empty.

After this there was the processing of parsing wikipedia pages, to get a useful text.

#### Wikisource and reddit

The same concept as wikipedia was applied to wikisource pages and reddit. After retrieving all the wikisource links using dumps, I made html requests and then parsed the content. As for reddit I used their specific API to get all the posts made by a certain user in a certain subreddit. 
#### Text from images and pdfs.

Most of the literature content, as well as poetry and theatrical works, was downloaded in either pdf format or png image.

For pdf I used the *pdfminer* library, which extracts all the visible texts and I save it into a .txt file.
https://pypi.org/project/pdfminer/
Sometimes one of the errors is to 
For image I used tesseract which is one of the most common technologies to perform character extraction from images.

Tesseract OCR is an open source image to text converter, it supports multiple languages, for my research I dowloaded the italian package, given the relative similarities between the regional languages and italian in terms of orthography and character used.
https://tesseract-ocr.com/

The rest of corpus was extracted by doing web scraping so, either copying and pasting text into txt file or downloading the html files and parsing them.

#### Opus
The opus corpus was downloaded from the official opus website.

### Parsing


#### General principles
There were some common principles accross all the specific parsing for each type. 
- Removing the repeated strings
- Page numbers
- Special characters

#### Parsing wikipedia

This process followed these steps:
- Removing duplicates: This issue is due to the presence in the wikipedia dump of the same title with subtle changes. 
- removing the content between square brackets, which usually indicates the citations to bibliography., and also the list of terms, indicated with special characters such as | *| etc..
- Removing the most common sentences, since especially in regional language articles there are numerous small articles which describe the same feature, like "x is a municipality of the province of Y". If these parts were left untouched they can negatively condition the output of the model, since it would learn to produce more sentences like these.
- Identifying and excluding pages that are written in varieties of these languages that are too distant from the standard. This regarded the specific case of Sicilian, since in the most broad definition Sicilian language indicates also the varieties spoken in calabria and salento, with especially the last ones being particularly different from insular sicilian. So thanks to some morphological characteristics like the usage of a specific form of to be "ete" and others I was able to identify and exclude these pages. Most of them appear to be duplicated of the sicilian form.
#### Parsing comedy

They are texts made by a continuos dialogue, where each speaker is identified and there are also brief description of the scenario and the action that the actor is performing. The Italian “dialectal” comedies and theater, contains usually funny or comical language, the description of the scenario is usually in Italian.

There can be numerous formats in which these dialogue can be represented in writing, more in general they consists in "line" each line is made by the actor and the text of the line. These two parts are delimited in different ways:
- X : Y
- X \n\n Y
- X -- Y
- etc...

The usage of the python regular expression library was essential this is the general structure of the function used.

To do this the code consisted in splitting and separating every single line, ignoring the title and other acts titles. Of course this has to take into account the specific structure of the line itself.

Another thing are the acting indications which are commonly written in brackets both square and round, which in the case of dialectal italian commedy are in italian. 


The textual line can be found in multiple text lines, so we need specific functions to extract them, the results of each theater line are saved in a json list of dictionaries with field actor and text.

The scene description and other prose text are saved in  the same way having the field actor empty, of course in the case where it was written in the regional language.

Insert code examples and parsing examples

[]
Example of output json.

#### Parsing prose and poetry

Parsing prose and poetry required similar technique, in fact the main issue was to extract pure text, so removing the links and the formatting typical of the extracted pdfs. 

In the case of more complex literature like a collection of novels, the main focus was to divide them  


However there is a problem with this kind of texts because they contain battute so they cannot be directly used for language training, so there needs to be paraphrasing.

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


