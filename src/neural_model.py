from collections import Counter
import os
import numpy as np
import pandas as pd
from preprocess import processar_dataset
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset

torch.manual_seed(42)
np.random.seed(42)


class Vocabularizacao:

    def __init__(self, max_tokens=5000):
        self.max_tokens = max_tokens
        self.word2idx = {'<PAD>': 0, '<UNK>': 1}
        self.idx2word = {0: '<PAD>', 1: '<UNK>'}

    def fit(self, textos):
        palavras = [palavra for t in textos for palavra in str(t).split()]
        contagem = Counter(palavras).most_common(self.max_tokens - 2)
        for idx, (palavra, _) in enumerate(contagem, start=2):
            self.word2idx[palavra] = idx
            self.idx2word[idx] = palavra

    def transform(self, textos, max_len=100):
        matriz = []
        for t in textos:
            tokens = [self.word2idx.get(w, 1) for w in str(t).split()[:max_len]]
            tokens += [0] * (max_len - len(tokens))
            matriz.append(tokens)
        return np.array(matriz)


class DatasetTexto(Dataset):

    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.long)
        self.y = torch.tensor(y, dtype=torch.long)

    def __len__(self):
        return len(self.y)

    def __getitem__(self, idx):
        return self.X[idx], self.y[idx]


class ClassificadorBiLSTM(nn.Module):

    def __init__(self, vocab_size, embedding_dim=64, hidden_dim=64, output_dim=2):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
        self.lstm = nn.LSTM(
            embedding_dim,
            hidden_dim,
            num_layers=1,
            bidirectional=True,
            batch_first=True,
        )
        self.fc = nn.Linear(hidden_dim * 2, output_dim)
        self.dropout = nn.Dropout(0.3)

    def forward(self, x):
        embedded = self.dropout(self.embedding(x))
        _, (hidden, _) = self.lstm(embedded)
        hidden = torch.cat((hidden[-2, :, :], hidden[-1, :, :]), dim=1)
        return self.fc(self.dropout(hidden))


def treinar_e_avaliar_neural(caminho_csv, nome_base='Dataset'):
    print(f'\nTreinando Bi-LSTM (PyTorch) - {nome_base}')

    if not os.path.exists(caminho_csv):
        print(f'Arquivo {caminho_csv} não encontrado.')
        return

    df = pd.read_csv(caminho_csv)
    coluna_texto = 'texto_limpo' if 'texto_limpo' in df.columns else 'texto'

    coluna_label = None
    for col in ['label', 'rotulo', 'vies', 'categoria', 'target']:
        if col in df.columns:
            coluna_label = col
            break

    if not coluna_label:
        print('Erro: Nenhuma coluna de rótulo encontrada.')
        return

    mapa_conversao = {
        'esquerda': 0,
        'left': 0,
        '0': 0,
        0: 0,
        'direita': 1,
        'right': 1,
        '1': 1,
        1: 1,
    }
    df['label_num'] = (
        df[coluna_label].astype(str).str.lower().str.strip().map(mapa_conversao)
    )

    df = df.dropna(subset=[coluna_texto, 'label_num'])

    X_textos = df[coluna_texto].tolist()
    y_labels = df['label_num'].astype(int).values

    vocab = Vocabularizacao(max_tokens=5000)
    vocab.fit(X_textos)
    X_vetores = vocab.transform(X_textos, max_len=100)

    X_train, X_test, y_train, y_test = train_test_split(
        X_vetores, y_labels, test_size=0.2, random_state=42, stratify=y_labels
    )

    train_loader = DataLoader(
        DatasetTexto(X_train, y_train), batch_size=8, shuffle=True
    )
    test_loader = DataLoader(
        DatasetTexto(X_test, y_test), batch_size=8, shuffle=False
    )

    model = ClassificadorBiLSTM(vocab_size=len(vocab.word2idx))
    criterion = nn.CrossEntropyLoss()
    optimizer = torch.optim.Adam(model.parameters(), lr=0.002)

    model.train()
    epochs = 15
    for epoch in range(1, epochs + 1):
        loss_total = 0
        for batch_X, batch_y in train_loader:
            optimizer.zero_grad()
            outputs = model(batch_X)
            loss = criterion(outputs, batch_y)
            loss.backward()
            optimizer.step()
            loss_total += loss.item()

    model.eval()
    preds = []
    with torch.no_grad():
        for batch_X, _ in test_loader:
            outputs = model(batch_X)
            preds.extend(torch.argmax(outputs, dim=1).numpy())

    print('\n--- Relatório de Classificação (Bi-LSTM) ---')
    print(
        classification_report(
            y_test, preds, target_names=['Esquerda (0)', 'Direita (1)']
        )
    )

    print('--- Matriz de Confusão ---')
    cm = confusion_matrix(y_test, preds)
    print(
        f'TN (Esquerda acertos): {cm[0][0]} | FP (Esquerda como Direita):'
        f' {cm[0][1]}'
    )
    print(
        f'FN (Direita como Esquerda): {cm[1][0]} | TP (Direita acertos):'
        f' {cm[1][1]}\n'
    )


if __name__ == '__main__':
    caminho_inter = 'data/dataset_internacional.csv'
    caminho_inter_limpo = 'data/dataset_internacional_limpo.csv'

    if os.path.exists(caminho_inter):
        print('\n[1/2] Higienizando base internacional (20Newsgroups)...')
        processar_dataset(caminho_inter, caminho_inter_limpo, idioma='english')
        treinar_e_avaliar_neural(
            caminho_inter_limpo, nome_base='Base Internacional Político'
        )
    else:
        print(
            f'Arquivo {caminho_inter} não encontrado. Execute'
            ' src/gerar_base_internacional.py primeiro.'
        )

    caminho_br = 'data/dataset_brasil.csv'
    caminho_br_limpo = 'data/dataset_brasil_limpo.csv'

    if os.path.exists(caminho_br):
        print('\n[2/2] Higienizando base brasileira (300 dados)...')
        processar_dataset(caminho_br, caminho_br_limpo, idioma='portuguese')
        treinar_e_avaliar_neural(
            caminho_br_limpo, nome_base='Base Brasileira (PT-BR)'
        )