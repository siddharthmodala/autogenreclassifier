'''
Created on Nov 30, 2013
@author: Kartik and Siddharth
'''

import nltk,math
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.classify.naivebayes import NaiveBayesClassifier
import random

bow = {}
genre_set={"Thriller","Horror","Documentary","Crime","Adventure"}
plot_tokens = nltk.defaultdict(int)
f= open("../output.txt")

for line in f:
    split_word = line.split(",")
    bow[split_word[0]] = split_word[1]
        #print split_word[0]

    #reading all synopsis_files
raw=''
synopsis_files = ['.\Data\HorrorOut.csv','.\Data\AdventureOut.csv','.\Data\CrimeOut.csv','.\Data\DocumentaryOut.csv','.\Data\ThrillerOut.csv' ]
for movie in synopsis_files:
    print movie
    f = open(movie)
    raw = raw  + f.read()

raw2 = raw.splitlines()

    # processing of each movie
tokenizer = nltk.RegexpTokenizer(r'\w+')
sw = stopwords.words('english')
stemmer = SnowballStemmer("english")
feature_set=[]

freq_count = {}
for w in bow:
    freq_count[w] = 0

for line in raw2:
    plot_tokens = {}
    for w in bow:
        plot_tokens[w] = 0

    z= line.split('","')
    li = z[2]
    tokens = tokenizer.tokenize(li)
    content = [w for w in tokens if w.lower() not in sw]
    final_words = [stemmer.stem(w) for w in content ]
    fdist = nltk.FreqDist(final_words)
    fdist1 = [(w,count) for w,count in fdist.items() if w in bow]
    #print fdist1

    for tag,c in fdist1:
        plot_tokens[tag] = plot_tokens[tag] + c
        if c != 0:
            freq_count[tag] +=1


    genre_list = z[1].split(",")
    for name in genre_list:
        if name in genre_set:
            feature_set.append((plot_tokens,name))
            #print feature_set

        #plot_tokens.clear()

    #modifying frequency based on tf-idf

for f in feature_set:
        #x = f[0]
        #print f
    for tag in f[0]:
        f[0][tag] =  f[0][tag] * (math.log(len(raw2)/(1+freq_count[tag])))


    '''
     writing feature set into a file.
    '''
output_file = open('../feature_set.txt', 'w')
for line in feature_set:
    output_file.write(str(line) + "\n")
    break

features =[(f,g) for f,g in feature_set]
for genre in genre_set:
    print "genre =" + genre
    features =[(f,g) for f,g in feature_set]
    for f in feature_set:
        if genre != f[1]:
            #print f[1]
            features.remove(f)
            features.append((f[0],"f"))

    random.shuffle(features)
    data_set,test_set = features[50:], features[:50]
    classifier = nltk.NaiveBayesClassifier.train(data_set)

    print nltk.classify.accuracy(classifier,test_set)
    classifier.show_most_informative_features(10)
    #print classifier.batch_classify(test_set)
    '''
    print nltk.classify.accuracy(c, test_set)
    c.show_most_informative_features(50)
    '''

        #print plot_tokens.items()
        #break

