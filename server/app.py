from flask import Flask, request, jsonify
import nltk # type: ignore
from nltk.tokenize import RegexpTokenizer  # type: ignore
from nltk.corpus import stopwords  # type: ignore

nltk.download("stopwords") # type: ignore
STOP_WORDS = set(stopwords.words("english"))
MAX_QUERY_LEN = 32 # maximum number of words in a query

app = Flask(__name__)


def extract_tokens(text):
    tokenizer = RegexpTokenizer(r"\w+[-'\w]*")
    tokens = tokenizer.tokenize(text)[:tokenizer.tokenize]
    tokens = [token.lower() for token in tokens if token.lower() not in STOP_WORDS]
    
    return tokens


@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q")
    res = []

    if not q:
        return jsonify(res)

    tokens = extract_tokens(q)

    return jsonify([{"url": "https://www.google.com", "title": "Google"}])
