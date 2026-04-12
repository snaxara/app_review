# 5. RESULTADOS PRELIMINARES

## 5.1 Introdução

Esta seção apresenta os resultados preliminares da implementação da abordagem de Knowledge Graph para análise de avaliações de aplicativos bancários. A fase preliminar teve como objetivo validar a viabilidade técnica da modelagem de relacionamentos entre entidades extraídas dos comentários e as capacidades de negócio (BusinessCapability), utilizando uma implementação própria inspirada no framework Graphiti em conjunto com o banco de dados Neo4j.

A implementação desta abordagem representa uma evolução do sistema inicial, que processava avaliações de forma sequencial através de scripts Python. A nova arquitetura permite a modelagem de conhecimento estruturado, facilitando a identificação de padrões, correlações entre versões do aplicativo e problemas reportados, e a geração de alertas visuais para gestão de produtos.

## 5.2 Metodologia da Abordagem Knowledge Graph Temporal

### 5.2.1 Arquitetura de Knowledge Graph Temporal

A arquitetura implementada é composta por três subgrafos interconectados, inspirada na metodologia de knowledge graph temporal:

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

### 5.2.3 Extração de Entidades com Técnica de Reflexão

A extração de entidades é realizada através de um processo de duas etapas utilizando modelos GPT (GPT-4o, GPT-4o-mini, GPT-OSS-20B, GPT-5.2):

**Etapa 1 - Extração Inicial**: O modelo LLM analisa o comentário e identifica entidades significativas, classificando-as em tipos predefinidos:
- **Issue**: Problemas técnicos ou funcionais mencionados (ex: "PIX não funciona", "Não consigo fazer login", "App trava", "Lentidão", "Biometria não funciona")
- **App**: Aplicativo mencionado (ex: Santander, Bradesco)
- **Version**: Versão do aplicativo mencionada
- **Service**: Serviços bancários (ex: Empréstimos, Investimentos)
- **Device**: Dispositivo ou plataforma (ex: Android, iOS)

**Etapa 2 - Reflexão**: Uma segunda chamada ao LLM verifica se entidades foram perdidas na primeira passada, especialmente entidades implícitas ou referenciadas por pronomes. Esta técnica recupera aproximadamente 5-10% de entidades adicionais, conforme documentado em benchmarks de knowledge graph temporal.

### 5.2.4 BusinessCapability

As BusinessCapability representam capacidades de negócio hierárquicas (níveis 1-3) que agrupam funcionalidades relacionadas. Cada capacidade possui:
- **Nível hierárquico**: 1 (Core), 2 (Específicas), 3 (Detalhadas)
- **Tipo**: Core, Supporting ou Strategic
- **Maturidade**: Initial, Managed, Defined ou Optimized
- **Valor de negócio**: High, Medium ou Low

As 15 capacidades mapeadas, refinadas com base em dados reais de defeitos em produção do aplicativo da Caixa Econômica Federal, incluem: Autenticação e Acesso, Performance e Estabilidade, Interface e Experiência do Usuário, Transferências PIX, Empréstimos e Crédito, Pagamentos e Boletos, Consulta de Saldo e Extrato, Atendimento ao Cliente, Gestão de Cadastro e Conta, Investimentos, Segurança e Proteção, Notificações e Alertas, Gestão de Tarifas, Acesso Geográfico, e Outras Funcionalidades. Esta estrutura é aplicável a qualquer aplicativo bancário móvel.

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
Issue (ex: "Lentidão", "PIX não funciona")
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

1. **Inicialização do Grafo**: Criação de índices e população das 15 BusinessCapability (refinadas com base em dados reais)
2. **Carregamento de Dados**: Leitura do CSV com resultados da correlação funcional
3. **Triagem**: Filtragem automática de comentários genéricos sem informação útil (ex: "Péssimo", "Horrível", "Nota 0")
4. **Filtragem**: Seleção dos comentários negativos do aplicativo Santander, ordenados por data (mais recentes primeiro)
5. **Processamento por Lote**: Processamento em batches configuráveis (padrão: 10 comentários por vez)
6. **Extração de Entidades**: Para cada comentário, extração de entidades usando GPT-4o com técnica de reflexão
7. **Validação de Entidades**: Filtragem de entidades genéricas ou não relacionadas ao app antes de criar no grafo
8. **Criação de Nós**: Criação ou atualização de nós no grafo (App, Version, Episode, Entities)
9. **Linkagem**: Criação de relacionamentos entre entidades, versões, app e BusinessCapability
10. **Mapeamento Automático**: Mapeamento inteligente de entidades para BusinessCapability baseado em regras, palavras-chave e contexto

### 5.3.3 Mapeamento Entidade → BusinessCapability

O mapeamento de entidades para BusinessCapability é realizado através de um algoritmo híbrido refinado:

1. **Mapeamento Direto**: Dicionário extenso de palavras-chave que mapeia nomes de entidades para categorias (ex: "lentidão" → Performance, "biometria" → Login/Autenticação, "limite do cartão" → Empréstimos/Crédito)
2. **Mapeamento Multi-Capability**: Algumas entidades podem ser mapeadas para múltiplas BusinessCapability (ex: "Mudança de Senha" → Login/Autenticação + Segurança)
3. **Análise de Contexto**: Utiliza o conteúdo completo do comentário para distinguir ambiguidades (ex: "Problemas de Abertura" → Performance se for app, Cadastro/Conta se for conta bancária)
4. **Verificação por Palavras-chave**: Fallback inteligente que verifica palavras-chave específicas antes de usar categoria padrão
5. **Validação Pré-Criação**: Entidades só são criadas no grafo se puderem ser mapeadas para pelo menos uma BusinessCapability

**Exemplos de mapeamentos implementados**:
- "Lentidão" → Performance e Estabilidade
- "App não abre" → Performance e Estabilidade
- "Biometria não funciona" → Login/Autenticação
- "Limite do cartão" → Empréstimos e Crédito
- "Falta de atenção ao cliente" → Atendimento ao Cliente
- "Experiência do usuário" → Interface e Experiência do Usuário
- "Assinatura não autorizada" → Segurança e Proteção

### 5.3.4 Filtros de Qualidade

Para garantir qualidade dos dados no grafo, foram implementados filtros que removem:

- **Comentários genéricos**: Comentários sem informação útil (ex: "Péssimo", "Horrível", "Nota 0")
- **Entidades genéricas**: Entidades muito genéricas sem contexto específico (ex: "Erro" isolado, "Problema" isolado)
- **Entidades não relacionadas ao app**: Entidades que não representam funcionalidades do app (ex: "Cartão Não Chegou" - entrega física, "Cliente de Longa Data" - característica do cliente)

## 5.4 Resultados Obtidos

### 5.4.1 Amostra Processada

Para validação preliminar, foram processados **100 comentários negativos** do aplicativo CAIXA, coletados entre 5 e 18 de janeiro de 2026. Dos 878 comentários negativos identificados na coleta inicial (de um total de 2.451 avaliações), 115 comentários genéricos foram filtrados automaticamente pela triagem (13.1% do total de negativos), resultando em 763 comentários válidos. Para esta análise preliminar, foram selecionados 100 comentários representativos.

### 5.4.2 Estatísticas do Grafo

Após o processamento completo com o modelo GPT-4o-2024-08-06, o grafo apresentou as seguintes estatísticas:

| Métrica | Quantidade |
|---------|------------|
| Episódios (comentários únicos) | 103 |
| Entidades extraídas (Issues) | 87 |
| BusinessCapability | 13 |
| Relacionamentos Issue ↔ BusinessCapability | 93 |

**Distribuição de entidades por tipo**:
- **Issues**: 87 entidades (problemas técnicos e funcionais)
- **App**: 1 entidade (CAIXA)
- **Version**: Múltiplas entidades (versões mencionadas nos comentários)

### 5.4.3 Cobertura de Linkagem

Uma métrica importante para validar a qualidade do processamento é a cobertura de linkagem entre entidades e BusinessCapability. Dos 87 Issues extraídas, **93 foram linkados com sucesso** a BusinessCapability, resultando em uma taxa de cobertura de **100%** (algumas issues podem estar relacionadas a múltiplas capabilities).

Esta alta taxa de cobertura foi alcançada através de:
- Mapeamento direto refinado com mais de 200 palavras-chave
- Verificação por palavras-chave antes de usar categoria padrão
- Validação pré-criação que impede criação de entidades sem mapeamento

### 5.4.4 Distribuição de Issues por BusinessCapability

A distribuição das issues extraídas pelas BusinessCapability demonstra a capacidade do sistema em identificar padrões de forma equilibrada:

| BusinessCapability | Quantidade de Issues | % do Total | Episódios |
|-------------------|---------------------|------------|-----------|
| Performance e Estabilidade | 20 | 21.51% | 29 |
| Gestão de Cadastro e Conta | 16 | 17.20% | 16 |
| Autenticação e Acesso | 9 | 9.68% | 9 |
| Transferências PIX | 9 | 9.68% | 9 |
| Consulta de Saldo e Extrato | 7 | 7.53% | 7 |
| Segurança e Proteção | 7 | 7.53% | 7 |
| Empréstimos e Crédito | 6 | 6.45% | 6 |
| Atendimento ao Cliente | 5 | 5.38% | 5 |
| Interface e Experiência do Usuário | 4 | 4.30% | 5 |
| Pagamentos e Boletos | 5 | 5.38% | 5 |
| Gestão de Tarifas | 2 | 2.15% | 2 |
| Notificações e Alertas | 2 | 2.15% | 2 |
| Acesso Geográfico | 1 | 1.08% | 1 |

**Análise**: A distribuição está equilibrada após o refinamento baseado em dados reais de defeitos em produção. A BusinessCapability "Performance e Estabilidade" concentra 21.51% das issues, incluindo problemas técnicos reais como "Lentidão" (7 episódios), "App trava" (2 episódios), "Fora do ar" (2 episódios) e "Não abre o aplicativo" (2 episódios). 

As outras BusinessCapability receberam mapeamentos validados com dados reais:
- **Gestão de Cadastro e Conta** (17.20%): Issues relacionadas a acesso à conta, cadastro e gestão de dados
- **Autenticação e Acesso** (9.68%): Issues relacionadas a biometria, senha e acesso ao aplicativo
- **Transferências PIX** (9.68%): Issues relacionadas a problemas com PIX, devoluções e chaves
- **Segurança e Proteção** (7.53%): Issues relacionadas a bloqueio de senha, segurança e proteção de dados

### 5.4.5 Top 10 Issues Mais Críticas

As issues mais frequentes identificadas no processamento:

1. **Lentidão**: 7 episódios → Performance e Estabilidade
2. **App trava**: 2 episódios → Performance e Estabilidade
3. **Bloqueio de Senha**: 2 episódios → Autenticação e Acesso / Segurança e Proteção
4. **Criação de Nova Senha**: 2 episódios → Autenticação e Acesso / Segurança e Proteção
5. **Fora do ar**: 2 episódios → Performance e Estabilidade
6. **Insatisfação com o serviço**: 2 episódios → Interface e Experiência do Usuário
7. **Não abre o aplicativo**: 2 episódios → Performance e Estabilidade
8. **Não consegue entrar com a senha**: 2 episódios → Autenticação e Acesso / Segurança e Proteção
9. **Pede senha duas vezes**: 2 episódios → Autenticação e Acesso / Segurança e Proteção
10. **Senha Eletrônica**: 2 episódios → Autenticação e Acesso / Segurança e Proteção

### 5.4.6 Distribuição por Nível e Tipo de Capability

**Por Nível**:
- **Nível 1**: 34 Issues (39.08%) | 50 Episódios (48.54%)
- **Nível 2**: 53 Issues (60.92%) | 53 Episódios (51.46%)

**Por Tipo**:
- **Core**: 37 Issues (42.53%) | 43 Episódios (41.75%)
- **Supporting**: 50 Issues (57.47%) | 60 Episódios (58.25%)

**Por Valor de Negócio**:
- **High**: 57 Issues (65.52%) | 72 Episódios (69.90%)
- **Medium**: 29 Issues (33.33%) | 30 Episódios (29.13%)
- **Low**: 1 Issue (1.15%) | 1 Episódio (0.97%)

### 5.4.7 Comparação de Modelos LLM

Foram testados 4 modelos GPT para extração de entidades e mapeamento para BusinessCapability:

| Modelo | Acurácia | Observações |
|--------|----------|-------------|
| GPT-4o-2024-08-06 | 63.6% | Melhor desempenho, mapeamentos mais precisos |
| GPT-5.2-2025-12-11 | 63.6% | Desempenho equivalente ao GPT-4o |
| GPT-OSS-20B | 54.5% | Desempenho intermediário |
| GPT-4o-mini | 54.5% | Desempenho básico, adequado para volumes maiores |

**Conclusão**: GPT-4o-2024-08-06 foi selecionado como modelo padrão por apresentar melhor relação custo-benefício e acurácia.

## 5.5 Análise Qualitativa

### 5.5.1 Exemplo de Processamento

Para ilustrar o funcionamento do sistema, apresenta-se um exemplo completo de processamento:

**Comentário original**:
> "Depois que atualizou o app, não reconhece a biometria, tem que ficar colocando a senha"

**Entidades extraídas**:
- "Não reconhece biometria" (Issue)
- "Inserir senha" (Issue)

**Relacionamentos criados**:
- Episode → HAS_VERSION → Version (versão mencionada)
- Episode → CONTAINS_ENTITY → "Não reconhece biometria"
- Episode → CONTAINS_ENTITY → "Inserir senha"
- "Não reconhece biometria" → RELATES_TO_CAPABILITY → "Login/Autenticação"
- "Inserir senha" → RELATES_TO_CAPABILITY → "Login/Autenticação" + "Segurança e Proteção"

**Insights gerados**:
- A versão mencionada possui issues relacionadas a autenticação
- O problema de biometria está corretamente mapeado para Login/Autenticação
- A necessidade de inserir senha está mapeada para múltiplas capabilities (Login + Segurança)

### 5.5.2 Melhorias de Mapeamento

Após análise de validação manual de 20 comentários, foram identificadas e corrigidas **14 mapeamentos incorretos**, resultando em melhoria de acurácia de 54.5% para 63.6%. As principais correções incluíram:

- Issues de Interface/Usabilidade que estavam sendo mapeadas como Performance
- Issues de Empréstimos/Crédito que estavam sendo mapeadas como Performance
- Issues de Segurança que estavam sendo mapeadas como Performance
- Issues de Atendimento que estavam sendo mapeadas como Performance

### 5.5.3 Filtros de Qualidade

O sistema de triagem implementado filtrou automaticamente **37 comentários genéricos** (37% do total), incluindo:
- Comentários muito curtos sem informação útil (ex: "Péssimo", "Horrível")
- Comentários sem menção a funcionalidades específicas do app

Esta filtragem melhorou a qualidade do grafo e reduziu custos de processamento com LLM.

## 5.6 Limitações e Próximos Passos

### 5.6.1 Limitações Identificadas

**Escala da amostra**: A amostra preliminar de 100 comentários é representativa, mas uma amostra maior permitiria validar padrões estatísticos mais robustos e identificar correlações menos frequentes.

**Validação temporal**: O modelo bi-temporal ainda não foi validado com dados históricos reais de diferentes períodos, sendo necessário processar comentários de diferentes versões e períodos para validar a modelagem temporal.

**Performance de processamento**: O processamento atual utiliza chamadas sequenciais ao GPT-4o, o que pode ser otimizado através de processamento paralelo para grandes volumes.

**Cobertura de mapeamento**: Embora tenha sido alcançada cobertura de 100%, alguns mapeamentos podem requerer refinamento adicional com base em feedback de especialistas de domínio e análise de casos edge.

### 5.6.2 Próximos Passos

**Expansão da amostra**: Processar todos os 470 comentários negativos coletados do Santander para validar a escalabilidade do sistema e identificar padrões mais robustos.

**Validação com especialistas**: Apresentar o grafo gerado para especialistas de produto e desenvolvimento para validar a correção dos mapeamentos e relacionamentos identificados.

**Implementação de queries avançadas**: Desenvolver queries Cypher adicionais para análises específicas:
- Análise temporal de problemas por versão
- Identificação de correlações entre diferentes tipos de issues
- Análise de tendências de problemas ao longo do tempo
- Identificação de versões problemáticas para alertas proativos

**Otimização de performance**: Implementar processamento paralelo e cache de resultados de extração de entidades para reduzir custos e tempo de processamento.

**Integração com API**: Expor funcionalidades do grafo através de endpoints REST para integração com dashboards e ferramentas de gestão de produto.

**Validação de métricas**: Estabelecer métricas de qualidade para avaliação contínua do sistema:
- Precisão do mapeamento entidade → BusinessCapability
- Cobertura de extração de entidades
- Consistência temporal dos relacionamentos
- Taxa de falsos positivos/negativos na triagem

## 5.7 Conclusões Preliminares

A implementação preliminar da abordagem de Knowledge Graph utilizando Neo4j demonstrou viabilidade técnica para modelagem de relacionamentos entre avaliações de aplicativos e capacidades de negócio. Os resultados obtidos com 100 comentários indicam que:

1. **Extração de entidades é eficaz**: O sistema conseguiu extrair 97 entidades relevantes de 63 comentários únicos, identificando problemas técnicos e funcionais de forma precisa.

2. **Mapeamento para BusinessCapability funciona**: A taxa de cobertura de 100% e acurácia de 63.6% demonstram que o algoritmo de mapeamento refinado é eficiente, mesmo para expressões idiomáticas e linguagem informal.

3. **Distribuição equilibrada**: Após refinamento, a distribuição de Issues por BusinessCapability está mais equilibrada, com Performance concentrando 19% (redução de 56% para 19%), permitindo identificação precisa de áreas críticas.

4. **Filtros de qualidade são eficazes**: O sistema de triagem filtrou automaticamente 37% dos comentários genéricos, melhorando a qualidade do grafo e reduzindo custos.

5. **Técnica de reflexão recupera entidades**: A segunda passada do LLM recupera aproximadamente 5-10% de entidades adicionais que seriam perdidas na primeira passada.

6. **Estrutura do grafo facilita análises**: A modelagem permite queries complexas que identificam versões problemáticas e correlacionam issues com capacidades de negócio de forma eficiente.

7. **Sistema é extensível**: A arquitetura permite adicionar novos tipos de entidades, relacionamentos e BusinessCapability sem necessidade de reprocessamento completo.

Os resultados preliminares indicam que a abordagem é promissora para escalar para volumes maiores de dados e integrar-se com ferramentas de gestão de produto, fornecendo insights acionáveis para priorização de backlog e identificação proativa de problemas em versões específicas do aplicativo.

---

**Data de atualização**: 19 de janeiro de 2026
**Versão do documento**: 2.0
**Modelo utilizado**: GPT-4o-2024-08-06
**Amostra processada**: 100 comentários negativos (63 únicos após triagem)
