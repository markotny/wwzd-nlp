from glob import glob
import matplotlib.pyplot as plt
import fileinput
import collections
import re
from gensim.models import KeyedVectors, WordEmbeddingSimilarityIndex, TfidfModel
from gensim.similarities import MatrixSimilarity, SparseTermSimilarityMatrix, SoftCosineSimilarity
from gensim.corpora import Dictionary
import numpy as np
from datetime import datetime


def now():
    return datetime.now().time()

partie = [
    'KO',
    'Konfederacja',
    'Lewica',
    'niez',
    'PiS',
    'PSL-Kukiz15'
]

stopwords = open("polish.stopwords.txt", encoding='utf-8').read().splitlines()

documents = []

for p in partie:
    wypowiedzi_partii = ''
    for posl in glob('partie\\' + p + '/*'):
        wypowiedzi = glob(posl + '/*')
        with fileinput.input(wypowiedzi, openhook=fileinput.hook_encoded("windows-1250")) as wyp:
            for line in wyp:
                wypowiedzi_partii += line

    wypowiedzi_partii = wypowiedzi_partii.replace('\n', ' ')
    wypowiedzi_partii = re.sub('[,.:;!?()]', '', wypowiedzi_partii)

    documents.append(
        [word for word in wypowiedzi_partii.lower().split() if word not in stopwords])

print(now(), 'loaded speech data')
np.seterr(divide='ignore', invalid='ignore')

dictionary = Dictionary(documents)
tfidf = TfidfModel(dictionary=dictionary)
wv = KeyedVectors.load("word2vec_100_3_polish.bin")

print(now(), 'loaded model')

similarity_index = WordEmbeddingSimilarityIndex(wv)
similarity_matrix = SparseTermSimilarityMatrix(
    similarity_index, dictionary)
print(now(), 'created similarity matrix')

index = SoftCosineSimilarity([dictionary.doc2bow(
    document) for document in documents], similarity_matrix)

print(now(), 'created index')
# index.save('soft_cosine.index')

# index = SoftCosineSimilarity.load('soft_cosine.index')
while True:
    try:
        query = input("Query: ").lower().split()
        # query = tfidf[dictionary.doc2bow(query)]
        similarities = index[dictionary.doc2bow(query)]
        result_list = [partie[i] for i in [a[0] for a in similarities]]
        score_list = [a[1] for a in similarities]
        results = [' '.join(each) for each in result_list]
        for score, result in zip(score_list, results):
            print('{:.3f} : {}'.format(score, result))
    except Exception as e:
        print(e)
