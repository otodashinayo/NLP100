def n_gram(s, n):
    res = []
    for i in range(len(s) + 1 - n):
        res.append(s[i:i + n])
    return res


def main():
    X = set(n_gram("paraparaparadise", 2))
    Y = set(n_gram("paragraph", 2))
    print(f"union: {X | Y}")
    print(f"intersection: {X & Y}")
    print(f"difference: {X - Y}")
    print(f"'se' in X: {'se' in X}")
    print(f"'se' in Y: {'se' in Y}")


if __name__ == "__main__":
    main()
