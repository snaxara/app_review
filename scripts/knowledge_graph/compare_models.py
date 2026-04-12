"""
Script para comparar diferentes modelos GPT na extração de entidades
Processa os mesmos comentários com diferentes modelos e compara métricas de correlação
"""

import sys
import os
import pandas as pd
import json
from typing import Dict, List
from datetime import datetime
import argparse

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.graph_manager import GraphManager
from knowledge_graph.process_reviews_to_graph import process_csv_to_graph
from knowledge_graph.calculate_correlation_metrics import (
    get_issues_by_capability,
    calculate_capability_statistics,
    calculate_distribution_percentages
)


def clear_episodes_and_entities(graph: GraphManager):
    """Remove todos os episódios e entidades do grafo, mantendo apenas BusinessCapabilities."""
    print("Limpando episódios e entidades anteriores...")
    
    # Remover relacionamentos primeiro
    graph.execute_query("MATCH ()-[r:CONTAINS_ENTITY]->() DELETE r")
    graph.execute_query("MATCH ()-[r:RELATES_TO_CAPABILITY]->() DELETE r")
    
    # Remover episódios e entidades
    graph.execute_query("MATCH (ep:Episode) DETACH DELETE ep")
    graph.execute_query("MATCH (e) WHERE 'Issue' IN labels(e) OR 'App' IN labels(e) OR 'Version' IN labels(e) DETACH DELETE e")
    
    print("Limpeza concluída!")


def process_with_model(csv_path: str, model_name: str, graph: GraphManager, 
                      limit: int = 20, batch_size: int = 5) -> Dict:
    """
    Processa comentários com um modelo específico.
    
    Args:
        csv_path: Caminho para CSV com comentários
        model_name: Nome do modelo GPT a usar
        graph: Instância do GraphManager
        limit: Limite de comentários para processar
        batch_size: Tamanho do lote
        
    Returns:
        Estatísticas do processamento
    """
    print(f"\n{'=' * 80}")
    print(f"PROCESSANDO COM MODELO: {model_name}")
    print(f"{'=' * 80}")
    
    # Definir variável de ambiente temporariamente
    original_model = os.environ.get('OPENAI_MODEL')
    os.environ['OPENAI_MODEL'] = model_name
    
    try:
        # Limpar dados anteriores
        clear_episodes_and_entities(graph)
        
        # Processar comentários
        stats = process_csv_to_graph(csv_path, graph, limit=limit, batch_size=batch_size)
        
        if not stats:
            print(f"ERRO: Falha ao processar com modelo {model_name}")
            return None
        
        # Calcular métricas de correlação
        print(f"\nCalculando métricas de correlação para {model_name}...")
        df = get_issues_by_capability(graph)
        
        if df.empty:
            print(f"AVISO: Nenhuma métrica calculada para {model_name}")
            return None
        
        capability_stats = calculate_capability_statistics(df)
        distribution = calculate_distribution_percentages(capability_stats)
        
        metrics = {
            'model': model_name,
            'processed_reviews': stats.get('processed', 0),
            'errors': stats.get('errors', 0),
            'total_issues': len(df['Issue'].unique()),
            'total_capabilities': len(df['BusinessCapability'].unique()),
            'total_episodes': int(df['TotalEpisodes'].sum()),
            'capability_statistics': capability_stats,
            'distribution': distribution,
            'top_10_issues': df.groupby('Issue')['TotalEpisodes'].sum().nlargest(10).to_dict()
        }
        
        return metrics
        
    except Exception as e:
        print(f"ERRO ao processar com modelo {model_name}: {e}")
        import traceback
        traceback.print_exc()
        return None
        
    finally:
        # Restaurar modelo original
        if original_model:
            os.environ['OPENAI_MODEL'] = original_model
        elif 'OPENAI_MODEL' in os.environ:
            del os.environ['OPENAI_MODEL']


def generate_comparison_report(results: List[Dict], output_path: str):
    """Gera relatório comparativo entre modelos."""
    
    report_lines = []
    report_lines.append("=" * 80)
    report_lines.append("COMPARACAO DE MODELOS GPT - METRICAS DE CORRELACAO")
    report_lines.append("=" * 80)
    report_lines.append(f"Data de geracao: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    report_lines.append("")
    
    # Resumo geral
    report_lines.append("RESUMO GERAL")
    report_lines.append("-" * 80)
    report_lines.append(f"Modelos testados: {len(results)}")
    report_lines.append(f"Comentarios processados por modelo: {results[0]['processed_reviews'] if results else 'N/A'}")
    report_lines.append("")
    
    # Tabela comparativa
    report_lines.append("COMPARACAO DE METRICAS")
    report_lines.append("-" * 80)
    report_lines.append(f"{'Modelo':<30} {'Issues':<10} {'Capabilities':<15} {'Episodios':<12} {'Erros':<8}")
    report_lines.append("-" * 80)
    
    for result in results:
        model = result['model']
        issues = result['total_issues']
        capabilities = result['total_capabilities']
        episodes = result['total_episodes']
        errors = result['errors']
        report_lines.append(f"{model:<30} {issues:<10} {capabilities:<15} {episodes:<12} {errors:<8}")
    
    report_lines.append("")
    
    # Detalhes por modelo
    for result in results:
        model = result['model']
        report_lines.append("=" * 80)
        report_lines.append(f"MODELO: {model}")
        report_lines.append("-" * 80)
        report_lines.append(f"Total de Issues: {result['total_issues']}")
        report_lines.append(f"Total de BusinessCapabilities: {result['total_capabilities']}")
        report_lines.append(f"Total de Episodios: {result['total_episodes']}")
        report_lines.append(f"Erros: {result['errors']}")
        report_lines.append("")
        
        # Top 5 Capabilities por número de episódios
        report_lines.append("Top 5 BusinessCapabilities (por numero de episodios):")
        stats = result['capability_statistics']
        sorted_stats = sorted(stats.items(), key=lambda x: x[1]['total_episodes'], reverse=True)[:5]
        
        for i, (capability, stat) in enumerate(sorted_stats, 1):
            report_lines.append(f"  {i}. {capability}: {stat['total_episodes']} episodios ({stat['total_issues']} issues)")
        
        report_lines.append("")
        
        # Top 5 Issues
        report_lines.append("Top 5 Issues (por numero de episodios):")
        top_issues = sorted(result['top_10_issues'].items(), key=lambda x: x[1], reverse=True)[:5]
        
        for i, (issue, episodes) in enumerate(top_issues, 1):
            report_lines.append(f"  {i}. {issue}: {episodes} episodio(s)")
        
        report_lines.append("")
    
    # Análise comparativa
    report_lines.append("=" * 80)
    report_lines.append("ANALISE COMPARATIVA")
    report_lines.append("-" * 80)
    
    if len(results) > 1:
        # Modelo com mais issues
        max_issues = max(results, key=lambda x: x['total_issues'])
        report_lines.append(f"Modelo com mais Issues extraidas: {max_issues['model']} ({max_issues['total_issues']} issues)")
        
        # Modelo com mais episódios
        max_episodes = max(results, key=lambda x: x['total_episodes'])
        report_lines.append(f"Modelo com mais Episodios: {max_episodes['model']} ({max_episodes['total_episodes']} episodios)")
        
        # Modelo com menos erros
        min_errors = min(results, key=lambda x: x['errors'])
        report_lines.append(f"Modelo com menos erros: {min_errors['model']} ({min_errors['errors']} erros)")
    
    report_lines.append("")
    report_lines.append("=" * 80)
    
    report_text = "\n".join(report_lines)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(report_text)
    
    print(f"\nRelatorio comparativo salvo em: {output_path}")
    return report_text


def main():
    parser = argparse.ArgumentParser(description="Compara diferentes modelos GPT na extração de entidades")
    parser.add_argument("--input", default="sentiment_results.csv",
                      help="CSV com comentários para processar")
    parser.add_argument("--models", nargs='+', 
                      default=['gpt-4o-mini', 'gpt-4o-2024-08-06', 'gpt-oss-20b', 'gpt-5.2-2025-12-11'],
                      help="Lista de modelos para testar")
    parser.add_argument("--limit", type=int, default=20,
                      help="Limite de comentários para processar (padrão: 20)")
    parser.add_argument("--batch-size", type=int, default=5,
                      help="Tamanho do lote (padrão: 5)")
    parser.add_argument("--output-report", default="reports/model_comparison.txt",
                      help="Caminho para salvar relatório comparativo")
    parser.add_argument("--output-json", default="reports/model_comparison.json",
                      help="Caminho para salvar resultados em JSON")
    
    args = parser.parse_args()
    
    # Verificar se CSV existe
    csv_path = args.input
    if not os.path.exists(csv_path):
        csv_path = os.path.join(scripts_dir, '..', csv_path)
        if not os.path.exists(csv_path):
            print(f"ERRO: Arquivo CSV não encontrado: {args.input}")
            return
    
    print("=" * 80)
    print("COMPARACAO DE MODELOS GPT")
    print("=" * 80)
    print(f"CSV de entrada: {csv_path}")
    print(f"Modelos para testar: {', '.join(args.models)}")
    print(f"Limite de comentarios: {args.limit}")
    print("")
    
    results = []
    
    with GraphManager() as graph:
        graph.initialize_indices()
        
        # Verificar se BusinessCapabilities existem
        check_capabilities_query = "MATCH (bc:BusinessCapability) RETURN count(bc) as count"
        result = graph.execute_query(check_capabilities_query)
        capabilities_count = result[0]['count'] if result else 0
        
        if capabilities_count == 0:
            print("BusinessCapabilities nao encontradas. Inicializando...")
            from knowledge_graph.create_capabilities import create_capabilities_from_categories
            create_capabilities_from_categories(graph)
            print("BusinessCapabilities criadas com sucesso!")
        
        # Processar com cada modelo
        for model in args.models:
            metrics = process_with_model(csv_path, model, graph, args.limit, args.batch_size)
            if metrics:
                results.append(metrics)
        
        if not results:
            print("ERRO: Nenhum modelo foi processado com sucesso!")
            return
        
        # Gerar relatório comparativo
        print("\n" + "=" * 80)
        print("GERANDO RELATORIO COMPARATIVO")
        print("=" * 80)
        
        os.makedirs(os.path.dirname(args.output_report), exist_ok=True)
        report = generate_comparison_report(results, args.output_report)
        print(report)
        
        # Salvar JSON
        if args.output_json:
            os.makedirs(os.path.dirname(args.output_json), exist_ok=True)
            json_data = {
                'generated_at': datetime.now().isoformat(),
                'models_tested': args.models,
                'comments_processed': args.limit,
                'results': results
            }
            
            with open(args.output_json, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, ensure_ascii=False, indent=2)
            print(f"\nResultados JSON salvos em: {args.output_json}")


if __name__ == "__main__":
    main()
