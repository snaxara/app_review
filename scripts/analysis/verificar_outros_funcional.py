"""Script simples para verificar categoria Outros no arquivo de classificação funcional"""

import pandas as pd
from pathlib import Path

# Procurar arquivo
csv_path = Path('functional_correlation_results.csv')

if not csv_path.exists():
    csv_path = Path('data/functional_correlation_results.csv')

if not csv_path.exists():
    print("Arquivo functional_correlation_results.csv nao encontrado")
    exit(1)

print(f"Lendo arquivo: {csv_path}")

try:
    df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
except:
    df = pd.read_csv(csv_path, sep=',', encoding='utf-8')

print(f"\nTotal de linhas: {len(df)}")
print(f"Colunas: {list(df.columns)}")

if 'Outros' in df.columns:
    total_outros = df['Outros'].sum()
    print(f"\n[OK] Coluna 'Outros' encontrada!")
    print(f"Total de comentarios classificados como 'Outros': {total_outros}")
    print(f"Percentual: {(total_outros / len(df) * 100):.2f}%")
    
    if total_outros > 0:
        print(f"\nExemplos de comentarios classificados como 'Outros':")
        outros = df[df['Outros'] == 1].head(5)
        for idx, row in outros.iterrows():
            content_col = 'content' if 'content' in df.columns else 'review'
            content = str(row.get(content_col, ''))[:100]
            print(f"  - {content}...")
else:
    print("\n[AVISO] Coluna 'Outros' nao encontrada")
    print("Colunas disponiveis:", list(df.columns))
