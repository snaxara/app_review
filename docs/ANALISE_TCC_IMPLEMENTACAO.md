# Análise Detalhada: TCC vs Implementação Atual

## Resumo Executivo

Este documento compara o projeto TCC "API SentimentalBanking: Correlação Funcional e Priorização de Backlog em Apps Bancários via Inteligência Artificial Híbrida" com a implementação atual no projeto `app_review`, identificando gaps, inconsistências e oportunidades de melhoria.

---

## 1. COLETA DE DADOS

### ✅ O que está implementado:
- Script `collect_reviews.py` funcional
- Coleta de Santander e Bradesco
- Extração de: content, score, date, version, app_name
- Filtragem básica (remove vazios e muito curtos)
- Ordenação por mais recentes (Sort.NEWEST)

### ⚠️ GAPS identificados:

#### 1.1 Janela Temporal de 90 dias
**TCC diz:** "janela recente de 90 dias"
**Implementação atual:** Coleta 1000 reviews mais recentes, mas não filtra por data

**Problema:** O arquivo se chama `app_review_dataset_30d.csv` mas não há garantia de que sejam exatamente 30 dias, muito menos 90 dias.

**Solução proposta:**
```python
# Adicionar filtro por data no collect_reviews.py
from datetime import datetime, timedelta

DAYS_WINDOW = 90  # Conforme TCC
cutoff_date = datetime.now() - timedelta(days=DAYS_WINDOW)

# Filtrar após coleta
df['date'] = pd.to_datetime(df['date'])
df = df[df['date'] >= cutoff_date]
```

#### 1.2 Volume Estimado
**TCC diz:** "Estima-se uma amostra inicial de aproximadamente 5.000 avaliações"
**Implementação atual:** 1000 por app = 2000 total

**Recomendação:** Ajustar para coletar mais reviews ou documentar a diferença no TCC.

---

## 2. ANÁLISE DE SENTIMENTOS

### ✅ O que está implementado:
- Modelo XLM-RoBERTa (BERTweet) implementado corretamente
- Pipeline de análise funcional
- Normalização de labels (positive/negative/neutral)
- Análise comparativa entre apps
- Processamento em batches

### ⚠️ GAPS identificados:

#### 2.1 Comparação de Modelos
**TCC diz:** "estudo comparativo empírico entre DistilBERT e BERTweet"
**Implementação atual:** Script `compare_models.py` existe e funciona

**Status:** ✅ Implementado, mas precisa ser executado e resultados documentados no TCC

#### 2.2 Validação com Ground Truth
**TCC diz:** "validação via dupla anotação humana (Inter-Annotator Agreement)"
**Implementação atual:** 
- Ground truth existe (`data/ground_truth_dataset.csv`)
- Scripts de validação existem (`validate_model.py`, `compare_human_vs_llm.py`)
- Métricas calculadas (Accuracy, Precision, Recall, F1-Score)

**Status:** ✅ Implementado, mas precisa garantir que os resultados estão sendo usados no TCC

---

## 3. CORRELAÇÃO FUNCIONAL

### ✅ O que está implementado:
- Script `functional_correlation.py` funcional
- Uso de GPT-4o para categorização
- Suporte a múltiplas categorias por avaliação
- Few-Shot Learning implementado
- 16 categorias funcionais definidas

### ⚠️ GAPS identificados:

#### 3.1 Processamento apenas de Negativas
**TCC diz:** "As avaliações classificadas como negativas são submetidas à API do modelo GPT-4o"
**Implementação atual:** ✅ Correto (`PROCESS_ONLY_NEGATIVE = True`)

**Status:** ✅ Alinhado

#### 3.2 Validação da Categorização
**TCC menciona:** Métricas de validação da categorização
**Implementação atual:** Script `validate_model.py` calcula métricas por categoria

**Status:** ✅ Implementado, mas precisa documentar resultados no TCC

---

## 4. PRIORIZAÇÃO DE BACKLOG

### ✅ O que está implementado:
- Algoritmo de priorização implementado
- Fórmula: (Frequência * 0.4) + (Severidade * 0.3) + (Impacto * 0.3)
- Pesos de impacto por categoria
- Geração de relatório de backlog

### ⚠️ GAPS identificados:

#### 4.1 Análise por Versão
**TCC diz:** "identificar picos de reclamações associados a versões específicas dos aplicativos"
**Implementação atual:** Campo `version` é coletado, mas não há análise específica por versão

**Solução proposta:** Criar script `analyze_by_version.py` que:
- Agrupa avaliações negativas por versão
- Identifica versões com maior volume de problemas
- Correlaciona versões com categorias funcionais

#### 4.2 Análise Temporal
**TCC menciona:** Análise temporal para identificar tendências
**Implementação atual:** Campo `date` existe, mas não há análise temporal

**Solução proposta:** Adicionar análise de tendências temporais no backlog report

---

## 5. API (CRÍTICO - FALTANDO)

### ❌ GAP CRÍTICO:

**TCC diz:** "A entrega final consiste em uma API desenvolvida em Python que processa as avaliações periodicamente e disponibiliza os resultados em formato estruturado (JSON/CSV)"

**Implementação atual:** ❌ NÃO EXISTE API

**Impacto:** Este é um requisito central do TCC e não está implementado.

**Solução proposta:** Criar API usando Flask ou FastAPI com:
- Endpoint para processar avaliações
- Endpoint para obter backlog priorizado
- Endpoint para métricas de validação
- Suporte a JSON e CSV
- Documentação Swagger/OpenAPI

---

## 6. MÉTRICAS E VALIDAÇÃO

### ✅ O que está implementado:
- Cálculo de Accuracy, Precision, Recall, F1-Score
- ROC AUC calculado
- Matriz de confusão
- Métricas por categoria funcional
- Inter-Annotator Agreement (Kappa)

### ⚠️ GAPS identificados:

#### 6.1 Documentação de Resultados
**TCC precisa:** Resultados preliminares com métricas específicas
**Implementação atual:** Métricas são calculadas, mas precisam ser consolidadas em um relatório para o TCC

**Solução proposta:** Criar script `generate_tcc_results.py` que gera relatório com:
- Métricas de validação do modelo de sentimentos
- Métricas de validação da categorização funcional
- Exemplos de predições corretas e incorretas
- Análise de casos edge

---

## 7. ESTRUTURA DE DADOS

### ⚠️ INCONSISTÊNCIAS:

#### 7.1 Nomenclatura de Arquivos
- TCC menciona dataset de 90 dias
- Arquivo atual: `app_review_dataset_30d.csv`
- Inconsistência entre nome e conteúdo

**Solução:** Renomear ou ajustar coleta para garantir 90 dias

#### 7.2 Campos Obrigatórios
**TCC precisa:** reviewId para fazer merge com ground truth
**Implementação atual:** Alguns scripts usam `content` para merge, outros esperam `reviewId`

**Solução:** Padronizar uso de `reviewId` em todos os scripts

---

## 8. MELHORIAS SUGERIDAS

### Prioridade ALTA:

1. **Implementar API** (requisito central do TCC)
2. **Filtrar coleta por 90 dias** (alinhar com TCC)
3. **Análise por versão** (mencionado no TCC como resultado)
4. **Consolidar resultados** para seção de Resultados Preliminares

### Prioridade MÉDIA:

5. **Análise temporal** (tendências ao longo do tempo)
6. **Padronizar reviewId** em todos os scripts
7. **Documentar métricas** obtidas nos resultados preliminares

### Prioridade BAIXA:

8. **Otimizar prompts** do LLM baseado em resultados
9. **Adicionar testes unitários** para garantir qualidade
10. **Melhorar tratamento de erros** na API

---

## 9. CHECKLIST PARA RESULTADOS PRELIMINARES

### Dados:
- [ ] Dataset com exatamente 90 dias de avaliações
- [ ] Volume documentado (quantas avaliações coletadas)
- [ ] Distribuição entre Santander e Bradesco

### Modelo de Sentimentos:
- [ ] Comparação DistilBERT vs BERTweet executada
- [ ] Métricas de validação com ground truth calculadas
- [ ] Resultados documentados (Accuracy, Precision, Recall, F1-Score)

### Categorização Funcional:
- [ ] Métricas por categoria calculadas
- [ ] Exemplos de categorização correta/incorreta
- [ ] Taxa de concordância com anotadores humanos

### Priorização:
- [ ] Backlog priorizado gerado
- [ ] Análise por versão implementada
- [ ] Identificação de picos de reclamações por versão

### API:
- [ ] API básica implementada
- [ ] Endpoints funcionais
- [ ] Documentação da API

---

## 10. PRÓXIMOS PASSOS RECOMENDADOS

1. **Imediato:** Implementar filtro de 90 dias na coleta
2. **Esta semana:** Criar API básica com Flask/FastAPI
3. **Esta semana:** Implementar análise por versão
4. **Próxima semana:** Consolidar todos os resultados em relatório para TCC
5. **Próxima semana:** Revisar e atualizar seção de Resultados Preliminares no PDF

---

## Conclusão

O projeto está bem estruturado e a maior parte da metodologia está implementada. Os principais gaps são:
1. Falta de API (requisito central)
2. Falta de análise por versão (resultado mencionado)
3. Inconsistência na janela temporal (90 dias vs 30 dias)
4. Necessidade de consolidar resultados para o TCC

Com as correções sugeridas, o projeto estará alinhado com o que foi proposto no TCC.

