import requests
from bs4 import BeautifulSoup
import json
import time
import random
from nltk.tokenize import RegexpTokenizer  # type: ignore


MAX_DEPTH = 0


def read_seed_urls():
    with open("seed_urls.txt", "r") as f:
        return [line.strip() for line in f.readlines()]


def extract_tokens(text, count):
    tokenizer = RegexpTokenizer(r"\w+[-'\w]*")
    tokens = tokenizer.tokenize(text)

    return tokens[:count]


def crawl(visited, to_be_visited, depth):
    urls = []
    new_to_be_visited = []

    for url in to_be_visited:
        url = url.rstrip("/")

        # filter out:
        # 1. duplicate
        # 2. url that is not started with https:// or http://
        if url in visited or not (
            url.startswith("https://") or url.startswith("http://")
        ):
            continue

        time.sleep(random.uniform(0, 0.5))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        if not soup.html or soup.html.get("lang") != "en":
            continue

        title = soup.title.get_text() if soup.title else ""
        body_text = soup.body.get_text() if soup.body else ""
        content = extract_tokens(body_text, 200)
        urls.append({"url": url, "title": title, "content": content})
        visited.add(url)
        print(f"#{len(urls)} (depth: {depth}) {url}")

        for a_tag in soup.find_all("a", href=True):
            link = a_tag["href"].rstrip("/")
            new_to_be_visited.append(link)

    return urls, new_to_be_visited


def main():
    print("read from seed_urls.txt")
    seed_urls = read_seed_urls()
    print("start crawling")

    urls = []  # a list of {url, title, content}
    visited = set()  # a set of url
    to_be_visited = seed_urls[:]
    depth = 0

    while depth <= MAX_DEPTH and len(to_be_visited) > 0:
        urls_partial, to_be_visited = crawl(visited, to_be_visited, depth)
        urls += urls_partial
        depth += 1

    with open("urls.json", "w") as f:
        json.dump(urls, f, indent=4)


if __name__ == "__main__":
    main()
