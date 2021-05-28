def main():
    from os import path
    from pprint import pformat
    import json
    import networkx as nx
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams["font.sans-serif"] = ["Hiragino Maru Gothic Pro"]

    class Morph:
        def __init__(self, d) -> None:
            self.surface = d["surface"]
            self.base = d["base"]
            self.pos = d["pos"]
            self.pos1 = d["pos1"]

        def __str__(self) -> str:
            res = pformat({"surface": self.surface, "base": self.base, "pos": self.pos, "pos1": self.pos1})
            return res

    class Chunk:
        def __init__(self, d) -> None:
            self.morphs = d["morphs"]
            self.dst = d["dst"]
            self.srcs = d["srcs"]

        def __str__(self) -> str:
            res = pformat({"morphs": self.morphs, "dst": self.dst, "srcs": self.srcs})
            return res

        @property
        def text(self):
            res = "".join([morph.surface for morph in self.morphs if morph.pos != "記号"])
            return res

        @property
        def contain_noun(self):
            res = any([morph.pos == "名詞" for morph in self.morphs])
            return res

        @property
        def contain_verb(self):
            res = any([morph.pos == "動詞" for morph in self.morphs])
            return res

    fp = "40/ai.ja.txt.parsed"
    s = json.load(open(path.join(path.dirname(path.abspath(__file__)), fp), "r"))
    for t in s:
        for src, chunk in t.items():
            chunk["morphs"] = [Morph(morph) for morph in chunk["morphs"]]
            t[src] = Chunk(t[src])
    G = nx.DiGraph()
    G.add_edges_from([(chunk.text, s[1][chunk.dst].text) for src, chunk in s[1].items() if chunk.dst != "-1"])
    pos = nx.spring_layout(G, seed=0)
    nx.draw_networkx_edges(G, pos)
    nx.draw_networkx_labels(G, pos, font_size=6)
    plt.pause(5)


if __name__ == "__main__":
    main()
