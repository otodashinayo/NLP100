def main():
    from os import path, mkdir
    from gensim.models import KeyedVectors
    import pandas as pd
    import numpy as np

    fp_model = "GoogleNews-vectors-negative300.bin"
    fp_data = "NewsAggregatorDataset/newsCorpora.csv"

    model = KeyedVectors.load_word2vec_format(
        path.join(path.dirname(path.abspath(__file__)), fp_model), binary=True)
    df = pd.read_csv(path.join(path.dirname(path.abspath(__file__)), fp_data), sep="\t", index_col=0, names=[
                     "ID", "TITLE", "URL", "PUBLISHER", "CATEGORY", "STORY", "HOSTNAME", "TIMESTAMP"])
    df = df[df["PUBLISHER"].isin(
        ["Reuters", "Huffington Post", "Businessweek", "Contactmusic.com", "Daily Mail"])]

    def emb(w):
        try:
            return model[w]
        except:
            return np.zeros(300)

    df[[str(i) for i in range(300)]] = np.array([np.array([emb(word)
                                                           for word in df.loc[i, "TITLE"].split()]).mean(axis=0) for i in df.index])
    df["CATEGORY"] = df["CATEGORY"].replace({"b": 0, "t": 1, "e": 2, "m": 3})

    print(df.head())

    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "70")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "70"))
    df = df.sample(frac=1, random_state=0)
    df_train = df[:int(len(df) * 0.8)]
    df_train.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "70/train.csv"))
    df_valid = df[int(len(df) * 0.8):int(len(df) * 0.9)]
    df_valid.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "70/valid.csv"))
    df_test = df[int(len(df) * 0.9):]
    df_test.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "70/test.csv"))


if __name__ == "__main__":
    main()
