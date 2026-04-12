"""
Script de inicialização do Knowledge Graph Temporal
Cria estrutura inicial e BusinessCapability
Implementação própria inspirada em metodologia de knowledge graph temporal
"""

import argparse
import sys
import os

# Adicionar caminho para importar módulos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.graph_manager import GraphManager
from knowledge_graph.create_capabilities import create_capabilities_from_categories


def init_graph(reset: bool = False):
    """
    Inicializa o grafo Neo4j com estrutura de Knowledge Graph Temporal.
    
    Args:
        reset: Se True, remove dados existentes antes de criar
    """
    print("Inicializando Knowledge Graph Temporal...")
    
    with GraphManager() as graph:
        # Criar índices
        print("Criando índices...")
        graph.initialize_indices()
        
        if reset:
            print("Removendo dados existentes...")
            graph.execute_query("MATCH (n) DETACH DELETE n")
            print("Dados removidos!")
        
        # Criar BusinessCapability
        print("Criando BusinessCapability...")
        category_to_id = create_capabilities_from_categories(graph)
        print(f"Total de {len(category_to_id)} capacidades criadas!")
        
        print("\nGrafo inicializado com sucesso!")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Inicializa Knowledge Graph Temporal")
    parser.add_argument("--reset", action="store_true", 
                       help="Remove todos os dados existentes antes de inicializar")
    
    args = parser.parse_args()
    
    init_graph(reset=args.reset)
