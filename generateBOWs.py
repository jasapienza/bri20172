import lxml.etree as ET
import random
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords

def readXMLUrls(filexml):
    documents = []
    tree = ET.parse(filexml)
    for doc in tree.xpath('document'):
        url = doc.attrib['url']
        if doc.attrib['isSource'] == 'yes':
            isSource = 1
        else:
            isSource = 0
        tokens = [t.attrib['name'] for t in doc.xpath('token')]
        documents.append((len(documents),url,tokens,isSource))
    return documents

def stemmer(docs):
    print "Begin!"
    PS = PorterStemmer()
    result = []
    for doc in docs:
        print "Processing " + doc[1]
        tokens = [t for t in doc[2] if (len(t)>2 and t not in stopwords.words('english'))]
        terms = map(PS.stem,tokens)
        result.append((doc[0],doc[1],terms,doc[3]))
        print "Finished! " + str(len(terms)) + " terms processed!"
    return result

def splitDocs(docs,percent):
    docs1 = []
    docs2 = []
    i = 0
    while i < len(docs):
        if random.random() < percent:
            docs1.append(docs[i])
        else:
            docs2.append(docs[i])
        i += 1
    return docs1,docs2

def saveBAG(filename,docs):
	roottag = ET.Element("root")
	for _,urldoc,terms,isSrc in docs:
		doctag = ET.SubElement(roottag, "document", url=urldoc, isSource=unicode(isSrc))
		for term in terms:
			ET.SubElement(doctag, "term", name=term)
	tree = ET.ElementTree(roottag)
	tree.write(filename)

print "Reading XML..."
documents = readXMLUrls("urlContents.xml")
print "Applying the Stemmer..."
docs_stemmer = stemmer(documents)
docs_training, docs_test = splitDocs(docs_stemmer,0.8)
del documents,docs_stemmer
print "Saving Bag of Words..."
saveBAG("BOW_training.xml",docs_training)
saveBAG("BOW_test.xml",docs_test)
print 'Done!'
