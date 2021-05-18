def main():
    from os import path, mkdir

    fp = "popular-names.txt"
    n = int(input())
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    res = []
    for t in s:
        res.append(t.replace("\n", "").replace("\t", " "))
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "16")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "16"))
    for i in range(n):
        with open(path.join(path.dirname(path.abspath(__file__)), f"16/{i}.txt"), "w") as f:
            f.write("\n".join(res[i * len(res) // n: (i + 1) * len(res) // n]))


if __name__ == "__main__":
    main()
