import json
import os


def read():
    with open("./urls.json", "r") as f:
        return json.load(f)


def split(urls, chunk_size):
    chunks = [urls[i:i + chunk_size] for i in range(0, len(urls), chunk_size)]

    if not os.path.exists("urls_chunks"):
        os.mkdir("urls_chunks")

    for i, chunk in enumerate(chunks):
        path = os.path.join("urls_chunks", f"chunk-{i}.json")
        
        with open(path, "w") as f:
            json.dump(chunk, f, indent=4)

    
    print(f"number of chunks: {len(chunks)}")


def main():
    urls = read()
    print(f"number of urls: {len(urls)}")
    split(urls, 500)


if __name__ == "__main__":
    main()
