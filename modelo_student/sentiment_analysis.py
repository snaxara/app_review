import pandas as pd
from transformers import pipeline
import os

# --- Configurações ---
CSV_PATH = 'app_review_ex.csv'  # Arquivo no mesmo diretório
MODEL_NAME = 'lxyuan/distilbert-base-multilingual-cased-sentiments-student'
OUTPUT_CSV_PATH = 'sentiment_results.csv'
REPORT_PATH = 'sentiment_report.md'

# Coluna que contém o texto da avaliação
TEXT_COLUMN = 'content' 

# --- Funções ---

def load_data(path):
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
        
        # Limitar para teste inicial (1000 primeiras linhas)
        if len(df) > 1000:
            print(f"Dataset com {len(df)} linhas. Limitando para 1000 para teste inicial.")
            df = df.head(1000)
            
        print(f"Dataset carregado: {len(df)} avaliações.")
        return df
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        return None

def analyze_sentiment(df):
    """Executa a análise de sentimentos usando o modelo DistilBERT."""
    print(f"\nCarregando modelo: {MODEL_NAME}...")
    print("(Primeira execução pode demorar alguns minutos para download do modelo)")
    
    try:
        sentiment_pipeline = pipeline(
            "sentiment-analysis", 
            model=MODEL_NAME, 
            tokenizer=MODEL_NAME
        )
        
        texts = df[TEXT_COLUMN].tolist()
        
        print(f"\nIniciando análise de sentimentos em {len(texts)} textos...")
        print("Aguarde... (isso pode levar alguns minutos)")
        
        results = sentiment_pipeline(texts, batch_size=16)
        
        labels = [res['label'] for res in results]
        scores = [res['score'] for res in results]
        
        df['sentiment_label'] = labels
        df['sentiment_score'] = scores
        
        print("\nAnálise de sentimentos concluída!")
        return df
        
    except Exception as e:
        print(f"\nErro ao executar o pipeline de sentimentos: {e}")
        return None

def generate_report(df):
    """Gera um relatório Markdown com estatísticas da análise."""
    
    total_reviews = len(df)
    sentiment_counts = df['sentiment_label'].value_counts().to_dict()
    
    report_content = f"""# Relatório de Análise de Sentimentos

## Visão Geral
- Modelo: {MODEL_NAME}
- Total de Avaliações: {total_reviews}
- Arquivo de Entrada: {CSV_PATH}
- Arquivo de Saída: {OUTPUT_CSV_PATH}

## Distribuição de Sentimentos

| Sentimento | Contagem | Porcentagem |
|:-----------|:---------|:------------|
"""
    
    for label, count in sentiment_counts.items():
        percentage = (count / total_reviews) * 100
        report_content += f"| {label} | {count} | {percentage:.2f}% |\n"
        
    report_content += "\n## Amostras de Resultados (Top 5 Negativos)\n\n"
    
    negative_samples = df[df['sentiment_label'] == 'negative'].head(5)
    
    if not negative_samples.empty:
        for idx, row in negative_samples.iterrows():
            text_preview = row[TEXT_COLUMN][:200] if len(row[TEXT_COLUMN]) > 200 else row[TEXT_COLUMN]
            report_content += f"""### Avaliação ID: {row.get('reviewId', idx)}
- Texto: {text_preview}...
- Sentimento: {row['sentiment_label']} (Confiança: {row['sentiment_score']:.4f})
- Score Original: {row.get('score', 'N/A')}

"""
    else:
        report_content += "Nenhuma amostra negativa encontrada.\n"
        
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(report_content)
        
    print(f"Relatório gerado em: {REPORT_PATH}")

# --- Execução Principal ---

if __name__ == "__main__":
    print("="*60)
    print("ANALISE DE SENTIMENTOS")
    print("="*60)
    
    # 1. Carregar Dados
    print(f"\nCarregando dados de: {CSV_PATH}")
    df_reviews = load_data(CSV_PATH)
    
    if df_reviews is not None and not df_reviews.empty:
        # 2. Analisar Sentimentos
        print("\nExecutando análise de sentimentos...")
        df_results = analyze_sentiment(df_reviews)
        
        if df_results is not None:
            # 3. Salvar Resultados
            print(f"\nSalvando resultados...")
            df_results.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
            print(f"Resultados salvos em: {OUTPUT_CSV_PATH}")
            
            # 4. Gerar Relatório
            print(f"\nGerando relatório...")
            generate_report(df_results)
            
            print("\n" + "="*60)
            print("PROCESSO CONCLUIDO")
            print("="*60)
            print(f"\nArquivos gerados:")
            print(f"   {OUTPUT_CSV_PATH}")
            print(f"   {REPORT_PATH}")
    else:
        print("\nFalha no carregamento dos dados. Processo interrompido.")
        print("Verifique se o arquivo CSV está no diretório correto.")
