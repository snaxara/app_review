"""
Script para gerar CSV de treino/teste para classificação manual
por duas pessoas do time

Uso:
    python generate_training_dataset.py --input sentiment_results.csv --output training_dataset.csv --size 200
"""

import pandas as pd
import argparse
import random
from datetime import datetime

# Categorias disponíveis
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

def generate_training_dataset(input_file, output_file, size=200, seed=42):
    """Gera CSV de treino/teste para classificação manual."""
    
    # Carregar dados
    print(f"Carregando dados de {input_file}...")
    df = pd.read_csv(input_file, encoding='utf-8')
    
    # Filtrar apenas avaliações negativas
    df_negative = df[df['sentiment_label'] == 'negative'].copy()
    print(f"Total de avaliações negativas: {len(df_negative)}")
    
    # Amostrar avaliações
    if len(df_negative) > size:
        random.seed(seed)
        df_sample = df_negative.sample(n=size, random_state=seed)
        print(f"Amostrando {size} avaliações para treino/teste")
    else:
        df_sample = df_negative.copy()
        print(f"Usando todas as {len(df_sample)} avaliações negativas")
    
    # Criar colunas para classificação manual
    training_df = pd.DataFrame({
        'id': range(1, len(df_sample) + 1),
        'reviewId': df_sample['reviewId'].values,
        'content': df_sample['content'].values,
        'score': df_sample['score'].values,
        'sentiment_label': df_sample['sentiment_label'].values,
        'sentiment_score': df_sample['sentiment_score'].values,
    })
    
    # Adicionar colunas para cada categoria (duas pessoas)
    for category in CATEGORIES:
        training_df[f'{category}_Pessoa1'] = ''
        training_df[f'{category}_Pessoa2'] = ''
    
    # Adicionar colunas de observações
    training_df['Observacoes_Pessoa1'] = ''
    training_df['Observacoes_Pessoa2'] = ''
    
    # Adicionar coluna de conjunto (treino/teste)
    # 80% treino, 20% teste
    n_train = int(len(training_df) * 0.8)
    training_df['conjunto'] = ['treino'] * n_train + ['teste'] * (len(training_df) - n_train)
    
    # Embaralhar
    training_df = training_df.sample(frac=1, random_state=seed).reset_index(drop=True)
    
    # Salvar
    training_df.to_csv(output_file, index=False, encoding='utf-8', sep=';')
    
    print(f"\n✓ Dataset de treino/teste gerado: {output_file}")
    print(f"  Total de avaliações: {len(training_df)}")
    print(f"  Treino: {len(training_df[training_df['conjunto'] == 'treino'])}")
    print(f"  Teste: {len(training_df[training_df['conjunto'] == 'teste'])}")
    print(f"\nInstruções:")
    print(f"  1. Cada pessoa deve marcar com '1' as categorias que se aplicam à avaliação")
    print(f"  2. Se uma avaliação menciona múltiplas funcionalidades, marque todas")
    print(f"  3. Use a coluna 'Observacoes' para comentários adicionais se necessário")
    print(f"\nCategorias disponíveis:")
    for i, cat in enumerate(CATEGORIES, 1):
        print(f"  {i}. {cat}")
    
    return training_df

def main():
    parser = argparse.ArgumentParser(
        description='Gera CSV de treino/teste para classificação manual'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='sentiment_results.csv',
        help='Arquivo CSV com resultados de análise de sentimentos'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='training_dataset.csv',
        help='Arquivo CSV de saída para treino/teste'
    )
    parser.add_argument(
        '--size',
        type=int,
        default=200,
        help='Número de avaliações para incluir no dataset (padrão: 200)'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=42,
        help='Seed para reprodutibilidade (padrão: 42)'
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("GERAÇÃO DE DATASET DE TREINO/TESTE")
    print("="*60)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print()
    
    generate_training_dataset(args.input, args.output, args.size, args.seed)
    
    print("\n" + "="*60)
    print("PROCESSO CONCLUÍDO")
    print("="*60)

if __name__ == "__main__":
    main()

