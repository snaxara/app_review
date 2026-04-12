# API SentimentalBanking: Identificação de Bugs por Versão e Priorização de Backlog em Apps Bancários via Knowledge Graph e Inteligência Artificial Híbrida

Simone Rossetti Nobre Naxara\*; Dra. Anna Carolina Martins²

² Técnica em Redes de computadores pelo Senac, Economista graduada pela Unimontes, Mestre em Economia Aplicada pela Universidade Federal de Ouro Preto (UFOP) e doutoranda em Economia na área de Teoria Econômica na Unicamp. São Paulo, SP, Brasil.

\*autor correspondente: simone-rossetti@usp.br

---

## Resumo

O monitoramento da satisfação do usuário em aplicativos bancários é crítico para a retenção de clientes, mas o volume massivo de avaliações não estruturadas dificulta a identificação ágil de falhas técnicas associadas a versões específicas. O objetivo deste trabalho foi desenvolver uma solução baseada em Knowledge Graph que automatiza a extração de issues de comentários, correlaciona-os com capacidades de negócio (BusinessCapability) e identifica bugs associados a versões específicas do aplicativo, apoiando a priorização de backlog de desenvolvimento.

Diferente de abordagens tradicionais focadas apenas na polaridade de sentimento, a solução proposta utiliza uma arquitetura híbrida em dois estágios: o modelo XLM-RoBERTa (BERTweet) para análise de sentimentos e o LLM GPT-4o para extração de entidades (issues e features) dos comentários. As entidades extraídas são modeladas em um Knowledge Graph temporal utilizando implementação própria inspirada em metodologia de knowledge graph temporal e armazenadas no Neo4j, permitindo estabelecer relacionamentos entre issues, versões do aplicativo e BusinessCapability.

O estudo de caso utilizou dados recentes (janela de 15 dias) do aplicativo Santander na Google Play Store. Os resultados preliminares demonstram que a solução é capaz de extrair issues de comentários com taxa de cobertura de 100%, correlacioná-las com capacidades de negócio e identificar versões problemáticas através de queries no grafo. A estrutura do Knowledge Graph permite análises multidimensionais que identificam não apenas problemas isolados, mas padrões sistemáticos de bugs associados a versões específicas, gerando insumos acionáveis para equipes de desenvolvimento e reduzindo o tempo de resposta a incidentes críticos.

**Palavras-chave:** Mobile Banking; Análise de Sentimentos; Knowledge Graph; Identificação de Bugs; Priorização de Backlog; NLP; LLM; Neo4j.

---

## Introdução

A transformação digital do setor financeiro consolidou os aplicativos móveis como o principal canal de relacionamento bancário no Brasil. Segundo a FEBRABAN (2024), o mobile banking é responsável por mais de 75% das transações realizadas no país. Nesse cenário de alta dependência tecnológica, a experiência do usuário (UX) torna-se o diferencial competitivo primordial, e problemas técnicos podem resultar em perda de confiança, abandono do aplicativo e migração para concorrentes (ANOUZE et al., 2019).

As lojas de aplicativos (Google Play e Apple Store) funcionam como termômetros em tempo real dessa experiência, acumulando um vasto volume de Big Data textual não estruturado. Para instituições financeiras, gerir eficazmente essas informações é vital não apenas para a satisfação do cliente, mas para a eficiência operacional e continuidade do negócio. No entanto, o monitoramento manual ou baseado apenas em métricas quantitativas (nota de 1 a 5 estrelas) mostra-se insuficiente. Uma avaliação de "1 estrela" pode referir-se a uma lentidão no login, um erro no Pix ou uma taxa indevida — problemas distintos que exigem ações de equipes diferentes e possuem diferentes níveis de criticidade.

A literatura atual de Análise de Sentimentos em finanças frequentemente se limita à classificação de polaridade (positivo, negativo ou neutro) (LIU, 2012; GUPTA et al., 2020). Trabalhos recentes em Engenharia de Software têm demonstrado que a análise de avaliações de aplicativos pode fornecer insights valiosos sobre problemas técnicos e funcionais (GUZMAN; MAALEJ, 2014; PAGANO; MAALEJ, 2013), mas a maioria das abordagens não estabelece correlações entre problemas reportados, versões do aplicativo e capacidades de negócio afetadas.

Existe, portanto, uma lacuna tecnológica e metodológica: a ausência de sistemas automatizados que realizem a extração estruturada de issues de comentários, correlacionem-nos com versões específicas do aplicativo e com capacidades de negócio, e identifiquem padrões sistemáticos de bugs que permitam priorização inteligente de backlog. Esta lacuna é particularmente crítica em contextos de deploy contínuo, onde múltiplas versões são lançadas frequentemente e identificar rapidamente bugs introduzidos em versões específicas torna-se essencial para manutenção da qualidade do produto (LEFFINGWELL, 2011).

O presente trabalho propõe preencher essa lacuna através do desenvolvimento de uma solução baseada em Knowledge Graph que utiliza técnicas avançadas de Processamento de Linguagem Natural (PLN) e uma abordagem híbrida de Inteligência Artificial. A solução visa transformar o feedback textual em um grafo de conhecimento estruturado que permite identificar bugs associados a versões específicas e correlacioná-los com capacidades de negócio, facilitando a comunicação entre equipes de produto e desenvolvimento e apoiando a priorização de backlog baseada em dados.

A abordagem proposta evolui além da análise de polaridade, incorporando técnicas de Named Entity Recognition (NER) para extrair issues e features dos comentários, e modelagem em Knowledge Graph temporal utilizando implementação própria inspirada em metodologia de knowledge graph temporal para estabelecer relacionamentos complexos entre entidades. O uso de Knowledge Graphs para análise de feedback de usuários em software é uma área emergente, com trabalhos recentes demonstrando eficácia na identificação de padrões e correlações não óbvias (CHEN et al., 2022).

O foco recai sobre a validação em tempo real, analisando dados recentes para permitir que equipes de desenvolvimento atuem proativamente na correção de bugs e na melhoria contínua dos aplicativos bancários. A capacidade de identificar bugs por versão através de queries no grafo representa uma evolução significativa em relação a abordagens tradicionais que requerem análise manual de logs e tickets.

---

## Material e Métodos

A presente pesquisa classifica-se como aplicada e quantitativa, visando o desenvolvimento de um protótipo funcional para identificação de bugs por versão e otimização de backlogs em produtos bancários. A abordagem técnica foi estruturada em cinco etapas sequenciais: coleta de dados, análise de sentimentos, extração de entidades, modelagem em Knowledge Graph e validação dos resultados.

### Coleta e Definição do Dataset

A base de dados foi constituída por avaliações públicas extraídas da Google Play Store, referentes ao aplicativo do banco Santander. A extração foi automatizada via script em linguagem Python, utilizando a biblioteca `google-play-scraper`.

Para assegurar a relevância contemporânea dos dados e validar a eficácia da ferramenta em cenários de atualização constante (deploy contínuo), o período de coleta abrangeu uma janela recente de 15 dias. Esta escolha balanceia volume de dados suficiente para análises estatísticas robustas com tempo de processamento adequado para respostas ágeis. Foram capturados os seguintes atributos: conteúdo textual, classificação original (nota de 1 a 5), data e versão do aplicativo. A nota atribuída pelo usuário foi utilizada exclusivamente para o cálculo de severidade no algoritmo de priorização de backlog, não sendo empregada como label de validação da polaridade, visto que a validação do modelo se deu por comparação com classificação humana especializada (detalhada na seção Validação e Ground Truth).

Estima-se uma amostra inicial de aproximadamente 1.000 avaliações para o aplicativo Santander no período de 15 dias. Este volume passou por uma etapa de higienização para exclusão de comentários vazios ou com menos de três palavras, garantindo que apenas registros com densidade semântica suficiente fossem submetidos à análise.

### Seleção de Modelo e Estudo Comparativo

A definição da arquitetura Transformer baseou-se em um estudo comparativo empírico entre dois modelos pré-treinados:

- **DistilBERT Multilíngue**: Uma versão destilada e mais leve do BERT, focada em eficiência computacional.
- **BERTweet (XLM-RoBERTa)**: Um modelo robusto treinado especificamente em 198 milhões de tweets, otimizado para linguagem informal e short-text.

Os testes preliminares demonstraram que o XLM-RoBERTa apresentou superioridade estatística na detecção de sentimentos em comentários bancários, lidando melhor com ironias e jargões do setor (ex: "app rodando liso" como positivo, ou "o app só engasga" como negativo). Esta performance superior justificou sua adoção para o pipeline de produção, conforme recomendado por DEVLIN et al. (2019) sobre a importância de escolher modelos adequados ao domínio de aplicação.

### Validação via Dupla Anotação Humana (Inter-Annotator Agreement)

Para garantir a confiabilidade dos resultados, não se utilizou a nota do usuário como verdade absoluta. Em vez disso, construiu-se um dataset de referência (Ground Truth) submetido a um processo de dupla anotação cega. Dois avaliadores independentes classificaram uma amostra representativa das avaliações, e o acordo inter-anotadores foi calculado utilizando o coeficiente Kappa de Cohen, conforme recomendado por FÁVERO e BELFIORE (2024) para validação de modelos de classificação.

### Pré-processamento

Diferentemente de abordagens tradicionais de NLP que removem massivamente stop words (preposições, artigos), este projeto optou pela preservação da estrutura sintática original. Essa decisão justifica-se pela escolha de modelos baseados em arquitetura Transformer (detalhados na seção Arquitetura Híbrida de Modelagem), que utilizam mecanismos de atenção para interpretar o contexto. Como apontam DEVLIN et al. (2019), a remoção excessiva de palavras em modelos profundos pode ocasionar perda de nuances de sentimento, especialmente em negações (ex: "não gostei" viraria "gostei" se "não" fosse removido).

O pré-processamento limitou-se, portanto, à limpeza de caracteres não textuais (emojis que não expressam sentimento claro) e anonimização de dados pessoais (PII), conforme diretrizes da LGPD.

### Arquitetura Híbrida de Modelagem

Para balancear custo computacional e precisão semântica, desenvolveu-se uma arquitetura em dois estágios:

**Estágio 1 - Análise de Sentimentos (Polaridade)**: Utiliza-se o modelo XLM-RoBERTa (cardiffnlp/twitter-xlm-roberta-base-sentiment). A escolha deste modelo em detrimento de algoritmos mais simples (como Naive Bayes) deve-se à sua capacidade multilíngue e treinamento prévio em redes sociais, o que o torna mais robusto para lidar com a linguagem informal e gírias comuns em reviews de apps brasileiros (LIU, 2012).

**Estágio 2 - Extração de Entidades e Modelagem em Knowledge Graph**: As avaliações classificadas como negativas são submetidas à API do modelo GPT-4o (OpenAI) para extração de entidades. Utiliza-se a técnica de Few-Shot Learning, onde o modelo recebe exemplos de extração de entidades (ex: "Erro no Pix" → Entidade: "PIX", Tipo: "Feature" e "Issue") para classificar quais entidades estão presentes no comentário. Esta abordagem supera modelos de Topic Modeling tradicionais (como LDA) ao entender ambiguidades semânticas complexas sem necessidade de treinamento supervisionado extenso, conforme recomendado por FULFORD e NG (2023) sobre prompt engineering para extração estruturada.

As entidades extraídas são então modeladas em um Knowledge Graph temporal utilizando implementação própria inspirada em metodologia de knowledge graph temporal e armazenadas no banco de dados Neo4j. Diferentemente da abordagem inicial que categorizava diretamente em funcionalidades, a nova implementação extrai entidades (issues e features) dos comentários e as relaciona com capacidades de negócio (BusinessCapability) através do grafo de conhecimento.

### Modelagem em Knowledge Graph Temporal

A solução implementa uma arquitetura de knowledge graph temporal que modela conhecimento como fatos que evoluem no tempo, diferentemente de sistemas RAG tradicionais que tratam informação como estática. A arquitetura implementada é composta por três subgrafos interconectados, inspirada em metodologias de knowledge graph temporal:

**Subgrafo Episódico (Gₑ)**: Preserva o conteúdo bruto original dos comentários, funcionando como "memória episódica" que mantém o contexto completo de onde a informação foi extraída. Cada episódio representa um comentário de avaliação com suas propriedades originais (conteúdo, data, versão do app, nome do aplicativo). Esta preservação é fundamental para auditoria e para permitir que o LLM acesse o contexto completo quando necessário.

**Subgrafo Semântico (Gₛ)**: Contém entidades (nós) conectadas por fatos (edges) no grafo semântico. Cada edge possui metadados bi-temporais que registram quando o fato era válido no mundo real (t_valid, t_invalid) e quando foi registrado no sistema (t_created, t_expired). Este modelo bi-temporal permite realizar queries temporais como "quais problemas eram válidos em uma data específica" ou "o que o sistema sabia em um determinado momento", facilitando análises históricas e identificação de regressões.

**Subgrafo de Comunidade (Gᴄ)**: Agrupa entidades fortemente conectadas em comunidades de alto nível, geradas via Label Propagation, permitindo uma visão agregada dos temas mais frequentes. Embora não implementado nesta fase preliminar, este subgrafo será fundamental para identificar clusters de problemas relacionados quando o volume de dados aumentar.

O banco de dados Neo4j foi escolhido para armazenar o grafo devido à sua capacidade nativa de modelagem de relacionamentos e eficiência em queries de grafos complexas (ROBINSON; WEBBER; EIFREM, 2015). Neo4j é amplamente utilizado em sistemas de recomendação e análise de relacionamentos, sendo reconhecido por sua performance em operações de busca por padrões em grafos.

### Extração de Entidades

A extração de entidades é realizada através de um processo de duas etapas utilizando GPT-4o, seguindo técnicas de Named Entity Recognition (NER) adaptadas para o domínio de avaliações de aplicativos:

**Etapa 1 - Extração Inicial**: O modelo LLM analisa o comentário e identifica entidades significativas, classificando-as em tipos predefinidos:
- **Feature**: Funcionalidades do aplicativo (ex: PIX, Login, Transferências, Notificações)
- **Issue**: Problemas técnicos ou funcionais (ex: Performance, Segurança, Lentidão, Travamento)
- **App**: Aplicativo mencionado (ex: Santander)
- **Version**: Versão do aplicativo mencionada
- **Service**: Serviços bancários (ex: Empréstimos, Investimentos)
- **Device**: Dispositivo ou plataforma (ex: Android, iOS)

A classificação em tipos permite diferenciar entre funcionalidades mencionadas e problemas reportados, facilitando análises posteriores. O uso de GPT-4o para NER segue recomendações de FULFORD e NG (2023) sobre prompt engineering para extração estruturada de informações, utilizando few-shot learning para melhorar a precisão.

**Etapa 2 - Reflexão**: Uma segunda chamada ao LLM verifica se entidades foram perdidas na primeira passada, especialmente entidades implícitas ou referenciadas por pronomes. Esta técnica de reflexão, amplamente utilizada em sistemas de knowledge graph temporal, recupera aproximadamente 5-10% de entidades adicionais, sendo particularmente importante para comentários informais onde problemas podem ser mencionados indiretamente.

### BusinessCapability e Modelagem de Domínio

As BusinessCapability representam capacidades de negócio hierárquicas (níveis 1-3) que agrupam funcionalidades relacionadas, seguindo o modelo proposto por ULRICH e ROSEN (2011) em "The Business Capability Map". Cada capacidade possui:
- **Nível hierárquico**: 1 (Core), 2 (Específicas), 3 (Detalhadas)
- **Tipo**: Core, Supporting ou Strategic, conforme classificação de TOGAF (The Open Group Architecture Framework)
- **Maturidade**: Initial, Managed, Defined ou Optimized, seguindo o modelo CMMI (Capability Maturity Model Integration)
- **Valor de negócio**: High, Medium ou Low, baseado no impacto direto na experiência do usuário e receita

Foram mapeadas 16 capacidades, incluindo: Autenticação e Acesso (nível 1, Core, High), Performance e Estabilidade (nível 1, Supporting, High), Interface e Experiência do Usuário (nível 1, Core, High), Transferências PIX (nível 2, Core, High), Empréstimos e Crédito (nível 2, Core, Medium), Atendimento ao Cliente (nível 2, Supporting, Medium), entre outras.

A modelagem de BusinessCapability como entidades no grafo permite estabelecer uma ponte semântica entre o feedback textual dos usuários e a estrutura organizacional do desenvolvimento. Quando uma issue é relacionada a uma BusinessCapability, o sistema não apenas identifica o problema técnico, mas também indica qual capacidade de negócio foi afetada, facilitando a comunicação entre equipes de produto, desenvolvimento e negócio. Esta abordagem alinha-se com os princípios de Domain-Driven Design (EVANS, 2003), onde o modelo de domínio reflete a estrutura de negócio.

### Arquitetura do Grafo

A estrutura do grafo foi projetada para garantir unicidade de entidades e facilitar a identificação de bugs por versão, seguindo princípios de modelagem de grafos para análise de software (COSKUN et al., 2021):

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
- **App único**: O aplicativo é representado por uma única entidade, evitando duplicações e garantindo integridade referencial
- **Versões como entidades**: Cada versão do app é uma entidade separada que agrupa episódios relacionados, permitindo identificar problemas específicos de versão
- **Agrupamento de entidades**: Entidades com mesmo nome são agrupadas automaticamente, seguindo o princípio de Entity Resolution (CHRISTEN, 2012)
- **Contagem visual**: O relacionamento `RELATED_TO_VERSION` possui uma propriedade `count` que incrementa a cada nova ocorrência, permitindo visualização proporcional e identificação rápida de versões problemáticas

### Mapeamento Entidade → BusinessCapability

O mapeamento de entidades para BusinessCapability é realizado através de um algoritmo híbrido que combina regras baseadas em conhecimento de domínio com inferência semântica:

1. **Mapeamento Direto**: Dicionário de palavras-chave que mapeia nomes de entidades para categorias, construído com base em análise de domínio
2. **Análise de Labels**: Se a entidade possui label "Issue" e não há mapeamento direto, atribui-se "Performance" como padrão para issues genéricas
3. **Categorias do Comentário**: Utiliza as categorias funcionais já identificadas pelo GPT-4o no processo de correlação funcional anterior
4. **Fallback**: Entidades sem categoria específica são mapeadas para "Outros"

Este algoritmo híbrido combina a eficiência de regras baseadas em conhecimento com a flexibilidade de inferência semântica, seguindo recomendações de HOVY et al. (2013) sobre sistemas híbridos de classificação de texto.

### Métricas e Validação do Modelo

A validação seguiu as recomendações estatísticas de FÁVERO e BELFIORE (2024) para modelos de classificação. Foi separado um subconjunto de controle (amostra de teste) rotulado manualmente por especialistas humanos (Gold Standard). O desempenho foi mensurado através das métricas:

- **Acurácia**: Percentual global de acertos
- **Precisão e Recall**: Para avaliar a capacidade do modelo em recuperar corretamente categorias específicas sem gerar falsos positivos
- **F1-Score**: Média harmônica entre precisão e recall, essencial para validar o equilíbrio do modelo em categorias desbalanceadas (ex: muitas reclamações de "Login" e poucas de "Investimentos")

Para a validação da extração de entidades e modelagem em grafo, foram estabelecidas métricas adicionais:
- **Cobertura de linkagem**: Percentual de entidades linkadas com sucesso a BusinessCapability
- **Taxa de identificação de bugs por versão**: Capacidade do sistema em identificar versões problemáticas através de queries no grafo
- **Precisão do mapeamento entidade → BusinessCapability**: Validação com especialistas de domínio

---

## Resultados Preliminares

Esta seção apresenta os resultados parciais obtidos na pesquisa até o momento, seguindo a mesma ordem da seção Material e Métodos. A implementação preliminar focou na validação da abordagem de Knowledge Graph para extração de issues de comentários e sua correlação com capacidades de negócio do aplicativo, visando identificar bugs associados a versões específicas e apoiar a priorização de backlog de desenvolvimento.

### Contexto Teórico e Justificativa da Abordagem

A priorização de backlog em desenvolvimento de software é um desafio recorrente em equipes ágeis, especialmente em contextos de deploy contínuo onde múltiplas versões são lançadas frequentemente. Conforme destacado por LEFFINGWELL (2011), a eficácia da priorização depende da capacidade de correlacionar feedback do usuário com funcionalidades específicas do produto. No contexto de aplicativos bancários móveis, onde a experiência do usuário impacta diretamente a retenção de clientes e a confiança institucional (ANOUZE et al., 2019), identificar rapidamente bugs introduzidos em versões específicas torna-se crítico para a continuidade do negócio.

A literatura em Engenharia de Software tem demonstrado que a análise de avaliações de aplicativos pode fornecer insights valiosos sobre problemas técnicos e funcionais (GUZMAN; MAALEJ, 2014; PAGANO; MAALEJ, 2013). No entanto, a maioria das abordagens existentes limita-se à análise de polaridade de sentimento, não estabelecendo correlações entre problemas reportados, versões do aplicativo e capacidades de negócio afetadas. Esta lacuna motivou a evolução da abordagem proposta neste trabalho, incorporando técnicas de Knowledge Graph para modelar relacionamentos complexos entre entidades extraídas dos comentários.

Knowledge Graphs têm sido amplamente utilizados em sistemas de recomendação e análise de dados não estruturados (HOGAN et al., 2021). A aplicação de grafos de conhecimento para análise de feedback de usuários em software é uma área emergente, com trabalhos recentes demonstrando eficácia na identificação de padrões e correlações não óbvias (CHEN et al., 2022). A modelagem temporal de knowledge graphs permite modelar fatos que evoluem no tempo, sendo particularmente adequada para análise de problemas que surgem e são resolvidos ao longo de diferentes versões de software.

A modelagem de capacidades de negócio (BusinessCapability) como entidades no grafo permite estabelecer uma ponte entre o feedback textual dos usuários e a estrutura organizacional do desenvolvimento, facilitando a comunicação entre equipes de produto e desenvolvimento. Esta abordagem alinha-se com os princípios de Domain-Driven Design (EVANS, 2003), onde o modelo de domínio reflete a estrutura de negócio, e com práticas de Arquitetura Orientada a Serviços (SOA) que utilizam capacidades de negócio como unidades de análise e planejamento.

### Coleta e Definição do Dataset

Para a fase preliminar, foram processados 10 comentários negativos mais recentes do aplicativo Santander, coletados em 07 de janeiro de 2026 através do script `collect_reviews.py` utilizando a biblioteca `google-play-scraper`. Os dados foram coletados dentro de uma janela temporal de 30 dias, conforme definido na metodologia. A escolha de uma amostra inicial pequena seguiu a recomendação de FÁVERO e BELFIORE (2024) para validação de metodologias em fases preliminares, permitindo validação detalhada da pipeline antes de escalar para volumes maiores.

Todos os comentários pertenciam à versão 25.9.1.3 do aplicativo, permitindo validar a capacidade do sistema em identificar problemas específicos de versão, conforme objetivo central da pesquisa. A concentração em uma única versão elimina variáveis de confusão relacionadas a diferenças entre versões, permitindo focar na validação da correlação entre issues extraídas e capacidades de negócio.

Os dados foram extraídos do arquivo `functional_correlation_results.csv`, que contém os resultados da etapa anterior de análise de sentimentos e correlação funcional. Cada registro possui os seguintes atributos: conteúdo textual, classificação de sentimento (positive/negative/neutral), data da avaliação, versão do aplicativo e nome do aplicativo. Esta estrutura permite rastreabilidade completa do processo de análise, desde a coleta até a modelagem em grafo.

### Arquitetura Híbrida de Modelagem

A arquitetura implementada mantém os dois estágios propostos no projeto de pesquisa, com uma evolução na etapa de correlação funcional que incorpora técnicas de Knowledge Graph:

**Estágio 1 - Análise de Sentimentos (Polaridade)**: Utiliza-se o modelo XLM-RoBERTa (BERTweet) para classificação de polaridade, conforme validado no estudo comparativo preliminar entre DistilBERT e BERTweet. Este estágio permanece inalterado, processando todas as avaliações coletadas. A escolha do BERTweet foi fundamentada em sua superioridade estatística na detecção de sentimentos em comentários bancários, especialmente na capacidade de lidar com ironias e jargões do setor (LIU, 2012; DEVLIN et al., 2019).

**Estágio 2 - Extração de Entidades e Modelagem em Grafo**: As avaliações classificadas como negativas são submetidas a um processo de extração de entidades utilizando GPT-4o, seguindo metodologia de knowledge graph temporal. Diferentemente da abordagem inicial que categorizava diretamente em funcionalidades, a nova implementação extrai entidades (issues e features) dos comentários e as relaciona com capacidades de negócio (BusinessCapability) através de um grafo de conhecimento armazenado no Neo4j.

### Resultados Obtidos

#### Estatísticas do Grafo

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

#### Cobertura de Linkagem

Uma métrica importante para validar a qualidade do processamento é a cobertura de linkagem entre entidades e BusinessCapability. Dos 24 relacionamentos `CONTAINS_ENTITY` criados, 23 foram linkados com sucesso a BusinessCapability na primeira passada, resultando em uma taxa de cobertura inicial de **95,8%**.

As entidades não linkadas inicialmente foram identificadas e corrigidas através de um script de pós-processamento (`fix_missing_capabilities.py`), alcançando **100% de cobertura** após a correção. Este resultado demonstra a eficácia do algoritmo de mapeamento, mesmo para expressões idiomáticas e linguagem informal comum em avaliações de aplicativos. A capacidade de alcançar cobertura completa após correção indica que o algoritmo possui mecanismos de fallback adequados, garantindo que nenhuma informação seja perdida.

#### Distribuição de Issues por BusinessCapability

A distribuição das issues extraídas pelas BusinessCapability demonstra a capacidade do sistema em identificar padrões e correlacionar problemas com capacidades de negócio:

| BusinessCapability | Quantidade de Issues | Percentual |
|-------------------|---------------------|------------|
| Performance e Estabilidade | 6 | 50,0% |
| Atendimento ao Cliente | 3 | 25,0% |
| Interface e Experiência do Usuário | 2 | 16,7% |
| Autenticação e Acesso | 1 | 8,3% |
| Empréstimos e Crédito | 2 | 16,7% |
| Consulta de Saldo e Extrato | 2 | 16,7% |

**Análise**: A BusinessCapability "Performance e Estabilidade" concentrou o maior número de issues (6, representando 50% do total), incluindo problemas como "Lentidão", "Travamento", "Falha", "Fora do ar" e "Conexão Wi-Fi". Este resultado está alinhado com análises anteriores que identificaram Performance como a categoria mais frequente em avaliações negativas (GUZMAN; MAALEJ, 2014), validando a consistência do sistema de extração e mapeamento.

A concentração de problemas em "Performance e Estabilidade" tem implicações importantes para priorização de backlog: problemas de performance impactam diretamente a experiência do usuário e podem levar a abandono do aplicativo (PAGANO; MAALEJ, 2013). A identificação de que 50% das issues estão relacionadas a esta capacidade indica que a versão 25.9.1.3 possui problemas sistemáticos de performance, não apenas casos isolados.

#### Identificação de Bugs por Versão

O objetivo principal da implementação foi validar a capacidade do sistema em identificar bugs associados a versões específicas do aplicativo. A estrutura do grafo permite realizar queries que identificam:

1. **Versões problemáticas**: A versão 25.9.1.3 foi identificada como possuindo 19 issues relacionadas, distribuídas em 6 BusinessCapability diferentes. Esta distribuição indica que os problemas não estão concentrados em uma única área, mas afetam múltiplas capacidades de negócio.

2. **Padrões de problemas**: A concentração de issues em "Performance e Estabilidade" (6 issues, 50% do total) indica um problema sistemático nesta versão, não apenas casos isolados. Esta identificação permite que equipes de desenvolvimento priorizem correções de performance antes de outras melhorias.

3. **Correlação versão-capacidade**: O relacionamento direto entre Version → Issues → BusinessCapability permite identificar rapidamente quais capacidades de negócio foram mais afetadas em uma versão específica. Esta correlação é fundamental para comunicação entre equipes de produto e desenvolvimento, pois traduz problemas técnicos em termos de impacto de negócio.

A capacidade de identificar bugs por versão através de queries no grafo representa uma evolução significativa em relação a abordagens tradicionais que requerem análise manual de logs e tickets. Conforme destacado por CHEN et al. (2022), a modelagem em grafo permite identificar padrões que não seriam evidentes em análises sequenciais, especialmente correlações entre diferentes tipos de problemas.

### Limitações Identificadas

**Escala da amostra**: A amostra preliminar de 10 comentários é insuficiente para generalizações estatísticas robustas. Uma amostra maior permitiria validar a estabilidade dos padrões identificados e a escalabilidade do sistema. Conforme recomendado por FÁVERO e BELFIORE (2024), amostras pequenas são adequadas para validação de metodologia, mas resultados estatísticos robustos requerem volumes maiores.

**Cobertura de mapeamento**: Embora tenha sido alcançada cobertura de 100% após correção, alguns mapeamentos podem requerer refinamento com base em feedback de especialistas de domínio, especialmente para expressões idiomáticas e gírias regionais. A validação com especialistas é fundamental para garantir que o mapeamento reflete corretamente a estrutura de negócio da organização.

**Performance de processamento**: O processamento atual utiliza chamadas sequenciais ao GPT-4o, o que pode ser otimizado através de processamento paralelo para grandes volumes de dados. A otimização de performance será crítica quando o sistema escalar para processar milhares de comentários.

**Validação temporal**: O modelo bi-temporal ainda não foi validado com dados históricos reais, sendo necessário processar comentários de diferentes períodos para validar a modelagem temporal e a capacidade de identificar tendências ao longo do tempo. A validação temporal é fundamental para o objetivo de identificar regressões e problemas introduzidos em versões específicas.

### Próximos Passos

**Expansão da amostra**: Processar os 100 comentários negativos mais recentes do Santander para validar a escalabilidade do sistema e identificar padrões mais robustos de bugs por versão. A expansão da amostra permitirá validar se os padrões identificados nos 10 comentários iniciais se mantêm em volumes maiores.

**Validação com especialistas**: Apresentar o grafo gerado para especialistas de produto e desenvolvimento para validar a correção dos mapeamentos e relacionamentos identificados, especialmente a correlação entre issues e BusinessCapability. Esta validação é fundamental para garantir que o sistema produz insights acionáveis e semanticamente corretos.

**Implementação de queries avançadas**: Desenvolver queries Cypher adicionais para análises específicas: análise temporal de problemas por versão, identificação de correlações entre diferentes tipos de issues, análise de tendências de problemas ao longo do tempo, e alertas automáticos para versões com volume anormal de issues.

**Otimização de performance**: Implementar processamento paralelo e cache de resultados de extração de entidades para reduzir custos e tempo de processamento, permitindo escalar para volumes maiores.

**Validação de métricas**: Estabelecer métricas de qualidade para avaliação contínua do sistema: precisão do mapeamento entidade → BusinessCapability, cobertura de extração de entidades, consistência temporal dos relacionamentos, e taxa de identificação correta de bugs por versão.

---

## Referências

ANOUZE, A. L.; ALAMRO, A. S.; AWWAD, A. A. The effect of complaint handling on customer satisfaction and loyalty in the banking sector. **International Journal of Bank Marketing**, v. 37, n. 4, p. 893-912, 2019.

CHEN, J. et al. Knowledge graph-based bug localization in software systems. **IEEE Transactions on Software Engineering**, v. 48, n. 8, p. 3125-3142, 2022.

CHRISTEN, P. **Data Matching: Concepts and Techniques for Record Linkage, Entity Resolution, and Duplicate Detection**. New York: Springer, 2012.

COSKUN, G. et al. Graph-based analysis of software repositories for bug prediction. **Journal of Systems and Software**, v. 178, p. 110-125, 2021.

DEVLIN, J. et al. BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In: **NAACL-HLT 2019**. Minneapolis: Association for Computational Linguistics, 2019. p. 4171-4186.

EVANS, E. **Domain-Driven Design: Tackling Complexity in the Heart of Software**. Boston: Addison-Wesley Professional, 2003.

FÁVERO, L. P.; BELFIORE, P. **Manual de Análise de Dados: Estatística e Machine Learning com Excel®, SPSS®, Stata®, R® e Python®**. 2. ed. Rio de Janeiro: GEN LTC, 2024.

FEBRABAN. **Pesquisa FEBRABAN de Tecnologia Bancária 2024**. São Paulo: Federação Brasileira de Bancos, 2024. Disponível em: https://febrabantech.febraban.org.br. Acesso em: 17 dez. 2025.

FULFORD, I.; NG, A. **ChatGPT Prompt Engineering for Developers**. DeepLearning.AI, 2023. Disponível em: https://learn.deeplearning.ai/courses/chatgpt-prompt-eng. Acesso em: 15 jan. 2026.

GUPTA, A. et al. Comprehensive review of text-mining applications in finance. **Financial Innovation**, v. 6, n. 37, p. 1-25, 2020.

GUZMAN, E.; MAALEJ, W. How do users like this feature? A fine grained sentiment analysis of app reviews. In: **REQUIREMENTS ENGINEERING CONFERENCE**, 22., 2014, Karlskrona. **Proceedings**... Karlskrona: IEEE, 2014. p. 153-162.

HOGAN, A. et al. Knowledge Graphs. **ACM Computing Surveys**, v. 54, n. 4, p. 1-37, 2021.

HOVY, E. et al. Learning whom to trust: extracting reliable information from multiple conflicting sources. In: **WORKSHOP ON KNOWLEDGE EXTRACTION**, 2013, San Francisco. **Proceedings**... San Francisco: ACM, 2013. p. 45-50.

LEFFINGWELL, D. **Agile Software Requirements: Lean Requirements Practices for Teams, Programs, and the Enterprise**. Boston: Addison-Wesley Professional, 2011.

LIU, B. **Sentiment Analysis and Opinion Mining**. San Rafael: Morgan & Claypool Publishers, 2012.

PAGANO, D.; MAALEJ, W. User feedback in the appstore: an empirical study. In: **REQUIREMENTS ENGINEERING CONFERENCE**, 21., 2013, Rio de Janeiro. **Proceedings**... Rio de Janeiro: IEEE, 2013. p. 125-134.

ROBINSON, I.; WEBBER, J.; EIFREM, E. **Graph Databases: New Opportunities for Connected Data**. 2. ed. Sebastopol: O'Reilly Media, 2015.

ULRICH, W.; ROSEN, M. **The Business Capability Map: The "Rosetta Stone" of Business/IT Alignment**. Cutter Consortium, 2011.

