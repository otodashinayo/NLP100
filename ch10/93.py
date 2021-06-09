
def main():
    from os import path
    import pandas as pd
    import json
    import torch
    from torch import tensor, nn
    from torch.utils.data import DataLoader
    from torchtext.data.metrics import bleu_score

    fp_test = "90/test.csv"
    fp_encoder = "91/encoder.pth"
    fp_decoder = "91/decoder.pth"
    fp_word_ids_j = "90/word_ids_j.json"
    fp_word_ids_e = "90/word_ids_e.json"
    batch_size = 1
    embedding_dim = 300
    hidden_size = 50

    df_test = pd.read_csv(path.join(path.dirname(
        path.abspath(__file__)), fp_test), index_col=0)

    word_ids_j = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_word_ids_j), "r"))
    word_ids_e = json.load(
        open(path.join(path.dirname(path.abspath(__file__)), fp_word_ids_e), "r"))
    id_words_e = {v: k for k, v in word_ids_e.items()}

    def sentence_to_ids_j(s):
        return [word_ids_j[w] if w in word_ids_j.keys() else 0 for w in s.split()]

    def sentence_to_ids_e(s):
        return [word_ids_e[w] if w in word_ids_e.keys() else 0 for w in s.split()]

    def ids_to_sentence_e(ids):
        return " ".join([id_words_e[i] for i in ids if i in id_words_e.keys()])

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
    encoder.load_state_dict(torch.load(
        path.join(path.dirname(path.abspath(__file__)), fp_encoder)))
    decoder.load_state_dict(torch.load(
        path.join(path.dirname(path.abspath(__file__)), fp_decoder)))

    X_test = df_test["j"].values
    X_id_test = nn.utils.rnn.pad_sequence(
        [tensor(sentence_to_ids_j(str(j))) for j in X_test], batch_first=True)

    dataset_test = [(X_i, X_id_i) for X_i, X_id_i in zip(X_test, X_id_test)]
    dataloader_test = DataLoader(dataset_test, batch_size=batch_size)
    
    for batch, (X, X_id) in enumerate(dataloader_test):
        X_id = X_id.to(device)
        encoder_output, encoder_hidden = encoder(X_id, None)
        decoder_output, decoder_hidden = decoder(tensor([[0]]), encoder_hidden)
        if batch < 5:
            print(batch, bleu_score([x.split() for x in X], [ids_to_sentence_e(output).split() for output in decoder_output[:, :, :-1].squeeze(0).int().detach().numpy()], ))
        else:
            break


if __name__ == "__main__":
    main()
