# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 17:09:31 2016

@author: Jose Augusto Sapienza Ramos
"""

import lxml.etree as ET
import math
import numpy
import nltk
import csv
from sklearn import svm

def readXMLBOW(filexml):
    documents = []
    isSources = []
    tree = ET.parse(filexml)
    for doc in tree.xpath('document'):
        url = doc.attrib['url']
        if doc.attrib['isSource'] == '1':
            isSource = 1
        else:
            isSource = 0
        terms = [t.attrib['name'] for t in doc.xpath('term')]
        documents.append((url,terms))
        isSources.append(isSource)
    return documents,isSources

def readCSVVectorTermDocuments(filename,maxterms):
    with open(filename,'rb') as csvfile:
        weighted_terms = []
        csvreader = csv.reader(csvfile,delimiter=';',quoting=csv.QUOTE_MINIMAL)
        csvreader.next()
        for row in csvreader:
            weighted_terms.append((row[0],float(row[1]),int(row[2])))
            if maxterms == len(weighted_terms):
                return weighted_terms
    return weighted_terms

def readCSVMatrixTermDocuments(filename,terms):
    with open(filename,'rb') as csvfile:
        matrix = numpy.zeros((0,len(terms)),dtype=float)
        isdtsrc = []
        cols = []
        for t in terms:
            cols.append(t[2]+2)
        csvreader = csv.reader(csvfile,delimiter=';',quoting=csv.QUOTE_MINIMAL)
        csvreader.next() #skip first line
        for row in csvreader:
            isdtsrc.append(int(row[1]))
            matrix = numpy.vstack((matrix,map(float,[row[i] for i in cols])))
    return matrix,isdtsrc

def readCSVFreqTermsInDocuments(filename,terms):
    freq_in_docs = {}
    ts = [t[0] for t in terms]
    with open(filename,'rb') as csvfile:
        csvreader = csv.reader(csvfile,delimiter=';',quoting=csv.QUOTE_MINIMAL)
        csvreader.next()
        for row in csvreader:
            if row[0] in ts:
                freq_in_docs.update({row[0]: float(row[2])})
    return freq_in_docs
            

def computeTestVectors(docs,terms,freq_in_docs):
    ts = [t[0] for t in terms]
    vecs = numpy.zeros((len(docs),len(ts)),dtype=float)
    i = 0
    while i < len(docs):
        freqdist = nltk.FreqDist(docs[i][1])
        j = 0
        while j < len(ts):
            if (freqdist[ts[j]] > 0):
                vecs[i,j] = 1
                #idf = math.log(1.0/freq_in_docs[ts[j]])
                #tf = float(freqdist[ts[j]])/freqdist[freqdist.max()]
                #vecs[i,j] = idf*tf
            j += 1
        i += 1
    return vecs

def testSVM(clf,vecs,issrc):
    test = clf.predict(vecs)
    i = 0
    hit = 0
    miss = 0
    while i < len(test):
        if test[i] == issrc[i]:
            hit += 1
        else:
            miss += 1
        i += 1
    return hit,miss

print 'Begining...'
print 'Reading matrix term document...'
maxterms = 16384
terms = readCSVVectorTermDocuments('vector_sum_cols_term_doc.csv',maxterms)
freq_in_docs = readCSVFreqTermsInDocuments('freq_in_docs.csv',terms)
mtd,issrc = readCSVMatrixTermDocuments('matrix_term_doc.csv',terms)
print 'Training Suport Vector Classifier...'
clf = svm.SVC(kernel='linear', C = 1.0)
clf.fit(mtd,issrc)
print "Done! Now testing..."
docs_test,issrc_test = readXMLBOW('BOW_test.xml')
test_vecs = computeTestVectors(docs_test,terms,freq_in_docs)
hit,miss = testSVM(clf,test_vecs,issrc_test)
print "Report:\n"+ str(maxterms) + " top terms applied\n" + str(mtd.shape[0]+len(docs_test)) + " documents processed (" + str(mtd.shape[0]*100/(mtd.shape[0]+len(docs_test))) + "% training / " + str(len(docs_test)*100/(mtd.shape[0]+len(docs_test))) + "% test)\n" + str(hit) + " hits and " + str(miss) + " misses: " + "%.2f" % (hit*100.0/len(issrc_test))+"% of accuracy!"
print 'Done!'
