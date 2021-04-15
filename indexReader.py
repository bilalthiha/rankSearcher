import ast
import sys

#dictionary to store inv index in memory
indexDict = {}
docSize = 0

#compression mode
comprMode = 0 #default no compression/dictionary data structure

#========================= Dictionary Interfaces ================================
def isTermPresentInDict(term):
    global indexDict
    result = False
    if term in indexDict.keys():
        result = True
    else:
        result = False               
    return result
    
def getDocListOfTermInDict(term):
    global indexDict
    rawDList = []
    dList = []
    if term in indexDict.keys():
        rawDList = (indexDict[term])[1:] #filter out doc frequency of term
        for i in range(len(rawDList)):
            if (i%2 != 0): #filter out term frequency of docs at even list indices
                dList.append(rawDList[i])            
    else:
        dList = []
    return dList
    
def getDocFreqOfTermInDict(term):
    global indexDict
    dFreq = 0
    if term in indexDict.keys():
        dFreq = (indexDict[term])[0] #first index of doc lis is doc id
    else:
        dFreq = 0
    return dFreq

def getTermFreqOfDocInDict(term, docId):
    global indexDict
    tFreq = 0
    rawDList = []
    docTfDict = {} #<doc, tf> dict
    if term in indexDict.keys():
        rawDList = (indexDict[term])[1:] #filter out doc frequency of term
        for i in range(len(rawDList)):
            if (i%2 != 0): #check each doc Id and add in <doc, tf> dict
                if rawDList[i] not in docTfDict.keys():
                    docTfDict[rawDList[i]] = int(rawDList[i-1]) #element before docId is its term frequency
        #get freqency of term in doc
        if docId in docTfDict.keys():
            tFreq = docTfDict[docId]                    
    else:
        tFreq = 0
    return tFreq
    
def getNumOfTotalDocs():
    return docSize    

def getDictSize():
    global indexDict
    size = sys.getsizeof(indexDict)
    return size

def invIdxFile2Dict(flPath):
    currLine = 'init'
    global indexDict
    global docSize
    try:
        invIdxFile = open(flPath, 'r', encoding ='utf-8')
    except FileNotFoundError:
        print('Provided inverted-index file does not exist. Please check file naming or directory. Program ends.')        
        sys.exit()
            
    #read total number of documents and update global doc size
    currline = invIdxFile.readline()
    halfline = currline.lstrip('Total documents:')
    docSize = int(halfline.rstrip('\n'))
    
    while(currLine != ''):
        term = ''
        termComponents = []
        lst = []
        currLine = invIdxFile.readline()
        if(currLine != ''):
            term = currLine[:currLine.index(':')]
            termComponents = term.split('\'')
            term = str(termComponents[1]) # the middle one is term [', term, ']
            lst = ast.literal_eval(currLine[(currLine.index(':')+ 1):])
            indexDict[term] = list(lst)
    #print(indexDict)    
    invIdxFile.close()
#=================================================================================

def isTermPresent(term):    
    result = False
    if (comprMode == 0): #no compression/dictionary
        result = isTermPresentInDict(term)
    #else: #dictAsStringMethod
        #RFU
    return result

def getDocListOfTerm(term):    
    docList = []
    if (comprMode == 0): #no compression/dictionary
        docList = getDocListOfTermInDict(term)
    #else: #dictAsStringMethod
        #RFU
    return docList
    
def getDocFreqOfTerm(term):
    docFreq = 0
    if (comprMode == 0): #no compression/dictionary
        docFreq = getDocFreqOfTermInDict(term)
    #else: #dictAsStringMethod
        #RFU
    return docFreq
    
def getTermFreqOfDoc(term, docId):
    termFreq = 0
    if (comprMode == 0): #no compression/dictionary
        termFreq = getTermFreqOfDocInDict(term, docId)
    #else: #dictAsStringMethod
        #RFU
    return termFreq        

    
def getIndexSizeInMemory():
    size = 0
    if (comprMode == 0): #no compression/dictionary
        size = getDictSize()
    #else: #dictAsStringMethod
        #RFU
    return size
    
def readInvIdxFile(inFile):
    if (comprMode == 0): #no compression/dictionary
        invIdxFile2Dict(inFile)
    #else: #dictAsStringMethod
        #RFU
       
def cleanGlobalData():
    global indexDict, docSize, comprMode
    del indexDict, docSize, comprMode    
