def main():
    from os import path
    import pandas as pd
    from gensim.models import KeyedVectors
    from scipy.stats import spearmanr

    fp_data = "wordsim353/combined.csv"
    fp_model = "GoogleNews-vectors-negative300.bin"
    df = pd.read_csv(path.join(path.dirname(path.abspath(__file__)), fp_data))
    model = KeyedVectors.load_word2vec_format(
        path.join(path.dirname(path.abspath(__file__)), fp_model), binary=True)
    for i in df.index:
        similarity = model.similarity(df.loc[i, "Word 1"], df.loc[i, "Word 2"])
        df.loc[i, "Model"] = similarity
        print(df.loc[i, "Word 1"], df.loc[i, "Word 2"], similarity)
    df["Human lank"] = df["Human (mean)"].rank(ascending=False)
    df["Model lank"] = df["Model"].rank(ascending=False)
    print(spearmanr(df["Human lank"], df["Model lank"]))


if __name__ == "__main__":
    main()
