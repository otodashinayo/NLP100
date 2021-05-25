def main():
    from os import path, mkdir
    from pprint import pprint
    import json

    fp = "jawiki-country.json"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    s = [json.loads(t) for t in s]
    res = ""
    for t in s:
        if t["title"] == "イギリス":
            res = t["text"]
            break
    pprint(res)
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "20")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "20"))
    with open(path.join(path.dirname(path.abspath(__file__)), "20/20.txt"), "w") as f:
        f.write(res)


if __name__ == "__main__":
    main()
