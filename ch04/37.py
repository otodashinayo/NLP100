def main():
    from os import path
    from pprint import pprint
    import json
    from collections import Counter
    import matplotlib.pyplot as plt
    from matplotlib import rcParams
    rcParams["font.sans-serif"] = ["Hiragino Maru Gothic Pro"]

    fp = "30/neko.txt.mecab"
    s = json.load(open(path.join(path.dirname(path.abspath(__file__)), fp), "r"))
    res = []
    for t in s:
        ws = [w["base"] for w in t]
        if "猫" in ws:
            res.extend(ws)
    res = Counter(res).most_common(10)
    plt.bar([t[0] for t in res], [t[1] for t in res])
    plt.pause(5)

if __name__ == "__main__":
    main()
