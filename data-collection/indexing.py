import json
import nltk  # type: ignore
from nltk.corpus import stopwords  # type: ignore

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))


def read_urls():
    with open("./urls.json", "r") as f:
        return json.load(f)


def process_urls(urls):
    tmp = {}

    for url in urls:
        for token in url["content"]:
            token = token.lower()

            # we don't need stop words
            if token in STOP_WORDS:
                continue

            if token not in tmp:
                tmp[token] = set()

            # url["content"] may contain duplicate tokens
            # use set to avoid duplicates
            tmp[token].add(url["url"])

    index = []

    for key, val in tmp.items():
        index.append({"token": key, "urls": list(val)})
    
    print(f"{len(index)} tokens")

    return index


def main():
    print("read from urls.json")
    urls = read_urls()
    index = process_urls(urls)

    with open("./index.json", "w") as f:
        json.dump(index, f, indent=4)


if __name__ == "__main__":
    main()
