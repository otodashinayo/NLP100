def main():
    from os import path
    from gensim.models import KeyedVectors

    fp = "GoogleNews-vectors-negative300.bin"
    model = KeyedVectors.load_word2vec_format(
        path.join(path.dirname(path.abspath(__file__)), fp), binary=True)
    print(model.similarity("United_States", "U.S."))


if __name__ == "__main__":
    main()
