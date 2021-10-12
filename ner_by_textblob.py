from textblob import TextBlob
from bs4 import BeautifulSoup
import urllib.request
import nltk
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import Counter
nltk.download('brown')
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

sparql = SPARQLWrapper("https://dbpedia.org/sparql")
sparql.setReturnFormat(JSON)
def disambiguation(name):
    try:
        query = "select distinct * where {?x rdfs:label '"+name+"' @en.}"
        sparql.setQuery(query)
        results_list = sparql.query().convert()
    except:
        tem=name.split("'")
        query = "select distinct * where {?x rdfs:label '" + tem[0] + "' @en.}"
        sparql.setQuery(query)
        results_list = sparql.query().convert()
    return results_list
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
def getwikipage(dburl):
    tmp="<http://xmlns.com/foaf/0.1/isPrimaryTopicOf>"
    query = "SELECT * WHERE {<"+dburl+"> "+tmp+" ?c.}"
    sparql.setQuery(query)
    result_list = sparql.query().convert()
    return result_list

data=str(html2txt())
blob = TextBlob(data)
ner=list(blob.noun_phrases)
cap_ner=[]
for i in ner:
    cap_ner.append(i.capitalize())

c=Counter(cap_ner)
flist=sorted(c,key=c.get,reverse=True)
sorted_ne = list(dict.fromkeys(flist))
t=1
with open("textblobOUTPUT.txt","w") as f:
    for i in sorted_ne:
        result=disambiguation(i)
        dblink=getdblink(result)
        tmp_wikipage = []
        for x in dblink:
            tmp = getwikipage(x)
            tmp_wikipage.append(tmp)
        wikipage = getwikilink(tmp_wikipage)
        if wikipage:
            print(str(t)+" "+i)
            f.write(str(t)+" "+i)
            f.write(" ")
            print(wikipage)
            f.write(str(wikipage))
            f.write("\n")
            t+=1
        else:
            continue
f.close()