"""Script para calcular o percentual real de cobertura excluindo 'Outros'"""

import pandas as pd
from pathlib import Path

print("=" * 80)
print("CALCULO: Percentual Real de Cobertura")
print("=" * 80)

# Ler arquivo de classificação funcional
csv_funcional = Path('functional_correlation_results.csv')
if not csv_funcional.exists():
    csv_funcional = Path('data/functional_correlation_results.csv')

if not csv_funcional.exists():
    print("[ERRO] Arquivo functional_correlation_results.csv nao encontrado")
    exit(1)

df_funcional = pd.read_csv(csv_funcional, sep=';', encoding='utf-8')

# Ler métricas do Knowledge Graph
csv_metrics = Path('reports/metrics_caixa_100_comments.csv')
if not csv_metrics.exists():
    csv_metrics = Path('reports/metrics_caixa_refinado.csv')

if not csv_metrics.exists():
    print("[ERRO] Arquivo de metricas nao encontrado")
    exit(1)

df_metrics = pd.read_csv(csv_metrics, sep=';', encoding='utf-8')

print(f"\n[INFO] Dados de Classificacao Funcional:")
print(f"   Total de comentarios: {len(df_funcional)}")
print(f"   Comentarios classificados como 'Outros': {df_funcional['Outros'].sum()}")
print(f"   Percentual: {(df_funcional['Outros'].sum() / len(df_funcional) * 100):.2f}%")

print(f"\n[INFO] Dados do Knowledge Graph (metrics_caixa_100_comments.csv):")
print(f"   Total de issues unicas: {df_metrics['Issue'].nunique()}")
print(f"   Total de relacionamentos: {len(df_metrics)}")
print(f"   BusinessCapabilities: {df_metrics['BusinessCapability'].nunique()}")

# Verificar se há issues em "Outras Funcionalidades"
outras_issues = df_metrics[df_metrics['BusinessCapability'].str.contains('Outras|Outros', case=False, na=False)]
print(f"   Issues em 'Outras Funcionalidades': {len(outras_issues)}")

# Calcular cobertura
total_issues = df_metrics['Issue'].nunique()
issues_outras = len(outras_issues['Issue'].unique()) if len(outras_issues) > 0 else 0
issues_mapeadas = total_issues - issues_outras

print(f"\n[RESULTADO] Calculo de Cobertura:")
print(f"   Total de Issues Extraidas: {total_issues}")
print(f"   Issues em 'Outras Funcionalidades': {issues_outras}")
print(f"   Issues Mapeadas para Capabilities Especificas: {issues_mapeadas}")

if total_issues > 0:
    percentual_cobertura = (issues_mapeadas / total_issues) * 100
    print(f"\n[OK] Percentual de Cobertura (excluindo 'Outras Funcionalidades'): {percentual_cobertura:.2f}%")
else:
    print("\n[AVISO] Nenhuma issue encontrada")

# Verificar se há comentários "Outros" que não foram processados
# Precisamos verificar quais comentários foram processados no Knowledge Graph
# Isso requer acesso ao Neo4j ou aos dados de processamento

print(f"\n[OBSERVACAO]")
print(f"   Se houver comentarios classificados como 'Outros' que nao foram processados,")
print(f"   o percentual real de cobertura pode ser menor que o calculado acima.")
print(f"   E necessario verificar no Neo4j ou nos dados de processamento.")
