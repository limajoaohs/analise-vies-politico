# Análise e Auditoria de Viés Político em Tweets

Projeto desenvolvido para a disciplina de Inteligência Artificial (2026.1) na Universidade Federal de Campina Grande (UFCG). O objetivo principal é classificar automaticamente textos e mensagens de redes sociais em vetores de viés ideológico (**Esquerda [0]** vs. **Direita [1]**) através de abordagens clássicas e de Deep Learning.

---

## Arquiteturas Avaliadas

1. **Baseline (TF-IDF + Logistic Regression):** Extração TF-IDF com n-gramas (1, 2) e classificador estatístico linear.
2. **BOW + MLP:** Vetorização *Bag-of-Words* simples (`CountVectorizer`) alimentando uma Rede Neural básica (*Multi-Layer Perceptron* - `MLPClassifier`).
3. **Bi-LSTM:** Rede Neural Recorrente Bidirecional implementada via PyTorch para modelagem sequencial profunda de contexto.

---

## Resultados

Os testes demonstraram que a eficácia da classificação e a escolha do algoritmo dependem diretamente do **volume de dados** disponível e da presença de marcadores lexicais explícitos. Modelos complexos sofrem de *Data Hunger* em bases menores, enquanto métodos baseados em contagem de frequência brilham pela estabilidade:

| Dataset | Amostras Totais | Baseline (TF-IDF + LogReg) | BOW + MLP | Bi-LSTM (Deep Learning) |
| --- | --- | --- | --- | --- |
| **Base Brasileira (PT-BR)** | 300 | **87%** | **87%** | 63% |
| **Base Internacional (20Newsgroups)** | 1.774 | **93%** | **92%** | 86% |

---