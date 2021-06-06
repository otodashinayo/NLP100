def main():
    from os import path
    import pandas as pd
    import json
    import torch
    from torch import tensor, nn
    from torch.utils.data import DataLoader

    fp_train = "80/train.csv"
    fp_words = "80/word_ids.json"
    batch_size = 1
    embedding_dim = 300
    hidden_size = 50

    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), index_col=0)
    word_ids = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_words), "r"))

    def title_to_ids(t):
        return [word_ids[w] if w in word_ids.keys() else 0 for w in t.split()]

    X_train = nn.utils.rnn.pad_sequence(
        [tensor(title_to_ids(title)) for title in df_train["TITLE"]], batch_first=True)
    y_train = tensor(df_train["CATEGORY"].values.astype("int"))

    dataset_train = [(X_i, y_i) for X_i, y_i in zip(X_train, y_train)]
    dataloader_train = DataLoader(dataset_train, batch_size=batch_size)

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(
                len(word_ids) + 1, embedding_dim, padding_idx=0)
            self.rnn = nn.RNN(embedding_dim, hidden_size, batch_first=True)
            self.linear = nn.Linear(hidden_size, 4)
            self.softmax = nn.Softmax(dim=1)

        def forward(self, x):
            hidden = torch.zeros(1, x.size(0), hidden_size).to(device)
            y = self.embedding(x)
            y, hidden = self.rnn(y, hidden)
            y = self.linear(y[:, -1, :])
            y = self.softmax(y)
            return y

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    model = Model().to(device)
    for batch, (inputs, targets) in enumerate(dataloader_train):
        if batch < 5:
            print(batch, model(inputs))
        else:
            break


if __name__ == "__main__":
    main()
