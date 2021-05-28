def main():
    from os import path, mkdir
    import re
    import CaboCha
    from pprint import pprint, pformat
    import json
    
    class Morph:
        def __init__(self, d) -> None:
            self.surface = d["surface"]
            self.base = d["base"]
            self.pos = d["pos"]
            self.pos1 = d["pos1"]

        def __str__(self) -> str:
            res = pformat({"surface": self.surface, "base": self.base, "pos": self.pos, "pos1": self.pos1})
            return res

    fp = "ai.ja/ai.ja.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    parser = CaboCha.Parser()
    s = [re.sub("\n", "", t) for t in s]
    s = [re.sub("\n*EOS\n$", "", parser.parse(t).toString(CaboCha.FORMAT_LATTICE)) for t in s if t != ""]
    s = [[re.split("\t|,| ", w) for w in t.split("\n")] for t in s]
    res = []
    for t in s:
        tmp = {}
        for w in t:
            if w[0] == "*":
                key = w[1]
                tmp[key] = {"dst": re.sub("D", "", w[2]), "srcs": [], "morphs": []}
            else:
                tmp[key]["morphs"].append({"surface": w[0], "base": w[7], "pos": w[1], "pos1": w[2]})
        res.append(tmp)
    for tmp in res:
        for src, chunk in tmp.items():
            dst = chunk["dst"]
            if dst != "-1":
                tmp[dst]["srcs"].append(src)
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "40")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "40"))
    json.dump(res, open(path.join(path.dirname(path.abspath(__file__)), "40/ai.ja.txt.parsed"), "w"))
    
    for tmp in res:
        for src, chunk in tmp.items():
            chunk["morphs"] = [Morph(morph) for morph in chunk["morphs"]]
    for src, chunk in res[1].items():
        pprint([str(morph) for morph in chunk["morphs"]])


if __name__ == "__main__":
    main()
