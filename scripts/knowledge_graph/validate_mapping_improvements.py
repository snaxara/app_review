"""
Script para validar melhorias no mapeamento comparando com CSV de validação manual
"""

import pandas as pd
import sys
import os

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)


def compare_mappings(validation_csv: str, current_csv: str):
    """
    Compara os mapeamentos do CSV de validação com os resultados atuais.
    
    Args:
        validation_csv: Caminho para CSV de validação manual
        current_csv: Caminho para CSV atual gerado
    """
    # Carregar CSVs
    df_val = pd.read_csv(validation_csv, sep=';', encoding='utf-8')
    df_curr = pd.read_csv(current_csv, sep=';', encoding='utf-8')
    
    print("=" * 80)
    print("VALIDACAO DE MELHORIAS NO MAPEAMENTO")
    print("=" * 80)
    print(f"\nCSV de Validacao: {validation_csv}")
    print(f"CSV Atual: {current_csv}")
    print(f"\nTotal de linhas na validacao: {len(df_val)}")
    print(f"Total de linhas no atual: {len(df_curr)}")
    
    # Criar dicionário de validação: (review_id, issue) -> business_capability_correta
    validation_map = {}
    for _, row in df_val.iterrows():
        review_id = str(row['review_id'])
        issue = str(row['issue']).strip()
        bc_correct = str(row['business_capability_ajuste']).strip()
        if bc_correct and bc_correct != 'nan':
            validation_map[(review_id, issue)] = bc_correct
    
    # Comparar com resultados atuais
    correct = 0
    incorrect = 0
    not_found = 0
    improvements = []
    still_wrong = []
    
    print("\n" + "=" * 80)
    print("COMPARACAO DE MAPEAMENTOS")
    print("=" * 80)
    
    for _, row in df_val.iterrows():
        review_id = str(row['review_id'])
        issue = str(row['issue']).strip()
        bc_old = str(row['business_capability']).strip()
        bc_correct = str(row['business_capability_ajuste']).strip()
        
        if not bc_correct or bc_correct == 'nan':
            continue
        
        # Buscar no CSV atual
        current_rows = df_curr[(df_curr['review_id'] == review_id) & 
                               (df_curr['issue'].str.strip() == issue)]
        
        if len(current_rows) == 0:
            not_found += 1
            print(f"\n[NAO ENCONTRADO] Review: {review_id[:8]}... | Issue: {issue}")
            print(f"  Esperado: {bc_correct}")
            continue
        
        bc_current = str(current_rows.iloc[0]['business_capability']).strip()
        
        # Normalizar nomes para comparação
        bc_correct_norm = bc_correct.lower().replace(' ', '').replace('/', '')
        bc_current_norm = bc_current.lower().replace(' ', '').replace('/', '')
        
        if bc_correct_norm == bc_current_norm or bc_correct in bc_current or bc_current in bc_correct:
            correct += 1
            if bc_old != bc_correct:
                improvements.append({
                    'review_id': review_id,
                    'issue': issue,
                    'old': bc_old,
                    'new': bc_current,
                    'correct': bc_correct
                })
        else:
            incorrect += 1
            still_wrong.append({
                'review_id': review_id,
                'issue': issue,
                'old': bc_old,
                'current': bc_current,
                'correct': bc_correct
            })
            print(f"\n[INCORRETO] Review: {review_id[:8]}... | Issue: {issue}")
            print(f"  Antes: {bc_old}")
            print(f"  Agora: {bc_current}")
            print(f"  Esperado: {bc_correct}")
    
    # Estatísticas
    total = correct + incorrect + not_found
    print("\n" + "=" * 80)
    print("ESTATISTICAS")
    print("=" * 80)
    print(f"Total de mapeamentos validados: {total}")
    print(f"  [OK] Corretos: {correct} ({correct/total*100:.1f}%)")
    print(f"  [ERRO] Ainda incorretos: {incorrect} ({incorrect/total*100:.1f}%)")
    print(f"  [AVISO] Nao encontrados: {not_found} ({not_found/total*100:.1f}%)")
    
    if improvements:
        print(f"\n[MELHORIAS APLICADAS]: {len(improvements)}")
        print("-" * 80)
        for imp in improvements[:10]:  # Mostrar primeiras 10
            print(f"Issue: {imp['issue']}")
            print(f"  Antes: {imp['old']}")
            print(f"  Agora: {imp['new']} [CORRIGIDO]")
    
    if still_wrong:
        print(f"\n[AINDA PRECISAM AJUSTE]: {len(still_wrong)}")
        print("-" * 80)
        for wrong in still_wrong[:10]:  # Mostrar primeiras 10
            print(f"Issue: {wrong['issue']}")
            print(f"  Atual: {wrong['current']}")
            print(f"  Esperado: {wrong['correct']}")
    
    return {
        'correct': correct,
        'incorrect': incorrect,
        'not_found': not_found,
        'total': total,
        'improvements': improvements,
        'still_wrong': still_wrong
    }


if __name__ == "__main__":
    validation_csv = "validation_BC.csv"
    current_csv = "reports/model_data_gpt-4o-mini.csv"
    
    if not os.path.exists(validation_csv):
        print(f"ERRO: Arquivo de validacao nao encontrado: {validation_csv}")
        sys.exit(1)
    
    if not os.path.exists(current_csv):
        print(f"ERRO: CSV atual nao encontrado: {current_csv}")
        sys.exit(1)
    
    results = compare_mappings(validation_csv, current_csv)
    
    print("\n" + "=" * 80)
    print("VALIDACAO CONCLUIDA")
    print("=" * 80)
