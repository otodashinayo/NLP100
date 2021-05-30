def main():
    from os import path
    import pandas as pd
    import pickle
    from sklearn.metrics import confusion_matrix

    fp_train = "51/train.feature.txt"
    fp_valid = "51/valid.feature.txt"
    fp_model = "52/model.pkl"
    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), sep="\t", index_col=0)
    df_valid = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_valid), sep="\t", index_col=0)
    model = pickle.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_model), "rb"))
    X_train, y_train = df_train.loc[:, df_train.columns.drop(
        "_CATEGORY")], df_train.loc[:, "_CATEGORY"]
    X_valid, y_valid = df_valid.loc[:, df_valid.columns.drop(
        "_CATEGORY")], df_valid.loc[:, "_CATEGORY"]
    y_pred_train = model.predict(X_train)
    y_pred_valid = model.predict(X_valid)
    confusion_train = confusion_matrix(y_train, y_pred_train)
    confusion_valid = confusion_matrix(y_valid, y_pred_valid)
    print(f"train")
    print(confusion_train)
    print()
    print(f"valid")
    print(confusion_valid)
    print()


if __name__ == "__main__":
    main()
