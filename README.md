Description:

Named Entity Recognition:
    Named entity recognition or entity extraction is technique in Natural Language processing that finds named entities in text and classifies them to predefined groups(Person,Organization,Location etc.). Named entities are important sets of elements to understand given text. Most of entities comes from part of speech(noun,verb,adjactive) but Nouns are essential to understand subtle details in text.Named Entity Recognition (NER) is a process where a sentence or a chunk of text is parsed through to find entities that can be put under categories like names,places and organizations. Find more details here: "https://en.wikipedia.org/wiki/Named-entity_recognition"
    
Named Entity Disambiguation:
    In natural language processing, entity linking, also referred to as named-entity linking (NEL), named-entity disambiguation (NED), named-entity recognition and disambiguation (NERD) or named-entity normalization (NEN) is the task of assigning a unique identity to entities (such as famous individuals, locations, or companies) mentioned in text. For example, given the sentence "Paris is the capital of France", the idea is to determine that "Paris" refers to the city of Paris and not to Paris Hilton or any other entity that could be referred to as "Paris". In this project, entity linking is performed on dbpedia.Find more details here:"https://en.wikipedia.org/wiki/Entity_linking"

Overview:

  This project is just for study purpose. In this project,I've used different tools to generate named entities from text. You can find different files for this tools(nltk,spacy,textblob). Furthermore, I've selected QALD dataset to check output of these three tools. There are many questions in dataset that contains named entities. I've passed each question through nltk,spacy and textblob and performed entity disambiguation or entity linking for each and every entity. Also, from dataset I've found perfect entities that are present in every question and based on that I've computed precision and recall for nltk,spacy and textblob. 

Requirement:

-python packages: nltk,spacy,textblob,json,SPARQLWrapper,urllib,bs4

-dataset : qald-9-train-multilingual.json

How to run:

> python ner_comparison.py


About "ner_comparison.py"

-Dataset used here is from Question Answering over Linked Data (QALD) "http://qald.aksw.org/", download it from here: "https://2018.nliwod.org/challenge" (~Training Data)

-get named entities from three different packages:"NLTK" https://www.nltk.org/ ,"spaCy" https://spacy.io/, "TextBlob" https://textblob.readthedocs.io/en/dev/

-by nltk get all entities separate ("Abraham Lincoln" will be considered two entities "Abraham" and "Lincoln"). This entities are stored as "testnltk"

-if dataset file is not in same directory please change fname.

-disambiguation and entity linking is performed on dbpedia : "https://www.dbpedia.org/"

-there are total 409 questions in dataset. These questions are filtered on basis of 'named entity presence' in question and query.

-named entities that are present in dataset are considered golden data and based on that precision and recall is generated

-output is stored in "final.json" file that includes: Question, named entities by nltk with wikipedia link, named entities by spacy with wikipedia link, named entities by textblob with wikipedia link, named entities by testnltk with wikipedia link ,dataset entities, precision and recall of nltk,spacy,textblob and testnltk


About "ner_by_nltk.py"

-It's simple ner that takes webpage link or text and finds all named entities.

-text option is available only if webpage is not accessible. so if you want to test for just text just enter anything random when it ask for link

-all related wikipedia links will be available in output(also in file "nltkOUTPUT.txt")

-entity linking is performed on dbpedia


About "ner_by_spacy.py"

-same as "ner_by_nltk",except output file is "spacyOUTPUT.txt"

-sometimes spacy entities include characters like "\n" that should not be in entity,so excluded those entities


About "ner_by_textblob.py"

-same as "ner_by_nltk",except output file is "textblobOUTPUT.txt"

-all entities returned by textblob is in lowercase. so, capitalized first alphabet in entity to get related wikipedia link

