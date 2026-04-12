"""
Script para gerar gráficos comparativos das métricas do modelo text-embedding-3-large
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
import os

# Configuração de estilo
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (16, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'DejaVu Sans'

def criar_diretorio_imagens():
    """Cria diretório para armazenar imagens"""
    dir_imagens = Path('charts')
    dir_imagens.mkdir(exist_ok=True)
    return dir_imagens

def plot_sentiment_metrics(output_dir):
    """Gera gráfico com métricas de classificação de polarização"""
    
    # Carregar dados
    df = pd.read_csv('results_embedding_model.csv')
    
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    # 1. Métricas principais
    ax1 = axes[0]
    metrics = ['Acurácia', 'Precisão', 'Recall', 'F1-Score']
    values = [
        df['Acurácia'].iloc[0],
        df['Precisão'].iloc[0],
        df['Recall'].iloc[0],
        df['F1-Score'].iloc[0]
    ]
    
    bars = ax1.bar(metrics, values, color='#06A77D', alpha=0.8)
    ax1.set_ylabel('Score', fontsize=12, fontweight='bold', labelpad=8)
    ax1.set_title('Métricas de Classificação de Polarização', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylim([0, 1.10])
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='x', pad=5)
    
    # Adicionar valores nas barras
    for bar, val in zip(bars, values):
        height = bar.get_height()
        offset = 0.02
        ax1.text(bar.get_x() + bar.get_width()/2., height + offset,
                f'{val:.2%}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 2. ROC AUC
    ax2 = axes[1]
    roc_auc = df['ROC AUC'].iloc[0]
    bars = ax2.bar(['ROC AUC'], [roc_auc], color='#2E86AB', alpha=0.8)
    ax2.set_ylabel('Score', fontsize=12, fontweight='bold', labelpad=8)
    ax2.set_title('ROC AUC', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylim([0, 1.10])
    ax2.grid(axis='y', alpha=0.3)
    
    # Adicionar valor na barra
    bar = bars[0]
    height = bar.get_height()
    offset = 0.02
    ax2.text(bar.get_x() + bar.get_width()/2., height + offset,
            f'{height:.2%}', ha='center', va='bottom', fontsize=11, fontweight='bold')
    
    # 3. Comparação geral
    ax3 = axes[2]
    all_metrics = ['Acurácia', 'Precisão', 'Recall', 'F1-Score', 'ROC AUC']
    all_values = [
        df['Acurácia'].iloc[0],
        df['Precisão'].iloc[0],
        df['Recall'].iloc[0],
        df['F1-Score'].iloc[0],
        df['ROC AUC'].iloc[0]
    ]
    
    bars = ax3.bar(all_metrics, all_values, color='#A23B72', alpha=0.8)
    ax3.set_ylabel('Score', fontsize=12, fontweight='bold', labelpad=8)
    ax3.set_title('Visão Geral - Todas as Métricas', fontsize=14, fontweight='bold', pad=15)
    ax3.set_ylim([0, 1.10])
    ax3.grid(axis='y', alpha=0.3)
    ax3.tick_params(axis='x', rotation=15, pad=5)
    
    # Adicionar valores nas barras
    for bar, val in zip(bars, all_values):
        height = bar.get_height()
        offset = 0.02
        ax3.text(bar.get_x() + bar.get_width()/2., height + offset,
                f'{val:.2%}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout(pad=2.0)
    plt.savefig(output_dir / 'sentiment_metrics_embedding.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()
    
    print(f"Gráfico de polarização salvo: {output_dir / 'sentiment_metrics_embedding.png'}")

def plot_functional_metrics(output_dir):
    """Gera gráfico com métricas de classificação funcional"""
    
    # Carregar dados
    df = pd.read_csv('results_functional_classification_embedding.csv')
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # 1. Métricas principais multi-label
    ax1 = axes[0]
    metrics = ['EMR', 'Jaccard\nSimilarity', 'F1-Score\nMacro', 'F1-Score\nMicro']
    values = [
        df['EMR'].iloc[0],
        df['Jaccard_Similarity'].iloc[0],
        df['F1_Macro'].iloc[0],
        df['F1_Micro'].iloc[0]
    ]
    
    bars = ax1.bar(metrics, values, color='#F18F01', alpha=0.8)
    ax1.set_ylabel('Score', fontsize=12, fontweight='bold', labelpad=8)
    ax1.set_title('Métricas de Classificação Funcional (Multi-label)', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylim([0, 1.10])
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='x', pad=5)
    
    # Adicionar valores nas barras
    for bar, val in zip(bars, values):
        height = bar.get_height()
        offset = 0.02
        ax1.text(bar.get_x() + bar.get_width()/2., height + offset,
                f'{val:.2%}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 2. Precisão e Recall (Macro e Micro)
    ax2 = axes[1]
    metrics_detailed = ['Precision\nMacro', 'Recall\nMacro', 'Precision\nMicro', 'Recall\nMicro']
    values_detailed = [
        df['Precision_Macro'].iloc[0],
        df['Recall_Macro'].iloc[0],
        df['Precision_Micro'].iloc[0],
        df['Recall_Micro'].iloc[0]
    ]
    
    bars = ax2.bar(metrics_detailed, values_detailed, color='#C73E1D', alpha=0.8)
    ax2.set_ylabel('Score', fontsize=12, fontweight='bold', labelpad=8)
    ax2.set_title('Precisão e Recall (Macro vs Micro)', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylim([0, 1.10])
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(axis='x', pad=5)
    
    # Adicionar valores nas barras
    for bar, val in zip(bars, values_detailed):
        height = bar.get_height()
        offset = 0.02
        ax2.text(bar.get_x() + bar.get_width()/2., height + offset,
                f'{val:.2%}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout(pad=2.0)
    plt.savefig(output_dir / 'functional_metrics_embedding.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()
    
    print(f"Gráfico de classificação funcional salvo: {output_dir / 'functional_metrics_embedding.png'}")

def plot_comparison_summary(output_dir):
    """Gera gráfico comparativo resumido dos dois testes"""
    
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # 1. Classificação de Polarização
    ax1 = axes[0]
    df_sentiment = pd.read_csv('results_embedding_model.csv')
    
    metrics_sentiment = ['Acurácia', 'Precisão', 'Recall', 'F1-Score', 'ROC AUC']
    values_sentiment = [
        df_sentiment['Acurácia'].iloc[0],
        df_sentiment['Precisão'].iloc[0],
        df_sentiment['Recall'].iloc[0],
        df_sentiment['F1-Score'].iloc[0],
        df_sentiment['ROC AUC'].iloc[0]
    ]
    
    bars1 = ax1.bar(metrics_sentiment, values_sentiment, color='#06A77D', alpha=0.8)
    ax1.set_ylabel('Score', fontsize=12, fontweight='bold', labelpad=8)
    ax1.set_title('Classificação de Polarização\n(text-embedding-3-large + SVM)', fontsize=14, fontweight='bold', pad=15)
    ax1.set_ylim([0, 1.10])
    ax1.grid(axis='y', alpha=0.3)
    ax1.tick_params(axis='x', rotation=15, pad=5)
    
    for bar, val in zip(bars1, values_sentiment):
        height = bar.get_height()
        offset = 0.02
        ax1.text(bar.get_x() + bar.get_width()/2., height + offset,
                f'{val:.2%}', ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    # 2. Classificação Funcional
    ax2 = axes[1]
    df_functional = pd.read_csv('results_functional_classification_embedding.csv')
    
    metrics_functional = ['EMR', 'Jaccard', 'F1-Macro', 'F1-Micro', 'Hamming\nLoss']
    values_functional = [
        df_functional['EMR'].iloc[0],
        df_functional['Jaccard_Similarity'].iloc[0],
        df_functional['F1_Macro'].iloc[0],
        df_functional['F1_Micro'].iloc[0],
        1 - df_functional['Hamming_Loss'].iloc[0]  # Converter para score (1 - loss)
    ]
    
    bars2 = ax2.bar(metrics_functional, values_functional, color='#F18F01', alpha=0.8)
    ax2.set_ylabel('Score', fontsize=12, fontweight='bold', labelpad=8)
    ax2.set_title('Classificação Funcional\n(text-embedding-3-large + Multi-label SVM)', fontsize=14, fontweight='bold', pad=15)
    ax2.set_ylim([0, 1.10])
    ax2.grid(axis='y', alpha=0.3)
    ax2.tick_params(axis='x', rotation=15, pad=5)
    
    for i, (bar, val) in enumerate(zip(bars2, values_functional)):
        height = bar.get_height()
        offset = 0.02
        if i == 4:  # Hamming Loss é o último
            label = f'{df_functional["Hamming_Loss"].iloc[0]:.4f}'  # Mostrar o loss original
        else:
            label = f'{val:.2%}'
        ax2.text(bar.get_x() + bar.get_width()/2., height + offset,
                label, ha='center', va='bottom', fontsize=9, fontweight='bold')
    
    plt.tight_layout(pad=2.0)
    plt.savefig(output_dir / 'comparison_summary_embedding.png', dpi=300, bbox_inches='tight', pad_inches=0.15)
    plt.close()
    
    print(f"Gráfico comparativo resumido salvo: {output_dir / 'comparison_summary_embedding.png'}")

def main():
    """Função principal"""
    print("Gerando gráficos das métricas do modelo text-embedding-3-large...")
    
    output_dir = criar_diretorio_imagens()
    
    print("\n1. Gerando gráfico de classificação de polarização...")
    plot_sentiment_metrics(output_dir)
    
    print("\n2. Gerando gráfico de classificação funcional...")
    plot_functional_metrics(output_dir)
    
    print("\n3. Gerando gráfico comparativo resumido...")
    plot_comparison_summary(output_dir)
    
    print("\n" + "="*70)
    print("Todos os gráficos foram gerados com sucesso!")
    print(f"Arquivos salvos em: {output_dir}")
    print("="*70)

if __name__ == '__main__':
    main()
