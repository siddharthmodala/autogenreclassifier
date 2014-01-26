'''
Created on Nov 27, 2013

@author: Kartik Siddharth
'''

import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
raw = ''
synopsis_files = ['..\..\Data\\synopsis\HorrorOut.csv','..\..\Data\\synopsis\AdventureOut.csv','..\..\Data\\synopsis\CrimeOut.csv','..\..\Data\\synopsis\DocumentaryOut.csv','..\..\Data\\synopsis\ThrillerOut.csv' ]
for movie in synopsis_files:
    print movie
    f = open(movie)
    raw = raw  + f.read()


"""
0-title
1-genres
2-plot summary
"""
""" first term begins with " and last ends with "
genre seperated by comma within
"""

raw2 = raw.splitlines()
li = list()
for x in raw2:
    z= x.split(',"')
    li.append(z[2])

tokens = list()
tokenizer = nltk.RegexpTokenizer(r'\w+')

for x in li:
    tokens = tokens + tokenizer.tokenize(x)
    #print len(tokens)
print(len(tokens))
sw = stopwords.words('english')
content = [w for w in tokens if w.lower() not in sw]

stemmer = SnowballStemmer("english")

final_words = [stemmer.stem(w) for w in content ]
#print len(final_words)

fdist = nltk.FreqDist(final_words)

fdist1 = [(w,count) for w,count in fdist.items() if count > 8]


d= {}
output_file = open('..\..\Data\output.txt', 'w')
#vocab = fdist1.keys()
'''for word in fdist1:
    output_file.write( word + "\n")

'''

for word in fdist1:
    #print word
    d[word[0]]= word[1]
#     print d[word[0]]
    output_file.write( word[0]+"," + str(word[1]) + "\n")

print len(d)