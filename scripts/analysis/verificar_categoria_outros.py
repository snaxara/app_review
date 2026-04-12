"""
Script para verificar quantas issues foram classificadas como "Outros" 
e se estão sendo mapeadas corretamente para "Outras Funcionalidades" no Knowledge Graph.
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Adicionar caminho para importar módulos
scripts_dir = Path(__file__).parent.parent
sys.path.insert(0, str(scripts_dir))

try:
    from knowledge_graph.graph_manager import GraphManager
except ImportError as e:
    print(f"ERRO: Não foi possível importar GraphManager: {e}")
    print(f"   Tentando caminho alternativo...")
    try:
        # Tentar caminho alternativo
        sys.path.insert(0, str(Path(__file__).parent.parent.parent))
        from scripts.knowledge_graph.graph_manager import GraphManager
    except ImportError as e2:
        print(f"ERRO: Não foi possível importar GraphManager: {e2}")
        print("   Continuando sem conexão ao Neo4j...")
        GraphManager = None


def verificar_classificacao_funcional():
    """Verifica quantos comentários foram classificados como 'Outros' na classificação funcional."""
    print("=" * 80)
    print("VERIFICAÇÃO: Classificação Funcional - Categoria 'Outros'")
    print("=" * 80)
    
    # Procurar arquivo de resultados de classificação funcional
    possible_files = [
        'functional_correlation_results.csv',
        'reports/functional_correlation_results.csv',
        'data/functional_correlation_results.csv'
    ]
    
    csv_path = None
    for file_path in possible_files:
        full_path = Path(scripts_dir) / file_path
        if full_path.exists():
            csv_path = full_path
            break
    
    if not csv_path:
        print("[AVISO] Arquivo de classificacao funcional nao encontrado.")
        print("   Procurando em:", [str(Path(scripts_dir) / f) for f in possible_files])
        return None
    
    print(f"\n[OK] Arquivo encontrado: {csv_path}")
    
    try:
        df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
    except:
        try:
            df = pd.read_csv(csv_path, sep=',', encoding='utf-8')
        except Exception as e:
            print(f"❌ Erro ao ler arquivo: {e}")
            return None
    
    print(f"   Total de linhas: {len(df)}")
    print(f"   Colunas: {list(df.columns)}")
    
    # Verificar se há coluna "Outros"
    if 'Outros' in df.columns:
        total_outros = df['Outros'].sum()
        print(f"\n[OK] Coluna 'Outros' encontrada!")
        print(f"   Total de comentarios classificados como 'Outros': {total_outros}")
        print(f"   Percentual: {(total_outros / len(df) * 100):.2f}%")
        
        # Mostrar alguns exemplos
        if total_outros > 0:
            outros_examples = df[df['Outros'] == 1].head(5)
            print(f"\n   Exemplos de comentarios classificados como 'Outros':")
            for idx, row in outros_examples.iterrows():
                content = str(row.get('content', row.get('review', '')))[:100]
                print(f"   - {content}...")
    else:
        print("\n[AVISO] Coluna 'Outros' nao encontrada no arquivo.")
        print(f"   Colunas disponiveis: {list(df.columns)}")
    
    return df


def verificar_knowledge_graph():
    """Verifica se há issues mapeadas para 'Outras Funcionalidades' no Knowledge Graph."""
    print("\n" + "=" * 80)
    print("VERIFICAÇÃO: Knowledge Graph - BusinessCapability 'Outras Funcionalidades'")
    print("=" * 80)
    
    if GraphManager is None:
        print("[AVISO] GraphManager nao disponivel. Pulando verificacao do Knowledge Graph.")
        return None
    
    try:
        graph = GraphManager()
        print("[OK] Conexao com Neo4j estabelecida")
    except Exception as e:
        print(f"[ERRO] Erro ao conectar com Neo4j: {e}")
        return None
    
    # Verificar se BusinessCapability "Outras Funcionalidades" existe
    query_check_capability = """
    MATCH (bc:BusinessCapability)
    WHERE bc.name CONTAINS 'Outras' OR bc.name CONTAINS 'Outros'
    RETURN bc.name AS name, bc.level AS level, bc.capability_type AS type, bc.business_value AS value
    """
    
    result = graph.execute_query(query_check_capability)
    
    if result:
        print(f"\n[OK] BusinessCapability relacionada a 'Outras' encontrada:")
        for row in result:
            print(f"   - Nome: {row['name']}")
            print(f"     Nivel: {row['level']}")
            print(f"     Tipo: {row['type']}")
            print(f"     Valor: {row['value']}")
    else:
        print("\n[AVISO] Nenhuma BusinessCapability 'Outras Funcionalidades' encontrada no grafo.")
    
    # Contar issues por BusinessCapability
    query_issues_by_capability = """
    MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
    WHERE 'Issue' IN labels(e)
    WITH bc.name AS capability, count(DISTINCT e) AS total_issues, count(e) AS total_relationships
    RETURN capability, total_issues, total_relationships
    ORDER BY total_issues DESC
    """
    
    result = graph.execute_query(query_issues_by_capability)
    
    if result:
        print(f"\n[INFO] Distribuicao de Issues por BusinessCapability:")
        print(f"   {'Capability':<40} {'Issues':<10} {'Relacionamentos':<15}")
        print("   " + "-" * 65)
        
        total_issues = 0
        outras_issues = 0
        
        for row in result:
            capability = row['capability']
            issues = row['total_issues']
            relationships = row['total_relationships']
            
            total_issues += issues
            
            if 'Outras' in capability or 'Outros' in capability:
                outras_issues += issues
                print(f"   {capability:<40} {issues:<10} {relationships:<15} [OUTRAS]")
            else:
                print(f"   {capability:<40} {issues:<10} {relationships:<15}")
        
        print("   " + "-" * 65)
        print(f"   {'TOTAL':<40} {total_issues:<10}")
        
        if outras_issues > 0:
            print(f"\n   Issues em 'Outras Funcionalidades': {outras_issues}")
            print(f"   Issues mapeadas para capabilities especificas: {total_issues - outras_issues}")
            print(f"   Percentual de cobertura (excluindo 'Outras'): {((total_issues - outras_issues) / total_issues * 100):.2f}%")
        else:
            print(f"\n[AVISO] Nenhuma issue encontrada em 'Outras Funcionalidades'")
            print(f"   Isso pode indicar que:")
            print(f"   1. Issues classificadas como 'Outros' nao foram processadas")
            print(f"   2. Issues foram filtradas antes do processamento")
            print(f"   3. Mapeamento 'Outros' -> 'Outras Funcionalidades' nao esta funcionando")
    else:
        print("\n[AVISO] Nenhuma issue encontrada no grafo.")
    
    # Verificar issues sem BusinessCapability
    query_issues_without_capability = """
    MATCH (e)
    WHERE 'Issue' IN labels(e)
    AND NOT (e)-[:RELATES_TO_CAPABILITY]->()
    RETURN count(e) AS total_issues_sem_capability
    """
    
    result = graph.execute_query(query_issues_without_capability)
    
    if result and result[0]['total_issues_sem_capability'] > 0:
        print(f"\n[AVISO] Issues sem BusinessCapability associada: {result[0]['total_issues_sem_capability']}")
        print("   Essas issues precisam ser mapeadas!")
    else:
        print(f"\n[OK] Todas as issues tem BusinessCapability associada")
    
    graph.close()
    return result


def calcular_cobertura_real():
    """Calcula o percentual real de cobertura excluindo 'Outras Funcionalidades'."""
    print("\n" + "=" * 80)
    print("CÁLCULO: Percentual Real de Cobertura")
    print("=" * 80)
    
    if GraphManager is None:
        print("[AVISO] GraphManager nao disponivel. Pulando calculo de cobertura.")
        return
    
    try:
        graph = GraphManager()
    except Exception as e:
        print(f"[ERRO] Erro ao conectar com Neo4j: {e}")
        return
    
    # Total de issues no grafo
    query_total_issues = """
    MATCH (e)
    WHERE 'Issue' IN labels(e)
    RETURN count(DISTINCT e) AS total_issues
    """
    
    result = graph.execute_query(query_total_issues)
    total_issues = result[0]['total_issues'] if result else 0
    
    # Issues em "Outras Funcionalidades"
    query_outras = """
    MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
    WHERE 'Issue' IN labels(e)
    AND (bc.name CONTAINS 'Outras' OR bc.name CONTAINS 'Outros')
    RETURN count(DISTINCT e) AS outras_issues
    """
    
    result = graph.execute_query(query_outras)
    outras_issues = result[0]['outras_issues'] if result else 0
    
    # Issues mapeadas para capabilities específicas
    issues_mapeadas = total_issues - outras_issues
    
    print(f"\n📊 Estatísticas:")
    print(f"   Total de Issues Extraídas: {total_issues}")
    print(f"   Issues em 'Outras Funcionalidades': {outras_issues}")
    print(f"   Issues Mapeadas para Capabilities Específicas: {issues_mapeadas}")
    
    if total_issues > 0:
        percentual_cobertura = (issues_mapeadas / total_issues) * 100
        print(f"\n✅ Percentual de Cobertura (excluindo 'Outras Funcionalidades'): {percentual_cobertura:.2f}%")
    else:
        print("\n⚠️  Nenhuma issue encontrada no grafo.")
    
    graph.close()


def main():
    """Executa todas as verificações."""
    print("\n" + "=" * 80)
    print("ANÁLISE COMPLETA: Categoria 'Outros' / 'Outras Funcionalidades'")
    print("=" * 80)
    
    # 1. Verificar classificação funcional
    df_funcional = verificar_classificacao_funcional()
    
    # 2. Verificar Knowledge Graph
    result_graph = verificar_knowledge_graph()
    
    # 3. Calcular cobertura real
    calcular_cobertura_real()
    
    print("\n" + "=" * 80)
    print("ANÁLISE CONCLUÍDA")
    print("=" * 80)
    print("\nProximos passos:")
    print("1. Se houver issues classificadas como 'Outros' mas nao no grafo -> Reprocessar")
    print("2. Se nao houver BusinessCapability 'Outras Funcionalidades' -> Criar no grafo")
    print("3. Se houver inconsistencias -> Corrigir mapeamento e reprocessar")
    print("4. Atualizar metricas e TCC com numeros corretos")


if __name__ == "__main__":
    main()
