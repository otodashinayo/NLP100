def main():
    from os import path, mkdir
    from gensim.models import KeyedVectors
    import json

    fp_model = "GoogleNews-vectors-negative300.bin"
    fp_data = "questions-words.txt"
    model = KeyedVectors.load_word2vec_format(
        path.join(path.dirname(path.abspath(__file__)), fp_model), binary=True)
    with open(path.join(path.dirname(path.abspath(__file__)), fp_data), "r") as f:
        s = f.readlines()
    s = [t.replace("\n", "") for t in s]
    s = [t.split(" ") if t[0] != ":" else t for t in s]
    for t in s:
        if t[0] != ":":
            most_similar = model.most_similar(
                positive=[t[1], t[2]], negative=[t[0]], topn=1)[0]
            t.extend(most_similar)
        print(t)
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "64")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "64"))
    json.dump(s, open(path.join(path.dirname(
        path.abspath(__file__)), "64/data.json"), "w"))


if __name__ == "__main__":
    main()
