import requests
from bs4 import BeautifulSoup
import json
import time
import random

MAX_DEPTH = 2


def read_seed_urls():
    with open("seed_urls.txt", "r") as f:
        return [line.strip() for line in f.readlines()]


def bfs(seed_urls):
    urls = set()
    depth = 0
    to_be_visited = seed_urls

    while len(to_be_visited) > 0 and depth < MAX_DEPTH:
        tmp = []  # to_be_visited for the next iteration

        for url in to_be_visited:
            url = url.rstrip("/")

            # filter out:
            # 1. duplicate
            # 2. url that is not started with https:// or http://
            if url in urls or not (
                url.startswith("https://") or url.startswith("http://")
            ):
                continue

            time.sleep(random.uniform(0, 1))
            print(f"{url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")

            if not soup.html or soup.html.get("lang") != "en":
                continue

            urls.add(url)

            for a_tag in soup.find_all("a", href=True):
                link = a_tag["href"].rstrip("/")
                tmp.append(link)

        depth += 1
        to_be_visited = tmp

    urls = list(urls)

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
