"""
Script para criar BusinessCapability no grafo Neo4j
Baseado nas categorias funcionais existentes
"""

import sys
import os
from typing import Dict, Optional
import uuid

# Adicionar caminho para importar modelos
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from models.business_capability import CATEGORY_TO_CAPABILITY, BusinessCapability
from knowledge_graph.graph_manager import GraphManager


def create_capabilities_from_categories(graph: GraphManager) -> Dict[str, str]:
    """
    Cria BusinessCapability no grafo baseado nas categorias funcionais.
    
    Args:
        graph: Instância do GraphManager
        
    Returns:
        Dicionário mapeando nome da categoria para ID da capacidade criada
    """
    category_to_capability_id = {}
    
    # Criar capacidades de nível 1 primeiro (sem parent)
    level_1_capabilities = {}
    for category, cap_data in CATEGORY_TO_CAPABILITY.items():
        if cap_data['level'] == 1:
            cap_id = str(uuid.uuid4())
            graph.create_business_capability(
                capability_id=cap_id,
                name=cap_data['name'],
                description=cap_data['description'],
                level=cap_data['level'],
                capability_type=cap_data['capability_type'].value,
                maturity=cap_data['maturity'].value,
                business_value=cap_data['business_value'].value,
                parent_id=None
            )
            level_1_capabilities[category] = cap_id
            category_to_capability_id[category] = cap_id
            print(f"Criada capacidade nível 1: {cap_data['name']} ({cap_id})")
    
    # Criar capacidades de nível 2 (sem parent automático - são independentes)
    level_2_capabilities = {}
    for category, cap_data in CATEGORY_TO_CAPABILITY.items():
        if cap_data['level'] == 2:
            cap_id = str(uuid.uuid4())
            # Capacidades nível 2 são independentes, sem parent automático
            # Se precisar de hierarquia específica, definir manualmente aqui
            parent_id = None
            
            graph.create_business_capability(
                capability_id=cap_id,
                name=cap_data['name'],
                description=cap_data['description'],
                level=cap_data['level'],
                capability_type=cap_data['capability_type'].value,
                maturity=cap_data['maturity'].value,
                business_value=cap_data['business_value'].value,
                parent_id=parent_id
            )
            level_2_capabilities[category] = cap_id
            category_to_capability_id[category] = cap_id
            print(f"Criada capacidade nível 2: {cap_data['name']} ({cap_id})")
    
    # Criar capacidades de nível 3 (sem parent automático - são independentes)
    for category, cap_data in CATEGORY_TO_CAPABILITY.items():
        if cap_data['level'] == 3:
            cap_id = str(uuid.uuid4())
            # Capacidades nível 3 são independentes, sem parent automático
            # Se precisar de hierarquia específica, definir manualmente aqui
            parent_id = None
            
            graph.create_business_capability(
                capability_id=cap_id,
                name=cap_data['name'],
                description=cap_data['description'],
                level=cap_data['level'],
                capability_type=cap_data['capability_type'].value,
                maturity=cap_data['maturity'].value,
                business_value=cap_data['business_value'].value,
                parent_id=parent_id
            )
            category_to_capability_id[category] = cap_id
            print(f"Criada capacidade nível 3: {cap_data['name']} ({cap_id})")
    
    return category_to_capability_id


def get_capability_by_category(category: str, graph: GraphManager) -> Optional[str]:
    """
    Busca o ID da BusinessCapability correspondente a uma categoria.
    
    Args:
        category: Nome da categoria funcional
        graph: Instância do GraphManager
        
    Returns:
        ID da capacidade ou None se não encontrada
    """
    if category not in CATEGORY_TO_CAPABILITY:
        return None
    
    cap_name = CATEGORY_TO_CAPABILITY[category]['name']
    
    query = """
    MATCH (bc:BusinessCapability {name: $name})
    RETURN bc.id as id
    LIMIT 1
    """
    
    result = graph.execute_query(query, {'name': cap_name})
    
    if result:
        return result[0]['id']
    
    return None


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Cria BusinessCapability no grafo Neo4j")
    parser.add_argument("--reset", action="store_true", help="Remove todas as capacidades existentes antes de criar")
    
    args = parser.parse_args()
    
    with GraphManager() as graph:
        if args.reset:
            print("Removendo capacidades existentes...")
            graph.execute_query("MATCH (bc:BusinessCapability) DETACH DELETE bc")
            print("Capacidades removidas!")
        
        print("Criando BusinessCapability...")
        category_to_id = create_capabilities_from_categories(graph)
        print(f"\nTotal de {len(category_to_id)} capacidades criadas!")
