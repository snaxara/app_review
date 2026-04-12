"""
Script para calcular métricas de correlação entre Issues e BusinessCapabilities
Gera relatório com estatísticas para apresentação ao gestor
"""

import sys
import os
import pandas as pd
from typing import Dict, List, Tuple
from collections import Counter
import json
from datetime import datetime

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.graph_manager import GraphManager


def get_issues_by_capability(graph: GraphManager) -> pd.DataFrame:
    """
    Extrai todas as Issues e suas BusinessCapabilities associadas.
    
    Returns:
        DataFrame com colunas: Issue, BusinessCapability, Level, CapabilityType, BusinessValue, TotalEpisodes
    """
    query = """
    MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
    OPTIONAL MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(e)
    WHERE 'Issue' IN labels(e)
    WITH e, bc, count(DISTINCT ep) AS total_episodios
    RETURN 
        e.name AS Issue,
        bc.name AS BusinessCapability,
        bc.level AS Level,
        bc.capability_type AS CapabilityType,
        bc.business_value AS BusinessValue,
        total_episodios AS TotalEpisodes
    ORDER BY bc.name, total_episodios DESC, e.name
    """
    
    result = graph.execute_query(query)
    
    if not result:
        return pd.DataFrame()
    
    return pd.DataFrame(result)


def calculate_capability_statistics(df: pd.DataFrame) -> Dict:
    """
    Calcula estatísticas agregadas por BusinessCapability.
    
    Returns:
        Dicionário com estatísticas por capability
    """
    stats = {}
    
    for capability in df['BusinessCapability'].unique():
        cap_df = df[df['BusinessCapability'] == capability]
        
        stats[capability] = {
            'total_issues': len(cap_df['Issue'].unique()),
            'total_episodes': int(cap_df['TotalEpisodes'].sum()),
            'avg_episodes_per_issue': float(cap_df['TotalEpisodes'].mean()) if len(cap_df) > 0 else 0,
            'level': int(cap_df['Level'].iloc[0]) if len(cap_df) > 0 else None,
            'capability_type': cap_df['CapabilityType'].iloc[0] if len(cap_df) > 0 else None,
            'business_value': cap_df['BusinessValue'].iloc[0] if len(cap_df) > 0 else None,
            'top_issues': cap_df.nlargest(5, 'TotalEpisodes')[['Issue', 'TotalEpisodes']].to_dict('records')
        }
    
    return stats


def calculate_distribution_percentages(stats: Dict) -> Dict:
    """
    Calcula distribuição percentual de Issues e Episódios por Capability.
    
    Returns:
        Dicionário com percentuais
    """
    total_issues = sum(s['total_issues'] for s in stats.values())
    total_episodes = sum(s['total_episodes'] for s in stats.values())
    
    distribution = {}
    
    for capability, stat in stats.items():
        distribution[capability] = {
            'issues_percentage': (stat['total_issues'] / total_issues * 100) if total_issues > 0 else 0,
            'episodes_percentage': (stat['total_episodes'] / total_episodes * 100) if total_episodes > 0 else 0
        }
    
    return distribution


def generate_correlation_matrix(df: pd.DataFrame) -> pd.DataFrame:
    """
    Gera matriz de correlação entre Issues e BusinessCapabilities.
    
    Returns:
        DataFrame com matriz de correlação
    """
    # Criar matriz de incidência
    matrix = pd.crosstab(df['Issue'], df['BusinessCapability'], values=df['TotalEpisodes'], aggfunc='sum', fill_value=0)
    
    return matrix


def generate_report(df: pd.DataFrame, output_path: str = None) -> str:
    """
    Gera relatório completo com métricas de correlação.
    
    Args:
        df: DataFrame com Issues e BusinessCapabilities
        output_path: Caminho para salvar relatório (opcional)
        
    Returns:
        String com relatório formatado
    """
    if df.empty:
        return "Nenhum dado encontrado no grafo."
    
    stats = calculate_capability_statistics(df)
    distribution = calculate_distribution_percentages(stats)
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("RELATORIO DE CORRELACAO: ISSUES <-> BUSINESS CAPABILITIES")
    report_lines.append("=" * 80)
    report_lines.append(f"Data de geração: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Resumo geral
    report_lines.append("RESUMO GERAL")
    report_lines.append("-" * 80)
    total_issues = len(df['Issue'].unique())
    total_capabilities = len(df['BusinessCapability'].unique())
    total_episodes = int(df['TotalEpisodes'].sum())
    report_lines.append(f"Total de Issues únicas: {total_issues}")
    report_lines.append(f"Total de BusinessCapabilities: {total_capabilities}")
    report_lines.append(f"Total de Episódios (comentários): {total_episodes}")
    report_lines.append("")
    
    # Estatísticas por Capability
    report_lines.append("ESTATÍSTICAS POR BUSINESS CAPABILITY")
    report_lines.append("-" * 80)
    
    # Ordenar por total de episódios (mais crítico primeiro)
    sorted_stats = sorted(stats.items(), key=lambda x: x[1]['total_episodes'], reverse=True)
    
    for capability, stat in sorted_stats:
        dist = distribution[capability]
        report_lines.append(f"\n{capability}")
        report_lines.append(f"  Nível: {stat['level']} | Tipo: {stat['capability_type']} | Valor: {stat['business_value']}")
        report_lines.append(f"  Total de Issues: {stat['total_issues']} ({dist['issues_percentage']:.2f}%)")
        report_lines.append(f"  Total de Episódios: {stat['total_episodes']} ({dist['episodes_percentage']:.2f}%)")
        report_lines.append(f"  Média de Episódios por Issue: {stat['avg_episodes_per_issue']:.2f}")
        
        if stat['top_issues']:
            report_lines.append("  Top 5 Issues mais frequentes:")
            for i, issue_data in enumerate(stat['top_issues'], 1):
                issue_name = issue_data['Issue']
                episodes = issue_data['TotalEpisodes']
                report_lines.append(f"    {i}. {issue_name}: {episodes} episódio(s)")
    
    # Top 10 Issues mais críticas (mais episódios)
    report_lines.append("\n" + "=" * 80)
    report_lines.append("TOP 10 ISSUES MAIS CRÍTICAS (por número de episódios)")
    report_lines.append("-" * 80)
    
    top_issues = df.groupby('Issue')['TotalEpisodes'].sum().nlargest(10)
    for i, (issue, episodes) in enumerate(top_issues.items(), 1):
        capabilities = df[df['Issue'] == issue]['BusinessCapability'].unique()
        report_lines.append(f"{i}. {issue}: {int(episodes)} episódio(s)")
        report_lines.append(f"   Relacionada a: {', '.join(capabilities)}")
    
    # Distribuição por Nível
    report_lines.append("\n" + "=" * 80)
    report_lines.append("DISTRIBUIÇÃO POR NÍVEL DE CAPABILITY")
    report_lines.append("-" * 80)
    
    level_stats = df.groupby('Level').agg({
        'Issue': 'nunique',
        'TotalEpisodes': 'sum'
    }).reset_index()
    level_stats.columns = ['Level', 'TotalIssues', 'TotalEpisodes']
    
    for _, row in level_stats.iterrows():
        level = int(row['Level'])
        issues = int(row['TotalIssues'])
        episodes = int(row['TotalEpisodes'])
        pct_issues = (issues / total_issues * 100) if total_issues > 0 else 0
        pct_episodes = (episodes / total_episodes * 100) if total_episodes > 0 else 0
        report_lines.append(f"Nível {level}: {issues} Issues ({pct_issues:.2f}%) | {episodes} Episódios ({pct_episodes:.2f}%)")
    
    # Distribuição por Tipo de Capability
    report_lines.append("\n" + "=" * 80)
    report_lines.append("DISTRIBUIÇÃO POR TIPO DE CAPABILITY")
    report_lines.append("-" * 80)
    
    type_stats = df.groupby('CapabilityType').agg({
        'Issue': 'nunique',
        'TotalEpisodes': 'sum'
    }).reset_index()
    type_stats.columns = ['CapabilityType', 'TotalIssues', 'TotalEpisodes']
    
    for _, row in type_stats.iterrows():
        cap_type = row['CapabilityType']
        issues = int(row['TotalIssues'])
        episodes = int(row['TotalEpisodes'])
        pct_issues = (issues / total_issues * 100) if total_issues > 0 else 0
        pct_episodes = (episodes / total_episodes * 100) if total_episodes > 0 else 0
        report_lines.append(f"{cap_type}: {issues} Issues ({pct_issues:.2f}%) | {episodes} Episódios ({pct_episodes:.2f}%)")
    
    # Distribuição por Valor de Negócio
    report_lines.append("\n" + "=" * 80)
    report_lines.append("DISTRIBUIÇÃO POR VALOR DE NEGÓCIO")
    report_lines.append("-" * 80)
    
    value_stats = df.groupby('BusinessValue').agg({
        'Issue': 'nunique',
        'TotalEpisodes': 'sum'
    }).reset_index()
    value_stats.columns = ['BusinessValue', 'TotalIssues', 'TotalEpisodes']
    
    for _, row in value_stats.iterrows():
        value = row['BusinessValue']
        issues = int(row['TotalIssues'])
        episodes = int(row['TotalEpisodes'])
        pct_issues = (issues / total_issues * 100) if total_issues > 0 else 0
        pct_episodes = (episodes / total_episodes * 100) if total_episodes > 0 else 0
        report_lines.append(f"{value}: {issues} Issues ({pct_issues:.2f}%) | {episodes} Episódios ({pct_episodes:.2f}%)")
    
    report_lines.append("\n" + "=" * 80)
    
    report_text = "\n".join(report_lines)
    
    if output_path:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(report_text)
        print(f"Relatório salvo em: {output_path}")
    
    return report_text


def export_to_csv(df: pd.DataFrame, output_path: str):
    """Exporta dados para CSV."""
    df.to_csv(output_path, index=False, encoding='utf-8-sig', sep=';')
    print(f"Dados exportados para: {output_path}")


def main():
    """Função principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Calcula métricas de correlação entre Issues e BusinessCapabilities")
    parser.add_argument("--output-report", default="reports/correlation_metrics_report.txt", 
                       help="Caminho para salvar relatório de métricas")
    parser.add_argument("--output-csv", default="reports/correlation_metrics_data.csv",
                       help="Caminho para salvar dados em CSV")
    parser.add_argument("--output-json", help="Caminho para salvar estatísticas em JSON")
    
    args = parser.parse_args()
    
    print("Conectando ao Neo4j...")
    with GraphManager() as graph:
        print("Extraindo dados do grafo...")
        df = get_issues_by_capability(graph)
        
        if df.empty:
            print("AVISO: Nenhum dado encontrado no grafo.")
            print("Certifique-se de que os comentários foram processados e as entidades foram criadas.")
            return
        
        print(f"Encontrados {len(df)} relacionamentos Issue <-> BusinessCapability")
        print(f"Total de Issues únicas: {len(df['Issue'].unique())}")
        print(f"Total de BusinessCapabilities: {len(df['BusinessCapability'].unique())}")
        
        # Gerar relatório
        print("\nGerando relatório...")
        report = generate_report(df, args.output_report)
        print(report)
        
        # Exportar CSV
        if args.output_csv:
            os.makedirs(os.path.dirname(args.output_csv), exist_ok=True)
            export_to_csv(df, args.output_csv)
        
        # Exportar JSON com estatísticas
        if args.output_json:
            stats = calculate_capability_statistics(df)
            distribution = calculate_distribution_percentages(stats)
            
            json_data = {
                'generated_at': datetime.now().isoformat(),
                'summary': {
                    'total_issues': len(df['Issue'].unique()),
                    'total_capabilities': len(df['BusinessCapability'].unique()),
                    'total_episodes': int(df['TotalEpisodes'].sum())
                },
                'capability_statistics': stats,
                'distribution': distribution
            }
            
            os.makedirs(os.path.dirname(args.output_json), exist_ok=True)
            with open(args.output_json, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"Estatísticas JSON salvas em: {args.output_json}")


if __name__ == "__main__":
    main()
