"""
Script para exportar dados de cada modelo em CSV
Gera um CSV por modelo com: comentário, Issue extraída e BusinessCapability associada
"""

import sys
import os
import pandas as pd
from typing import Dict, List
import argparse

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.graph_manager import GraphManager
from knowledge_graph.process_reviews_to_graph import process_csv_to_graph
from knowledge_graph.filter_generic_comments import filter_generic_comments


def clear_episodes_and_entities(graph: GraphManager):
    """Remove todos os episódios e entidades do grafo, mantendo apenas BusinessCapabilities."""
    print("Limpando episodios e entidades anteriores...")
    
    # Remover relacionamentos primeiro
    graph.execute_query("MATCH ()-[r:CONTAINS_ENTITY]->() DELETE r")
    graph.execute_query("MATCH ()-[r:RELATES_TO_CAPABILITY]->() DELETE r")
    
    # Remover episódios e entidades
    graph.execute_query("MATCH (ep:Episode) DETACH DELETE ep")
    graph.execute_query("MATCH (e) WHERE 'Issue' IN labels(e) OR 'App' IN labels(e) OR 'Version' IN labels(e) DETACH DELETE e")
    
    print("Limpeza concluida!")


def export_model_data_to_csv(graph: GraphManager, model_name: str, output_path: str):
    """
    Exporta dados do grafo para CSV com comentário, Issue e BusinessCapability.
    
    Args:
        graph: Instância do GraphManager
        model_name: Nome do modelo
        output_path: Caminho para salvar CSV
    """
    query = """
    MATCH (ep:Episode)-[:CONTAINS_ENTITY]->(e)
    WHERE 'Issue' IN labels(e)
    OPTIONAL MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability)
    RETURN 
        ep.id AS review_id,
        ep.content AS comentario,
        ep.app_name AS app_name,
        e.name AS issue,
        COALESCE(bc.name, 'Sem BusinessCapability') AS business_capability,
        COALESCE(bc.level, NULL) AS capability_level,
        COALESCE(bc.capability_type, NULL) AS capability_type,
        COALESCE(bc.business_value, NULL) AS business_value
    ORDER BY ep.id, e.name, bc.name
    """
    
    result = graph.execute_query(query)
    
    if not result:
        print(f"AVISO: Nenhum dado encontrado para modelo {model_name}")
        return None
    
    df = pd.DataFrame(result)
    
    # Salvar CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False, encoding='utf-8-sig', sep=';')
    
    print(f"CSV gerado: {output_path}")
    print(f"  Total de linhas: {len(df)}")
    print(f"  Comentarios unicos: {df['review_id'].nunique()}")
    print(f"  Issues unicas: {df['issue'].nunique()}")
    print(f"  BusinessCapabilities: {df['business_capability'].nunique()}")
    
    return df


def process_and_export_model(csv_path: str, model_name: str, graph: GraphManager,
                            limit: int = 20, batch_size: int = 5, output_dir: str = "reports"):
    """
    Processa comentários com um modelo e exporta para CSV.
    
    Args:
        csv_path: Caminho para CSV com comentários
        model_name: Nome do modelo GPT a usar
        graph: Instância do GraphManager
        limit: Limite de comentários para processar
        batch_size: Tamanho do lote
        output_dir: Diretório para salvar CSVs
        
    Returns:
        Caminho do CSV gerado
    """
    print(f"\n{'=' * 80}")
    print(f"PROCESSANDO E EXPORTANDO: {model_name}")
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
        
        print(f"Processamento concluido: {stats.get('processed', 0)} comentarios processados")
        
        # Exportar para CSV
        safe_model_name = model_name.replace('/', '_').replace(':', '_')
        output_path = os.path.join(output_dir, f"model_data_{safe_model_name}.csv")
        
        df = export_model_data_to_csv(graph, model_name, output_path)
        
        return output_path
        
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


def main():
    parser = argparse.ArgumentParser(
        description="Exporta dados de cada modelo em CSV separado"
    )
    parser.add_argument("--input", default="sentiment_results.csv",
                      help="CSV com comentarios para processar")
    parser.add_argument("--models", nargs='+', 
                      default=['gpt-4o-mini', 'gpt-4o-2024-08-06', 'gpt-oss-20b', 'gpt-5.2-2025-12-11'],
                      help="Lista de modelos para processar")
    parser.add_argument("--limit", type=int, default=20,
                      help="Limite de comentarios para processar (padrao: 20)")
    parser.add_argument("--batch-size", type=int, default=5,
                      help="Tamanho do lote (padrao: 5)")
    parser.add_argument("--output-dir", default="reports",
                      help="Diretorio para salvar CSVs (padrao: reports)")
    
    args = parser.parse_args()
    
    # Verificar se CSV existe
    csv_path = args.input
    if not os.path.exists(csv_path):
        csv_path = os.path.join(scripts_dir, '..', csv_path)
        if not os.path.exists(csv_path):
            print(f"ERRO: Arquivo CSV nao encontrado: {args.input}")
            return
    
    print("=" * 80)
    print("EXPORTACAO DE DADOS POR MODELO")
    print("=" * 80)
    print(f"CSV de entrada: {csv_path}")
    print(f"Modelos para processar: {', '.join(args.models)}")
    print(f"Limite de comentarios: {args.limit}")
    print(f"Diretorio de saida: {args.output_dir}")
    print("")
    
    csv_files = []
    
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
        
        # Processar e exportar cada modelo
        for model in args.models:
            csv_file = process_and_export_model(
                csv_path, model, graph, 
                args.limit, args.batch_size, args.output_dir
            )
            if csv_file:
                csv_files.append(csv_file)
        
        print("\n" + "=" * 80)
        print("EXPORTACAO CONCLUIDA")
        print("=" * 80)
        print(f"Total de CSVs gerados: {len(csv_files)}")
        print("\nArquivos gerados:")
        for csv_file in csv_files:
            print(f"  - {csv_file}")


if __name__ == "__main__":
    main()
