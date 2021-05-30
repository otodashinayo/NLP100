def main():
    from os import path
    import pandas as pd
    import pickle
    from operator import itemgetter
    from pprint import pprint

    fp_train = "51/train.feature.txt"
    fp_model = "52/model.pkl"
    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), sep="\t", index_col=0)
    model = pickle.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_model), "rb"))
    weights_b = sorted([(variable, weight) for variable, weight in zip(
        df_train.columns.drop("_CATEGORY"), model.coef_[0])], key=itemgetter(1), reverse=True)
    weights_t = sorted([(variable, weight) for variable, weight in zip(
        df_train.columns.drop("_CATEGORY"), model.coef_[1])], key=itemgetter(1), reverse=True)
    weights_e = sorted([(variable, weight) for variable, weight in zip(
        df_train.columns.drop("_CATEGORY"), model.coef_[2])], key=itemgetter(1), reverse=True)
    weights_m = sorted([(variable, weight) for variable, weight in zip(
        df_train.columns.drop("_CATEGORY"), model.coef_[3])], key=itemgetter(1), reverse=True)
    print("b best features")
    pprint(weights_b[:10])
    print()
    print("b worst1 features")
    pprint(weights_b[-10:])
    print()
    print("t best features")
    pprint(weights_t[:10])
    print()
    print("t worst1 features")
    pprint(weights_t[-10:])
    print()
    print("e best features")
    pprint(weights_e[:10])
    print()
    print("e worst1 features")
    pprint(weights_e[-10:])
    print()
    print("m best features")
    pprint(weights_m[:10])
    print()
    print("m worst1 features")
    pprint(weights_m[-10:])
    print()


if __name__ == "__main__":
    main()
