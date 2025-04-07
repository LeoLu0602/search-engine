import requests
from bs4 import BeautifulSoup
import json
import re
import time
import random

MAX_DEPTH = 2
TEXT_LEN = 200


def read_seed_urls():
    seed_urls = []

    with open("seed_urls.txt", "r") as f:
        lines = f.readlines()

        for line in lines:
            seed_urls.append(line.strip())

    return seed_urls


def bfs(seed_urls):
    urls = {}
    depth = 0
    queue = seed_urls

    while len(queue) > 0 and depth < MAX_DEPTH:
        new_queue = []

        for url in queue:
            url = url.rstrip("/")

            # filter out: url that is not started with https:// or http://
            # url is guaranteed to be new
            if not (url.startswith("https://") or url.startswith("http://")):
                continue

            time.sleep(random.uniform(0, 1))
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            lang = soup.html.get('lang')

            # only crawl english sites
            if lang != "en":
                continue

            title = soup.title.string if soup.title else ""
            text = re.sub(r"\s+", " ", soup.get_text()).strip()[:TEXT_LEN]
            urls[url] = {"url": url, "title": title, "text": text, "in_degree": 0}
            print(f"{url}")

            for a_tag in soup.find_all("a", href=True):
                link = a_tag["href"].rstrip("/")

                if link in urls:
                    urls[link]["in_degree"] += 1

                    # link was visited before -> don't put it into queue again
                    continue 

                new_queue.append(link)

        depth += 1
        queue = new_queue

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
