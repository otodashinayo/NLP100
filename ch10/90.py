
def main():
    from os import path, listdir, mkdir
    import xml.etree.ElementTree as et
    import pandas as pd
    import MeCab
    from collections import Counter
    from itertools import chain
    import json

    dp = "kftt-moses-1.4/orig"

    tagger = MeCab.Tagger("-Owakati")
    df = pd.DataFrame()
    for dp_category in listdir(path.join(path.dirname(path.abspath(__file__)), dp)):
        if path.isdir(path.join(path.dirname(path.abspath(__file__)), dp, dp_category)):
            for fp in listdir(path.join(path.dirname(path.abspath(__file__)), dp, dp_category)):
                try:
                    art = et.parse(path.join(path.dirname(
                        path.abspath(__file__)), dp, dp_category, fp)).getroot()
                    for par in art.findall("par"):
                        for sen in par.findall("sen"):
                            j = tagger.parse(
                                sen.find("j").text).replace("\n", "")
                            e = sen.find("e").text
                            df = df.append({"j": j, "e": e}, ignore_index=True)
                except:
                    pass

    print(df.head())

    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "90")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "90"))
    df = df.sample(frac=1, random_state=0)
    df_train = df[:int(len(df) * 0.8)]
    df_train.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "90/train.csv"))
    df_valid = df[int(len(df) * 0.8):int(len(df) * 0.9)]
    df_valid.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "90/valid.csv"))
    df_test = df[int(len(df) * 0.9):]
    df_test.to_csv(path.join(path.dirname(
        path.abspath(__file__)), "90/test.csv"))

    words_j = chain.from_iterable(
        [str(j).split() for j in df_train["j"]])
    word_ids_j = {word: i + 1 for i, (word, count) in enumerate(
        Counter(words_j).most_common()) if count >= 2}
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "90")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "90"))
    json.dump(word_ids_j, open(path.join(path.dirname(
        path.abspath(__file__)), "90/word_ids_j.json"), "w"))

    words_e = chain.from_iterable(
        [str(e).split() for e in df_train["e"]])
    word_ids_e = {word: i + 1 for i, (word, count) in enumerate(
        Counter(words_e).most_common()) if count >= 2}
    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "90")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "90"))
    json.dump(word_ids_e, open(path.join(path.dirname(
        path.abspath(__file__)), "90/word_ids_e.json"), "w"))

    def sentence_to_ids_j(s):
        return [word_ids_j[w] if w in word_ids_j.keys() else 0 for w in s.split()]

    def sentence_to_ids_e(s):
        return [word_ids_e[w] if w in word_ids_e.keys() else 0 for w in s.split()]

    print(df_train.loc[0, "j"])
    print(sentence_to_ids_j(df_train.loc[0, "j"]))
    print(df_train.loc[0, "e"])
    print(sentence_to_ids_e(df_train.loc[0, "e"]))


if __name__ == "__main__":
    main()
