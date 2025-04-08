import json


def read_urls():
    with open("./crawler/urls.json", "r") as f:
        return json.load(f)


def process_urls(urls):
    index = {}
    
    for url in urls:
        pass

    return index

def main():
    print("read from ./crawler/urls.json")
    urls = read_urls()
    index = process_urls(urls)


if __name__ == "__main__":
    main()
