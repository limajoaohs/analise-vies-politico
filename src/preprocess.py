import os
import re
import string
import nltk
import pandas as pd
from nltk.corpus import stopwords

nltk.download('stopwords', quiet=True)

def limpar_texto(texto, idioma='portuguese'):
    if not isinstance(texto, str):
        return ''

    texto = texto.lower()
    texto = re.sub(r'https?://\S+|www\.\S+', '', texto)
    texto = re.sub(r'<.*?>', '', texto)
    texto = re.sub(r'[/_—–-]', ' ', texto)
    texto = texto.translate(str.maketrans('', '', string.punctuation))
    texto = re.sub(r'\d+', '', texto)

    try:
        stop_words = set(stopwords.words(idioma))
        palavras = texto.split()
        palavras_filtradas = [w for w in palavras if w not in stop_words]
        texto = ' '.join(palavras_filtradas)
    except Exception:
        pass

    return re.sub(r'\s+', ' ', texto).strip()

def processar_dataset(caminho_entrada, caminho_saida, idioma='portuguese'):
    if not os.path.exists(caminho_entrada):
        print(f'Arquivo não encontrado: {caminho_entrada}')
        return

    print(f'Higienizando dataset: {caminho_entrada} ({idioma})...')
    df = pd.read_csv(caminho_entrada)

    if 'texto' not in df.columns:
        print(f'Coluna "texto" não encontrada no CSV {caminho_entrada}.')
        return

    df['texto_limpo'] = df['texto'].apply(lambda x: limpar_texto(x, idioma))
    df.to_csv(caminho_saida, index=False, encoding='utf-8')
    print(f'Salvo com sucesso em: {caminho_saida}\n')