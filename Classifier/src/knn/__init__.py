'''
Author: siddharth & Karthik
'''

from sklearn import datasets
import numpy as np
from sklearn import svm
from sklearn import neighbors


import nltk,math,pickle,random
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import stopwords
from nltk.classify.naivebayes import NaiveBayesClassifier
from sklearn.preprocessing import LabelBinarizer

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

    print 'after removing stop words: ', len(filtered_tokens)

    stemmer = SnowballStemmer("english")

    stemmed_words = [stemmer.stem(w) for w in filtered_tokens]

    stem_words_freq = nltk.FreqDist(stemmed_words)

    print 'after freq dist: ', len(stem_words_freq)

    filtered_stem_words = [(w,count) for w,count in stem_words_freq.items() if count > 15 and not w.isdigit()]

    feature_list = '..\..\Data\\knnfeatureset\\feature_list.p'

    print 'length of filtered stem words: ',len(filtered_stem_words)

    pickle.dump(filtered_stem_words, open(feature_list,"wb"))

    print 'feature list saved at ', feature_list

    bow = {}
    for line in filtered_stem_words:
        bow[line[0]] = line[1]


    feature_dict = '..\..\Data\\knnfeatureset\\feature_dict.p'

    pickle.dump(bow,open(feature_dict,"wb"))

    print 'feature dict saved at ', feature_dict

    return [feature_dict,feature_list]


def filter_data(li):
    # processing of each movie
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    sw = stopwords.words('english')
    stemmer = SnowballStemmer("english")
    tokens = tokenizer.tokenize(li)
    content = [w for w in tokens if w.lower() not in sw]
    final_words = [stemmer.stem(w) for w in content ]
    freqDist = nltk.FreqDist(final_words)
    freqDist = {key: value for key, value in freqDist.items()
             if not key.isdigit()}
    return freqDist

def feature_data_set(synopsis_files,genre_set,feature_set_files,list_type):
    plot_tokens = nltk.defaultdict(int)

    bow = pickle.load(open(feature_set_files[0],"rb"))

    raw_synopsis=''

    for movie in synopsis_files:
        print movie
        f = open(movie)
        raw_synopsis = raw_synopsis  + f.read()

    movie_details = raw_synopsis.splitlines()
    print "No of Samples: ", len(movie_details)
    data_set=[]
    genre_data_set=[]
    movie_data_set=[]
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

        temp_genre=[]
        genre_list = z[1].split(",")
        for name in genre_set:
            if name in genre_list:
                temp_genre.append(genre_set.index(name))


        if len(temp_genre) == 0:
            print genre_list
        else:
            data_set.append(plot_tokens.values())
            genre_data_set.append(temp_genre)
            movie_data_set.append(z[0])



    loc = "..\..\Data\\knnfeatureset\\"

    if list_type:
        data_set_file = loc + "test_data_set.p"
        genre_set_file = loc + "test_genre_set.p"
        movie_set_file = loc + "test_moviename_set.p"
    else:
        data_set_file = loc + "data_set.p"
        genre_set_file = loc + "genre_set.p"
        movie_set_file = loc + "moviename_set.p"

    print "No of Samples: ", len(data_set)

    pickle.dump(data_set,open(data_set_file,"wb"))
    pickle.dump(genre_data_set,open(genre_set_file,"wb"))
    pickle.dump(movie_data_set,open(movie_set_file,"wb"))

    '''sample_data_file = loc + "sample_data_set.p"
    sample_genre_file = loc + "sample_genre_set.p"

    sample_data = data_set[:300]
    sample_genre = genre_data_set[:300]

    pickle.dump(sample_data, open(sample_data_file,"wb"))
    pickle.dump(sample_genre, open(sample_genre_file,"wb"))'''
    print 'data written into ', data_set_file , genre_set_file
    return [data_set_file,genre_set_file,movie_set_file]
    #return ["..\..\Data\\knnfeatureset\test_data_set.p","..\..\Data\\knnfeatureset\test_genre_set.p"]


if __name__ == '__main__':

    synopsis_files = ['..\..\Data\synopsis\HorrorOut.csv',
                      '..\..\Data\synopsis\AdventureOut.csv',
                      '..\..\Data\synopsis\CrimeOut.csv',
                      '..\..\Data\synopsis\DocumentaryOut.csv',
                      '..\..\Data\synopsis\ThrillerOut.csv' ]
    genre_set = ["Thriller",
                 "Horror",
                 "Documentary",
                 "Crime",
                 "Adventure"]
    loc = "..\..\Data\\knnfeatureset\\"
    knn_file = loc + "knn"

    feature_set_files = ['..\..\Data\\knnfeatureset\\feature_dict.p','..\..\Data\\knnfeatureset\\feature_list.p',]
    #feature_set_files = feature_extractor(synopsis_files)


    data_set_file = ["..\..\Data\\knnfeatureset\data_set.p",
                     "..\..\Data\\knnfeatureset\genre_set.p",
                     "..\..\Data\\knnfeatureset\moviename_set.p"]

    #data_set_file = feature_data_set(synopsis_files, genre_set, feature_set_files,False)

    test_set_file = ["..\..\Data\\knnfeatureset\\test_data_set.p",
                     "..\..\Data\\knnfeatureset\\test_genre_set.p",
                     "..\..\Data\\knnfeatureset\\test_moviename_set.p"]
    #test_set_file = feature_data_set(['..\..\Data\synopsis\TestSamplesOut.csv'],genre_set,feature_set_files,True)

    test_data_set = pickle.load(open(test_set_file[0],"rb"))
    test_genre_set= pickle.load(open(test_set_file[1],"rb"))
    test_moviename_set = pickle.load(open(test_set_file[2],"rb"))


    training_data_set = pickle.load(open(data_set_file[0],"rb"))
    training_genre_set = pickle.load(open(data_set_file[1],"rb"))
    training_moviename_set = pickle.load(open(data_set_file[2],"rb"))



    '''data = []
    i = 0
    for d in data_set:
        data.append((d,genre_set[i]))
        i+=1
    random.shuffle(data)
    test_data_set, test_genre_set = [[d[i] for d in data] for i in (0,1)]'''


    lb= LabelBinarizer()
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=15,algorithm='kd_tree',weights='distance')
    knn_clf.fit(training_data_set, lb.fit_transform(training_genre_set))

    pickle.dump(knn_clf,open(knn_file,"wb"))

    #knn_clf = pickle.load(open(knn_file,"rb"))

    i = 0
    '''for test in test_data_set:
        result = knn_clf.predict(test)
        resultx = lb.inverse_transform(result)
        #print test_moviename_set[i],resultx,test_genre_set[i]
        print test_moviename_set[i],[genre_set[z] for z in resultx[0]],[genre_set[z] for z in test_genre_set[i]]
        i+=1'''

    result = knn_clf.kneighbors(test_data_set[3],return_distance=False)
    print 'Test Set INformation: ',test_moviename_set[3],[genre_set[z] for z in test_genre_set[3]]
    for x in result:
        genre_count = [0,0,0,0,0]
        i+=1
        for y in x:
            neighbour = training_genre_set[y]
            final_genre = []
            print training_moviename_set[y],[genre_set[z] for z in neighbour]
            '''for genre in neighbour:
                genre_count[genre] += 1
            for j in range(5):
            if genre_count[j] > 1:
                final_genre.append(j)
        print test_moviename_set[i],genre_count, [genre_set[z] for z in final_genre],[genre_set[z] for z in test_genre_set[i]]'''

    test_genre_set = lb.transform(test_genre_set)
    '''for i in [3,6,9,12,15,18,21,24,27,30]:
        for j in ['kd_tree']:
            for k in ['uniform','distance']:
                knn_clf = neighbors.KNeighborsClassifier(n_neighbors=i,algorithm=j,weights=k)
                knn_clf.fit(training_data_set, LabelBinarizer().fit_transform(training_genre_set))
                print i,j,k,knn_clf.score(test_data_set,test_genre_set)'''



    print 'done!'


    '''result = knn_clf.kneighbors(test_data_set,return_distance=False)
    for x in result:
        genre_count = [0,0,0,0,0]
        i+=1
        for y in x:
            neighbour = training_genre_set[y]
            final_genre = []
            for genre in neighbour:
                genre_count[genre] += 1
        for j in range(5):
            if genre_count[j] > 1:
                final_genre.append(j)
        print test_moviename_set[i],genre_count, [genre_set[z] for z in final_genre],[genre_set[z] for z in test_genre_set[i]]'''
    '''
    iris = datasets.load_iris()
    svm_clf = svm.LinearSVC()
    svm_clf.fit(iris.data,iris.target)
    test = [ 5.0,  3.6,  1.3,  0.25]
    result = svm_clf.predict(test)

    print 'Using svm: ',iris.target_names[result[0]]

    knn_clf = neighbors.KNeighborsClassifier()
    knn_clf.fit(iris.data,iris.target)
    result = knn_clf.predict(test)

    print 'knn result :', iris.target_names[result[0]]'''
