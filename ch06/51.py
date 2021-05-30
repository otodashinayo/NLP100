def main():
    from os import path, mkdir
    import pandas as pd
    from pprint import pprint
    from itertools import chain
    from collections import Counter

    fp_train = "50/train.txt"
    fp_valid = "50/valid.txt"
    fp_test = "50/test.txt"
    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), sep="\t", index_col=0)
    df_valid = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_valid), sep="\t", index_col=0)
    df_test = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_test), sep="\t", index_col=0)
    words_in_title = chain.from_iterable(
        [title.split() for title in df_train["TITLE"]])
    common_words_in_title = [word for word, count in Counter(
        words_in_title).most_common(1000)]
    df_feature_train = pd.DataFrame(
        0, index=df_train.index, columns=common_words_in_title)
    for i in df_train.index:
        for word in df_train.loc[i, "TITLE"].split():
            if word in df_feature_train.columns:
                df_feature_train.loc[i, word] += 1
    df_feature_valid = pd.DataFrame(
        0, index=df_valid.index, columns=common_words_in_title)
    for i in df_valid.index:
        for word in df_valid.loc[i, "TITLE"].split():
            if word in df_feature_valid.columns:
                df_feature_valid.loc[i, word] += 1
    df_feature_test = pd.DataFrame(
        0, index=df_test.index, columns=common_words_in_title)
    for i in df_test.index:
        for word in df_test.loc[i, "TITLE"].split():
            if word in df_feature_test.columns:
                df_feature_test.loc[i, word] += 1
    df_feature_train["_CATEGORY"] = df_train["CATEGORY"].replace(
        {"b": 0, "t": 1, "e": 2, "m": 3})
    df_feature_valid["_CATEGORY"] = df_valid["CATEGORY"].replace(
        {"b": 0, "t": 1, "e": 2, "m": 3})
    df_feature_test["_CATEGORY"] = df_test["CATEGORY"].replace(
        {"b": 0, "t": 1, "e": 2, "m": 3})
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "51")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "51"))
    df_feature_train.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "51/train.feature.txt"), sep="\t")
    df_feature_valid.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "51/valid.feature.txt"), sep="\t")
    df_feature_test.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "51/test.feature.txt"), sep="\t")
    pprint(df_feature_train.head())


if __name__ == "__main__":
    main()
