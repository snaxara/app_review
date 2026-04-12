"""
Script de Validação de Métricas para Classificação de Funcionalidades

Este script calcula métricas completas para validar a qualidade da classificação
automática de funcionalidades feita pelo LLM, comparando com classificação manual (ground truth).

Métricas calculadas:
1. Métricas Multi-Label (por categoria e gerais)
   - Precision, Recall, F1-Score por categoria
   - Exact Match Ratio (EMR)
   - Hamming Loss
   - Subset Accuracy
   - Jaccard Similarity

2. Métricas de Priorização
   - Correlação de Spearman
   - Top-K Accuracy
   - MAP@K (Mean Average Precision)
   - NDCG@K (Normalized Discounted Cumulative Gain)

Uso:
    python validate_functional_classification.py --ground-truth data/ground_truth_dataset.csv --llm functional_correlation_results.csv
"""

import pandas as pd
import numpy as np
import argparse
import os
from datetime import datetime
from sklearn.metrics import (
    precision_recall_fscore_support,
    accuracy_score,
    hamming_loss,
    jaccard_score,
    multilabel_confusion_matrix
)
from scipy.stats import spearmanr
import json

# Categorias funcionais (mesma lista do functional_correlation.py)
CATEGORIES = [
    "PIX",
    "Login/Autenticação",
    "Performance",
    "Interface/Usabilidade",
    "Empréstimos/Crédito",
    "Pagamentos/Boletos",
    "Saldo/Extrato",
    "Atendimento",
    "Cadastro/Conta",
    "Investimentos",
    "Segurança",
    "Notificações",
    "Questões geográficas",
    "Placas/Veículos",
    "Tarifas/Cobranças",
    "Outros"
]

def detect_separator(filepath):
    """Detecta o separador do CSV (vírgula ou ponto e vírgula)."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        
        semicolon_count = first_line.count(';')
        comma_count = first_line.count(',')
        
        return ';' if semicolon_count > comma_count else ','
    except Exception:
        return ';'  # Default

def load_data(filepath, description="", app_name=None):
    """Carrega dados de um arquivo CSV ou Excel."""
    print(f"\nCarregando {description}: {filepath}")
    
    if not os.path.exists(filepath):
        print(f"ERRO: Arquivo não encontrado: {filepath}")
        return None
    
    try:
        # Tentar Excel primeiro
        if filepath.endswith('.xlsx') or filepath.endswith('.xls'):
            df = pd.read_excel(filepath)
            print(f"  Arquivo Excel carregado")
        else:
            # CSV
            separator = detect_separator(filepath)
            df = pd.read_csv(
                filepath,
                sep=separator,
                encoding='utf-8',
                on_bad_lines='skip',
                quotechar='"'
            )
        
        # Filtrar por app se especificado
        if app_name and 'app_name' in df.columns:
            initial_count = len(df)
            df = df[df['app_name'] == app_name].copy()
            print(f"  Filtrado para {app_name}: {len(df)} linhas (de {initial_count})")
        
        print(f"  Total de linhas: {len(df)}")
        print(f"  Colunas: {len(df.columns)}")
        return df
    except Exception as e:
        print(f"  ERRO ao carregar: {e}")
        import traceback
        traceback.print_exc()
        return None

def prepare_category_columns(df, prefix=""):
    """Prepara colunas de categorias, normalizando nomes."""
    category_cols = {}
    
    for cat in CATEGORIES:
        # Tenta diferentes variações do nome
        possible_names = [
            cat,
            f"{cat}_{prefix}" if prefix else cat,
            cat.replace("/", "-"),
            cat.replace("/", "_")
        ]
        
        for name in possible_names:
            if name in df.columns:
                category_cols[cat] = name
                break
    
    return category_cols

def calculate_multilabel_metrics(y_true, y_pred, category_name=""):
    """
    Calcula métricas multi-label para uma categoria específica.
    
    y_true: array binário (ground truth)
    y_pred: array binário (predições do LLM)
    """
    # Métricas básicas por categoria
    precision, recall, f1, support = precision_recall_fscore_support(
        y_true, y_pred, average='binary', zero_division=0
    )
    
    accuracy = accuracy_score(y_true, y_pred)
    
    # True Positives, False Positives, False Negatives
    tp = np.sum((y_true == 1) & (y_pred == 1))
    fp = np.sum((y_true == 0) & (y_pred == 1))
    fn = np.sum((y_true == 1) & (y_pred == 0))
    tn = np.sum((y_true == 0) & (y_pred == 0))
    
    # Calcular support (número de amostras positivas no ground truth)
    support_value = int(np.sum(y_true))
    
    return {
        'precision': float(precision),
        'recall': float(recall),
        'f1_score': float(f1),
        'accuracy': float(accuracy),
        'support': support_value,
        'tp': int(tp),
        'fp': int(fp),
        'fn': int(fn),
        'tn': int(tn)
    }

def calculate_overall_multilabel_metrics(y_true_matrix, y_pred_matrix):
    """
    Calcula métricas gerais multi-label para todas as categorias.
    
    y_true_matrix: matriz (n_samples, n_categories) com ground truth
    y_pred_matrix: matriz (n_samples, n_categories) com predições
    """
    metrics = {}
    
    # Exact Match Ratio (EMR): porcentagem de avaliações com todas as categorias corretas
    exact_matches = np.all(y_true_matrix == y_pred_matrix, axis=1)
    metrics['exact_match_ratio'] = float(np.mean(exact_matches))
    
    # Hamming Loss: média da fração de labels incorretos
    metrics['hamming_loss'] = float(hamming_loss(y_true_matrix, y_pred_matrix))
    
    # Subset Accuracy (mesmo que EMR)
    metrics['subset_accuracy'] = metrics['exact_match_ratio']
    
    # Jaccard Similarity: média da interseção sobre união por amostra
    jaccard_scores = []
    for i in range(len(y_true_matrix)):
        intersection = np.sum((y_true_matrix[i] == 1) & (y_pred_matrix[i] == 1))
        union = np.sum((y_true_matrix[i] == 1) | (y_pred_matrix[i] == 1))
        if union > 0:
            jaccard_scores.append(intersection / union)
        else:
            jaccard_scores.append(1.0)  # Ambos vazios = perfeito
    
    metrics['jaccard_similarity'] = float(np.mean(jaccard_scores))
    
    # Precision, Recall, F1 macro (média não ponderada entre categorias)
    precision_macro, recall_macro, f1_macro, _ = precision_recall_fscore_support(
        y_true_matrix, y_pred_matrix, average='macro', zero_division=0
    )
    
    # Precision, Recall, F1 micro (agrega todos os TP, FP, FN)
    precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(
        y_true_matrix, y_pred_matrix, average='micro', zero_division=0
    )
    
    # Precision, Recall, F1 weighted (média ponderada por suporte)
    precision_weighted, recall_weighted, f1_weighted, _ = precision_recall_fscore_support(
        y_true_matrix, y_pred_matrix, average='weighted', zero_division=0
    )
    
    metrics['precision_macro'] = float(precision_macro)
    metrics['recall_macro'] = float(recall_macro)
    metrics['f1_macro'] = float(f1_macro)
    
    metrics['precision_micro'] = float(precision_micro)
    metrics['recall_micro'] = float(recall_micro)
    metrics['f1_micro'] = float(f1_micro)
    
    metrics['precision_weighted'] = float(precision_weighted)
    metrics['recall_weighted'] = float(recall_weighted)
    metrics['f1_weighted'] = float(f1_weighted)
    
    return metrics

def calculate_priorization_metrics(df_merged, score_col='score'):
    """
    Calcula métricas de priorização comparando backlog humano vs LLM.
    
    Métricas:
    - Correlação de Spearman: compara ranking de categorias
    - Top-K Accuracy: porcentagem de categorias corretas no top K
    - MAP@K: Mean Average Precision at K
    - NDCG@K: Normalized Discounted Cumulative Gain at K
    """
    metrics = {}
    
    # Filtrar apenas avaliações negativas
    if 'sentiment_label' in df_merged.columns:
        df_neg = df_merged[df_merged['sentiment_label'] == 'negative'].copy()
    elif 'negative' in df_merged.columns:
        df_neg = df_merged[df_merged['negative'] == 1].copy()
    else:
        df_neg = df_merged.copy()
    
    if len(df_neg) == 0:
        print("  AVISO: Nenhuma avaliação negativa encontrada")
        return None
    
    # Identificar colunas de score
    if score_col not in df_neg.columns:
        score_cols = [c for c in df_neg.columns if 'score' in c.lower()]
        score_col = score_cols[0] if score_cols else None
    
    if score_col:
        df_neg[score_col] = pd.to_numeric(df_neg[score_col], errors='coerce')
    
    # Preparar colunas de categorias
    human_cat_cols = prepare_category_columns(df_neg, prefix="human")
    llm_cat_cols = prepare_category_columns(df_neg, prefix="llm")
    
    # Se não tem sufixo, tentar sem sufixo
    if not human_cat_cols:
        human_cat_cols = prepare_category_columns(df_neg, prefix="")
    if not llm_cat_cols:
        llm_cat_cols = prepare_category_columns(df_neg, prefix="")
    
    # Calcular prioridades humanas
    human_priorities = {}
    for cat in CATEGORIES:
        if cat in human_cat_cols:
            col = human_cat_cols[cat]
            count = int(df_neg[col].sum()) if col in df_neg.columns else 0
            
            if count > 0:
                # Calcular severidade média
                cat_mask = df_neg[col] == 1
                if score_col and cat_mask.sum() > 0:
                    severity = float(df_neg[cat_mask][score_col].mean())
                else:
                    severity = 2.0  # Default
                
                # Calcular score de prioridade (mesmo algoritmo do generate_backlog_report.py)
                freq_norm = count / len(df_neg)
                sev_norm = (5 - severity) / 5
                
                # Impacto baseado na categoria
                high_impact_cats = ['PIX', 'Login/Autenticação', 'Segurança']
                impact = 0.9 if cat in high_impact_cats else 0.7
                
                priority_score = (freq_norm * 0.4) + (sev_norm * 0.3) + (impact * 0.3)
                human_priorities[cat] = {
                    'priority_score': priority_score,
                    'frequency': count,
                    'severity': severity
                }
    
    # Calcular prioridades do LLM
    llm_priorities = {}
    for cat in CATEGORIES:
        if cat in llm_cat_cols:
            col = llm_cat_cols[cat]
            count = int(df_neg[col].sum()) if col in df_neg.columns else 0
            
            if count > 0:
                cat_mask = df_neg[col] == 1
                if score_col and cat_mask.sum() > 0:
                    severity = float(df_neg[cat_mask][score_col].mean())
                else:
                    severity = 2.0
                
                freq_norm = count / len(df_neg)
                sev_norm = (5 - severity) / 5
                
                high_impact_cats = ['PIX', 'Login/Autenticação', 'Segurança']
                impact = 0.9 if cat in high_impact_cats else 0.7
                
                priority_score = (freq_norm * 0.4) + (sev_norm * 0.3) + (impact * 0.3)
                llm_priorities[cat] = {
                    'priority_score': priority_score,
                    'frequency': count,
                    'severity': severity
                }
    
    if not human_priorities or not llm_priorities:
        print("  AVISO: Não foi possível calcular prioridades")
        return None
    
    # Ordenar por prioridade
    human_sorted = sorted(human_priorities.items(), key=lambda x: x[1]['priority_score'], reverse=True)
    llm_sorted = sorted(llm_priorities.items(), key=lambda x: x[1]['priority_score'], reverse=True)
    
    # Correlação de Spearman
    common_cats = set(human_priorities.keys()) & set(llm_priorities.keys())
    if len(common_cats) > 1:
        human_ranks = {cat: i+1 for i, (cat, _) in enumerate(human_sorted)}
        llm_ranks = {cat: i+1 for i, (cat, _) in enumerate(llm_sorted)}
        
        human_rank_list = [human_ranks[cat] for cat in common_cats]
        llm_rank_list = [llm_ranks[cat] for cat in common_cats]
        
        correlation, p_value = spearmanr(human_rank_list, llm_rank_list)
        metrics['spearman_correlation'] = float(correlation)
        metrics['spearman_p_value'] = float(p_value)
    
    # Top-K Accuracy
    for k in [3, 5, 10]:
        top_k_human = set([cat for cat, _ in human_sorted[:k]])
        top_k_llm = set([cat for cat, _ in llm_sorted[:k]])
        
        if len(top_k_human) > 0:
            accuracy = len(top_k_human & top_k_llm) / len(top_k_human)
            metrics[f'top_{k}_accuracy'] = float(accuracy)
    
    # MAP@K (Mean Average Precision at K)
    for k in [3, 5, 10]:
        top_k_human = [cat for cat, _ in human_sorted[:k]]
        top_k_llm = [cat for cat, _ in llm_sorted[:k]]
        
        # Calcular Average Precision
        ap_scores = []
        for i, cat in enumerate(top_k_llm[:k]):
            if cat in top_k_human:
                # Posição na lista humana
                pos_human = top_k_human.index(cat) + 1
                # Precision neste ponto
                precision_at_i = len(set(top_k_llm[:i+1]) & set(top_k_human[:pos_human])) / (i + 1)
                ap_scores.append(precision_at_i)
        
        map_score = np.mean(ap_scores) if ap_scores else 0.0
        metrics[f'map_at_{k}'] = float(map_score)
    
    # NDCG@K (Normalized Discounted Cumulative Gain)
    for k in [3, 5, 10]:
        top_k_human = [cat for cat, _ in human_sorted[:k]]
        top_k_llm = [cat for cat, _ in llm_sorted[:k]]
        
        # DCG: relevância descontada por posição
        dcg = 0.0
        for i, cat in enumerate(top_k_llm[:k]):
            if cat in top_k_human:
                relevance = 1.0
                position = i + 1
                dcg += relevance / np.log2(position + 1)
        
        # IDCG: DCG ideal (ordem perfeita)
        idcg = sum(1.0 / np.log2(i + 2) for i in range(min(k, len(top_k_human))))
        
        ndcg = dcg / idcg if idcg > 0 else 0.0
        metrics[f'ndcg_at_{k}'] = float(ndcg)
    
    metrics['human_backlog'] = [cat for cat, _ in human_sorted]
    metrics['llm_backlog'] = [cat for cat, _ in llm_sorted]
    
    return metrics

def print_category_metrics(category_metrics):
    """Imprime métricas por categoria de forma formatada."""
    print("\n" + "="*100)
    print("MÉTRICAS POR CATEGORIA")
    print("="*100)
    
    print(f"\n{'Categoria':<30} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Suporte':<10} {'TP':<6} {'FP':<6} {'FN':<6}")
    print("-" * 100)
    
    f1_scores = []
    for category, metrics in sorted(category_metrics.items(), key=lambda x: x[1]['f1_score'], reverse=True):
        f1_scores.append(metrics['f1_score'])
        print(f"{category:<30} {metrics['precision']*100:>10.2f}% {metrics['recall']*100:>10.2f}% "
              f"{metrics['f1_score']*100:>10.2f}% {metrics['support']:>10d} "
              f"{metrics['tp']:>6d} {metrics['fp']:>6d} {metrics['fn']:>6d}")
    
    # Resumo
    avg_f1 = np.mean(f1_scores) if f1_scores else 0
    categories_above_80 = sum(1 for f1 in f1_scores if f1 > 0.8)
    categories_above_70 = sum(1 for f1 in f1_scores if f1 > 0.7)
    
    print("\n" + "-"*100)
    print(f"Média F1-Score: {avg_f1*100:.2f}%")
    print(f"Categorias com F1-Score > 80%: {categories_above_80}/{len(f1_scores)} ({categories_above_80/len(f1_scores)*100:.1f}%)")
    print(f"Categorias com F1-Score > 70%: {categories_above_70}/{len(f1_scores)} ({categories_above_70/len(f1_scores)*100:.1f}%)")
    print(f"Meta: F1-Score > 80% em pelo menos 80% das categorias")
    
    status = "ATINGIDO" if categories_above_80 >= len(f1_scores) * 0.8 else "NAO ATINGIDO"
    print(f"Status: {status}")

def print_overall_metrics(overall_metrics):
    """Imprime métricas gerais multi-label."""
    print("\n" + "="*100)
    print("MÉTRICAS GERAIS MULTI-LABEL")
    print("="*100)
    
    print(f"\nExact Match Ratio (EMR): {overall_metrics['exact_match_ratio']*100:.2f}%")
    print(f"  Porcentagem de avaliações com todas as categorias corretas")
    
    print(f"\nHamming Loss: {overall_metrics['hamming_loss']:.4f}")
    print(f"  Média da fração de labels incorretos (menor é melhor)")
    
    print(f"\nJaccard Similarity: {overall_metrics['jaccard_similarity']*100:.2f}%")
    print(f"  Média da interseção sobre união por avaliação")
    
    print(f"\nPrecision (Macro): {overall_metrics['precision_macro']*100:.2f}%")
    print(f"Recall (Macro): {overall_metrics['recall_macro']*100:.2f}%")
    print(f"F1-Score (Macro): {overall_metrics['f1_macro']*100:.2f}%")
    print(f"  Média não ponderada entre todas as categorias")
    
    print(f"\nPrecision (Micro): {overall_metrics['precision_micro']*100:.2f}%")
    print(f"Recall (Micro): {overall_metrics['recall_micro']*100:.2f}%")
    print(f"F1-Score (Micro): {overall_metrics['f1_micro']*100:.2f}%")
    print(f"  Agrega todos os TP, FP, FN de todas as categorias")
    
    print(f"\nPrecision (Weighted): {overall_metrics['precision_weighted']*100:.2f}%")
    print(f"Recall (Weighted): {overall_metrics['recall_weighted']*100:.2f}%")
    print(f"F1-Score (Weighted): {overall_metrics['f1_weighted']*100:.2f}%")
    print(f"  Média ponderada pelo suporte de cada categoria")

def print_priorization_metrics(prior_metrics):
    """Imprime métricas de priorização."""
    print("\n" + "="*100)
    print("MÉTRICAS DE PRIORIZAÇÃO DE BACKLOG")
    print("="*100)
    
    if not prior_metrics:
        print("\nNão foi possível calcular métricas de priorização")
        return
    
    print(f"\nCorrelação de Spearman: {prior_metrics['spearman_correlation']:.4f}")
    print(f"  p-value: {prior_metrics['spearman_p_value']:.4f}")
    print(f"  Meta: > 0.7 | Status: {'ATINGIDO' if prior_metrics['spearman_correlation'] > 0.7 else 'NAO ATINGIDO'}")
    
    print(f"\nTop-K Accuracy:")
    for k in [3, 5, 10]:
        key = f'top_{k}_accuracy'
        if key in prior_metrics:
            print(f"  Top-{k}: {prior_metrics[key]*100:.2f}%")
    
    print(f"\nMAP@K (Mean Average Precision):")
    for k in [3, 5, 10]:
        key = f'map_at_{k}'
        if key in prior_metrics:
            print(f"  MAP@{k}: {prior_metrics[key]:.4f}")
            print(f"    Meta: > 0.75 | Status: {'ATINGIDO' if prior_metrics[key] > 0.75 else 'NAO ATINGIDO'}")
    
    print(f"\nNDCG@K (Normalized Discounted Cumulative Gain):")
    for k in [3, 5, 10]:
        key = f'ndcg_at_{k}'
        if key in prior_metrics:
            print(f"  NDCG@{k}: {prior_metrics[key]:.4f}")
            print(f"    Meta: > 0.8 | Status: {'ATINGIDO' if prior_metrics[key] > 0.8 else 'NAO ATINGIDO'}")
    
    print(f"\nComparação Top 10:")
    print(f"{'Posição':<10} {'Backlog Humano':<30} {'Backlog LLM':<30} {'Match':<10}")
    print("-" * 80)
    
    human_backlog = prior_metrics.get('human_backlog', [])
    llm_backlog = prior_metrics.get('llm_backlog', [])
    
    for i in range(min(10, len(human_backlog), len(llm_backlog))):
        human_cat = human_backlog[i] if i < len(human_backlog) else "-"
        llm_cat = llm_backlog[i] if i < len(llm_backlog) else "-"
        match = "SIM" if human_cat == llm_cat else "NAO"
        print(f"{i+1:<10} {human_cat:<30} {llm_cat:<30} {match:<10}")

def save_results(category_metrics, overall_metrics, prior_metrics, output_file):
    """Salva resultados em JSON."""
    results = {
        'timestamp': datetime.now().isoformat(),
        'category_metrics': category_metrics,
        'overall_metrics': overall_metrics,
        'priorization_metrics': prior_metrics
    }
    
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"\nResultados salvos em: {output_file}")

def main():
    parser = argparse.ArgumentParser(
        description='Valida classificação de funcionalidades com métricas completas'
    )
    parser.add_argument(
        '--ground-truth',
        type=str,
        default='ground_truth_dataset_std.xlsx',
        help='Arquivo CSV ou Excel com classificação manual (ground truth)'
    )
    parser.add_argument(
        '--llm',
        type=str,
        default='functional_correlation_results.csv',
        help='Arquivo CSV com classificação do LLM'
    )
    parser.add_argument(
        '--app-name',
        type=str,
        default='Santander',
        help='Nome do app para filtrar (padrão: Santander)'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='validation_metrics.json',
        help='Arquivo de saída JSON com todas as métricas'
    )
    parser.add_argument(
        '--merge-key',
        type=str,
        default='reviewId',
        help='Coluna para fazer merge entre datasets (reviewId ou content)'
    )
    
    args = parser.parse_args()
    
    print("="*100)
    print("VALIDAÇÃO DE CLASSIFICAÇÃO DE FUNCIONALIDADES")
    print("="*100)
    print(f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    
    # Carregar dados
    df_gt = load_data(args.ground_truth, "Ground Truth", app_name=args.app_name)
    if df_gt is None:
        return
    
    df_llm = load_data(args.llm, "Classificação LLM", app_name=args.app_name)
    if df_llm is None:
        return
    
    # Fazer merge
    print(f"\nFazendo merge usando coluna: {args.merge_key}")
    
    # Identificar melhor chave de merge disponível em ambos
    merge_key = None
    for key in [args.merge_key, 'reviewId', 'content']:
        if key in df_gt.columns and key in df_llm.columns:
            merge_key = key
            break
    
    if merge_key is None:
        print(f"ERRO: Nenhuma coluna comum encontrada para merge")
        print(f"Colunas disponíveis em GT: {list(df_gt.columns)[:10]}")
        print(f"Colunas disponíveis em LLM: {list(df_llm.columns)[:10]}")
        return
    
    print(f"Usando coluna '{merge_key}' para merge")
    
    # Preparar colunas de categorias antes do merge
    gt_cat_cols = prepare_category_columns(df_gt, prefix="")
    llm_cat_cols = prepare_category_columns(df_llm, prefix="")
    
    # Fazer merge
    df_merged = df_gt.merge(
        df_llm,
        on=merge_key,
        how='inner',
        suffixes=('_human', '_llm')
    )
    
    print(f"Avaliações em comum após merge: {len(df_merged)}")
    
    if len(df_merged) == 0:
        print("ERRO: Nenhuma avaliação em comum encontrada")
        return
    
    # Filtrar apenas avaliações negativas
    if 'sentiment_label' in df_merged.columns:
        df_neg = df_merged[df_merged['sentiment_label'] == 'negative'].copy()
    elif 'negative' in df_merged.columns:
        df_neg = df_merged[df_merged['negative'] == 1].copy()
    else:
        df_neg = df_merged.copy()
    
    print(f"Avaliações negativas: {len(df_neg)}")
    
    # Preparar matrizes de categorias
    y_true_matrix = []
    y_pred_matrix = []
    
    category_metrics = {}
    
    for cat in CATEGORIES:
        # Identificar colunas
        human_col = None
        llm_col = None
        
        # Tentar diferentes variações
        for suffix in ['_human', '']:
            if f'{cat}{suffix}' in df_neg.columns:
                human_col = f'{cat}{suffix}'
                break
        
        for suffix in ['_llm', '']:
            if f'{cat}{suffix}' in df_neg.columns:
                llm_col = f'{cat}{suffix}'
                break
        
        if human_col and llm_col:
            y_true = df_neg[human_col].fillna(0).astype(int).values
            y_pred = df_neg[llm_col].fillna(0).astype(int).values
            
            # Calcular métricas por categoria
            metrics = calculate_multilabel_metrics(y_true, y_pred, cat)
            category_metrics[cat] = metrics
            
            # Adicionar à matriz
            if len(y_true_matrix) == 0:
                y_true_matrix = y_true.reshape(-1, 1)
                y_pred_matrix = y_pred.reshape(-1, 1)
            else:
                y_true_matrix = np.hstack([y_true_matrix, y_true.reshape(-1, 1)])
                y_pred_matrix = np.hstack([y_pred_matrix, y_pred.reshape(-1, 1)])
    
    if len(y_true_matrix) == 0:
        print("ERRO: Nenhuma coluna de categoria encontrada")
        return
    
    # Calcular métricas gerais
    overall_metrics = calculate_overall_multilabel_metrics(y_true_matrix, y_pred_matrix)
    
    # Calcular métricas de priorização
    prior_metrics = calculate_priorization_metrics(df_merged)
    
    # Imprimir resultados
    print_category_metrics(category_metrics)
    print_overall_metrics(overall_metrics)
    print_priorization_metrics(prior_metrics)
    
    # Salvar resultados
    save_results(category_metrics, overall_metrics, prior_metrics, args.output)
    
    print("\n" + "="*100)
    print("VALIDAÇÃO CONCLUÍDA")
    print("="*100)

if __name__ == "__main__":
    main()
