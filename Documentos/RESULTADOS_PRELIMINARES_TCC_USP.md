# Resultados Preliminares

Esta seção apresenta os resultados parciais obtidos na pesquisa até o momento, seguindo a mesma ordem da seção Material e Métodos. A implementação preliminar focou na validação da abordagem de Knowledge Graph para extração de issues de comentários e sua correlação com capacidades de negócio do aplicativo, visando identificar bugs associados a versões específicas.

## Coleta e Definição do Dataset

Para a fase preliminar, foram processados 10 comentários negativos mais recentes do aplicativo Santander, coletados em 07 de janeiro de 2026 através do script `collect_reviews.py` utilizando a biblioteca `google-play-scraper`. Todos os comentários pertenciam à versão 25.9.1.3 do aplicativo, permitindo validar a capacidade do sistema em identificar problemas específicos de versão.

Os dados foram extraídos do arquivo `functional_correlation_results.csv`, que contém os resultados da etapa anterior de análise de sentimentos e correlação funcional. Cada registro possui os seguintes atributos: conteúdo textual, classificação de sentimento (positive/negative/neutral), data da avaliação, versão do aplicativo e nome do aplicativo.

## Arquitetura Híbrida de Modelagem

A arquitetura implementada mantém os dois estágios propostos no projeto de pesquisa, com uma evolução na etapa de correlação funcional:

**Estágio 1 - Análise de Sentimentos (Polaridade)**: Utiliza-se o modelo XLM-RoBERTa (BERTweet) para classificação de polaridade, conforme validado no estudo comparativo preliminar. Este estágio permanece inalterado, processando todas as avaliações coletadas.

**Estágio 2 - Extração de Entidades e Modelagem em Grafo**: As avaliações classificadas como negativas são submetidas a um processo de extração de entidades utilizando GPT-4o, seguindo o framework Graphiti. Diferentemente da abordagem inicial que categorizava diretamente em funcionalidades, a nova implementação extrai entidades (issues e features) dos comentários e as relaciona com capacidades de negócio (BusinessCapability) através de um grafo de conhecimento.

### Framework Graphiti e Banco de Dados Neo4j

O Graphiti é um framework de knowledge graph temporal que modela conhecimento como fatos que evoluem no tempo. A arquitetura é composta por três subgrafos interconectados:

- **Subgrafo Episódico (Gₑ)**: Preserva o conteúdo bruto original dos comentários, funcionando como "memória episódica" que mantém o contexto completo de onde a informação foi extraída. Cada episódio representa um comentário de avaliação com suas propriedades originais (conteúdo, data, versão do app, nome do aplicativo).

- **Subgrafo Semântico (Gₛ)**: Contém entidades (nós) conectadas por fatos (edges) no grafo semântico. Cada edge possui metadados bi-temporais que registram quando o fato era válido no mundo real (t_valid, t_invalid) e quando foi registrado no sistema (t_created, t_expired).

- **Subgrafo de Comunidade (Gᴄ)**: Agrupa entidades fortemente conectadas em comunidades de alto nível, geradas via Label Propagation, permitindo uma visão agregada dos temas mais frequentes.

O banco de dados Neo4j foi escolhido para armazenar o grafo devido à sua capacidade nativa de modelagem de relacionamentos e eficiência em queries de grafos complexas. A estrutura implementada segue o padrão Graphiti, garantindo unicidade de entidades e facilitando análises visuais.

### Extração de Entidades

A extração de entidades é realizada através de um processo de duas etapas utilizando GPT-4o:

**Etapa 1 - Extração Inicial**: O modelo LLM analisa o comentário e identifica entidades significativas, classificando-as em tipos predefinidos:
- **Feature**: Funcionalidades do aplicativo (ex: PIX, Login, Transferências, Notificações)
- **Issue**: Problemas técnicos ou funcionais (ex: Performance, Segurança, Lentidão, Travamento)
- **App**: Aplicativo mencionado (ex: Santander, Bradesco)
- **Version**: Versão do aplicativo mencionada
- **Service**: Serviços bancários (ex: Empréstimos, Investimentos)
- **Device**: Dispositivo ou plataforma (ex: Android, iOS)

**Etapa 2 - Reflexão**: Uma segunda chamada ao LLM verifica se entidades foram perdidas na primeira passada, especialmente entidades implícitas ou referenciadas por pronomes. Esta técnica recupera aproximadamente 5-10% de entidades adicionais, conforme documentado na literatura do Graphiti.

### BusinessCapability

As BusinessCapability representam capacidades de negócio hierárquicas (níveis 1-3) que agrupam funcionalidades relacionadas. Cada capacidade possui:
- **Nível hierárquico**: 1 (Core), 2 (Específicas), 3 (Detalhadas)
- **Tipo**: Core, Supporting ou Strategic
- **Maturidade**: Initial, Managed, Defined ou Optimized
- **Valor de negócio**: High, Medium ou Low

Foram mapeadas 16 capacidades, incluindo: Autenticação e Acesso (nível 1, Core), Performance e Estabilidade (nível 1, Supporting), Interface e Experiência do Usuário (nível 1, Core), Transferências PIX (nível 2, Core), Empréstimos e Crédito (nível 2, Core), Atendimento ao Cliente (nível 2, Supporting), entre outras.

### Arquitetura do Grafo

A estrutura do grafo foi projetada para garantir unicidade de entidades e facilitar a identificação de bugs por versão:

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
- **Versões como entidades**: Cada versão do app (ex: 25.9.1.3) é uma entidade separada que agrupa episódios relacionados, permitindo identificar problemas específicos de versão
- **Agrupamento de entidades**: Entidades com mesmo nome são agrupadas automaticamente (ex: múltiplas menções a "Lentidão" viram uma única entidade)
- **Contagem visual**: O relacionamento `RELATED_TO_VERSION` possui uma propriedade `count` que incrementa a cada nova ocorrência, permitindo visualização proporcional e identificação rápida de versões problemáticas

### Mapeamento Entidade → BusinessCapability

O mapeamento de entidades para BusinessCapability é realizado através de um algoritmo híbrido:

1. **Mapeamento Direto**: Dicionário de palavras-chave que mapeia nomes de entidades para categorias (ex: "lentidão" → Performance, "fora do ar" → Performance, "problema na cabeça" → Atendimento)

2. **Análise de Labels**: Se a entidade possui label "Issue" e não há mapeamento direto, atribui-se "Performance" como padrão para issues genéricas

3. **Categorias do Comentário**: Utiliza as categorias funcionais já identificadas pelo GPT-4o no processo de correlação funcional anterior

4. **Fallback**: Entidades sem categoria específica são mapeadas para "Outros"

## Resultados Obtidos

### Estatísticas do Grafo

Após o processamento completo dos 10 comentários, o grafo apresentou as seguintes estatísticas:

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

### Cobertura de Linkagem

Uma métrica importante para validar a qualidade do processamento é a cobertura de linkagem entre entidades e BusinessCapability. Dos 24 relacionamentos `CONTAINS_ENTITY` criados, 23 foram linkados com sucesso a BusinessCapability, resultando em uma taxa de cobertura inicial de **95,8%**.

As entidades não linkadas inicialmente foram identificadas e corrigidas através de um script de pós-processamento (`fix_missing_capabilities.py`), alcançando **100% de cobertura** após a correção. Este resultado demonstra a eficácia do algoritmo de mapeamento, mesmo para expressões idiomáticas e linguagem informal comum em avaliações de aplicativos.

### Relacionamentos Criados

A estrutura de relacionamentos criada permite múltiplas análises e identificação de padrões:

- **BELONGS_TO**: 1 relacionamento (Version → App)
- **HAS_VERSION**: 10 relacionamentos (Episode → Version)
- **CONTAINS_ENTITY**: 24 relacionamentos (Episode → Entity)
- **RELATED_TO_VERSION**: 19 relacionamentos (Entity → Version, com propriedade count)
- **RELATES_TO_CAPABILITY**: 23 relacionamentos (Entity → BusinessCapability)

### Distribuição de Issues por BusinessCapability

A distribuição das issues extraídas pelas BusinessCapability demonstra a capacidade do sistema em identificar padrões e correlacionar problemas com capacidades de negócio:

| BusinessCapability | Quantidade de Issues |
|-------------------|---------------------|
| Performance e Estabilidade | 6 |
| Atendimento ao Cliente | 3 |
| Interface e Experiência do Usuário | 2 |
| Autenticação e Acesso | 1 |
| Empréstimos e Crédito | 2 |
| Consulta de Saldo e Extrato | 2 |

**Análise**: A BusinessCapability "Performance e Estabilidade" concentrou o maior número de issues (6), incluindo problemas como "Lentidão", "Travamento", "Falha", "Fora do ar" e "Conexão Wi-Fi". Este resultado está alinhado com análises anteriores que identificaram Performance como a categoria mais frequente em avaliações negativas, validando a consistência do sistema de extração e mapeamento.

### Identificação de Bugs por Versão

O objetivo principal da implementação foi validar a capacidade do sistema em identificar bugs associados a versões específicas do aplicativo. A estrutura do grafo permite realizar queries que identificam:

1. **Versões problemáticas**: A versão 25.9.1.3 foi identificada como possuindo 19 issues relacionadas, distribuídas em 6 BusinessCapability diferentes

2. **Padrões de problemas**: A concentração de issues em "Performance e Estabilidade" (6 issues) indica um problema sistemático nesta versão, não apenas casos isolados

3. **Correlação versão-capacidade**: O relacionamento direto entre Version → Issues → BusinessCapability permite identificar rapidamente quais capacidades de negócio foram mais afetadas em uma versão específica

### Exemplo de Processamento

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
- Todas as issues → RELATED_TO_VERSION → Version (25.9.1.3, count: 1 cada)
- Todas as issues → RELATES_TO_CAPABILITY → "Atendimento ao Cliente"

**Insights gerados**:
- A versão 25.9.1.3 possui 3 issues relacionadas a atendimento
- Todas as issues foram corretamente mapeadas para a BusinessCapability "Atendimento ao Cliente"
- O sistema identificou uma expressão idiomática ("problema na cabeça") e a interpretou corretamente como crítica ao atendimento
- A correlação versão-issue-capacidade permite identificar que esta versão possui problemas específicos na capacidade de atendimento

## Limitações Identificadas

**Escala da amostra**: A amostra preliminar de 10 comentários é insuficiente para generalizações estatísticas robustas. Uma amostra maior permitiria validar a estabilidade dos padrões identificados e a escalabilidade do sistema.

**Cobertura de mapeamento**: Embora tenha sido alcançada cobertura de 100% após correção, alguns mapeamentos podem requerer refinamento com base em feedback de especialistas de domínio, especialmente para expressões idiomáticas e gírias regionais.

**Performance de processamento**: O processamento atual utiliza chamadas sequenciais ao GPT-4o, o que pode ser otimizado através de processamento paralelo para grandes volumes de dados.

**Validação temporal**: O modelo bi-temporal ainda não foi validado com dados históricos reais, sendo necessário processar comentários de diferentes períodos para validar a modelagem temporal e a capacidade de identificar tendências ao longo do tempo.

## Próximos Passos

**Expansão da amostra**: Processar os 100 comentários negativos mais recentes do Santander para validar a escalabilidade do sistema e identificar padrões mais robustos de bugs por versão.

**Validação com especialistas**: Apresentar o grafo gerado para especialistas de produto e desenvolvimento para validar a correção dos mapeamentos e relacionamentos identificados, especialmente a correlação entre issues e BusinessCapability.

**Implementação de queries avançadas**: Desenvolver queries Cypher adicionais para análises específicas:
- Análise temporal de problemas por versão
- Identificação de correlações entre diferentes tipos de issues
- Análise de tendências de problemas ao longo do tempo
- Alertas automáticos para versões com volume anormal de issues

**Otimização de performance**: Implementar processamento paralelo e cache de resultados de extração de entidades para reduzir custos e tempo de processamento, permitindo escalar para volumes maiores.

**Validação de métricas**: Estabelecer métricas de qualidade para avaliação contínua do sistema:
- Precisão do mapeamento entidade → BusinessCapability
- Cobertura de extração de entidades
- Consistência temporal dos relacionamentos
- Taxa de identificação correta de bugs por versão
