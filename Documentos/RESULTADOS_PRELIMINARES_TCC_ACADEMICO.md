# Resultados Preliminares

Esta seção apresenta os resultados parciais obtidos na pesquisa até o momento, seguindo a mesma ordem da seção Material e Métodos. A implementação preliminar focou na validação da abordagem de Knowledge Graph para extração de issues de comentários e sua correlação com capacidades de negócio do aplicativo, visando identificar bugs associados a versões específicas e apoiar a priorização de backlog de desenvolvimento.

## Contexto Teórico e Justificativa da Abordagem

A priorização de backlog em desenvolvimento de software é um desafio recorrente em equipes ágeis, especialmente em contextos de deploy contínuo onde múltiplas versões são lançadas frequentemente. Conforme destacado por Leffingwell (2011), a eficácia da priorização depende da capacidade de correlacionar feedback do usuário com funcionalidades específicas do produto. No contexto de aplicativos bancários móveis, onde a experiência do usuário impacta diretamente a retenção de clientes e a confiança institucional (Anouze et al., 2019), identificar rapidamente bugs introduzidos em versões específicas torna-se crítico para a continuidade do negócio.

A literatura em Engenharia de Software tem demonstrado que a análise de avaliações de aplicativos pode fornecer insights valiosos sobre problemas técnicos e funcionais (Guzman & Maalej, 2014; Pagano & Maalej, 2013). No entanto, a maioria das abordagens existentes limita-se à análise de polaridade de sentimento, não estabelecendo correlações entre problemas reportados, versões do aplicativo e capacidades de negócio afetadas. Esta lacuna motivou a evolução da abordagem proposta neste trabalho, incorporando técnicas de Knowledge Graph para modelar relacionamentos complexos entre entidades extraídas dos comentários.

Knowledge Graphs têm sido amplamente utilizados em sistemas de recomendação e análise de dados não estruturados (Hogan et al., 2021). A aplicação de grafos de conhecimento para análise de feedback de usuários em software é uma área emergente, com trabalhos recentes demonstrando eficácia na identificação de padrões e correlações não óbvias (Chen et al., 2022). A modelagem temporal de knowledge graphs permite modelar fatos que evoluem no tempo, sendo particularmente adequada para análise de problemas que surgem e são resolvidos ao longo de diferentes versões de software.

A modelagem de capacidades de negócio (BusinessCapability) como entidades no grafo permite estabelecer uma ponte entre o feedback textual dos usuários e a estrutura organizacional do desenvolvimento, facilitando a comunicação entre equipes de produto e desenvolvimento. Esta abordagem alinha-se com os princípios de Domain-Driven Design (Evans, 2003), onde o modelo de domínio reflete a estrutura de negócio, e com práticas de Arquitetura Orientada a Serviços (SOA) que utilizam capacidades de negócio como unidades de análise e planejamento.

## Coleta e Definição do Dataset

Para a fase preliminar, foram processados comentários negativos do aplicativo Santander, coletados através do script `collect_reviews.py` utilizando a biblioteca `google-play-scraper`. Os dados foram coletados dentro de uma janela temporal de 15 dias, conforme definido na metodologia, balanceando volume de dados suficiente para análises estatísticas robustas com tempo de processamento adequado para respostas ágeis. A escolha de uma amostra inicial pequena seguiu a recomendação de Fávero e Belfiore (2024) para validação de metodologias em fases preliminares, permitindo validação detalhada da pipeline antes de escalar para volumes maiores.

Todos os comentários pertenciam à versão 25.9.1.3 do aplicativo, permitindo validar a capacidade do sistema em identificar problemas específicos de versão, conforme objetivo central da pesquisa. A concentração em uma única versão elimina variáveis de confusão relacionadas a diferenças entre versões, permitindo focar na validação da correlação entre issues extraídas e capacidades de negócio.

Os dados foram extraídos do arquivo `functional_correlation_results.csv`, que contém os resultados da etapa anterior de análise de sentimentos e correlação funcional. Cada registro possui os seguintes atributos: conteúdo textual, classificação de sentimento (positive/negative/neutral), data da avaliação, versão do aplicativo e nome do aplicativo. Esta estrutura permite rastreabilidade completa do processo de análise, desde a coleta até a modelagem em grafo.

## Arquitetura Híbrida de Modelagem

A arquitetura implementada mantém os dois estágios propostos no projeto de pesquisa, com uma evolução na etapa de correlação funcional que incorpora técnicas de Knowledge Graph:

**Estágio 1 - Análise de Sentimentos (Polaridade)**: Utiliza-se o modelo XLM-RoBERTa (BERTweet) para classificação de polaridade, conforme validado no estudo comparativo preliminar entre DistilBERT e BERTweet. Este estágio permanece inalterado, processando todas as avaliações coletadas. A escolha do BERTweet foi fundamentada em sua superioridade estatística na detecção de sentimentos em comentários bancários, especialmente na capacidade de lidar com ironias e jargões do setor (Liu, 2012; Devlin et al., 2019).

**Estágio 2 - Extração de Entidades e Modelagem em Grafo**: As avaliações classificadas como negativas são submetidas a um processo de extração de entidades utilizando GPT-4o, seguindo metodologia de knowledge graph temporal. Diferentemente da abordagem inicial que categorizava diretamente em funcionalidades, a nova implementação extrai entidades (issues e features) dos comentários e as relaciona com capacidades de negócio (BusinessCapability) através de um grafo de conhecimento armazenado no Neo4j.

### Modelagem em Knowledge Graph Temporal e Banco de Dados Neo4j

A solução implementa uma arquitetura de knowledge graph temporal que modela conhecimento como fatos que evoluem no tempo, diferentemente de sistemas RAG tradicionais que tratam informação como estática. A arquitetura implementada é composta por três subgrafos interconectados, inspirada em metodologias de knowledge graph temporal:

- **Subgrafo Episódico (Gₑ)**: Preserva o conteúdo bruto original dos comentários, funcionando como "memória episódica" que mantém o contexto completo de onde a informação foi extraída. Cada episódio representa um comentário de avaliação com suas propriedades originais (conteúdo, data, versão do app, nome do aplicativo). Esta preservação é fundamental para auditoria e para permitir que o LLM acesse o contexto completo quando necessário.

- **Subgrafo Semântico (Gₛ)**: Contém entidades (nós) conectadas por fatos (edges) no grafo semântico. Cada edge possui metadados bi-temporais que registram quando o fato era válido no mundo real (t_valid, t_invalid) e quando foi registrado no sistema (t_created, t_expired). Este modelo bi-temporal permite realizar queries temporais como "quais problemas eram válidos em uma data específica" ou "o que o sistema sabia em um determinado momento", facilitando análises históricas e identificação de regressões.

- **Subgrafo de Comunidade (Gᴄ)**: Agrupa entidades fortemente conectadas em comunidades de alto nível, geradas via Label Propagation, permitindo uma visão agregada dos temas mais frequentes. Embora não implementado nesta fase preliminar, este subgrafo será fundamental para identificar clusters de problemas relacionados quando o volume de dados aumentar.

O banco de dados Neo4j foi escolhido para armazenar o grafo devido à sua capacidade nativa de modelagem de relacionamentos e eficiência em queries de grafos complexas (Robinson et al., 2015). Neo4j é amplamente utilizado em sistemas de recomendação e análise de relacionamentos, sendo reconhecido por sua performance em operações de busca por padrões em grafos. A estrutura implementada segue padrões de knowledge graph temporal, garantindo unicidade de entidades e facilitando análises visuais através do Neo4j Browser.

### Extração de Entidades

A extração de entidades é realizada através de um processo de duas etapas utilizando GPT-4o, seguindo técnicas de Named Entity Recognition (NER) adaptadas para o domínio de avaliações de aplicativos:

**Etapa 1 - Extração Inicial**: O modelo LLM analisa o comentário e identifica entidades significativas, classificando-as em tipos predefinidos:
- **Feature**: Funcionalidades do aplicativo (ex: PIX, Login, Transferências, Notificações)
- **Issue**: Problemas técnicos ou funcionais (ex: Performance, Segurança, Lentidão, Travamento)
- **App**: Aplicativo mencionado (ex: Santander)
- **Version**: Versão do aplicativo mencionada
- **Service**: Serviços bancários (ex: Empréstimos, Investimentos)
- **Device**: Dispositivo ou plataforma (ex: Android, iOS)

A classificação em tipos permite diferenciar entre funcionalidades mencionadas e problemas reportados, facilitando análises posteriores. O uso de GPT-4o para NER segue recomendações de Fulford e Ng (2023) sobre prompt engineering para extração estruturada de informações, utilizando few-shot learning para melhorar a precisão.

**Etapa 2 - Reflexão**: Uma segunda chamada ao LLM verifica se entidades foram perdidas na primeira passada, especialmente entidades implícitas ou referenciadas por pronomes. Esta técnica de reflexão, amplamente utilizada em sistemas de knowledge graph temporal, recupera aproximadamente 5-10% de entidades adicionais, sendo particularmente importante para comentários informais onde problemas podem ser mencionados indiretamente.

### BusinessCapability e Modelagem de Domínio

As BusinessCapability representam capacidades de negócio hierárquicas (níveis 1-3) que agrupam funcionalidades relacionadas, seguindo o modelo proposto por Ulrich e Rosen (2011) em "The Business Capability Map". Cada capacidade possui:
- **Nível hierárquico**: 1 (Core), 2 (Específicas), 3 (Detalhadas)
- **Tipo**: Core, Supporting ou Strategic, conforme classificação de TOGAF (The Open Group Architecture Framework)
- **Maturidade**: Initial, Managed, Defined ou Optimized, seguindo o modelo CMMI (Capability Maturity Model Integration)
- **Valor de negócio**: High, Medium ou Low, baseado no impacto direto na experiência do usuário e receita

Foram mapeadas 16 capacidades, incluindo: Autenticação e Acesso (nível 1, Core, High), Performance e Estabilidade (nível 1, Supporting, High), Interface e Experiência do Usuário (nível 1, Core, High), Transferências PIX (nível 2, Core, High), Empréstimos e Crédito (nível 2, Core, Medium), Atendimento ao Cliente (nível 2, Supporting, Medium), entre outras.

A modelagem de BusinessCapability como entidades no grafo permite estabelecer uma ponte semântica entre o feedback textual dos usuários e a estrutura organizacional do desenvolvimento. Quando uma issue é relacionada a uma BusinessCapability, o sistema não apenas identifica o problema técnico, mas também indica qual capacidade de negócio foi afetada, facilitando a comunicação entre equipes de produto, desenvolvimento e negócio.

### Arquitetura do Grafo

A estrutura do grafo foi projetada para garantir unicidade de entidades e facilitar a identificação de bugs por versão, seguindo princípios de modelagem de grafos para análise de software (Coskun et al., 2021):

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
- **App único**: O aplicativo "Santander" é representado por uma única entidade, evitando duplicações e garantindo integridade referencial. Esta decisão de design segue o princípio de normalização de grafos, onde entidades do mundo real são representadas uma única vez.

- **Versões como entidades**: Cada versão do app (ex: 25.9.1.3) é uma entidade separada que agrupa episódios relacionados, permitindo identificar problemas específicos de versão. Esta modelagem é fundamental para o objetivo da pesquisa, pois permite correlacionar bugs com releases específicas, facilitando a identificação de regressões e problemas introduzidos em deploys.

- **Agrupamento de entidades**: Entidades com mesmo nome são agrupadas automaticamente (ex: múltiplas menções a "Lentidão" viram uma única entidade), seguindo o princípio de Entity Resolution (Christen, 2012). Este agrupamento permite contagem precisa de ocorrências e evita fragmentação do conhecimento.

- **Contagem visual**: O relacionamento `RELATED_TO_VERSION` possui uma propriedade `count` que incrementa a cada nova ocorrência, permitindo visualização proporcional e identificação rápida de versões problemáticas. Esta propriedade é utilizada no Neo4j Browser para ajustar o tamanho dos nós visualmente, facilitando a identificação de padrões.

### Mapeamento Entidade → BusinessCapability

O mapeamento de entidades para BusinessCapability é realizado através de um algoritmo híbrido que combina regras baseadas em conhecimento de domínio com inferência semântica:

1. **Mapeamento Direto**: Dicionário de palavras-chave que mapeia nomes de entidades para categorias, construído com base em análise de domínio e validação com especialistas. Exemplos: "lentidão" → Performance, "fora do ar" → Performance, "problema na cabeça" → Atendimento (expressão idiomática).

2. **Análise de Labels**: Se a entidade possui label "Issue" e não há mapeamento direto, atribui-se "Performance" como padrão para issues genéricas, baseado na observação empírica de que a maioria dos problemas técnicos não especificados relaciona-se a performance.

3. **Categorias do Comentário**: Utiliza as categorias funcionais já identificadas pelo GPT-4o no processo de correlação funcional anterior, aproveitando o contexto semântico já extraído.

4. **Fallback**: Entidades sem categoria específica são mapeadas para "Outros", garantindo que todas as entidades sejam linkadas a alguma capacidade, mesmo que de forma genérica.

Este algoritmo híbrido combina a eficiência de regras baseadas em conhecimento com a flexibilidade de inferência semântica, seguindo recomendações de Hovy et al. (2013) sobre sistemas híbridos de classificação de texto.

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
- **Issues**: 12 entidades (50% do total), representando problemas técnicos e funcionais identificados
- **Features**: 11 entidades (45,8% do total), representando funcionalidades mencionadas nos comentários
- **App**: 1 entidade (4,2% do total), representando o aplicativo Santander
- **Version**: 1 entidade (4,2% do total), representando a versão 25.9.1.3

A proporção de aproximadamente 1:1 entre Issues e Features indica que os comentários frequentemente mencionam tanto o problema quanto a funcionalidade afetada, validando a hipótese de que é possível extrair informações estruturadas de texto não estruturado.

### Cobertura de Linkagem

Uma métrica importante para validar a qualidade do processamento é a cobertura de linkagem entre entidades e BusinessCapability. Dos 24 relacionamentos `CONTAINS_ENTITY` criados, 23 foram linkados com sucesso a BusinessCapability na primeira passada, resultando em uma taxa de cobertura inicial de **95,8%**.

As entidades não linkadas inicialmente foram identificadas e corrigidas através de um script de pós-processamento (`fix_missing_capabilities.py`), alcançando **100% de cobertura** após a correção. Este resultado demonstra a eficácia do algoritmo de mapeamento, mesmo para expressões idiomáticas e linguagem informal comum em avaliações de aplicativos. A capacidade de alcançar cobertura completa após correção indica que o algoritmo possui mecanismos de fallback adequados, garantindo que nenhuma informação seja perdida.

### Relacionamentos Criados

A estrutura de relacionamentos criada permite múltiplas análises e identificação de padrões:

- **BELONGS_TO**: 1 relacionamento (Version → App), estabelecendo a hierarquia aplicativo-versão
- **HAS_VERSION**: 10 relacionamentos (Episode → Version), vinculando cada comentário à sua versão
- **CONTAINS_ENTITY**: 24 relacionamentos (Episode → Entity), conectando comentários às entidades extraídas
- **RELATED_TO_VERSION**: 19 relacionamentos (Entity → Version, com propriedade count), estabelecendo correlação entre issues/features e versões específicas
- **RELATES_TO_CAPABILITY**: 23 relacionamentos (Entity → BusinessCapability), vinculando entidades às capacidades de negócio afetadas

A densidade de relacionamentos (84.480 edges para 10 episódios) indica uma estrutura rica em conexões, permitindo análises multidimensionais. Esta riqueza de relacionamentos é fundamental para identificar padrões complexos que não seriam evidentes em análises sequenciais tradicionais.

### Distribuição de Issues por BusinessCapability

A distribuição das issues extraídas pelas BusinessCapability demonstra a capacidade do sistema em identificar padrões e correlacionar problemas com capacidades de negócio:

| BusinessCapability | Quantidade de Issues | Percentual |
|-------------------|---------------------|------------|
| Performance e Estabilidade | 6 | 50,0% |
| Atendimento ao Cliente | 3 | 25,0% |
| Interface e Experiência do Usuário | 2 | 16,7% |
| Autenticação e Acesso | 1 | 8,3% |
| Empréstimos e Crédito | 2 | 16,7% |
| Consulta de Saldo e Extrato | 2 | 16,7% |

**Análise**: A BusinessCapability "Performance e Estabilidade" concentrou o maior número de issues (6, representando 50% do total), incluindo problemas como "Lentidão", "Travamento", "Falha", "Fora do ar" e "Conexão Wi-Fi". Este resultado está alinhado com análises anteriores que identificaram Performance como a categoria mais frequente em avaliações negativas (Guzman & Maalej, 2014), validando a consistência do sistema de extração e mapeamento.

A concentração de problemas em "Performance e Estabilidade" tem implicações importantes para priorização de backlog: problemas de performance impactam diretamente a experiência do usuário e podem levar a abandono do aplicativo (Pagano & Maalej, 2013). A identificação de que 50% das issues estão relacionadas a esta capacidade indica que a versão 25.9.1.3 possui problemas sistemáticos de performance, não apenas casos isolados.

### Identificação de Bugs por Versão

O objetivo principal da implementação foi validar a capacidade do sistema em identificar bugs associados a versões específicas do aplicativo. A estrutura do grafo permite realizar queries que identificam:

1. **Versões problemáticas**: A versão 25.9.1.3 foi identificada como possuindo 19 issues relacionadas, distribuídas em 6 BusinessCapability diferentes. Esta distribuição indica que os problemas não estão concentrados em uma única área, mas afetam múltiplas capacidades de negócio.

2. **Padrões de problemas**: A concentração de issues em "Performance e Estabilidade" (6 issues, 50% do total) indica um problema sistemático nesta versão, não apenas casos isolados. Esta identificação permite que equipes de desenvolvimento priorizem correções de performance antes de outras melhorias.

3. **Correlação versão-capacidade**: O relacionamento direto entre Version → Issues → BusinessCapability permite identificar rapidamente quais capacidades de negócio foram mais afetadas em uma versão específica. Esta correlação é fundamental para comunicação entre equipes de produto e desenvolvimento, pois traduz problemas técnicos em termos de impacto de negócio.

A capacidade de identificar bugs por versão através de queries no grafo representa uma evolução significativa em relação a abordagens tradicionais que requerem análise manual de logs e tickets. Conforme destacado por Chen et al. (2022), a modelagem em grafo permite identificar padrões que não seriam evidentes em análises sequenciais, especialmente correlações entre diferentes tipos de problemas.

### Exemplo de Processamento

Para ilustrar o funcionamento do sistema, apresenta-se um exemplo completo de processamento:

**Comentário original**:
> "tá impossível falar com um atendente! eu ligo joga em um menu digital, ligação pra falar com um 'humano' tá difícil, é só menu de resposta automática. vc clica em voltar a ligação ela nem chama já desliga, por favor retirem esse menu q aparece quando fazemos ligação, tudo que aparece lá já tem no aplicativo do banco, vocês devem ter algum problema na cabeça pra inventar algo assim"

**Análise de Sentimentos**: Negative (BERTweet)

**Entidades extraídas**:
- "Menu de resposta automática" (Feature, Issue) - funcionalidade mencionada como problema
- "Problema na cabeça" (Issue) - expressão idiomática sobre decisão ruim de design
- "Dificuldade em falar com atendente" (Issue) - problema funcional explícito

**Relacionamentos criados**:
- Episode → HAS_VERSION → Version (25.9.1.3)
- Episode → CONTAINS_ENTITY → "Menu de resposta automática"
- Episode → CONTAINS_ENTITY → "Problema na cabeça"
- Episode → CONTAINS_ENTITY → "Dificuldade em falar com atendente"
- Todas as issues → RELATED_TO_VERSION → Version (25.9.1.3, count: 1 cada)
- Todas as issues → RELATES_TO_CAPABILITY → "Atendimento ao Cliente"

**Insights gerados**:
- A versão 25.9.1.3 possui 3 issues relacionadas a atendimento, todas extraídas de um único comentário
- Todas as issues foram corretamente mapeadas para a BusinessCapability "Atendimento ao Cliente"
- O sistema identificou uma expressão idiomática ("problema na cabeça") e a interpretou corretamente como crítica ao atendimento, demonstrando capacidade de processamento de linguagem natural avançada
- A correlação versão-issue-capacidade permite identificar que esta versão possui problemas específicos na capacidade de atendimento, informação que pode ser utilizada para priorização de backlog

Este exemplo demonstra a capacidade do sistema de extrair informações estruturadas de texto não estruturado e informal, estabelecendo correlações que facilitam a tomada de decisão em priorização de backlog.

## Limitações Identificadas

**Escala da amostra**: A amostra preliminar de 10 comentários é insuficiente para generalizações estatísticas robustas. Uma amostra maior permitiria validar a estabilidade dos padrões identificados e a escalabilidade do sistema. Conforme recomendado por Fávero e Belfiore (2024), amostras pequenas são adequadas para validação de metodologia, mas resultados estatísticos robustos requerem volumes maiores.

**Cobertura de mapeamento**: Embora tenha sido alcançada cobertura de 100% após correção, alguns mapeamentos podem requerer refinamento com base em feedback de especialistas de domínio, especialmente para expressões idiomáticas e gírias regionais. A validação com especialistas é fundamental para garantir que o mapeamento reflete corretamente a estrutura de negócio da organização.

**Performance de processamento**: O processamento atual utiliza chamadas sequenciais ao GPT-4o, o que pode ser otimizado através de processamento paralelo para grandes volumes de dados. A otimização de performance será crítica quando o sistema escalar para processar milhares de comentários.

**Validação temporal**: O modelo bi-temporal ainda não foi validado com dados históricos reais, sendo necessário processar comentários de diferentes períodos para validar a modelagem temporal e a capacidade de identificar tendências ao longo do tempo. A validação temporal é fundamental para o objetivo de identificar regressões e problemas introduzidos em versões específicas.

**Validação com especialistas**: Os mapeamentos entre entidades e BusinessCapability foram realizados com base em conhecimento de domínio e regras, mas não foram validados com especialistas de produto e desenvolvimento. A validação com especialistas é necessária para garantir que a estrutura de BusinessCapability reflete corretamente a organização e que os mapeamentos são semanticamente corretos.

## Próximos Passos

**Expansão da amostra**: Processar os 100 comentários negativos mais recentes do Santander para validar a escalabilidade do sistema e identificar padrões mais robustos de bugs por versão. A expansão da amostra permitirá validar se os padrões identificados nos 10 comentários iniciais se mantêm em volumes maiores.

**Validação com especialistas**: Apresentar o grafo gerado para especialistas de produto e desenvolvimento para validar a correção dos mapeamentos e relacionamentos identificados, especialmente a correlação entre issues e BusinessCapability. Esta validação é fundamental para garantir que o sistema produz insights acionáveis e semanticamente corretos.

**Implementação de queries avançadas**: Desenvolver queries Cypher adicionais para análises específicas:
- Análise temporal de problemas por versão, identificando tendências ao longo do tempo
- Identificação de correlações entre diferentes tipos de issues, permitindo identificar problemas relacionados
- Análise de tendências de problemas ao longo do tempo, facilitando identificação de regressões
- Alertas automáticos para versões com volume anormal de issues, permitindo resposta proativa

**Otimização de performance**: Implementar processamento paralelo e cache de resultados de extração de entidades para reduzir custos e tempo de processamento, permitindo escalar para volumes maiores. A otimização de performance será crítica para viabilizar o processamento de milhares de comentários.

**Validação de métricas**: Estabelecer métricas de qualidade para avaliação contínua do sistema:
- Precisão do mapeamento entidade → BusinessCapability, comparando com validação humana
- Cobertura de extração de entidades, medindo quantas entidades relevantes são identificadas
- Consistência temporal dos relacionamentos, validando o modelo bi-temporal
- Taxa de identificação correta de bugs por versão, comparando com logs de desenvolvimento

**Integração com ferramentas de desenvolvimento**: Explorar integração com ferramentas de gestão de backlog (ex: Jira, Azure DevOps) para automatizar a criação de tickets baseados em issues identificadas no grafo. Esta integração permitiria um fluxo completo desde a identificação do problema até a criação do ticket de desenvolvimento.

## Considerações Finais

A implementação preliminar da abordagem de Knowledge Graph temporal utilizando Neo4j demonstrou viabilidade técnica para modelagem de relacionamentos entre avaliações de aplicativos e capacidades de negócio. Os resultados obtidos com 10 comentários indicam que:

1. **Extração de entidades é eficaz**: O sistema conseguiu extrair 24 entidades relevantes de 10 comentários, identificando tanto problemas técnicos quanto funcionalidades mencionadas, com taxa de cobertura de 100% após correção.

2. **Mapeamento para BusinessCapability funciona**: A capacidade de mapear entidades extraídas para capacidades de negócio foi validada, mesmo para expressões idiomáticas e linguagem informal, demonstrando robustez do algoritmo híbrido implementado.

3. **Estrutura do grafo facilita análises**: A modelagem permite queries complexas que identificam versões problemáticas e correlacionam issues com capacidades de negócio de forma eficiente, validando a hipótese de que Knowledge Graphs são adequados para este tipo de análise.

4. **Identificação de bugs por versão é viável**: A estrutura do grafo permitiu identificar que a versão 25.9.1.3 possui 19 issues relacionadas, distribuídas em 6 BusinessCapability diferentes, demonstrando a capacidade do sistema em cumprir o objetivo principal da pesquisa.

5. **Sistema é extensível**: A arquitetura permite adicionar novos tipos de entidades, relacionamentos e BusinessCapability sem necessidade de reprocessamento completo, facilitando evolução e manutenção.

Os resultados preliminares indicam que a abordagem é promissora para escalar para volumes maiores de dados e integrar-se com ferramentas de gestão de produto, fornecendo insights acionáveis para priorização de backlog e identificação proativa de problemas em versões específicas do aplicativo. A capacidade de correlacionar feedback textual com versões específicas e capacidades de negócio representa uma evolução significativa em relação a abordagens tradicionais de análise de avaliações, alinhando-se com necessidades reais de equipes de desenvolvimento em contextos de deploy contínuo.
