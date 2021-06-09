
def main():
    from os import path, mkdir
    import pandas as pd
    import json
    import torch
    from torch import tensor, nn
    from torch.utils.data import DataLoader
    from torch.optim import SGD
    from torch.optim.lr_scheduler import ExponentialLR

    fp_train = "90/train.csv"
    fp_valid = "90/valid.csv"
    fp_word_ids_j = "90/word_ids_j.json"
    fp_word_ids_e = "90/word_ids_e.json"
    batch_size = 1
    embedding_dim = 300
    hidden_size = 50
    learning_rate = 0.01

    df_train = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_train), index_col=0)

    word_ids_j = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_word_ids_j), "r"))
    word_ids_e = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_word_ids_e), "r"))

    def sentence_to_ids_j(s):
        return [word_ids_j[w] if w in word_ids_j.keys() else 0 for w in s.split()]

    def sentence_to_ids_e(s):
        return [word_ids_e[w] if w in word_ids_e.keys() else 0 for w in s.split()]

    X_train = nn.utils.rnn.pad_sequence(
        [tensor(sentence_to_ids_j(str(j))) for j in df_train["j"]], batch_first=True)
    Y_train = nn.utils.rnn.pad_sequence(
        [tensor(sentence_to_ids_e(str(e))) for e in df_train["e"]], batch_first=True)

    dataset_train = [(X_i, Y_i) for X_i, Y_i in zip(X_train, Y_train)]
    dataloader_train = DataLoader(dataset_train, batch_size=batch_size)

    class Encoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(
                len(word_ids_j) + 1, embedding_dim, padding_idx=0)
            self.rnn = nn.RNN(embedding_dim, hidden_size, batch_first=True)
            self.softmax = nn.Softmax(dim=1)

        def forward(self, x, hidden):
            y = self.embedding(x)
            output, hidden = self.rnn(y, hidden)
            output = self.softmax(output)
            return output, hidden

    class Decoder(nn.Module):
        def __init__(self):
            super().__init__()
            self.embedding = nn.Embedding(
                len(word_ids_e) + 1, embedding_dim, padding_idx=0)
            self.rnn = nn.RNN(embedding_dim, hidden_size, batch_first=True)
            self.linear = nn.Linear(hidden_size, len(word_ids_e) + 1)
            self.softmax = nn.Softmax(dim=1)

        def forward(self, x, hidden):
            y = self.embedding(x)
            output, hidden = self.rnn(y, hidden)
            output = self.linear(output)
            output = self.softmax(output)
            return output, hidden

    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"Device: {device}")

    encoder = Encoder().to(device)
    decoder = Decoder().to(device)
    loss_fn = nn.CrossEntropyLoss()
    encoder_optimizer = SGD(encoder.parameters(), lr=learning_rate)
    decoder_optimizer = SGD(decoder.parameters(), lr=learning_rate)
    encoder_scheduler = ExponentialLR(encoder_optimizer, gamma=0.9)
    decoder_scheduler = ExponentialLR(decoder_optimizer, gamma=0.9)

    for epoch in range(10):
        print(f"Epoch {epoch + 1}\n-------------------------------")
        size = len(dataloader_train.dataset)
        for batch, (X, Y) in enumerate(dataloader_train):
            X, Y = X.to(device), Y.to(device)
            encoder_output, encoder_hidden = encoder(X, None)
            decoder_output, decoder_hidden = decoder(Y[:, :-1], encoder_hidden)
            loss = 0
            for i in range(decoder_output.size(1)):
                loss += loss_fn(decoder_output[:, i], Y[:, i + 1])
            loss.backward()
            encoder_optimizer.step()
            decoder_optimizer.step()
            if batch % 1000 == 0:
                loss, current = loss.item(), batch * len(X)
                print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")
        encoder_scheduler.step()
        decoder_scheduler.step()

    if not path.isdir(path.join(path.dirname(path.abspath(__file__)), "91")):
        mkdir(path.join(path.dirname(path.abspath(__file__)), "91"))
    torch.save(encoder.state_dict(), path.join(
        path.dirname(path.abspath(__file__)), "91/encoder.pth"))
    torch.save(decoder.state_dict(), path.join(
        path.dirname(path.abspath(__file__)), "91/decoder.pth"))


if __name__ == "__main__":
    main()
