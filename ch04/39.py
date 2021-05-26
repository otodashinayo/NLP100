def main():
    from os import path
    import json
    from collections import Counter
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams["font.sans-serif"] = ["Hiragino Maru Gothic Pro"]

    fp = "30/neko.txt.mecab"
    s = json.load(open(path.join(path.dirname(path.abspath(__file__)), fp), "r"))
    res = []
    for t in s:
        for w in t:
            res.append(w["base"])
    res = Counter(res).most_common()
    plt.plot(range(len(res)), [t[1] for t in res])
    plt.xscale("log")
    plt.yscale("log")
    plt.pause(5)

if __name__ == "__main__":
    main()
