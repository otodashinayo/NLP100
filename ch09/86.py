def main():
    from os import path
    import pandas as pd
    import json
    from torch import tensor, nn
    from torch.utils.data import DataLoader

    fp_train = "80/train.csv"
    fp_words = "80/word_ids.json"
    batch_size = 1
    embedding_dim = 300
    hidden_size = 50
    kernel_size = 3
    stride = 1
    padding = 1

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
            self.conv2d = nn.Conv2d(1, out_channels=hidden_size, kernel_size=(
                kernel_size, embedding_dim), stride=stride, padding=(padding, 0))
            self.relu = nn.ReLU()
            self.maxpool1d = nn.MaxPool1d(X_train.size(1))
            self.linear = nn.Linear(hidden_size, 4)
            self.softmax = nn.Softmax(dim=1)

        def forward(self, x):
            y = self.embedding(x)
            y = self.conv2d(y.unsqueeze(1))
            y = self.relu(y.squeeze(3))
            y = self.maxpool1d(y)
            y = self.linear(y.squeeze(2))
            y = self.softmax(y)
            return y

    model = Model()
    for batch, (inputs, targets) in enumerate(dataloader_train):
        if batch < 5:
            print(batch, model(inputs))
        else:
            break


if __name__ == "__main__":
    main()
