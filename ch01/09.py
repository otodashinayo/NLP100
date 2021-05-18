def main():
    import random

    s = "I couldn’t believe that I could actually understand what I was reading : the phenomenal power of the human mind ."
    res = []
    for t in s.split():
        if len(t) > 4:
            res.append(t[0] + "".join(random.sample([u for u in t[1:-1]], len(t) - 2)) + t[-1])
        else:
            res.append(t)
    res = " ".join(res)
    print(res)


if __name__ == "__main__":
    main()
