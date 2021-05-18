def f(x, y, z):
    res = f"{x}時の{y}は{z}"
    return res


def main():
    x = 12
    y = "気温"
    z = 22.4
    res = f(x, y, z)
    print(res)


if __name__ == "__main__":
    main()
