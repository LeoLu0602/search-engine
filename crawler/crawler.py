from bs4 import BeautifulSoup


def read_seed_urls():
    seed_urls = []

    with open("seed_urls.txt", "r") as f:
        lines = f.readlines()

        for line in lines:
            seed_urls.append(line.strip())

    return seed_urls


def bfs(seed_urls):
    urls = []

    return urls


def main():
    print("reading from seed_urls.txt")
    seed_urls = read_seed_urls()


if __name__ == "__main__":
    main()
