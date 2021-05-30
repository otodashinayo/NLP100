def main():
    from os import path, mkdir
    import pandas as pd
    from sklearn.linear_model import LogisticRegression
    import pickle

    fp_train = "51/train.feature.txt"
    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), sep="\t", index_col=0)
    X_train, y_train = df_train.loc[:, df_train.columns.drop(
        "_CATEGORY")], df_train.loc[:, "_CATEGORY"]
    model = LogisticRegression(random_state=0, max_iter=1000)
    model.fit(X_train, y_train)
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "52")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "52"))
    pickle.dump(model, open(path.join(path.dirname(
        path.abspath(__file__)), "52/model.pkl"), "wb"))


if __name__ == "__main__":
    main()
