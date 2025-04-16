import requests
from bs4 import BeautifulSoup
import json
import time
import random
import nltk
from nltk.tokenize import RegexpTokenizer  # type: ignore
from nltk.corpus import stopwords  # type: ignore
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse, urlunparse

nltk.download("stopwords")
STOP_WORDS = set(stopwords.words("english"))
MAX_DEPTH = 0


def read_seed_urls():
    with open("seed_urls.txt", "r") as f:
        return [line.strip() for line in f.readlines()]


def extract_tokens(text, count):
    tokenizer = RegexpTokenizer(r"\w+[-'\w]*")
    tokens = tokenizer.tokenize(text)
    tokens = list(
        set([token.lower() for token in tokens if token.lower() not in STOP_WORDS])
    )

    return tokens[:count]


def visit(url, urls_dict, url_in_degrees, depth):
    try:
        url = url.rstrip("/")
        links = []

        # filter out:
        # 1. duplicate
        # 2. url that is not started with https:// or http://
        if url in urls_dict or not (
            url.startswith("https://") or url.startswith("http://")
        ):
            return None

        time.sleep(random.uniform(0, 0.5))
        response = requests.get(
            url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/122.0.0.0 Safari/537.36"
                )
            },
        )
        soup = BeautifulSoup(response.content, "html.parser")

        if not soup.html:
            return None

        parsed_url = urlparse(url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))
        title = soup.title.get_text() if soup.title else ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        description = meta_desc["content"] if meta_desc else ""
        tokens = extract_tokens(
            soup.body.get_text() if soup.body else "", 1000
        )  # unique tokens

        urls_dict[url] = {
            "title": title,
            "description": description,
            "tokens": tokens,
        }

        for a_tag in soup.find_all("a", href=True):
            link = a_tag["href"].rstrip("/")

            # handle relative path
            if link.startswith("/"):
                parsed_url = urlparse(url)
                base_url = urlunparse(
                    (parsed_url.scheme, parsed_url.netloc, "", "", "", "")
                )
                link = base_url + link

                if link not in url_in_degrees:
                    url_in_degrees[link] = 0

                url_in_degrees[link] += 1

            links.append(link)

        print(f"depth={depth} {url}")

        return links
    except Exception as e:
        print(e)

        return None


def crawl(urls_dict, url_in_degrees, to_be_visited, depth, max_workers):
    new_to_be_visited = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [
            executor.submit(visit, url, urls_dict, url_in_degrees, depth)
            for url in to_be_visited
        ]

        for future in futures:
            links = future.result()

            if links:
                new_to_be_visited += links

    return new_to_be_visited


def main():
    seed_urls = read_seed_urls()
    urls_dict = {}  # url -> {title, description, tokens, in_degrees}
    url_in_degrees = {}  # url -> in-degrees
    to_be_visited = seed_urls[:]  # urls to be visited for depth n
    depth = 0

    while depth <= MAX_DEPTH and len(to_be_visited) > 0:
        to_be_visited = crawl(urls_dict, url_in_degrees, to_be_visited, depth, 30)
        depth += 1

    urls = []

    for url in urls_dict:
        urls.append(
            {
                "url": url,
                "title": urls_dict[url]["title"],
                "description": urls_dict[url]["description"],
                "tokens": urls_dict[url]["tokens"],
                "in_degrees": url_in_degrees[url] if url in url_in_degrees else 0,
            }
        )

    with open("urls.json", "w") as f:
        json.dump(urls, f, indent=4)


if __name__ == "__main__":
    main()
