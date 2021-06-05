def main():
    from os import path
    import pandas as pd
    from torch import tensor, nn

    fp_train = "70/train.csv"

    class Model(nn.Module):
        def __init__(self):
            super().__init__()
            self.linear = nn.Linear(300, 4, bias=False)
            self.softmax = nn.Softmax(dim=1)

        def forward(self, x):
            y = self.linear(x)
            y = self.softmax(y)
            return y

    df_train = pd.read_csv(path.join(path.dirname(path.abspath(__file__)), fp_train), index_col=0)

    X_train = tensor(df_train[[str(r) for r in range(300)]].values.astype("float32"))
    y_train = tensor(df_train["CATEGORY"].values.astype("int"))
    
    model = Model()
    loss_fn = nn.CrossEntropyLoss()

    loss = loss_fn(model(X_train)[0:1], y_train[0:1])
    loss.backward()
    grad = model.linear.weight.grad

    print(f"loss: {loss}")
    print(f"grad: {grad}")
    
    loss = loss_fn(model(X_train)[0:4], y_train[0:4])
    loss.backward()
    grad = model.linear.weight.grad

    print(f"loss: {loss}")
    print(f"grad: {grad}")
    
if __name__ == "__main__":
    main()
