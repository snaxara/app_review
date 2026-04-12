"""
Exporta visualização do Knowledge Graph (Issue ↔ BusinessCapability) do Neo4j.
Gera imagem PNG para uso no TCC.

Uso (a partir da raiz do projeto):
  python scripts/knowledge_graph/exportar_grafo_visualizacao.py

Requer: neo4j, networkx, matplotlib
"""

import sys
import os
from pathlib import Path

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

from knowledge_graph.graph_manager import GraphManager


# Cores alinhadas ao resto das visualizações do TCC
COR_ISSUE = '#5B8FB9'       # azul claro - nós periféricos (estilo Neo4j)
COR_ISSUE_ALT = '#9B59B6'   # roxo - variação para Issues
COR_CAPABILITY = '#3498DB'  # azul - hubs centrais
COR_PERFORMANCE = '#F39C12' # laranja - destaque para Performance
COR_EDGE = '#7F8C8D'


def extrair_grafo_do_neo4j(graph: GraphManager):
    """
    Extrai o grafo bipartido Issue ↔ BusinessCapability do Neo4j.
    Retorna: (lista de edges [(issue, capability), ...], set de issues, set de capabilities)
    """
    query = """
    MATCH (i:Issue)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
    RETURN i.name AS issue, bc.name AS capability
    """
    rows = graph.execute_query(query)
    edges = [(r['issue'], r['capability']) for r in rows if r.get('issue') and r.get('capability')]
    issues = set(e[0] for e in edges)
    capabilities = set(e[1] for e in edges)
    return edges, issues, capabilities


def criar_grafo_bipartido(edges, issues, capabilities):
    """Cria grafo NetworkX bipartido."""
    G = nx.Graph()
    G.add_nodes_from(issues, bipartite=0)  # 0 = Issue
    G.add_nodes_from(capabilities, bipartite=1)  # 1 = BusinessCapability
    G.add_edges_from(edges)
    return G


def gerar_visualizacao_completa(edges, issues, capabilities, output_path, figsize=(18, 14)):
    """
    Gera visualização bipartida do grafo completo.
    Issues à esquerda, BusinessCapabilities à direita.
    """
    G = criar_grafo_bipartido(edges, issues, capabilities)
    
    # Layout bipartido: Issues em uma coluna, Capabilities em outra
    pos = nx.bipartite_layout(G, issues, align='vertical')
    
    # Ajustar posições para melhor leitura (issues à esquerda, capabilities à direita)
    for node, (x, y) in pos.items():
        if node in issues:
            pos[node] = (x - 1.2, y)  # empurrar issues para esquerda
        else:
            pos[node] = (x + 1.2, y)  # empurrar capabilities para direita
    
    fig, ax = plt.subplots(figsize=figsize)
    
    # Desenhar arestas
    nx.draw_networkx_edges(G, pos, alpha=0.4, edge_color=COR_EDGE, ax=ax)
    
    # Desenhar nós Issues (esquerda)
    issue_nodes = [n for n in G.nodes() if n in issues]
    nx.draw_networkx_nodes(G, pos, nodelist=issue_nodes, node_color=COR_ISSUE, 
                           node_size=80, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, {n: n for n in issue_nodes}, font_size=6, 
                             font_family='sans-serif', ax=ax)
    
    # Desenhar nós BusinessCapabilities (direita)
    cap_nodes = [n for n in G.nodes() if n in capabilities]
    nx.draw_networkx_nodes(G, pos, nodelist=cap_nodes, node_color=COR_CAPABILITY, 
                           node_size=120, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, {n: n for n in cap_nodes}, font_size=7, 
                             font_family='sans-serif', ax=ax)
    
    ax.axis('off')
    ax.set_title('Knowledge Graph: Issues e BusinessCapabilities\n'
                 '(85 Issues | 15 BusinessCapabilities | 91 relacionamentos)', fontsize=12)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Grafo completo salvo: {output_path}")


def gerar_visualizacao_subgrafo(edges, issues, capabilities, output_path, 
                                 top_issues=25, incluir_degree2=True, figsize=(16, 10)):
    """
    Gera subgrafo mais legível: issues com degree 2 (transversais) + top N por conexões,
    mais todas as BusinessCapabilities.
    """
    from collections import Counter
    
    # Contar conexões por issue (degree)
    issue_degree = Counter(i for i, _ in edges)
    
    # Selecionar issues: todas com degree 2 + top por degree até completar top_issues
    issues_degree2 = {i for i in issues if issue_degree[i] >= 2}
    restantes = sorted((i for i in issues if i not in issues_degree2), 
                       key=lambda x: issue_degree[x], reverse=True)
    n_restantes = max(0, top_issues - len(issues_degree2))
    issues_selecionadas = issues_degree2 | set(restantes[:n_restantes])
    
    # Filtrar edges e capabilities que aparecem
    edges_filtrados = [(i, c) for i, c in edges if i in issues_selecionadas]
    caps_no_subgrafo = set(c for _, c in edges_filtrados)
    
    G = criar_grafo_bipartido(edges_filtrados, issues_selecionadas, caps_no_subgrafo)
    pos = nx.bipartite_layout(G, issues_selecionadas, align='vertical')
    
    for node, (x, y) in pos.items():
        if node in issues_selecionadas:
            pos[node] = (x - 1.1, y)
        else:
            pos[node] = (x + 1.1, y)
    
    fig, ax = plt.subplots(figsize=figsize)
    
    nx.draw_networkx_edges(G, pos, alpha=0.5, edge_color=COR_EDGE, ax=ax)
    
    # Issues: tamanho maior para degree 2 (destacar transversais)
    issue_nodes = [n for n in G.nodes() if n in issues_selecionadas]
    sizes_issues = [120 if G.degree(n) >= 2 else 60 for n in issue_nodes]
    nx.draw_networkx_nodes(G, pos, nodelist=issue_nodes, node_color=COR_ISSUE, 
                           node_size=sizes_issues, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, {n: n for n in issue_nodes}, font_size=7, ax=ax)
    
    cap_nodes = [n for n in G.nodes() if n in caps_no_subgrafo]
    nx.draw_networkx_nodes(G, pos, nodelist=cap_nodes, node_color=COR_CAPABILITY, 
                           node_size=150, alpha=0.9, ax=ax)
    nx.draw_networkx_labels(G, pos, {n: n for n in cap_nodes}, font_size=8, ax=ax)
    
    ax.axis('off')
    n_issues = len(issues_selecionadas)
    n_caps = len(caps_no_subgrafo)
    n_edges = len(edges_filtrados)
    titulo = f'Subgrafo do Knowledge Graph (amostra)\n'
    titulo += f'{n_issues} Issues (incl. {len(issues_degree2)} transversais) | {n_caps} BusinessCapabilities | {n_edges} relacionamentos'
    ax.set_title(titulo, fontsize=11)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight')
    plt.close()
    print(f"Subgrafo salvo: {output_path}")


def gerar_visualizacao_organica(edges, issues, capabilities, output_path, figsize=(16, 12)):
    """
    Visualização estilo Neo4j: layout orgânico/clustered, Performance em destaque.
    BusinessCapabilities como hubs centrais (azul), Issues periféricas (azul/roxo).
    """
    G = criar_grafo_bipartido(edges, issues, capabilities)
    
    # Layout força-direcionada para aparência orgânica
    pos = nx.spring_layout(G, k=1.2, iterations=80, seed=42)
    
    # Identificar Performance para destaque (aceita variações de nome)
    performance_node = None
    for cap in capabilities:
        if 'Performance' in cap and ('Estabilidade' in cap or 'escalabilidade' in cap):
            performance_node = cap
            break
    if not performance_node:
        for cap in capabilities:
            if 'Performance' in cap:
                performance_node = cap
                break
    
    fig, ax = plt.subplots(figsize=figsize, facecolor='#2C3E50')
    ax.set_facecolor('#2C3E50')
    
    # Arestas primeiro (mais suaves)
    nx.draw_networkx_edges(G, pos, alpha=0.35, edge_color=COR_EDGE, width=1, ax=ax)
    
    # Issues: nós menores (periféricos, estilo Neo4j)
    issue_nodes = [n for n in G.nodes() if n in issues]
    nx.draw_networkx_nodes(G, pos, nodelist=issue_nodes, node_color=COR_ISSUE, 
                           node_size=180, alpha=0.85, ax=ax)
    nx.draw_networkx_labels(G, pos, {n: n for n in issue_nodes}, font_size=6, 
                             font_color='white', ax=ax)
    
    # BusinessCapabilities: hubs maiores (exceto Performance)
    cap_nodes = [n for n in G.nodes() if n in capabilities]
    cap_sem_perf = [n for n in cap_nodes if n != performance_node]
    if cap_sem_perf:
        nx.draw_networkx_nodes(G, pos, nodelist=cap_sem_perf, node_color=COR_CAPABILITY,
                               node_size=400, alpha=0.9, ax=ax)
        nx.draw_networkx_labels(G, pos, {n: n for n in cap_sem_perf}, font_size=8,
                                 font_color='white', font_weight='bold', ax=ax)
    
    # Performance: destaque (maior, cor laranja, borda)
    if performance_node:
        nx.draw_networkx_nodes(G, pos, nodelist=[performance_node], node_color=COR_PERFORMANCE,
                               node_size=800, alpha=0.95, ax=ax)
        nx.draw_networkx_labels(G, pos, {performance_node: performance_node}, font_size=10,
                                 font_color='white', font_weight='bold', ax=ax)
        # Borda/contorno para mais destaque
        nx.draw_networkx_nodes(G, pos, nodelist=[performance_node], node_size=850,
                               node_shape='o', node_color='none', edgecolors='white',
                               linewidths=3, ax=ax)
    
    ax.axis('off')
    titulo = 'Knowledge Graph: Issues e BusinessCapabilities\n'
    titulo += f'{len(issues)} Issues | {len(capabilities)} BusinessCapabilities | {len(edges)} relacionamentos'
    ax.set_title(titulo, fontsize=11, color='white', pad=15)
    plt.tight_layout()
    plt.savefig(output_path, dpi=200, bbox_inches='tight', facecolor='#2C3E50', edgecolor='none')
    plt.close()
    print(f"Grafo orgânico (Performance destacado) salvo: {output_path}")


def extrair_grafo_do_json(json_path: Path):
    """
    Fallback: extrai arestas do metrics_caixa_refinado.json.
    Usar quando Neo4j não estiver disponível.
    """
    import json
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    edges = []
    for capability, info in data.get('capability_statistics', {}).items():
        for item in info.get('top_issues', []):
            issue = item.get('Issue')
            if issue:
                edges.append((issue, capability))
    issues = set(e[0] for e in edges)
    capabilities = set(e[1] for e in edges)
    return edges, issues, capabilities


def main():
    import argparse
    parser = argparse.ArgumentParser(description='Exporta visualização do grafo Neo4j')
    parser.add_argument('--from-json', metavar='PATH',
                        default='reports/metrics_caixa_refinado.json',
                        help='Usar JSON como fallback quando Neo4j indisponível')
    args = parser.parse_args()
    
    project_root = Path(__file__).resolve().parents[2]
    output_dir = project_root / 'Documentos' / 'imagens_tcc'
    output_dir.mkdir(parents=True, exist_ok=True)
    
    edges, issues, capabilities = [], set(), set()
    
    print("Conectando ao Neo4j...")
    try:
        with GraphManager() as graph:
            edges, issues, capabilities = extrair_grafo_do_neo4j(graph)
    except Exception as e:
        print(f"Neo4j indisponível: {e}")
        json_path = project_root / args.from_json
        if json_path.exists():
            print(f"Usando fallback: {json_path}")
            edges, issues, capabilities = extrair_grafo_do_json(json_path)
        else:
            print(f"Arquivo JSON não encontrado: {json_path}")
            return 1
    
    if not edges:
        print("Nenhum relacionamento Issue-BusinessCapability encontrado no grafo.")
        return 1
    
    print(f"Extraídos: {len(issues)} Issues, {len(capabilities)} BusinessCapabilities, {len(edges)} relacionamentos")
    
    # Gerar as três visualizações
    gerar_visualizacao_completa(
        edges, issues, capabilities, 
        output_dir / 'grafo_issues_capabilities_completo.png'
    )
    gerar_visualizacao_subgrafo(
        edges, issues, capabilities,
        output_dir / 'grafo_issues_capabilities_subgrafo.png',
        top_issues=30
    )
    gerar_visualizacao_organica(
        edges, issues, capabilities,
        output_dir / 'grafo_issues_capabilities_organico.png'
    )
    
    print("\nConcluído. Imagens em Documentos/imagens_tcc/")
    return 0


if __name__ == '__main__':
    sys.exit(main())
