def main():
    from os import path
    import pandas as pd
    from gensim.models import KeyedVectors
    from scipy.cluster.hierarchy import dendrogram, linkage
    from pprint import pprint
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
    model_clf = linkage(df[range(300)], method="ward")
    pprint(model_clf[:5])
    dendrogram(model_clf)
    plt.pause(5)


if __name__ == "__main__":
    main()
