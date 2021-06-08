def main():
    from os import path
    import pandas as pd
    import json
    import torch
    from torch import tensor, nn
    from torch.utils.data import DataLoader
    from torch.optim import SGD
    from torch.optim.lr_scheduler import ExponentialLR
    import matplotlib.pyplot as plt

    fp_train = "80/train.csv"
    fp_valid = "80/valid.csv"
    fp_words = "80/word_ids.json"
    batch_size = 1
    embedding_dim = 300
    hidden_size = 50
    learning_rate = 0.001

    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), index_col=0)
    df_valid = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_valid), index_col=0)
    word_ids = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_words), "r"))

    def title_to_ids(t):
        return [word_ids[w] if w in word_ids.keys() else 0 for w in t.split()]

    X_train = nn.utils.rnn.pad_sequence(
        [tensor(title_to_ids(title)) for title in df_train["TITLE"]], batch_first=True)
    y_train = tensor(df_train["CATEGORY"].values.astype("int"))
    X_valid = nn.utils.rnn.pad_sequence(
        [tensor(title_to_ids(title)) for title in df_valid["TITLE"]], batch_first=True)
    y_valid = tensor(df_valid["CATEGORY"].values.astype("int"))

    dataset_train = [(X_i, y_i) for X_i, y_i in zip(X_train, y_train)]
    dataloader_train = DataLoader(dataset_train, batch_size=batch_size)
    dataset_valid = [(X_i, y_i) for X_i, y_i in zip(X_valid, y_valid)]
    dataloader_valid = DataLoader(dataset_valid, batch_size=batch_size)

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(
                len(word_ids) + 1, embedding_dim, padding_idx=0)
            self.rnn = nn.RNN(embedding_dim, hidden_size, batch_first=True)
            self.linear = nn.Linear(hidden_size, 4)
            self.softmax = nn.Softmax(dim=1)

        def forward(self, x):
            y = self.embedding(x)
            y, hidden = self.rnn(y)
            y = self.linear(y[:, -1, :])
            y = self.softmax(y)
            return y

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    model = Model().to(device)
    loss_fn = nn.CrossEntropyLoss()
    optimizer = SGD(model.parameters(), lr=learning_rate)
    scheduler = ExponentialLR(optimizer, gamma=0.9)

    loss_train = []
    correct_train = []
    loss_valid = []
    correct_valid = []

    for epoch in range(10):
        print(f"Epoch {epoch + 1}\n-------------------------------")
        size = len(dataloader_train.dataset)
        for batch, (X, y) in enumerate(dataloader_train):
            X, y = X.to(device), y.to(device)
            loss = loss_fn(model(X), y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if batch % 1000 == 0:
                loss, current = loss.item(), batch * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
        scheduler.step()

        size = len(dataloader_train.dataset)
        loss, correct = 0, 0
        with torch.no_grad():
            for X, y in dataloader_train:
                X, y = X.to(device), y.to(device)
                pred = model(X)
                loss += loss_fn(pred, y).item()
                correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        loss /= size
        correct /= size
        loss_train.append(loss)
        correct_train.append(correct)

        size = len(dataloader_valid.dataset)
        loss, correct = 0, 0
        with torch.no_grad():
            for X, y in dataloader_valid:
                X, y = X.to(device), y.to(device)
                pred = model(X)
                loss += loss_fn(pred, y).item()
                correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        loss /= size
        correct /= size
        loss_valid.append(loss)
        correct_valid.append(correct)
        print(f"Valid Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {loss:>8f} \n")

    plt.subplot(211)
    plt.plot(loss_train, label="train")
    plt.plot(loss_valid, label="valid")
    plt.title("Loss")
    plt.legend()

    plt.subplot(212)
    plt.plot(correct_train, label="train")
    plt.plot(correct_valid, label="valid")
    plt.title("Accuracy")
    plt.legend()
    plt.show()


if __name__ == "__main__":
    main()
