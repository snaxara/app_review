"""
Teste do modelo cardiffnlp/twitter-xlm-roberta-base-sentiment para análise de sentimentos

Este modelo é treinado especificamente em dados de redes sociais (tweets),
o que pode ser mais adequado para avaliações de apps que têm linguagem similar.
"""

import pandas as pd
from transformers import pipeline
import os

# --- Configurações ---
CSV_PATH = 'app_review_ex.csv'
MODEL_NAME = 'cardiffnlp/twitter-xlm-roberta-base-sentiment'
OUTPUT_CSV_PATH = 'sentiment_results_bertweet.csv'
REPORT_PATH = 'sentiment_report_bertweet.md'

# Coluna que contém o texto da avaliação
TEXT_COLUMN = 'content'

# Limite de avaliações para teste
LIMIT_REVIEWS = 100

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

def analyze_sentiment(df):
    """Analisa sentimentos usando o modelo BERTweet."""
    print(f"\nCarregando modelo: {MODEL_NAME}...")
    print("Este modelo é treinado em dados de redes sociais (tweets).")
    print("(Primeira execução pode demorar alguns minutos para download do modelo)\n")
    
    try:
        # Criar pipeline de sentiment-analysis
        print("Criando pipeline de análise de sentimentos...")
        
        # Este modelo tem problemas conhecidos com o tokenizer fast
        # Vamos usar uma abordagem mais direta
        from transformers import AutoTokenizer, AutoModelForSequenceClassification
        from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
        import torch
        
        print("Carregando tokenizer SentencePiece...")
        # Usar o tokenizer SentencePiece diretamente
        tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_NAME)
        
        print("Carregando modelo...")
        model = XLMRobertaForSequenceClassification.from_pretrained(MODEL_NAME)
        
        print("Criando pipeline...")
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
            return_all_scores=False,
            device=-1  # Usar CPU
        )
        print("✓ Pipeline criado com sucesso!")
        
        texts = df[TEXT_COLUMN].tolist()
        
        print(f"\nProcessando {len(texts)} textos...")
        print("Aguarde... (isso pode levar alguns minutos)")
        
        # Processar em batches menores para evitar problemas de memória
        results = []
        batch_size = 16
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_results = sentiment_pipeline(batch)
            results.extend(batch_results)
            
            if (i + batch_size) % 50 == 0:
                print(f"   Processadas: {min(i + batch_size, len(texts))}/{len(texts)}")
        
        # Extrair labels e scores
        labels = []
        scores = []
        
        for res in results:
            if isinstance(res, dict):
                label = res.get('label', 'unknown')
                score = res.get('score', 0.0)
                
                # Normalizar labels do modelo (pode usar diferentes convenções)
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
            elif isinstance(res, list) and len(res) > 0:
                # Se retornar lista, pegar o primeiro resultado
                first_res = res[0]
                label = first_res.get('label', 'unknown')
                score = first_res.get('score', 0.0)
                
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
            else:
                labels.append('unknown')
                scores.append(0.0)
        
        df['sentiment_label'] = labels
        df['sentiment_score'] = scores
        
        print("\nAnálise concluída!")
        print(f"Distribuição: {df['sentiment_label'].value_counts().to_dict()}")
        print(f"Score médio: {df['sentiment_score'].mean():.4f}")
        
        return df
        
    except Exception as e:
        print(f"\nErro ao executar análise: {e}")
        import traceback
        traceback.print_exc()
        return None

def generate_report(df):
    """Gera relatório."""
    total_reviews = len(df)
    sentiment_counts = df['sentiment_label'].value_counts().to_dict()
    avg_score = df['sentiment_score'].mean()
    
    report_content = f"""# Relatório de Análise de Sentimentos - BERTweet

## Visão Geral
- Modelo: {MODEL_NAME}
- Total de Avaliações: {total_reviews}
- Arquivo de Entrada: {CSV_PATH}
- Arquivo de Saída: {OUTPUT_CSV_PATH}
- Score Médio de Confiança: {avg_score:.4f}

## Sobre o Modelo

Este modelo (`cardiffnlp/twitter-xlm-roberta-base-sentiment`) é treinado especificamente 
em dados de redes sociais (tweets), o que pode ser mais adequado para avaliações de apps 
que têm linguagem similar e informal.

## Distribuição de Sentimentos

| Sentimento | Contagem | Porcentagem |
|:-----------|:---------|:------------|
"""
    
    for label, count in sentiment_counts.items():
        percentage = (count / total_reviews) * 100
        report_content += f"| {label} | {count} | {percentage:.2f}% |\n"
    
    report_content += "\n## Amostras de Resultados\n\n"
    
    # Amostras por sentimento
    for sentiment in ['positive', 'negative', 'neutral']:
        if sentiment in sentiment_counts:
            samples = df[df['sentiment_label'] == sentiment].head(5)
            if not samples.empty:
                report_content += f"### {sentiment.capitalize()}\n\n"
                for idx, row in samples.iterrows():
                    text_preview = row[TEXT_COLUMN][:150] if len(row[TEXT_COLUMN]) > 150 else row[TEXT_COLUMN]
                    report_content += f"- **Score Original:** {row.get('score', 'N/A')} | **Confiança:** {row['sentiment_score']:.4f}\n"
                    report_content += f"  \"{text_preview}...\"\n\n"
    
    # Comparação com scores originais
    report_content += "\n## Análise de Consistência\n\n"
    
    # Converter scores originais para sentimentos esperados
    def score_to_expected_sentiment(score):
        if pd.isna(score):
            return None
        score = float(score)
        if score <= 2:
            return 'negative'
        elif score == 3:
            return 'neutral'
        else:  # 4 ou 5
            return 'positive'
    
    df['expected_sentiment'] = df['score'].apply(score_to_expected_sentiment)
    
    # Calcular concordância
    matches = df[df['expected_sentiment'].notna() & (df['sentiment_label'] == df['expected_sentiment'])].shape[0]
    total_with_score = df[df['expected_sentiment'].notna()].shape[0]
    
    if total_with_score > 0:
        accuracy = (matches / total_with_score) * 100
        report_content += f"**Taxa de Concordância com Scores Originais:** {accuracy:.1f}%\n"
        report_content += f"(Comparando {total_with_score} avaliações com scores disponíveis)\n\n"
        
        if accuracy >= 80:
            report_content += "✅ **Excelente:** Alta concordância com scores originais.\n\n"
        elif accuracy >= 60:
            report_content += "🟡 **Moderado:** Concordância moderada. Algumas diferenças esperadas.\n\n"
        else:
            report_content += "⚠️ **Atenção:** Baixa concordância. Pode precisar de ajustes.\n\n"
    
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"Relatório gerado em: {REPORT_PATH}")

# --- Execução Principal ---

if __name__ == "__main__":
    print("="*60)
    print("TESTE: BERTweet (Twitter XLM-RoBERTa)")
    print("="*60)
    
    print(f"\nCarregando dados de: {CSV_PATH}")
    df_reviews = load_data(CSV_PATH, limit=LIMIT_REVIEWS)
    
    if df_reviews is not None and not df_reviews.empty:
        print("\nExecutando análise de sentimentos...")
        df_results = analyze_sentiment(df_reviews)
        
        if df_results is not None:
            print(f"\nSalvando resultados...")
            df_results.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
            print(f"Resultados salvos em: {OUTPUT_CSV_PATH}")
            
            print(f"\nGerando relatório...")
            generate_report(df_results)
            
            print("\n" + "="*60)
            print("PROCESSO CONCLUIDO")
            print("="*60)
            print(f"\nArquivos gerados:")
            print(f"   {OUTPUT_CSV_PATH}")
            print(f"   {REPORT_PATH}")
        else:
            print("\nNão foi possível executar a análise com este modelo.")
    else:
        print("\nFalha no carregamento dos dados.")

