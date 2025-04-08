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


def bfs(seed_urls):
    urls = []
    url_visited = set()
    depth = 0
    to_be_visited = seed_urls

    while len(to_be_visited) > 0:
        tmp = []  # to_be_visited for the next iteration

        for url in to_be_visited:
            url = url.rstrip("/")

            # filter out:
            # 1. duplicate
            # 2. url that is not started with https:// or http://
            if url in url_visited or not (
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
            url_visited.add(url)
            print(f"#{len(urls)} {url} (depth: {depth})")

            for a_tag in soup.find_all("a", href=True):
                link = a_tag["href"].rstrip("/")
                tmp.append(link)

        depth += 1
        to_be_visited = tmp

        if depth > MAX_DEPTH:
            break

    return urls


def main():
    print("read from seed_urls.txt")
    seed_urls = read_seed_urls()
    print("start crawling")
    urls = bfs(seed_urls[:])

    with open("urls.json", "w") as f:
        json.dump(urls, f, indent=4)


if __name__ == "__main__":
    main()
