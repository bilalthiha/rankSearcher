import sys
import queryProcessor
import indexReader
from pathlib import Path
import time

#module global
queryText = ''
invIdxFile = ''
outFileName = 'out_queryResult.txt'
startSearchTime = 0
endSearchTime=0
totalSearchTime=0

#=================== Functions =======================
def cleanGlobalData():
    global queryText, invIdxFile, outFileName, startSearchTime, endSearchTime, totalSearchTime
    del queryText, invIdxFile, outFileName, startSearchTime, endSearchTime, totalSearchTime
#=================== End of Functions =======================

print('\nPlease key in your query:')
queryText = input()

print('\nPlease key in the path to the inverted index file.')
print('E.g .\sampleInput\out_invertedIndexForRanking.txt')
invIdxFile = input()

#0. Initialization
queryProcessor.cleanPrevOutputFiles()

#1. Process query text
queryProcessor.processQueryText(queryText)

#2. Read inverted index file (into local dictionary)
# Get start time for search
startSearchTime = time.time()
indexReader.readInvIdxFile(invIdxFile)

#3. Drop unpresent query terms for ranked search. No point to calculate tf.idf for terms not present in any doc at all
queryProcessor.dropUnpresentTermsInQuery()

#4. List all document ids which contain any of query terms. This is to avoid calculating tf.idf score for docs without any query terms
queryProcessor.pullDocsWithQueryTerms()

#5. Calculate weighted tf and idf score of each doc and rank top 20 doc list
queryProcessor.rankDocList(20)

endSearchTime = time.time()
totalSearchTime = endSearchTime-startSearchTime

#6. Store search results in text file
queryProcessor.outputQueryResult(outFileName, str(totalSearchTime))
print('\nPlease find the query results in\n' + outFileName + ' under the directory\n' + str(Path.cwd()))

# #5. DeInit Program
indexReader.cleanGlobalData()
queryProcessor.cleanGlobalData()
cleanGlobalData()

