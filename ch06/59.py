def main():
    from os import path
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    from pprint import pprint

    fp_train = "51/train.feature.txt"
    fp_valid = "51/valid.feature.txt"
    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), sep="\t", index_col=0)
    df_valid = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_valid), sep="\t", index_col=0)
    X_train, y_train = df_train.loc[:, df_train.columns.drop(
        "_CATEGORY")], df_train.loc[:, "_CATEGORY"]
    X_valid, y_valid = df_valid.loc[:, df_valid.columns.drop(
        "_CATEGORY")], df_valid.loc[:, "_CATEGORY"]
    cs = np.logspace(-2, 2, 10)
    best_model = None
    best_accuracy_valid = 0
    for c in cs:
        model = LogisticRegression(C=c, random_state=0, max_iter=1000)
        model.fit(X_train, y_train)
        y_pred_valid = model.predict(X_valid)
        accuracy_valid = accuracy_score(y_valid, y_pred_valid)
        if accuracy_valid > best_accuracy_valid:
            best_accuracy_valid = accuracy_valid
            best_model = model
        print(
            f"C: {c}, valid: {accuracy_valid}")
    print("param")
    pprint(best_model.get_params())
    print()
    print("accuracy_valid")
    print(best_accuracy_valid)
    print()


if __name__ == "__main__":
    main()
