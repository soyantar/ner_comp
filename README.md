
Requirement:

-python packages: nltk,spacy,textblob,json,SPARQLWrapper,urllib,bs4
-dataset : qald-9-train-multilingual.json


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
