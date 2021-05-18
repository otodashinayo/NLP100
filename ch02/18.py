def main():
    from os import path, mkdir

    fp = "popular-names.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    res = []
    for t in s:
        res.append(t.split())
    for i in range(len(res)):
        res[i][2] = int(res[i][2])
    res.sort(key=lambda x:x[2], reverse=True)
    print(res)


if __name__ == "__main__":
    main()
