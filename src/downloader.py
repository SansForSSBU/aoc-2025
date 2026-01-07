import requests
import sys

cookie = sys.argv[1]
cj = {"session": cookie}

year=2025
for day in range(1, 13):
    req = requests.get(f"https://adventofcode.com/{year}/day/{day}/input", cookies=cj)
    with open(f"../inputs/{day}.txt", "w") as f:
        f.write(req.text)