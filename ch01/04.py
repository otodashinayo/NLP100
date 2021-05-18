def main():
    s = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
    s = s.replace(",", "").replace(".", "")
    res = {}
    for i, t in enumerate(s.split()):
        if i + 1 in [1, 5, 6, 7, 8, 9, 15, 16, 19]:
            res[t[0]] = i + 1
        else:
            res[t[:2]] = i + 1
    print(res)


if __name__ == "__main__":
    main()
