# RESUMO DAS ALTERAÇÕES NO TCC_COMPLETO_ATUALIZADO.md

## 1. REMOÇÃO DE REFERÊNCIAS A DADOS INTERNOS DA CAIXA

### Linha ~35 (Introdução)
**ANTES:**
```
Dados internos da Caixa mostram que 67.6% dos defeitos chegam em produção...
```

**DEPOIS:**
```
considerando que em contextos de deploy contínuo múltiplas versões são lançadas com frequência e bugs introduzidos podem afetar milhões de usuários antes de serem detectados pelos processos tradicionais de monitoramento.
```

### Linha ~104 (BusinessCapability)
**ANTES:**
```
Foram mapeadas 15 capacidades, refinadas com base em dados reais de defeitos em produção do aplicativo da Caixa Econômica Federal...
```

**DEPOIS:**
```
Foram mapeadas 15 capacidades baseadas em análise de domínio e funcionalidades típicas de aplicativos bancários móveis.
```

### Seção removida completamente (~linhas 367-383)
- Removida toda a seção "Validação com Dados Reais de Defeitos em Produção"
- Removidas referências a validação cruzada com defeitos reais em "Próximos Passos"

---

## 2. MELHORIAS DE FLUIDEZ E CONSOLIDAÇÃO DE TÓPICOS

### Linhas ~80-94 (Arquitetura Híbrida)
**CONSOLIDADO:** Seções repetitivas sobre arquitetura foram unificadas em parágrafos mais fluidos.

### Linhas ~146-148 (Métricas SNA)
**ANTES:** Descrição longa e repetitiva das métricas SNA
**DEPOIS:** Descrição consolidada mencionando que clustering coefficient varia de 0 a 1 conforme Newman (2010)

---

## 3. REORGANIZAÇÃO DE FIGURAS E TABELAS

### Ordem corrigida:
1. **Figura 1** - Pipeline de processamento (Material e Métodos)
2. **Quadro 1** - Estrutura do Knowledge Graph Temporal
3. **Figura 2** - Comparação de modelos GPT (era Figura 4)
4. **Figura 3** - Comparação de métricas de polarização (era Figura 2)
5. **Figura 4** - Matrizes de confusão (era Figura 3)
6. **Tabela 1** - Estatísticas do Knowledge Graph
7. **Figura 5** - Distribuição de Issues por BusinessCapability
8. **Tabela 2** - Distribuição de Issues por BusinessCapability
9. **Figura 6** - Top 10 Issues Mais Críticas
10. **Tabela 3** - Top 10 Issues Mais Críticas (NOVA - transformada de lista para tabela)
11. **Figura 7** - Distribuição por Nível, Tipo e Valor
12. **Tabela 4** - Distribuição por Nível Hierárquico (NOVA - separada)
13. **Tabela 5** - Distribuição por Tipo (NOVA - separada)
14. **Tabela 6** - Distribuição por Valor de Negócio (NOVA - separada)
15. **Figura 8** - Degree Centrality
16. **Figura 9** - Métricas SNA Combinadas

---

## 4. TRANSFORMAÇÃO DE LISTAS EM TABELAS

### Linhas ~271-296 (Top 10 Issues)
**ANTES:** Lista numerada simples
**DEPOIS:** Tabela 3 formatada conforme ABNT com colunas: Posição, Issue, Episódios, BusinessCapability

### Linhas ~298-337 (Distribuição por Nível e Tipo)
**ANTES:** Listas com bullets
**DEPOIS:** Três tabelas separadas (Tabelas 4, 5 e 6) mais didáticas

---

## 5. CORREÇÃO DO CLUSTERING COEFFICIENT

### Linha ~148 (Material e Métodos)
**ANTES:**
```
clustering coefficient de 9.0
```

**DEPOIS:**
```
Clustering Coefficient, que mede a proporção de conexões entre vizinhos de um nó em relação ao número máximo possível, variando de 0 a 1 conforme definição de Newman (2010)
```

### Linha ~354 (Resultados)
**ANTES:**
```
Distribuição de Degree Centrality para Issues...
```

**DEPOIS:**
```
Métricas combinadas de Social Network Analysis. (A) Densidade da rede, (B) Distribuição de Degree Centrality para Issues, (C) Top 10 Issues por Clustering Coefficient, (D) Resumo estatístico da rede. O clustering coefficient é calculado conforme definição de Newman (2010), medindo a proporção de conexões entre vizinhos e variando de 0 a 1.
```

### Linha ~356 (Análise)
**ANTES:**
```
clustering coefficient de 9.0
```

**DEPOIS:**
```
degree centrality de 2, conectando-se a múltiplas BusinessCapabilities (Autenticação e Acesso + Segurança e Proteção), indicando impacto transversal
```

---

## 6. MELHORIAS DE TEXTO E CONEXÃO

### Linha ~300
**ADICIONADO:** Texto conectando Figura 7 com Tabelas 4, 5 e 6

### Linha ~296
**ADICIONADO:** Parágrafo de análise conectando os dados da Tabela 3 com análises anteriores

### Linha ~337
**ADICIONADO:** Parágrafo de análise conectando Tabelas 4, 5 e 6 com a relevância da abordagem

---

## ARQUIVOS MODIFICADOS (código)

1. `scripts/knowledge_graph/calculate_sna_metrics.py` - Correção da fórmula do clustering coefficient
2. `scripts/knowledge_graph/queries_sna_metrics.cypher` - Query Cypher corrigida
3. `scripts/generate_sna_visualizations.py` - Limite do eixo X ajustado para 0-1
