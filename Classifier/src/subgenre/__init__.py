'''
Authors: Siddharth & Karthik
'''

'''
Created on Nov 27, 2013

@author: Kartik Siddharth
'''

import nltk,math,pickle,random
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.classify.naivebayes import NaiveBayesClassifier


'''
Function to create feature set by using all the synopsis from all synopsis_files
'''
def feature_extractor(synopsis_files):
    raw_synopsis = ''
    for movie in synopsis_files:
        print movie
        f = open(movie)
        raw_synopsis = raw_synopsis  + f.read()


    """
    0-title
    1-genres
    2-plot summary-first term begins with " and last ends with "
    genre seperated by comma within
    """

    movie_details = raw_synopsis.splitlines()
    movie_synopsis = list()
    for x in movie_details:
        z= x.split(',"')
        movie_synopsis.append(z[2])

    synopsis_tokens = list()

    tokenizer = nltk.RegexpTokenizer(r'\w+')

    for x in movie_synopsis:
        synopsis_tokens = synopsis_tokens + tokenizer.tokenize(x)

    print 'length of synopsis_tokens ',len(synopsis_tokens)

    sw = stopwords.words('english')

    filtered_tokens = [w for w in synopsis_tokens if w.lower() not in sw]

    stemmer = SnowballStemmer("english")

    stemmed_words = [stemmer.stem(w) for w in filtered_tokens ]

    stem_words_freq = nltk.FreqDist(stemmed_words)

    filtered_stem_words = [(w,count) for w,count in stem_words_freq.items() if count > 8 and not w.isdigit()]

    print 'filtered stem words length: ',len(filtered_stem_words)

    '''feature_list = '..\..\Data\\subgenre\\feature_list.p'

    pickle.dump(filtered_stem_words, open(feature_list,"wb"))



    print 'feature list saved at ', feature_list'''

    d= {}
    output_file = open('..\..\Data\\subgenre\\subgenre.txt', 'w')
    for word in filtered_stem_words:
        d[word[0]]= word[1]
        output_file.write( word[0]+"," + str(word[1]) + "\n")

    '''bow = {}
    for line in filtered_stem_words:
        bow[line[0]] = line[1]


    feature_dict = '..\..\Data\\subgenre\\feature_dict.p'

    pickle.dump(bow,open(feature_dict,"wb"))

    print 'feature dict saved at ', feature_dict'''


def filter_data(li):
    # processing of each movie
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    sw = stopwords.words('english')
    stemmer = SnowballStemmer("english")
    tokens = tokenizer.tokenize(li)
    content = [w for w in tokens if w.lower() not in sw]
    final_words = [stemmer.stem(w) for w in content ]
    return nltk.FreqDist(final_words)

def feature_data_set(synopsis_files,genre_set,feature_set_files):
    plot_tokens = nltk.defaultdict(int)

    bow = pickle.load(open(feature_set_files[0],"rb"))

    raw_synopsis=''

    for movie in synopsis_files:
        print movie
        f = open(movie)
        raw_synopsis = raw_synopsis  + f.read()

    movie_details = raw_synopsis.splitlines()

    data_set=[]

    freq_count = {}
    for w in bow:
        freq_count[w] = 0

    for line in movie_details:
        plot_tokens = {}
        for w in bow:
            plot_tokens[w] = 0

        z= line.split('","')
        synopsis = z[2]
        fdist = filter_data(synopsis)
        fdist1 = [(w,count) for w,count in fdist.items() if w in bow]


        for tag,c in fdist1:
            plot_tokens[tag] = plot_tokens[tag] + c
            if c != 0:
                freq_count[tag] +=1


        genre_list = z[1].split(",")
        for name in genre_list:
            if name in genre_set:
                data_set.append((plot_tokens,name))


    #modifying frequency based on tf-idf
    for f in data_set:
        for tag in f[0]:
            f[0][tag] =  f[0][tag] * (math.log(len(movie_details)/(1+freq_count[tag])))



    data_set_file = "..\..\Data\\featureset\data_set.p"
    pickle.dump(data_set,open(data_set_file,"wb"))
    print 'data set written into ', data_set_file
    return data_set_file


if __name__ == '__main__':
    synopsis_files = ['..\..\Data\synopsis\\warOut.csv',
                      '..\..\Data\synopsis\\scifiOut.csv',
                      '..\..\Data\synopsis\\fantasyOut.csv'
                 ]
    genre_set = {"Thriller",
                 "Horror",
                 "Documentary",
                 "Crime",
                 "Adventure"}

    #feature_set_files = ['..\..\Data\\subgenre\\fantasy_dict.p','..\..\Data\\subgenre\\fantasy_list.p']
    feature_set_files = feature_extractor(synopsis_files)
    #data_set_file = "..\..\Data\\featureset\data_set.p"
    #data_set_file = feature_data_set(synopsis_files, genre_set, feature_set_files)
    print 'done!'