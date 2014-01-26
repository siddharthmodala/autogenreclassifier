'''
Created on Nov 27, 2013

@author: Kartik Siddharth
'''


import nltk
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords

def intersect(a, b):
    return list(set(a) & set(b))

if __name__ == '__main__':
    raw = ''
    genre=['Horror','Adventure','Crime','Documentary','Thriller']

    i = 0;
    j = 0;
    for gen1 in range(0,4):

        gen1filename = ''.join(['..\..\Data\\',genre[gen1],'.txt'])
        for gen2 in range(gen1+1,5):

            fgen1 = open(gen1filename,"r")
            gen2filename = ''.join(['..\..\Data\\',genre[gen2],'.txt'])
            fgen2 = open(gen2filename,'r')
            listgen1 = list()

            for line in fgen1:
                term = line.split(",")
                listgen1.append(term[0])
            listgen2 = list()
            for line in fgen2:
                term = line.split(",")
                listgen2.append(term[0])

            common = intersect(listgen1,listgen2)

            print genre[gen1] + '->'+ genre[gen2] +':'+str(len(common))


