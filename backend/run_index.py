# -*- coding: utf-8 -*-
"""run-index.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Cb7fBzcDMetoBATwmxucgMu-7YM0cqub
"""

import glob
import os
import time
import warnings

import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import faiss
from sentence_transformers import SentenceTransformer, CrossEncoder

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

warnings.filterwarnings("ignore", category=DeprecationWarning)

# Commented out IPython magic to ensure Python compatibility.
# %cd /content/drive/My Drive/research

for ix, csv in enumerate(glob.glob('arabic.csv')):
    if ix == 0:
        data = pd.read_csv(csv, lineterminator='\n')
    else:
        temp = pd.read_csv(csv, lineterminator='\n')
        data = pd.concat([data, temp], axis=0).reset_index(drop=True)


def search(query, index, lang):
    print("Searching query:", query)
    print("Searching language:", lang)

    for ix, csv in enumerate(glob.glob('arabic.csv')):
        if ix == 0:
            data = pd.read_csv(csv, lineterminator='\n')
        else:
            temp = pd.read_csv(csv, lineterminator='\n')
            data = pd.concat([data, temp], axis=0).reset_index(drop=True)

    data = data.dropna(subset=['Course Title', 'Description']).reset_index(drop=True)
    data['Description'] = data['Description'].apply(lambda x: x.replace('\n', ' ')[9:].strip())

    # We use the Bi-Encoder to encode all passages, so that we can use it with sematic search
    model_name = 'model/arabic/search/search-model'
    bi_encoder = SentenceTransformer(model_name)
    top_k = 100  # Number of passages we want to retrieve with the bi-encoder

    # The bi-encoder will retrieve 100 documents. We use a cross-encoder, to re-rank the results list to improve the quality
    cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-2-v2')

    # As dataset, we use Simple English Wikipedia. Compared to the full English wikipedia, it has only
    # Prepare the result: [Course Title] + [Provider] + [Institute] + [Link]
    passages = (data['Course Title'] + ' - ' + data['Provider']).values.tolist()

    # If you like, you can also limit the number of passages you want to use
    print("Passages:", len(passages))

    ##### Sematic Search #####
    # Encode the query using the bi-encoder and find potentially relevant passages
    t = time.time()
    query_vector = bi_encoder.encode([query])
    top_k = index.search(query_vector, 10)
    top_k_ids = top_k[1].tolist()[0]
    top_k_ids = list(np.unique(top_k_ids))
    print('>>>> Bi-Encoder Results in Total Time: {}'.format(time.time() - t))

    ##### Re-Ranking #####
    # Now, score all retrieved passages with the cross_encoder
    t = time.time()
    cross_inp = [[query, passages[hit]] for hit in top_k_ids]
    bienc_op = [passages[hit] for hit in top_k_ids]
    cross_scores = cross_encoder.predict(cross_inp)
    print('>>>> Cross-Encoder Results in Total Time: {}'.format(time.time() - t))

    # Output of top-10 hits from bi-encoder
    print("\n-------------------------\n")
    print("Top-10 Bi-Encoder Retrieval hits")
    for result in bienc_op:
        print("\t{}".format(result.replace("\n", " ")))

    # Output of top-10 hits from re-ranker
    print("\n-------------------------\n")
    print("Top-10 Cross-Encoder Re-ranker hits")
    for hit in np.argsort(np.array(cross_scores))[::-1]:
        print("\t{}".format(bienc_op[hit].replace("\n", " ")))


query = 'كيف تتعلم لغة ++ C؟'
index = faiss.read_index('arabic.index')
search(query, index, 'arabic')
