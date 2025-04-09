import requests
from bs4 import BeautifulSoup
import json
import time
import random
from nltk.tokenize import RegexpTokenizer  # type: ignore
from concurrent.futures import ThreadPoolExecutor


MAX_DEPTH = 1


def read_seed_urls():
    with open("seed_urls.txt", "r") as f:
        return [line.strip() for line in f.readlines()]


def extract_tokens(text, count):
    tokenizer = RegexpTokenizer(r"\w+[-'\w]*")
    tokens = tokenizer.tokenize(text)

    return tokens[:count]


def visit(url, visited, depth):
    try:
        url = url.rstrip("/")
        links = []

        # filter out:
        # 1. duplicate
        # 2. url that is not started with https:// or http://
        if url in visited or not (
            url.startswith("https://") or url.startswith("http://")
        ):
            return None

        time.sleep(random.uniform(0, 0.5))
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        if not soup.html or soup.html.get("lang") != "en":
            return None

        title = soup.title.get_text() if soup.title else ""
        body_text = soup.body.get_text() if soup.body else ""
        content = extract_tokens(body_text, 200)

        for a_tag in soup.find_all("a", href=True):
            link = a_tag["href"].rstrip("/")
            links.append(link)

        visited.add(url)
        print(f"depth={depth} {url}")

        return {"url": url, "title": title, "content": content}, links
    except:
        return None


def crawl(visited, to_be_visited, depth, max_workers):
    urls = []
    new_to_be_visited = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(visit, url, visited, depth) for url in to_be_visited]

        for future in futures:
            res = future.result()

            if res:
                details, links = res
                urls.append(details)
                new_to_be_visited += links

    return urls, new_to_be_visited


def main():
    print("read from seed_urls.txt")
    seed_urls = read_seed_urls()
    print("start crawling")

    urls = []  # a list of {url, title, content}
    visited = set()  # a set of url
    to_be_visited = seed_urls[:]  # urls to be visited for a certain depth
    depth = 0

    while depth <= MAX_DEPTH and len(to_be_visited) > 0:
        urls_partial, to_be_visited = crawl(visited, to_be_visited, depth, 20)
        urls += urls_partial
        depth += 1

    with open("urls.json", "w") as f:
        json.dump(urls, f, indent=4)


if __name__ == "__main__":
    main()
