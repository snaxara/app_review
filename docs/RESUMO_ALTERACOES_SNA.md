# Resumo das Alterações - SNA e Polarização

## Data: 19 de Janeiro de 2026

---

## ✅ ALTERAÇÕES REALIZADAS

### 1. **Substituição de "Sentimento" por "Polarização do Comentário"**

**Ocorrências substituídas:**
- ✅ "análise de sentimentos" → "análise de polarização do comentário"
- ✅ "Análise de Sentimentos" → "Análise de Polarização"
- ✅ "detecção de sentimentos" → "classificação de polarização"
- ✅ "matrizes de confusão de sentimentos" → "matrizes de confusão de polarização"
- ✅ "nuances de sentimento" → "nuances na polarização"
- ✅ "expressam sentimento claro" → "expressam polarização clara"

**Seções atualizadas:**
- ✅ Resumo
- ✅ Palavras-chave
- ✅ Introdução
- ✅ Material e Métodos (Seleção de Modelo)
- ✅ Material e Métodos (Pré-processamento)
- ✅ Material e Métodos (Arquitetura Híbrida)
- ✅ Figuras 5 e 6 (legendas)

---

### 2. **Integração de Social Network Analysis (SNA)**

#### **Referências Adicionadas:**
- ✅ **PINHEIRO, C. A. R.** (2011) - Social Network Analysis in Telecommunications
- ✅ **NEWMAN, M. E. J.** (2010) - Networks: An Introduction

#### **Seção Adicionada: "Métricas de Social Network Analysis (SNA)"**

**Localização**: Material e Métodos, após "Mapeamento Entidade → BusinessCapability"

**Conteúdo:**
- ✅ Explicação de cada métrica de centralidade (Degree, Betweenness, Closeness)
- ✅ Clustering Coefficient
- ✅ Densidade da Rede
- ✅ Referências aos materiais de SNA das aulas
- ✅ Explicação de como as métricas são calculadas no Neo4j

#### **Seção Adicionada: "Métricas de Social Network Analysis Aplicadas ao Knowledge Graph"**

**Localização**: Resultados Preliminares, após "Validação com Dados Reais"

**Conteúdo:**
- ✅ Figura 8: Degree Centrality (Issues e BusinessCapabilities)
- ✅ Figura 9: Métricas SNA Combinadas
- ✅ Interpretação dos resultados das métricas
- ✅ Exemplos práticos (Issues de senha com degree 2, clustering 9.0)
- ✅ Densidade da rede (7.13%)

---

### 3. **Scripts e Queries Criados**

#### **Scripts Python:**
- ✅ `scripts/knowledge_graph/calculate_sna_metrics.py` - Calcula todas as métricas SNA
- ✅ `scripts/generate_sna_visualizations.py` - Gera gráficos de métricas SNA

#### **Queries Cypher:**
- ✅ `scripts/knowledge_graph/queries_sna_metrics.cypher` - 10 queries para visualização no Neo4j

**Métricas implementadas:**
- ✅ Degree Centrality (Issues e BusinessCapabilities)
- ✅ Betweenness Centrality (aproximado)
- ✅ Closeness Centrality (aproximado)
- ✅ Clustering Coefficient
- ✅ Densidade da Rede
- ✅ Identificação de Comunidades

---

### 4. **Visualizações Geradas**

#### **Gráficos Criados:**
- ✅ **Figura 8**: Degree Centrality - Top 15 Issues e Top 15 BusinessCapabilities
- ✅ **Figura 9**: Métricas SNA Combinadas (4 subgráficos):
  - Densidade da Rede (pizza)
  - Distribuição de Degree Centrality (histograma)
  - Top 10 Issues por Clustering Coefficient
  - Resumo estatístico da rede

**Localização**: `Documentos/imagens_tcc/`
- `sna_degree_centrality.png`
- `sna_metricas_combinadas.png`

---

### 5. **Resultados das Métricas SNA**

#### **Densidade da Rede:**
- Total de Issues: 87
- Total de BusinessCapabilities: 15
- Total de Links: 93
- Densidade: 0.0713 (7.13%)

#### **Top Issues por Degree Centrality:**
1. Pede senha duas vezes: 2
2. Não consegue entrar com a senha: 2
3. Bloqueio de Senha: 2
4. Senha bloqueada: 2
5. Criação de Nova Senha: 2

#### **Top BusinessCapabilities por Degree Centrality:**
1. Performance e Estabilidade: 20
2. Gestão de Cadastro e Conta: 16
3. Autenticação e Acesso: 9
4. Transferências PIX: 9
5. Segurança e Proteção: 7

#### **Clustering Coefficient:**
- Issues relacionadas a senha: 9.0 (cluster denso)
- Indica padrões sistemáticos de problemas relacionados

---

## 📚 REFERÊNCIAS ADICIONADAS

### **Novas Referências:**
1. **NEWMAN, M. E. J.** (2010) - Networks: An Introduction
2. **PINHEIRO, C. A. R.** (2011) - Social Network Analysis in Telecommunications

### **Citações no Texto:**
- ✅ Pinheiro (2011) - citado 4 vezes
- ✅ Newman (2010) - citado 3 vezes
- ✅ Menção às aulas de SNA do MBA USP/Esalq

---

## 🎯 ALINHAMENTO COM MATERIAIS DE AULA

### **Conceitos Aplicados:**
- ✅ Degree Centrality (conforme material de SNA)
- ✅ Betweenness Centrality (conforme material de SNA)
- ✅ Closeness Centrality (conforme material de SNA)
- ✅ Clustering Coefficient (conforme material de SNA)
- ✅ Densidade da Rede (conforme material de SNA)
- ✅ Identificação de Comunidades (conforme material de SNA)

### **Metodologia:**
- ✅ Cálculos realizados conforme metodologia de Pinheiro (2011)
- ✅ Interpretação conforme Newman (2010)
- ✅ Aplicação prática no contexto de Knowledge Graph

---

## ✅ CHECKLIST DE CONCLUSÃO

### Substituição de Termos
- [x] Substituir "sentimento" por "polarização do comentário"
- [x] Atualizar todas as ocorrências no documento
- [x] Atualizar legendas de figuras

### Integração SNA
- [x] Adicionar referências (Pinheiro, Newman)
- [x] Criar seção de Métricas SNA em Material e Métodos
- [x] Criar seção de Resultados SNA em Resultados Preliminares
- [x] Criar scripts de cálculo de métricas
- [x] Criar queries Cypher para Neo4j
- [x] Gerar visualizações das métricas
- [x] Inserir figuras no documento
- [x] Interpretar resultados das métricas

---

## 📊 ESTATÍSTICAS

### **Total de Figuras no TCC**: 9
1. Figura 1: Distribuição de Issues por BusinessCapability
2. Figura 2: Top 10 Issues Mais Críticas
3. Figura 3: Distribuição por Nível/Tipo/Valor
4. Figura 4: Pipeline de Processamento
5. Figura 5: Comparação de Modelos de Polarização
6. Figura 6: Matrizes de Confusão - Polarização
7. Figura 7: Comparação de Modelos GPT
8. Figura 8: Degree Centrality (SNA)
9. Figura 9: Métricas SNA Combinadas

### **Referências Adicionadas**: 2
- Newman (2010)
- Pinheiro (2011)

---

## 🎓 CONCLUSÃO

O documento agora está:
- ✅ Alinhado com terminologia correta ("polarização do comentário")
- ✅ Integrado com conceitos de SNA das aulas
- ✅ Com métricas de análise de rede implementadas
- ✅ Com visualizações profissionais das métricas SNA
- ✅ Com referências adequadas aos materiais de aula

**O TCC demonstra aplicação prática dos conceitos aprendidos em Social Network Analysis!**
