import os
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import seaborn as sns


def run_bow_pipeline(data_path, lang_label, save_prefix):
    df = pd.read_csv(data_path)
    coluna_texto = 'texto_limpo' if 'texto_limpo' in df.columns else ('texto' if 'texto' in df.columns else 'text_clean')
    coluna_label = None
    for col in ['label', 'rotulo', 'vies', 'categoria', 'target', 'class']:
        if col in df.columns:
            coluna_label = col
            break

    mapa_conversao = {'esquerda': 0, 'left': 0, '0': 0, 0: 0, 'direita': 1, 'right': 1, '1': 1, 1: 1}
    df['label_num'] = df[coluna_label].astype(str).str.lower().str.strip().map(mapa_conversao)
    df = df.dropna(subset=[coluna_texto, 'label_num'])

    X = df[coluna_texto]
    y = df['label_num'].astype(int)

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    vectorizer = CountVectorizer(max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    clf = MultinomialNB()
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)

    print(f"\n--- BoW (Bag-of-Words + Naive Bayes) - {lang_label} ---")
    print(classification_report(y_test, y_pred, target_names=['Esquerda (0)', 'Direita (1)']))

    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(5, 4))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues',
                xticklabels=['Esquerda', 'Direita'],
                yticklabels=['Esquerda', 'Direita'])
    plt.title(f'Matriz de Confusão - BoW ({lang_label})')
    plt.ylabel('Real')
    plt.xlabel('Previsto')
    plt.tight_layout()

    os.makedirs('results', exist_ok=True)
    plt.savefig(f'results/cm_bow_{save_prefix}.png', dpi=300)
    plt.close()


if __name__ == '__main__':
    run_bow_pipeline('data/dataset_internacional_limpo.csv', 'Internacional', 'intl')
    run_bow_pipeline('data/dataset_brasil_limpo.csv', 'Brasil', 'br')
