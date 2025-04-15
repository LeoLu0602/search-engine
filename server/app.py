from flask import Flask, request, jsonify
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from pymongo import MongoClient
import os
from dotenv import load_dotenv

nltk.download("stopwords")  # type: ignore
STOP_WORDS = set(stopwords.words("english"))
MAX_QUERY_LEN = 32  # maximum number of words in a query

load_dotenv()
client = MongoClient(os.getenv("MONGO_URI"))
db = client["search-engine"]
app = Flask(__name__)


def extract_tokens(text):
    tokenizer = RegexpTokenizer(r"\w+[-'\w]*")
    tokens = tokenizer.tokenize(text)[:MAX_QUERY_LEN]
    tokens = [token.lower() for token in tokens if token.lower() not in STOP_WORDS]

    return tokens


@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q")
    res = []

    if not q:
        return jsonify(res)

    tokens = extract_tokens(q)
    urls_dict = {} # url -> appearance

    for token in tokens:
        print(token)
        token_urls = db["index"].find_one({"token": token})["urls"]
        
        if not token_urls:
            token_urls = []
        
        for url in token_urls:
            if url not in urls_dict:
                urls_dict[url] = 0
            
            urls_dict[url] += 1

    print(urls_dict.keys())

    return jsonify([{"url": "https://www.google.com", "title": "Google"}])
