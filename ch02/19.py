def main():
    from os import path
    from collections import Counter
    from pprint import pprint

    fp = "popular-names.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    res = []
    for t in s:
        res.append(t.split()[0])
    res = Counter(res)
    pprint(res)


if __name__ == "__main__":
    main()
