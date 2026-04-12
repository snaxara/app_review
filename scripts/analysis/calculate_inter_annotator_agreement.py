"""
Script para calcular inter-annotator agreement entre Carol e Samuel
e criar ground truth resolvendo discrepâncias

Uso:
    python calculate_inter_annotator_agreement.py
"""

import pandas as pd
import numpy as np
from sklearn.metrics import cohen_kappa_score
from collections import Counter
from datetime import datetime

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

def load_datasets():
    """Carrega os datasets de Carol e Samuel."""
    
    print("="*80)
    print("CÁLCULO DE INTER-ANNOTATOR AGREEMENT")
    print("="*80)
    print(f"Data: {datetime.now().strftime('%d/%m/%Y %H:%M')}\n")
    
    print("Carregando datasets...")
    df_carol = pd.read_csv('data/app_review_dataset_carol.csv', encoding='utf-8', sep=';')
    df_samuel = pd.read_csv('data/app_review_dataset_samuel.csv', encoding='utf-8', sep=';')
    
    print(f"Carol: {len(df_carol)} avaliacoes")
    print(f"Samuel: {len(df_samuel)} avaliacoes")
    
    # Fazer merge por reviewId
    df_merged = df_carol.merge(
        df_samuel,
        on='reviewId',
        how='inner',
        suffixes=('_carol', '_samuel')
    )
    
    print(f"Avaliacoes em comum: {len(df_merged)}")
    
    return df_merged

def calculate_kappa_by_category(df_merged):
    """Calcula Cohen's Kappa por categoria."""
    
    print("\n" + "="*80)
    print("COHEN'S KAPPA POR CATEGORIA")
    print("="*80)
    
    kappa_results = {}
    
    print(f"\n{'Categoria':<30} {'Kappa':<12} {'Interpretação':<20} {'Carol':<10} {'Samuel':<10}")
    print("-" * 85)
    
    for category in CATEGORIES:
        carol_col = f'{category}_carol' if f'{category}_carol' in df_merged.columns else category
        samuel_col = f'{category}_samuel' if f'{category}_samuel' in df_merged.columns else category
        
        if carol_col not in df_merged.columns or samuel_col not in df_merged.columns:
            continue
        
        y_carol = df_merged[carol_col].values
        y_samuel = df_merged[samuel_col].values
        
        # Calcular Kappa
        kappa = cohen_kappa_score(y_carol, y_samuel)
        
        # Interpretação
        if kappa < 0:
            interpretation = "Pior que aleatorio"
        elif kappa < 0.2:
            interpretation = "Insignificante"
        elif kappa < 0.4:
            interpretation = "Razoavel"
        elif kappa < 0.6:
            interpretation = "Moderada"
        elif kappa < 0.8:
            interpretation = "Substancial OK"
        else:
            interpretation = "Quase perfeita OK"
        
        carol_count = int(y_carol.sum())
        samuel_count = int(y_samuel.sum())
        
        kappa_results[category] = {
            'kappa': kappa,
            'interpretation': interpretation,
            'carol_count': carol_count,
            'samuel_count': samuel_count
        }
        
        print(f"{category:<30} {kappa:>10.3f}  {interpretation:<20} {carol_count:>10} {samuel_count:>10}")
    
    # Kappa médio (ignorar NaN)
    valid_kappas = [r['kappa'] for r in kappa_results.values() if not np.isnan(r['kappa'])]
    avg_kappa = np.mean(valid_kappas) if valid_kappas else 0
    substantial_agreement = sum(1 for r in kappa_results.values() if not np.isnan(r['kappa']) and r['kappa'] >= 0.6)
    
    print("\n" + "-"*85)
    print(f"Kappa Médio: {avg_kappa:.3f}")
    print(f"Categorias com concordancia substancial (Kappa >= 0.6): {substantial_agreement}/{len(kappa_results)}")
    print(f"Meta: Kappa > 0.7 | Status: {'ATINGIDO' if avg_kappa > 0.7 else 'NAO ATINGIDO'}")
    
    return kappa_results

def analyze_discrepancies(df_merged):
    """Analisa discrepâncias entre classificadores."""
    
    print("\n" + "="*80)
    print("ANÁLISE DE DISCREPÂNCIAS")
    print("="*80)
    
    discrepancies = []
    
    for category in CATEGORIES:
        carol_col = f'{category}_carol' if f'{category}_carol' in df_merged.columns else category
        samuel_col = f'{category}_samuel' if f'{category}_samuel' in df_merged.columns else category
        
        if carol_col not in df_merged.columns or samuel_col not in df_merged.columns:
            continue
        
        # Casos onde Carol marcou mas Samuel não
        carol_yes_samuel_no = df_merged[
            (df_merged[carol_col] == 1) & (df_merged[samuel_col] == 0)
        ]
        
        # Casos onde Samuel marcou mas Carol não
        samuel_yes_carol_no = df_merged[
            (df_merged[carol_col] == 0) & (df_merged[samuel_col] == 1)
        ]
        
        # Casos onde ambos concordam
        both_yes = df_merged[
            (df_merged[carol_col] == 1) & (df_merged[samuel_col] == 1)
        ]
        
        # Casos onde ambos concordam que não
        both_no = df_merged[
            (df_merged[carol_col] == 0) & (df_merged[samuel_col] == 0)
        ]
        
        total_discrepancies = len(carol_yes_samuel_no) + len(samuel_yes_carol_no)
        total_agreements = len(both_yes) + len(both_no)
        agreement_rate = total_agreements / len(df_merged) * 100 if len(df_merged) > 0 else 0
        
        if total_discrepancies > 0:
            discrepancies.append({
                'category': category,
                'carol_yes_samuel_no': len(carol_yes_samuel_no),
                'samuel_yes_carol_no': len(samuel_yes_carol_no),
                'both_yes': len(both_yes),
                'both_no': len(both_no),
                'total_discrepancies': total_discrepancies,
                'agreement_rate': agreement_rate
            })
    
    if discrepancies:
        print(f"\n{'Categoria':<30} {'Carol+ Samuel-':<15} {'Samuel+ Carol-':<15} {'Ambos+':<10} {'Taxa Acordo':<12}")
        print("-" * 90)
        
        for disc in sorted(discrepancies, key=lambda x: x['total_discrepancies'], reverse=True):
            print(f"{disc['category']:<30} {disc['carol_yes_samuel_no']:<15} {disc['samuel_yes_carol_no']:<15} "
                  f"{disc['both_yes']:<10} {disc['agreement_rate']:.1f}%")
    
    return discrepancies

def create_ground_truth(df_merged, strategy='majority'):
    """Cria ground truth resolvendo discrepâncias."""
    
    print("\n" + "="*80)
    print("CRIANDO GROUND TRUTH")
    print("="*80)
    print(f"Estratégia: {strategy}\n")
    
    df_gt = df_merged[['reviewId', 'content_carol', 'score_carol', 'negative_carol', 'positive_carol', 'neutral_carol']].copy()
    df_gt.columns = ['reviewId', 'content', 'score', 'negative', 'positive', 'neutral']
    
    # Criar ground truth para cada categoria
    for category in CATEGORIES:
        carol_col = f'{category}_carol' if f'{category}_carol' in df_merged.columns else category
        samuel_col = f'{category}_samuel' if f'{category}_samuel' in df_merged.columns else category
        
        if carol_col not in df_merged.columns or samuel_col not in df_merged.columns:
            continue
        
        if strategy == 'majority':
            # Maioria vence (se pelo menos um marcou, marca)
            df_gt[category] = ((df_merged[carol_col] == 1) | (df_merged[samuel_col] == 1)).astype(int)
        elif strategy == 'consensus':
            # Apenas se ambos concordarem
            df_gt[category] = ((df_merged[carol_col] == 1) & (df_merged[samuel_col] == 1)).astype(int)
        elif strategy == 'carol':
            # Usar apenas Carol como referência
            df_gt[category] = df_merged[carol_col].astype(int)
        else:
            # Default: majority
            df_gt[category] = ((df_merged[carol_col] == 1) | (df_merged[samuel_col] == 1)).astype(int)
    
    # Estatísticas do ground truth
    print("Estatísticas do Ground Truth:")
    print(f"  Total de avaliações: {len(df_gt)}")
    
    neg_count = df_gt['negative'].sum()
    print(f"  Avaliações negativas: {neg_count}")
    
    print(f"\n  Distribuição de categorias (apenas negativas):")
    df_neg = df_gt[df_gt['negative'] == 1]
    for category in CATEGORIES:
        if category in df_gt.columns:
            count = int(df_neg[category].sum())
            if count > 0:
                pct = (count / neg_count * 100) if neg_count > 0 else 0
                print(f"    {category}: {count} ({pct:.1f}%)")
    
    # Salvar ground truth
    output_file = 'data/ground_truth_dataset.csv'
    df_gt.to_csv(output_file, index=False, encoding='utf-8', sep=';')
    print(f"\nGround truth salvo em: {output_file}")
    
    return df_gt

def main():
    # Carregar datasets
    df_merged = load_datasets()
    
    # Calcular Kappa por categoria
    kappa_results = calculate_kappa_by_category(df_merged)
    
    # Analisar discrepâncias
    discrepancies = analyze_discrepancies(df_merged)
    
    # Criar ground truth
    df_ground_truth = create_ground_truth(df_merged, strategy='majority')
    
    # Resumo final
    print("\n" + "="*80)
    print("RESUMO FINAL")
    print("="*80)
    
    valid_kappas = [r['kappa'] for r in kappa_results.values() if not np.isnan(r['kappa'])]
    avg_kappa = np.mean(valid_kappas) if valid_kappas else 0
    total_discrepancies = sum(d['total_discrepancies'] for d in discrepancies)
    
    print(f"\nKappa Medio: {avg_kappa:.3f}")
    print(f"Total de discrepancias: {total_discrepancies}")
    print(f"Ground truth criado: {len(df_ground_truth)} avaliacoes")
    
    print("\n📋 Próximos Passos:")
    print("1. Revisar discrepâncias críticas manualmente (se necessário)")
    print("2. Usar ground truth para validar modelo LLM")
    print("3. Executar: python validate_model.py --human ground_truth_dataset.csv --llm functional_correlation_results.csv")
    print("4. Ajustar prompts do LLM baseado em erros identificados")

if __name__ == "__main__":
    main()

