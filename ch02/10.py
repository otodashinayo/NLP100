def main():
    from os import path

    fp = "popular-names.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp)) as f:
        s = f.readlines()
    res = len(s)
    print(res)


if __name__ == "__main__":
    main()
