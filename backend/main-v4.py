import glob
import logging
import os
import warnings
from typing import List

import faiss
import numpy as np
import pandas as pd
import json
import uvicorn
from fastapi import FastAPI, Response, HTTPException
from sentence_transformers import SentenceTransformer, CrossEncoder

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

print("start app")
warnings.filterwarnings("ignore", category=DeprecationWarning)
cross_encoder = CrossEncoder('cross-encoder/ms-marco-MiniLM-L-2-v2')
print("cross finished")

languages = {
    'arabic': {
        'model_name': 'model/arabic/search/search-model',
        'csv_files': ['arabic.csv'],
        'passages': None,
        'bi_encoder': None
    },
    'spanish': {
        'model_name': 'model/spanish/search/search-model',
        'csv_files': ['spanish.csv'],
        'passages': None,
        'bi_encoder': None
    },
    'german': {
        'model_name': 'model/german/search/search-model',
        'csv_files': ['german.csv'],
        'passages': None,
        'bi_encoder': None
    },
    'english': {
        'model_name': 'model/english/search/search-model',
        'csv_files': ['english.csv'],
        'passages': None,
        'bi_encoder': None
    }
}

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    logger = logging.getLogger("uvicorn.access")
    handler = logging.StreamHandler()
    handler.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))
    logger.addHandler(handler)


def load_data(language):
    model_name = languages[language]['model_name']
    csv_files = languages[language]['csv_files']
    passages = []

    if languages[language]['passages'] is None:
        bi_encoder = SentenceTransformer(model_name)
        for csv_file in csv_files:
            data = pd.read_csv(csv_file, lineterminator='\n')
            data['Description'] = data['Description'].str[9:].str.strip()
            data['Instructor'] = data['Instructor'].map(lambda x: x.lstrip('Taught by\n').rstrip('aAbBcC'))
            passages.extend((data['Course Title'] + ' - ' + data['Description'] + ' - ' + data['Instructor'] + ' - ' +
                             data['Subject'] + ' - ' + data['Provider'] + ' - ' + data['Course_Link']).values.tolist())

        languages[language]['passages'] = passages
        languages[language]['bi_encoder'] = bi_encoder

    return languages[language]['bi_encoder'], languages[language]['passages']


def search(query: str, lang: str, skip: int = 0, limit: int = 10):
    res = []
    if lang in languages:
        bi_encoder, passages = load_data(lang)
        index = faiss.read_index(f'{lang}.index')
        query_vector = bi_encoder.encode([query])
        top_k = index.search(query_vector, limit + skip)
        top_k_ids = top_k[1].tolist()[0]
        top_k_ids = list(np.unique(top_k_ids))
        top_k_ids = [int(id) for id in top_k_ids]  # Convert int64 IDs to integers

        # Re-Ranking
        cross_inp = [[query, passages[hit]] for hit in top_k_ids]
        bienc_op = [passages[hit] for hit in top_k_ids]
        cross_scores = cross_encoder.predict(cross_inp)

        # Top-10 Cross-Encoder Re-ranker hits
        for hit in np.argsort(np.array(cross_scores))[::-1]:
            res = bienc_op[hit].split(" - ")
            res.insert(0, int(top_k_ids[hit]))

    return res


def construct_responses(res):
    results = []
    result = {
        "id": res[0],
        "title": res[1],
        "instructor": res[3],
        "provider": res[5],
        "url": res[6]
    }
    results.append(result)
    return json.dumps(results, ensure_ascii=False)


def construct_response_by_id(res):
    results = []
    result = {
        "id": res[0],
        "title": res[1],
        "description": res[2],
        "instructor": res[3],
        "subject": res[4],
        "provider": res[5],
        "url": res[6]
    }
    results.append(result)
    return results


@app.get("/")
async def root():
    return {"message": "Welcome to MoocMaven the first unified MOOCs Semantic Search platform!"}


@app.post("/search", response_class=Response)
def perform_search(query: str = "", lang: str = "", skip: int = 0, limit: int = 10):
    res = search(query, lang, skip, limit)
    results = construct_responses(res)
    return results


@app.get('/results/{result_id}', response_class=Response)
def get_result_by_id(result_id: int):
    # Call your search function and retrieve the result by ID
    res = search(query='', lang='', skip=0, limit=10)  # Replace with your actual implementation
    results = construct_response_by_id(res)

    for result in results:
        if result['id'] == result_id:
            return json.dumps(results, ensure_ascii=False)

    raise HTTPException(status_code=404, detail="Result not found")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
