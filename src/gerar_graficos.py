import matplotlib.pyplot as plt
import numpy as np
import os

os.makedirs('results', exist_ok=True)

datasets = ['Internacional (1.774)', 'Brasil (300)']
baseline_acc = [0.93, 0.87]
bow_acc = [0.86, 0.82]
bilstm_acc = [0.85, 0.67]
bertimbau_acc = [0.95, 0.90]

x = np.arange(len(datasets))
width = 0.18

fig, ax = plt.subplots(figsize=(10, 6))
rects1 = ax.bar(x - 1.5 * width, baseline_acc, width, label='TF-IDF + LogReg (Baseline)', color='#1f77b4')
rects2 = ax.bar(x - 0.5 * width, bow_acc, width, label='BOW + MLP', color='#9467bd')
rects3 = ax.bar(x + 0.5 * width, bilstm_acc, width, label='Bi-LSTM (Deep Learning)', color='#2ca02c')
rects4 = ax.bar(x + 1.5 * width, bertimbau_acc, width, label='BERTimbau (Transformer)', color='#d62728')

ax.set_ylabel('Acurácia')
ax.set_title('Comparação de Desempenho de PLN: Baseline, BOW + MLP, Bi-LSTM e BERTimbau')
ax.set_xticks(x)
ax.set_xticklabels(datasets)
ax.set_ylim(0, 1.10)
ax.legend()

ax.bar_label(rects1, padding=3, fmt='%.2f')
ax.bar_label(rects2, padding=3, fmt='%.2f')
ax.bar_label(rects3, padding=3, fmt='%.2f')
ax.bar_label(rects4, padding=3, fmt='%.2f')

plt.tight_layout()
plt.savefig('results/comparacao_modelos.png', dpi=300)
print("Gráfico comparativo salvo em 'results/comparacao_modelos.png'!")