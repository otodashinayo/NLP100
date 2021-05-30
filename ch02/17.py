def main():
    from os import path

    fp = "popular-names.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    res = []
    for t in s:
        res.append(t.split()[0])
    res = set(res)
    print(len(res))


if __name__ == "__main__":
    main()
