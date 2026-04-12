# Graphiti: Pipeline de Construção de Knowledge Graph

## Guia Técnico Completo

---

# 1. VISÃO GERAL

## 1.1 O Que é Graphiti?

Graphiti é um framework de **knowledge graph temporal** desenvolvido pela Zep para agentes de IA. Diferente de sistemas RAG tradicionais que tratam informação como estática, Graphiti modela conhecimento como **fatos que evoluem no tempo**.

### Problema que Resolve

```
RAG Tradicional:
"João trabalha na Empresa X" → Documento estático

Graphiti:
"João trabalha na Empresa X" 
  → t_valid: 2020-01-15 (quando começou)
  → t_invalid: 2023-06-30 (quando saiu)
  → t_created: 2023-07-01 (quando o sistema soube)
```

### Arquitetura de 3 Subgrafos

```
┌─────────────────────────────────────────────────────────────────┐
│                        GRAPHITI GRAPH                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              COMMUNITY SUBGRAPH (Gᴄ)                      │  │
│  │                                                           │  │
│  │  Clusters de alto nível que agrupam entidades             │  │
│  │  relacionadas. Gerados via Label Propagation.             │  │
│  │                                                           │  │
│  │  Ex: "Preferências Musicais", "Histórico Profissional"    │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              SEMANTIC SUBGRAPH (Gₛ)                       │  │
│  │                                                           │  │
│  │  Entidades (nós) conectadas por Fatos (edges).            │  │
│  │  Cada edge tem metadados bi-temporais.                    │  │
│  │                                                           │  │
│  │  (Preston)──[FAVORITE_BAND]──▶(Pink Floyd)                │  │
│  │       │                            │                      │  │
│  │       └─────[LIVES_IN]────────▶(California)               │  │
│  └───────────────────────────────────────────────────────────┘  │
│                              │                                  │
│                              ▼                                  │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │              EPISODIC SUBGRAPH (Gₑ)                       │  │
│  │                                                           │  │
│  │  Nós episódicos preservam o conteúdo BRUTO original.      │  │
│  │  Funcionam como "memória episódica" - o contexto          │  │
│  │  completo de onde a informação veio.                      │  │
│  │                                                           │  │
│  │  Episode: "User said: I love Pink Floyd, been listening   │  │
│  │            to them since I moved to California"           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**Por que 3 subgrafos?**

1. **Episodic (Gₑ)**: Preserva contexto original. Útil para auditoria, debugging e quando o LLM precisa do texto completo.

2. **Semantic (Gₛ)**: Conhecimento estruturado e navegável. Permite queries como "quais entidades estão conectadas a X?"

3. **Community (Gᴄ)**: Visão de alto nível. Responde "sobre o que esse grafo fala?" sem precisar navegar milhares de nós.

---

# 2. MODELO BI-TEMPORAL

## 2.1 Por Que Bi-Temporal?

O mundo real tem duas dimensões temporais distintas:

1. **Quando algo ACONTECEU** (Timeline Cronológica - T)
2. **Quando SOUBEMOS** que aconteceu (Timeline Transacional - T')

### Exemplo Prático

```
Evento real: Kamala Harris foi Attorney General da Califórnia de 2011 a 2017.

Cenário 1: Sistema aprende em 2015
  - t_valid = 2011-01-03 (quando começou)
  - t_invalid = NULL (ainda é AG em 2015)
  - t_created = 2015-06-01 (quando inserimos)
  - t_expired = NULL

Cenário 2: Sistema aprende em 2024 (retrospectivo)
  - t_valid = 2011-01-03 
  - t_invalid = 2017-01-03 (quando terminou)
  - t_created = 2024-08-01 (quando inserimos)
  - t_expired = NULL
```

## 2.2 Os 4 Timestamps

```python
class BiTemporalEdge:
    """
    Cada edge no grafo semântico tem 4 timestamps.
    """
    
    # TIMELINE T - CRONOLÓGICA
    # "Quando o fato era verdade no mundo real"
    t_valid: datetime      # Início da validade
    t_invalid: datetime    # Fim da validade (null = ainda válido)
    
    # TIMELINE T' - TRANSACIONAL  
    # "Quando o sistema registrou/invalidou o fato"
    t_created: datetime    # Quando inserimos no grafo
    t_expired: datetime    # Quando marcamos como inválido
```

**Por que isso importa?**

```
Query: "Quem era o Attorney General em 2015?"
→ Filtra por: t_valid <= 2015 AND (t_invalid IS NULL OR t_invalid > 2015)
→ Resultado: Kamala Harris

Query: "O que o sistema sabia em Junho de 2023?"
→ Filtra por: t_created <= 2023-06 AND (t_expired IS NULL OR t_expired > 2023-06)
→ Permite "time travel" no conhecimento do sistema
```

---

# 3. O PIPELINE DE INGESTÃO

## 3.1 Visão Geral

O pipeline processa **episódios** (mensagens, eventos, documentos) e atualiza o grafo. Consiste em **7 etapas**, cada uma com seu próprio prompt LLM.

```
┌─────────────┐
│   EPISODE   │  Uma mensagem, documento ou evento
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 1: ENTITY EXTRACTION                                    │
│  ─────────────────────────                                     │
│  Extrai entidades mencionadas no episódio.                     │
│  LLM identifica: pessoas, lugares, conceitos, etc.             │
│  CUSTO: 1-2 chamadas LLM                                       │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 2: ENTITY RESOLUTION                                    │
│  ──────────────────────────                                    │
│  Verifica se entidades extraídas já existem no grafo.          │
│  "John Doe" == "john.doe@email.com"?                           │
│  CUSTO: N chamadas LLM (1 por entidade, paralelo)              │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 3: EDGE EXTRACTION                                      │
│  ─────────────────────────                                     │
│  Extrai relacionamentos entre as entidades resolvidas.         │
│  "João TRABALHA_EM Empresa X"                                  │
│  CUSTO: 1 chamada LLM                                          │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 4: EDGE DEDUPLICATION                                   │
│  ──────────────────────────                                    │
│  Verifica se o edge extraído já existe (mesmo fato,            │
│  redação diferente).                                           │
│  CUSTO: M chamadas LLM (1 por edge, paralelo)                  │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 5: TEMPORAL EXTRACTION                                  │
│  ─────────────────────────────                                 │
│  Extrai informações temporais para popular t_valid/t_invalid.  │
│  "desde 2020", "há duas semanas", "até março"                  │
│  CUSTO: M chamadas LLM (1 por edge, paralelo)                  │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 6: EDGE INVALIDATION                                    │
│  ─────────────────────────                                     │
│  Detecta contradições com edges existentes.                    │
│  Se "João mora em SP" e novo diz "João mora em RJ",            │
│  o antigo é invalidado.                                        │
│  CUSTO: Variável                                               │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────────────────────────────────────────────────────────┐
│  ETAPA 7: COMMUNITY DETECTION                                  │
│  ────────────────────────────                                  │
│  Atualiza comunidades afetadas pelas novas entidades.          │
│  Usa Label Propagation incremental.                            │
│  CUSTO: 1 chamada LLM por comunidade atualizada                │
└─────────────────────────────────────────────────────────────────┘
       │
       ▼
┌─────────────┐
│   GRAPH     │  Atualizado com novos nós e edges
│   UPDATED   │
└─────────────┘
```

**Por que etapas separadas?**

A versão inicial do Graphiti usava um "mega-prompt" que fazia tudo junto:
- 35 guidelines em um único prompt
- Incluía todo o grafo como contexto
- Lento e imprevisível
- Exigia modelos grandes

A separação traz:
1. **Paralelização**: Etapas 2, 4, 5 rodam em paralelo
2. **Testabilidade**: Cada etapa pode ser testada isoladamente
3. **Modelos menores**: gpt-4o-mini funciona bem em tarefas focadas
4. **Contexto mínimo**: Cada etapa recebe apenas o necessário

---

# 4. ETAPA 1: ENTITY EXTRACTION

## 4.1 O Que Faz

Extrai todas as entidades significativas mencionadas no episódio usando **zero-shot NER** (Named Entity Recognition).

## 4.2 Contexto Fornecido

```
┌─────────────────────────────────────────┐
│  CURRENT_EPISODE                        │
│  ─────────────────                      │
│  A mensagem/evento sendo processado     │
├─────────────────────────────────────────┤
│  PREVIOUS_EPISODES (últimos 4)          │
│  ───────────────────────────            │
│  Contexto conversacional recente        │
├─────────────────────────────────────────┤
│  REFERENCE_TIME                         │
│  ──────────────                         │
│  Timestamp do episódio (para datas      │
│  relativas)                             │
└─────────────────────────────────────────┘
```

**Por que NÃO inclui o grafo existente?**

LLMs são naturalmente bons em NER. Incluir o grafo:
- Aumentaria custo de tokens
- Poderia enviesar a extração
- Não melhora qualidade significativamente

## 4.3 Prompt de Entity Extraction

```python
ENTITY_EXTRACTION_SYSTEM = """
You are an AI assistant that extracts entities from conversational text.

<CURRENT_NODES>
Below are the existing node types in the knowledge graph. 
If you extract an entity that fits one of these types, assign that label.
If not, you may create a new label or assign an empty array.

Node types:
- Preference: User preferences, likes, dislikes
- Requirement: Needs, requirements, constraints
- Procedure: Processes, workflows, methods
- Location: Places, addresses, regions
- Event: Occurrences, happenings, occasions
- Organization: Companies, institutions, groups
- Document: Files, reports, articles
- Topic: Subjects, themes, areas of interest
- Object: Physical items, products, tools
</CURRENT_NODES>

<EXTRACTION_GUIDELINES>
1. Extract the SPEAKER first (the person before the colon in "Speaker: message")
2. Extract ALL significant entities explicitly or implicitly mentioned
3. Use the full, unabbreviated name for entities
4. Include entities referenced with pronouns if identifiable from context
5. Create a brief summary (<250 words) for each entity
6. DO NOT extract:
   - Relationships (those come later)
   - Temporal information (handled separately)
   - Actions or verbs
</EXTRACTION_GUIDELINES>
"""

ENTITY_EXTRACTION_USER = """
<PREVIOUS_EPISODES>
{previous_episodes}
</PREVIOUS_EPISODES>

<CURRENT_EPISODE>
{current_episode}
</CURRENT_EPISODE>

<REFERENCE_TIME>
{reference_time}
</REFERENCE_TIME>

Extract all entities from the CURRENT_EPISODE. Use context from PREVIOUS_EPISODES 
if it helps identify entities.

Respond with JSON:
{{
  "extracted_entities": [
    {{
      "name": "Entity Name",
      "labels": ["Preference", "Topic"],
      "summary": "Brief description of the entity and what we know about it"
    }}
  ]
}}
"""
```

## 4.4 Técnica de Reflexão

Após a primeira extração, uma segunda chamada LLM verifica se entidades foram perdidas:

```python
REFLECTION_PROMPT = """
<EXTRACTED_ENTITIES>
{already_extracted}
</EXTRACTED_ENTITIES>

<ORIGINAL_EPISODE>
{episode}
</ORIGINAL_EPISODE>

Review the episode again. Are there any entities that were missed?
Look for:
- Implicit entities (referenced but not named directly)
- Entities mentioned in pronouns
- Background entities assumed but not stated

Return only NEW entities not in EXTRACTED_ENTITIES, or empty array if complete.
"""
```

**Por que reflexão?**

Em benchmarks, a reflexão recupera ~5-10% de entidades perdidas na primeira passada, especialmente entidades implícitas.

## 4.5 Output Esperado

```json
{
  "extracted_entities": [
    {
      "name": "Preston",
      "labels": ["Person"],
      "summary": "The user/speaker in this conversation"
    },
    {
      "name": "Pink Floyd",
      "labels": ["Organization", "Preference"],
      "summary": "British rock band, mentioned as user's favorite band"
    },
    {
      "name": "California",
      "labels": ["Location"],
      "summary": "US state where the user currently lives"
    }
  ]
}
```

---

# 5. ETAPA 2: ENTITY RESOLUTION

## 5.1 O Que Faz

Determina se cada entidade extraída já existe no grafo (deduplicação).

## 5.2 O Problema

```
Grafo existente tem: "John Doe" (uuid: abc123)
Episódio novo menciona: "john.doe@company.com"

São a mesma pessoa? 
→ Sim, devem ter o mesmo UUID
→ Summary deve ser unificado
```

## 5.3 Evolução do Prompt

### Versão Antiga (Problemática)

```python
# ❌ Processava TODAS as entidades juntas
# Saída confusa, difícil de parsear
PROMPT_V1 = """
Here are the extracted entities: {all_entities}
Here are existing entities: {existing_entities}

For each extracted entity, determine if it matches any existing entity.
"""
```

### Versão Atual (1 entidade por vez)

```python
# ✅ Uma chamada LLM por entidade
# Output binário simples: is_duplicate true/false
ENTITY_RESOLUTION_SYSTEM = """
You are an AI that determines if two entities refer to the same real-world thing.

<RESOLUTION_GUIDELINES>
1. Compare BOTH name AND summary/description
2. Entities with different names CAN be the same entity:
   - "NYC" == "New York City"
   - "john@email.com" == "John Smith" (if context confirms)
3. Entities with same name might NOT be the same:
   - "Apple" (fruit) != "Apple" (company)
4. When in doubt, they are DIFFERENT entities
5. If duplicate, provide a merged summary combining all known information
</RESOLUTION_GUIDELINES>
"""

ENTITY_RESOLUTION_USER = """
<EXISTING_ENTITY>
UUID: {existing_uuid}
Name: {existing_name}
Labels: {existing_labels}
Summary: {existing_summary}
</EXISTING_ENTITY>

<NEW_ENTITY>
Name: {new_name}
Labels: {new_labels}
Summary: {new_summary}
</NEW_ENTITY>

Do these refer to the same real-world entity?

Respond with JSON:
{{
  "is_duplicate": true|false,
  "confidence": 0.0-1.0,
  "reasoning": "Brief explanation",
  "merged_summary": "Combined summary if duplicate, null otherwise"
}}
"""
```

## 5.4 Otimização: Entropy-Gated Matching

Nem toda resolução precisa de LLM. O Graphiti v1.0 introduziu uma estratégia híbrida:

```
┌─────────────────────────────────────────────────────────────────┐
│                   ENTITY RESOLUTION FLOW                        │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Normalize     │
                    │   (lowercase,   │
                    │    trim spaces) │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │  Exact Match?   │───── Sim ──▶ DUPLICATA
                    │  (normalized)   │              (sem LLM)
                    └────────┬────────┘
                             │ Não
                             ▼
                    ┌─────────────────┐
                    │ Calculate       │
                    │ Shannon Entropy │
                    └────────┬────────┘
                             │
              ┌──────────────┴──────────────┐
              │                             │
              ▼                             ▼
     Entropy < 2.5              Entropy >= 2.5
     (nome curto/simples)       (nome complexo/único)
              │                             │
              ▼                             ▼
     ┌────────────────┐          ┌─────────────────┐
     │  Direto → LLM  │          │ MinHash + LSH   │
     │  (fuzzy match  │          │ (encontra       │
     │   instável)    │          │  candidatos)    │
     └────────────────┘          └────────┬────────┘
                                          │
                                          ▼
                                 ┌─────────────────┐
                                 │  Candidatos     │
                                 │  encontrados?   │
                                 └────────┬────────┘
                                          │
                           ┌──────────────┴──────────────┐
                           │ Não                         │ Sim
                           ▼                             ▼
                    NOVA ENTIDADE              ┌─────────────────┐
                    (sem LLM)                  │   LLM confirma  │
                                               │   is_duplicate? │
                                               └─────────────────┘
```

### Código da Entropia

```python
import math

def shannon_entropy(text: str) -> float:
    """
    Calcula entropia de Shannon.
    
    Baixa entropia: nomes curtos/repetitivos ("John", "NYC", "API")
    Alta entropia: nomes únicos ("calculateDeploymentRiskScore")
    """
    if not text:
        return 0.0
    
    freq = {}
    for char in text.lower():
        freq[char] = freq.get(char, 0) + 1
    
    length = len(text)
    entropy = 0.0
    for count in freq.values():
        prob = count / length
        entropy -= prob * math.log2(prob)
    
    return entropy

# Exemplos:
shannon_entropy("John")                     # ~2.0 (baixa)
shannon_entropy("NYC")                      # ~1.6 (baixa)
shannon_entropy("calculateDeploymentRisk")  # ~3.8 (alta)
```

### Por que Entropy Gate?

Nomes com **baixa entropia** têm fuzzy matching instável:
- "John" vs "Jon" → Jaccard similarity alta, mas podem ser pessoas diferentes
- Melhor deixar o LLM decidir

Nomes com **alta entropia** são mais únicos:
- "calculateDeploymentRiskScore" é muito específico
- MinHash+LSH encontra candidatos similares de forma determinística
- LLM só confirma os candidatos encontrados

### MinHash + LSH

```python
from datasketch import MinHash, MinHashLSH

def get_shingles(text: str, k: int = 3) -> set:
    """Gera k-gram shingles."""
    text = text.lower()
    return set(text[i:i+k] for i in range(len(text) - k + 1))

def create_minhash(shingles: set, num_perm: int = 128) -> MinHash:
    """Cria assinatura MinHash."""
    m = MinHash(num_perm=num_perm)
    for shingle in shingles:
        m.update(shingle.encode('utf8'))
    return m

# Exemplo:
name1 = "calculateRiskScore"
name2 = "calculateRiskScores"  # Muito similar

shingles1 = get_shingles(name1)  # {'cal', 'alc', 'lcu', 'cul', ...}
shingles2 = get_shingles(name2)

mh1 = create_minhash(shingles1)
mh2 = create_minhash(shingles2)

similarity = mh1.jaccard(mh2)  # ~0.95 (muito similar)
```

**Por que MinHash?**

1. **O(1) para comparar**: Depois de computar assinatura, comparação é constante
2. **LSH para busca**: Locality-Sensitive Hashing agrupa similares no mesmo bucket
3. **Escalável**: Funciona com milhões de entidades

---

# 6. ETAPA 3: EDGE EXTRACTION

## 6.1 O Que Faz

Extrai **relacionamentos factuais** entre as entidades já resolvidas.

## 6.2 Contexto Fornecido

```
┌─────────────────────────────────────────┐
│  CURRENT_EPISODE                        │
│  PREVIOUS_EPISODES                      │
├─────────────────────────────────────────┤
│  RESOLVED_ENTITIES                      │
│  ───────────────────                    │
│  Lista de entidades COM UUIDs válidos   │
│  (resultado das etapas 1 e 2)           │
└─────────────────────────────────────────┘
```

**Por que precisa dos UUIDs?**

O LLM deve usar EXATAMENTE os UUIDs fornecidos. Se inventar UUIDs, o edge é rejeitado.

## 6.3 Prompt de Edge Extraction

```python
EDGE_EXTRACTION_SYSTEM = """
You are an AI that extracts factual relationships between entities.

<EDGE_GUIDELINES>
1. Extract only FACTS, not opinions or hypotheticals
2. Each edge connects exactly TWO DISTINCT entities
3. Use SCREAMING_SNAKE_CASE for relation_type (e.g., WORKS_AT, LOVES, LOCATED_IN)
4. The "fact" field should be a natural language description of the relationship
5. CRITICAL: source_entity_id and target_entity_id MUST be UUIDs from the ENTITIES list
   - If you cannot find a valid UUID, DO NOT create the edge
6. Do NOT extract temporal information here (that's a separate step)
7. Prefer specific relation types over generic ones:
   - ✓ FAVORITE_BAND
   - ✗ LIKES (too generic)
</EDGE_GUIDELINES>

<COMMON_RELATION_TYPES>
- WORKS_AT, EMPLOYED_BY
- LIVES_IN, LOCATED_IN
- MANAGES, REPORTS_TO
- CREATED, AUTHORED
- MEMBER_OF, PART_OF
- KNOWS, FRIEND_OF
- MARRIED_TO, PARENT_OF
- OWNS, PURCHASED
- PREFERS, FAVORITE_X
</COMMON_RELATION_TYPES>
"""

EDGE_EXTRACTION_USER = """
<PREVIOUS_EPISODES>
{previous_episodes}
</PREVIOUS_EPISODES>

<CURRENT_EPISODE>
{current_episode}
</CURRENT_EPISODE>

<ENTITIES>
{entities_with_uuids}
</ENTITIES>

Extract all factual relationships between the ENTITIES based on CURRENT_EPISODE.

CRITICAL: Use ONLY UUIDs from the ENTITIES list above. Do not invent UUIDs.

Respond with JSON:
{{
  "extracted_edges": [
    {{
      "source_entity_id": "uuid-from-entities-list",
      "target_entity_id": "uuid-from-entities-list",
      "relation_type": "RELATION_TYPE",
      "fact": "Natural language description of the relationship"
    }}
  ]
}}
"""
```

## 6.4 Exemplo de Extração

**Episódio:**
```
Preston: I've been a huge Pink Floyd fan since I moved to California in 2015.
```

**Entities (resolvidas):**
```json
[
  {"uuid": "e1", "name": "Preston", "labels": ["Person"]},
  {"uuid": "e2", "name": "Pink Floyd", "labels": ["Organization"]},
  {"uuid": "e3", "name": "California", "labels": ["Location"]}
]
```

**Edges Extraídos:**
```json
{
  "extracted_edges": [
    {
      "source_entity_id": "e1",
      "target_entity_id": "e2",
      "relation_type": "FAVORITE_BAND",
      "fact": "Preston has been a huge Pink Floyd fan since 2015"
    },
    {
      "source_entity_id": "e1",
      "target_entity_id": "e3",
      "relation_type": "LIVES_IN",
      "fact": "Preston moved to California in 2015"
    }
  ]
}
```

## 6.5 Hiper-Edges (Implícito)

Graphiti suporta "hiper-edges" implicitamente. O mesmo fato pode gerar múltiplos edges:

```
Fato: "João, Maria e Pedro trabalham na Empresa X"

Edges gerados:
- João → WORKS_AT → Empresa X
- Maria → WORKS_AT → Empresa X  
- Pedro → WORKS_AT → Empresa X
```

---

# 7. ETAPA 4: EDGE DEDUPLICATION

## 7.1 O Que Faz

Verifica se um edge extraído já existe no grafo (mesmo fato, possivelmente com redação diferente).

## 7.2 Otimização Crítica

**Busca RESTRITA ao mesmo par de entidades:**

```python
def find_duplicate_candidates(new_edge, graph):
    """
    NÃO busca em todo o grafo.
    Busca apenas edges entre o MESMO PAR de entidades.
    """
    query = """
    MATCH (a {uuid: $source})-[r]->(b {uuid: $target})
    RETURN r
    """
    return graph.query(query, {
        "source": new_edge.source_entity_id,
        "target": new_edge.target_entity_id
    })
```

**Por que isso importa?**

```
Grafo com 100,000 edges:
- Busca global: O(100,000) comparações
- Busca por par: O(~10) comparações (poucos edges entre mesmo par)
```

## 7.3 Prompt de Edge Deduplication

```python
EDGE_DEDUPLICATION_SYSTEM = """
You are an AI that determines if two edges represent the same fact.

<DEDUPLICATION_GUIDELINES>
1. Two edges are duplicates if they express the SAME fact about the SAME entities
2. Different wording is OK - focus on semantic equivalence:
   - "John works at Google" == "John is employed by Google"
3. Different facts about same entities are NOT duplicates:
   - "John founded Google" != "John works at Google"
4. Temporal differences matter:
   - "John worked at Google in 2020" != "John worked at Google in 2015"
5. If duplicate, explain which existing edge it duplicates
</DEDUPLICATION_GUIDELINES>
"""

EDGE_DEDUPLICATION_USER = """
<NEW_EDGE>
Source: {source_entity_name}
Target: {target_entity_name}
Relation: {relation_type}
Fact: {fact}
</NEW_EDGE>

<EXISTING_EDGES_BETWEEN_SAME_ENTITIES>
{existing_edges}
</EXISTING_EDGES_BETWEEN_SAME_ENTITIES>

Is NEW_EDGE a duplicate of any existing edge?

Respond with JSON:
{{
  "is_duplicate": true|false,
  "duplicate_of_uuid": "uuid or null",
  "reasoning": "Brief explanation"
}}
"""
```

## 7.4 IR-Backed Edge Workflows (v1.0)

Antes de chamar o LLM, o sistema usa técnicas de Information Retrieval:

```python
def find_related_edges(new_edge, existing_edges):
    """
    Usa IR para filtrar candidatos antes do LLM.
    """
    scores = []
    
    for existing in existing_edges:
        # 1. Text overlap (Jaccard nos tokens)
        text_sim = jaccard_similarity(
            tokenize(new_edge.fact),
            tokenize(existing.fact)
        )
        
        # 2. Embedding similarity
        embed_sim = cosine_similarity(
            embed(new_edge.fact),
            embed(existing.fact)
        )
        
        # 3. Relation type match
        type_match = 1.0 if new_edge.relation_type == existing.relation_type else 0.5
        
        # Combine com RRF
        rrf_score = reciprocal_rank_fusion([text_sim, embed_sim, type_match])
        scores.append((existing, rrf_score))
    
    # Retorna top-K para o LLM analisar
    return sorted(scores, key=lambda x: x[1], reverse=True)[:5]
```

---

# 8. ETAPA 5: TEMPORAL EXTRACTION

## 8.1 O Que Faz

Extrai informações temporais para popular `t_valid` e `t_invalid` de cada edge.

## 8.2 Tipos de Referências Temporais

| Tipo | Exemplo | Resolução |
|------|---------|-----------|
| **Absoluta** | "23 de junho de 1912" | Parse direto |
| **Relativa** | "duas semanas atrás" | Calcula a partir de reference_time |
| **Parcial** | "em 2020", "no verão passado" | Usa defaults (Jan 1, 00:00) |
| **Implícita** | Presente do indicativo | t_valid = reference_time |
| **Ausente** | Sem menção temporal | null (sempre válido) |

## 8.3 Prompt de Temporal Extraction

```python
TEMPORAL_EXTRACTION_SYSTEM = """
You are an AI that extracts temporal information from facts.

<TEMPORAL_GUIDELINES>
1. Use REFERENCE_TIME as "now" for relative dates
2. Output dates in ISO 8601: YYYY-MM-DDTHH:MM:SS.SSSSSSZ
3. For partial dates, use reasonable defaults:
   - "in 2020" → 2020-01-01T00:00:00.000000Z
   - "last summer" → estimate based on reference_time
4. valid_at: When the fact STARTED being true
5. invalid_at: When the fact STOPPED being true (null if still true)
6. For present tense statements, valid_at = reference_time
7. Do NOT infer dates from unrelated events
8. If no temporal info, return null for both dates

<EXAMPLES>
Fact: "John moved to NYC in March 2020"
→ valid_at: "2020-03-01T00:00:00.000000Z" (moved TO = start)
→ invalid_at: null (presumably still there)

Fact: "John worked at Google from 2018 to 2021"
→ valid_at: "2018-01-01T00:00:00.000000Z"
→ invalid_at: "2021-12-31T23:59:59.999999Z"

Fact: "John is a software engineer"
(reference_time: 2024-01-15)
→ valid_at: "2024-01-15T00:00:00.000000Z"
→ invalid_at: null
</EXAMPLES>
</TEMPORAL_GUIDELINES>
"""

TEMPORAL_EXTRACTION_USER = """
<REFERENCE_TIME>
{reference_time}
</REFERENCE_TIME>

<FACT>
{fact}
</FACT>

<EPISODE_CONTEXT>
{episode_content}
</EPISODE_CONTEXT>

Extract temporal validity for this FACT.

Respond with JSON:
{{
  "valid_at": "ISO8601 datetime or null",
  "invalid_at": "ISO8601 datetime or null",
  "temporal_expression_found": "the original temporal phrase, or null",
  "reasoning": "Brief explanation of how you determined the dates"
}}
"""
```

## 8.4 Exemplo de Extração

**Episódio (reference_time: 2024-08-15):**
```
"I've been listening to Pink Floyd since I moved to California in 2015"
```

**Edges para processar:**
```json
[
  {
    "fact": "Preston has been a huge Pink Floyd fan since 2015",
    "source": "Preston",
    "target": "Pink Floyd"
  },
  {
    "fact": "Preston moved to California in 2015",
    "source": "Preston", 
    "target": "California"
  }
]
```

**Output:**
```json
[
  {
    "edge_uuid": "e1",
    "valid_at": "2015-01-01T00:00:00.000000Z",
    "invalid_at": null,
    "temporal_expression_found": "since 2015",
    "reasoning": "'since 2015' indicates ongoing relationship that started in 2015"
  },
  {
    "edge_uuid": "e2",
    "valid_at": "2015-01-01T00:00:00.000000Z",
    "invalid_at": null,
    "temporal_expression_found": "in 2015",
    "reasoning": "'moved to in 2015' indicates relocation, presumably still there"
  }
]
```

---

# 9. ETAPA 6: EDGE INVALIDATION

## 9.1 O Que Faz

Detecta quando um novo fato **contradiz** um fato existente e marca o antigo como inválido.

## 9.2 A Regra de Ouro

```
╔═══════════════════════════════════════════════════════════╗
║                                                           ║
║         INFORMAÇÃO NOVA SEMPRE VENCE (em T')              ║
║                                                           ║
║  Na timeline transacional, o dado mais recente é          ║
║  considerado a verdade atual do sistema.                  ║
║                                                           ║
╚═══════════════════════════════════════════════════════════╝
```

## 9.3 Lógica de Invalidação

```python
def invalidate_contradicting_edges(new_edge, existing_edges):
    """
    Para cada edge existente, verifica se contradiz o novo.
    """
    invalidations = []
    
    for existing in existing_edges:
        # 1. LLM detecta contradição
        if llm_detects_contradiction(new_edge, existing):
            
            # 2. Verifica overlap temporal
            if temporal_overlap(new_edge, existing):
                
                # 3. Invalida o antigo
                existing.t_invalid = new_edge.t_valid  # Cronológico
                existing.t_expired = now()              # Transacional
                
                invalidations.append({
                    "invalidated_edge": existing.uuid,
                    "reason": "Contradicted by new information",
                    "new_edge": new_edge.uuid
                })
    
    return invalidations
```

## 9.4 Prompt de Edge Invalidation

```python
EDGE_INVALIDATION_SYSTEM = """
You are an AI that detects contradictions between facts.

<CONTRADICTION_GUIDELINES>
1. Two facts CONTRADICT if they make mutually exclusive claims:
   - "John lives in NYC" contradicts "John lives in LA" (for same time period)
   - "John is CEO" contradicts "John is CFO" (same company, same time)
   
2. Two facts DO NOT contradict if:
   - They refer to different time periods
   - They are about different aspects
   - One is more specific than the other (subset, not contradiction)
   
3. Additive facts never contradict:
   - "File was modified in commit A" + "File was modified in commit B" = both true
   
4. State changes ARE contradictions if temporal overlap:
   - "John is married to Mary" (2020-present)
   - "John is married to Susan" (2022-present)
   → Contradiction with overlap

5. When in doubt, they do NOT contradict (preserve both)
</CONTRADICTION_GUIDELINES>
"""

EDGE_INVALIDATION_USER = """
<NEW_EDGE>
Source: {source_name}
Target: {target_name}
Relation: {relation_type}
Fact: {fact}
Valid from: {valid_at}
Valid until: {invalid_at}
</NEW_EDGE>

<EXISTING_EDGE>
UUID: {existing_uuid}
Source: {existing_source}
Target: {existing_target}
Relation: {existing_relation}
Fact: {existing_fact}
Valid from: {existing_valid_at}
Valid until: {existing_invalid_at}
</EXISTING_EDGE>

Does NEW_EDGE contradict EXISTING_EDGE?

Respond with JSON:
{{
  "is_contradiction": true|false,
  "has_temporal_overlap": true|false,
  "reasoning": "Explanation of why this is or isn't a contradiction",
  "suggested_invalid_at": "ISO8601 datetime for existing edge, or null"
}}
"""
```

## 9.5 Exemplo de Invalidação

**Grafo existente:**
```
Edge: Preston LIVES_IN California
- t_valid: 2015-01-01
- t_invalid: null (presente)
- t_created: 2024-08-01
```

**Novo episódio:**
```
"I just moved to New York last month!"
(reference_time: 2024-09-15)
```

**Novo edge extraído:**
```
Edge: Preston LIVES_IN New York
- t_valid: 2024-08-15 ("last month")
- t_invalid: null
```

**Resultado da invalidação:**
```
Edge antigo atualizado:
- t_invalid: 2024-08-15 (quando mudou)
- t_expired: 2024-09-15 (quando soubemos)

Razão: "LIVES_IN is exclusive - person can only live in one place at a time"
```

---

# 10. ETAPA 7: COMMUNITY DETECTION

## 10.1 O Que Faz

Agrupa entidades fortemente conectadas em **comunidades** de alto nível, com sumários gerados por LLM.

## 10.2 Algoritmo: Label Propagation

**Por que Label Propagation e não Leiden?**

| Aspecto | Label Propagation | Leiden |
|---------|-------------------|--------|
| Atualização incremental | Fácil | Difícil |
| Recomputação completa | Raramente necessária | Frequente |
| Latência de ingestão | Baixa | Alta |
| Qualidade | Boa | Melhor |

Graphiti prioriza **latência baixa** na ingestão, então usa Label Propagation.

## 10.3 Atualização Incremental

```python
def add_entity_to_community(new_entity, graph):
    """
    Quando uma nova entidade é adicionada:
    1. Encontra vizinhos diretos
    2. Conta comunidades dos vizinhos
    3. Atribui à comunidade com mais vizinhos (plurality)
    4. Atualiza sumário da comunidade
    """
    # 1. Encontrar vizinhos
    neighbors = graph.get_neighbors(new_entity.uuid)
    
    if not neighbors:
        # Entidade isolada: criar nova comunidade
        community = create_new_community(new_entity)
        return community
    
    # 2. Contar votos por comunidade
    community_votes = Counter()
    for neighbor in neighbors:
        community_votes[neighbor.community_id] += 1
    
    # 3. Atribuir à comunidade vencedora
    winning_community = community_votes.most_common(1)[0][0]
    new_entity.community_id = winning_community
    
    # 4. Atualizar sumário
    update_community_summary(winning_community)
    
    return winning_community
```

## 10.4 Prompt de Community Summary

```python
COMMUNITY_SUMMARY_SYSTEM = """
You are an AI that creates concise summaries for groups of related entities.

<SUMMARY_GUIDELINES>
1. The summary should describe WHAT the community is about
2. Include key entities by name
3. Highlight common themes or relationships
4. Keep under 100 words
5. Include searchable keywords that would help find this community
</SUMMARY_GUIDELINES>
"""

COMMUNITY_SUMMARY_USER = """
<COMMUNITY_ENTITIES>
{entity_names_and_summaries}
</COMMUNITY_ENTITIES>

<COMMUNITY_EDGES>
{edges_within_community}
</COMMUNITY_EDGES>

Create a summary for this community.

Respond with JSON:
{{
  "name": "Short descriptive name (2-4 words)",
  "summary": "Detailed summary of what this community represents",
  "keywords": ["keyword1", "keyword2", "keyword3"]
}}
"""
```

## 10.5 Exemplo de Comunidade

**Entidades no cluster:**
- Preston (Person)
- Pink Floyd (Organization)  
- California (Location)
- "The Wall" (Album)
- "Wish You Were Here" (Album)

**Summary gerado:**
```json
{
  "name": "Preston's Music Preferences",
  "summary": "This community centers on Preston's musical interests, particularly their long-standing appreciation for Pink Floyd. Includes albums like 'The Wall' and 'Wish You Were Here'. Connected to California, where Preston has lived since becoming a fan.",
  "keywords": ["music", "Pink Floyd", "Preston", "rock", "albums"]
}
```

## 10.6 Limitação: Drift

Com atualizações incrementais, as comunidades gradualmente **divergem** do que um algoritmo completo produziria.

**Solução**: Refresh periódico (ex: diário) que reexecuta Label Propagation em todo o grafo.

---

# 11. RETRIEVAL (BUSCA)

## 11.1 Busca Híbrida

O retrieval combina três métodos de busca:

```
f(α) = χ(ρ(φ(α))) = β

Onde:
- α = query do usuário
- φ = funções de busca (cosine, BM25, BFS)
- ρ = reranker (RRF, MMR, cross-encoder)
- χ = construtor de contexto
- β = string de contexto para o LLM
```

## 11.2 Métodos de Busca (φ)

### φ_cos: Cosine Similarity

```python
def cosine_search(query_embedding, graph, top_k=20):
    """
    Busca por similaridade de cosseno nos embeddings.
    
    Alvos:
    - Edge facts (campo: fact)
    - Entity names (campo: name)
    - Community names (campo: name)
    """
    results = []
    
    # Buscar edges
    edge_query = """
    CALL db.index.vector.queryNodes('edge_embeddings', $k, $embedding)
    YIELD node, score
    WHERE node.t_expired IS NULL
    RETURN node, score
    """
    results.extend(graph.query(edge_query, {"k": top_k, "embedding": query_embedding}))
    
    # Buscar entities
    entity_query = """
    CALL db.index.vector.queryNodes('entity_embeddings', $k, $embedding)
    YIELD node, score
    RETURN node, score
    """
    results.extend(graph.query(entity_query, {"k": top_k, "embedding": query_embedding}))
    
    return results
```

### φ_bm25: Full-Text Search

```python
def bm25_search(query_text, graph, top_k=20):
    """
    Busca full-text usando BM25 (via Lucene/Neo4j).
    
    Bom para:
    - Keywords exatas
    - Nomes próprios
    - Termos técnicos
    """
    edge_query = """
    CALL db.index.fulltext.queryNodes('edge_facts', $query)
    YIELD node, score
    WHERE node.t_expired IS NULL
    RETURN node, score
    LIMIT $k
    """
    return graph.query(edge_query, {"query": query_text, "k": top_k})
```

### φ_bfs: Breadth-First Search

```python
def bfs_search(center_uuid, graph, depth=2):
    """
    Busca por proximidade no grafo a partir de um nó central.
    
    Útil quando:
    - Usuário mencionou uma entidade específica
    - Queremos contexto ao redor dessa entidade
    """
    query = """
    MATCH (center {uuid: $uuid})
    CALL apoc.path.subgraphAll(center, {
        maxLevel: $depth,
        relationshipFilter: null
    })
    YIELD nodes, relationships
    RETURN nodes, relationships
    """
    return graph.query(query, {"uuid": center_uuid, "depth": depth})
```

## 11.3 Reranking (ρ)

### Reciprocal Rank Fusion (RRF)

Combina rankings de diferentes métodos:

```python
def reciprocal_rank_fusion(rankings, k=60):
    """
    RRF score = Σ 1/(k + rank_i)
    
    k=60 é o valor padrão (empírico).
    """
    scores = {}
    
    for ranking in rankings:
        for rank, item in enumerate(ranking):
            item_id = item["uuid"]
            if item_id not in scores:
                scores[item_id] = 0
            scores[item_id] += 1 / (k + rank + 1)
    
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

### Maximal Marginal Relevance (MMR)

Balanceia relevância com diversidade:

```python
def mmr_rerank(query_embedding, candidates, lambda_param=0.5):
    """
    MMR = λ * sim(query, doc) - (1-λ) * max(sim(doc, selected))
    
    Evita redundância nos resultados.
    """
    selected = []
    remaining = candidates.copy()
    
    while remaining and len(selected) < 10:
        best_score = -1
        best_item = None
        
        for item in remaining:
            relevance = cosine_similarity(query_embedding, item["embedding"])
            
            if selected:
                redundancy = max(
                    cosine_similarity(item["embedding"], s["embedding"])
                    for s in selected
                )
            else:
                redundancy = 0
            
            mmr_score = lambda_param * relevance - (1 - lambda_param) * redundancy
            
            if mmr_score > best_score:
                best_score = mmr_score
                best_item = item
        
        selected.append(best_item)
        remaining.remove(best_item)
    
    return selected
```

## 11.4 Construção de Contexto (χ)

```python
def construct_context(results, max_tokens=4000):
    """
    Formata resultados em string para o LLM.
    """
    context_parts = []
    
    # Seção de FATOS
    facts = [r for r in results if r["type"] == "edge"]
    if facts:
        context_parts.append("FACTS (with validity periods):")
        context_parts.append("<FACTS>")
        for fact in facts[:20]:
            valid = fact.get("t_valid", "unknown")
            invalid = fact.get("t_invalid", "present")
            context_parts.append(f"- {fact['fact']} (valid: {valid} to {invalid})")
        context_parts.append("</FACTS>")
    
    # Seção de ENTIDADES
    entities = [r for r in results if r["type"] == "entity"]
    if entities:
        context_parts.append("\nENTITIES:")
        context_parts.append("<ENTITIES>")
        for entity in entities[:10]:
            context_parts.append(f"- {entity['name']}: {entity.get('summary', '')}")
        context_parts.append("</ENTITIES>")
    
    # Seção de COMUNIDADES
    communities = [r for r in results if r["type"] == "community"]
    if communities:
        context_parts.append("\nRELATED TOPICS:")
        context_parts.append("<COMMUNITIES>")
        for comm in communities[:3]:
            context_parts.append(f"- {comm['name']}: {comm.get('summary', '')}")
        context_parts.append("</COMMUNITIES>")
    
    return "\n".join(context_parts)
```

---

# 12. ANÁLISE DE CUSTOS

## 12.1 Chamadas LLM por Episódio

| Etapa | Chamadas | Paralelo? | Modelo Sugerido |
|-------|:--------:|:---------:|-----------------|
| Entity Extraction | 1-2 | N/A | gpt-4o-mini |
| Entity Resolution | N (por entidade) | ✅ | gpt-4o-mini |
| Edge Extraction | 1 | N/A | gpt-4o-mini |
| Edge Deduplication | M (por edge) | ✅ | gpt-4o-mini |
| Temporal Extraction | M (por edge) | ✅ | gpt-4o-mini |
| Edge Invalidation | Variável | Parcial | gpt-4o-mini |
| Community Detection | 1 | N/A | gpt-4o-mini |

**Total típico: 5-20+ chamadas LLM por episódio**

## 12.2 Por Que Usuários Atingem Rate Limits

```
Configuração: SEMAPHORE_LIMIT = 10 (episódios paralelos)

Episódio típico:
- 3 entidades → 3 chamadas de resolution
- 2 edges → 2 chamadas de dedup + 2 de temporal
- Total: ~10 chamadas por episódio

Com 10 episódios paralelos:
→ 100 chamadas LLM simultâneas!

Rate limit OpenAI (tier 1): 60 req/min
→ BOOM! Rate limit atingido
```

**Solução**: Reduzir SEMAPHORE_LIMIT ou usar modelos com rate limits maiores.

## 12.3 Otimizações que Reduzem Custos

1. **Exact match em entity resolution**: Evita LLM se nomes normalizados são iguais
2. **Entropy gate**: Evita LLM para nomes únicos sem candidatos
3. **Edge dedup restrito**: Busca apenas edges entre mesmo par
4. **LRU cache em shingles**: Evita recomputação

Resultado: **30-50% menos chamadas LLM** em cenários típicos.

---

# 13. RESUMO: POR QUE CADA DECISÃO

| Decisão | Por Quê |
|---------|---------|
| **3 subgrafos** | Separar dados brutos (episodic) de conhecimento estruturado (semantic) de visão alto nível (community) |
| **Bi-temporal** | Modelar tanto "quando aconteceu" quanto "quando soubemos" |
| **7 etapas separadas** | Paralelização, testabilidade, modelos menores |
| **1 LLM call por entidade** | Output simples (is_duplicate), menos confusão |
| **Entropy gate** | Evitar LLM quando desnecessário (nomes únicos) |
| **MinHash + LSH** | Encontrar candidatos em O(1) |
| **Edge dedup restrito** | Reduzir espaço de busca drasticamente |
| **Label Propagation** | Atualização incremental com baixa latência |
| **Busca híbrida** | Cobrir diferentes aspectos de relevância |
| **RRF para fusão** | Combinar rankings sem precisar de pesos manuais |
| **Novo sempre vence (T')** | Simplifica resolução de conflitos |

---

# APÊNDICE: COMPARAÇÃO COM ALTERNATIVAS

| Aspecto | Graphiti | GraphRAG (MS) | Mem0 |
|---------|----------|---------------|------|
| **Temporalidade** | Bi-temporal (4 timestamps) | Nenhuma | Nenhuma |
| **Atualização** | Incremental | Batch (reprocessa tudo) | Incremental |
| **Comunidades** | Label Propagation | Leiden | Nenhuma |
| **Entity Resolution** | Entropy-gated + LLM | Simples | LLM |
| **Edge Dedup** | Por par de entidades | Global | Nenhuma |
| **Custo por episódio** | 5-20 LLM calls | 1-3 LLM calls | 1-2 LLM calls |
| **Complexidade** | Alta | Média | Baixa |
| **Caso de uso ideal** | Agentes com memória evolutiva | Análise de corpus estático | Memória simples de chat |
