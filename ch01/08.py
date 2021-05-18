def cipher(s):
    res = ""
    for t in s:
        if ord("a") <= ord(t) <= ord("z"):
            res += chr(219 - ord(t))
        else:
            res += t
    return res


def main():
    s = "Hi He Lied Because Boron Could Not Oxidize Fluorine. New Nations Might Also Sign Peace Security Clause. Arthur King Can."
    c_1 = cipher(s)
    c_2 = cipher(c_1)
    print(f"c_1: {c_1}")
    print(f"c_2: {c_2}")


if __name__ == "__main__":
    main()
