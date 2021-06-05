def main():
    from os import path
    import pandas as pd
    import torch
    from torch import tensor, nn
    from torch.utils.data import DataLoader
    from torch.optim import SGD
    import matplotlib.pyplot as plt
    from time import time

    fp_train = "70/train.csv"
    fp_valid = "70/valid.csv"
    batch_sizes = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512]
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

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

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

    times = []

    for batch_size in batch_sizes:
        dataset_train = [(X_i, y_i) for X_i, y_i in zip(X_train, y_train)]
        dataloader_train = DataLoader(dataset_train, batch_size=batch_size)
        dataset_valid = [(X_i, y_i) for X_i, y_i in zip(X_valid, y_valid)]
        dataloader_valid = DataLoader(dataset_valid, batch_size=batch_size)

        model = Model().to(device)
        loss_fn = nn.CrossEntropyLoss()
        optimizer = SGD(model.parameters(), lr=learning_rate)

        start_time = time()

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

            size = len(dataloader_train.dataset)
            loss, correct = 0, 0
            with torch.no_grad():
                for X, y in dataloader_train:
                    X, y = X.to(device), y.to(device)
                    pred = model(X)
                    loss += loss_fn(pred, y).item()
                    correct += (pred.argmax(1) ==
                                y).type(torch.float).sum().item()
            loss /= size
            correct /= size

            size = len(dataloader_valid.dataset)
            loss, correct = 0, 0
            with torch.no_grad():
                for X, y in dataloader_valid:
                    X, y = X.to(device), y.to(device)
                    pred = model(X)
                    loss += loss_fn(pred, y).item()
                    correct += (pred.argmax(1) ==
                                y).type(torch.float).sum().item()
            loss /= size
            correct /= size
            print(
                f"Valid Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {loss:>8f} \n")

        end_time = time()
        times.append((end_time - start_time) / 10)

    plt.plot(batch_sizes, times)
    plt.xlabel("Batch Size")
    plt.ylabel("Time")
    plt.xscale("log")
    plt.show()


if __name__ == "__main__":
    main()
