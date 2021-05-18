def main():
    from os import path

    fp = "popular-names.txt"
    n = int(input())
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    res = []
    for t in s:
        res.append(t.replace("\n", "").replace("\t", " "))
    print(res[:n])


if __name__ == "__main__":
    main()
