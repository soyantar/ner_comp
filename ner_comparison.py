import json
import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.tree import Tree
from SPARQLWrapper import SPARQLWrapper, JSON
import spacy
from textblob import TextBlob
from collections import Counter

def get_number_of_elements(list):
    count = 0
    for element in list:
        count += 1
    return count

def get_data(filename):
    file = open(str(filename))
    data = json.load(file)
    tmp_list = data['questions']
    count = get_number_of_elements(tmp_list)
    questions = []
    query = []
    for i in range(0, count):
        lst = list(tmp_list[i].values())
        if lst[1] == 'resource':
            que = lst[-3]
            en_que = que[3]
            quet = list(en_que.values())
            questions.append(quet[1])
            q1 = lst[6]
            q2 = list(q1.values())
            query.append(q2[0])
    return questions,query

def sort_list_by_count(lst):
    c = Counter(lst)
    flist = sorted(c, key=c.get, reverse=True)
    sorted_list = list(dict.fromkeys(flist))
    return sorted_list

def get_ner_nltk(text):
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
    sorted_ner=sort_list_by_count(continuous_chunk)
    return sorted_ner

def get_ner_spacy(text):
    spacy_ner = spacy.load("en_core_web_sm")
    ne = spacy_ner(text)
    result=[]
    for i in ne.ents:
        result.append(str(i.text))
    sorted_ner = sort_list_by_count(result)
    return sorted_ner

def get_ner_textblob(text):
    blob = TextBlob(text)
    ne = list(blob.noun_phrases)
    cap_ne = []
    for i in ne:
        cap_ne.append(i.capitalize())
    sorted_ner = sort_list_by_count(cap_ne)
    return sorted_ner

def get_ner_testNLTK(text):
    chunked = nltk.ne_chunk(pos_tag(word_tokenize(text)))
    ner_list = []
    def getNER(tree):
        for i in tree:
            if hasattr(i, 'label'):
                getNER(i)
            else:
                tag = str(i[1])
                if tag[0] == "N" and tag[1] == "N":
                    ner_list.append(i[0])
    getNER(chunked)
    ner_list_only_letter = []
    for element in ner_list:
        if len(element)>1 and element[0] != ' ':
            ner_list_only_letter.append(element)
    cap_ne = []
    for i in ner_list_only_letter:
        cap_ne.append(i.capitalize())
    sorted_ner = sort_list_by_count(cap_ne)
    return sorted_ner

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

def getwikipage(dburl):
    tmp="<http://xmlns.com/foaf/0.1/isPrimaryTopicOf>"
    query = "SELECT * WHERE {<"+dburl+"> "+tmp+" ?c.}"
    sparql.setQuery(query)
    result_list = sparql.query().convert()
    return result_list

def getdblink(lst):
    result=[]
    for el in lst:
        tmp_string = str(lst.values())
        tmp_list = tmp_string.split("'")
        result = [idx for idx in tmp_list if idx[0].lower() == 'h']
    return result

def getwikilink(s):
    tmp_string = str(s)
    tmp_list = tmp_string.split("'")
    result = [idx for idx in tmp_list if idx[0] == 'h' and idx[1] == 't']
    return result

def get_ne_from_dataset(query):
    tmp_list1=query.split("/")
    ne_result=[]
    co=get_number_of_elements(tmp_list1)
    tmp_ne_result = []
    for x in range(0,co):
        if tmp_list1[x]=='resource':
            entity=(tmp_list1[x+1].split(">"))[0]
            tmp_ne_result.append(entity)
            tmp_list2=tmp_list1[-1].split(":")
            cv=get_number_of_elements(tmp_list2)
            for y in range(0,cv):
                if (str(tmp_list2[y]))[-1]=="s" and (str(tmp_list2[y]))[-2]=="e" and (str(tmp_list2[y]))[-3]=="r":
                    res=tmp_list2[y+1].split(" ")
                    tmp_ne_result.append(res[0])
                else:
                    continue
        else:
            continue
    tmp_ne_result_2=[]
    for ele in tmp_ne_result:
        if len(ele) > 1:
            tmp_ne_result_2.append(ele)
    for element in tmp_ne_result_2:
        divided_named_entity=element.split("_")
        named_entity=" ".join(divided_named_entity)
        ne_result.append(named_entity)
    return list(dict.fromkeys(ne_result))

def precision_recall(ner_list,dataset_entity_list):
    true_positive=0
    false_positive=0
    false_negative=get_number_of_elements(dataset_entity_list)
    ner_count=get_number_of_elements(ner_list)
    dataset_count=get_number_of_elements(dataset_entity_list)

    for ner_element in range(0,ner_count):
        for dataset_element in range(0,dataset_count):
            if ner_list[ner_element]==dataset_entity_list[dataset_element]:
                true_positive+=1
                false_negative-=1
        false_positive+=1
    false_positive-=true_positive
    if true_positive+false_positive>0 and true_positive+false_negative>0:
        precision=true_positive/(true_positive+false_positive)
        recall=true_positive/(true_positive+false_negative)
    else:
        precision=0
        recall=0
    return precision,recall

def get_result_of_ne(element):
    result = []
    disambiguate=disambiguation(element)
    dblink=getdblink(disambiguate)
    tmp_wikipage = []
    for x in dblink:
        tmp = getwikipage(x)
        tmp_wikipage.append(tmp)
    wikipage = getwikilink(tmp_wikipage)
    if wikipage:
        for el in wikipage:
            result.append(el)
    return result
def firstwritesegment(question):
    f.write("\t\t")
    f.write("\"question\":\"" + question + "\",\n")
    f.write("\t\t")
    f.write("\"nltk\":[")
def secondwritesegment(ent_num,element,output):
    f.write("\n\t\t\t\t{\n")
    f.write("\t\t\t\t\t")
    f.write("\"entity" + str(ent_num) + "\":\"" + element + "\",\n")
    f.write("\t\t\t\t\t")
    f.write("\"wikipage\":\"" + str(output) + "\"\n")

def precision_recall_segment(precision,recall):
    f.write("\t\t\t\t},\n\t\t\t\t{\n")
    f.write("\t\t\t\t\t\"precision\":\"" + str(precision) + "\",\n")
    f.write("\t\t\t\t\t\"recall\":\"" + str(recall) + "\"\n")
    f.write("\t\t\t\t}\n")
def entitysegment():
    f.write("\t\t\t\t},\n")

def beforesegment(ner_name):
    f.write("\t\t\t\t],\n")
    f.write("\t\t")
    f.write("\""+ner_name+"\":[")


f=open("finaldata.json","w");
f.write("[\n")
fname="qald-9-train-multilingual.json"
questions=(get_data(fname)[0])
queries=(get_data(fname)[1])

def final_process():
    f.write("\t{\n")
    t = 1
    r = get_number_of_elements(questions)
    for_nltk_average_precision=0
    for_spacy_average_precision=0
    for_textblob_average_precision=0
    for_testnltk_average_precision=0
    for_nltk_average_recall = 0
    for_spacy_average_recall = 0
    for_textblob_average_recall = 0
    for_testnltk_average_recall = 0

    for x in range(0,r):
        nenltk = get_ner_nltk(questions[x])
        nespacy = get_ner_spacy(questions[x])
        netextblob = get_ner_textblob(questions[x])
        netestnltk = get_ner_testNLTK(questions[x])
        dataset_entity = get_ne_from_dataset(queries[x])
        nltk_precision_recall=precision_recall(nenltk,dataset_entity)
        spacy_precision_recall=precision_recall(nespacy,dataset_entity)
        textblob_precision_recall=precision_recall(netextblob,dataset_entity)
        testnltk_precision_recall=precision_recall(netestnltk,dataset_entity)
        for_nltk_average_precision+=nltk_precision_recall[0]
        for_nltk_average_recall+=nltk_precision_recall[1]
        for_spacy_average_precision += spacy_precision_recall[0]
        for_spacy_average_recall += spacy_precision_recall[1]
        for_textblob_average_precision += textblob_precision_recall[0]
        for_textblob_average_recall += textblob_precision_recall[1]
        for_testnltk_average_precision += testnltk_precision_recall[0]
        for_testnltk_average_recall += testnltk_precision_recall[1]

        print(str(t) + " " + questions[x] + " ")
        firstwritesegment(questions[x])
        print("NLTK")
        ent_num = 1
        for element in nenltk:
            output = get_result_of_ne(element)
            secondwritesegment(ent_num,element,output)
            if element==nenltk[-1]:
                precision_recall_segment(nltk_precision_recall[0],nltk_precision_recall[1])
            else:
                entitysegment()
            ent_num += 1
            print(element, end=' ')
            print(output)
        print("NLTK : precision:"+str(nltk_precision_recall[0])+"  recall:"+str(nltk_precision_recall[1]))
        ner_name = "spacy"
        beforesegment(ner_name)
        print("Spacy")
        ent_num = 1
        for element in nespacy:
            output = get_result_of_ne(element)
            secondwritesegment(ent_num,element,output)
            if element == nespacy[-1]:
                precision_recall_segment(spacy_precision_recall[0],spacy_precision_recall[1])
            else:
                entitysegment()
            ent_num += 1
            print(element, end=' ')
            print(output)
        print("Spacy : precision:" + str(spacy_precision_recall[0]) + "  recall:" + str(spacy_precision_recall[1]))
        ner_name="textblob"
        beforesegment(ner_name)
        print("TextBLOB")
        ent_num = 1
        for element in netextblob:
            output = get_result_of_ne(element)
            secondwritesegment(ent_num,element,output)
            if element == netextblob[-1]:
                precision_recall_segment(textblob_precision_recall[0],textblob_precision_recall[1])
            else:
                entitysegment()
            ent_num += 1
            print(element, end=' ')
            print(output)
        print("TextBLOB : precision:" + str(textblob_precision_recall[0]) + "  recall:" + str(textblob_precision_recall[1]))
        ner_name="testnltk"
        beforesegment(ner_name)
        print("testNLTK")
        ent_num = 1
        for element in netestnltk:
            output = get_result_of_ne(element)
            secondwritesegment(ent_num,element,output)
            if element == netestnltk[-1]:
                precision_recall_segment(testnltk_precision_recall[0],testnltk_precision_recall[1])
            else:
                entitysegment()
            ent_num += 1
            print(element, end=' ')
            print(output)
        print("testNLTK : precision:" + str(testnltk_precision_recall[0]) + "  recall:" + str(testnltk_precision_recall[1]))
        f.write("\t\t\t\t] ,\n")
        f.write("\t\t")
        f.write("\"fromdataset\":[")
        print("Dataset")
        ent_num = 1
        for element in dataset_entity:
            if len(element)>1:
                f.write("\n\t\t\t\t{\n")
                f.write("\t\t\t\t\t")
                f.write("\"entity" + str(ent_num) + "\":\"" + element + "\"\n")
                if element == dataset_entity[-1]:
                    f.write("\t\t\t\t}\n")
                else:
                    f.write("\t\t\t\t},\n")
                ent_num += 1
                print(element,end=' ')
        f.write("\t\t\t\t] \n")

        if x==r-1:
            f.write("\t}\n")
        else:
            f.write("\t},\n")
            f.write("\t\t{")
        t+=1
        print(" ")
        print(" ")
    f.write("]")
    f.close()
    print("NLTK")
    print("Average Precision: "+str(for_nltk_average_precision/r))
    print("Average Recall: "+str(for_nltk_average_recall/r))
    print("SpaCy")
    print("Average Precision: " + str(for_spacy_average_precision / r))
    print("Average Recall: " + str(for_spacy_average_recall / r))
    print("TextBlob")
    print("Average Precision: " + str(for_textblob_average_precision / r))
    print("Average Recall: " + str(for_textblob_average_recall / r))
    print("testNLTK")
    print("Average Precision: " + str(for_testnltk_average_precision / r))
    print("Average Recall: " + str(for_testnltk_average_recall / r))
final_process()

