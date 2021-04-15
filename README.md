# rankSearcher
This program performs rank search on an inverted index

==========DESCRIPTION=============

This python program (rankSearcher) implements the search component of an information retrieval system.

Input to the program:
1. Search query 
2. Path of the inverted index file (E.g C:\rankSearcher\sampleInput\out_invertedIndexForRanking.txt)

Output of the program: A text file containing search query results, out_queryResult.txt.
Note: An example output is available in the package as "sampleOutput\out_queryResult.txt" for use.

==========ENVIRONMENT SET-UP=============

1. Download this package (rankSearcher) from GitHub (easy as a zip file). Save and unzip it in a preferred directory in your machine (e.g "C:\rankSearcher") 
2. Note: An example input inverted index is available in the package as "sampleInput\out_invertedIndexForRanking.zip" for use.
3. Install Python 3.8.0 or above from https://www.python.org/downloads/.
4. Install Natural Language Toolkit from https://www.nltk.org/ Note: A reference tutorial of NLTK can be found in this YouTube video. https://www.youtube.com/watch?v=FLZvOKSCkxY

==========HOW TO RUN THE PROGRAM=============

1. Launch the command line. E.g For Windows, press Window Key + R on keyboard and then type 'cmd'
2. Change current directory in the command line to the path of this program. E.g for Windows "cd C:\rankSearcher"
3. Get the path of python installation on your machine. E.g For Windows, "C:\Users\YourUserId\AppData\Local\Programs\Python\Python38-32"
4. Run this python program. E.g For Windows, "C:\Users\YourUserId\AppData\Local\Programs\Python\Python38-32\python rankSearcherMain.py"
5. Find the program output file which contains the query results and statistics under the same path as the program. E.g "C:\rankSearcher\out_queryResult.txt"
