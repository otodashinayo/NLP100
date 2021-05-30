def main():
    from os import path
    from pprint import pformat
    import json

    class Morph:
        def __init__(self, d) -> None:
            self.surface = d["surface"]
            self.base = d["base"]
            self.pos = d["pos"]
            self.pos1 = d["pos1"]

        def __str__(self) -> str:
            res = pformat({"surface": self.surface, "base": self.base,
                          "pos": self.pos, "pos1": self.pos1})
            return res

    class Chunk:
        def __init__(self, d) -> None:
            self.morphs = d["morphs"]
            self.dst = d["dst"]
            self.srcs = d["srcs"]

        def __str__(self) -> str:
            res = pformat(
                {"morphs": self.morphs, "dst": self.dst, "srcs": self.srcs})
            return res

        @property
        def text(self):
            res = "".join(
                [morph.surface for morph in self.morphs if morph.pos != "記号"])
            return res

        @property
        def contain_noun(self):
            res = any([morph.pos == "名詞" for morph in self.morphs])
            return res

        @property
        def contain_verb(self):
            res = any([morph.pos == "動詞" for morph in self.morphs])
            return res

        @property
        def contain_particle(self):
            res = any([morph.pos == "助詞" for morph in self.morphs])
            return res

        @property
        def contain_particle_2(self):
            if len(self.morphs) >= 2:
                res = any([morph_1.pos1 == "サ変接続" and morph_2.surface == "を" and morph_2.pos ==
                          "助詞" for morph_1, morph_2 in zip(self.morphs[:-1], self.morphs[1:])])
            else:
                res = False
            return res

        @property
        def verbs(self):
            res = [morph.base for morph in self.morphs if morph.pos == "動詞"]
            return res

        @property
        def particles(self):
            res = [morph.base for morph in self.morphs if morph.pos == "助詞"]
            return res

        @property
        def particles_2(self):
            if len(self.morphs) >= 2:
                res = [morph_2.base for morph_1, morph_2 in zip(
                    self.morphs[:-1], self.morphs[1:]) if morph_1.pos1 == "サ変接続" and morph_2.surface == "を" and morph_2.pos == "助詞"]
            else:
                res = []
            return res

    fp = "40/ai.ja.txt.parsed"
    s = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp), "r"))
    for t in s:
        for src, chunk in t.items():
            chunk["morphs"] = [Morph(morph) for morph in chunk["morphs"]]
            t[src] = Chunk(t[src])
    for src, chunk in s[13].items():
        if chunk.contain_noun:
            texts = []
            target = chunk
            dst = target.dst
            while dst != "-1":
                texts.append(target.text)
                target = s[13][dst]
                dst = target.dst
            print(" -> ".join(texts))


if __name__ == "__main__":
    main()
