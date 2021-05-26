def main():
    from os import path
    from pprint import pprint
    import json

    fp = "30/neko.txt.mecab"
    s = json.load(open(path.join(path.dirname(path.abspath(__file__)), fp), "r"))
    res = []
    for t in s:
        for w in t:
            res.append(w["base"])
    pprint(res)

if __name__ == "__main__":
    main()
