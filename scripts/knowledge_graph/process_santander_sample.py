"""
Script para processar 100 comentários negativos mais recentes do Santander
"""

import sys
import os
import pandas as pd
from datetime import datetime

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.graph_manager import GraphManager
from knowledge_graph.process_reviews_to_graph import process_csv_to_graph, process_review_to_graph
from knowledge_graph.entity_extraction import EntityExtractor
from knowledge_graph.create_capabilities import get_capability_by_category
from functional_correlation import CATEGORIES


def filter_santander_negative_reviews(csv_path: str, limit: int = 100):
    """
    Filtra comentários negativos do Santander, ordenados por data (mais recentes primeiro).
    
    Args:
        csv_path: Caminho para CSV
        limit: Número de comentários para retornar
        
    Returns:
        DataFrame filtrado
    """
    # Detectar separador
    with open(csv_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        separator = ';' if ';' in first_line else ','
    
    print(f"Carregando CSV: {csv_path}")
    df = pd.read_csv(csv_path, sep=separator, encoding='utf-8')
    print(f"Total de linhas no CSV: {len(df)}")
    
    # Filtrar por app_name = Santander
    df_santander = df[df['app_name'] == 'Santander'].copy()
    print(f"Comentários do Santander: {len(df_santander)}")
    
    # Filtrar por sentiment_label = negative
    df_negative = df_santander[df_santander['sentiment_label'] == 'negative'].copy()
    print(f"Comentários negativos do Santander: {len(df_negative)}")
    
    # Converter data para datetime e ordenar (mais recentes primeiro)
    if 'date' in df_negative.columns:
        df_negative['date'] = pd.to_datetime(df_negative['date'], errors='coerce')
        df_negative = df_negative.dropna(subset=['date'])
        df_negative = df_negative.sort_values('date', ascending=False)
        print(f"Ordenado por data (mais recentes primeiro)")
    
    # Limitar a N comentários
    if len(df_negative) > limit:
        df_negative = df_negative.head(limit)
        print(f"Limitado a {limit} comentários mais recentes")
    else:
        print(f"Processando todos os {len(df_negative)} comentários disponíveis")
    
    # Mostrar período coberto
    if 'date' in df_negative.columns and len(df_negative) > 0:
        min_date = df_negative['date'].min()
        max_date = df_negative['date'].max()
        print(f"Período: {min_date.strftime('%Y-%m-%d')} até {max_date.strftime('%Y-%m-%d')}")
    
    return df_negative


def process_santander_sample(csv_path: str, limit: int = 100, batch_size: int = 10):
    """
    Processa 100 comentários negativos mais recentes do Santander no grafo.
    
    Args:
        csv_path: Caminho para CSV
        limit: Número de comentários para processar
        batch_size: Tamanho do lote para processamento
    """
    print("=" * 60)
    print("PROCESSAMENTO: 100 Comentários Negativos do Santander")
    print("=" * 60)
    
    # Filtrar comentários
    df_filtered = filter_santander_negative_reviews(csv_path, limit)
    
    if len(df_filtered) == 0:
        print("ERRO: Nenhum comentário encontrado com os filtros aplicados!")
        return
    
    # Salvar CSV temporário com dados filtrados
    temp_csv = "santander_sample_100.csv"
    df_filtered.to_csv(temp_csv, index=False, sep=';', encoding='utf-8')
    print(f"\nCSV temporário criado: {temp_csv}")
    
    # Processar no grafo
    with GraphManager() as graph:
        graph.initialize_indices()
        
        # Carregar mapeamento categoria -> capability_id
        category_to_capability_id = {}
        for category in CATEGORIES:
            cap_id = get_capability_by_category(category, graph)
            if cap_id:
                category_to_capability_id[category] = cap_id
        
        if not category_to_capability_id:
            print("ERRO: Nenhuma BusinessCapability encontrada. Execute init_graph.py primeiro!")
            return
        
        print(f"\n{len(category_to_capability_id)} BusinessCapability mapeadas")
        
        extractor = EntityExtractor()
        
        stats = {
            'total_reviews': len(df_filtered),
            'processed': 0,
            'errors': 0,
            'entities_created': 0,
            'relationships_created': 0
        }
        
        print(f"\nProcessando {len(df_filtered)} avaliações no grafo...")
        
        for idx, row in df_filtered.iterrows():
            try:
                review = {
                    'reviewId': str(row.get('reviewId', f'santander_{idx}')),
                    'content': str(row.get('content', '')),
                    'app_name': str(row.get('app_name', 'Santander')),
                    'date': str(row.get('date', '')),
                    'version': str(row.get('version', 'N/A')),
                    'sentiment_label': 'negative'
                }
                
                # Adicionar categorias se existirem no CSV
                for cat in CATEGORIES:
                    col_name = cat.lower().replace('/', '_')
                    if col_name in row:
                        review[cat] = bool(row[col_name])
                
                process_review_to_graph(review, graph, extractor, category_to_capability_id)
                stats['processed'] += 1
                
                if (stats['processed']) % batch_size == 0:
                    print(f"  Processadas {stats['processed']}/{len(df_filtered)} avaliações...")
            
            except Exception as e:
                print(f"  Erro ao processar avaliação {idx}: {e}")
                stats['errors'] += 1
        
        print(f"\n{'=' * 60}")
        print("PROCESSAMENTO CONCLUÍDO")
        print(f"{'=' * 60}")
        print(f"Avaliações processadas: {stats['processed']}")
        print(f"Erros: {stats['errors']}")
        
        # Estatísticas do grafo
        query_stats = """
        MATCH (ep:Episode)
        OPTIONAL MATCH (e) WHERE 'Issue' IN labels(e) OR 'App' IN labels(e) OR 'Version' IN labels(e)
        MATCH (bc:BusinessCapability)
        OPTIONAL MATCH ()-[r:RELATES_TO_CAPABILITY]->()
        RETURN 
            count(DISTINCT ep) as episodes,
            count(DISTINCT e) as entities,
            count(DISTINCT bc) as capabilities,
            count(r) as relationships
        """
        result = graph.execute_query(query_stats)
        if result:
            print(f"\nEstatísticas do Grafo:")
            print(f"  Episódios: {result[0]['episodes']}")
            print(f"  Entidades: {result[0]['entities']}")
            print(f"  BusinessCapability: {result[0]['capabilities']}")
            print(f"  Relacionamentos: {result[0]['relationships']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Processa 100 comentários negativos mais recentes do Santander")
    parser.add_argument("--input", default="functional_correlation_results.csv", 
                       help="CSV com avaliações (padrão: functional_correlation_results.csv)")
    parser.add_argument("--limit", type=int, default=100, 
                       help="Número de comentários para processar (padrão: 100)")
    parser.add_argument("--batch-size", type=int, default=10, 
                       help="Tamanho do lote (padrão: 10)")
    
    args = parser.parse_args()
    
    process_santander_sample(args.input, args.limit, args.batch_size)
