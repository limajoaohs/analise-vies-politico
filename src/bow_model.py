import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split

def treinar_e_avaliar_bow(caminho_csv, nome_base='Dataset'):
    print(f'\nTreinando modelo BOW (Bag of Words + MLP) - {nome_base}')
    if not os.path.exists(caminho_csv):
        return

    df = pd.read_csv(caminho_csv)
    coluna_texto = 'texto_limpo' if 'texto_limpo' in df.columns else 'texto'
    coluna_label = None
    for col in ['label', 'rotulo', 'vies', 'categoria', 'target', 'class']:
        if col in df.columns: coluna_label = col; break

    mapa_conversao = {'esquerda': 0, 'left': 0, '0': 0, 0: 0, 'direita': 1, 'right': 1, '1': 1, 1: 1}
    df['label_num'] = df[coluna_label].astype(str).str.lower().str.strip().map(mapa_conversao)
    df = df.dropna(subset=[coluna_texto, 'label_num'])

    X = df[coluna_texto]
    y = df['label_num'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

    # Implementação do BOW usando CountVectorizer: conta a frequência bruta das palavras, sem o peso relativo do TF-IDF
    vectorizer = CountVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_bow = vectorizer.fit_transform(X_train)
    X_test_bow = vectorizer.transform(X_test)

    # Classificador MLP (Rede Neural Feedforward Simples)
    model = MLPClassifier(hidden_layer_sizes=(100,), max_iter=1000, random_state=42, early_stopping=True)
    model.fit(X_train_bow, y_train)
    y_pred = model.predict(X_test_bow)

    print('\n--- Relatório de Classificação (BOW + MLP) ---')
    print(classification_report(y_test, y_pred, target_names=['Esquerda (0)', 'Direita (1)']))

if __name__ == '__main__':
    treinar_e_avaliar_bow('data/dataset_internacional_limpo.csv', 'Base Internacional')
    treinar_e_avaliar_bow('data/dataset_brasil_limpo.csv', 'Base Brasileira (PT-BR)')