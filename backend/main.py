import json
import logging
import os
import random
import secrets
import warnings
from datetime import datetime, timedelta
from typing import List

import faiss
import jwt
import numpy as np
import pandas as pd
import redis
import uvicorn
from fastapi import Depends
from fastapi import FastAPI, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer, CrossEncoder

from redis_config import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

# from fastapi_limiter import FastAPILimiter
# from fastapi_limiter.depends import RateLimiter
# from fastapi_limiter.limits import Rate, Minutes

os.environ['KMP_DUPLICATE_LIB_OK'] = 'True'

app = FastAPI(
    title='MOOCMaven API',
    description='Unified MOOCs Open Platform API'
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create a Redis client
redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
CACHE_PREFIX = "search_results:"

# Define a secret key for JWT encoding/decoding
SECRET_KEY = secrets.token_urlsafe(32)

# Define token expiration time
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User data (replace with your own user database or ORM)
users = [
    {
        "username": "user1",
        "password": "$2b$12$54e2ETBEs55x29rBPrXWJurwapWxsFrT7ZXz9OAaZfFZg5fWCoSVe",  # Hashed password: "password1"
    },
    {
        "username": "user2",
        "password": "$2b$12$DR2.ZKp2SlLw/o3LGAb6j.XwUN.ykQ5vdv50m7vjcppwC3OU2wh.C",  # Hashed password: "password2"
    },
]


class SearchResult(BaseModel):
    id: int
    title: str
    description: str
    instructor: str
    subject: str
    provider: str
    url: str


class SearchResponse(BaseModel):
    results: List[SearchResult]
    total_results: int


# Function to verify password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# Function to get user by username
def get_user(username):
    for user in users:
        if user["username"] == username:
            return user


# Function to authenticate user
def authenticate_user(username, password):
    user = get_user(username)
    if not user or not verify_password(password, user["password"]):
        return False
    return user


# Function to create access token
def create_access_token(data, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
    return encoded_jwt


# OAuth2 scheme for authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


class SearchRequest(BaseModel):
    query: str
    lang: str
    skip: int = 0
    limit: int = 10


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
    },
    'indonesian': {
        'model_name': 'model/indonesian/search/search-model',
        'csv_files': ['indonesian.csv'],
        'passages': None,
        'bi_encoder': None
    },
    'chinese': {
        'model_name': 'model/chinese/search/search-model',
        'csv_files': ['chinese.csv'],
        'passages': None,
        'bi_encoder': None
    },
    'french': {
        'model_name': 'model/french/search/search-model',
        'csv_files': ['french.csv'],
        'passages': None,
        'bi_encoder': None
    },
    'portuguese': {
        'model_name': 'model/portuguese/search/search-model',
        'csv_files': ['portuguese.csv'],
        'passages': None,
        'bi_encoder': None
    }
}


# rate_limit = Rate(limit=2, period=Minutes(1))
# limiter = RateLimiter(rate_limit)
#
# app.add_middleware(
#     RateLimiter,
#     app=limiter,
#     on_failure=lambda request, _: JSONResponse(
#         status_code=HTTP_429_TOO_MANY_REQUESTS,
#         content={"message": "Too many requests"}
#     )
# )


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
            csv_path = os.path.join("model", language, csv_file)
            data = pd.read_csv(csv_path, lineterminator='\n')
            data['Description'] = data['Description'].str[9:].str.strip()
            data['Instructor'] = data['Instructor'].map(lambda x: x.lstrip('Taught by\n').rstrip('aAbBcC'))
            passages.extend((data['Course Title'] + ' - ' + data['Description'] + ' - ' + data['Instructor'] + ' - ' +
                             data['Subject'] + ' - ' + data['Provider'] + ' - ' + data['Course_Link']).values.tolist())

        languages[language]['passages'] = passages
        languages[language]['bi_encoder'] = bi_encoder

    return languages[language]['bi_encoder'], languages[language]['passages']


def search(query: str, lang: str, skip: int = 0, limit: int = 10):
    cache_key = f"{CACHE_PREFIX}{query}-{lang}-{skip}-{limit}"

    if redis_client.exists(cache_key):
        # Retrieve the cached results and return them
        cached_results = redis_client.get(cache_key)
        return json.loads(cached_results)

    results = []
    if lang in languages:
        bi_encoder, passages = load_data(lang)
        index = faiss.read_index(os.path.join("model", lang, f'{lang}.index'))
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
            result = bienc_op[hit].split(" - ")
            result.insert(0, int(top_k_ids[hit]))
            results.append(result)

        # Cache the results in Redis
        redis_client.set(cache_key, json.dumps(results))

    return results


def construct_responses(res):
    results = []
    for r in res:
        result = {
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "instructor": r[3],
            "subject": r[4],
            "provider": r[5],
            "url": r[6]
        }
        results.append(result)
    return json.dumps(results, ensure_ascii=False)


def construct_response_by_id(res):
    results = []
    for r in res:
        result = {
            "id": r[0],
            "title": r[1],
            "description": r[2],
            "instructor": r[3],
            "subject": r[4],
            "provider": r[5],
            "url": r[6]
        }
        results.append(result)
    return results


@app.get("/")
async def root():
    return {"message": "Welcome to MoocMaven the first unified MOOCs Semantic Search platform!"}


@app.post("/search", response_model=SearchResponse)
def perform_search(request: SearchRequest):
    res = search(request.query, request.lang, request.skip, request.limit)
    total_results = len(res)
    # Parse the JSON-encoded results string into a list of dictionaries
    results = json.loads(construct_responses(res))
    # Construct the response
    response_data = {
        "results": results,
        "total_results": total_results
    }
    # Return the response with appropriate headers
    return response_data


@app.get('/search', response_class=Response)
def get_result_by_id(query: str = "", lang: str = "", id: int = 0):
    res = search(query, lang, skip=0, limit=10)
    results = construct_response_by_id(res)

    for result in results:
        if result['id'] == id:
            return json.dumps(result, ensure_ascii=False)

    raise HTTPException(status_code=404, detail="Result not found")


@app.get("/download/{language}", response_class=Response)
def get_csv_file(language: str, token: str = Depends(oauth2_scheme)):
    verify_token(token)
    # Assuming you have language-specific CSV files in a "dataset" folder
    file_path = os.path.join("model", language, f"{language}.csv")

    # Open the CSV file
    with open(file_path, "r") as file:
        # Read the contents of the file
        csv_content = file.read()

    # Set the response headers
    response_headers = {
        "Content-Disposition": f"attachment; filename={language}.csv",
        "Content-Type": "text/csv"
    }

    # Return the CSV content as the response
    return Response(content=csv_content, headers=response_headers)


def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload["sub"]
        return username
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidTokenError, jwt.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/providers/{lang}")
def get_providers(lang: str):
    if lang not in languages:
        raise HTTPException(status_code=404, detail="Language not found")

    csv_files = languages[lang]['csv_files']
    providers = set()

    for csv_file in csv_files:
        csv_path = os.path.join("model", lang, csv_file)
        data = pd.read_csv(csv_path, lineterminator='\n')
        providers.update(data['Provider'].tolist())

    return JSONResponse(content={"providers": list(providers)})


# API endpoint for user registration
@app.post("/register", include_in_schema=False)
def register(username: str, password: str):
    # Check if username is already taken
    if get_user(username):
        raise HTTPException(status_code=400, detail="Username already registered")

    # Hash the password
    hashed_password = pwd_context.hash(password)

    # Create a new user
    user = {"username": username, "password": hashed_password}
    users.append(user)

    return {"message": "User registered successfully"}


# API endpoint for user login
@app.post("/login", include_in_schema=False)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username or password")

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}


# Protected API endpoint
@app.get("/protected", include_in_schema=False)
def protected_route(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        username = payload["sub"]
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except (jwt.InvalidTokenError, jwt.DecodeError):
        raise HTTPException(status_code=401, detail="Invalid token")

    return {"message": f"Hello, {username}! This is a protected route"}


@app.get("/languages")
def get_supported_languages():
    return {"languages": list(languages.keys())}


@app.get("/lucky")
def get_random_title(lang: str):
    file_path = f"model/{lang}/{lang}.csv"

    try:
        data = pd.read_csv(file_path, lineterminator='\n')

        if data.empty:
            return {"error": "No titles found for the specified language"}

        titles = data['Course Title'].tolist()
        random_title = random.choice(titles)

        return {"title": random_title}

    except FileNotFoundError:
        return {"error": "Language not found"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
