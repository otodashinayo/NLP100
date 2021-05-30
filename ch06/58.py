def main():
    from os import path
    import pandas as pd
    import numpy as np
    from sklearn.linear_model import LogisticRegression
    from sklearn.metrics import accuracy_score
    import matplotlib.pyplot as plt

    fp_train = "51/train.feature.txt"
    fp_valid = "51/valid.feature.txt"
    fp_test = "51/test.feature.txt"
    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), sep="\t", index_col=0)
    df_valid = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_valid), sep="\t", index_col=0)
    df_test = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_test), sep="\t", index_col=0)
    X_train, y_train = df_train.loc[:, df_train.columns.drop(
        "_CATEGORY")], df_train.loc[:, "_CATEGORY"]
    X_valid, y_valid = df_valid.loc[:, df_valid.columns.drop(
        "_CATEGORY")], df_valid.loc[:, "_CATEGORY"]
    X_test, y_test = df_test.loc[:, df_test.columns.drop(
        "_CATEGORY")], df_test.loc[:, "_CATEGORY"]
    cs = np.logspace(-2, 2, 10)
    accuracy_trains = []
    accuracy_valids = []
    accuracy_tests = []
    for c in cs:
        model = LogisticRegression(C=c, random_state=0, max_iter=1000)
        model.fit(X_train, y_train)
        y_pred_train = model.predict(X_train)
        y_pred_valid = model.predict(X_valid)
        y_pred_test = model.predict(X_test)
        accuracy_train = accuracy_score(y_train, y_pred_train)
        accuracy_valid = accuracy_score(y_valid, y_pred_valid)
        accuracy_test = accuracy_score(y_test, y_pred_test)
        accuracy_trains.append(accuracy_train)
        accuracy_valids.append(accuracy_valid)
        accuracy_tests.append(accuracy_test)
        print(
            f"C: {c}, train: {accuracy_train}, valid: {accuracy_valid}, test: {accuracy_test}")
    plt.plot(cs, accuracy_trains, label="train")
    plt.plot(cs, accuracy_valids, label="valid")
    plt.plot(cs, accuracy_tests, label="test")
    plt.xscale("log")
    plt.legend()
    plt.pause(5)


if __name__ == "__main__":
    main()
