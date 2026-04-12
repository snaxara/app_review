"""
Script para gerar visualizações para o TCC
Gera gráficos e tabelas formatadas para inserção no documento
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import json
import os
from pathlib import Path

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'DejaVu Sans'

# Cores para gráficos (paleta profissional)
CORES = {
    'primary': '#2E86AB',
    'secondary': '#A23B72',
    'accent': '#F18F01',
    'success': '#C73E1D',
    'background': '#F5F5F5'
}

def carregar_dados_metricas():
    """Carrega dados das métricas do grafo"""
    with open('reports/metrics_caixa_refinado.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def criar_diretorio_imagens():
    """Cria diretório para armazenar imagens"""
    dir_imagens = Path('Documentos/imagens_tcc')
    dir_imagens.mkdir(exist_ok=True)
    return dir_imagens

def grafico_distribuicao_issues_por_capability(dados, output_dir):
    """Gera gráfico de barras horizontal com distribuição de issues por BusinessCapability"""
    capabilities = []
    issues_count = []
    episodios_count = []
    
    for cap_name, stats in dados['capability_statistics'].items():
        capabilities.append(cap_name)
        issues_count.append(stats['total_issues'])
        episodios_count.append(stats['total_episodes'])
    
    # Criar DataFrame
    df = pd.DataFrame({
        'BusinessCapability': capabilities,
        'Issues': issues_count,
        'Episódios': episodios_count
    })
    
    # Ordenar por número de issues
    df = df.sort_values('Issues', ascending=True)
    
    # Criar figura com dois subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))
    
    # Gráfico 1: Issues por Capability
    ax1.barh(df['BusinessCapability'], df['Issues'], color=CORES['primary'])
    ax1.set_xlabel('Quantidade de Issues', fontsize=12, fontweight='bold')
    ax1.set_title('Distribuição de Issues por BusinessCapability', fontsize=14, fontweight='bold', pad=20)
    ax1.grid(axis='x', alpha=0.3)
    
    # Adicionar valores nas barras
    for i, v in enumerate(df['Issues']):
        ax1.text(v + 0.5, i, str(v), va='center', fontweight='bold')
    
    # Gráfico 2: Episódios por Capability
    ax2.barh(df['BusinessCapability'], df['Episódios'], color=CORES['secondary'])
    ax2.set_xlabel('Quantidade de Episódios', fontsize=12, fontweight='bold')
    ax2.set_title('Distribuição de Episódios por BusinessCapability', fontsize=14, fontweight='bold', pad=20)
    ax2.grid(axis='x', alpha=0.3)
    
    # Adicionar valores nas barras
    for i, v in enumerate(df['Episódios']):
        ax2.text(v + 0.5, i, str(v), va='center', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'distribuicao_issues_capabilities.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Grafico salvo: {output_dir / 'distribuicao_issues_capabilities.png'}")

def grafico_top_10_issues(dados, output_dir):
    """Gera gráfico com top 10 issues mais críticas"""
    todas_issues = []
    
    for cap_name, stats in dados['capability_statistics'].items():
        for issue in stats['top_issues']:
            todas_issues.append({
                'Issue': issue['Issue'],
                'Episódios': issue['TotalEpisodes'],
                'Capability': cap_name
            })
    
    df = pd.DataFrame(todas_issues)
    df = df.sort_values('Episódios', ascending=False).head(10)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Criar gráfico de barras
    bars = ax.barh(range(len(df)), df['Episódios'], color=CORES['primary'])
    
    # Personalizar
    ax.set_yticks(range(len(df)))
    ax.set_yticklabels(df['Issue'], fontsize=10)
    ax.set_xlabel('Número de Episódios', fontsize=12, fontweight='bold')
    ax.set_title('Top 10 Issues Mais Críticas (por Frequência)', fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3)
    
    # Adicionar valores
    for i, v in enumerate(df['Episódios']):
        ax.text(v + 0.1, i, str(v), va='center', fontweight='bold')
    
    # Inverter ordem (maior no topo)
    ax.invert_yaxis()
    
    plt.tight_layout()
    plt.savefig(output_dir / 'top_10_issues.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Grafico salvo: {output_dir / 'top_10_issues.png'}")

def grafico_distribuicao_por_nivel_tipo(dados, output_dir):
    """Gera gráficos de pizza para distribuição por nível, tipo e valor de negócio"""
    # Preparar dados
    nivel_stats = {'Nível 1': 0, 'Nível 2': 0}
    tipo_stats = {'Core': 0, 'Supporting': 0, 'Strategic': 0}
    valor_stats = {'High': 0, 'Medium': 0, 'Low': 0}
    
    for cap_name, stats in dados['capability_statistics'].items():
        nivel = f"Nível {stats['level']}"
        tipo = stats['capability_type']
        valor = stats['business_value']
        
        nivel_stats[nivel] += stats['total_issues']
        tipo_stats[tipo] += stats['total_issues']
        valor_stats[valor] += stats['total_issues']
    
    # Criar figura com 3 subplots
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # Gráfico 1: Por Nível
    nivel_labels = list(nivel_stats.keys())
    nivel_values = list(nivel_stats.values())
    cores_nivel = [CORES['primary'], CORES['secondary']]
    
    axes[0].pie(nivel_values, labels=nivel_labels, autopct='%1.1f%%', 
                colors=cores_nivel, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[0].set_title('Distribuição por Nível Hierárquico', fontsize=12, fontweight='bold', pad=15)
    
    # Gráfico 2: Por Tipo
    tipo_labels = list(tipo_stats.keys())
    tipo_values = list(tipo_stats.values())
    cores_tipo = [CORES['primary'], CORES['secondary'], CORES['accent']]
    
    axes[1].pie(tipo_values, labels=tipo_labels, autopct='%1.1f%%',
                colors=cores_tipo[:len(tipo_labels)], startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[1].set_title('Distribuição por Tipo de Capability', fontsize=12, fontweight='bold', pad=15)
    
    # Gráfico 3: Por Valor de Negócio
    valor_labels = list(valor_stats.keys())
    valor_values = list(valor_stats.values())
    cores_valor = [CORES['success'], CORES['accent'], CORES['primary']]
    
    axes[2].pie(valor_values, labels=valor_labels, autopct='%1.1f%%',
                colors=cores_valor[:len(valor_labels)], startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
    axes[2].set_title('Distribuição por Valor de Negócio', fontsize=12, fontweight='bold', pad=15)
    
    plt.tight_layout()
    plt.savefig(output_dir / 'distribuicao_nivel_tipo_valor.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Grafico salvo: {output_dir / 'distribuicao_nivel_tipo_valor.png'}")

def grafico_pipeline_processamento(output_dir):
    """Gera diagrama do pipeline de processamento"""
    fig, ax = plt.subplots(figsize=(14, 6))
    
    # Etapas do pipeline
    etapas = [
        'Coleta de\nAvaliações',
        'Análise de\nSentimentos',
        'Triagem\nAutomática',
        'Extração de\nEntidades',
        'Modelagem em\nKnowledge Graph',
        'Geração de\nDocumentos'
    ]
    
    # Posições
    x_positions = [1, 2.5, 4, 5.5, 7, 8.5]
    
    # Desenhar setas e caixas
    for i, (etapa, x) in enumerate(zip(etapas, x_positions)):
        # Caixa
        rect = plt.Rectangle((x-0.4, 0.3), 0.8, 0.4, 
                            facecolor=CORES['primary'], edgecolor='black', linewidth=2)
        ax.add_patch(rect)
        
        # Texto
        ax.text(x, 0.5, etapa, ha='center', va='center', 
               fontsize=10, fontweight='bold', color='white')
        
        # Seta (exceto última etapa)
        if i < len(etapas) - 1:
            ax.arrow(x + 0.4, 0.5, 0.5, 0, head_width=0.05, head_length=0.1,
                    fc='black', ec='black', linewidth=2)
    
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 1)
    ax.set_title('Pipeline de Processamento de Avaliações', fontsize=14, fontweight='bold', pad=20)
    ax.axis('off')
    
    plt.tight_layout()
    plt.savefig(output_dir / 'pipeline_processamento.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    print(f"Grafico salvo: {output_dir / 'pipeline_processamento.png'}")

def gerar_todas_visualizacoes():
    """Gera todas as visualizações"""
    print("Gerando visualizacoes para o TCC...")
    
    # Criar diretório
    output_dir = criar_diretorio_imagens()
    
    # Carregar dados
    dados = carregar_dados_metricas()
    
    # Gerar gráficos
    print("\n1. Gerando grafico de distribuicao de issues por capability...")
    grafico_distribuicao_issues_por_capability(dados, output_dir)
    
    print("\n2. Gerando grafico top 10 issues...")
    grafico_top_10_issues(dados, output_dir)
    
    print("\n3. Gerando graficos de distribuicao por nivel/tipo/valor...")
    grafico_distribuicao_por_nivel_tipo(dados, output_dir)
    
    print("\n4. Gerando diagrama do pipeline...")
    grafico_pipeline_processamento(output_dir)
    
    print("\nTodas as visualizacoes foram geradas com sucesso!")
    print(f"Arquivos salvos em: {output_dir}")

if __name__ == '__main__':
    gerar_todas_visualizacoes()
