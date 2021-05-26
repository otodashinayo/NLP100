def main():
    from os import path
    from pprint import pprint
    import json

    fp = "30/neko.txt.mecab"
    s = json.load(open(path.join(path.dirname(path.abspath(__file__)), fp), "r"))
    res = []
    for t in s:
        tmp = []
        for w in t:
            if w["pos"][:2] == "名詞":
                tmp.append(w["surface"])
            else:
                break
        if len(tmp) > len(res):
            res = tmp
    pprint("".join(res))

if __name__ == "__main__":
    main()
