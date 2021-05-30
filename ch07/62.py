def main():
    from os import path
    from gensim.models import KeyedVectors
    from pprint import pprint

    fp = "GoogleNews-vectors-negative300.bin"
    model = KeyedVectors.load_word2vec_format(
        path.join(path.dirname(path.abspath(__file__)), fp), binary=True)
    pprint(model.most_similar(positive=["United_States"], topn=10))


if __name__ == "__main__":
    main()
