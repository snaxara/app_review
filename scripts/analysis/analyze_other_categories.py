"""
Script para analisar o uso das categorias "Outros" e "Não Identificado"
"""

import pandas as pd

df = pd.read_csv('app_review_dataset_carol.csv', encoding='utf-8', sep=';')

print("="*60)
print("ANÁLISE: 'Outros' vs 'Não Identificado'")
print("="*60)

print(f"\n'Outros': {df['Outros'].sum()} marcações")
print(f"'Não Identificado': {df['Não Identificado'].sum()} marcações")
print(f"'Não aplicável': {df['Não aplicável'].sum()} marcações")

# Avaliações com ambas marcadas
both = ((df['Outros'] == 1) & (df['Não Identificado'] == 1)).sum()
print(f"\nAvaliações com 'Outros' E 'Não Identificado': {both}")

# Avaliações negativas
print(f"\n--- Avaliações Negativas ---")
neg_outros = df[(df['negative'] == 1) & (df['Outros'] == 1)].shape[0]
neg_nao_id = df[(df['negative'] == 1) & (df['Não Identificado'] == 1)].shape[0]
print(f"Negativas com 'Outros': {neg_outros}")
print(f"Negativas com 'Não Identificado': {neg_nao_id}")

# Exemplos
print(f"\n--- Exemplos de 'Outros' ---")
outros_examples = df[df['Outros'] == 1].head(5)
for idx, row in outros_examples.iterrows():
    print(f"  - {row['content'][:80]}...")

print(f"\n--- Exemplos de 'Não Identificado' ---")
nao_id_examples = df[df['Não Identificado'] == 1].head(5)
for idx, row in nao_id_examples.iterrows():
    print(f"  - {row['content'][:80]}...")

