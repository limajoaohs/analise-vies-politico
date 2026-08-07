import os
import base64
import subprocess

def image_to_base64(path):
    if not os.path.exists(path):
        return ""
    with open(path, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
        return f"data:image/png;base64,{encoded_string}"

# Load images as base64
img_comparacao = image_to_base64('/home/joaolima/Projetos/analise-vies-politico/results/comparacao_modelos.png')
img_cm_bow = image_to_base64('/home/joaolima/Projetos/analise-vies-politico/results/cm_bow_br.png')
img_cm_mlp = image_to_base64('/home/joaolima/Projetos/analise-vies-politico/results/cm_mlp_br.png')
img_cm_bert = image_to_base64('/home/joaolima/Projetos/analise-vies-politico/results/cm_bertimbau.png')

html_content = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>Guia de Estudo - Análise de Viés Político em Textos com PLN</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Fira+Code:wght@400;500;600&display=swap');

        @page {
            size: A4;
            margin: 12mm 15mm 15mm 15mm;
        }

        * {
            box-sizing: border-box;
            -webkit-print-color-adjust: exact !important;
            print-color-adjust: exact !important;
        }

        body {
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            color: #0f172a;
            background-color: #ffffff;
            line-height: 1.5;
            font-size: 10pt;
            margin: 0;
            padding: 0;
        }

        /* Header / Cover Banner */
        .cover-header {
            background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 100%);
            color: #ffffff;
            padding: 22px 26px;
            border-radius: 12px;
            margin-bottom: 20px;
            box-shadow: 0 4px 12px rgba(15, 23, 42, 0.15);
        }

        .badge-tag {
            display: inline-block;
            background: rgba(255, 255, 255, 0.18);
            color: #93c5fd;
            font-size: 8pt;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 1px;
            padding: 3px 9px;
            border-radius: 20px;
            margin-bottom: 8px;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .cover-title {
            font-size: 18pt;
            font-weight: 800;
            margin: 0 0 6px 0;
            line-height: 1.25;
            letter-spacing: -0.5px;
        }

        .cover-subtitle {
            font-size: 10.5pt;
            color: #cbd5e1;
            font-weight: 400;
            margin: 0 0 14px 0;
        }

        .cover-meta {
            display: flex;
            justify-content: space-between;
            border-top: 1px solid rgba(255, 255, 255, 0.15);
            padding-top: 10px;
            font-size: 8.5pt;
            color: #94a3b8;
        }

        /* Headings */
        h1 {
            font-size: 14pt;
            font-weight: 700;
            color: #1e3a8a;
            border-bottom: 2px solid #e2e8f0;
            padding-bottom: 5px;
            margin-top: 20px;
            margin-bottom: 12px;
            page-break-after: avoid;
        }

        h2 {
            font-size: 12pt;
            font-weight: 700;
            color: #0f172a;
            margin-top: 16px;
            margin-bottom: 8px;
            page-break-after: avoid;
        }

        h3 {
            font-size: 10.5pt;
            font-weight: 600;
            color: #2563eb;
            margin-top: 12px;
            margin-bottom: 6px;
            page-break-after: avoid;
        }

        p {
            margin-top: 0;
            margin-bottom: 8px;
            text-align: justify;
        }

        /* Callout Boxes */
        .callout {
            background-color: #f8fafc;
            border-left: 4px solid #2563eb;
            padding: 10px 14px;
            border-radius: 0 8px 8px 0;
            margin: 12px 0;
            page-break-inside: avoid;
        }

        .callout-title {
            font-weight: 700;
            color: #1e3a8a;
            margin-bottom: 3px;
            font-size: 9.5pt;
        }

        .callout-warning {
            background-color: #fef2f2;
            border-left-color: #ef4444;
        }
        .callout-warning .callout-title {
            color: #991b1b;
        }

        .callout-success {
            background-color: #f0fdf4;
            border-left-color: #22c55e;
        }
        .callout-success .callout-title {
            color: #166534;
        }

        /* Code Blocks */
        pre {
            background-color: #0f172a;
            color: #f8fafc;
            font-family: 'Fira Code', monospace;
            font-size: 8pt;
            padding: 12px 14px;
            border-radius: 8px;
            overflow-x: auto;
            margin: 10px 0;
            line-height: 1.4;
            page-break-inside: avoid;
            box-shadow: inset 0 0 6px rgba(0,0,0,0.2);
        }

        code {
            font-family: 'Fira Code', monospace;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 2px 4px;
            border-radius: 4px;
            font-size: 8.5pt;
        }

        pre code {
            background-color: transparent;
            color: inherit;
            padding: 0;
        }

        /* Tables */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 12px 0;
            font-size: 9pt;
            page-break-inside: avoid;
        }

        th {
            background-color: #1e293b;
            color: #ffffff;
            font-weight: 600;
            text-align: left;
            padding: 7px 10px;
            border: 1px solid #1e293b;
        }

        td {
            padding: 7px 10px;
            border: 1px solid #e2e8f0;
        }

        tr:nth-child(even) {
            background-color: #f8fafc;
        }

        /* Image Grid */
        .img-container {
            text-align: center;
            margin: 12px 0;
            page-break-inside: avoid;
        }

        .img-container img {
            max-width: 80%;
            height: auto;
            border-radius: 8px;
            border: 1px solid #e2e8f0;
            box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05);
        }

        .img-caption {
            font-size: 8pt;
            color: #64748b;
            margin-top: 4px;
            font-style: italic;
        }

        .grid-2 {
            display: flex;
            gap: 12px;
            margin: 12px 0;
            page-break-inside: avoid;
        }

        .grid-2 .img-container {
            flex: 1;
            margin: 0;
        }

        .grid-2 .img-container img {
            max-width: 100%;
        }

        /* Key-Value Lists & Badges */
        .badge {
            display: inline-block;
            padding: 2px 7px;
            border-radius: 4px;
            font-size: 8pt;
            font-weight: 600;
        }
        .badge-blue { background-color: #dbeafe; color: #1e40af; }
        .badge-green { background-color: #dcfce7; color: #166534; }
        .badge-red { background-color: #fee2e2; color: #991b1b; }

        .page-break {
            page-break-before: always;
        }

        .script-step {
            background: #ffffff;
            border: 1px solid #cbd5e1;
            border-radius: 8px;
            padding: 10px 14px;
            margin-bottom: 10px;
            page-break-inside: avoid;
        }
        .script-time {
            font-weight: 700;
            color: #2563eb;
            font-size: 8.5pt;
            text-transform: uppercase;
        }
        .script-quote {
            font-style: italic;
            color: #334155;
            margin-top: 4px;
            border-left: 3px solid #94a3b8;
            padding-left: 8px;
        }

        /* Syntax Highlight colors */
        .kw { color: #f43f5e; font-weight: bold; } /* keyword */
        .func { color: #38bdf8; } /* function */
        .str { color: #4ade80; } /* string */
        .com { color: #94a3b8; font-style: italic; } /* comment */
        .num { color: #fbbf24; } /* number */
    </style>
</head>
<body>

    <!-- COVER HEADER -->
    <div class="cover-header">
        <div class="badge-tag">Processamento de Linguagem Natural & Deep Learning</div>
        <div class="cover-title">Guia de Estudo e Defesa do Projeto:<br>Análise de Viés Político em Textos</div>
        <div class="cover-subtitle">Comparação Sistemática: Bag-of-Words (Naive Bayes & MLP), Bi-LSTM e BERTimbau (Transformers)</div>
        <div class="cover-meta">
            <span><strong>Preparado para:</strong> Apresentação e Avaliação do Projeto</span>
            <span><strong>Modelos:</strong> BoW + Naive Bayes | BoW + MLP | BERTimbau</span>
        </div>
    </div>

    <!-- SEÇÃO 1 -->
    <h1>📌 1. Visão Geral do Projeto e Objetivos</h1>

    <p>O objetivo deste projeto é construir e avaliar modelos estatísticos e neurais para a <strong>classificação automática de viés político</strong> (<strong>Esquerda <code>[0]</code></strong> vs. <strong>Direita <code>[1]</code></strong>) em dados textuais de redes sociais e fóruns de discussão.</p>

    <div class="callout callout-success">
        <div class="callout-title">🎯 Objetivo da Apresentação</div>
        Demonstrar como a evolução das arquiteturas de PLN — partindo de modelos estatísticos ingênuos (Bag-of-Words + Naive Bayes) para Redes Neurais Densas (MLP), Redes Recorrentes (Bi-LSTM) e Transformers Pré-treinados (BERTimbau) — impacta diretamente a acurácia no diagnóstico ideológico.
    </div>

    <h2>📊 Datasets Utilizados nos Experimentos</h2>
    <table>
        <thead>
            <tr>
                <th>Dataset</th>
                <th>Origem dos Dados</th>
                <th>Volume Total</th>
                <th>Distribuição de Classes</th>
                <th>Idioma</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Internacional</strong></td>
                <td>20Newsgroups (grupos <code>talk.politics.*</code>)</td>
                <td><strong>1.774 registros</strong></td>
                <td>887 Esquerda / 887 Direita (100% Balanceado)</td>
                <td>Inglês</td>
            </tr>
            <tr>
                <td><strong>Brasil (PT-BR)</strong></td>
                <td>Posts e Tweets de discussões políticas nacionais</td>
                <td><strong>300 registros</strong></td>
                <td>150 Esquerda / 150 Direita (100% Balanceado)</td>
                <td>Português (PT-BR)</td>
            </tr>
        </tbody>
    </table>

    <h2>⚙️ Pipeline de Engenharia de Dados & Pré-processamento</h2>
    <ol style="margin-top:4px; padding-left:20px;">
        <li style="margin-bottom:4px;"><strong>Higienização e Normalização:</strong> Remoção de caracteres especiais, conversão para minúsculas (<code>str.lower()</code>) e remoção de espaços nas extremidades (<code>str.strip()</code>).</li>
        <li style="margin-bottom:4px;"><strong>Mapeamento Estrito de Rótulos:</strong> Conversão unificada de strings (<code>'esquerda'</code>, <code>'left'</code>, <code>'0'</code> &rarr; <code>0</code>) e (<code>'direita'</code>, <code>'right'</code>, <code>'1'</code> &rarr; <code>1</code>).</li>
        <li style="margin-bottom:4px;"><strong>Divisão Estratificada (Train-Test Split):</strong> <strong>80% para Treino</strong> e <strong>20% para Teste</strong> utilizando <code>stratify=y</code> e <code>random_state=42</code> para garantir reprodutibilidade exata e manter o balanceamento nas amostras de avaliação.</li>
    </ol>

    <!-- SEÇÃO 2 -->
    <div class="page-break"></div>
    <h1>💻 2. Análise Técnica dos 3 Modelos Principais</h1>

    <!-- MODELO 1 -->
    <h2>1️⃣ Modelo 1: Bag-of-Words + Naive Bayes (<code style="font-size: 10pt;">bow_model.py</code>)</h2>

    <p>O <strong>Bag-of-Words (BoW)</strong> vetoriza o texto contando a frequência das palavras no vocabulário de treino, ignorando a ordem das palavras. O <strong>Multinomial Naive Bayes</strong> calcula a probabilidade da classe aplicando o Teorema de Bayes sob a premissa "ingênua" de independência entre os termos:</p>

    <div class="callout">
        <div class="callout-title">📐 Formulário Teórico: Teorema de Bayes</div>
        $$P(\text{Classe} \mid w_1, w_2, \dots, w_n) \propto P(\text{Classe}) \prod_{i=1}^{n} P(w_i \mid \text{Classe})$$
    </div>

    <h3>Código Consolidado Comentado:</h3>
    <pre><code><span class="kw">import</span> os
<span class="kw">import</span> pandas <span class="kw">as</span> pd
<span class="kw">from</span> sklearn.feature_extraction.text <span class="kw">import</span> CountVectorizer
<span class="kw">from</span> sklearn.naive_bayes <span class="kw">import</span> MultinomialNB
<span class="kw">from</span> sklearn.metrics <span class="kw">import</span> classification_report, confusion_matrix
<span class="kw">from</span> sklearn.model_selection <span class="kw">import</span> train_test_split

<span class="kw">def</span> <span class="func">run_bow_pipeline</span>(data_path, lang_label, save_prefix):
    df = pd.read_csv(data_path)
    coluna_texto = <span class="str">'texto_limpo'</span> <span class="kw">if</span> <span class="str">'texto_limpo'</span> <span class="kw">in</span> df.columns <span class="kw">else</span> <span class="str">'texto'</span>
    
    mapa = {<span class="str">'esquerda'</span>: 0, <span class="str">'left'</span>: 0, <span class="str">'0'</span>: 0, 0: 0, <span class="str">'direita'</span>: 1, <span class="str">'right'</span>: 1, <span class="str">'1'</span>: 1, 1: 1}
    df[<span class="str">'label_num'</span>] = df[<span class="str">'rotulo'</span>].astype(str).str.lower().str.strip().map(mapa)
    df = df.dropna(subset=[coluna_texto, <span class="str">'label_num'</span>])

    X_train, X_test, y_train, y_test = train_test_split(
        df[coluna_texto], df[<span class="str">'label_num'</span>].astype(int), 
        test_size=0.2, random_state=42, stratify=df[<span class="str">'label_num'</span>]
    )

    <span class="com"># Vetorização BoW limitada aos 1000 termos mais frequentes</span>
    vectorizer = CountVectorizer(max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    <span class="com"># Treinamento Multinomial Naive Bayes</span>
    clf = MultinomialNB()
    clf.fit(X_train_vec, y_train)

    y_pred = clf.predict(X_test_vec)
    print(classification_report(y_test, y_pred, target_names=[<span class="str">'Esquerda (0)'</span>, <span class="str">'Direita (1)'</span>]))</code></pre>

    <!-- MODELO 2 -->
    <h2>2️⃣ Modelo 2: Bag-of-Words + MLP / Rede Neural Densa (<code style="font-size: 10pt;">mlp_model.py</code>)</h2>

    <p>A <strong>MLP (Multi-Layer Perceptron)</strong> utiliza a mesma entrada em frequências de palavras (BoW com 1000 termos), porém direciona os dados para uma <strong>camada oculta densa com 64 neurônios</strong> ativados não-linearmente. O aprendizado ocorre via retropropagação do erro (<em>Backpropagation</em>).</p>

    <div class="callout callout-success">
        <div class="callout-title">💡 Vantagem da MLP sobre o Naive Bayes</div>
        Enquanto o Naive Bayes considera cada palavra isoladamente, os neurônios da camada oculta da MLP aprendem <strong>combinações ponderadas de palavras</strong> (ex: "redução" + "imposto" &rarr; viés de direita; "justiça" + "social" &rarr; viés de esquerda).
    </div>

    <h3>Código Consolidado Comentado:</h3>
    <pre><code><span class="kw">from</span> sklearn.neural_network <span class="kw">import</span> MLPClassifier

<span class="kw">def</span> <span class="func">run_mlp_pipeline</span>(data_path, lang_label, save_prefix):
    <span class="com"># (Leitura e pré-processamento idênticos ao pipeline BoW)</span>
    ...
    vectorizer = CountVectorizer(max_features=1000)
    X_train_vec = vectorizer.fit_transform(X_train)
    X_test_vec = vectorizer.transform(X_test)

    <span class="com"># Configuração da Rede Neural Densa (1 camada oculta com 64 neurônios)</span>
    mlp = MLPClassifier(hidden_layer_sizes=(64,), max_iter=300, random_state=42)
    mlp.fit(X_train_vec, y_train)

    y_pred = mlp.predict(X_test_vec)
    print(classification_report(y_test, y_pred, target_names=[<span class="str">'Esquerda (0)'</span>, <span class="str">'Direita (1)'</span>]))</code></pre>

    <!-- MODELO 3 -->
    <div class="page-break"></div>
    <h2>3️⃣ Modelo 3: Transformer Pré-treinado BERTimbau (<code style="font-size: 10pt;">bert_model.py</code>)</h2>

    <p>O <strong>BERT (Bidirectional Encoder Representations from Transformers)</strong> revoluciona o PLN ao utilizar mecanismos de <strong>Self-Attention (Atenção Multicabeça)</strong>. O modelo processa as palavras considerando o contexto bidirecional completo da frase.</p>
    <p>Utilizamos o <strong>BERTimbau (<code>neuralmind/bert-base-portuguese-cased</code>)</strong>, um modelo pré-treinado em bilhões de palavras em Português do Brasil, realizando <strong>Fine-Tuning por 3 épocas</strong> com o otimizador <code>AdamW</code> e taxa de aprendizado baixa (<code>lr=2e-5</code>).</p>

    <h3>Código Consolidado PyTorch Comentado:</h3>
    <pre><code><span class="kw">import</span> torch
<span class="kw">from</span> torch.utils.data <span class="kw">import</span> Dataset, DataLoader
<span class="kw">from</span> torch.optim <span class="kw">import</span> AdamW
<span class="kw">from</span> transformers <span class="kw">import</span> AutoTokenizer, AutoModelForSequenceClassification

<span class="kw">class</span> <span class="func">TweetDataset</span>(Dataset):
    <span class="kw">def</span> <span class="func">__init__</span>(self, texts, labels, tokenizer, max_len=128):
        self.texts, self.labels, self.tokenizer, self.max_len = texts, labels, tokenizer, max_len

    <span class="kw">def</span> <span class="func">__getitem__</span>(self, item):
        encoding = self.tokenizer(
            str(self.texts[item]), truncation=True, padding=<span class="str">'max_length'</span>,
            max_length=self.max_len, return_tensors=<span class="str">'pt'</span>
        )
        <span class="kw">return</span> {
            <span class="str">'input_ids'</span>: encoding[<span class="str">'input_ids'</span>].flatten(),
            <span class="str">'attention_mask'</span>: encoding[<span class="str">'attention_mask'</span>].flatten(),
            <span class="str">'labels'</span>: torch.tensor(self.labels[item], dtype=torch.long)
        }

<span class="kw">def</span> <span class="func">treinar_bertimbau</span>(caminho_csv):
    model_name = <span class="str">'neuralmind/bert-base-portuguese-cased'</span>
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name, num_labels=2)

    device = torch.device(<span class="str">'cuda'</span> <span class="kw">if</span> torch.cuda.is_available() <span class="kw">else</span> <span class="str">'cpu'</span>)
    model.to(device)
    optimizer = AdamW(model.parameters(), lr=2e-5)

    <span class="com"># Fine-tuning por 3 Épocas</span>
    model.train()
    <span class="kw">for</span> epoch <span class="kw">in</span> range(3):
        <span class="kw">for</span> batch <span class="kw">in</span> train_loader:
            optimizer.zero_grad()
            outputs = model(
                input_ids=batch[<span class="str">'input_ids'</span>].to(device),
                attention_mask=batch[<span class="str">'attention_mask'</span>].to(device),
                labels=batch[<span class="str">'labels'</span>].to(device)
            )
            outputs.loss.backward()
            optimizer.step()</code></pre>

    <h2>🖼️ Matrizes de Confusão nos Dados do Brasil (PT-BR)</h2>
    <div class="grid-2">
        <div class="img-container">
            <img src="__IMG_BOW__" alt="Matriz BoW">
            <div class="img-caption">1. BoW + Naive Bayes (Acurácia: 82%)</div>
        </div>
        <div class="img-container">
            <img src="__IMG_MLP__" alt="Matriz MLP">
            <div class="img-caption">2. BoW + MLP Densa (Acurácia: 87%)</div>
        </div>
    </div>
    <div class="img-container">
        <img src="__IMG_BERT__" alt="Matriz BERTimbau" style="max-width: 45%;">
        <div class="img-caption">3. BERTimbau Transformer SOTA (Acurácia: 90%)</div>
    </div>

    <!-- SEÇÃO 3 -->
    <div class="page-break"></div>
    <h1>📈 3. Comparativo de Desempenho Geral do Projeto</h1>

    <table>
        <thead>
            <tr>
                <th>Modelo / Arquitetura</th>
                <th>Dataset Internacional</th>
                <th>Dataset Brasil (PT-BR)</th>
                <th>Comportamento / Observações Principais</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td><strong>Baseline (TF-IDF + LogReg)</strong></td>
                <td>0.93 (93%)</td>
                <td>0.87 (87%)</td>
                <td>Vetorização por relevância estatística de termos.</td>
            </tr>
            <tr>
                <td><strong>BoW + Naive Bayes</strong></td>
                <td>0.86 (86%)</td>
                <td>0.82 (82%)</td>
                <td>Rápido, mas limitado pela suposição de independência.</td>
            </tr>
            <tr>
                <td><strong>BoW + MLP (Rede Densa)</strong></td>
                <td>0.86 (86%)</td>
                <td><span class="badge badge-blue">0.87 (87%)</span></td>
                <td>Captura relações não-lineares no vocabulário.</td>
            </tr>
            <tr>
                <td><strong>Bi-LSTM (PyTorch)</strong></td>
                <td>0.85 (85%)</td>
                <td><span class="badge badge-red">0.67 (67%)</span></td>
                <td>Sofreu <strong>overfitting</strong> no Brasil por falta de dados (300 amostras).</td>
            </tr>
            <tr>
                <td><strong>BERTimbau (Transformer)</strong></td>
                <td><span class="badge badge-green">0.95 (95%)</span></td>
                <td><span class="badge badge-green">0.90 (90%)</span></td>
                <td><strong>Campeão Absoluto</strong>: Entende contexto e sintaxe do PT-BR.</td>
            </tr>
        </tbody>
    </table>

    <div class="img-container">
        <img src="__IMG_COMPARACAO__" alt="Gráfico Comparativo de Desempenho">
        <div class="img-caption">Figura: Gráfico consolidado de acurácia gerado pelo script <code>gerar_graficos.py</code>.</div>
    </div>

    <!-- SEÇÃO 4 -->
    <div class="page-break"></div>
    <h1>🎤 4. Roteiro Prático de Apresentação & Defesa</h1>

    <div class="script-step">
        <div class="script-time">⏱️ Minuto 1: Introdução ao Problema</div>
        <div class="script-quote">
            "Boa noite! Nosso trabalho investiga o diagnóstico automático de viés político (Esquerda vs. Direita) em textos usando Processamento de Linguagem Natural. Avaliamos a transição entre modelos clássicos baseados em frequência e modelos modernos de Deep Learning em dois cenários: um benchmark internacional com 1.774 textos e uma base brasileira com 300 dados."
        </div>
    </div>

    <div class="script-step">
        <div class="script-time">⏱️ Minuto 2: Arquiteturas de Machine Learning</div>
        <div class="script-quote">
            "Testamos o Bag-of-Words com Naive Bayes como baseline probabilístico. Em seguida, elevamos a capacidade computacional usando uma Rede Neural Densa (MLP) de 64 neurônios, capaz de relacionar combinações não-lineares de palavras. Por fim, implementamos o BERTimbau, um Transformer pré-treinado em Português ajustado via Fine-Tuning em PyTorch."
        </div>
    </div>

    <div class="script-step">
        <div class="script-time">⏱️ Minuto 3: Resultados e Comparação da Acurácia</div>
        <div class="script-quote">
            "Nos resultados: a MLP atingiu 87% de acurácia no Brasil, demonstrando superioridade sobre o Naive Bayes (82%). Contudo, o BERTimbau dominou com 90% no Brasil e 95% no Internacional, provando que embeddings contextuais são indispensáveis para capturar a complexidade do discurso político."
        </div>
    </div>

    <h2>💡 Perguntas da Banca e Respostas Rápidas</h2>

    <div class="callout callout-warning">
        <div class="callout-title">❓ Pergunta 1: Por que a MLP superou o Naive Bayes no Brasil se ambas usaram Bag-of-Words?</div>
        <strong>Resposta:</strong> "O Naive Bayes assume que a presença de uma palavra não influencia a outra. A MLP passa as palavras por neurônios na camada oculta, aprendendo que a presença simultânea de certas palavras (ex: 'redução' + 'impostos') altera a classificação para Direita, algo que o Naive Bayes não consegue computar."
    </div>

    <div class="callout callout-warning">
        <div class="callout-title">❓ Pergunta 2: Por que a Bi-LSTM teve desempenho inferior (67%) no dataset brasileiro?</div>
        <strong>Resposta:</strong> "Redes recorrentes como a Bi-LSTM precisam treinar a matriz de embeddings e os gates da LSTM a partir do zero. Com apenas 300 textos, o modelo sofreu overfitting. O BERTimbau evitou isso porque utiliza Transfer Learning: ele já foi pré-treinado em bilhões de frases em português."
    </div>

    <div class="callout callout-warning">
        <div class="callout-title">❓ Pergunta 3: Como funcionou o Fine-Tuning do BERTimbau no código PyTorch?</div>
        <strong>Resposta:</strong> "Carregamos o modelo pré-treinado `neuralmind/bert-base-portuguese-cased` e adicionamos uma camada linear de classificação de 2 classes no topo. Treinamos durante 3 épocas com o otimizador AdamW e taxa de aprendizado baixa (`2e-5`) para ajustar os pesos sem destruir o conhecimento semântico prévio do modelo."
    </div>

</body>
</html>
"""

# Replace placeholders
html_content = html_content.replace("__IMG_COMPARACAO__", img_comparacao)
html_content = html_content.replace("__IMG_BOW__", img_cm_bow)
html_content = html_content.replace("__IMG_MLP__", img_cm_mlp)
html_content = html_content.replace("__IMG_BERT__", img_cm_bert)

html_path = "/tmp/guia_estudo.html"
pdf_path = "/home/joaolima/Projetos/analise-vies-politico/Guia_Estudo_Vies_Politico.pdf"

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print("HTML gerado com sucesso!")

# Generate PDF with Google Chrome
cmd = f"google-chrome --headless --no-sandbox --disable-gpu --print-to-pdf={pdf_path} {html_path}"
subprocess.run(cmd, shell=True, check=True)

print(f"PDF gerado com sucesso em: {pdf_path}")
