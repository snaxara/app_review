"""
Script para gerar visualizações de métricas SNA
"""

import matplotlib.pyplot as plt
import seaborn as sns
import json
import numpy as np
from pathlib import Path

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (16, 8)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'DejaVu Sans'

CORES = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#C73E1D',
}

def criar_diretorio_imagens():
    """Cria diretório para armazenar imagens"""
    dir_imagens = Path('Documentos/imagens_tcc')
    dir_imagens.mkdir(exist_ok=True)
    return dir_imagens

def grafico_degree_centrality(dados, output_dir):
    """Gera gráfico de Degree Centrality"""
    
    # Carregar dados JSON
    with open(dados, 'r', encoding='utf-8') as f:
        metrics = json.load(f)
    
    # Preparar dados
    issues_degree = metrics.get('degree', {}).get('issues', [])
    capabilities_degree = metrics.get('degree', {}).get('capabilities', [])
    
    # Criar figura com 2 subplots
    fig, axes = plt.subplots(1, 2, figsize=(18, 8))
    
    # Gráfico 1: Top 15 Issues por Degree Centrality
    if issues_degree:
        top_issues = sorted(issues_degree, key=lambda x: x.get('DegreeCentrality', 0), reverse=True)[:15]
        issues_names = [i['Issue'] for i in top_issues]
        degrees = [i['DegreeCentrality'] for i in top_issues]
        
        bars1 = axes[0].barh(range(len(issues_names)), degrees, color=CORES['primary'], alpha=0.8)
        axes[0].set_yticks(range(len(issues_names)))
        axes[0].set_yticklabels(issues_names, fontsize=9)
        axes[0].set_xlabel('Degree Centrality', fontsize=12, fontweight='bold')
        axes[0].set_title('Top 15 Issues por Degree Centrality', fontsize=14, fontweight='bold', pad=15)
        axes[0].grid(axis='x', alpha=0.3)
        axes[0].invert_yaxis()
        
        # Adicionar valores
        for i, (bar, deg) in enumerate(zip(bars1, degrees)):
            axes[0].text(deg + 0.05, i, str(int(deg)), va='center', fontweight='bold', fontsize=9)
    
    # Gráfico 2: Top 15 BusinessCapabilities por Degree Centrality
    if capabilities_degree:
        top_caps = sorted(capabilities_degree, key=lambda x: x.get('DegreeCentrality', 0), reverse=True)[:15]
        caps_names = [c['BusinessCapability'] for c in top_caps]
        degrees = [c['DegreeCentrality'] for c in top_caps]
        
        bars2 = axes[1].barh(range(len(caps_names)), degrees, color=CORES['secondary'], alpha=0.8)
        axes[1].set_yticks(range(len(caps_names)))
        axes[1].set_yticklabels(caps_names, fontsize=9)
        axes[1].set_xlabel('Degree Centrality', fontsize=12, fontweight='bold')
        axes[1].set_title('Top 15 BusinessCapabilities por Degree Centrality', fontsize=14, fontweight='bold', pad=15)
        axes[1].grid(axis='x', alpha=0.3)
        axes[1].invert_yaxis()
        
        # Adicionar valores
        for i, (bar, deg) in enumerate(zip(bars2, degrees)):
            axes[1].text(deg + 0.5, i, str(int(deg)), va='center', fontweight='bold', fontsize=9)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'sna_degree_centrality.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Grafico salvo: {output_dir / 'sna_degree_centrality.png'}")

def grafico_metricas_combinadas(dados, output_dir):
    """Gera gráfico combinando múltiplas métricas SNA"""
    
    with open(dados, 'r', encoding='utf-8') as f:
        metrics = json.load(f)
    
    density = metrics.get('density', {})
    
    # Criar figura
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Densidade da Rede
    ax1 = axes[0, 0]
    if density and density.get('total_links') is not None:
        total_links = density.get('total_links', 0)
        max_links = density.get('max_possible_links', 0)
        density_value = density.get('Density', 0)
        
        if max_links > 0:
            labels = ['Links Existentes', 'Links Possíveis (não utilizados)']
            values = [total_links, max_links - total_links]
            colors = [CORES['primary'], '#E0E0E0']
            
            ax1.pie(values, labels=labels, autopct='%1.1f%%', colors=colors, startangle=90, 
                   textprops={'fontsize': 10, 'fontweight': 'bold'})
            ax1.set_title(f'Densidade da Rede: {density_value:.4f} ({density_value*100:.2f}%)', 
                         fontsize=12, fontweight='bold', pad=15)
        else:
            ax1.text(0.5, 0.5, 'Dados de densidade\nnão disponíveis', 
                    ha='center', va='center', fontsize=12, fontweight='bold')
            ax1.set_title('Densidade da Rede', fontsize=12, fontweight='bold', pad=15)
    else:
        ax1.text(0.5, 0.5, 'Dados de densidade\nnão disponíveis', 
                ha='center', va='center', fontsize=12, fontweight='bold')
        ax1.set_title('Densidade da Rede', fontsize=12, fontweight='bold', pad=15)
    
    # 2. Distribuição de Degree Centrality - Issues
    ax2 = axes[0, 1]
    issues_degree = metrics.get('degree', {}).get('issues', [])
    if issues_degree:
        degrees = [i.get('DegreeCentrality', 0) for i in issues_degree]
        # Criar bins baseados nos valores únicos de degree
        unique_degrees = sorted(set(degrees))
        bins = unique_degrees + [max(unique_degrees) + 1] if unique_degrees else [0, 1, 2]
        
        counts, bins_edges, patches = ax2.hist(degrees, bins=bins, color=CORES['primary'], alpha=0.7, edgecolor='black', align='left')
        
        # Adicionar valores nas barras
        for count, patch in zip(counts, patches):
            if count > 0:
                height = patch.get_height()
                ax2.text(patch.get_x() + patch.get_width()/2., height,
                        f'{int(count)}', ha='center', va='bottom', fontweight='bold', fontsize=10)
        
        ax2.set_xlabel('Degree Centrality', fontsize=11, fontweight='bold')
        ax2.set_ylabel('Frequência', fontsize=11, fontweight='bold')
        ax2.set_title('Distribuição de Degree Centrality - Issues', fontsize=12, fontweight='bold', pad=15)
        ax2.set_xticks(unique_degrees)
        ax2.grid(axis='y', alpha=0.3)
    
    # 3. Clustering Coefficient - Top 10
    ax3 = axes[1, 0]
    clustering = metrics.get('clustering', {}).get('issues', [])
    if clustering:
        top_clustering = sorted(clustering, key=lambda x: x.get('ClusteringCoefficient', 0), reverse=True)[:10]
        issues_names = [c['Issue'] for c in top_clustering]
        coeffs = [c.get('ClusteringCoefficient', 0) for c in top_clustering]
        
        # Clustering Coefficient conforme Newman (2010) varia de 0 a 1
        bars = ax3.barh(range(len(issues_names)), coeffs, color=CORES['accent'], alpha=0.8)
        ax3.set_yticks(range(len(issues_names)))
        ax3.set_yticklabels(issues_names, fontsize=9)
        ax3.set_xlabel('Clustering Coefficient', fontsize=11, fontweight='bold')
        ax3.set_title('Top 10 Issues por Clustering Coefficient', fontsize=12, fontweight='bold', pad=15)
        ax3.set_xlim(0, 1)  # Clustering coefficient varia de 0 a 1 conforme Newman (2010)
        ax3.grid(axis='x', alpha=0.3)
        ax3.invert_yaxis()
        
        # Adicionar valores
        for i, (bar, coeff) in enumerate(zip(bars, coeffs)):
            ax3.text(coeff + 0.01, i, f'{coeff:.2f}', va='center', fontweight='bold', fontsize=9)
    
    # 4. Resumo de Métricas da Rede
    ax4 = axes[1, 1]
    ax4.axis('off')
    
    # Buscar dados de densidade e degree para o resumo
    total_issues = len(metrics.get('degree', {}).get('issues', []))
    total_capabilities = len(metrics.get('degree', {}).get('capabilities', []))
    total_links = density.get('total_links', 0) if density else 0
    max_links = density.get('max_possible_links', 0) if density else 0
    density_value = density.get('Density', 0) if density else 0
    
    summary_text = f"""
RESUMO DA REDE

Total de Issues: {total_issues}
Total de BusinessCapabilities: {total_capabilities}
Total de Links: {total_links}
Links Máximos Possíveis: {max_links}
Densidade: {density_value:.4f} ({density_value*100:.2f}%)

INTERPRETAÇÃO:
• Densidade baixa indica distribuição específica
• Issues concentradas em capabilities críticas
• Estrutura facilita identificação de áreas prioritárias
"""
    ax4.text(0.1, 0.5, summary_text, fontsize=11, verticalalignment='center',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5), 
            family='monospace', transform=ax4.transAxes)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'sna_metricas_combinadas.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Grafico salvo: {output_dir / 'sna_metricas_combinadas.png'}")

def gerar_todos_graficos_sna():
    """Gera todos os gráficos SNA"""
    print("Gerando visualizacoes de metricas SNA...")
    
    output_dir = criar_diretorio_imagens()
    dados_json = 'reports/sna_metrics.json'
    
    print("\n1. Gerando grafico de Degree Centrality...")
    grafico_degree_centrality(dados_json, output_dir)
    
    print("\n2. Gerando grafico de metricas combinadas...")
    grafico_metricas_combinadas(dados_json, output_dir)
    
    print("\nTodos os graficos SNA foram gerados com sucesso!")
    print(f"Arquivos salvos em: {output_dir}")

if __name__ == '__main__':
    gerar_todos_graficos_sna()
