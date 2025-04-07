import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random

MAX_DEPTH = 2
TEXT_LEN = 1000


def read_seed_urls():
    with open("seed_urls.txt", "r") as f:
        return [line.strip() for line in f.readlines()]


def bfs(seed_urls):
    urls = {} # url => { title, text, links }
    depth = 0
    to_be_visited = seed_urls

    while len(to_be_visited) > 0 and depth < MAX_DEPTH:
        tmp = [] # to_be_visited for the next iteration

        for url in to_be_visited:
            url = url.rstrip("/")

            # filter out:
            # 1. duplicate
            # 2. url that is not started with https:// or http://
            if url in urls or not (
                url.startswith("https://") or 
                url.startswith("http://")
            ):
                continue

            time.sleep(random.uniform(0, 1))
            print(f"{url}")
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            lang = soup.html.get("lang")

            # only crawl english sites
            if lang != "en":
                continue

            title = soup.title.string if soup.title else ""
            text = re.sub(r"\s+", " ", soup.get_text()).strip()[:TEXT_LEN]
            urls[url] = { 
                "url": url, 
                "title": title, 
                "text": text, 
                "links": [] 
            }

            for a_tag in soup.find_all("a", href=True):
                link = a_tag["href"].rstrip("/")
                urls[url]["links"].append(link)
                tmp.append(link)

        depth += 1
        to_be_visited = tmp

    return urls


def main():
    print("reading from seed_urls.txt")
    seed_urls = read_seed_urls()
    print("start crawling")
    urls = bfs(seed_urls[:])

    with open("urls.json", "w") as f:
        json.dump(urls, f, indent=4)


if __name__ == "__main__":
    main()
