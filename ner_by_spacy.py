import spacy
from bs4 import BeautifulSoup
import urllib.request
from SPARQLWrapper import SPARQLWrapper, JSON
from collections import Counter

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
    query = "select distinct * where {?x rdfs:label '"+name+"' @en.}"
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

spacy_ner = spacy.load("en_core_web_sm")
data=str(html2txt())
ner=spacy_ner(data)
contmp1=[]
for i in ner.ents:
    contmp1.append(str(i.text))
#print(Counter(contmp1))
c=Counter(contmp1)
flist=sorted(c,key=c.get,reverse=True)
sorted_ne = list(dict.fromkeys(flist))
t=1
#print(sorted_ne)
with open("spacyOUTPUT.txt","w") as f:
    for i in sorted_ne:
        try:
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
        except:
            continue
f.close()