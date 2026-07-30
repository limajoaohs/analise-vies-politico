#  Análise e Auditoria de Viés Político em Tweets

Projeto desenvolvido para a disciplina de Inteligência Artificial (2026.1) na Universidade Federal de Campina Grande (UFCG). O objetivo principal é classificar automaticamente textos e mensagens de redes sociais em vetores de viés ideológico (**Esquerda [0]** vs. **Direita [1]**) através de abordagens clássicas e de Deep Learning.

---

## Resultados

Os testes demonstraram que a escolha do algoritmo depende diretamente do volume de dados disponível e da presença de marcadores lexicais específicos:

| Dataset | Amostras Totais | Baseline (TF-IDF + LogReg) | Rede Neural (Bi-LSTM) |
| :--- | :---: | :---: | :---: |
| **Base Brasileira (PT-BR)** | 300 | **87% Acurácia** | 77% Acurácia |
| **Base Internacional (20Newsgroups)** | 1.774 | **93% Acurácia** | 84% Acurácia |
