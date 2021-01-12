from glob import glob
import matplotlib.pyplot as plt
import fileinput
import collections
import re
from gensim.models import KeyedVectors, WordEmbeddingSimilarityIndex, TfidfModel
from gensim.similarities import MatrixSimilarity, SparseTermSimilarityMatrix, SoftCosineSimilarity
from gensim.corpora import Dictionary
import numpy as np
np.seterr(divide='ignore', invalid='ignore')

def get_stopwords():
    return open("polish.stopwords.txt", encoding='utf-8').read().splitlines()

def load_parties(stopwords, documents, tags, partie):
    for p in partie:
        wypowiedzi_partii = ''
        for posl in glob('partie/' + p + '/*'):
            wypowiedzi = glob(posl + '/*')

            for wypowiedz in wypowiedzi:
                tags.append(wypowiedz[len('partie/'):-len('.txt')].replace('\\',': '))
                wyp_text = ''
                with fileinput.input(wypowiedz, openhook=fileinput.hook_encoded("windows-1250")) as wyp:
                    for line in wyp:
                        wyp_text += line
                
                wyp_text = wyp_text.replace('\n', ' ')
                wyp_text = re.sub('[,.:;!?()]', '', wyp_text)
                documents.append(
                    [word for word in wyp_text.lower().split() if word not in stopwords])

def prepare_index(dictionary, wv, tfidf, documents):
    similarity_index = WordEmbeddingSimilarityIndex(wv)
    similarity_matrix = SparseTermSimilarityMatrix(similarity_index, dictionary, tfidf)

    index = SoftCosineSimilarity(tfidf[[dictionary.doc2bow(document) for document in documents]], similarity_matrix)

    index.save('soft_cosine.index')

    return SoftCosineSimilarity.load('soft_cosine.index')

def recognize(query):
    partie = [
        'KO',
        'Konfederacja',
        'Lewica',
        'niez',
        'PiS',
        'PSL-Kukiz15'
    ]

    documents = []
    tags = []

    stopwords = get_stopwords()

    load_parties(stopwords, documents, tags, partie)

    wv = KeyedVectors.load("word2vec_100_3_polish.bin")
    dictionary = Dictionary(documents)
    tfidf = TfidfModel(dictionary=dictionary)

    index = prepare_index(dictionary, wv, tfidf, documents)

    try:
        # query = "".lower().split()
        bow = dictionary.doc2bow(query, return_missing=True)
        query = tfidf[bow[0]]
        print("Słowa nierozpoznane: ", bow[1])
        similarities = index[query]
        for score, wyp in sorted(zip(similarities, tags), key= lambda t: t[0], reverse=True)[:20]:
            print('{:.3f} : {}'.format(score, wyp))
    except Exception as e:
        print(e)