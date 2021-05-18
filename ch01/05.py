def n_gram(s, n):
    res = []
    for i in range(len(s) + 1 - n):
        res.append(s[i:i + n])
    return res


def main():
    s = "I am an NLPer"
    word_bi_gram = n_gram(s.split(), 2)
    print(f"word bi-gram: {word_bi_gram}")
    char_bi_gram = n_gram(s, 2)
    print(f"char bi-gram: {char_bi_gram}")


if __name__ == "__main__":
    main()
