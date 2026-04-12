"""
Script para comparar diferentes modelos de análise de sentimentos
Permite testar múltiplos modelos e comparar resultados
"""

import pandas as pd
from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import os
from datetime import datetime

# --- Configurações ---
CSV_PATH = 'app_review_ex.csv'
OUTPUT_CSV_PATH = 'sentiment_results_comparison.csv'
REPORT_PATH = 'sentiment_comparison_report.md'

# Coluna que contém o texto da avaliação
TEXT_COLUMN = 'content'

# Modelos para testar
MODELS_TO_TEST = [
    {
        'name': 'DistilBERT Multilíngue (Atual)',
        'model_id': 'lxyuan/distilbert-base-multilingual-cased-sentiments-student',
        'task': 'sentiment-analysis'
    },
    {
        'name': 'BERT Português + Classificador',
        'model_id': 'neuralmind/bert-base-portuguese-cased',
        'task': 'sentiment-analysis',
        'note': 'Pode precisar de fine-tuning ou usar com classificador'
    },
    {
        'name': 'BERTweet PT-BR',
        'model_id': 'cardiffnlp/twitter-xlm-roberta-base-sentiment',
        'task': 'sentiment-analysis',
        'note': 'Treinado em dados de redes sociais'
    }
]

# Limite de avaliações para teste (None = todas)
LIMIT_REVIEWS = 100

# --- Funções ---

def load_data(path, limit=None):
    """Carrega o CSV, tratando o formato de separação e aspas."""
    try:
        df = pd.read_csv(path, sep=',', quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
        
        # Limpar colunas com sufixo ';;;;'
        df.columns = [col.split(';;;;')[0] for col in df.columns]
        
        if TEXT_COLUMN not in df.columns:
            print(f"Aviso: Coluna '{TEXT_COLUMN}' não encontrada.")
            print(f"Colunas disponíveis: {list(df.columns)}")
            return None
        
        # Limpeza: remover linhas com valores nulos na coluna de texto
        df.dropna(subset=[TEXT_COLUMN], inplace=True)
        
        if limit and len(df) > limit:
            print(f"Dataset com {len(df)} linhas. Limitando para {limit} para teste.")
            df = df.head(limit)
            
        print(f"Dataset carregado: {len(df)} avaliações.")
        return df
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        return None

def analyze_with_model(df, model_config):
    """Analisa sentimentos usando um modelo específico."""
    model_name = model_config['name']
    model_id = model_config['model_id']
    task = model_config.get('task', 'sentiment-analysis')
    
    print(f"\n{'='*60}")
    print(f"Testando: {model_name}")
    print(f"Modelo: {model_id}")
    print(f"{'='*60}")
    
    try:
        print(f"Carregando modelo... (primeira execução pode demorar)")
        
        # Tentar criar pipeline
        try:
            sentiment_pipeline = pipeline(
                task,
                model=model_id,
                tokenizer=model_id
            )
        except Exception as e:
            print(f"Erro ao carregar modelo: {e}")
            print("Tentando carregar apenas o tokenizer...")
            
            # Tentar carregar tokenizer e modelo separadamente
            try:
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = AutoModelForSequenceClassification.from_pretrained(model_id)
                sentiment_pipeline = pipeline(
                    task,
                    model=model,
                    tokenizer=tokenizer
                )
            except Exception as e2:
                print(f"Erro ao carregar modelo alternativo: {e2}")
                return None
        
        texts = df[TEXT_COLUMN].tolist()
        
        print(f"Processando {len(texts)} textos...")
        results = sentiment_pipeline(texts, batch_size=16)
        
        # Extrair labels e scores
        labels = []
        scores = []
        
        for res in results:
            if isinstance(res, dict):
                # Formato padrão: {'label': '...', 'score': ...}
                labels.append(res.get('label', 'unknown'))
                scores.append(res.get('score', 0.0))
            elif isinstance(res, list) and len(res) > 0:
                # Formato alternativo: [{'label': '...', 'score': ...}]
                labels.append(res[0].get('label', 'unknown'))
                scores.append(res[0].get('score', 0.0))
            else:
                labels.append('unknown')
                scores.append(0.0)
        
        # Normalizar labels (alguns modelos usam diferentes convenções)
        normalized_labels = []
        for label in labels:
            label_lower = label.lower()
            if 'pos' in label_lower or 'posit' in label_lower:
                normalized_labels.append('positive')
            elif 'neg' in label_lower:
                normalized_labels.append('negative')
            elif 'neu' in label_lower:
                normalized_labels.append('neutral')
            else:
                normalized_labels.append(label)
        
        print(f"Análise concluída!")
        print(f"Distribuição: {pd.Series(normalized_labels).value_counts().to_dict()}")
        
        return {
            'labels': normalized_labels,
            'scores': scores,
            'model_name': model_name,
            'model_id': model_id
        }
        
    except Exception as e:
        print(f"Erro ao executar análise: {e}")
        import traceback
        traceback.print_exc()
        return None

def compare_models(df, model_configs):
    """Compara resultados de múltiplos modelos."""
    results = {}
    
    for model_config in model_configs:
        result = analyze_with_model(df, model_config)
        if result:
            results[model_config['name']] = result
    
    return results

def generate_comparison_report(df, comparison_results):
    """Gera relatório comparativo dos modelos."""
    
    report = f"""# Relatório Comparativo de Modelos de Análise de Sentimentos

Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}
Total de Avaliações: {len(df)}

---

## Modelos Testados

"""
    
    for model_name, result in comparison_results.items():
        labels = result['labels']
        scores = result['scores']
        
        # Estatísticas
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
        report += "---\n\n"
    
    # Comparação lado a lado
    report += """## Comparação Lado a Lado

| Avaliação | Score Original | """
    
    for model_name in comparison_results.keys():
        report += f"{model_name} | "
    report += "\n|:-----------|:---------------|"
    
    for _ in comparison_results:
        report += ":-----------|"
    report += "\n"
    
    # Mostrar primeiras 10 avaliações como exemplo
    for idx in range(min(10, len(df))):
        row = df.iloc[idx]
        text_preview = row[TEXT_COLUMN][:50] + "..." if len(row[TEXT_COLUMN]) > 50 else row[TEXT_COLUMN]
        report += f"| {text_preview} | {row.get('score', 'N/A')} | "
        
        for model_name, result in comparison_results.items():
            label = result['labels'][idx]
            score = result['scores'][idx]
            report += f"{label} ({score:.2f}) | "
        
        report += "\n"
    
    report += "\n---\n\n## Recomendações\n\n"
    
    # Análise de consistência
    if len(comparison_results) > 1:
        report += "### Consistência entre Modelos\n\n"
        
        # Comparar primeiras 10 avaliações
        agreements = 0
        total = min(10, len(df))
        
        for idx in range(total):
            labels_for_review = [result['labels'][idx] for result in comparison_results.values()]
            if len(set(labels_for_review)) == 1:  # Todos concordam
                agreements += 1
        
        agreement_rate = (agreements / total) * 100
        report += f"Taxa de concordância nas primeiras {total} avaliações: {agreement_rate:.1f}%\n\n"
        
        if agreement_rate < 70:
            report += "⚠️ **Atenção:** Baixa concordância entre modelos. Recomenda-se validação manual.\n\n"
        elif agreement_rate < 90:
            report += "🟡 **Moderado:** Concordância moderada. Algumas diferenças esperadas.\n\n"
        else:
            report += "✅ **Bom:** Alta concordância entre modelos.\n\n"
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\nRelatório comparativo gerado em: {REPORT_PATH}")

# --- Execução Principal ---

if __name__ == "__main__":
    print("="*60)
    print("COMPARACAO DE MODELOS DE ANALISE DE SENTIMENTOS")
    print("="*60)
    
    # 1. Carregar Dados
    print(f"\nCarregando dados de: {CSV_PATH}")
    df_reviews = load_data(CSV_PATH, limit=LIMIT_REVIEWS)
    
    if df_reviews is not None and not df_reviews.empty:
        # 2. Comparar Modelos
        print("\nIniciando comparação de modelos...")
        comparison_results = compare_models(df_reviews, MODELS_TO_TEST)
        
        if comparison_results:
            # 3. Salvar Resultados
            print(f"\nSalvando resultados...")
            
            # Criar DataFrame com resultados de todos os modelos
            df_results = df_reviews.copy()
            
            for model_name, result in comparison_results.items():
                df_results[f'sentiment_label_{model_name.replace(" ", "_")}'] = result['labels']
                df_results[f'sentiment_score_{model_name.replace(" ", "_")}'] = result['scores']
            
            df_results.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
            print(f"Resultados salvos em: {OUTPUT_CSV_PATH}")
            
            # 4. Gerar Relatório Comparativo
            print(f"\nGerando relatório comparativo...")
            generate_comparison_report(df_reviews, comparison_results)
            
            print("\n" + "="*60)
            print("PROCESSO CONCLUIDO")
            print("="*60)
            print(f"\nArquivos gerados:")
            print(f"   {OUTPUT_CSV_PATH}")
            print(f"   {REPORT_PATH}")
        else:
            print("\nNenhum modelo foi executado com sucesso.")
    else:
        print("\nFalha no carregamento dos dados. Processo interrompido.")

