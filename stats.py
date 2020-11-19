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
    glob('partie\\KO/*'),
    glob('partie\\Konfederacja/*'),
    glob('partie\\Lewica/*'),
    glob('partie\\niez/*'),
    glob('partie\\PiS/*'),
    glob('partie\\PSL-Kukiz15/*')
]

stopwords = open("polish.stopwords.txt", encoding='utf-8').read().splitlines()

documents = []

for p in partie:
    partia = p[0].split('\\')[1]
    wypowiedzi_partii = ''
    for posl in p:
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
model = KeyedVectors.load("word2vec_100_3_polish.bin")

print(now(), 'loaded model')

similarity_index = WordEmbeddingSimilarityIndex(model)
similarity_matrix = SparseTermSimilarityMatrix(
    similarity_index, dictionary, tfidf)
print(now(), 'created similarity matrix')

index = SoftCosineSimilarity(tfidf[[dictionary.doc2bow(
    document) for document in documents]], similarity_matrix)
print(now(), 'created index')

while True:
    try:
        query = input("Query: ").lower().split()
        query = tfidf[dictionary.doc2bow(query)]
        similarities = index[query]
        print(now, similarities)
    except Exception as e:
        print(e)
