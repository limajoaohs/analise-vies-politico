#  Análise e Auditoria de Viés Político em Tweets

Projeto desenvolvido para a disciplina de Inteligência Artificial (2026.1) na Universidade Federal de Campina Grande (UFCG). O objetivo principal é classificar automaticamente textos e mensagens de redes sociais em vetores de viés ideológico (**Esquerda [0]** vs. **Direita [1]**) através de abordagens clássicas e de Deep Learning.

---

## Arquiteturas Avaliadas

1. **Baseline (TF-IDF + Logistic Regression)**: Extração TF-IDF com n-gramas (1, 2) e classificador linear.
2. **BOW + MLP**: Vetorização Bag-of-Words simples (`CountVectorizer`) alimentando uma Rede Neural Feedforward Densa (Multi-Layer Perceptron - `MLPClassifier`).
3. **Bi-LSTM**: Rede Neural Recorrente Bidirecional para modelagem sequencial de contexto.
4. **BERTimbau / Transformers**: Modelo pré-treinado em português ajustado para classificação.

---

## Resultados

Os testes demonstraram que a escolha do algoritmo depende diretamente do volume de dados disponível e da presença de marcadores lexicais específicos:

| Dataset | Amostras Totais | Baseline (TF-IDF + LogReg) | BOW + MLP | Bi-LSTM | BERTimbau |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Base Brasileira (PT-BR)** | 300 | **87%** | **82%** | 67% | **90%** |
| **Base Internacional (20Newsgroups)** | 1.774 | **93%** | **86%** | 85% | **95%** |
