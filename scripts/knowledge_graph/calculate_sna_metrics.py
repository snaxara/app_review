"""
Script para calcular métricas de Social Network Analysis (SNA) no Knowledge Graph
Baseado nos conceitos de SNA aplicados a análise de redes
"""

import sys
import os
import re
from typing import Dict, List
import json
from datetime import datetime

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.graph_manager import GraphManager

_RUN_ID = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")


def _validate_ingestion_run(ingestion_run: str) -> None:
    if ingestion_run == "all":
        return
    if ingestion_run == "v1":
        return
    if not _RUN_ID.match(ingestion_run):
        raise ValueError(
            "ingestion_run deve ser 'all', 'v1' ou um identificador (letras, dígitos, _-)"
        )


def _episode_predicate(ep_var: str, ingestion_run: str) -> str:
    """Expressão Cypher para restringir episódios a uma rodada de carga."""
    if ingestion_run == "v1":
        return f"({ep_var}.ingestion_run IS NULL OR {ep_var}.ingestion_run = 'v1')"
    return f"{ep_var}.ingestion_run = '{ingestion_run}'"


def calculate_degree_centrality(graph: GraphManager, ingestion_run: str = "all") -> Dict:
    """
    Calcula Degree Centrality para Issues e BusinessCapabilities.
    Degree = número de conexões diretas de um nó.
    """
    _validate_ingestion_run(ingestion_run)
    print("Calculando Degree Centrality...")
    
    if ingestion_run == "all":
        query_issues = """
        MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WITH i, count(bc) AS degree
        RETURN i.name AS Issue, degree AS DegreeCentrality
        ORDER BY degree DESC
        """
        query_capabilities = """
        MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WITH bc, count(i) AS degree
        RETURN bc.name AS BusinessCapability, degree AS DegreeCentrality
        ORDER BY degree DESC
        """
    else:
        pred = _episode_predicate("ep", ingestion_run)
        query_issues = f"""
        MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WHERE {pred}
        WITH i, count(DISTINCT bc) AS degree
        RETURN i.name AS Issue, degree AS DegreeCentrality
        ORDER BY degree DESC
        """
        query_capabilities = f"""
        MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WHERE {pred}
        WITH bc, count(DISTINCT i) AS degree
        RETURN bc.name AS BusinessCapability, degree AS DegreeCentrality
        ORDER BY degree DESC
        """
    
    issues_degree = graph.execute_query(query_issues)
    capabilities_degree = graph.execute_query(query_capabilities)
    
    return {
        'issues': issues_degree,
        'capabilities': capabilities_degree
    }


def calculate_betweenness_centrality(graph: GraphManager, ingestion_run: str = "all") -> Dict:
    """
    Calcula Betweenness Centrality aproximado.
    Betweenness = número de caminhos mais curtos que passam pelo nó.
    """
    _validate_ingestion_run(ingestion_run)
    print("Calculando Betweenness Centrality (aproximado)...")
    
    if ingestion_run == "all":
        query_issues = """
        MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WITH i, collect(DISTINCT bc) AS connected_caps
        WITH i, size(connected_caps) AS betweenness
        RETURN i.name AS Issue, betweenness AS BetweennessCentrality
        ORDER BY betweenness DESC
        """
        query_capabilities = """
        MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WITH bc, collect(DISTINCT i) AS connected_issues
        WITH bc, size(connected_issues) AS betweenness
        RETURN bc.name AS BusinessCapability, betweenness AS BetweennessCentrality
        ORDER BY betweenness DESC
        """
    else:
        pred = _episode_predicate("ep", ingestion_run)
        query_issues = f"""
        MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WHERE {pred}
        WITH i, collect(DISTINCT bc) AS connected_caps
        WITH i, size(connected_caps) AS betweenness
        RETURN i.name AS Issue, betweenness AS BetweennessCentrality
        ORDER BY betweenness DESC
        """
        query_capabilities = f"""
        MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WHERE {pred}
        WITH bc, collect(DISTINCT i) AS connected_issues
        WITH bc, size(connected_issues) AS betweenness
        RETURN bc.name AS BusinessCapability, betweenness AS BetweennessCentrality
        ORDER BY betweenness DESC
        """
    
    issues_betweenness = graph.execute_query(query_issues)
    capabilities_betweenness = graph.execute_query(query_capabilities)
    
    return {
        'issues': issues_betweenness,
        'capabilities': capabilities_betweenness
    }


def calculate_closeness_centrality(graph: GraphManager, ingestion_run: str = "all") -> Dict:
    """
    Calcula Closeness Centrality aproximado.
    Closeness = inverso da soma das distâncias até todos os outros nós.
    """
    _validate_ingestion_run(ingestion_run)
    print("Calculando Closeness Centrality (aproximado)...")
    
    if ingestion_run == "all":
        query_issues = """
        MATCH (i1:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(i2:Issue)
        WHERE i1 <> i2
        WITH i1, count(DISTINCT i2) AS reachable_issues, 
             avg(CASE WHEN i1 <> i2 THEN 1 ELSE 0 END) AS avg_distance
        RETURN i1.name AS Issue, 
               reachable_issues AS ReachableNodes,
               CASE WHEN reachable_issues > 0 THEN 1.0 / reachable_issues ELSE 0 END AS ClosenessCentrality
        ORDER BY ClosenessCentrality DESC
        """
        query_capabilities = """
        MATCH (bc1:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(i:Issue)-[:RELATES_TO_CAPABILITY]->(bc2:BusinessCapability)
        WHERE bc1 <> bc2
        WITH bc1, count(DISTINCT bc2) AS reachable_caps
        RETURN bc1.name AS BusinessCapability,
               reachable_caps AS ReachableNodes,
               CASE WHEN reachable_caps > 0 THEN 1.0 / reachable_caps ELSE 0 END AS ClosenessCentrality
        ORDER BY ClosenessCentrality DESC
        """
    else:
        p1 = _episode_predicate("ep1", ingestion_run)
        p2 = _episode_predicate("ep2", ingestion_run)
        query_issues = f"""
        MATCH (ep1:Episode)-[:CONTAINS_ENTITY]->(i1:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        MATCH (ep2:Episode)-[:CONTAINS_ENTITY]->(i2:Issue)-[:RELATES_TO_CAPABILITY]->(bc)
        WHERE i1 <> i2 AND {p1} AND {p2}
        WITH i1, count(DISTINCT i2) AS reachable_issues, 
             avg(CASE WHEN i1 <> i2 THEN 1 ELSE 0 END) AS avg_distance
        RETURN i1.name AS Issue, 
               reachable_issues AS ReachableNodes,
               CASE WHEN reachable_issues > 0 THEN 1.0 / reachable_issues ELSE 0 END AS ClosenessCentrality
        ORDER BY ClosenessCentrality DESC
        """
        pe = _episode_predicate("ep", ingestion_run)
        query_capabilities = f"""
        MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i:Issue)-[:RELATES_TO_CAPABILITY]->(bc1:BusinessCapability)
        MATCH (i)-[:RELATES_TO_CAPABILITY]->(bc2:BusinessCapability)
        WHERE bc1 <> bc2 AND {pe}
        WITH bc1, count(DISTINCT bc2) AS reachable_caps
        RETURN bc1.name AS BusinessCapability,
               reachable_caps AS ReachableNodes,
               CASE WHEN reachable_caps > 0 THEN 1.0 / reachable_caps ELSE 0 END AS ClosenessCentrality
        ORDER BY ClosenessCentrality DESC
        """
    
    issues_closeness = graph.execute_query(query_issues)
    capabilities_closeness = graph.execute_query(query_capabilities)
    
    return {
        'issues': issues_closeness,
        'capabilities': capabilities_closeness
    }


def calculate_clustering_coefficient(graph: GraphManager, ingestion_run: str = "all") -> Dict:
    """
    Calcula Clustering Coefficient conforme definição de Newman (2010).
    Mede a proporção de conexões entre vizinhos de um nó em relação ao número máximo possível.
    Varia de 0 a 1, onde 1 indica que todos os vizinhos estão conectados entre si.
    """
    _validate_ingestion_run(ingestion_run)
    print("Calculando Clustering Coefficient...")
    
    # Clustering Coefficient conforme Newman (2010):
    # C_i = (2 * número de conexões entre vizinhos) / (k_i * (k_i - 1))
    # onde k_i é o grau do nó i
    # Para Issues: vizinhos são outras Issues que compartilham BusinessCapabilities
    # Conexão entre vizinhos: duas Issues compartilham pelo menos uma BusinessCapability
    if ingestion_run == "all":
        query_issues = """
        MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WITH i, collect(DISTINCT bc) AS connected_caps, size(collect(DISTINCT bc)) AS k
        WHERE k > 1
        MATCH (i)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(neighbor:Issue)
        WHERE neighbor <> i
        WITH i, k, collect(DISTINCT neighbor) AS neighbors_list
        WITH i, k, size(neighbors_list) AS num_neighbors, neighbors_list
        UNWIND range(0, size(neighbors_list) - 1) AS idx1
        UNWIND range(idx1 + 1, size(neighbors_list) - 1) AS idx2
        WITH i, k, num_neighbors, neighbors_list[idx1] AS n1, neighbors_list[idx2] AS n2
        MATCH (n1)-[:RELATES_TO_CAPABILITY]->(shared_bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(n2)
        WITH i, k, num_neighbors, count(DISTINCT {n1: n1, n2: n2}) AS edges_between_neighbors
        WITH i, k, num_neighbors, edges_between_neighbors,
             CASE 
               WHEN num_neighbors > 1 THEN 2.0 * edges_between_neighbors / (num_neighbors * (num_neighbors - 1))
               ELSE 0.0
             END AS clustering
        RETURN i.name AS Issue, k AS Degree, num_neighbors AS Neighbors, 
               edges_between_neighbors AS EdgesBetweenNeighbors, clustering AS ClusteringCoefficient
        ORDER BY clustering DESC
        """
    else:
        pred = _episode_predicate("ep", ingestion_run)
        pred_n = _episode_predicate("epn", ingestion_run)
        query_issues = f"""
        MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WHERE {pred}
        WITH i, collect(DISTINCT bc) AS connected_caps, size(collect(DISTINCT bc)) AS k
        WHERE k > 1
        MATCH (epn:Episode)-[:CONTAINS_ENTITY]->(neighbor:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        MATCH (i)-[:RELATES_TO_CAPABILITY]->(bc)
        WHERE neighbor <> i AND {pred_n}
        WITH i, k, collect(DISTINCT neighbor) AS neighbors_list
        WITH i, k, size(neighbors_list) AS num_neighbors, neighbors_list
        UNWIND range(0, size(neighbors_list) - 1) AS idx1
        UNWIND range(idx1 + 1, size(neighbors_list) - 1) AS idx2
        WITH i, k, num_neighbors, neighbors_list[idx1] AS n1, neighbors_list[idx2] AS n2
        MATCH (n1)-[:RELATES_TO_CAPABILITY]->(shared_bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(n2)
        WITH i, k, num_neighbors, count(DISTINCT {{n1: n1, n2: n2}}) AS edges_between_neighbors
        WITH i, k, num_neighbors, edges_between_neighbors,
             CASE 
               WHEN num_neighbors > 1 THEN 2.0 * edges_between_neighbors / (num_neighbors * (num_neighbors - 1))
               ELSE 0.0
             END AS clustering
        RETURN i.name AS Issue, k AS Degree, num_neighbors AS Neighbors, 
               edges_between_neighbors AS EdgesBetweenNeighbors, clustering AS ClusteringCoefficient
        ORDER BY clustering DESC
        """
    
    issues_clustering = graph.execute_query(query_issues)
    
    return {
        'issues': issues_clustering
    }


def calculate_network_density(graph: GraphManager, ingestion_run: str = "all") -> Dict:
    """
    Calcula densidade da rede.
    Densidade = número de links / número máximo possível de links.
    """
    _validate_ingestion_run(ingestion_run)
    print("Calculando densidade da rede...")
    
    if ingestion_run == "all":
        query_stats = """
        MATCH (i:Issue)
        WITH count(i) AS total_issues
        MATCH (bc:BusinessCapability)
        WITH total_issues, count(bc) AS total_capabilities
        MATCH (i:Issue)-[r:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WITH total_issues, total_capabilities, count(r) AS total_links
        RETURN total_issues, total_capabilities, total_links,
               (total_issues * total_capabilities) AS max_possible_links,
               CASE WHEN (total_issues * total_capabilities) > 0 
                    THEN 1.0 * total_links / (total_issues * total_capabilities)
                    ELSE 0 END AS Density
        """
    else:
        pred = _episode_predicate("ep", ingestion_run)
        query_stats = f"""
        MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(i:Issue)
        WHERE {pred}
        WITH count(DISTINCT i) AS total_issues
        MATCH (bc:BusinessCapability)
        WITH total_issues, count(bc) AS total_capabilities
        MATCH (ep2:Episode)-[:CONTAINS_ENTITY]->(i2:Issue)-[r:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        WHERE {_episode_predicate("ep2", ingestion_run)}
        WITH total_issues, total_capabilities, count(r) AS total_links
        RETURN total_issues, total_capabilities, total_links,
               (total_issues * total_capabilities) AS max_possible_links,
               CASE WHEN (total_issues * total_capabilities) > 0 
                    THEN 1.0 * total_links / (total_issues * total_capabilities)
                    ELSE 0 END AS Density
        """
    
    stats = graph.execute_query(query_stats)
    
    return stats[0] if stats else {}


def identify_communities(graph: GraphManager, ingestion_run: str = "all") -> Dict:
    """
    Identifica comunidades usando Label Propagation (aproximado).
    Agrupa Issues que compartilham muitas BusinessCapabilities.
    """
    _validate_ingestion_run(ingestion_run)
    print("Identificando comunidades...")
    
    if ingestion_run == "all":
        query_communities = """
        MATCH (i1:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)<-[:RELATES_TO_CAPABILITY]-(i2:Issue)
        WHERE i1 <> i2
        WITH i1, i2, count(bc) AS shared_caps
        WHERE shared_caps >= 1
        WITH i1, collect({issue: i2.name, shared: shared_caps}) AS neighbors
        RETURN i1.name AS Issue, 
               size(neighbors) AS CommunitySize,
               neighbors[0..5] AS TopNeighbors
        ORDER BY CommunitySize DESC
        """
    else:
        p1 = _episode_predicate("ep1", ingestion_run)
        p2 = _episode_predicate("ep2", ingestion_run)
        query_communities = f"""
        MATCH (ep1:Episode)-[:CONTAINS_ENTITY]->(i1:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
        MATCH (ep2:Episode)-[:CONTAINS_ENTITY]->(i2:Issue)-[:RELATES_TO_CAPABILITY]->(bc)
        WHERE i1 <> i2 AND {p1} AND {p2}
        WITH i1, i2, count(bc) AS shared_caps
        WHERE shared_caps >= 1
        WITH i1, collect({{issue: i2.name, shared: shared_caps}}) AS neighbors
        RETURN i1.name AS Issue, 
               size(neighbors) AS CommunitySize,
               neighbors[0..5] AS TopNeighbors
        ORDER BY CommunitySize DESC
        """
    
    communities = graph.execute_query(query_communities)
    
    return communities


def generate_sna_report(metrics: Dict, output_path: str):
    """Gera relatório de métricas SNA"""
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("METRICAS DE SOCIAL NETWORK ANALYSIS (SNA)")
    report_lines.append("=" * 80)
    report_lines.append(f"Data de geracao: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    ir = metrics.get("ingestion_run")
    if ir is not None:
        report_lines.append(
            f"Filtro Episode.ingestion_run: {ir} (all = sem filtro; v1 inclui episodios sem tag)"
        )
    report_lines.append("")
    
    # Densidade da Rede
    if 'density' in metrics:
        density = metrics['density']
        report_lines.append("DENSIDADE DA REDE")
        report_lines.append("-" * 80)
        report_lines.append(f"Total de Issues: {density.get('total_issues', 'N/A')}")
        report_lines.append(f"Total de BusinessCapabilities: {density.get('total_capabilities', 'N/A')}")
        report_lines.append(f"Total de Links: {density.get('total_links', 'N/A')}")
        report_lines.append(f"Densidade: {density.get('Density', 0):.4f}")
        report_lines.append("")
    
    # Degree Centrality - Top 10 Issues
    if 'degree' in metrics and 'issues' in metrics['degree']:
        report_lines.append("TOP 10 ISSUES POR DEGREE CENTRALITY")
        report_lines.append("-" * 80)
        for i, issue in enumerate(metrics['degree']['issues'][:10], 1):
            report_lines.append(f"{i}. {issue['Issue']}: {issue['DegreeCentrality']}")
        report_lines.append("")
    
    # Degree Centrality - Top 10 Capabilities
    if 'degree' in metrics and 'capabilities' in metrics['degree']:
        report_lines.append("TOP 10 BUSINESS CAPABILITIES POR DEGREE CENTRALITY")
        report_lines.append("-" * 80)
        for i, cap in enumerate(metrics['degree']['capabilities'][:10], 1):
            report_lines.append(f"{i}. {cap['BusinessCapability']}: {cap['DegreeCentrality']}")
        report_lines.append("")
    
    # Betweenness Centrality
    if 'betweenness' in metrics:
        report_lines.append("BETWEENNESS CENTRALITY - TOP 10 ISSUES")
        report_lines.append("-" * 80)
        if 'issues' in metrics['betweenness']:
            for i, issue in enumerate(metrics['betweenness']['issues'][:10], 1):
                report_lines.append(f"{i}. {issue['Issue']}: {issue['BetweennessCentrality']}")
        report_lines.append("")
    
    # Clustering Coefficient
    if 'clustering' in metrics and 'issues' in metrics['clustering']:
        report_lines.append("CLUSTERING COEFFICIENT - TOP 10 ISSUES")
        report_lines.append("-" * 80)
        for i, issue in enumerate(metrics['clustering']['issues'][:10], 1):
            clustering = issue.get('ClusteringCoefficient', 0)
            report_lines.append(f"{i}. {issue['Issue']}: {clustering:.4f}")
        report_lines.append("")
    
    report = "\n".join(report_lines)
    
    # Salvar relatório
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report)
    
    return report


def main():
    """Função principal"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Calcula métricas SNA do Knowledge Graph")
    parser.add_argument("--output-report", default="reports/sna_metrics_report.txt",
                       help="Caminho para salvar relatório")
    parser.add_argument("--output-json", help="Caminho para salvar métricas em JSON")
    parser.add_argument(
        "--ingestion-run",
        default="all",
        metavar="TAG",
        help="Rodada: all (padrão), v1 (NULL ou v1), v2, etc. Restringe SNA a episódios dessa carga.",
    )
    
    args = parser.parse_args()
    
    print("Conectando ao Neo4j...")
    with GraphManager() as graph:
        print(f"Calculando métricas SNA (ingestion_run={args.ingestion_run})...")
        
        metrics = {"ingestion_run": args.ingestion_run}
        
        # Calcular todas as métricas
        metrics['degree'] = calculate_degree_centrality(graph, args.ingestion_run)
        metrics['betweenness'] = calculate_betweenness_centrality(graph, args.ingestion_run)
        metrics['closeness'] = calculate_closeness_centrality(graph, args.ingestion_run)
        metrics['clustering'] = calculate_clustering_coefficient(graph, args.ingestion_run)
        metrics['density'] = calculate_network_density(graph, args.ingestion_run)
        metrics['communities'] = identify_communities(graph, args.ingestion_run)
        
        # Gerar relatório
        print("\nGerando relatório...")
        report = generate_sna_report(metrics, args.output_report)
        print(report)
        
        # Salvar JSON
        if args.output_json:
            os.makedirs(os.path.dirname(args.output_json), exist_ok=True)
            # Converter para formato serializável
            json_metrics = {}
            for key, value in metrics.items():
                if isinstance(value, dict):
                    # Incluir tanto listas quanto outros valores (como density que tem valores numéricos)
                    json_metrics[key] = {}
                    for k, v in value.items():
                        if isinstance(v, (list, dict, int, float, str, bool)) or v is None:
                            json_metrics[key][k] = v
                elif isinstance(value, list):
                    json_metrics[key] = value
                else:
                    json_metrics[key] = value
            
            with open(args.output_json, 'w', encoding='utf-8') as f:
                json.dump(json_metrics, f, ensure_ascii=False, indent=2, default=str)
            print(f"\nMétricas JSON salvas em: {args.output_json}")


if __name__ == '__main__':
    main()
