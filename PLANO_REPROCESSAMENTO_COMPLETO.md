# Plano de Reprocessamento Completo - TCC Final

## Objetivo
Reprocessar todos os dados incluindo a categoria "Outros"/"Outras Funcionalidades" que foi removida das métricas, garantindo cálculo preciso do percentual de cobertura e atualização completa do TCC.

## Status Atual Identificado

### Problemas Encontrados:
1. ✅ Categoria "Outros" existe no `functional_correlation.py` (linha 61)
2. ❌ Categoria "Outras Funcionalidades" existe no mapeamento do Knowledge Graph
3. ❌ Métricas CSV não incluem issues classificadas como "Outros"
4. ❌ Percentual de cobertura está sendo calculado incorretamente (assumindo 100% quando deveria excluir "Outros")

## Etapas do Reprocessamento

### FASE 1: Análise e Diagnóstico

#### 1.1 Verificar Dados Originais
- [ ] Verificar quantos comentários foram classificados como "Outros" no `functional_correlation_results.csv`
- [ ] Verificar se há arquivo com resultados de classificação funcional
- [ ] Contar total de issues extraídas vs issues mapeadas

#### 1.2 Verificar Mapeamento
- [ ] Verificar se "Outros" está sendo mapeado para "Outras Funcionalidades" no Knowledge Graph
- [ ] Verificar se a BusinessCapability "Outras Funcionalidades" existe no Neo4j
- [ ] Verificar se há issues no grafo sem BusinessCapability associada

#### 1.3 Identificar Onde Está a Filtragem
- [ ] Verificar scripts que geram métricas CSV
- [ ] Verificar se há filtros que removem "Outras Funcionalidades"
- [ ] Verificar queries Cypher que geram relatórios

### FASE 2: Correção e Reprocessamento

#### 2.1 Corrigir Mapeamento (se necessário)
- [ ] Garantir que "Outros" → "Outras Funcionalidades" no mapeamento
- [ ] Verificar se BusinessCapability "Outras Funcionalidades" está criada no Neo4j
- [ ] Testar mapeamento com amostra pequena

#### 2.2 Reprocessar Dados no Knowledge Graph
- [ ] Limpar dados antigos do Neo4j (ou criar novo banco)
- [ ] Reprocessar todos os 100 comentários negativos
- [ ] Garantir que issues classificadas como "Outros" sejam mapeadas para "Outras Funcionalidades"
- [ ] Validar que todas as issues foram processadas

#### 2.3 Gerar Métricas Completas
- [ ] Executar script de cálculo de métricas incluindo "Outras Funcionalidades"
- [ ] Gerar CSV com todas as BusinessCapabilities incluindo "Outras Funcionalidades"
- [ ] Calcular percentual real de cobertura: (issues mapeadas - issues em "Outras Funcionalidades") / total de issues × 100

### FASE 3: Atualização de Visualizações

#### 3.1 Regenerar Gráficos
- [ ] Distribuição de Issues por BusinessCapability (incluindo "Outras Funcionalidades")
- [ ] Top 10 Issues Mais Críticas
- [ ] Distribuição por Nível, Tipo e Valor de Negócio
- [ ] Métricas SNA (incluindo "Outras Funcionalidades" se aplicável)

#### 3.2 Atualizar Tabelas
- [ ] Tabela 1: Estatísticas do Knowledge Graph (verificar números)
- [ ] Tabela 2: Distribuição de Issues por BusinessCapability (incluir "Outras Funcionalidades" se houver)
- [ ] Recalcular percentuais excluindo "Outras Funcionalidades"

### FASE 4: Atualização do TCC

#### 4.1 Atualizar Números no Documento
- [ ] Total de issues extraídas
- [ ] Total de issues mapeadas para BusinessCapabilities específicas (excluindo "Outras Funcionalidades")
- [ ] Percentual real de cobertura
- [ ] Distribuição por BusinessCapability (incluindo menção a "Outras Funcionalidades" se houver)

#### 4.2 Atualizar Texto
- [ ] Resumo: Corrigir percentual de cobertura
- [ ] Seção "Cobertura de Linkagem": Explicar cálculo correto
- [ ] Seção "Distribuição de Issues": Incluir "Outras Funcionalidades" se houver issues
- [ ] Conclusão: Atualizar números

#### 4.3 Revisão Crítica
- [ ] Verificar consistência de todos os números
- [ ] Verificar se todas as métricas estão corretas
- [ ] Verificar se gráficos correspondem aos dados
- [ ] Verificar se tabelas estão corretas
- [ ] Verificar formatação conforme normas USP/ESALQ

### FASE 5: Validação Final

#### 5.1 Validação de Dados
- [ ] Soma de issues por BusinessCapability = total de issues (ou total de relacionamentos se houver múltiplos mapeamentos)
- [ ] Percentual de cobertura calculado corretamente
- [ ] Números consistentes entre tabelas, gráficos e texto

#### 5.2 Validação de Conteúdo
- [ ] Revisar texto para garantir que não há contradições
- [ ] Verificar se explicações estão claras
- [ ] Verificar se metodologia está bem descrita

#### 5.3 Gerar Versão Final
- [ ] Regenerar arquivo Word formatado
- [ ] Verificar formatação
- [ ] Preparar para entrega

## Scripts a Serem Executados (em ordem)

1. **Análise Inicial**
   ```bash
   # Verificar dados de classificação funcional
   python scripts/analysis/analyze_other_categories.py
   
   # Verificar dados no Neo4j
   # Query Cypher para contar issues por BusinessCapability
   ```

2. **Reprocessamento**
   ```bash
   # Reprocessar comentários no Knowledge Graph
   python scripts/knowledge_graph/process_reviews_to_graph.py
   
   # Ou usar script específico para Caixa
   python scripts/knowledge_graph/process_caixa_reviews.py  # se existir
   ```

3. **Geração de Métricas**
   ```bash
   # Calcular métricas de correlação
   python scripts/knowledge_graph/calculate_correlation_metrics.py
   
   # Calcular métricas SNA
   python scripts/knowledge_graph/calculate_sna_metrics.py
   ```

4. **Geração de Visualizações**
   ```bash
   # Gerar gráficos do TCC
   python scripts/generate_tcc_visualizations.py
   
   # Gerar gráficos de comparação de modelos
   python scripts/generate_model_comparison_charts.py
   
   # Gerar visualizações SNA
   python scripts/generate_sna_visualizations.py
   ```

5. **Atualização do TCC**
   ```bash
   # Regenerar Word formatado
   python scripts/gerar_word_tcc.py
   ```

## Métricas a Serem Calculadas

### Cobertura de Linkagem
```
Total de Issues Extraídas: X
Issues Mapeadas para BusinessCapabilities Específicas: Y (excluindo "Outras Funcionalidades")
Issues em "Outras Funcionalidades": Z

Percentual de Cobertura = (Y / X) × 100
```

### Distribuição de Issues
- Contar issues por BusinessCapability (incluindo "Outras Funcionalidades")
- Calcular percentuais excluindo "Outras Funcionalidades" para métrica de cobertura
- Incluir "Outras Funcionalidades" na distribuição geral para transparência

## Observações Importantes

1. **Transparência**: Incluir "Outras Funcionalidades" nas tabelas e gráficos para transparência, mas excluir do cálculo de cobertura conforme solicitado.

2. **Consistência**: Garantir que todos os números sejam consistentes entre:
   - Dados do Neo4j
   - CSVs de métricas
   - Tabelas do TCC
   - Gráficos
   - Texto do documento

3. **Validação**: Fazer validação cruzada de todos os números antes de atualizar o TCC final.

4. **Documentação**: Documentar todas as decisões e cálculos para referência futura.

## Próximos Passos Imediatos

1. Verificar dados atuais no Neo4j
2. Identificar quantas issues estão classificadas como "Outros"
3. Verificar se "Outras Funcionalidades" existe no grafo
4. Decidir se vamos reprocessar tudo ou apenas corrigir métricas
5. Executar reprocessamento/correção
6. Atualizar TCC com números corretos
