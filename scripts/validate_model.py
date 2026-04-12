"""
Script completo para validar o modelo de categorização e priorização

Uso:
    python validate_model.py --human app_review_dataset_carol.csv --llm functional_correlation_results.csv
"""

import pandas as pd
import argparse
from sklearn.metrics import precision_recall_fscore_support, accuracy_score
from scipy.stats import spearmanr
import numpy as np

# Categorias funcionais
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

def calculate_categorization_metrics(df_human, df_llm_merged):
    """Calcula métricas de categorização automática."""
    
    print("\n" + "="*80)
    print("VALIDAÇÃO DA CATEGORIZAÇÃO AUTOMÁTICA")
    print("="*80)
    
    # Filtrar apenas avaliações negativas (mais relevantes)
    df_neg = df_llm_merged[df_llm_merged['negative'] == 1].copy()
    
    print(f"\nAvaliações negativas analisadas: {len(df_neg)}")
    
    metrics_by_category = {}
    
    # Funções auxiliares para identificar colunas
    human_cat_col = lambda cat: f'{cat}_human' if f'{cat}_human' in df_neg.columns else (cat if cat in df_neg.columns else None)
    llm_cat_col = lambda cat: f'{cat}_llm' if f'{cat}_llm' in df_neg.columns else (cat if cat in df_neg.columns else None)
    
    for category in CATEGORIES:
        human_col = human_cat_col(category)
        llm_col = llm_cat_col(category)
        
        if not human_col or not llm_col:
            continue
        
        y_true = df_neg[human_col].values
        y_pred = df_neg[llm_col].values
        
        # Calcular métricas
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_true, y_pred, average='binary', zero_division=0
        )
        
        accuracy = accuracy_score(y_true, y_pred)
        
        metrics_by_category[category] = {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'accuracy': accuracy,
            'support': int(y_true.sum())  # Quantas avaliações realmente têm essa categoria
        }
    
    # Mostrar resultados
    print(f"\n{'Categoria':<25} {'Precision':<12} {'Recall':<12} {'F1-Score':<12} {'Suporte':<10}")
    print("-" * 80)
    
    f1_scores = []
    for category, metrics in sorted(metrics_by_category.items(), key=lambda x: x[1]['f1'], reverse=True):
        f1_scores.append(metrics['f1'])
        print(f"{category:<25} {metrics['precision']*100:>10.2f}% {metrics['recall']*100:>10.2f}% "
              f"{metrics['f1']*100:>10.2f}% {metrics['support']:>10d}")
    
    # Métricas gerais
    avg_f1 = np.mean(f1_scores) if f1_scores else 0
    categories_above_80 = sum(1 for f1 in f1_scores if f1 > 0.8)
    
    print("\n" + "-"*80)
    print(f"Média F1-Score: {avg_f1*100:.2f}%")
    print(f"Categorias com F1-Score > 80%: {categories_above_80}/{len(f1_scores)}")
    print(f"Meta: F1-Score > 80% em pelo menos 80% das categorias")
    print(f"Status: {'✅ ATINGIDO' if categories_above_80 >= len(f1_scores) * 0.8 else '❌ NÃO ATINGIDO'}")
    
    return metrics_by_category

def calculate_priorization_metrics(df_human, df_llm_merged):
    """Calcula métricas de priorização de backlog."""
    
    print("\n" + "="*80)
    print("VALIDAÇÃO DA PRIORIZAÇÃO DE BACKLOG")
    print("="*80)
    
    # Identificar coluna de score (pode ser score_human ou score)
    score_col = 'score_human' if 'score_human' in df_llm_merged.columns else 'score'
    if score_col not in df_llm_merged.columns:
        score_col = [c for c in df_llm_merged.columns if 'score' in c.lower()][0] if any('score' in c.lower() for c in df_llm_merged.columns) else None
    
    df_neg = df_llm_merged[df_llm_merged['negative'] == 1].copy()
    if score_col:
        df_neg[score_col] = pd.to_numeric(df_neg[score_col], errors='coerce')
    
    # Calcular prioridades humanas
    human_priorities = {}
    human_cat_col = lambda cat: f'{cat}_human' if f'{cat}_human' in df_neg.columns else cat
    
    for category in CATEGORIES:
        cat_col = human_cat_col(category)
        if cat_col in df_neg.columns:
            count = int(df_neg[cat_col].sum())
            if count > 0:
                severity = df_neg[df_neg[cat_col] == 1][score_col].mean() if score_col else 2.0
                # Score de prioridade: (frequência * 0.4) + ((5-severidade) * 0.3) + (impacto * 0.3)
                freq_norm = count / len(df_neg)
                sev_norm = (5 - severity) / 5
                impact = 0.9 if category in ['PIX', 'Login/Autenticação', 'Segurança'] else 0.7
                priority_score = (freq_norm * 0.4) + (sev_norm * 0.3) + (impact * 0.3)
                human_priorities[category] = priority_score
    
    # Calcular prioridades do LLM (usando colunas binárias)
    llm_priorities = {}
    llm_cat_col = lambda cat: f'{cat}_llm' if f'{cat}_llm' in df_llm_merged.columns else cat
    
    for category in CATEGORIES:
        llm_col = llm_cat_col(category)
        if llm_col in df_llm_merged.columns:
            llm_count = int(df_llm_merged[llm_col].sum())
            if llm_count > 0:
                llm_severity = df_llm_merged[df_llm_merged[llm_col] == 1][score_col].mean() if score_col else 2.0
                freq_norm = llm_count / len(df_llm_merged)
                sev_norm = (5 - llm_severity) / 5
                impact = 0.9 if category in ['PIX', 'Login/Autenticação', 'Segurança'] else 0.7
                priority_score = (freq_norm * 0.4) + (sev_norm * 0.3) + (impact * 0.3)
                llm_priorities[category] = priority_score
    
    # Ordenar por prioridade
    human_sorted = sorted(human_priorities.items(), key=lambda x: x[1], reverse=True)
    llm_sorted = sorted(llm_priorities.items(), key=lambda x: x[1], reverse=True) if llm_priorities else []
    
    print("\nTop 5 Categorias - Comparação:")
    print(f"{'Posição':<10} {'Humano':<25} {'LLM':<25}")
    print("-" * 60)
    
    for i in range(min(5, len(human_sorted))):
        human_cat, human_pri = human_sorted[i]
        llm_cat = llm_sorted[i][0] if i < len(llm_sorted) else "N/A"
        match = "✓" if human_cat == llm_cat else "✗"
        print(f"{i+1:<10} {human_cat:<25} {llm_cat:<25} {match}")
    
    # Calcular correlação de Spearman
    if llm_priorities:
        # Criar listas ordenadas de categorias
        human_order = [cat for cat, _ in human_sorted]
        llm_order = [cat for cat, _ in llm_sorted]
        
        # Criar ranking
        human_ranks = {cat: i+1 for i, cat in enumerate(human_order)}
        llm_ranks = {cat: i+1 for i, cat in enumerate(llm_order)}
        
        # Pegar categorias comuns
        common_cats = set(human_priorities.keys()) & set(llm_priorities.keys())
        if len(common_cats) > 1:
            human_rank_list = [human_ranks.get(cat, len(human_order)+1) for cat in common_cats]
            llm_rank_list = [llm_ranks.get(cat, len(llm_order)+1) for cat in common_cats]
            
            correlation, p_value = spearmanr(human_rank_list, llm_rank_list)
            
            print(f"\nCorrelação de Spearman: {correlation:.3f} (p-value: {p_value:.3f})")
            print(f"Meta: > 0.7 | Status: {'✅ ATINGIDO' if correlation > 0.7 else '❌ NÃO ATINGIDO'}")
        
        # Top-K Acurácia
        top3_human = set([cat for cat, _ in human_sorted[:3]])
        top3_llm = set([cat for cat, _ in llm_sorted[:3]]) if len(llm_sorted) >= 3 else set()
        top3_accuracy = len(top3_human & top3_llm) / 3
        
        print(f"\nTop-3 Acurácia: {top3_accuracy*100:.1f}%")
        print(f"Meta: > 70% | Status: {'✅ ATINGIDO' if top3_accuracy > 0.7 else '❌ NÃO ATINGIDO'}")
    
    return human_sorted, llm_sorted

def split_train_test(df, test_size=0.2, seed=42):
    """Divide dataset em treino e teste."""
    np.random.seed(seed)
    indices = np.random.permutation(len(df))
    test_indices = indices[:int(len(df) * test_size)]
    train_indices = indices[int(len(df) * test_size):]
    
    df_train = df.iloc[train_indices].copy()
    df_test = df.iloc[test_indices].copy()
    
    return df_train, df_test

def main():
    parser = argparse.ArgumentParser(
        description='Valida modelo de categorização e priorização'
    )
    parser.add_argument(
        '--human',
        type=str,
        default='app_review_dataset_carol.csv',
        help='Arquivo CSV com classificações humanas'
    )
    parser.add_argument(
        '--llm',
        type=str,
        default='functional_correlation_results.csv',
        help='Arquivo CSV com classificações do LLM'
    )
    parser.add_argument(
        '--test-size',
        type=float,
        default=0.2,
        help='Tamanho do conjunto de teste (padrao: 0.2 = 20 por cento)'
    )
    
    args = parser.parse_args()
    
    print("="*80)
    print("VALIDAÇÃO COMPLETA DO MODELO")
    print("="*80)
    
    # Carregar dados
    print(f"\nCarregando dados humanos: {args.human}")
    df_human = pd.read_csv(args.human, encoding='utf-8', sep=';')
    print(f"  Total: {len(df_human)} avaliações")
    
    print(f"\nCarregando dados LLM: {args.llm}")
    try:
        df_llm = pd.read_csv(args.llm, encoding='utf-8')
        print(f"  Total: {len(df_llm)} avaliações")
    except:
        print(f"  ⚠️  Arquivo não encontrado ou formato diferente")
        print(f"  Execute primeiro: python functional_correlation.py")
        return
    
    # Fazer merge - o LLM já tem colunas binárias de categorias
    llm_cols = ['reviewId', 'sentiment_label', 'score'] + [c for c in CATEGORIES if c in df_llm.columns]
    df_merged = df_human.merge(
        df_llm[llm_cols],
        on='reviewId',
        how='inner',
        suffixes=('_human', '_llm')
    )
    
    print(f"\nAvaliações em comum: {len(df_merged)}")
    
    # Renomear colunas de categoria do LLM para adicionar sufixo _llm
    for category in CATEGORIES:
        if category in df_merged.columns and f'{category}_human' not in df_merged.columns:
            # Se a coluna existe mas não tem sufixo, renomear
            if category in df_llm.columns:
                df_merged = df_merged.rename(columns={category: f'{category}_llm'})
    
    # Garantir que temos colunas _human e _llm
    for category in CATEGORIES:
        if category in df_human.columns:
            if f'{category}_human' not in df_merged.columns:
                df_merged[f'{category}_human'] = df_merged[category]
        if category in df_llm.columns:
            if f'{category}_llm' not in df_merged.columns:
                df_merged[f'{category}_llm'] = df_merged[category] if category in df_merged.columns else 0
    
    # Divisão treino/teste
    print(f"\n{'='*80}")
    print("DIVISÃO TREINO/TESTE")
    print("="*80)
    
    df_train, df_test = split_train_test(df_merged, test_size=args.test_size)
    print(f"\nTreino: {len(df_train)} avaliações ({len(df_train)/len(df_merged)*100:.1f}%)")
    print(f"Teste: {len(df_test)} avaliações ({len(df_test)/len(df_merged)*100:.1f}%)")
    
    # Validação da categorização (usar teste)
    cat_metrics = calculate_categorization_metrics(df_human, df_test)
    
    # Validação da priorização (usar todas)
    prior_metrics = calculate_priorization_metrics(df_human, df_merged)
    
    print("\n" + "="*80)
    print("RESUMO DA VALIDAÇÃO")
    print("="*80)
    print("\n✅ Próximos Passos:")
    print("1. Receber segunda classificação manual")
    print("2. Calcular inter-annotator agreement")
    print("3. Resolver discrepâncias e criar ground truth")
    print("4. Re-executar validação com ground truth final")
    print("5. Ajustar prompts do LLM se métricas não atingirem meta")

if __name__ == "__main__":
    main()

