import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
import glob
import os
import indexReader
import sys
import math

#global query term-list for rank search
#global query term-list for rank search
rawQryText = ''
queryTermsForRankSearch = []
procQueryTextList = []
docListForRankSearch = []
docScoreListForRankSearch = {}
topNum = 0 

#optimization switches
CLEAN_DUPLICATED_INPUT = True
AND_OPERATION_OPTIMIZATION = True


def processQueryText(qryText):
    global rawQryText
    global procQueryTextList    
    rawQryText = qryText
    
    #1. Tokenize
    tkzr = RegexpTokenizer(r'\w+')
    tokenizedWords = tkzr.tokenize(qryText)
    
    #2. Remove duplicated tokens
    if (CLEAN_DUPLICATED_INPUT):
        uniqueTokens = []
        for j in tokenizedWords:
            if j not in uniqueTokens:
                uniqueTokens.append(j)
    else: #no input cleaning
        uniqueTokens = tokenizedWords
    
    #3. Remove stop words
    stopWords = set(stopwords.words("english"))
    filteredWords=[]
    for w in uniqueTokens:
        if w not in stopWords:
            filteredWords.append(w)
            
    #4. Stem words (create terms)
    ps = PorterStemmer()
    procQueryTextList = []
    for i in filteredWords:
        procQueryTextList.append(ps.stem(i))    

def dropUnpresentTermsInQuery():
    global queryTermsForRankSearch
    global procQueryTextList
    #remove terms which are not present in index for rank search later
    queryTermsForRankSearch = []
    for i in procQueryTextList:
        if indexReader.isTermPresent(i):
            queryTermsForRankSearch.append(i)
    #print(queryTermsForRankSearch)
    
def pullDocsWithQueryTerms():
    global queryTermsForRankSearch
    global docListForRankSearch
    queryTerms = [] #local copy of query terms for rank search
    for i in queryTermsForRankSearch:
        queryTerms.append(i)
    if (queryTerms == []):
        docListForRankSearch = []
    else:
        prevDocList = []
        docListForRankSearch = []
        term = ''
        while(queryTerms != []):
            term = queryTerms.pop()
            docListForRankSearch = indexReader.getDocListOfTerm(term)
            docListForRankSearch = operateOR(prevDocList, docListForRankSearch) #merge doc lists
            prevDocList = docListForRankSearch
    #print(docListForRankSearch)

def calcWtTF(term, docID):
    #formula (1 + log_base10_Tf)
    result = 0
    rawTf = indexReader.getTermFreqOfDoc(term, docID)    
    if rawTf == 0:        
        return result #avoid calculating log of 0 and its error
    else:
        result = 1 + math.log(rawTf, 10)
        return result    

def calcWtIDF(term):
    #formula log_base10_(NumOfDocs/df)
    result = 0
    totalDoc = indexReader.getNumOfTotalDocs()
    rawDf = indexReader.getDocFreqOfTerm(term) 
    if rawDf == 0: #avoid calculating log of 0 and its error
        return result
    else:
        result = math.log((totalDoc/rawDf), 10)
        return result    

def calcTfIdfScore(docId):# calculate tf.idf score of a document given query terms
    #Sum of  idf x wtf = log(N/df) x log(1+tf)
    global queryTermsForRankSearch    
    curTf = 0
    curIdf = 0
    score = 0    
    for i in queryTermsForRankSearch:        
        curTF = calcWtTF(i, docId)
        curIdf = calcWtIDF(i)        
        score = score + (curTF * curIdf)
    return score

def rankDocList(topK):
    global docListForRankSearch
    global docScoreListForRankSearch
    global topNum
    scoreDocDict = {} #<document, score>
    #1. Go through each document in doc list and calculate its tf.idf score
    for i in docListForRankSearch:
        scoreDocDict[i] = round(calcTfIdfScore(i), 3)
    #sort by scores
    docScoreListForRankSearch = {k: v for k, v in sorted(scoreDocDict.items(), key=lambda item: item[1], reverse = True)}
    
    if (topK > len(docScoreListForRankSearch)):
        topNum = len(docScoreListForRankSearch)
    else:
        topNum = topK    

def operateOR(posting1, posting2):
    p1 = 0
    p2 = 0
    result = []   
    
    while p1 < len(posting1) and p2 < len(posting2):
        if posting1[p1] == posting2[p2]:
            result.append(posting1[p1])
            p1 += 1
            p2 += 1
        elif posting1[p1] > posting2[p2]:
            result.append(posting2[p2])
            p2 += 1
        else:
            result.append(posting1[p1])
            p1 += 1
    while p1 < len(posting1):
        result.append(posting1[p1])
        p1 += 1
    while p2 < len(posting2):
        result.append(posting2[p2])
        p2 += 1
    return result
    
def outputQueryResult(descFileName, ttlTime):
    global rawQryText
    global docScoreListForRankSearch
    global topNum
    topN = topNum
    resultFile = open(descFileName, 'w', encoding ='utf-8')
    #update search time
    resultFile.write('Time taken for search (in seconds): '+ttlTime+ '\n')
    
    #update query result list (document list)
    resultFile.write('\n\n')    
    resultFile.write('For given query text: ' + rawQryText + '\n')    
    resultFile.write('Total number of document hits: ' + str(len(docListForRankSearch)) + '\n')    
    resultFile.write('Query Result is as follows for top ' +str(topNum) + ' documents\n')
    resultFile.write('Document_ID ' + 'Score ' + '\n')
    for k,v in docScoreListForRankSearch.items():
        if (topN > 0):
            resultFile.write(str(k) + '.txt' + ' ' + str(v) + '\n')
            topN -= 1
    resultFile.close()

def cleanPrevOutputFiles():
    flName2Del = ''
    #get list of files with 'out_' prefix
    obsFileList = glob.glob("out_*.txt")
    #print(obsFileList)
    while (len(obsFileList) > 0):
        flName2Del = obsFileList.pop(0)
        os.remove(flName2Del)

def cleanGlobalData():
    global procQueryTextList, queryTermsForRankSearch, docListForRankSearch, CLEAN_DUPLICATED_INPUT, AND_OPERATION_OPTIMIZATION
    del procQueryTextList, queryTermsForRankSearch, docListForRankSearch, CLEAN_DUPLICATED_INPUT, AND_OPERATION_OPTIMIZATION
