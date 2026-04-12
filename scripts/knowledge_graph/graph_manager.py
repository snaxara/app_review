"""
Gerenciador de Grafo Neo4j - Pipeline de Knowledge Graph Temporal
Gerencia conexão e operações básicas no Neo4j
Implementação própria inspirada em metodologia de knowledge graph temporal
"""

from neo4j import GraphDatabase
from typing import Dict, List, Optional, Any
import os
from datetime import datetime

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class GraphManager:
    """Gerenciador de conexão e operações no Neo4j"""
    
    def __init__(self, uri: Optional[str] = None, user: Optional[str] = None, 
                 password: Optional[str] = None):
        """
        Inicializa conexão com Neo4j.
        
        Args:
            uri: URI do Neo4j (padrão: bolt://localhost:7687)
            user: Usuário (padrão: neo4j)
            password: Senha (padrão: do .env)
        """
        self.uri = uri or os.getenv('NEO4J_URI', 'bolt://localhost:7687')
        self.user = user or os.getenv('NEO4J_USER', 'neo4j')
        self.password = password or os.getenv('NEO4J_PASSWORD', '')
        
        if not self.password:
            raise ValueError(
                "Senha do Neo4j não fornecida.\n"
                "Configure de uma das formas:\n"
                "  1. Arquivo .env na raiz: NEO4J_PASSWORD=sua_senha\n"
                "  2. Argumento: --password sua_senha\n"
                "  3. Variável de ambiente: set NEO4J_PASSWORD=sua_senha"
            )
        
        self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))
    
    def close(self):
        """Fecha conexão com Neo4j"""
        if self.driver:
            self.driver.close()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def execute_query(self, query: str, parameters: Optional[Dict] = None) -> List[Dict]:
        """
        Executa uma query Cypher e retorna resultados.
        
        Args:
            query: Query Cypher
            parameters: Parâmetros da query
            
        Returns:
            Lista de resultados
        """
        with self.driver.session() as session:
            result = session.run(query, parameters or {})
            return [record.data() for record in result]
    
    def get_or_create_app_entity(self, app_name: str) -> str:
        """
        Busca ou cria entidade única do aplicativo.
        
        Args:
            app_name: Nome do aplicativo (ex: Santander)
            
        Returns:
            UUID da entidade do app
        """
        query = """
        MATCH (app:App {name: $app_name})
        RETURN app.uuid as uuid
        LIMIT 1
        """
        
        result = self.execute_query(query, {'app_name': app_name})
        
        if result:
            return result[0]['uuid']
        
        # Criar se não existir
        import uuid as uuid_lib
        app_id = str(uuid_lib.uuid4())
        
        query_create = """
        CREATE (app:App:SemanticSubgraph {
            uuid: $uuid,
            name: $name,
            summary: $summary,
            created_at: $created_at,
            updated_at: $updated_at
        })
        RETURN app.uuid as uuid
        """
        
        self.execute_query(query_create, {
            'uuid': app_id,
            'name': app_name,
            'summary': f'Aplicativo {app_name}',
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        return app_id
    
    def get_or_create_version_entity(self, version: str, app_name: str) -> str:
        """
        Busca ou cria entidade de versão do app.
        
        Args:
            version: Versão do app (ex: 25.9.1.3)
            app_name: Nome do app para contexto
            
        Returns:
            UUID da entidade de versão
        """
        if not version or version == 'N/A':
            return None
        
        query = """
        MATCH (v:Version {name: $version})
        RETURN v.uuid as uuid
        LIMIT 1
        """
        
        result = self.execute_query(query, {'version': version})
        
        if result:
            return result[0]['uuid']
        
        # Criar se não existir
        import uuid as uuid_lib
        version_id = str(uuid_lib.uuid4())
        
        query_create = """
        CREATE (v:Version:SemanticSubgraph {
            uuid: $uuid,
            name: $name,
            summary: $summary,
            app_name: $app_name,
            created_at: $created_at,
            updated_at: $updated_at
        })
        RETURN v.uuid as uuid
        """
        
        self.execute_query(query_create, {
            'uuid': version_id,
            'name': version,
            'summary': f'Versão {version} do aplicativo {app_name}',
            'app_name': app_name,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        return version_id
    
    def link_version_to_app(self, version_id: str, app_id: str) -> bool:
        """
        Cria relacionamento versão -> app.
        
        Args:
            version_id: UUID da versão
            app_id: UUID do app
            
        Returns:
            True se criado com sucesso
        """
        query = """
        MATCH (v {uuid: $version_id})
        MATCH (app {uuid: $app_id})
        MERGE (v)-[r:BELONGS_TO]->(app)
        SET r.t_created = $t_created
        RETURN r
        """
        
        result = self.execute_query(query, {
            'version_id': version_id,
            'app_id': app_id,
            't_created': datetime.now().isoformat()
        })
        
        return len(result) > 0
    
    def link_episode_to_version(self, episode_id: str, version_id: str) -> bool:
        """
        Cria relacionamento episódio -> versão.
        
        Args:
            episode_id: ID do episódio
            version_id: UUID da versão
            
        Returns:
            True se criado com sucesso
        """
        query = """
        MATCH (ep:Episode {id: $episode_id})
        MATCH (v {uuid: $version_id})
        MERGE (ep)-[r:HAS_VERSION]->(v)
        SET r.t_created = $t_created
        RETURN r
        """
        
        result = self.execute_query(query, {
            'episode_id': episode_id,
            'version_id': version_id,
            't_created': datetime.now().isoformat()
        })
        
        return len(result) > 0
    
    def link_issue_to_version(self, issue_id: str, version_id: str) -> bool:
        """
        Cria relacionamento issue -> versão com contagem para visualização.
        Incrementa contador a cada nova ocorrência.
        
        Args:
            issue_id: UUID da entidade issue (problema)
            version_id: UUID da versão
            
        Returns:
            True se criado/atualizado com sucesso
        """
        query = """
        MATCH (issue {uuid: $issue_id})
        MATCH (v {uuid: $version_id})
        MERGE (issue)-[r:RELATED_TO_VERSION]->(v)
        ON CREATE SET r.count = 1, r.t_created = $t_created
        ON MATCH SET r.count = r.count + 1, r.updated_at = $t_created
        RETURN r.count as count
        """
        
        result = self.execute_query(query, {
            'issue_id': issue_id,
            'version_id': version_id,
            't_created': datetime.now().isoformat()
        })
        
        return len(result) > 0
    
    def get_or_create_entity_by_name(self, name: str, labels: List[str], 
                                    summary: str, properties: Optional[Dict] = None) -> str:
        """
        Busca ou cria entidade por nome (para agrupar entidades similares).
        
        Args:
            name: Nome da entidade
            labels: Lista de labels
            summary: Resumo (será atualizado se entidade existir)
            properties: Propriedades adicionais
            
        Returns:
            UUID da entidade (existente ou criada)
        """
        # Buscar por nome exato (buscar em qualquer label que tenha o nome)
        # Tenta primeiro com label específico, depois genérico
        main_label = labels[0] if labels else 'Entity'
        
        # Tentar buscar com label específico primeiro
        query_search = f"""
        MATCH (e:{main_label} {{name: $name}})
        RETURN e.uuid as uuid
        LIMIT 1
        """
        
        result = self.execute_query(query_search, {'name': name})
        
        # Se não encontrou, buscar em qualquer Entity
        if not result:
            query_search_generic = """
            MATCH (e {name: $name})
            WHERE 'Entity' IN labels(e) OR 'Issue' IN labels(e)
            RETURN e.uuid as uuid, labels(e) as existing_labels
            LIMIT 1
            """
            result = self.execute_query(query_search_generic, {'name': name})
        
        if result:
            # Atualizar summary e labels se necessário
            uuid_existing = result[0]['uuid']
            existing_labels = result[0].get('existing_labels', [])
            
            # Atualizar labels para incluir SemanticSubgraph se não tiver
            # No Neo4j, SET adiciona labels, não substitui
            query_update = f"""
            MATCH (e {{uuid: $uuid}})
            SET e:SemanticSubgraph
            SET e.summary = $summary,
                e.updated_at = $updated_at
            """
            self.execute_query(query_update, {
                'uuid': uuid_existing,
                'summary': summary,
                'updated_at': datetime.now().isoformat()
            })
            return uuid_existing
        
        # Criar nova entidade
        import uuid as uuid_lib
        entity_id = str(uuid_lib.uuid4())
        self.create_entity(entity_id, name, labels, summary, properties)
        return entity_id
    
    def create_entity(self, entity_id: str, name: str, labels: List[str], 
                     summary: str, properties: Optional[Dict] = None) -> bool:
        """
        Cria ou atualiza uma entidade no Semantic Subgraph (Gₛ).
        Entidades são nós conectados por fatos (edges) no grafo semântico.
        
        Args:
            entity_id: UUID da entidade
            name: Nome da entidade
            labels: Lista de labels (tipos: Issue, App, etc.)
            summary: Resumo da entidade
            properties: Propriedades adicionais
            
        Returns:
            True se criado com sucesso
        """
        props = properties or {}
        props.update({
            'name': name,
            'summary': summary,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        # Usar apenas o primeiro label principal + SemanticSubgraph
        # Evitar múltiplos labels confusos (seguindo padrão de knowledge graph)
        main_label = labels[0] if labels else 'Entity'
        
        # Criar nó com label principal + SemanticSubgraph
        # No Neo4j, precisamos criar com os labels corretos desde o início
        query = f"""
        MERGE (e:{main_label}:SemanticSubgraph {{uuid: $entity_id}})
        SET e += $properties
        RETURN e
        """
        
        result = self.execute_query(query, {
            'entity_id': entity_id,
            'properties': props
        })
        
        return len(result) > 0
    
    def create_business_capability(self, capability_id: str, name: str, description: str,
                                  level: int, capability_type: str, maturity: str,
                                  business_value: str, parent_id: Optional[str] = None) -> bool:
        """
        Cria ou atualiza uma BusinessCapability no grafo.
        
        Args:
            capability_id: ID da capacidade
            name: Nome da capacidade
            description: Descrição
            level: Nível hierárquico (1-3)
            capability_type: Tipo (Core, Supporting, Strategic)
            maturity: Maturidade (Initial, Managed, Defined, Optimized)
            business_value: Valor (High, Medium, Low)
            parent_id: ID da capacidade pai (opcional)
            
        Returns:
            True se criado com sucesso
        """
        query = """
        MERGE (bc:BusinessCapability {id: $capability_id})
        SET bc.name = $name,
            bc.description = $description,
            bc.level = $level,
            bc.capability_type = $capability_type,
            bc.maturity = $maturity,
            bc.business_value = $business_value,
            bc.created_at = $created_at,
            bc.updated_at = $updated_at
        """
        
        if parent_id:
            query += """
            WITH bc
            MATCH (parent:BusinessCapability {id: $parent_id})
            MERGE (bc)-[:CHILD_OF]->(parent)
            """
        
        query += " RETURN bc"
        
        result = self.execute_query(query, {
            'capability_id': capability_id,
            'name': name,
            'description': description,
            'level': level,
            'capability_type': capability_type,
            'maturity': maturity,
            'business_value': business_value,
            'parent_id': parent_id,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        })
        
        return len(result) > 0
    
    def create_relationship(self, source_id: str, target_id: str, 
                           relation_type: str, fact: str,
                           t_valid: Optional[str] = None,
                           t_invalid: Optional[str] = None,
                           t_created: Optional[str] = None,
                           t_expired: Optional[str] = None) -> bool:
        """
        Cria um relacionamento (edge) bi-temporal entre duas entidades.
        Segue modelo bi-temporal com 4 timestamps:
        - t_valid: Quando o fato era verdade no mundo real (Timeline T - Cronológica)
        - t_invalid: Quando o fato deixou de ser verdade (Timeline T - Cronológica)
        - t_created: Quando inserimos no grafo (Timeline T' - Transacional)
        - t_expired: Quando marcamos como inválido (Timeline T' - Transacional)
        
        Args:
            source_id: UUID da entidade origem
            target_id: UUID da entidade destino
            relation_type: Tipo do relacionamento (ex: RELATES_TO, IMPACTS)
            fact: Descrição textual do fato
            t_valid: Data de início da validade (ISO format, padrão: agora)
            t_invalid: Data de fim da validade (ISO format, None = ainda válido)
            t_created: Quando foi criado no sistema (ISO format, padrão: agora)
            t_expired: Quando foi invalidado (ISO format, None = não invalidado)
            
        Returns:
            True se criado com sucesso
        """
        now = datetime.now().isoformat()
        
        query = f"""
        MATCH (source {{uuid: $source_id}})
        MATCH (target {{uuid: $target_id}})
        MERGE (source)-[r:{relation_type}]->(target)
        SET r.fact = $fact,
            r.t_valid = $t_valid,
            r.t_invalid = $t_invalid,
            r.t_created = $t_created,
            r.t_expired = $t_expired
        RETURN r
        """
        
        result = self.execute_query(query, {
            'source_id': source_id,
            'target_id': target_id,
            'fact': fact,
            't_valid': t_valid or now,
            't_invalid': t_invalid,
            't_created': t_created or now,
            't_expired': t_expired
        })
        
        return len(result) > 0
    
    def link_entity_to_capability(self, entity_id: str, capability_id: str,
                                 fact: str, sentiment: str = "negative",
                                 t_valid: Optional[str] = None,
                                 t_invalid: Optional[str] = None) -> bool:
        """
        Cria relacionamento bi-temporal entre uma entidade extraída e uma BusinessCapability.
        Usa modelo bi-temporal para rastreamento temporal de fatos.
        
        Args:
            entity_id: UUID da entidade
            capability_id: ID da BusinessCapability
            fact: Descrição do relacionamento
            sentiment: Sentimento associado (negative, positive, neutral)
            t_valid: Quando o relacionamento era válido (padrão: agora)
            t_invalid: Quando deixou de ser válido (None = ainda válido)
            
        Returns:
            True se criado com sucesso
        """
        now = datetime.now().isoformat()
        
        query = """
        MATCH (e {uuid: $entity_id})
        MATCH (bc:BusinessCapability {id: $capability_id})
        MERGE (e)-[r:RELATES_TO_CAPABILITY]->(bc)
        SET r.fact = $fact,
            r.sentiment = $sentiment,
            r.t_valid = $t_valid,
            r.t_invalid = $t_invalid,
            r.t_created = $t_created,
            r.t_expired = NULL
        RETURN r
        """
        
        result = self.execute_query(query, {
            'entity_id': entity_id,
            'capability_id': capability_id,
            'fact': fact,
            'sentiment': sentiment,
            't_valid': t_valid or now,
            't_invalid': t_invalid,
            't_created': now
        })
        
        return len(result) > 0
    
    def create_episode(
        self,
        episode_id: str,
        content: str,
        app_name: str,
        review_date: str,
        review_version: str,
        ingestion_run: Optional[str] = None,
    ) -> bool:
        """
        Cria um nó episódico (Episodic Subgraph - Gₑ) preservando conteúdo original.
        Episódios funcionam como "memória episódica" - preservam o contexto completo
        de onde a informação veio, útil para auditoria e debugging.
        
        IMPORTANTE: Cada episódio é único. Se já existir um episódio com o mesmo ID,
        não atualiza, apenas retorna False (evita sobrescrever conteúdo).
        
        Args:
            episode_id: ID único do episódio
            content: Conteúdo completo do comentário (preservado bruto)
            app_name: Nome do app
            review_date: Data da avaliação
            review_version: Versão do app
            
        Returns:
            True se criado com sucesso, False se já existe
        """
        # Verificar se já existe
        check_query = """
        MATCH (ep:Episode {id: $episode_id})
        RETURN ep.id as id
        LIMIT 1
        """
        
        existing = self.execute_query(check_query, {'episode_id': episode_id})
        
        if existing:
            # Episódio já existe, não atualizar (preservar conteúdo original)
            return False
        
        # Criar novo episódio (ingestion_run identifica a rodada de carga: ex. v1, v2)
        query = """
        CREATE (ep:Episode:EpisodicSubgraph {
            id: $episode_id,
            content: $content,
            app_name: $app_name,
            review_date: $review_date,
            review_version: $review_version,
            t_created: $t_created,
            ingestion_run: $ingestion_run
        })
        RETURN ep
        """
        
        result = self.execute_query(query, {
            'episode_id': episode_id,
            'content': content,
            'app_name': app_name,
            'review_date': review_date,
            'review_version': review_version,
            't_created': datetime.now().isoformat(),
            'ingestion_run': ingestion_run,
        })
        
        return len(result) > 0
    
    def link_episode_to_entity(self, episode_id: str, entity_id: str) -> bool:
        """
        Cria relacionamento entre episódio e entidade extraída.
        
        Args:
            episode_id: ID do episódio
            entity_id: UUID da entidade
            
        Returns:
            True se criado com sucesso
        """
        query = """
        MATCH (ep:Episode {id: $episode_id})
        MATCH (e {uuid: $entity_id})
        MERGE (ep)-[:CONTAINS_ENTITY]->(e)
        RETURN ep, e
        """
        
        result = self.execute_query(query, {
            'episode_id': episode_id,
            'entity_id': entity_id
        })
        
        return len(result) > 0
    
    def get_entities_by_capability(self, capability_id: str) -> List[Dict]:
        """
        Retorna todas as entidades relacionadas a uma BusinessCapability.
        
        Args:
            capability_id: ID da BusinessCapability
            
        Returns:
            Lista de entidades relacionadas
        """
        query = """
        MATCH (e)-[:RELATES_TO_CAPABILITY]->(bc:BusinessCapability {id: $capability_id})
        RETURN e, bc, r
        """
        
        return self.execute_query(query, {'capability_id': capability_id})
    
    def initialize_indices(self):
        """Cria índices para melhorar performance"""
        indices = [
            "CREATE INDEX entity_uuid IF NOT EXISTS FOR (e:Entity) ON (e.uuid)",
            "CREATE INDEX capability_id IF NOT EXISTS FOR (bc:BusinessCapability) ON (bc.id)",
            "CREATE INDEX episode_id IF NOT EXISTS FOR (ep:Episode) ON (ep.id)",
            "CREATE INDEX semantic_subgraph IF NOT EXISTS FOR (e:SemanticSubgraph) ON (e.uuid)",
            "CREATE INDEX episodic_subgraph IF NOT EXISTS FOR (ep:EpisodicSubgraph) ON (ep.id)",
            "CREATE INDEX episode_ingestion_run IF NOT EXISTS FOR (ep:Episode) ON (ep.ingestion_run)",
        ]
        
        for index_query in indices:
            try:
                self.execute_query(index_query)
            except Exception as e:
                print(f"Erro ao criar índice: {e}")


if __name__ == "__main__":
    # Teste de conexão
    try:
        with GraphManager() as gm:
            print("Conexão com Neo4j estabelecida com sucesso!")
            gm.initialize_indices()
            print("Índices criados!")
    except Exception as e:
        print(f"Erro: {e}")
