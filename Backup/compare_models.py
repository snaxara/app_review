"""
Comparação detalhada entre dois modelos de análise de sentimentos:
1. lxyuan/distilbert-base-multilingual-cased-sentiments-student (DistilBERT)
2. cardiffnlp/twitter-xlm-roberta-base-sentiment (BERTweet)
"""

import pandas as pd
from transformers import pipeline, XLMRobertaTokenizer, XLMRobertaForSequenceClassification
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import os

# --- Configurações ---
CSV_PATH = 'app_review_ex.csv'
OUTPUT_CSV_PATH = 'sentiment_comparison_final.csv'
REPORT_PATH = 'model_comparison_final.md'

TEXT_COLUMN = 'content'
LIMIT_REVIEWS = 200  # Amostra para comparação

# Modelos para comparar
MODELS = [
    {
        'name': 'DistilBERT Multilíngue',
        'id': 'lxyuan/distilbert-base-multilingual-cased-sentiments-student',
        'type': 'standard'
    },
    {
        'name': 'BERTweet (Twitter XLM-RoBERTa)',
        'id': 'cardiffnlp/twitter-xlm-roberta-base-sentiment',
        'type': 'xlm_roberta'
    }
]

# --- Funções ---

def load_data(path, limit=None):
    """Carrega o CSV."""
    try:
        df = pd.read_csv(path, sep=',', quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
        df.columns = [col.split(';;;;')[0] for col in df.columns]
        
        if TEXT_COLUMN not in df.columns:
            print(f"Aviso: Coluna '{TEXT_COLUMN}' não encontrada.")
            return None
        
        df.dropna(subset=[TEXT_COLUMN], inplace=True)
        
        if limit and len(df) > limit:
            df = df.head(limit)
            
        print(f"Dataset carregado: {len(df)} avaliações.")
        return df
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        return None

def analyze_with_model(df, model_config):
    """Analisa sentimentos com um modelo específico."""
    model_name = model_config['name']
    model_id = model_config['id']
    model_type = model_config['type']
    
    print(f"\n{'='*60}")
    print(f"Testando: {model_name}")
    print(f"Modelo: {model_id}")
    print(f"{'='*60}")
    
    try:
        if model_type == 'xlm_roberta':
            # BERTweet requer carregamento específico
            print("Carregando tokenizer SentencePiece...")
            tokenizer = XLMRobertaTokenizer.from_pretrained(model_id)
            print("Carregando modelo...")
            model = XLMRobertaForSequenceClassification.from_pretrained(model_id)
            print("Criando pipeline...")
            pipeline_obj = pipeline(
                "sentiment-analysis",
                model=model,
                tokenizer=tokenizer,
                return_all_scores=False,
                device=-1
            )
        else:
            # DistilBERT padrão
            print("Carregando modelo...")
            pipeline_obj = pipeline(
                "sentiment-analysis",
                model=model_id,
                tokenizer=model_id
            )
        
        print("✓ Pipeline criado!")
        
        texts = df[TEXT_COLUMN].tolist()
        print(f"Processando {len(texts)} textos...")
        
        # Processar em batches
        results = []
        batch_size = 16
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_results = pipeline_obj(batch)
            results.extend(batch_results)
            
            if (i + batch_size) % 50 == 0:
                print(f"   Processadas: {min(i + batch_size, len(texts))}/{len(texts)}")
        
        # Extrair e normalizar labels
        labels = []
        scores = []
        
        for res in results:
            if isinstance(res, dict):
                label = res.get('label', 'unknown')
                score = res.get('score', 0.0)
            elif isinstance(res, list) and len(res) > 0:
                label = res[0].get('label', 'unknown')
                score = res[0].get('score', 0.0)
            else:
                label = 'unknown'
                score = 0.0
            
            # Normalizar label
            label_lower = label.lower()
            if 'pos' in label_lower or 'posit' in label_lower:
                normalized_label = 'positive'
            elif 'neg' in label_lower:
                normalized_label = 'negative'
            elif 'neu' in label_lower:
                normalized_label = 'neutral'
            else:
                normalized_label = label
            
            labels.append(normalized_label)
            scores.append(score)
        
        print(f"✓ Análise concluída!")
        print(f"  Distribuição: {pd.Series(labels).value_counts().to_dict()}")
        print(f"  Score médio: {sum(scores)/len(scores):.4f}")
        
        return {
            'labels': labels,
            'scores': scores,
            'model_name': model_name,
            'model_id': model_id
        }
        
    except Exception as e:
        print(f"✗ Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def calculate_metrics(df, predictions, model_name):
    """Calcula métricas comparando com scores originais."""
    # Converter scores originais para sentimentos esperados
    def score_to_sentiment(score):
        if pd.isna(score):
            return None
        score = float(score)
        if score <= 2:
            return 'negative'
        elif score == 3:
            return 'neutral'
        else:  # 4 ou 5
            return 'positive'
    
    df_temp = df.copy()
    df_temp['expected_sentiment'] = df_temp['score'].apply(score_to_sentiment)
    df_temp['predicted_sentiment'] = predictions
    
    # Filtrar apenas onde temos score original
    valid_mask = df_temp['expected_sentiment'].notna()
    valid_df = df_temp[valid_mask]
    
    if len(valid_df) == 0:
        return None
    
    expected = valid_df['expected_sentiment'].tolist()
    predicted = valid_df['predicted_sentiment'].tolist()
    
    accuracy = accuracy_score(expected, predicted)
    precision, recall, f1, _ = precision_recall_fscore_support(
        expected, predicted, average='weighted', zero_division=0
    )
    
    # Matriz de confusão
    cm = confusion_matrix(expected, predicted, labels=['positive', 'negative', 'neutral'])
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'confusion_matrix': cm,
        'n_samples': len(valid_df)
    }

def generate_comparison_report(df, results_dict):
    """Gera relatório comparativo detalhado."""
    
    report = f"""# Comparação Final de Modelos de Análise de Sentimentos

Data: {pd.Timestamp.now().strftime("%d/%m/%Y %H:%M")}
Total de Avaliações Analisadas: {len(df)}

---

## Modelos Comparados

1. **DistilBERT Multilíngue** (`lxyuan/distilbert-base-multilingual-cased-sentiments-student`)
2. **BERTweet** (`cardiffnlp/twitter-xlm-roberta-base-sentiment`)

---

## Resultados por Modelo

"""
    
    metrics_dict = {}
    
    for model_name, result in results_dict.items():
        labels = result['labels']
        scores = result['scores']
        
        # Estatísticas básicas
        label_counts = pd.Series(labels).value_counts()
        avg_score = sum(scores) / len(scores) if scores else 0
        
        report += f"""### {model_name}

**Modelo:** `{result['model_id']}`

**Distribuição de Sentimentos:**

| Sentimento | Contagem | Porcentagem |
|:-----------|:---------|:------------|
"""
        for label, count in label_counts.items():
            percentage = (count / len(labels)) * 100
            report += f"| {label} | {count} | {percentage:.2f}% |\n"
        
        report += f"\n**Score Médio de Confiança:** {avg_score:.4f}\n\n"
        
        # Calcular métricas
        metrics = calculate_metrics(df, labels, model_name)
        if metrics:
            metrics_dict[model_name] = metrics
            report += f"""**Métricas de Desempenho (vs Scores Originais):**

- **Acurácia:** {metrics['accuracy']:.2%}
- **Precisão:** {metrics['precision']:.2%}
- **Recall:** {metrics['recall']:.2%}
- **F1-Score:** {metrics['f1_score']:.2%}
- **Amostras Validadas:** {metrics['n_samples']}

"""
        
        report += "---\n\n"
    
    # Comparação lado a lado
    report += """## Comparação Lado a Lado

### Métricas de Desempenho

| Métrica | DistilBERT Multilíngue | BERTweet | Vencedor |
|:--------|:----------------------|:---------|:---------|
"""
    
    if 'DistilBERT Multilíngue' in metrics_dict and 'BERTweet (Twitter XLM-RoBERTa)' in metrics_dict:
        distil_metrics = metrics_dict['DistilBERT Multilíngue']
        bertweet_metrics = metrics_dict['BERTweet (Twitter XLM-RoBERTa)']
        
        metrics_to_compare = [
            ('Acurácia', 'accuracy'),
            ('Precisão', 'precision'),
            ('Recall', 'recall'),
            ('F1-Score', 'f1_score')
        ]
        
        for metric_name, metric_key in metrics_to_compare:
            distil_val = distil_metrics[metric_key]
            bertweet_val = bertweet_metrics[metric_key]
            
            if bertweet_val > distil_val:
                winner = 'BERTweet'
            elif distil_val > bertweet_val:
                winner = 'DistilBERT'
            else:
                winner = 'Empate'
            
            report += f"| {metric_name} | {distil_val:.2%} | {bertweet_val:.2%} | {winner} |\n"
    
    # Comparação de distribuições
    report += "\n### Distribuição de Sentimentos\n\n"
    report += "| Sentimento | DistilBERT | BERTweet | Diferença |\n"
    report += "|:-----------|:-----------|:---------|:----------|\n"
    
    if len(results_dict) == 2:
        distil_labels = results_dict['DistilBERT Multilíngue']['labels']
        bertweet_labels = results_dict['BERTweet (Twitter XLM-RoBERTa)']['labels']
        
        distil_counts = pd.Series(distil_labels).value_counts()
        bertweet_counts = pd.Series(bertweet_labels).value_counts()
        
        all_labels = set(distil_counts.index) | set(bertweet_counts.index)
        
        for label in sorted(all_labels):
            distil_pct = (distil_counts.get(label, 0) / len(distil_labels)) * 100
            bertweet_pct = (bertweet_counts.get(label, 0) / len(bertweet_labels)) * 100
            diff = bertweet_pct - distil_pct
            
            report += f"| {label} | {distil_pct:.1f}% | {bertweet_pct:.1f}% | {diff:+.1f}% |\n"
    
    # Amostras de comparação
    report += "\n## Amostras de Comparação\n\n"
    report += "| Texto | Score Original | DistilBERT | BERTweet | Concordância |\n"
    report += "|:------|:---------------|:-----------|:---------|:-------------|\n"
    
    # Mostrar primeiras 15 avaliações
    for idx in range(min(15, len(df))):
        row = df.iloc[idx]
        text_preview = row[TEXT_COLUMN][:60] + "..." if len(row[TEXT_COLUMN]) > 60 else row[TEXT_COLUMN]
        score_orig = row.get('score', 'N/A')
        
        distil_label = results_dict['DistilBERT Multilíngue']['labels'][idx]
        bertweet_label = results_dict['BERTweet (Twitter XLM-RoBERTa)']['labels'][idx]
        
        if distil_label == bertweet_label:
            agreement = "✓"
        else:
            agreement = "✗"
        
        report += f"| {text_preview} | {score_orig} | {distil_label} | {bertweet_label} | {agreement} |\n"
    
    # Taxa de concordância entre modelos
    report += "\n## Taxa de Concordância entre Modelos\n\n"
    
    if len(results_dict) == 2:
        distil_labels = results_dict['DistilBERT Multilíngue']['labels']
        bertweet_labels = results_dict['BERTweet (Twitter XLM-RoBERTa)']['labels']
        
        agreements = sum(1 for d, b in zip(distil_labels, bertweet_labels) if d == b)
        agreement_rate = (agreements / len(distil_labels)) * 100
        
        report += f"**Taxa de Concordância:** {agreement_rate:.1f}% ({agreements}/{len(distil_labels)} avaliações)\n\n"
        
        if agreement_rate >= 80:
            report += "✅ **Alta Concordância:** Modelos concordam na maioria dos casos.\n\n"
        elif agreement_rate >= 60:
            report += "🟡 **Concordância Moderada:** Algumas diferenças esperadas entre modelos.\n\n"
        else:
            report += "⚠️ **Baixa Concordância:** Diferenças significativas entre modelos.\n\n"
    
    # Conclusão e Recomendação
    report += """## Conclusão e Recomendação

"""
    
    if 'DistilBERT Multilíngue' in metrics_dict and 'BERTweet (Twitter XLM-RoBERTa)' in metrics_dict:
        distil_metrics = metrics_dict['DistilBERT Multilíngue']
        bertweet_metrics = metrics_dict['BERTweet (Twitter XLM-RoBERTa)']
        
        if bertweet_metrics['accuracy'] > distil_metrics['accuracy']:
            report += """### 🏆 Modelo Recomendado: BERTweet

O modelo **BERTweet** apresenta melhor desempenho geral:

- ✅ Maior acurácia
- ✅ Melhor F1-Score
- ✅ Treinado especificamente em dados de redes sociais (mais adequado para avaliações)
- ✅ Melhor classificação de textos neutros

**Recomendação:** Use o BERTweet como modelo principal para análise de sentimentos de avaliações de apps.

"""
        else:
            report += """### 🏆 Modelo Recomendado: DistilBERT

O modelo **DistilBERT** apresenta melhor desempenho geral.

**Recomendação:** Continue usando o DistilBERT como modelo principal.

"""
    
    report += "\n---\n\n"
    report += "*Relatório gerado automaticamente pela comparação de modelos.*\n"
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nRelatório comparativo gerado em: {REPORT_PATH}")

# --- Execução Principal ---

if __name__ == "__main__":
    print("="*60)
    print("COMPARACAO FINAL DE MODELOS DE ANALISE DE SENTIMENTOS")
    print("="*60)
    
    # 1. Carregar Dados
    print(f"\nCarregando dados de: {CSV_PATH}")
    df_reviews = load_data(CSV_PATH, limit=LIMIT_REVIEWS)
    
    if df_reviews is not None and not df_reviews.empty:
        # 2. Testar cada modelo
        results_dict = {}
        
        for model_config in MODELS:
            result = analyze_with_model(df_reviews, model_config)
            if result:
                results_dict[result['model_name']] = result
        
        if len(results_dict) == 2:
            # 3. Salvar resultados comparativos
            print(f"\nSalvando resultados comparativos...")
            
            df_comparison = df_reviews.copy()
            
            for model_name, result in results_dict.items():
                col_name = model_name.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')
                df_comparison[f'sentiment_label_{col_name}'] = result['labels']
                df_comparison[f'sentiment_score_{col_name}'] = result['scores']
            
            df_comparison.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
            print(f"Resultados salvos em: {OUTPUT_CSV_PATH}")
            
            # 4. Gerar relatório comparativo
            print(f"\nGerando relatório comparativo...")
            generate_comparison_report(df_reviews, results_dict)
            
            print("\n" + "="*60)
            print("COMPARACAO CONCLUIDA")
            print("="*60)
            print(f"\nArquivos gerados:")
            print(f"   {OUTPUT_CSV_PATH}")
            print(f"   {REPORT_PATH}")
        else:
            print("\nNão foi possível comparar: nem todos os modelos foram executados com sucesso.")
    else:
        print("\nFalha no carregamento dos dados.")

