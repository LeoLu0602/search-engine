import os
import json
import math
import random


def main():
    if not os.path.exists("index_chunks"):
        os.mkdir("index_chunks")

    with open("index.json", "r") as f:
        dict = json.load(f)

    print(f"number of keys: {len(dict)}")

    chunk_size = 5000
    keys = list(dict.keys())
    random.shuffle(keys) # first few keys in index have huge lists

    for i in range(0, len(dict), chunk_size):
        tmp = {}

        for j in range(i, min(i + chunk_size, len(dict))):
            key = keys[j]
            tmp[key] = dict[key]

        path = os.path.join("index_chunks", f"chunk-{math.floor(i / chunk_size)}.json")

        with open(path, "w") as f:
            json.dump(tmp, f, indent=4)

    print(f"number of chunks: {math.ceil(len(dict) / chunk_size)}")


if __name__ == "__main__":
    main()
