def main():
    from os import path
    import pandas as pd
    from gensim.models import KeyedVectors
    from sklearn.cluster import KMeans
    from sklearn.manifold import TSNE
    import matplotlib.pyplot as plt

    fp_data = "country_list.csv"
    fp_model = "GoogleNews-vectors-negative300.bin"
    df = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_data), index_col=0)
    model = KeyedVectors.load_word2vec_format(
        path.join(path.dirname(path.abspath(__file__)), fp_model), binary=True)
    for i in df.index:
        vec = model[df.loc[i, "COUNTRY"]]
        df.loc[i, range(300)] = vec
        print(df.loc[i, "COUNTRY"])
    model_clf = KMeans(n_clusters=5, random_state=0)
    df["CLUSTER"] = model_clf.fit_predict(df[range(300)])
    model_tsne = TSNE(random_state=0)
    df[["X", "Y"]] = model_tsne.fit_transform(df[range(300)])
    for cluster in range(5):
        plt.scatter(df[df["CLUSTER"] == cluster]["X"],
                    df[df["CLUSTER"] == cluster]["Y"])
    for i in df.index:
        plt.text(df.loc[i, "X"], df.loc[i, "Y"], df.loc[i, "COUNTRY"])
    plt.pause(5)


if __name__ == "__main__":
    main()
