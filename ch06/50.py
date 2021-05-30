def main():
    from os import path, mkdir
    import pandas as pd
    from pprint import pprint

    fp = "NewsAggregatorDataset/newsCorpora.csv"
    names = ["ID", "TITLE", "URL", "PUBLISHER",
             "CATEGORY", "STORY", "HOSTNAME", "TIMESTAMP"]
    df = pd.read_csv(path.join(path.dirname(path.abspath(
        __file__)), fp), sep="\t", index_col=0, names=names)
    df = df[(df["PUBLISHER"] == "Reuters") | (df["PUBLISHER"] == "Huffington Post") | (df["PUBLISHER"]
                                                                                       == "Businessweek") | (df["PUBLISHER"] == "Contactmusic.com") | (df["PUBLISHER"] == "Daily Mail")]
    df = df.sample(frac=1, random_state=0)
    df_train = df[:int(len(df) * 0.8)]
    df_valid = df[int(len(df) * 0.8):int(len(df) * 0.9)]
    df_test = df[int(len(df) * 0.9):]
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "50")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "50"))
    df_train.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "50/train.txt"), sep="\t")
    df_valid.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "50/valid.txt"), sep="\t")
    df_test.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "50/test.txt"), sep="\t")
    print("train")
    pprint(df_train["CATEGORY"].value_counts())
    print()
    print("valid")
    pprint(df_valid["CATEGORY"].value_counts())
    print()


if __name__ == "__main__":
    main()
