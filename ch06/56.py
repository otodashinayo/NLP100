def main():
    from os import path
    import pandas as pd
    import pickle
    from sklearn.metrics import precision_score, recall_score, f1_score

    fp_valid = "51/valid.feature.txt"
    fp_model = "52/model.pkl"
    df_valid = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_valid), sep="\t", index_col=0)
    model = pickle.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_model), "rb"))
    X_valid, y_valid = df_valid.loc[:, df_valid.columns.drop(
        "_CATEGORY")], df_valid.loc[:, "_CATEGORY"]
    y_pred_valid = model.predict(X_valid)
    precision_micro_valid = precision_score(
        y_valid, y_pred_valid, average="micro")
    recall_micro_valid = recall_score(y_valid, y_pred_valid, average="micro")
    f1_micro_valid = f1_score(y_valid, y_pred_valid, average="micro")
    precision_macro_valid = precision_score(
        y_valid, y_pred_valid, average="macro")
    recall_macro_valid = recall_score(y_valid, y_pred_valid, average="macro")
    f1_macro_valid = f1_score(y_valid, y_pred_valid, average="macro")
    print(f"precision micro")
    print(precision_micro_valid)
    print()
    print(f"recall micro")
    print(recall_micro_valid)
    print()
    print(f"f1 micro")
    print(f1_micro_valid)
    print()
    print(f"precision macro")
    print(precision_macro_valid)
    print()
    print(f"recall macro")
    print(recall_macro_valid)
    print()
    print(f"f1 macro")
    print(f1_macro_valid)
    print()


if __name__ == "__main__":
    main()
