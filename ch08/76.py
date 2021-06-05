def main():
    from os import path, mkdir
    import pandas as pd
    import torch
    from torch import tensor, nn
    from torch.utils.data import DataLoader
    from torch.optim import SGD

    fp_train = "70/train.csv"
    fp_valid = "70/valid.csv"
    batch_size = 1
    learning_rate = 0.001

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(300, 4, bias=False)
            self.softmax = nn.Softmax(dim=1)

        def forward(self, x):
            y = self.linear(x)
            y = self.softmax(y)
            return y

    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), index_col=0)
    df_valid = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_valid), index_col=0)

    X_train = tensor(df_train[[str(r)
                     for r in range(300)]].values.astype("float32"))
    y_train = tensor(df_train["CATEGORY"].values.astype("int"))
    X_valid = tensor(df_valid[[str(r)
                     for r in range(300)]].values.astype("float32"))
    y_valid = tensor(df_valid["CATEGORY"].values.astype("int"))

    dataset_train = [(X_i, y_i) for X_i, y_i in zip(X_train, y_train)]
    dataloader_train = DataLoader(dataset_train, batch_size=batch_size)
    dataset_valid = [(X_i, y_i) for X_i, y_i in zip(X_valid, y_valid)]
    dataloader_valid = DataLoader(dataset_valid, batch_size=batch_size)

    model = Model()
    loss_fn = nn.CrossEntropyLoss()
    optimizer = SGD(model.parameters(), lr=learning_rate)

    loss_train = []
    correct_train = []
    loss_valid = []
    correct_valid = []

    for epoch in range(100):
        print(f"Epoch {epoch + 1}\n-------------------------------")
        size = len(dataloader_train.dataset)
        for batch, (X, y) in enumerate(dataloader_train):
            loss = loss_fn(model(X), y)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            if batch % 1000 == 0:
                loss, current = loss.item(), batch * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")

        size = len(dataloader_train.dataset)
        loss, correct = 0, 0
        with torch.no_grad():
            for X, y in dataloader_train:
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
                pred = model(X)
                loss += loss_fn(pred, y).item()
                correct += (pred.argmax(1) == y).type(torch.float).sum().item()
        loss /= size
        correct /= size
        loss_valid.append(loss)
        correct_valid.append(correct)
        print(
            f"Valid Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {loss:>8f} \n")

        if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "76")):
            mkdir(path.join(path.dirname(path.abspath(__file__)), "76"))
        torch.save({"epoch": epoch, "model": model.state_dict(), "optim": optimizer.state_dict(
        )}, path.join(path.dirname(path.abspath(__file__)), f"76/model_{epoch}.pth"))


if __name__ == "__main__":
    main()
