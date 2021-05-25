def main():
    from os import path
    from pprint import pprint

    fp = "popular-names.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    res = []
    for t in s:
        res.append(t.replace("\n", "").replace("\t", " "))
    pprint(res)


if __name__ == "__main__":
    main()
