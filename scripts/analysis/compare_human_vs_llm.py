"""
Script para comparar classificações humanas vs. classificações do LLM

Uso:
    python compare_human_vs_llm.py --human app_review_dataset_carol.csv --llm functional_correlation_results.csv
"""

import pandas as pd
import argparse
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
import numpy as np

# Categorias funcionais
CATEGORIES = [
    "PIX",
    "Login/Autenticação",
    "Performance",
    "Interface/Usabilidade",
    "Empréstimos/Crédito",
    "Pagamentos/Boletos",
    "Saldo/Extrato",
    "Atendimento",
    "Cadastro/Conta",
    "Investimentos",
    "Segurança",
    "Notificações",
    "Questões geográficas",
    "Placas/Veículos",
    "Tarifas/Cobranças",
    "Outros"
]

def load_data(human_file, llm_file):
    """Carrega os datasets humano e LLM."""
    
    print("Carregando datasets...")
    
    # Carregar dataset humano
    df_human = pd.read_csv(human_file, encoding='utf-8', sep=';')
    print(f"✓ Dataset humano: {len(df_human)} avaliações")
    
    # Carregar dataset LLM
    try:
        df_llm = pd.read_csv(llm_file, encoding='utf-8')
        print(f"✓ Dataset LLM: {len(df_llm)} avaliações")
    except:
        print(f"⚠️  Dataset LLM não encontrado ou formato diferente")
        return None, None
    
    # Fazer merge por reviewId
    df_merged = df_human.merge(
        df_llm[['reviewId', 'functional_category'] + CATEGORIES if all(c in df_llm.columns for c in CATEGORIES) else ['reviewId', 'functional_category']],
        on='reviewId',
        how='inner',
        suffixes=('_human', '_llm')
    )
    
    print(f"✓ Avaliações em comum: {len(df_merged)}")
    
    return df_human, df_merged

def compare_sentiments(df_human, df_llm_merged):
    """Compara classificações de sentimentos."""
    
    print("\n" + "="*60)
    print("COMPARAÇÃO DE SENTIMENTOS")
    print("="*60)
    
    # Se o dataset LLM tem sentiment_label, comparar
    if 'sentiment_label' in df_llm_merged.columns:
        # Converter classificações humanas para formato do LLM
        df_llm_merged['sentiment_human'] = 'neutral'
        df_llm_merged.loc[df_llm_merged['positive'] == 1, 'sentiment_human'] = 'positive'
        df_llm_merged.loc[df_llm_merged['negative'] == 1, 'sentiment_human'] = 'negative'
        
        # Calcular acurácia
        accuracy = accuracy_score(
            df_llm_merged['sentiment_human'],
            df_llm_merged['sentiment_label']
        )
        
        print(f"\nAcurácia geral: {accuracy*100:.2f}%")
        
        # Matriz de confusão
        cm = confusion_matrix(
            df_llm_merged['sentiment_human'],
            df_llm_merged['sentiment_label'],
            labels=['positive', 'negative', 'neutral']
        )
        
        print("\nMatriz de Confusão:")
        print("                  Predito:")
        print("                  Positive  Negative  Neutral")
        print(f"Real Positive    {cm[0][0]:8d}  {cm[0][1]:8d}  {cm[0][2]:7d}")
        print(f"      Negative    {cm[1][0]:8d}  {cm[1][1]:8d}  {cm[1][2]:7d}")
        print(f"      Neutral     {cm[2][0]:8d}  {cm[2][1]:8d}  {cm[2][2]:7d}")
    else:
        print("⚠️  Dataset LLM não contém classificações de sentimento")

def compare_categories(df_merged):
    """Compara classificações de categorias funcionais."""
    
    print("\n" + "="*60)
    print("COMPARAÇÃO DE CATEGORIAS FUNCIONAIS")
    print("="*60)
    
    # Verificar se temos colunas de categoria do LLM
    llm_category_cols = [c for c in df_merged.columns if c in CATEGORIES and '_llm' in c]
    human_category_cols = [c for c in df_merged.columns if c in CATEGORIES]
    
    if not llm_category_cols and 'functional_category' in df_merged.columns:
        # Se temos apenas uma coluna functional_category, converter para formato binário
        print("Convertendo classificações do LLM para formato binário...")
        for category in CATEGORIES:
            df_merged[f'{category}_llm'] = (df_merged['functional_category'] == category).astype(int)
        llm_category_cols = [f'{c}_llm' for c in CATEGORIES]
    
    if not llm_category_cols:
        print("⚠️  Não foi possível comparar categorias - formato do dataset LLM diferente")
        return
    
    # Comparar cada categoria
    print("\nMétricas por Categoria:")
    print(f"{'Categoria':<25} {'Precisão':<12} {'Recall':<12} {'F1-Score':<12} {'Acurácia':<12}")
    print("-" * 75)
    
    category_metrics = {}
    
    for category in CATEGORIES:
        human_col = category
        llm_col = f'{category}_llm' if f'{category}_llm' in df_merged.columns else None
        
        if human_col not in df_merged.columns or not llm_col:
            continue
        
        y_true = df_merged[human_col].values
        y_pred = df_merged[llm_col].values
        
        # Calcular métricas
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='binary', zero_division=0
        )
        
        accuracy = accuracy_score(y_true, y_pred)
        
        category_metrics[category] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'accuracy': accuracy
        }
        
        print(f"{category:<25} {precision*100:>10.2f}% {recall*100:>10.2f}% {f1*100:>10.2f}% {accuracy*100:>10.2f}%")
    
    # Identificar categorias com melhor/pior desempenho
    print("\n" + "-"*60)
    print("TOP 3 MELHORES CATEGORIAS (F1-Score):")
    print("-"*60)
    
    sorted_categories = sorted(category_metrics.items(), key=lambda x: x[1]['f1'], reverse=True)
    for i, (cat, metrics) in enumerate(sorted_categories[:3], 1):
        print(f"{i}. {cat}: F1={metrics['f1']*100:.2f}%, Precision={metrics['precision']*100:.2f}%, Recall={metrics['recall']*100:.2f}%")
    
    print("\n" + "-"*60)
    print("TOP 3 PIORES CATEGORIAS (F1-Score):")
    print("-"*60)
    
    for i, (cat, metrics) in enumerate(sorted_categories[-3:], 1):
        print(f"{i}. {cat}: F1={metrics['f1']*100:.2f}%, Precision={metrics['precision']*100:.2f}%, Recall={metrics['recall']*100:.2f}%")
    
    return category_metrics

def identify_discrepancies(df_merged):
    """Identifica discrepâncias entre classificações humanas e LLM."""
    
    print("\n" + "="*60)
    print("ANÁLISE DE DISCREPÂNCIAS")
    print("="*60)
    
    # Filtrar apenas avaliações negativas (mais relevantes)
    df_negative = df_merged[df_merged['negative'] == 1].copy()
    
    print(f"\nAvaliações negativas analisadas: {len(df_negative)}")
    
    # Identificar casos onde humano marcou categoria mas LLM não
    discrepancies = []
    
    for category in CATEGORIES:
        human_col = category
        llm_col = f'{category}_llm' if f'{category}_llm' in df_merged.columns else None
        
        if human_col not in df_merged.columns or not llm_col:
            continue
        
        # Casos onde humano marcou mas LLM não
        human_yes_llm_no = df_negative[
            (df_negative[human_col] == 1) & (df_negative[llm_col] == 0)
        ]
        
        # Casos onde LLM marcou mas humano não
        llm_yes_human_no = df_negative[
            (df_negative[human_col] == 0) & (df_negative[llm_col] == 1)
        ]
        
        if len(human_yes_llm_no) > 0 or len(llm_yes_human_no) > 0:
            discrepancies.append({
                'category': category,
                'human_yes_llm_no': len(human_yes_llm_no),
                'llm_yes_human_no': len(llm_yes_human_no)
            })
    
    if discrepancies:
        print("\nDiscrepâncias por Categoria:")
        print(f"{'Categoria':<25} {'Humano✓ LLM✗':<15} {'LLM✓ Humano✗':<15}")
        print("-" * 55)
        
        for disc in discrepancies:
            print(f"{disc['category']:<25} {disc['human_yes_llm_no']:<15} {disc['llm_yes_human_no']:<15}")
    else:
        print("\n✓ Nenhuma discrepância encontrada")

def main():
    parser = argparse.ArgumentParser(
        description='Compara classificações humanas vs. LLM'
    )
    parser.add_argument(
        '--human',
        type=str,
        default='app_review_dataset_carol.csv',
        help='Arquivo CSV com classificações humanas'
    )
    parser.add_argument(
        '--llm',
        type=str,
        default='functional_correlation_results.csv',
        help='Arquivo CSV com classificações do LLM'
    )
    
    args = parser.parse_args()
    
    df_human, df_merged = load_data(args.human, args.llm)
    
    if df_merged is None or len(df_merged) == 0:
        print("\n⚠️  Não foi possível fazer a comparação. Verifique os arquivos.")
        return
    
    # Comparar sentimentos
    compare_sentiments(df_human, df_merged)
    
    # Comparar categorias
    category_metrics = compare_categories(df_merged)
    
    # Identificar discrepâncias
    identify_discrepancies(df_merged)
    
    print("\n" + "="*60)
    print("COMPARAÇÃO CONCLUÍDA")
    print("="*60)

if __name__ == "__main__":
    main()

