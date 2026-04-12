# Próximos Passos - Pipeline de Knowledge Graph

## Data: 16/01/2026

## Status Atual

### ✅ Concluído
- ✅ Pipeline de extração de entidades implementado
- ✅ Mapeamento de entidades para BusinessCapabilities refinado
- ✅ Comparação entre 4 modelos GPT realizada
- ✅ Validação manual de 20 comentários realizada
- ✅ Melhorias aplicadas: **63.6% de acurácia** (melhorou de 54.5%)
- ✅ Filtro de triagem para comentários genéricos implementado
- ✅ Scripts de exportação e validação criados

### 📊 Resultados da Validação
- **14 correções aplicadas** com sucesso
- **1 ainda precisa ajuste**: "Cartão físico não chegou" (não está sendo extraída pelo modelo)
- **7 não encontradas**: Issues extraídas com nomes diferentes pelo modelo (variação normal)

---

## Próximos Passos Recomendados

### 1. **Curto Prazo (Esta Semana)**

#### 1.1. Processar Volume Maior de Comentários
- [ ] Processar **100 comentários** para validar em escala maior
- [ ] Comparar métricas de correlação com os 20 comentários iniciais
- [ ] Verificar se padrões se mantêm com mais dados

**Comando:**
```bash
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --limit 100 --batch-size 10
```

#### 1.2. Testar Outros Modelos com Mapeamento Ajustado
- [ ] Reprocessar os 20 comentários com os outros 3 modelos usando o mapeamento melhorado
- [ ] Comparar resultados entre modelos com as melhorias aplicadas
- [ ] Identificar qual modelo tem melhor acurácia após ajustes

**Comando:**
```bash
python scripts/knowledge_graph/compare_models.py --input sentiment_results.csv --models gpt-4o-mini gpt-4o-2024-08-06 gpt-oss-20b gpt-5.2-2025-12-11 --limit 20
```

#### 1.3. Investigar Issues Não Encontradas
- [ ] Analisar por que algumas issues não estão sendo extraídas (ex: "Telefone péssimo", "Monitoramento")
- [ ] Verificar se o modelo está extraindo com nomes diferentes
- [ ] Ajustar prompt de extração se necessário para capturar essas variações

**Análise necessária:**
- Comparar issues extraídas vs. issues esperadas no CSV de validação
- Identificar padrões de nomes diferentes usados pelo modelo

---

### 2. **Médio Prazo (Próximas 2 Semanas)**

#### 2.1. Refinamento do Prompt de Extração
- [ ] Adicionar exemplos específicos de issues que estão sendo perdidas
- [ ] Melhorar instruções para capturar variações de linguagem
- [ ] Testar diferentes temperaturas/configurações do modelo

#### 2.2. Validação com Ground Truth Expandido
- [ ] Criar ground truth manual para 100 comentários
- [ ] Calcular métricas de precisão/recall por BusinessCapability
- [ ] Identificar BusinessCapabilities com maior taxa de erro

#### 2.3. Análise de Métricas Avançadas
- [ ] Calcular correlação entre Issues e BusinessCapabilities
- [ ] Identificar Issues mais críticas por BusinessCapability
- [ ] Gerar relatórios de priorização de backlog

---

### 3. **Longo Prazo (Próximo Mês)**

#### 3.1. Processamento Completo dos Dados
- [ ] Processar todos os **470 comentários negativos** coletados
- [ ] Processar comentários dos últimos **15 dias** do Santander
- [ ] Validar performance do pipeline em escala completa

#### 3.2. Análise Temporal
- [ ] Implementar análise de evolução das Issues ao longo do tempo
- [ ] Identificar tendências e padrões temporais
- [ ] Correlacionar Issues com versões do aplicativo

#### 3.3. Dashboard e Visualizações
- [ ] Criar dashboard interativo para visualizar métricas
- [ ] Implementar visualizações do grafo de conhecimento
- [ ] Gerar relatórios executivos automáticos

---

## Decisões Pendentes

### 1. **"Cartão físico não chegou"**
**Situação:** Não está sendo extraída pelo modelo LLM  
**Opções:**
- A) Ajustar prompt para capturar melhor questões de logística/envio
- B) Aceitar que algumas issues não serão capturadas (limitação do modelo)
- C) Adicionar regra específica pós-processamento para detectar esse padrão

**Recomendação:** Opção A + C (melhorar prompt E adicionar regra de fallback)

### 2. **Issues com Nomes Diferentes**
**Situação:** Modelo extrai com nomes diferentes do esperado (ex: "Telefone péssimo" vs. "Atendimento telefônico péssimo")  
**Opções:**
- A) Normalizar nomes de issues após extração
- B) Melhorar prompt para usar nomes mais consistentes
- C) Aceitar variação como parte da natureza do modelo

**Recomendação:** Opção B (melhorar prompt com exemplos mais específicos)

### 3. **Escala de Processamento**
**Situação:** Atualmente processando 20 comentários por vez  
**Opções:**
- A) Processar em lotes maiores (100+)
- B) Implementar processamento paralelo
- C) Manter processamento sequencial para controle

**Recomendação:** Opção A (lotes maiores) com monitoramento de custos

---

## Métricas de Sucesso

### Objetivos para Próxima Validação (100 comentários)
- [ ] **Acurácia de mapeamento**: > 70%
- [ ] **Cobertura de Issues**: > 80% das issues relevantes extraídas
- [ ] **Tempo de processamento**: < 30 minutos para 100 comentários
- [ ] **Custo por comentário**: < $0.10 USD

### Objetivos para Produção (470 comentários)
- [ ] **Processamento completo**: Todos os comentários processados sem erros
- [ ] **Métricas de correlação**: Relatórios gerados automaticamente
- [ ] **Qualidade do grafo**: > 1000 relacionamentos Issue ↔ BusinessCapability

---

## Arquivos e Scripts Disponíveis

### Scripts Principais
- `scripts/knowledge_graph/process_negative_reviews.py` - Processamento principal
- `scripts/knowledge_graph/compare_models.py` - Comparação entre modelos
- `scripts/knowledge_graph/export_model_data_to_csv.py` - Exportação de dados
- `scripts/knowledge_graph/validate_mapping_improvements.py` - Validação de melhorias
- `scripts/knowledge_graph/calculate_correlation_metrics.py` - Cálculo de métricas

### Relatórios Gerados
- `reports/model_comparison.txt` - Comparação entre modelos
- `reports/metrics_gpt4o_mini.txt` - Métricas do modelo base
- `reports/model_data_*.csv` - Dados exportados por modelo
- `docs/MELHORIAS_MAPEAMENTO_BC.md` - Documentação das melhorias

---

## Próxima Ação Imediata

**Recomendação:** Começar com **processamento de 100 comentários** para validar em escala maior e identificar novos padrões de erro.

**Comando sugerido:**
```bash
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --limit 100 --batch-size 10
python scripts/knowledge_graph/calculate_correlation_metrics.py --output-report reports/metrics_100_comments.txt
```

---

**Última atualização:** 16/01/2026  
**Próxima revisão:** Após processamento de 100 comentários
