# Próximos Passos - Daily

**Data:** Hoje  
**Status:** Recebido primeiro dataset classificado manualmente (Carol)

---

## 📊 O que recebi ontem

- **Dataset:** `app_review_dataset_carol.csv`
- **Total:** 1000 avaliações classificadas manualmente
- **Classificações:** 
  - Sentimentos (positive, negative, neutral)
  - Categorias funcionais (15 categorias, classificação múltipla)

---

## 🎯 O que vou fazer HOJE

### 1. Análise do Dataset Recebido ✅ CONCLUÍDO
- [x] Executar script de análise (`analyze_human_classification.py`)
- [x] Verificar qualidade das classificações
- [x] Identificar inconsistências ou padrões
- [x] Gerar relatório de estatísticas

**Resultados:**
- ✅ 1000 avaliações analisadas
- ✅ 294 avaliações negativas (29.4%)
- ⚠️  33 avaliações negativas sem categoria (precisam revisão)
- 📊 Categoria mais frequente: Interface/Usabilidade (27.7%)
- 📊 65 avaliações com múltiplas categorias

**Entregável:** ✅ Relatório `analise_classificacao_carol.md` gerado

---

### 2. Comparação com Classificações do LLM (1h)
- [ ] Carregar resultados do modelo LLM (`functional_correlation_results.csv`)
- [ ] Comparar classificações humanas vs. LLM
- [ ] Calcular métricas de acurácia por categoria
- [ ] Identificar categorias com maior/menor concordância

**Entregável:** Script de comparação e métricas

---

### 3. Análise de Discrepâncias (1h)
- [ ] Identificar casos onde humano e LLM discordam
- [ ] Analisar padrões de erro do modelo
- [ ] Documentar exemplos para revisão
- [ ] Priorizar categorias que precisam de ajuste

**Entregável:** Lista de discrepâncias e exemplos

---

### 4. Preparação para Treino/Fine-tuning (1h)
- [ ] Converter formato do dataset para treino
- [ ] Separar conjunto de treino/teste (se necessário)
- [ ] Validar formato para fine-tuning do modelo
- [ ] Documentar estrutura do dataset de treino

**Entregável:** Dataset formatado para treino

---

### 5. Planejamento para Próxima Classificação (30 min)
- [ ] Definir critérios para segunda pessoa classificar
- [ ] Preparar dataset para segunda pessoa (se necessário)
- [ ] Documentar instruções de classificação
- [ ] Estabelecer prazo para recebimento

**Entregável:** Instruções e dataset para segunda pessoa

---

## 📈 Métricas que vou calcular

1. **Distribuição de Sentimentos**
   - Positive, Negative, Neutral

2. **Distribuição de Categorias**
   - Frequência de cada categoria
   - Média de categorias por avaliação

3. **Acurácia do Modelo LLM**
   - Comparação com classificação humana
   - Por categoria e geral

4. **Inter-Annotator Agreement** (quando tiver segunda pessoa)
   - Coeficiente de concordância

---

## ⏱️ Tempo Estimado

- **Total:** ~4 horas
- **Prioridade Alta:** Itens 1, 2 e 3 (análise e comparação)
- **Prioridade Média:** Itens 4 e 5 (preparação)

---

## 🚀 Próximos Passos (Amanhã)

1. Receber segunda classificação manual
2. Calcular inter-annotator agreement
3. Resolver discrepâncias entre classificadores
4. Iniciar fine-tuning do modelo (se métricas indicarem necessidade)

---

## 📝 Notas e Observações

- ✅ Dataset recebido está no formato correto (classificação múltipla)
- ⚠️  33 avaliações negativas sem categoria - **precisam revisão com Carol**
- ✅ 204 avaliações positivas com categorias (sugestões de melhoria - comportamento esperado)
- 📊 Interface/Usabilidade é a categoria mais frequente (277 marcações)
- 📊 Média de 0.54 categorias por avaliação
- 📊 65 avaliações têm múltiplas categorias (13% das classificadas)

## 🔍 Descobertas Importantes

1. **Distribuição de Sentimentos:**
   - 67.6% positivas (676)
   - 29.4% negativas (294)
   - 2.9% neutras (29)

2. **Top 5 Categorias Mais Frequentes:**
   - Interface/Usabilidade: 277 (27.7%)
   - Outros: 52 (5.2%)
   - Performance: 50 (5.0%)
   - Atendimento: 46 (4.6%)
   - Empréstimos/Crédito: 34 (3.4%)

3. **Pontos de Atenção:**
   - 33 avaliações negativas sem categoria precisam ser revisadas
   - Categorias raras (Questões geográficas: 1, Segurança: 3) podem precisar de mais exemplos

