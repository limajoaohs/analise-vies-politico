import os
import random
import numpy as np
import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from torch.optim import AdamW
from transformers import AutoTokenizer, AutoModelForSequenceClassification, set_seed
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns


class TweetDataset(Dataset):
    def __init__(self, texts, labels, tokenizer, max_len=128):
        self.texts = texts
        self.labels = labels
        self.tokenizer = tokenizer
        self.max_len = max_len

    def __len__(self):
        return len(self.texts)

    def __getitem__(self, item):
        text = str(self.texts[item])
        encoding = self.tokenizer(
            text,
            truncation=True,
            padding='max_length',
            max_length=self.max_len,
            return_tensors='pt'
        )
        return {
            'input_ids': encoding['input_ids'].flatten(),
            'attention_mask': encoding['attention_mask'].flatten(),
            'labels': torch.tensor(self.labels[item], dtype=torch.long)
        }


def treinar_e_avaliar_bertimbau(caminho_csv='data/dataset_brasil_limpo.csv'):
    print("\n--- Treinando BERTimbau (Transformer Pré-treinado) - Brasil (PT-BR) ---")
    SEED = 42
    random.seed(SEED)
    np.random.seed(SEED)
    torch.manual_seed(SEED)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)
    set_seed(SEED)

    df = pd.read_csv(caminho_csv)
    coluna_texto = 'texto_limpo' if 'texto_limpo' in df.columns else 'texto'
    coluna_label = 'rotulo' if 'rotulo' in df.columns else 'label'

    mapa_conversao = {'esquerda': 0, 'left': 0, 0: 0, 'direita': 1, 'right': 1, 1: 1}
    df['label_num'] = df[coluna_label].astype(str).str.lower().str.strip().map(mapa_conversao)
    df = df.dropna(subset=[coluna_texto, 'label_num'])

    X = df[coluna_texto].to_numpy()
    y = df['label_num'].astype(int).to_numpy()

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=SEED, stratify=y
    )

    model_name = 'neuralmind/bert-base-portuguese-cased'
    tokenizer = AutoTokenizer.from_pretrained(model_name)

    train_dataset = TweetDataset(X_train, y_train, tokenizer)
    test_dataset = TweetDataset(X_test, y_test, tokenizer)

    train_loader = DataLoader(train_dataset, batch_size=8, shuffle=True)
    test_loader = DataLoader(test_dataset, batch_size=8, shuffle=False)

    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)
    model.to(device)

    optimizer = AdamW(model.parameters(), lr=2e-5)

    model.train()
    epochs = 3
    for epoch in range(epochs):
        for batch in train_loader:
            optimizer.zero_grad()
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
            loss = outputs.loss
            loss.backward()
            optimizer.step()

    model.eval()
    predictions = []
    true_labels = []

    with torch.no_grad():
        for batch in test_loader:
            input_ids = batch['input_ids'].to(device)
            attention_mask = batch['attention_mask'].to(device)
            labels = batch['labels'].to(device)
            outputs = model(input_ids=input_ids, attention_mask=attention_mask)
            preds = torch.argmax(outputs.logits, dim=1)
            predictions.extend(preds.cpu().numpy())
            true_labels.extend(labels.cpu().numpy())

    print('\n--- Relatório de Classificação (BERTimbau) ---')
    print(classification_report(true_labels, predictions, target_names=['Esquerda (0)', 'Direita (1)']))

    cm = confusion_matrix(true_labels, predictions)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Esquerda', 'Direita'],
                yticklabels=['Esquerda', 'Direita'])
    plt.title('Matriz de Confusão - BERTimbau')
    plt.xlabel('Previsto')
    plt.ylabel('Real')
    plt.tight_layout()

    os.makedirs('results', exist_ok=True)
    plt.savefig('results/cm_bertimbau.png', dpi=300)
    plt.close()


if __name__ == '__main__':
    treinar_e_avaliar_bertimbau('data/dataset_brasil_limpo.csv')
