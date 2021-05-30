def main():
    from os import path
    import pandas as pd
    import pickle

    def f(title):
        df = pd.DataFrame(0, index=[0], columns=df_train.columns)
        for word in title.split():
            if word in df.columns:
                df.loc[0, word] += 1
        X_train = df.loc[:, df.columns.drop("_CATEGORY")]
        y_pred = {0: "b", 1: "t", 2: "e", 3: "m"}[model.predict(X_train)[0]]
        probabilities = {category: proba for category, proba in zip(
            ["b", "t", "e", "m"], model.predict_proba(X_train)[0])}
        return y_pred, probabilities

    fp_train = "51/train.feature.txt"
    fp_model = "52/model.pkl"
    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), sep="\t", index_col=0)
    model = pickle.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_model), "rb"))
    y_pred, probabilities = f(
        "RPT-Fitch Updates EMEA Consumer ABS Rating Criteria & Auto Residual Value  ...")
    print(f"y_pred: {y_pred}")
    print(f"probabilities: {probabilities}")


if __name__ == "__main__":
    main()
