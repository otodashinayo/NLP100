def main():
    from os import path
    from pprint import pprint
    import json

    fp = "30/neko.txt.mecab"
    s = json.load(open(path.join(path.dirname(path.abspath(__file__)), fp), "r"))
    res = []
    for t in s:
        if len(t) >= 3:
            for w_1, w_2, w_3 in zip(t[:-2], t[1:-1], t[2:]):
                if w_1["pos"][:2] == "名詞" and w_2["surface"] == "の" and w_3["pos"][:2] == "名詞":
                    res.append(w_1["surface"] + w_2["surface"] + w_3["surface"])
    pprint(res)

if __name__ == "__main__":
    main()
