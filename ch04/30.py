def main():
    from os import path, mkdir
    import re
    import MeCab
    from pprint import pprint
    import json

    fp = "neko.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    tagger = MeCab.Tagger("-Ochasen")
    s = [re.sub("\n", "", t) for t in s]
    s = [re.sub("\n*EOS\n$", "", tagger.parse(t)) for t in s if t != ""]
    s = [[w.split("\t") for w in t.split("\n")] for t in s]
    res = [[{"surface": w[0], "base": w[2], "pos": w[3], "pos1": w[4]}
            for w in t] for t in s]
    pprint(res[:5])
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "30")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "30"))
    json.dump(res, open(path.join(path.dirname(
        path.abspath(__file__)), "30/neko.txt.mecab"), "w"))


if __name__ == "__main__":
    main()
