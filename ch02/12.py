def main():
    from os import path, mkdir
    from pprint import pprint

    fp = "popular-names.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    res = []
    for t in s:
        res.append(t.split())
    pprint(res)

    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "12")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "12"))
    with open(path.join(path.dirname(path.abspath(__file__)), "12/col1.txt"), "w") as f:
        f.write("\n".join([t[0] for t in res]))
    with open(path.join(path.dirname(path.abspath(__file__)), "12/col2.txt"), "w") as f:
        f.write("\n".join([t[1] for t in res]))


if __name__ == "__main__":
    main()
