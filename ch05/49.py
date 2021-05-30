def main():
    from os import path
    from pprint import pformat
    import json
    from itertools import combinations
    from collections import deque

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

        @property
        def text_X(self):
            res = ""
            flg = False
            for morph in self.morphs:
                if morph.pos != "記号":
                    if morph.pos == "名詞":
                        if not flg:
                            res += "X"
                            flg = True
                    else:
                        res += morph.surface
                        flg = False
            return res

        @property
        def text_Y(self):
            res = ""
            flg = False
            for morph in self.morphs:
                if morph.pos != "記号":
                    if morph.pos == "名詞":
                        if not flg:
                            res += "Y"
                            flg = True
                    else:
                        res += morph.surface
                        flg = False
            return res

    fp = "40/ai.ja.txt.parsed"
    s = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp), "r"))
    for t in s:
        for src, chunk in t.items():
            chunk["morphs"] = [Morph(morph) for morph in chunk["morphs"]]
            t[src] = Chunk(t[src])
    for (src, chunk_1), (src, chunk_2) in combinations(s[13].items(), 2):
        if chunk_1.contain_noun and chunk_2.contain_noun:
            texts_1 = deque([])
            target = chunk_1
            dst = target.dst
            while dst != "-1":
                texts_1.append(target)
                target = s[13][dst]
                dst = target.dst
            texts_2 = deque([])
            target = chunk_2
            dst = target.dst
            while dst != "-1":
                texts_2.append(target)
                target = s[13][dst]
                dst = target.dst
            texts_3 = deque([])
            flg = True
            while len(texts_1) > 0 and len(texts_2) and flg:
                text_1, text_2 = texts_1.pop(), texts_2.pop()
                if text_1.text == text_2.text:
                    texts_3.appendleft(text_2)
                else:
                    texts_1.append(text_1)
                    texts_2.append(text_2)
                    flg = False
            texts = []
            if len(texts_1) > 0 and len(texts_2) == 0 and len(texts_3) > 0:
                print(" -> ".join([" -> ".join([t.text_X if i == 0 else t.text for i,
                      t in enumerate(texts_1)]), texts_3[0].text_Y]))
            elif len(texts_1) > 0 and len(texts_2) > 0 and len(texts_3) > 0:
                print(" | ".join([" -> ".join([t.text_X if i == 0 else t.text for i, t in enumerate(texts_1)]),
                      " -> ".join([t.text_Y if i == 0 else t.text for i, t in enumerate(texts_2)]), texts_3[0].text]))


if __name__ == "__main__":
    main()
