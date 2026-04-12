"""
Script para processar comentários negativos do sentiment_results.csv no grafo
"""

import sys
import os
import pandas as pd
from typing import Optional

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.graph_manager import GraphManager
from knowledge_graph.process_reviews_to_graph import process_csv_to_graph
from knowledge_graph.create_capabilities import get_capability_by_category
from knowledge_graph.filter_generic_comments import filter_generic_comments

try:
    from functional_correlation import CATEGORIES
except ImportError:
    CATEGORIES = [
        "PIX", "Login/Autenticação", "Performance", "Interface/Usabilidade",
        "Empréstimos/Crédito", "Pagamentos/Boletos", "Saldo/Extrato",
        "Atendimento", "Cadastro/Conta", "Investimentos", "Segurança",
        "Notificações", "Questões geográficas",
        "Tarifas/Cobranças", "Outros"
    ]


def filter_negative_reviews(csv_path: str):
    """
    Filtra apenas comentários negativos do CSV.
    
    Args:
        csv_path: Caminho para sentiment_results.csv
        
    Returns:
        DataFrame filtrado apenas com comentários negativos
    """
    # Detectar separador
    with open(csv_path, 'r', encoding='utf-8') as f:
        first_line = f.readline()
        separator = ';' if ';' in first_line else ','
    
    print(f"Carregando CSV: {csv_path}")
    df = pd.read_csv(csv_path, sep=separator, encoding='utf-8')
    print(f"Total de linhas no CSV: {len(df)}")
    
    # Filtrar apenas comentários negativos
    if 'sentiment_label' not in df.columns:
        print("ERRO: Coluna 'sentiment_label' não encontrada no CSV!")
        return None
    
    df_negative = df[df['sentiment_label'] == 'negative'].copy()
    print(f"Comentários negativos: {len(df_negative)}")
    
    # Filtrar comentários genéricos (triagem antes do processamento)
    print("\nAplicando triagem para remover comentários genéricos...")
    df_filtered, filter_stats = filter_generic_comments(df_negative, content_column='content')
    
    print(f"  Total de comentários negativos: {filter_stats['total']}")
    print(f"  Comentários genéricos filtrados: {filter_stats['filtered']} ({filter_stats['filter_percentage']:.1f}%)")
    print(f"  Comentários válidos para processar: {filter_stats['remaining']}")
    
    # Garantir que temos as colunas necessárias
    required_columns = ['content', 'app_name', 'date', 'version', 'sentiment_label']
    missing_columns = [col for col in required_columns if col not in df_filtered.columns]
    
    if missing_columns:
        print(f"AVISO: Colunas faltando: {missing_columns}")
    
    return df_filtered


def process_negative_to_graph(
    csv_path: str,
    limit: Optional[int] = None,
    offset: int = 0,
    batch_size: int = 10,
    keep_temp: bool = False,
    ingestion_run: Optional[str] = None,
):
    """
    Processa comentários negativos do CSV no grafo.
    
    Args:
        csv_path: Caminho para sentiment_results.csv
        limit: Limite de comentários para processar (None = todos)
        offset: Índice inicial para começar o processamento (padrão: 0)
        batch_size: Tamanho do lote para processamento
        keep_temp: Se True, mantém o arquivo temporário após processamento
        ingestion_run: Tag gravada em Episode.ingestion_run (ex.: v2); None = legado
    """
    print("=" * 60)
    print("PROCESSAMENTO: Comentários Negativos no Knowledge Graph")
    print("=" * 60)
    
    # Filtrar comentários negativos
    df_negative = filter_negative_reviews(csv_path)
    
    if df_negative is None or len(df_negative) == 0:
        print("ERRO: Nenhum comentário negativo encontrado!")
        return
    
    # Aplicar offset e limite
    total_available = len(df_negative)
    
    if offset > 0:
        if offset >= total_available:
            print(f"ERRO: Offset {offset} maior que total disponível ({total_available})!")
            return
        df_negative = df_negative.iloc[offset:].copy()
        print(f"Começando do índice {offset} (restam {len(df_negative)} comentários)")
    
    if limit and len(df_negative) > limit:
        df_negative = df_negative.head(limit)
        print(f"Limitado a {limit} comentários")
    
    if len(df_negative) == 0:
        print("Nenhum comentário para processar!")
        return
    
    # Salvar CSV temporário com dados filtrados (nome único por rodada evita colisão)
    safe_tag = ingestion_run.replace("/", "_") if ingestion_run else "untagged"
    temp_csv = f"negative_reviews_temp_{safe_tag}.csv"
    df_negative.to_csv(temp_csv, index=False, sep=';', encoding='utf-8')
    print(f"\nCSV temporário criado: {temp_csv} ({len(df_negative)} comentários)")
    
    # Processar no grafo
    with GraphManager() as graph:
        graph.initialize_indices()
        
        # Verificar se BusinessCapabilities existem, caso contrário inicializar
        check_capabilities_query = "MATCH (bc:BusinessCapability) RETURN count(bc) as count"
        result = graph.execute_query(check_capabilities_query)
        capabilities_count = result[0]['count'] if result else 0
        
        if capabilities_count == 0:
            print("\nBusinessCapabilities não encontradas. Inicializando...")
            from knowledge_graph.create_capabilities import create_capabilities_from_categories
            create_capabilities_from_categories(graph)
            print("BusinessCapabilities criadas com sucesso!")
        
        print("\nProcessando no grafo...")
        stats = process_csv_to_graph(
            temp_csv,
            graph,
            limit=None,
            batch_size=batch_size,
            ingestion_run=ingestion_run,
        )
        
        print(f"\n{'=' * 60}")
        print("PROCESSAMENTO CONCLUÍDO")
        print(f"{'=' * 60}")
        
        if stats:
            print(f"Avaliações processadas: {stats.get('processed', 0)}")
            print(f"Erros: {stats.get('errors', 0)}")
        else:
            print("Nenhuma avaliação processada (erro na inicialização)")
        
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
        
        # Limpar arquivo temporário (a menos que keep_temp seja True)
        if not keep_temp and os.path.exists(temp_csv):
            os.remove(temp_csv)
            print(f"\nArquivo temporário removido: {temp_csv}")
        elif keep_temp:
            print(f"\nArquivo temporário mantido: {temp_csv} (use --keep-temp para manter)")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Processa comentários negativos no Knowledge Graph")
    parser.add_argument("--input", default="sentiment_results.csv", 
                       help="CSV com resultados de sentimentos (padrão: sentiment_results.csv)")
    parser.add_argument("--limit", type=int, default=None, 
                       help="Limite de comentários para processar (padrão: todos)")
    parser.add_argument("--offset", type=int, default=0, 
                       help="Índice inicial para começar processamento (padrão: 0)")
    parser.add_argument("--batch-size", type=int, default=10, 
                       help="Tamanho do lote (padrão: 10)")
    parser.add_argument("--keep-temp", action="store_true",
                       help="Mantém arquivo temporário após processamento")
    parser.add_argument(
        "--ingestion-run",
        default=None,
        metavar="TAG",
        help="Tag da rodada (ex.: v2) em Episode.ingestion_run para filtrar SNA depois",
    )
    
    args = parser.parse_args()
    
    process_negative_to_graph(
        args.input,
        args.limit,
        args.offset,
        args.batch_size,
        args.keep_temp,
        ingestion_run=args.ingestion_run,
    )
