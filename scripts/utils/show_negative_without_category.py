"""
Script para mostrar avaliações negativas sem categoria funcional

Uso:
    python show_negative_without_category.py --input app_review_dataset_carol.csv
"""

import pandas as pd
import argparse

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

def show_negative_without_category(filepath, output_file=None):
    """Mostra avaliações negativas sem categoria funcional."""
    
    # Carregar dados
    df = pd.read_csv(filepath, encoding='utf-8', sep=';')
    
    # Filtrar avaliações negativas
    df_negative = df[df['negative'] == 1].copy()
    
    # Calcular número de categorias por avaliação
    df_negative['num_categories'] = df_negative[CATEGORIES].sum(axis=1)
    
    # Filtrar avaliações sem categoria
    df_no_category = df_negative[df_negative['num_categories'] == 0].copy()
    
    print("="*80)
    print(f"AVALIAÇÕES NEGATIVAS SEM CATEGORIA FUNCIONAL")
    print("="*80)
    print(f"\nTotal encontrado: {len(df_no_category)} avaliações\n")
    
    # Mostrar avaliações
    for idx, row in df_no_category.iterrows():
        print(f"\n{'='*80}")
        print(f"ID: {row.get('reviewId', idx)}")
        print(f"Score Original: {row.get('score', 'N/A')}/5")
        print(f"Sentimento: Negative")
        print(f"\nComentário:")
        print(f"  {row['content']}")
        print(f"{'='*80}")
    
    # Salvar em arquivo CSV
    if output_file:
        df_no_category[['reviewId', 'content', 'score', 'negative']].to_csv(
            output_file, 
            index=False, 
            encoding='utf-8',
            sep=';'
        )
        print(f"\n✓ Lista salva em: {output_file}")
    
    # Salvar em Markdown também
    md_file = output_file.replace('.csv', '.md') if output_file else 'avaliacoes_negativas_sem_categoria.md'
    
    with open(md_file, 'w', encoding='utf-8') as f:
        f.write("# Avaliações Negativas Sem Categoria Funcional\n\n")
        f.write(f"**Total:** {len(df_no_category)} avaliações\n\n")
        f.write("---\n\n")
        
        for idx, row in df_no_category.iterrows():
            f.write(f"## Avaliação {idx + 1}\n\n")
            f.write(f"**ID:** {row.get('reviewId', idx)}\n\n")
            f.write(f"**Score Original:** {row.get('score', 'N/A')}/5\n\n")
            f.write(f"**Comentário:**\n\n")
            f.write(f"{row['content']}\n\n")
            f.write("---\n\n")
    
    print(f"✓ Relatório Markdown salvo em: {md_file}")
    
    return df_no_category

def main():
    parser = argparse.ArgumentParser(
        description='Mostra avaliações negativas sem categoria funcional'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='app_review_dataset_carol.csv',
        help='Arquivo CSV com classificações da Carol'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='avaliacoes_negativas_sem_categoria.csv',
        help='Arquivo CSV de saída (opcional)'
    )
    
    args = parser.parse_args()
    
    df_result = show_negative_without_category(args.input, args.output)
    
    print(f"\n{'='*80}")
    print("PROCESSO CONCLUÍDO")
    print(f"{'='*80}")

if __name__ == "__main__":
    main()

