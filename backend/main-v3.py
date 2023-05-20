import glob
import logging
import os
import warnings
from typing import List

import faiss
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import uvicorn
from fastapi import FastAPI
from sentence_transformers import SentenceTransformer, CrossEncoder

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

print("start app")
warnings.filterwarnings("ignore", category=DeprecationWarning)
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-2-v2')
print("cross finished")


def load_arabic():
    # Load the SentenceTransformer and CrossEncoder models
    model_name = 'model/arabic/search/search-model'
    bi_encoder = SentenceTransformer(model_name)

    # Combine the CSV files efficiently
    csv_files = glob.glob('arabic.csv')
    data = pd.concat([pd.read_csv(csv, lineterminator='\n') for csv in csv_files], axis=0)

    # Clean the data
    data['Description'] = data['Description'].str[9:].str.strip()
    passages = (data['Course Title'] + ' - ' + data['Provider'] + ' - ' + data['Course_Link'] + data[
        'Subject']).values.tolist()
    print("load arabic success")
    return bi_encoder, passages


def load_spanish():
    # Load the SentenceTransformer and CrossEncoder models
    model_name = 'model/spanish/search/search-model'
    bi_encoder = SentenceTransformer(model_name)

    # Combine the CSV files efficiently
    csv_files = glob.glob('spanish.csv')
    data = pd.concat([pd.read_csv(csv, lineterminator='\n') for csv in csv_files], axis=0)

    # Clean the data
    data['Description'] = data['Description'].str[9:].str.strip()
    passages = (data['Course Title'] + ' - ' + data['Provider'] + ' - ' + data['Course_Link'] + data[
        'Subject']).values.tolist()
    return bi_encoder, passages


def load_german():
    # Load the SentenceTransformer and CrossEncoder models
    model_name = 'model/german/search/search-model'
    bi_encoder = SentenceTransformer(model_name)

    # Combine the CSV files efficiently
    csv_files = glob.glob('german.csv')
    data = pd.concat([pd.read_csv(csv, lineterminator='\n') for csv in csv_files], axis=0)

    # Clean the data
    data['Description'] = data['Description'].str[9:].str.strip()
    passages = (data['Course Title'] + ' - ' + data['Provider'] + ' - ' + data['Course_Link'] + data[
        'Subject']).values.tolist()
    return bi_encoder, passages


def load_english():
    # Load the SentenceTransformer and CrossEncoder models
    model_name = 'model/english/search/search-model'
    bi_encoder = SentenceTransformer(model_name)

    # Combine the CSV files efficiently
    csv_files = glob.glob('english.csv')
    data = pd.concat([pd.read_csv(csv, lineterminator='\n') for csv in csv_files], axis=0)

    # Clean the data
    data['Description'] = data['Description'].str[9:].str.strip()
    passages = (data['Course Title'] + ' - ' + data['Provider'] + ' - ' + data['Course_Link'] + data[
        'Subject']).values.tolist()
    return bi_encoder, passages


# en_bi_encoder, en_passages = load_english()
ar_bi_encoder, ar_passages = load_arabic()
# sp_bi_encoder, sp_passages = load_spanish()
# ge_bi_encoder, ge_passages = load_german()

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


def search(query: str, lang: str, skip: int = 0, limit: int = 10) -> List[str]:
    results = []

    if lang == 'arabic':
        index = faiss.read_index('arabic.index')
        query_vector = ar_bi_encoder.encode([query])
        top_k = index.search(query_vector, limit + skip)
        top_k_ids = np.unique(top_k[1].tolist()[0][skip:])

        cross_inp = [[query, ar_passages[hit]] for hit in top_k_ids]
        bi_encoder_op = [ar_passages[hit] for hit in top_k_ids]
        cross_scores = cross_encoder.predict(cross_inp)

        for hit in np.argsort(np.array(cross_scores))[::-1]:
            results.append(bi_encoder_op[hit].replace("\n", " "))
    elif lang == 'spanish':
        results.append("spanish")
        # index = faiss.read_index('spanish.index')
        # query_vector = sp_bi_encoder.encode([query])
        # top_k = index.search(query_vector, limit + skip)
        # top_k_ids = np.unique(top_k[1].tolist()[0][skip:])
        #
        # cross_inp = [[query, sp_passages[hit]] for hit in top_k_ids]
        # bi_encoder_op = [sp_passages[hit] for hit in top_k_ids]
        # cross_scores = cross_encoder.predict(cross_inp)
        #
        # for hit in np.argsort(np.array(cross_scores))[::-1]:
        #     results.append(bi_encoder_op[hit].replace("\n", " "))

    return results


@app.post("/search")
def perform_search(query: str = "", lang: str = "", skip: int = 0, limit: int = 10):
    # Call the search function and get the results
    results = search(query, lang, skip, limit)

    # Return the results as the API response
    return {"results": results}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
