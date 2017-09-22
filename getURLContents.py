# -*- coding: utf-8 -*-
"""
Created on Sun Feb 21 10:08:44 2016

@author: Jose Augusto Sapienza Ramos
"""

from urllib import FancyURLopener
import re
import lxml.etree as ET
from bs4 import BeautifulSoup
import nltk
import csv
from nltk.corpus import stopwords
import socket
socket.setdefaulttimeout(10)

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11'

def generateSetsOfStopWords():
    result = {}
    for lang in stopwords.fileids():
        result.update({lang: set(stopwords.words(lang))})
    return result
 
def detectLanguage(tokens,stopwordsset):
    settokens = set(tokens)
    langdetected = 'unknown'
    maxscore = 0
    for lang in stopwords.fileids():
        score = len(settokens.intersection(stopwordsset[lang]))
        if score > maxscore:
            maxscore = score
            langdetected = lang
    return langdetected

def readCSVUrls(filename):
    urls = []
    with open(filename,"rb") as csvfile:
        content = csv.DictReader(csvfile,delimiter=';')
        for line in content:
            urls.append(line['URL'])
    return urls

def analyzeUrls(urls,language,stopwordsset,maxurls=999999999999):
    result = []
    counturls = min(len(urls),maxurls)
    i = 0
    for url in urls:
        i += 1
        print "[ "+str(i*100/counturls)+"% ]"+"  Processing " + url
        try:
            page = myopener.open(url)
            html = page.read()
        except:
            print ">>> Error getting html content <<<"
            continue
        soup = BeautifulSoup(html,"lxml")
        if len(soup) == 0:
            print "Page content is not HTML or page not found!"
            continue
        for script in soup(["script", "style"]):
            script.extract()    # rip it out
        raw = re.sub("[^a-zA-Z]"," ",soup.get_text()).lower()
        tokens = nltk.word_tokenize(raw)
        if len(tokens) < 50:
            print "Few tokens found! Skipped..."
            continue
        doclanguage = detectLanguage(tokens,stopwordsset)
        print "Detected language: " + doclanguage
        if language == doclanguage:
            result.append((url,tokens))
        if len(result) >= maxurls:
            return result
    return result

def saveXMLUrlsSelected(filename,docssrcselected,docsnonsrcselected):    
    roottag = ET.Element("root")
    for doc in docssrcselected:
        doctag = ET.SubElement(roottag, "document", url=doc[0], isSource='yes')
        for token in doc[1]:
            ET.SubElement(doctag, "token", name=token)
    for doc in docsnonsrcselected:
        doctag = ET.SubElement(roottag, "document", url=doc[0], isSource='no')
        for token in doc[1]:
            ET.SubElement(doctag, "token", name=token)
    tree = ET.ElementTree(roottag)
    tree.write(filename)

language = 'portuguese'
print 'Begin! Reading data...'
myopener = MyOpener()
urlssrc = readCSVUrls('urls_are_source.csv')
urlsnonsrc = readCSVUrls('urls_non_source.csv')
stopwordsset = generateSetsOfStopWords()
print 'Analyzing urls - part one: is source'
docssrcselected = analyzeUrls(urlssrc,language,stopwordsset)
print 'Analyzing urls - part two: not is source'
docsnonsrcselected = analyzeUrls(urlsnonsrc,language,stopwordsset,len(docssrcselected))
print str(len(docsnonsrcselected)+len(docssrcselected))+" documents found in "+language+"!"
print 'Writing output XML...'
saveXMLUrlsSelected('urlContent.xml',docssrcselected,docsnonsrcselected)
print 'Done!'