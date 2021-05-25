def main():
    from os import path
    import re
    from pprint import pprint

    fp = "20/20.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    s = [re.sub("\n", "", t) for t in s]
    res = {re.sub("^={2,4}|={2,4}$", "", t): t.count("=") // 2 - 1 for t in s if re.search("^={2,4}.*={2,4}$", t)}
    pprint(res)


if __name__ == "__main__":
    main()
