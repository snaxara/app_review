# Resumo das Mudanças no TCC - Alinhamento com Knowledge Graph

## Mudanças Realizadas

### 1. TÍTULO
**Antes:** "API SentimentalBanking: Correlação Funcional e Priorização de Backlog em Apps Bancários via Inteligência Artificial Híbrida"

**Depois:** "API SentimentalBanking: Identificação de Bugs por Versão e Priorização de Backlog em Apps Bancários via Knowledge Graph e Inteligência Artificial Híbrida"

**Justificativa:** O novo título reflete o objetivo central da pesquisa (identificar bugs por versão) e menciona explicitamente a tecnologia utilizada (Knowledge Graph).

---

### 2. RESUMO
**Mudanças principais:**
- Adicionada menção explícita à extração de issues e correlação com BusinessCapability
- Incluída descrição do framework Graphiti e Neo4j
- Destaque para identificação de bugs por versão
- Menção à taxa de cobertura de 100% na extração de entidades
- Enfatizada capacidade de identificar padrões sistemáticos

**Palavras-chave adicionadas:**
- Knowledge Graph
- Identificação de Bugs
- Neo4j

---

### 3. INTRODUÇÃO
**Mudanças principais:**
- Expandida justificativa sobre importância de identificar bugs por versão
- Adicionada referência à literatura sobre análise de avaliações (Guzman & Maalej, 2014; Pagano & Maalej, 2013)
- Incluída menção à lacuna de sistemas que correlacionam problemas com versões e capacidades de negócio
- Adicionada justificativa sobre deploy contínuo e necessidade de identificar bugs rapidamente
- Expandida descrição da abordagem de Knowledge Graph
- Incluída referência a trabalhos recentes sobre Knowledge Graphs em software (Chen et al., 2022)

**Estrutura mantida:**
- Contexto do mobile banking no Brasil (FEBRABAN)
- Problema da análise manual
- Lacuna tecnológica
- Proposta de solução

---

### 4. MATERIAL E MÉTODOS
**Nova estrutura com quebras claras:**

#### 4.1 Coleta e Definição do Dataset
- Mantida estrutura original
- Mantida janela de 90 dias
- Mantida estimativa de 5.000 avaliações

#### 4.2 Seleção de Modelo e Estudo Comparativo
- Mantida comparação DistilBERT vs BERTweet
- Adicionada referência a Devlin et al. (2019) sobre escolha de modelos

#### 4.3 Validação via Dupla Anotação Humana
- Mantida estrutura original
- Adicionada referência a Fávero e Belfiore (2024)

#### 4.4 Pré-processamento
- Mantida decisão de preservar estrutura sintática
- Adicionada referência a Devlin et al. (2019) sobre remoção de stop words

#### 4.5 Arquitetura Híbrida de Modelagem
**Estágio 1 - Análise de Sentimentos:**
- Mantida descrição do BERTweet
- Adicionadas referências (Liu, 2012; Devlin et al., 2019)

**Estágio 2 - Extração de Entidades e Modelagem em Knowledge Graph:**
- **NOVA SEÇÃO** descrevendo a evolução da abordagem
- Mudança de categorização direta para extração de entidades + grafo
- Adicionada referência a Fulford e Ng (2023) sobre prompt engineering

#### 4.6 Framework Graphiti e Modelagem em Knowledge Graph
**NOVA SEÇÃO COMPLETA** incluindo:
- Descrição dos 3 subgrafos (Episódico, Semântico, Comunidade)
- Modelo bi-temporal detalhado
- Justificativa da escolha do Neo4j com referência (Robinson et al., 2015)

#### 4.7 Extração de Entidades
**NOVA SEÇÃO** descrevendo:
- Processo de duas etapas (Extração Inicial + Reflexão)
- Tipos de entidades (Feature, Issue, App, Version, Service, Device)
- Referência a Fulford e Ng (2023) sobre NER

#### 4.8 BusinessCapability e Modelagem de Domínio
**NOVA SEÇÃO** incluindo:
- Modelo de BusinessCapability (Ulrich & Rosen, 2011)
- Classificação TOGAF e CMMI
- Alinhamento com Domain-Driven Design (Evans, 2003)
- Lista das 16 capacidades mapeadas

#### 4.9 Arquitetura do Grafo
**NOVA SEÇÃO** com:
- Diagrama da estrutura do grafo
- Características principais explicadas
- Referência a Coskun et al. (2021) sobre modelagem de grafos
- Referência a Christen (2012) sobre Entity Resolution

#### 4.10 Mapeamento Entidade → BusinessCapability
**NOVA SEÇÃO** descrevendo:
- Algoritmo híbrido (4 etapas)
- Referência a Hovy et al. (2013) sobre sistemas híbridos

#### 4.11 Métricas e Validação do Modelo
- Mantidas métricas originais (Acurácia, Precisão, Recall, F1-Score)
- **Adicionadas novas métricas:**
  - Cobertura de linkagem
  - Taxa de identificação de bugs por versão
  - Precisão do mapeamento entidade → BusinessCapability

---

### 5. REFERÊNCIAS
**Novas referências adicionadas:**
- ANOUZE et al. (2019) - Customer satisfaction em bancos
- CHEN et al. (2022) - Knowledge graph para bug localization
- CHRISTEN (2012) - Entity Resolution
- COSKUN et al. (2021) - Graph-based analysis de software
- EVANS (2003) - Domain-Driven Design
- FULFORD & NG (2023) - Prompt Engineering
- GUZMAN & MAALEJ (2014) - Análise de app reviews
- HOGAN et al. (2021) - Knowledge Graphs (survey)
- HOVY et al. (2013) - Sistemas híbridos
- LEFFINGWELL (2011) - Priorização de backlog
- PAGANO & MAALEJ (2013) - User feedback no appstore
- ROBINSON et al. (2015) - Neo4j e Graph Databases
- ULRICH & ROSEN (2011) - Business Capability Map
- ZEP (2024) - Graphiti framework

**Total:** 15 novas referências adicionadas ao conjunto original

---

## Estrutura Final do Documento

1. **Título** - Atualizado
2. **Resumo** - Expandido com nova abordagem
3. **Palavras-chave** - Adicionadas: Knowledge Graph, Identificação de Bugs, Neo4j
4. **Introdução** - Expandida com contexto teórico e justificativas
5. **Material e Métodos** - Reestruturado com 11 subseções:
   - 4.1 Coleta e Definição do Dataset
   - 4.2 Seleção de Modelo e Estudo Comparativo
   - 4.3 Validação via Dupla Anotação Humana
   - 4.4 Pré-processamento
   - 4.5 Arquitetura Híbrida de Modelagem
   - 4.6 Framework Graphiti e Modelagem em Knowledge Graph (NOVO)
   - 4.7 Extração de Entidades (NOVO)
   - 4.8 BusinessCapability e Modelagem de Domínio (NOVO)
   - 4.9 Arquitetura do Grafo (NOVO)
   - 4.10 Mapeamento Entidade → BusinessCapability (NOVO)
   - 4.11 Métricas e Validação do Modelo (Expandido)
6. **Referências** - Expandido de ~7 para ~22 referências

---

## Alinhamento com Objetivo Atualizado

**Objetivo Original:** Correlação funcional e priorização de backlog

**Objetivo Atualizado:** Identificar bugs de comentários e relacionar com capacidades do aplicativo para identificar bugs de versão e apoiar priorização de backlog

**Todas as seções foram ajustadas para refletir este novo objetivo:**
- Título menciona "Identificação de Bugs por Versão"
- Resumo descreve extração de issues e correlação com versões
- Introdução justifica necessidade de identificar bugs por versão
- Material e Métodos detalha processo de extração e modelagem em grafo
- Resultados Preliminares apresenta resultados da nova abordagem

---

## Próximos Passos Recomendados

1. **Revisar referências**: Verificar se todas as referências estão corretas e completas
2. **Validar citações**: Garantir que todas as citações no texto correspondem às referências
3. **Ajustar formatação**: Verificar se está conforme normas USP/ESALQ
4. **Revisar consistência**: Garantir que todas as seções estão alinhadas entre si
5. **Adicionar figuras**: Considerar adicionar diagramas da arquitetura do grafo
