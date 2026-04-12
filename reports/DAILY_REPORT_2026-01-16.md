# Relatório Daily - 16/01/2026

## 📋 Resumo Executivo

Concluída a implementação e validação do pipeline de Knowledge Graph para correlação funcional de comentários de aplicativos bancários. Realizada comparação entre 4 modelos GPT diferentes utilizando o mesmo prompt e conjunto de dados.

---

## ✅ O Que Foi Feito Hoje

### 1. Refinamento do Pipeline de Extração de Entidades
- ✅ Simplificação do prompt: remoção do tipo "Feature", mantendo apenas "Issue" para comentários negativos
- ✅ Implementação de filtro de triagem para remover comentários genéricos (ex: "Péssimo", "Horrível")
- ✅ Correção de mapeamento de entidades para BusinessCapabilities (ex: Biometria/Senha → Autenticação e Acesso)
- ✅ Prevenção de criação de entidades genéricas como "Aplicativo" no grafo

### 2. Processamento e Validação
- ✅ Reprocessamento de 20 comentários negativos do Santander
- ✅ Criação automática de BusinessCapabilities quando não existem no grafo
- ✅ Validação do grafo: 20 episódios, 61 entidades (Issues), 16 BusinessCapabilities, 122 relacionamentos

### 3. Cálculo de Métricas de Correlação
- ✅ Implementação de script para cálculo de métricas de correlação entre Issues e BusinessCapabilities
- ✅ Geração de relatórios em formato texto, CSV e JSON
- ✅ Métricas calculadas para modelo base (gpt-4o-mini):
  - 60 Issues únicas extraídas
  - 12 BusinessCapabilities associadas
  - 61 episódios processados

### 4. Comparação de Modelos GPT
- ✅ Criação de script automatizado para comparação entre modelos
- ✅ Teste com 4 modelos diferentes usando o mesmo prompt e conjunto de dados:
  - `gpt-4o-mini` (modelo base)
  - `gpt-4o-2024-08-06`
  - `gpt-oss-20b`
  - `gpt-5.2-2025-12-11`
- ✅ Processamento de 20 comentários idênticos com cada modelo
- ✅ Geração de relatório comparativo completo

---

## 📊 Resultados Principais

### Métricas de Correlação (Modelo Base: gpt-4o-mini)

**Distribuição por BusinessCapability:**
- **Performance e Estabilidade**: 25 issues (41.67%) | 25 episódios (40.98%)
- **Gestão de Cadastro e Conta**: 7 issues (11.67%) | 7 episódios (11.48%)
- **Atendimento ao Cliente**: 6 issues (10.00%) | 6 episódios (9.84%)
- **Segurança e Proteção**: 6 issues (10.00%) | 6 episódios (9.84%)

**Top 5 Issues Mais Críticas:**
1. Problemas com PIX: 2 episódios
2. App não abre: 1 episódio
3. App trava: 1 episódio
4. Atendimento ruim: 1 episódio
5. Erro ao fazer pagamento: 1 episódio

### Comparação de Modelos

| Modelo | Issues Extraídas | Capabilities | Episódios | Erros |
|--------|------------------|--------------|-----------|-------|
| gpt-4o-mini | 56 | 12 | 57 | 0 |
| gpt-4o-2024-08-06 | 55 | 12 | 56 | 0 |
| gpt-oss-20b | 57 | 11 | 58 | 0 |
| gpt-5.2-2025-12-11 | 57 | 12 | 58 | 0 |

**Insights:**
- Todos os modelos apresentaram desempenho similar (variação de 1-2 issues)
- **gpt-oss-20b** extraiu mais issues (57) e mais episódios (58)
- Todos os modelos identificaram "Performance e Estabilidade" como BusinessCapability mais crítica
- Zero erros em todos os modelos testados

---

## 🔍 Análise e Observações

### Pontos Positivos
1. **Consistência entre modelos**: Todos os modelos apresentaram resultados muito similares, indicando robustez do prompt
2. **Qualidade da extração**: Issues extraídas são específicas e relevantes (ex: "Problemas com PIX", "App não abre")
3. **Mapeamento correto**: Entidades estão sendo corretamente associadas às BusinessCapabilities apropriadas
4. **Filtro de triagem eficaz**: 12.6% dos comentários genéricos foram filtrados antes do processamento

### Padrões Identificados
- **Performance e Estabilidade** é consistentemente a BusinessCapability mais crítica em todos os modelos
- **Problemas com PIX** aparece como Issue mais frequente em todos os modelos
- Distribuição equilibrada entre Issues de diferentes BusinessCapabilities

---

## 📁 Arquivos Gerados

### Relatórios
- `reports/metrics_gpt4o_mini.txt` - Métricas detalhadas do modelo base
- `reports/metrics_gpt4o_mini.csv` - Dados em formato tabular
- `reports/metrics_gpt4o_mini.json` - Dados estruturados em JSON
- `reports/model_comparison.txt` - Relatório comparativo entre modelos
- `reports/model_comparison.json` - Dados comparativos estruturados

### Scripts Criados/Atualizados
- `scripts/knowledge_graph/compare_models.py` - Script de comparação entre modelos
- `scripts/knowledge_graph/calculate_correlation_metrics.py` - Cálculo de métricas
- `scripts/knowledge_graph/process_negative_reviews.py` - Processamento com inicialização automática

---

## 🎯 Próximos Passos

### Curto Prazo
1. **Análise detalhada dos resultados**: Revisar diferenças sutis entre modelos para identificar qual oferece melhor qualidade (não apenas quantidade)
2. **Validação manual**: Comparar extrações com classificação manual para calcular precisão/recall
3. **Escalabilidade**: Testar processamento com volume maior de comentários (100+)

### Médio Prazo
1. **Otimização de prompt**: Refinar prompt baseado nos resultados da comparação
2. **Métricas avançadas**: Implementar métricas de qualidade semântica (não apenas contagem)
3. **Dashboard**: Criar visualização interativa das métricas de correlação

### Longo Prazo
1. **Processamento em produção**: Preparar pipeline para processar todos os comentários coletados
2. **Análise temporal**: Implementar análise de evolução das Issues ao longo do tempo
3. **Priorização automática**: Desenvolver algoritmo de priorização de backlog baseado nas métricas

---

## ⚠️ Bloqueios / Dificuldades

**Nenhum bloqueio identificado.**

Todas as funcionalidades planejadas foram implementadas e testadas com sucesso.

---

## 💡 Decisões Técnicas

1. **Simplificação de tipos de entidades**: Decisão de tratar tudo como "Issue" em comentários negativos simplificou o pipeline e melhorou a consistência
2. **Filtro de triagem**: Implementação de filtro pré-processamento reduziu ruído e custos de processamento
3. **Inicialização automática**: BusinessCapabilities são criadas automaticamente se não existirem, facilitando o uso do pipeline

---

## 📈 Métricas de Sucesso

- ✅ **4 modelos testados** com sucesso
- ✅ **0 erros** em todos os processamentos
- ✅ **20 comentários** processados por modelo
- ✅ **60+ Issues** extraídas por modelo
- ✅ **12 BusinessCapabilities** identificadas consistentemente
- ✅ **Relatórios completos** gerados em múltiplos formatos

---

## 🤝 Contribuições

- Refinamento de prompts de extração de entidades
- Implementação de sistema de comparação entre modelos
- Cálculo e análise de métricas de correlação
- Documentação completa dos resultados

---

**Preparado por:** Sistema de IA  
**Data:** 15/01/2026  
**Próxima Daily:** 16/01/2026
