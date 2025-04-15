import sys
import json
import os
import random
import math


def main():
    with open(f"{sys.argv[1]}.json", "r") as f:
        full_list = json.load(f)

    print(f"list length: {len(full_list)}")
    random.shuffle(full_list)
    chunk_size = int(sys.argv[2])

    if not os.path.exists(f"{sys.argv[1]}_chunks"):
        os.mkdir(f"{sys.argv[1]}_chunks")

    for i in range(0, len(full_list), chunk_size):
        chunk = full_list[i : i + chunk_size]
        path = os.path.join(
            f"{sys.argv[1]}_chunks",
            f"{sys.argv[1]}_{math.floor(i / chunk_size) + 1}_chunks.json",
        )

        with open(path, "w") as f:
            json.dump(chunk, f, indent=4)

    print(f"number of chunks: {math.ceil(len(full_list) / chunk_size)}")


if __name__ == "__main__":
    main()
