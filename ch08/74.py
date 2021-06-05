def main():
    from os import path
    import pandas as pd
    import torch
    from torch import tensor, nn
    from torch.utils.data import DataLoader

    fp_train = "70/train.csv"
    fp_test = "70/test.csv"
    fp_model = "73/model.pth"
    batch_size = 1

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
    df_test = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_test), index_col=0)

    X_train = tensor(df_train[[str(r)
                     for r in range(300)]].values.astype("float32"))
    y_train = tensor(df_train["CATEGORY"].values.astype("int"))
    X_test = tensor(df_test[[str(r)
                             for r in range(300)]].values.astype("float32"))
    y_test = tensor(df_test["CATEGORY"].values.astype("int"))

    dataset_train = [(X_i, y_i) for X_i, y_i in zip(X_train, y_train)]
    dataloader_train = DataLoader(dataset_train, batch_size=batch_size)
    dataset_test = [(X_i, y_i) for X_i, y_i in zip(X_test, y_test)]
    dataloader_test = DataLoader(dataset_test, batch_size=batch_size)

    model = Model()
    model.load_state_dict(torch.load(
        path.join(path.dirname(path.abspath(__file__)), fp_model)))
    loss_fn = nn.CrossEntropyLoss()

    size = len(dataloader_train.dataset)
    loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader_train:
            pred = model(X)
            loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    loss /= size
    correct /= size
    print(
        f"Train Data\nTest Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {loss:>8f} \n")

    size = len(dataloader_test.dataset)
    loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader_test:
            pred = model(X)
            loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    loss /= size
    correct /= size
    print(
        f"Test Data\nTest Error: \n Accuracy: {(100 * correct):>0.1f}%, Avg loss: {loss:>8f} \n")


if __name__ == "__main__":
    main()
