"""
Script para comparar acurácia de todos os modelos usando CSV de validação manual
"""

import pandas as pd
import sys
import os
from typing import Dict, List

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)


def validate_model_accuracy(validation_csv: str, model_csv: str, model_name: str) -> Dict:
    """
    Valida acurácia de um modelo comparando com CSV de validação manual.
    
    Args:
        validation_csv: Caminho para CSV de validação manual
        model_csv: Caminho para CSV gerado pelo modelo
        model_name: Nome do modelo
        
    Returns:
        Dicionário com estatísticas de acurácia
    """
    # Carregar CSVs
    df_val = pd.read_csv(validation_csv, sep=';', encoding='utf-8')
    df_model = pd.read_csv(model_csv, sep=';', encoding='utf-8')
    
    correct = 0
    incorrect = 0
    not_found = 0
    improvements = []
    errors = []
    
    for _, row in df_val.iterrows():
        review_id = str(row['review_id'])
        issue = str(row['issue']).strip()
        bc_old = str(row['business_capability']).strip()
        bc_correct = str(row['business_capability_ajuste']).strip()
        
        if not bc_correct or bc_correct == 'nan':
            continue
        
        # Buscar no CSV do modelo
        current_rows = df_model[(df_model['review_id'] == review_id) & 
                               (df_model['issue'].str.strip() == issue)]
        
        if len(current_rows) == 0:
            not_found += 1
            continue
        
        bc_current = str(current_rows.iloc[0]['business_capability']).strip()
        
        # Normalizar nomes para comparação
        bc_correct_norm = bc_correct.lower().replace(' ', '').replace('/', '').replace('-', '')
        bc_current_norm = bc_current.lower().replace(' ', '').replace('/', '').replace('-', '')
        
        # Verificar se está correto (exato ou contém)
        is_correct = (bc_correct_norm == bc_current_norm or 
                     bc_correct in bc_current or 
                     bc_current in bc_correct or
                     bc_current == 'Sem BusinessCapability' and 'Outra Business Capability' in bc_correct)
        
        if is_correct:
            correct += 1
            if bc_old != bc_correct:
                improvements.append({
                    'issue': issue,
                    'old': bc_old,
                    'new': bc_current
                })
        else:
            incorrect += 1
            errors.append({
                'issue': issue,
                'current': bc_current,
                'correct': bc_correct
            })
    
    total = correct + incorrect + not_found
    accuracy = (correct / total * 100) if total > 0 else 0
    
    return {
        'model': model_name,
        'correct': correct,
        'incorrect': incorrect,
        'not_found': not_found,
        'total': total,
        'accuracy': accuracy,
        'improvements': improvements,
        'errors': errors
    }


def generate_accuracy_report(results: List[Dict], output_path: str):
    """Gera relatório comparativo de acurácia."""
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("COMPARACAO DE ACURACIA ENTRE MODELOS GPT")
    report_lines.append("=" * 80)
    report_lines.append("Validacao baseada em CSV manual com 22 mapeamentos validados")
    report_lines.append("")
    
    # Tabela comparativa
    report_lines.append("RESUMO DE ACURACIA POR MODELO")
    report_lines.append("-" * 80)
    report_lines.append(f"{'Modelo':<30} {'Corretos':<10} {'Incorretos':<12} {'Nao Encontrados':<18} {'Acuracia':<10}")
    report_lines.append("-" * 80)
    
    # Ordenar por acurácia
    sorted_results = sorted(results, key=lambda x: x['accuracy'], reverse=True)
    
    for result in sorted_results:
        model = result['model']
        correct = result['correct']
        incorrect = result['incorrect']
        not_found = result['not_found']
        accuracy = result['accuracy']
        report_lines.append(f"{model:<30} {correct:<10} {incorrect:<12} {not_found:<18} {accuracy:.1f}%")
    
    report_lines.append("")
    
    # Detalhes por modelo
    for result in sorted_results:
        model = result['model']
        report_lines.append("=" * 80)
        report_lines.append(f"MODELO: {model}")
        report_lines.append("-" * 80)
        report_lines.append(f"Acuracia: {result['accuracy']:.1f}%")
        report_lines.append(f"Corretos: {result['correct']}/{result['total']}")
        report_lines.append(f"Incorretos: {result['incorrect']}")
        report_lines.append(f"Nao encontrados: {result['not_found']}")
        
        if result['errors']:
            report_lines.append("")
            report_lines.append("Erros encontrados:")
            for error in result['errors'][:5]:  # Mostrar primeiros 5
                report_lines.append(f"  - Issue: {error['issue']}")
                report_lines.append(f"    Atual: {error['current']}")
                report_lines.append(f"    Esperado: {error['correct']}")
        
        report_lines.append("")
    
    # Ranking
    report_lines.append("=" * 80)
    report_lines.append("RANKING DE MODELOS POR ACURACIA")
    report_lines.append("-" * 80)
    for i, result in enumerate(sorted_results, 1):
        report_lines.append(f"{i}. {result['model']}: {result['accuracy']:.1f}%")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    
    report_text = "\n".join(report_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\nRelatorio de acuracia salvo em: {output_path}")
    return report_text


def main():
    validation_csv = "validation_BC.csv"
    models = [
        ('gpt-4o-mini', 'reports/model_data_gpt-4o-mini.csv'),
        ('gpt-4o-2024-08-06', 'reports/model_data_gpt-4o-2024-08-06.csv'),
        ('gpt-oss-20b', 'reports/model_data_gpt-oss-20b.csv'),
        ('gpt-5.2-2025-12-11', 'reports/model_data_gpt-5.2-2025-12-11.csv')
    ]
    
    if not os.path.exists(validation_csv):
        print(f"ERRO: Arquivo de validacao nao encontrado: {validation_csv}")
        sys.exit(1)
    
    print("=" * 80)
    print("COMPARACAO DE ACURACIA ENTRE MODELOS")
    print("=" * 80)
    print(f"CSV de Validacao: {validation_csv}")
    print("")
    
    results = []
    
    for model_name, model_csv in models:
        if not os.path.exists(model_csv):
            print(f"AVISO: CSV do modelo {model_name} nao encontrado: {model_csv}")
            continue
        
        print(f"Validando modelo: {model_name}...")
        result = validate_model_accuracy(validation_csv, model_csv, model_name)
        results.append(result)
        print(f"  Acuracia: {result['accuracy']:.1f}% ({result['correct']}/{result['total']} corretos)")
    
    if not results:
        print("ERRO: Nenhum modelo foi validado!")
        return
    
    # Gerar relatório
    output_path = "reports/model_accuracy_comparison.txt"
    report = generate_accuracy_report(results, output_path)
    print(report)


if __name__ == "__main__":
    main()
