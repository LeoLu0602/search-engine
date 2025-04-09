from flask import Flask, request, jsonify
from nltk.tokenize import RegexpTokenizer  # type: ignore

app = Flask(__name__)


def extract_tokens(text):
    tokenizer = RegexpTokenizer(r"\w+[-'\w]*")
    tokens = tokenizer.tokenize(text)
    tokens = [token.lower() for token in tokens]
    
    return tokens


@app.route("/search", methods=["GET"])
def search():
    q = request.args.get("q")
    res = []

    if not q:
        return jsonify(res)

    tokens = extract_tokens(q)

    return jsonify([{"url": "https://www.google.com", "title": "Google"}])
