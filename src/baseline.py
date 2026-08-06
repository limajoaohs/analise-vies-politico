import os
import pandas as pd
from preprocess import processar_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split


def treinar_e_avaliar_baseline(caminho_csv, nome_base='Dataset'):
    print(f'\nTreinando Baseline (TF-IDF + LogReg) - {nome_base}')

    if not os.path.exists(caminho_csv):
        print(f'Arquivo não encontrado: {caminho_csv}')
        return

    df = pd.read_csv(caminho_csv)

    coluna_texto = 'texto_limpo' if 'texto_limpo' in df.columns else 'texto'

    coluna_label = None
    for col in ['label', 'rotulo', 'vies', 'categoria', 'target', 'class']:
        if col in df.columns:
            coluna_label = col
            break

    if not coluna_label:
        print(f'Erro: Nenhuma coluna de rótulo encontrada. Colunas no CSV: {list(df.columns)}')
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

    df['label_num'] = df[coluna_label].astype(str).str.lower().str.strip().map(mapa_conversao)
    df = df.dropna(subset=[coluna_texto, 'label_num'])

    X = df[coluna_texto]
    y = df['label_num'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = TfidfVectorizer(max_features=5000, ngram_range=(1, 2))
    X_train_tfidf = vectorizer.fit_transform(X_train)
    X_test_tfidf = vectorizer.transform(X_test)

    model = LogisticRegression(max_iter=1000, random_state=42)
    model.fit(X_train_tfidf, y_train)

    y_pred = model.predict(X_test_tfidf)

    print('\n--- Relatório de Classificação ---')
    print(classification_report(y_test, y_pred, target_names=['Esquerda (0)', 'Direita (1)']))

    print('--- Matriz de Confusão ---')
    cm = confusion_matrix(y_test, y_pred)
    print(f'TN (Esquerda acertos): {cm[0][0]} | FP (Esquerda como Direita): {cm[0][1]}')
    print(f'FN (Direita como Esquerda): {cm[1][0]} | TP (Direita acertos): {cm[1][1]}\n')


if __name__ == '__main__':
    caminho_inter = 'data/dataset_internacional.csv'
    caminho_inter_limpo = 'data/dataset_internacional_limpo.csv'

    if os.path.exists(caminho_inter):
        processar_dataset(caminho_inter, caminho_inter_limpo, idioma='english')
        treinar_e_avaliar_baseline(caminho_inter_limpo, nome_base='Base Internacional (10k)')

    caminho_br = 'data/dataset_brasil.csv'
    caminho_br_limpo = 'data/dataset_brasil_limpo.csv'

    if os.path.exists(caminho_br):
        processar_dataset(caminho_br, caminho_br_limpo, idioma='portuguese')
        treinar_e_avaliar_baseline(caminho_br_limpo, nome_base='Base Brasileira (PT-BR)')