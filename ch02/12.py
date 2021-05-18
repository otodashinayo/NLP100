def main():
    from os import path

    fp = "popular-names.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    res = []
    for t in s:
        res.append(t.split())
    print(res)
    with open(path.join(path.dirname(path.abspath(__file__)), "col1.txt"), "w") as f:
        f.write("\n".join([t[0] for t in res]))
    with open(path.join(path.dirname(path.abspath(__file__)), "col2.txt"), "w") as f:
        f.write("\n".join([t[1] for t in res]))


if __name__ == "__main__":
    main()
