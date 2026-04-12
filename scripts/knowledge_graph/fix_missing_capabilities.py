"""
Script para linkar issues sem BusinessCapability
"""

import sys
import os
scripts_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, scripts_dir)

from knowledge_graph.graph_manager import GraphManager
from knowledge_graph.process_reviews_to_graph import map_entity_to_capability
from knowledge_graph.create_capabilities import get_capability_by_category
from functional_correlation import CATEGORIES


def fix_missing_capabilities():
    """Linka issues sem BusinessCapability"""
    
    with GraphManager() as graph:
        # Buscar issues sem BusinessCapability
        query = """
        MATCH (issue:Issue)
        WHERE NOT (issue)-[:RELATES_TO_CAPABILITY]->()
        RETURN issue.uuid as uuid, issue.name as name, labels(issue) as labels
        """
        
        issues = graph.execute_query(query)
        
        if not issues:
            print("Nenhuma issue sem BusinessCapability encontrada!")
            return
        
        print(f"Encontradas {len(issues)} issues sem BusinessCapability")
        
        # Carregar mapeamento categoria -> capability_id
        category_to_capability_id = {}
        for category in CATEGORIES:
            cap_id = get_capability_by_category(category, graph)
            if cap_id:
                category_to_capability_id[category] = cap_id
        
        linked_count = 0
        
        for issue in issues:
            issue_uuid = issue['uuid']
            issue_name = issue['name']
            issue_labels = issue['labels']
            
            # Mapear para categoria
            category = map_entity_to_capability(issue_name, issue_labels, [])
            
            # Se não encontrou, usar fallback baseado em labels
            if not category:
                if 'Issue' in issue_labels:
                    # Issues genéricas -> Performance
                    category = 'Performance'
                else:
                    category = 'Outros'
            
            if category and category in category_to_capability_id:
                capability_id = category_to_capability_id[category]
                
                fact = f"Issue '{issue_name}' relacionada à capacidade '{category}'"
                
                graph.link_entity_to_capability(
                    entity_id=issue_uuid,
                    capability_id=capability_id,
                    fact=fact,
                    sentiment='negative',
                    t_valid=None,
                    t_invalid=None
                )
                
                print(f"  Linkado: {issue_name} -> {category}")
                linked_count += 1
            else:
                print(f"  [AVISO] Nao encontrou categoria para: {issue_name}")
        
        print(f"\nTotal linkado: {linked_count}/{len(issues)}")


if __name__ == "__main__":
    fix_missing_capabilities()
