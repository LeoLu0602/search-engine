import json
import nltk  # type: ignore
from nltk.corpus import stopwords  # type: ignore

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))


def read_urls():
    with open("./urls.json", "r") as f:
        return json.load(f)


def process_urls(urls):
    index = {}

    for url in urls:
        for token in url["content"]:
            token = token.lower()

            # we don't need stop words
            if token in STOP_WORDS:
                continue

            if token not in index:
                index[token] = []

            index[token].append(url["url"])

    print(f"{len(index.keys())} tokens")

    return index


def main():
    print("read from urls.json")
    urls = read_urls()
    index = process_urls(urls)

    with open("./index.json", "w") as f:
        json.dump(index, f, indent=4)


if __name__ == "__main__":
    main()
