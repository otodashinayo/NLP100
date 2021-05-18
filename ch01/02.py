def main():
    s_1 = "パトカー"
    s_2 = "タクシー"
    res = ""
    for t_1, t_2 in zip(s_1, s_2):
        res += t_1 + t_2
    print(res)


if __name__ == "__main__":
    main()
