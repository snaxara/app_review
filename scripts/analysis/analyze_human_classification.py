"""
Script para analisar o dataset classificado manualmente por humanos
e comparar com as classificações do modelo LLM

Uso:
    python analyze_human_classification.py --input app_review_dataset_carol.csv
"""

import pandas as pd
import argparse
from collections import Counter
from datetime import datetime

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

def analyze_human_classification(filepath):
    """Analisa o dataset classificado manualmente."""
    
    print("="*60)
    print("ANÁLISE DO DATASET CLASSIFICADO MANUALMENTE")
    print("="*60)
    print(f"Arquivo: {filepath}")
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    
    # Carregar dados
    df = pd.read_csv(filepath, encoding='utf-8', sep=';')
    
    print(f"✓ Total de avaliações: {len(df)}")
    
    # Análise de sentimentos
    print("\n" + "-"*60)
    print("1. DISTRIBUIÇÃO DE SENTIMENTOS (Classificação Manual)")
    print("-"*60)
    
    sentiment_cols = ['positive', 'negative', 'neutral', 'mixed']
    sentiment_counts = {}
    for col in sentiment_cols:
        if col in df.columns:
            sentiment_counts[col] = int(df[col].sum())
            percentage = (sentiment_counts[col] / len(df)) * 100
            print(f"  {col.capitalize()}: {sentiment_counts[col]} ({percentage:.1f}%)")
    
    # Verificar avaliações sem classificação de sentimento
    no_sentiment = df[(df['positive'] == 0) & (df['negative'] == 0) & (df['neutral'] == 0) & (df.get('mixed', 0) == 0)]
    if len(no_sentiment) > 0:
        print(f"\n  ⚠️  Avaliações sem classificação de sentimento: {len(no_sentiment)}")
    
    # Análise de categorias funcionais
    print("\n" + "-"*60)
    print("2. DISTRIBUIÇÃO DE CATEGORIAS FUNCIONAIS")
    print("-"*60)
    
    category_counts = {}
    for category in CATEGORIES:
        if category in df.columns:
            count = int(df[category].sum())
            if count > 0:
                percentage = (count / len(df)) * 100
                category_counts[category] = count
                print(f"  {category}: {count} ({percentage:.1f}%)")
    
    # Análise de múltiplas categorias
    print("\n" + "-"*60)
    print("3. ANÁLISE DE MÚLTIPLAS CATEGORIAS")
    print("-"*60)
    
    # Contar quantas categorias cada avaliação tem
    df['num_categories'] = df[CATEGORIES].sum(axis=1)
    
    multi_category_counts = df['num_categories'].value_counts().sort_index()
    print("  Distribuição de número de categorias por avaliação:")
    for num_cats, count in multi_category_counts.items():
        percentage = (count / len(df)) * 100
        print(f"    {int(num_cats)} categoria(s): {count} avaliações ({percentage:.1f}%)")
    
    # Avaliações sem categoria
    no_category = df[df['num_categories'] == 0]
    if len(no_category) > 0:
        print(f"\n  ⚠️  Avaliações sem categoria funcional: {len(no_category)}")
        print(f"      Exemplos:")
        for idx, row in no_category.head(3).iterrows():
            print(f"        - {row['content'][:100]}...")
    
    # Análise de qualidade
    print("\n" + "-"*60)
    print("4. ANÁLISE DE QUALIDADE")
    print("-"*60)
    
    # Verificar consistência: avaliações negativas devem ter pelo menos uma categoria
    negative_reviews = df[df['negative'] == 1]
    negative_without_category = negative_reviews[negative_reviews['num_categories'] == 0]
    
    if len(negative_without_category) > 0:
        print(f"  ⚠️  Avaliações negativas sem categoria: {len(negative_without_category)}")
    else:
        print(f"  ✓ Todas as avaliações negativas têm pelo menos uma categoria")
    
    # Verificar avaliações mixed (devem ter categorias também)
    if 'mixed' in df.columns:
        mixed_reviews = df[df['mixed'] == 1]
        mixed_with_category = mixed_reviews[mixed_reviews['num_categories'] > 0]
        print(f"  ℹ️  Avaliações mixed: {len(mixed_reviews)}")
        print(f"      Com categorias: {len(mixed_with_category)}")
    
    # Verificar avaliações positivas com categorias (pode ser normal)
    positive_reviews = df[df['positive'] == 1]
    positive_with_category = positive_reviews[positive_reviews['num_categories'] > 0]
    if len(positive_with_category) > 0:
        print(f"  ℹ️  Avaliações positivas com categorias: {len(positive_with_category)}")
        print(f"      (Isso pode indicar sugestões de melhoria)")
    
    # Estatísticas gerais
    print("\n" + "-"*60)
    print("5. ESTATÍSTICAS GERAIS")
    print("-"*60)
    
    total_categories_marked = df[CATEGORIES].sum().sum()
    avg_categories_per_review = total_categories_marked / len(df)
    
    print(f"  Total de marcações de categoria: {int(total_categories_marked)}")
    print(f"  Média de categorias por avaliação: {avg_categories_per_review:.2f}")
    print(f"  Avaliações com múltiplas categorias: {len(df[df['num_categories'] > 1])}")
    
    # Salvar relatório
    report_path = 'analise_classificacao_carol.md'
    generate_report(df, sentiment_counts, category_counts, report_path)
    
    print(f"\n✓ Relatório salvo em: {report_path}")
    
    return df

def generate_report(df, sentiment_counts, category_counts, output_path):
    """Gera relatório em Markdown."""
    
    report = f"""# Análise do Dataset Classificado Manualmente

**Data:** {datetime.now().strftime('%d/%m/%Y %H:%M')}  
**Classificador:** Carol  
**Total de Avaliações:** {len(df)}

---

## 1. Distribuição de Sentimentos

| Sentimento | Quantidade | Porcentagem |
|:-----------|:-----------|:------------|
"""
    
    for sentiment, count in sentiment_counts.items():
        percentage = (count / len(df)) * 100
        report += f"| {sentiment.capitalize()} | {count} | {percentage:.1f}% |\n"
    
    report += "\n---\n\n## 2. Distribuição de Categorias Funcionais\n\n"
    report += "| Categoria | Quantidade | Porcentagem |\n"
    report += "|:----------|:-----------|:------------|\n"
    
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(df)) * 100
        report += f"| {category} | {count} | {percentage:.1f}% |\n"
    
    report += "\n---\n\n## 3. Próximos Passos\n\n"
    report += "1. Comparar com classificações do modelo LLM\n"
    report += "2. Calcular métricas de acurácia/inter-annotator agreement\n"
    report += "3. Identificar discrepâncias para revisão\n"
    report += "4. Preparar dataset para treino/fine-tuning\n"
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)

def main():
    parser = argparse.ArgumentParser(
        description='Analisa dataset classificado manualmente'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='app_review_dataset_carol.csv',
        help='Arquivo CSV com classificações manuais'
    )
    
    args = parser.parse_args()
    
    df = analyze_human_classification(args.input)
    
    print("\n" + "="*60)
    print("ANÁLISE CONCLUÍDA")
    print("="*60)

if __name__ == "__main__":
    main()

