"""
Análise dos dados de defeitos da Caixa para refinamento do projeto TCC
"""

import pandas as pd
import sys

def analyze_defects():
    """Analisa defeitos em produção e não produção"""
    
    print("=" * 80)
    print("ANÁLISE DE DEFEITOS CAIXA - REFINAMENTO DO PROJETO TCC")
    print("=" * 80)
    
    # Carregar dados
    df_prod = pd.read_csv('tcc/defeitos_producao.csv', sep=';', encoding='utf-8')
    df_nprod = pd.read_csv('tcc/defeitos_nao_producao.csv', sep=';', encoding='utf-8')
    df_siglas = pd.read_csv('tcc/siglas_caixa.csv', sep=';', encoding='utf-8')
    
    print("\n1. ESTATÍSTICAS GERAIS")
    print("-" * 80)
    print(f"Defeitos em PRODUÇÃO: {len(df_prod):,}")
    print(f"Defeitos NÃO PRODUÇÃO: {len(df_nprod):,}")
    print(f"Total de sistemas mapeados: {len(df_siglas)}")
    
    print("\n2. DISTRIBUIÇÃO POR COMUNIDADE (PRODUÇÃO)")
    print("-" * 80)
    comm_prod = df_prod['Comunidade'].value_counts()
    print(comm_prod.head(10))
    
    print("\n3. DISTRIBUIÇÃO POR COMUNIDADE (NÃO PRODUÇÃO)")
    print("-" * 80)
    comm_nprod = df_nprod['Comunidade'].value_counts()
    print(comm_nprod.head(10))
    
    print("\n4. DISTRIBUIÇÃO POR CRITICIDADE (PRODUÇÃO)")
    print("-" * 80)
    crit_prod = df_prod['Criticidade'].value_counts()
    print(crit_prod)
    
    print("\n5. DISTRIBUIÇÃO POR CRITICIDADE (NÃO PRODUÇÃO)")
    print("-" * 80)
    crit_nprod = df_nprod['Criticidade'].value_counts()
    print(crit_nprod)
    
    print("\n6. TOP 10 SISTEMAS COM MAIS DEFEITOS EM PRODUÇÃO")
    print("-" * 80)
    sistemas_prod = df_prod['Sistema'].value_counts().head(10)
    print(sistemas_prod)
    
    print("\n7. ANÁLISE DE STATUS (PRODUÇÃO)")
    print("-" * 80)
    status_prod = df_prod['Status'].value_counts()
    print(status_prod)
    
    print("\n8. ANÁLISE DE STATUS (NÃO PRODUÇÃO)")
    print("-" * 80)
    status_nprod = df_nprod['Status'].value_counts()
    print(status_nprod)
    
    # Análise comparativa
    print("\n9. COMPARAÇÃO: PRODUÇÃO vs NÃO PRODUÇÃO")
    print("-" * 80)
    print(f"Taxa de defeitos em produção: {len(df_prod) / (len(df_prod) + len(df_nprod)) * 100:.1f}%")
    print(f"Taxa de defeitos capturados antes de produção: {len(df_nprod) / (len(df_prod) + len(df_nprod)) * 100:.1f}%")
    
    # Sistemas relacionados ao app móvel
    print("\n10. SISTEMAS RELACIONADOS AO APP MÓVEL")
    print("-" * 80)
    app_keywords = ['SINBC', 'SIGMP', 'SIGPM', 'SIGLM', 'SIACC', 'SIPPG']
    app_systems_prod = df_prod[df_prod['Sistema'].isin(app_keywords)]
    app_systems_nprod = df_nprod[df_nprod['Sistema'].isin(app_keywords)]
    
    if len(app_systems_prod) > 0:
        print(f"Defeitos em produção relacionados ao app: {len(app_systems_prod)}")
        print("\nDistribuição por sistema:")
        print(app_systems_prod['Sistema'].value_counts())
    
    if len(app_systems_nprod) > 0:
        print(f"\nDefeitos não produção relacionados ao app: {len(app_systems_nprod)}")
        print("\nDistribuição por sistema:")
        print(app_systems_nprod['Sistema'].value_counts())
    
    # Salvar análises
    print("\n11. GERANDO RELATÓRIOS")
    print("-" * 80)
    
    # Top sistemas por comunidade
    sistemas_por_comunidade = df_prod.groupby('Comunidade')['Sistema'].value_counts().groupby(level=0).head(5)
    sistemas_por_comunidade.to_csv('reports/top_sistemas_por_comunidade.csv', sep=';', encoding='utf-8')
    print("OK - Relatorio: reports/top_sistemas_por_comunidade.csv")
    
    # Distribuição de criticidade por comunidade
    criticidade_comunidade = pd.crosstab(df_prod['Comunidade'], df_prod['Criticidade'])
    criticidade_comunidade.to_csv('reports/criticidade_por_comunidade.csv', sep=';', encoding='utf-8')
    print("OK - Relatorio: reports/criticidade_por_comunidade.csv")
    
    print("\n" + "=" * 80)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 80)

if __name__ == "__main__":
    analyze_defects()
