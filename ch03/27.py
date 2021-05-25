def main():
    from os import path
    import re
    from pprint import pprint

    fp = "20/20.txt"
    with open(path.join(path.dirname(path.abspath(__file__)), fp), "r") as f:
        s = f.readlines()
    s = [re.sub("\n", "", t) for t in s]
    res = {}
    cnt = 0
    for t in s:
        if re.search("^\{\{基礎情報", t):
            cnt += 1
        elif cnt > 0:
            if re.search("\{\{", t):
                cnt += len(re.findall("\{\{", t))
            if re.search("\}\}", t):
                cnt -= len(re.findall("\}\}", t))
            if cnt > 0:
                if re.search("^\|.*=", t):
                    key = re.sub("^\||=.*", "", t)
                    key = re.sub(" *$", "", key)
                    value = re.sub("^\|.*?=", "", t)
                    value = re.sub("^ *", "", value)
                    value = re.sub("'", "", value)
                    value = re.sub("\[\[|(#[^[]*?)*(\|[^[]*?)*\]\]", "", value)
                    res[key] = value
                else:
                    value = re.sub("^\|.*?=", "", t)
                    value = re.sub("^ *", "", value)
                    value = re.sub("'", "", value)
                    value = re.sub("\[\[|(#[^[]*?)*(\|[^[]*?)*\]\]", "", value)
                    res[key] += "\n" + value
    pprint(res)


if __name__ == "__main__":
    main()
