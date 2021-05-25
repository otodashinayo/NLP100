def main():
    from os import path
    from pprint import pprint

    with open(path.join(path.dirname(path.abspath(__file__)), "12/col1.txt"), "r") as f:
        s_1 = f.readlines()
    with open(path.join(path.dirname(path.abspath(__file__)), "12/col2.txt"), "r") as f:
        s_2 = f.readlines()
    res = []
    for t_1, t_2 in zip(s_1, s_2):
        res.append([t_1.replace("\n", ""), t_2.replace("\n", "")])
    pprint(res)


if __name__ == "__main__":
    main()
