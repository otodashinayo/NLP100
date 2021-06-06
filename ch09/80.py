def main():
    from os import path, mkdir
    import pandas as pd
    from collections import Counter
    from itertools import chain
    import json

    fp = "NewsAggregatorDataset/newsCorpora.csv"

    df = pd.read_csv(path.join(path.dirname(path.abspath(__file__)), fp), sep="\t", index_col=0, names=[
                     "ID", "TITLE", "URL", "PUBLISHER", "CATEGORY", "STORY", "HOSTNAME", "TIMESTAMP"])
    df = df[df["PUBLISHER"].isin(
        ["Reuters", "Huffington Post", "Businessweek", "Contactmusic.com", "Daily Mail"])]
    df["CATEGORY"] = df["CATEGORY"].replace({"b": 0, "t": 1, "e": 2, "m": 3})

    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "80")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "80"))
    df = df.sample(frac=1, random_state=0)
    df_train = df[:int(len(df) * 0.8)]
    df_train.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "80/train.csv"))
    df_valid = df[int(len(df) * 0.8):int(len(df) * 0.9)]
    df_valid.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "80/valid.csv"))
    df_test = df[int(len(df) * 0.9):]
    df_test.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "80/test.csv"))

    words_in_title = chain.from_iterable(
        [title.split() for title in df_train["TITLE"]])
    word_ids = {word: i + 1 for i, (word, count) in enumerate(
        Counter(words_in_title).most_common()) if count >= 2}
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "80")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "80"))
    json.dump(word_ids, open(path.join(path.dirname(
        path.abspath(__file__)), "80/word_ids.json"), "w"))

    def title_to_ids(t):
        return [word_ids[w] if w in word_ids.keys() else 0 for w in t.split()]

    print(title_to_ids("Europe reaches crunch point on banking union"))


if __name__ == "__main__":
    main()
