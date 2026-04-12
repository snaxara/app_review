"""
Script de análise de polarização de comentários usando modelo BERTweet.

Este script classifica cada comentário como positivo, negativo ou neutro
usando o modelo BERTweet pré-treinado. O modelo foi treinado com dados
de redes sociais, o que ajuda na análise de avaliações de aplicativos.
"""

import pandas as pd
from transformers import pipeline

# Arquivo de entrada com as avaliações coletadas
CSV_PATH = 'app_review_dataset.csv'

# Modelo BERTweet para análise de sentimentos
# Este modelo é multilíngue e funciona bem com português brasileiro
MODEL_NAME = 'cardiffnlp/twitter-xlm-roberta-base-sentiment'

# Arquivo de saída com os resultados da análise
OUTPUT_CSV_PATH = 'sentiment_results.csv'

# Nome da coluna que contém o texto das avaliações
TEXT_COLUMN = 'content'

def load_data(path):
    """
    Carrega o arquivo CSV com as avaliações dos aplicativos.
    
    O script tenta detectar automaticamente o separador usado no CSV
    (ponto e vírgula ou vírgula) para garantir compatibilidade.
    """
    try:
        # Tenta primeiro com ponto e vírgula, depois com vírgula
        try:
            df = pd.read_csv(path, sep=';', quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
            print(f"Arquivo carregado com separador ponto e vírgula")
        except:
            df = pd.read_csv(path, sep=',', quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
            print(f"Arquivo carregado com separador vírgula")
        
        # Remove sufixos estranhos das colunas que podem aparecer em alguns CSVs
        df.columns = [col.split(';;;;')[0] for col in df.columns]
        
        # Verifica se a coluna de texto existe no arquivo
        if TEXT_COLUMN not in df.columns:
            print(f"Erro: coluna '{TEXT_COLUMN}' não encontrada no arquivo")
            print(f"Colunas disponíveis: {list(df.columns)}")
            return None
        
        # Remove avaliações que não têm texto (comentários vazios)
        df.dropna(subset=[TEXT_COLUMN], inplace=True)
        
        print(f"Dataset carregado: {len(df)} avaliações")
        return df
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        import traceback
        traceback.print_exc()
        return None

def analyze_sentiment(df):
    """
    Executa a análise de polarização dos comentários usando o modelo BERTweet.
    
    O BERTweet é um modelo pré-treinado que funciona bem com português brasileiro
    e foi treinado com dados de redes sociais, o que ajuda na análise de avaliações.
    Na primeira execução, o modelo será baixado automaticamente.
    """
    print(f"\nCarregando modelo: {MODEL_NAME}")
    print("Este modelo foi treinado com dados de redes sociais, o que ajuda na análise de avaliações")
    print("A primeira execução pode demorar um pouco para baixar o modelo")
    
    try:
        from transformers import XLMRobertaTokenizer, XLMRobertaForSequenceClassification
        
        print("Carregando tokenizer...")
        tokenizer = XLMRobertaTokenizer.from_pretrained(MODEL_NAME)
        
        print("Carregando modelo...")
        model = XLMRobertaForSequenceClassification.from_pretrained(MODEL_NAME)
        
        print("Configurando pipeline de análise...")
        # Configura o pipeline de análise de sentimentos
        # device=-1 significa que vai usar CPU (não requer GPU)
        sentiment_pipeline = pipeline(
            "sentiment-analysis",
            model=model,
            tokenizer=tokenizer,
            return_all_scores=False,
            device=-1
        )
        
        texts = df[TEXT_COLUMN].tolist()
        
        print(f"\nIniciando análise de sentimentos em {len(texts)} textos")
        print("Aguarde, isso pode levar alguns minutos...")
        
        # Processa os textos em lotes para melhor performance
        # Processar tudo de uma vez pode consumir muita memória
        results = []
        batch_size = 16
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_results = sentiment_pipeline(batch)
            results.extend(batch_results)
            
            # Mostra progresso a cada 50 avaliações processadas
            if (i + batch_size) % 50 == 0:
                print(f"   Processadas: {min(i + batch_size, len(texts))}/{len(texts)}")
        
        # Extrai os resultados e normaliza os labels para um formato padrão
        labels = []
        scores = []
        
        for res in results:
            if isinstance(res, dict):
                label = res.get('label', 'unknown')
                score = res.get('score', 0.0)
                
                # Normaliza os labels para um formato padrão
                # O modelo pode retornar labels em diferentes formatos, então normalizamos
                label_lower = label.lower()
                if 'pos' in label_lower or 'posit' in label_lower:
                    normalized_label = 'positive'
                elif 'neg' in label_lower:
                    normalized_label = 'negative'
                elif 'neu' in label_lower:
                    normalized_label = 'neutral'
                else:
                    # Se não reconhecer, mantém o label original
                    normalized_label = label
                
                labels.append(normalized_label)
                scores.append(score)
            elif isinstance(res, list) and len(res) > 0:
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
        
        print("\nAnálise de sentimentos concluída")
        return df
        
    except Exception as e:
        print(f"\nErro ao executar a análise de sentimentos: {e}")
        return None

def generate_comparison_stats(df):
    """Gera estatísticas comparativas entre os apps Santander e Bradesco."""
    print("\n" + "="*60)
    print("ANALISE COMPARATIVA ENTRE APPS")
    print("="*60)
    
    # Verifica se existe a coluna app_name
    if 'app_name' not in df.columns:
        print("Aviso: coluna 'app_name' não encontrada, não é possível fazer comparação")
        return
    
    apps = df['app_name'].unique()
    print(f"\nApps encontrados: {', '.join(apps)}")
    
    # Estatísticas gerais por app
    print("\n--- Distribuição de Sentimentos por App ---")
    for app in apps:
        app_data = df[df['app_name'] == app]
        total = len(app_data)
        
        if total == 0:
            continue
        
        sentiment_counts = app_data['sentiment_label'].value_counts()
        
        print(f"\n{app}:")
        print(f"  Total de avaliações: {total}")
        
        for sentiment in ['positive', 'negative', 'neutral']:
            count = sentiment_counts.get(sentiment, 0)
            percentage = (count / total) * 100
            print(f"  {sentiment.capitalize()}: {count} ({percentage:.2f}%)")
    
    # Comparação de scores médios
    print("\n--- Score Médio por App ---")
    if 'score' in df.columns:
        for app in apps:
            app_data = df[df['app_name'] == app]
            avg_score = app_data['score'].mean()
            print(f"  {app}: {avg_score:.2f} estrelas")
    
    # Comparação de sentimentos
    print("\n--- Comparação de Percentuais ---")
    comparison_data = []
    for app in apps:
        app_data = df[df['app_name'] == app]
        total = len(app_data)
        
        if total == 0:
            continue
        
        positive_pct = (len(app_data[app_data['sentiment_label'] == 'positive']) / total) * 100
        negative_pct = (len(app_data[app_data['sentiment_label'] == 'negative']) / total) * 100
        neutral_pct = (len(app_data[app_data['sentiment_label'] == 'neutral']) / total) * 100
        
        comparison_data.append({
            'app': app,
            'positive': positive_pct,
            'negative': negative_pct,
            'neutral': neutral_pct
        })
        
        print(f"\n{app}:")
        print(f"  Positivo: {positive_pct:.2f}%")
        print(f"  Negativo: {negative_pct:.2f}%")
        print(f"  Neutro: {neutral_pct:.2f}%")
    
    # Diferencial entre apps
    if len(comparison_data) == 2:
        print("\n--- Diferencial entre Apps ---")
        app1 = comparison_data[0]
        app2 = comparison_data[1]
        
        positive_diff = app1['positive'] - app2['positive']
        negative_diff = app1['negative'] - app2['negative']
        
        print(f"Diferença em avaliações positivas: {positive_diff:+.2f} pontos percentuais")
        print(f"  ({app1['app']} tem {abs(positive_diff):.2f}% {'mais' if positive_diff > 0 else 'menos'} positivas que {app2['app']})")
        
        print(f"Diferença em avaliações negativas: {negative_diff:+.2f} pontos percentuais")
        print(f"  ({app1['app']} tem {abs(negative_diff):.2f}% {'mais' if negative_diff > 0 else 'menos'} negativas que {app2['app']})")

def print_final_stats(df):
    """Imprime estatísticas finais da análise."""
    print("\n" + "="*60)
    print("ESTATISTICAS FINAIS")
    print("="*60)
    
    total_reviews = len(df)
    sentiment_counts = df['sentiment_label'].value_counts()
    
    print(f"\nTotal de avaliações analisadas: {total_reviews}")
    print("\nDistribuição geral de sentimentos:")
    
    for label in ['positive', 'negative', 'neutral']:
        count = sentiment_counts.get(label, 0)
        percentage = (count / total_reviews) * 100
        print(f"  {label.capitalize()}: {count} ({percentage:.2f}%)")
    
    # Estatísticas por app se disponível
    if 'app_name' in df.columns:
        generate_comparison_stats(df)

if __name__ == "__main__":
    print("="*60)
    print("ANALISE DE SENTIMENTOS")
    print("="*60)
    
    # Carrega os dados
    print(f"\nCarregando dados de: {CSV_PATH}")
    df_reviews = load_data(CSV_PATH)
    
    if df_reviews is not None and not df_reviews.empty:
        # Executa a análise de sentimentos
        print("\nExecutando análise de sentimentos...")
        df_results = analyze_sentiment(df_reviews)
        
        if df_results is not None:
            # Salva os resultados
            print(f"\nSalvando resultados...")
            df_results.to_csv(OUTPUT_CSV_PATH, index=False, sep=';', encoding='utf-8')
            print(f"Resultados salvos em: {OUTPUT_CSV_PATH}")
            
            # Mostra estatísticas finais
            print_final_stats(df_results)
            
            print("\n" + "="*60)
            print("PROCESSO CONCLUIDO")
            print("="*60)
            print(f"\nArquivo gerado: {OUTPUT_CSV_PATH}")
    else:
        print("\nFalha no carregamento dos dados. Processo interrompido.")
        print("Verifique se o arquivo CSV está no diretório correto.")
