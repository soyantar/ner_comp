import urllib.request
from bs4 import BeautifulSoup
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.tree import Tree
from SPARQLWrapper import SPARQLWrapper, JSON
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
def html2txt():
    try:
        url=str(input("Enter URL: "))
        r= urllib.request.urlopen(url).read()
        soup = BeautifulSoup(r,'lxml')
        return soup.body.get_text()
    except :
        print("Sorry, not able to access the content \n")
        text=str(input("Enter Text Here: "))
        return text

def get_continuous_chunks(text):
    chunked = nltk.ne_chunk(pos_tag(word_tokenize(text)))
    continuous_chunk = []
    current_chunk = []
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        if current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    return continuous_chunk

sparql = SPARQLWrapper("https://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)

def disambiguation(name):
    query = "select distinct * where {?x rdfs:label '"+name+"' @en.}"
    sparql.setQuery(query)
    results_list = sparql.query().convert()
    return results_list

def getwikipage(dburl):
    tmp="<http://xmlns.com/foaf/0.1/isPrimaryTopicOf>"
    query = "SELECT * WHERE {<"+dburl+"> "+tmp+" ?c.}"
    sparql.setQuery(query)
    result_list = sparql.query().convert()
    return result_list

def getdblink(list):
    result=[]
    for el in list:
        tmp_string = str(list.values())
        tmp_list = tmp_string.split("'")
        result = [idx for idx in tmp_list if idx[0].lower() == 'h']
    return result

def getwikilink(s):
    result=[]
    tmp_string = str(s)
    tmp_list = tmp_string.split("'")
    result = [idx for idx in tmp_list if idx[0] == 'h' and idx[1] == 't']
    return result
data=str(html2txt())
ner=get_continuous_chunks(data)
print(ner)
t=1
with open("nltkOUTPUT.txt","w") as f:
    for element in ner:
        result = disambiguation(str(element))
        dblink = getdblink(result)
        tmp_wikipage=[]
        for x in dblink:
            tmp=getwikipage(x)
            tmp_wikipage.append(tmp)
        wikipage=getwikilink(tmp_wikipage)
        if wikipage:
            print(str(t)+" "+element)
            f.write(str(t)+" "+element)
            f.write(" ")
            print(wikipage)
            f.write(str(wikipage))
            f.write("\n")
            t+=1
        else:
            continue
f.close()
