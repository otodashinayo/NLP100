def main():
    s = "Now I need a drink, alcoholic of course, after the heavy lectures involving quantum mechanics."
    s = s.replace(",", "").replace(".", "")
    res = [len(t) for t in s.split()]
    print(res)


if __name__ == "__main__":
    main()
