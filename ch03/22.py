def main():
    from os import path
    import re
    from pprint import pprint

    fp = "20/20.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    s = [re.sub("\n", "", t) for t in s]
    res = [re.sub("^\[\[Category\:|(\|.)*\]\]$", "", t)
           for t in s if re.search("^\[\[Category\:.*(\|.)*\]\]$", t)]
    pprint(res)


if __name__ == "__main__":
    main()
