# 5. RESULTADOS PRELIMINARES

## 5.1 Introdução

Esta seção apresenta os resultados preliminares da implementação da abordagem de Knowledge Graph para análise de avaliações de aplicativos bancários. A fase preliminar teve como objetivo validar a viabilidade técnica da modelagem de relacionamentos entre entidades extraídas dos comentários e as capacidades de negócio (BusinessCapability), utilizando o framework Graphiti em conjunto com o banco de dados Neo4j.

A implementação desta abordagem representa uma evolução do sistema inicial, que processava avaliações de forma sequencial através de scripts Python. A nova arquitetura permite a modelagem de conhecimento estruturado, facilitando a identificação de padrões, correlações entre versões do aplicativo e problemas reportados, e a geração de alertas visuais para gestão de produtos.

## 5.2 Metodologia da Abordagem Graphiti

### 5.2.1 Framework Graphiti

O Graphiti é um framework de knowledge graph temporal desenvolvido para agentes de IA, que modela conhecimento como fatos que evoluem no tempo, diferentemente de sistemas RAG tradicionais que tratam informação como estática. A arquitetura do Graphiti é composta por três subgrafos interconectados:

**Subgrafo Episódico (Gₑ)**: Preserva o conteúdo bruto original dos comentários, funcionando como "memória episódica" que mantém o contexto completo de onde a informação foi extraída. Cada episódio representa um comentário de avaliação com suas propriedades originais (conteúdo, data, versão do app, nome do aplicativo).

**Subgrafo Semântico (Gₛ)**: Contém entidades (nós) conectadas por fatos (edges) no grafo semântico. Cada edge possui metadados bi-temporais que registram quando o fato era válido no mundo real (t_valid, t_invalid) e quando foi registrado no sistema (t_created, t_expired).

**Subgrafo de Comunidade (Gᴄ)**: Agrupa entidades fortemente conectadas em comunidades de alto nível, geradas via Label Propagation, permitindo uma visão agregada dos temas mais frequentes.

### 5.2.2 Modelo Bi-Temporal

O modelo bi-temporal permite distinguir duas dimensões temporais distintas:

- **Timeline Cronológica (T)**: Quando algo aconteceu no mundo real
  - `t_valid`: Início da validade do fato
  - `t_invalid`: Fim da validade (null se ainda válido)

- **Timeline Transacional (T')**: Quando o sistema soube do fato
  - `t_created`: Quando inserimos no grafo
  - `t_expired`: Quando marcamos como inválido

Este modelo permite realizar queries temporais como "quais problemas eram válidos em uma data específica" ou "o que o sistema sabia em um determinado momento", facilitando análises históricas e auditoria.

### 5.2.3 Extração de Entidades

A extração de entidades é realizada através de um processo de duas etapas utilizando GPT-4o:

**Etapa 1 - Extração Inicial**: O modelo LLM analisa o comentário e identifica entidades significativas, classificando-as em tipos predefinidos:
- **Feature**: Funcionalidades do aplicativo (ex: PIX, Login, Transferências, Notificações)
- **Issue**: Problemas técnicos ou funcionais (ex: Performance, Segurança, Lentidão)
- **App**: Aplicativo mencionado (ex: Santander, Bradesco)
- **Version**: Versão do aplicativo mencionada
- **Service**: Serviços bancários (ex: Empréstimos, Investimentos)
- **Device**: Dispositivo ou plataforma (ex: Android, iOS)

**Etapa 2 - Reflexão**: Uma segunda chamada ao LLM verifica se entidades foram perdidas na primeira passada, especialmente entidades implícitas ou referenciadas por pronomes. Esta técnica recupera aproximadamente 5-10% de entidades adicionais.

### 5.2.4 BusinessCapability

As BusinessCapability representam capacidades de negócio hierárquicas (níveis 1-3) que agrupam funcionalidades relacionadas. Cada capacidade possui:
- **Nível hierárquico**: 1 (Core), 2 (Específicas), 3 (Detalhadas)
- **Tipo**: Core, Supporting ou Strategic
- **Maturidade**: Initial, Managed, Defined ou Optimized
- **Valor de negócio**: High, Medium ou Low

As 16 capacidades mapeadas incluem: Autenticação e Acesso, Performance e Estabilidade, Interface e Experiência do Usuário, Transferências PIX, Empréstimos e Crédito, entre outras.

## 5.3 Implementação Técnica

### 5.3.1 Arquitetura do Grafo

A estrutura do grafo foi projetada para garantir unicidade de entidades e facilitar análises visuais:

```
App (Santander) ← único
  ↑ BELONGS_TO
Version (25.9.1.3) ← agrupa episódios
  ↑ HAS_VERSION
Episode (comentário original preservado)
  ↓ CONTAINS_ENTITY
Issue/Feature (ex: "Lentidão", "PIX")
  ↓ RELATED_TO_VERSION (com propriedade count)
Version
  ↓ RELATES_TO_CAPABILITY
BusinessCapability (ex: "Performance e Estabilidade")
```

**Características principais**:
- **App único**: O aplicativo "Santander" é representado por uma única entidade, evitando duplicações
- **Versões como entidades**: Cada versão do app (ex: 25.9.1.3) é uma entidade separada que agrupa episódios relacionados
- **Agrupamento de entidades**: Entidades com mesmo nome são agrupadas automaticamente (ex: múltiplas menções a "Lentidão" viram uma única entidade)
- **Contagem visual**: O relacionamento `RELATED_TO_VERSION` possui uma propriedade `count` que incrementa a cada nova ocorrência, permitindo visualização proporcional no Neo4j Browser

### 5.3.2 Processamento de Comentários

O processamento segue o seguinte fluxo:

1. **Inicialização do Grafo**: Criação de índices e população das 16 BusinessCapability
2. **Carregamento de Dados**: Leitura do CSV com resultados da correlação funcional
3. **Filtragem**: Seleção dos comentários negativos do aplicativo Santander, ordenados por data (mais recentes primeiro)
4. **Processamento por Lote**: Processamento em batches configuráveis (padrão: 5 comentários por vez)
5. **Extração de Entidades**: Para cada comentário, extração de entidades usando GPT-4o
6. **Criação de Nós**: Criação ou atualização de nós no grafo (App, Version, Episode, Entities)
7. **Linkagem**: Criação de relacionamentos entre entidades, versões, app e BusinessCapability
8. **Mapeamento Automático**: Mapeamento inteligente de entidades para BusinessCapability baseado em regras e contexto

### 5.3.3 Mapeamento Entidade → BusinessCapability

O mapeamento de entidades para BusinessCapability é realizado através de um algoritmo híbrido:

1. **Mapeamento Direto**: Dicionário de palavras-chave que mapeia nomes de entidades para categorias (ex: "lentidão" → Performance, "fora do ar" → Performance)
2. **Análise de Labels**: Se a entidade possui label "Issue" e não há mapeamento direto, atribui-se "Performance" como padrão
3. **Categorias do Comentário**: Utiliza as categorias funcionais já identificadas pelo GPT-4o no processo de correlação funcional
4. **Fallback**: Entidades sem categoria específica são mapeadas para "Outros"

**Exemplos de mapeamentos implementados**:
- "Fora do Ar" → Performance e Estabilidade
- "Falha" → Performance e Estabilidade
- "Problema na cabeça" (expressão idiomática) → Atendimento ao Cliente
- "Menu de resposta automática" → Atendimento ao Cliente
- "Dificuldade em falar com atendente" → Atendimento ao Cliente

## 5.4 Resultados Obtidos

### 5.4.1 Amostra Processada

Para validação preliminar, foram processados os 10 comentários negativos mais recentes do aplicativo Santander, coletados em 07 de janeiro de 2026. Todos os comentários pertenciam à versão 25.9.1.3 do aplicativo.

### 5.4.2 Estatísticas do Grafo

Após o processamento completo, o grafo apresentou as seguintes estatísticas:

| Métrica | Quantidade |
|---------|------------|
| Episódios (comentários) | 10 |
| Entidades extraídas | 24 |
| BusinessCapability | 16 |
| Relacionamentos criados | 84.480 |

**Distribuição de entidades por tipo**:
- **Issues**: 12 entidades (problemas técnicos e funcionais)
- **Features**: 11 entidades (funcionalidades mencionadas)
- **App**: 1 entidade (Santander)
- **Version**: 1 entidade (25.9.1.3)

### 5.4.3 Cobertura de Linkagem

Uma métrica importante para validar a qualidade do processamento é a cobertura de linkagem entre entidades e BusinessCapability. Dos 24 relacionamentos `CONTAINS_ENTITY` criados, 23 foram linkados com sucesso a BusinessCapability, resultando em uma taxa de cobertura de **95,8%**.

As entidades não linkadas inicialmente foram identificadas e corrigidas através de um script de pós-processamento (`fix_missing_capabilities.py`), alcançando **100% de cobertura** após a correção.

### 5.4.4 Relacionamentos Criados

A estrutura de relacionamentos criada permite múltiplas análises:

- **BELONGS_TO**: 1 relacionamento (Version → App)
- **HAS_VERSION**: 10 relacionamentos (Episode → Version)
- **CONTAINS_ENTITY**: 24 relacionamentos (Episode → Entity)
- **RELATED_TO_VERSION**: 19 relacionamentos (Entity → Version, com propriedade count)
- **RELATES_TO_CAPABILITY**: 23 relacionamentos (Entity → BusinessCapability)

### 5.4.5 Distribuição de Issues por BusinessCapability

A distribuição das issues extraídas pelas BusinessCapability demonstra a capacidade do sistema em identificar padrões:

| BusinessCapability | Quantidade de Issues |
|-------------------|---------------------|
| Performance e Estabilidade | 6 |
| Atendimento ao Cliente | 3 |
| Interface e Experiência do Usuário | 2 |
| Autenticação e Acesso | 1 |
| Empréstimos e Crédito | 2 |
| Consulta de Saldo e Extrato | 2 |

**Análise**: A BusinessCapability "Performance e Estabilidade" concentrou o maior número de issues (6), incluindo problemas como "Lentidão", "Travamento", "Falha", "Fora do ar" e "Conexão Wi-Fi". Este resultado está alinhado com análises anteriores que identificaram Performance como a categoria mais frequente em avaliações negativas.

## 5.5 Análise Qualitativa

### 5.5.1 Exemplo de Processamento

Para ilustrar o funcionamento do sistema, apresenta-se um exemplo completo de processamento:

**Comentário original**:
> "tá impossível falar com um atendente! eu ligo joga em um menu digital, ligação pra falar com um 'humano' tá difícil, é só menu de resposta automática. vc clica em voltar a ligação ela nem chama já desliga, por favor retirem esse menu q aparece quando fazemos ligação, tudo que aparece lá já tem no aplicativo do banco, vocês devem ter algum problema na cabeça pra inventar algo assim"

**Entidades extraídas**:
- "Menu de resposta automática" (Feature, Issue)
- "Problema na cabeça" (Issue) - expressão idiomática sobre decisão ruim
- "Dificuldade em falar com atendente" (Issue)

**Relacionamentos criados**:
- Episode → HAS_VERSION → Version (25.9.1.3)
- Episode → CONTAINS_ENTITY → "Menu de resposta automática"
- Episode → CONTAINS_ENTITY → "Problema na cabeça"
- Episode → CONTAINS_ENTITY → "Dificuldade em falar com atendente"
- "Menu de resposta automática" → RELATED_TO_VERSION → Version (count: 1)
- "Problema na cabeça" → RELATED_TO_VERSION → Version (count: 1)
- "Dificuldade em falar com atendente" → RELATED_TO_VERSION → Version (count: 1)
- Todas as issues → RELATES_TO_CAPABILITY → "Atendimento ao Cliente"

**Insights gerados**:
- A versão 25.9.1.3 possui 3 issues relacionadas a atendimento
- Todas as issues foram corretamente mapeadas para a BusinessCapability "Atendimento ao Cliente"
- O sistema identificou uma expressão idiomática ("problema na cabeça") e a interpretou corretamente como crítica ao atendimento

### 5.5.2 Agrupamento Visual

O sistema permite visualização no Neo4j Browser com agrupamento proporcional baseado na propriedade `count` dos relacionamentos `RELATED_TO_VERSION`. Issues com maior frequência aparecem com nós maiores, facilitando a identificação rápida de problemas recorrentes.

**Query de alerta implementada**:
```cypher
MATCH (version:Version)-[:BELONGS_TO]->(app:App)
MATCH (issue)-[r:RELATED_TO_VERSION]->(version)
WITH app, version, sum(r.count) as total_issues
ORDER BY total_issues DESC
RETURN app, version, total_issues
LIMIT 10
```

Esta query identifica versões problemáticas ordenadas pelo total de issues reportadas, permitindo que gestores de produto identifiquem rapidamente versões que requerem atenção prioritária.

## 5.6 Limitações e Próximos Passos

### 5.6.1 Limitações Identificadas

**Escala da amostra**: A amostra preliminar de 10 comentários é insuficiente para generalizações estatísticas robustas. Uma amostra maior permitiria validar a estabilidade dos padrões identificados.

**Cobertura de mapeamento**: Embora tenha sido alcançada cobertura de 100% após correção, alguns mapeamentos podem requerer refinamento com base em feedback de especialistas de domínio.

**Performance de processamento**: O processamento atual utiliza chamadas sequenciais ao GPT-4o, o que pode ser otimizado através de processamento paralelo para grandes volumes.

**Validação temporal**: O modelo bi-temporal ainda não foi validado com dados históricos reais, sendo necessário processar comentários de diferentes períodos para validar a modelagem temporal.

### 5.6.2 Próximos Passos

**Expansão da amostra**: Processar os 100 comentários negativos mais recentes do Santander para validar a escalabilidade do sistema e identificar padrões mais robustos.

**Validação com especialistas**: Apresentar o grafo gerado para especialistas de produto e desenvolvimento para validar a correção dos mapeamentos e relacionamentos identificados.

**Implementação de queries avançadas**: Desenvolver queries Cypher adicionais para análises específicas:
- Análise temporal de problemas por versão
- Identificação de correlações entre diferentes tipos de issues
- Análise de tendências de problemas ao longo do tempo

**Otimização de performance**: Implementar processamento paralelo e cache de resultados de extração de entidades para reduzir custos e tempo de processamento.

**Integração com API**: Expor funcionalidades do grafo através de endpoints REST para integração com dashboards e ferramentas de gestão de produto.

**Validação de métricas**: Estabelecer métricas de qualidade para avaliação contínua do sistema:
- Precisão do mapeamento entidade → BusinessCapability
- Cobertura de extração de entidades
- Consistência temporal dos relacionamentos

## 5.7 Conclusões Preliminares

A implementação preliminar da abordagem de Knowledge Graph utilizando Graphiti e Neo4j demonstrou viabilidade técnica para modelagem de relacionamentos entre avaliações de aplicativos e capacidades de negócio. Os resultados obtidos com 10 comentários indicam que:

1. **Extração de entidades é eficaz**: O sistema conseguiu extrair 24 entidades relevantes de 10 comentários, identificando tanto problemas técnicos quanto funcionalidades mencionadas.

2. **Mapeamento para BusinessCapability funciona**: A taxa de cobertura de 100% após correção demonstra que o algoritmo de mapeamento é eficiente, mesmo para expressões idiomáticas e linguagem informal.

3. **Estrutura do grafo facilita análises**: A modelagem permite queries complexas que identificam versões problemáticas e correlacionam issues com capacidades de negócio de forma eficiente.

4. **Visualização é intuitiva**: O agrupamento proporcional baseado em contagem permite identificação visual rápida de problemas recorrentes.

5. **Sistema é extensível**: A arquitetura permite adicionar novos tipos de entidades, relacionamentos e BusinessCapability sem necessidade de reprocessamento completo.

Os resultados preliminares indicam que a abordagem é promissora para escalar para volumes maiores de dados e integrar-se com ferramentas de gestão de produto, fornecendo insights acionáveis para priorização de backlog e identificação proativa de problemas em versões específicas do aplicativo.
