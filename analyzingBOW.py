import lxml.etree as ET
import math
import numpy
import csv
import nltk

def readXMLBOW(filexml):
    documents = []
    tree = ET.parse(filexml)
    for doc in tree.xpath('document'):
        url = doc.attrib['url']
        if doc.attrib['isSource'] == '1':
            isSource = 1
        else:
            isSource = 0
        terms = [t.attrib['name'] for t in doc.xpath('term')]
        documents.append((len(documents),url,terms,isSource))
    return documents

def calculateFreqInDocs(documents):
   uniqueterms = []
   for doc in documents:
       uniqueterms.extend(list(set(doc[2])))
   return nltk.FreqDist(uniqueterms)

def calculateFreqTermsInEachDoc(documents):
    docs_freq = []
    for doc in documents:
        docs_freq.append((doc[0],doc[1],nltk.FreqDist(doc[2])))
    return docs_freq

def calculateFreqTermsInCorpus(documents):
    allterms = []
    for doc in documents:
        allterms.extend(doc[2])
    return nltk.FreqDist(allterms),len(allterms)

def calculateMatrixTermDocument(freq_in_docs,docs_freq,freq_terms_in_corpus,terms):
    cnt_docs = float(len(docs_freq))
    matrix = numpy.zeros((len(docs_freq),len(terms)),dtype=float)
    j = 0
    for term in terms:
        idf = math.log(cnt_docs/freq_in_docs[term])
        for i,_,freqdist in docs_freq:
            if freqdist.N()>0:
                tf = float(freqdist[term])/freqdist[freqdist.max()]
                matrix[i,j] = tf*idf
        j += 1
    return matrix


def saveCSVFreqAllTerms(filename,freq_terms_in_corpus,count_allterms):
    with open(filename,'wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=';',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['TERM','CORPUSCOUNT','CORPUSFREQUENCY'])
        count_allterms = float(count_allterms)
        for term,tcnt in freq_terms_in_corpus.most_common():
            writer.writerow([term.encode('utf-8'),tcnt,tcnt/count_allterms])

def saveCSVFreqTermsInDocuments(filename,freq_in_docs,count_docs):
    with open(filename,'wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=';',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(['TERM','DOCCOUNT','DOCFREQUENCY'])
        count = float(count_docs)
        for term,tcnt in freq_in_docs.most_common():
            writer.writerow([term.encode('utf-8'),tcnt,tcnt/count])

def saveCSVMatrixTermDocuments(filename,matrix,terms,docs):
    with open(filename,'wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=';',quoting=csv.QUOTE_MINIMAL)
        height = matrix.shape[0]
        writer.writerow(["TERM/DOCNUM","isSource"]+[t.encode('utf8') for t in terms])
        i = 0
        while i < height:
            writer.writerow([docs[i][0],docs[i][3]] + list(matrix[i,:]))
            i += 1

def saveCSVVectorTermDocuments(filename,terms_sorted):
    with open(filename,'wb') as csvfile:
        writer = csv.writer(csvfile,delimiter=';',quoting=csv.QUOTE_MINIMAL)
        writer.writerow(["TERM","SUM_IDFTF","MATRIX_COL"])
        for term in terms_sorted:
            writer.writerow([term[1],term[0],term[2]])

def sortTermsByWeight(terms,vector_sum_cols_term_doc):
    result = [(vector_sum_cols_term_doc[i],terms[i].encode('utf8'),i) for i in range(len(terms))]
    result.sort(reverse=True)
    return result

print "Reading XML..."
docs = readXMLBOW('BOW_training.xml')
print "Analyzing dataset..."
freq_in_docs = calculateFreqInDocs(docs)
docs_freq = calculateFreqTermsInEachDoc(docs)
freq_terms_in_corpus,count_allwords = calculateFreqTermsInCorpus(docs)
terms = [t for t,_ in freq_terms_in_corpus.most_common()]
print "Computing Matrix Term Document..."
matrix_term_doc = calculateMatrixTermDocument(freq_in_docs,docs_freq,freq_terms_in_corpus,terms)
vector_sum_cols_term_doc = matrix_term_doc.sum(axis=0,dtype=float)
terms_sorted = sortTermsByWeight(terms,vector_sum_cols_term_doc)
print "Saving results..."
saveCSVFreqAllTerms('freq_terms_in_corpus.csv',freq_terms_in_corpus,count_allwords)
saveCSVFreqTermsInDocuments('freq_in_docs.csv',freq_in_docs,len(docs_freq))
saveCSVVectorTermDocuments('vector_sum_cols_term_doc.csv',terms_sorted)
saveCSVMatrixTermDocuments('matrix_term_doc.csv',matrix_term_doc,terms,docs)
print 'Done!'
