import os
import pandas as pd
from sklearn.datasets import fetch_20newsgroups


def gerar_base_politica_internacional():
    print("Gerando Dataset Internacional Político Real (20Newsgroups)...")

    categorias_politicas = [
        "talk.politics.guns",
        "talk.politics.mideast",
        "talk.politics.misc",
    ]

    print("Carregando posts e discussões políticas do benchmark oficial...")
    news_all = fetch_20newsgroups(
        subset="all",
        categories=categorias_politicas,
        remove=("headers", "footers", "quotes"),
    )

    df = pd.DataFrame({
        "texto": news_all.data,
        "target_orig": news_all.target,
    })

    print("Limpando dados...")
    df["texto"] = df["texto"].astype(str).str.strip()
    df = df[df["texto"].str.len() > 50].copy()

    print("Rotulando dados: 0 para esquerda/liberal, 1 para direita/conservador.")
    df["label"] = df["target_orig"].apply(lambda x: 0 if x in [0, 2] else 1)

    df_0 = df[df["label"] == 0]
    df_1 = df[df["label"] == 1]

    tamanho_real = min(len(df_0), len(df_1))

    df_balanced = pd.concat([
        df_0.sample(n=tamanho_real, random_state=42, replace=False),
        df_1.sample(n=tamanho_real, random_state=42, replace=False),
    ]).sample(frac=1, random_state=42).reset_index(drop=True)

    print("Salvando dataset balanceado...")
    os.makedirs("data", exist_ok=True)
    caminho_destino = "data/dataset_internacional.csv"
    df_balanced[["texto", "label"]].to_csv(caminho_destino, index=False)

    print(f"\nDataset real gerado com sucesso em: {caminho_destino}")
    print(f"Total de registros reais obtidos: {len(df_balanced)}")
    print("\nDistribuição das classes reais:")
    print(df_balanced["label"].value_counts())


if __name__ == "__main__":
    gerar_base_politica_internacional()