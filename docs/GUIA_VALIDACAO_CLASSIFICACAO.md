# Guia de Validação de Classificação de Funcionalidades

Este guia explica como usar o script `validate_functional_classification.py` para calcular métricas de validação da classificação automática de funcionalidades.

## Objetivo

Validar a qualidade da classificação automática de funcionalidades feita pelo LLM, comparando com classificação manual (ground truth) para atender à solicitação do gestor.

## Métricas Calculadas

### 1. Métricas Multi-Label por Categoria

Para cada categoria funcional (PIX, Login/Autenticação, Performance, etc.), calcula:

- **Precision**: Das categorias preditas pelo LLM, quantas estão corretas
- **Recall**: Das categorias reais (humanas), quantas foram identificadas pelo LLM
- **F1-Score**: Média harmônica entre Precision e Recall
- **Suporte**: Quantas avaliações realmente têm essa categoria no ground truth
- **TP/FP/FN/TN**: True Positives, False Positives, False Negatives, True Negatives

**Meta**: F1-Score > 80% em pelo menos 80% das categorias

### 2. Métricas Gerais Multi-Label

- **Exact Match Ratio (EMR)**: Porcentagem de avaliações com todas as categorias corretas
- **Hamming Loss**: Média da fração de labels incorretos (menor é melhor)
- **Jaccard Similarity**: Média da interseção sobre união por avaliação
- **Precision/Recall/F1 (Macro)**: Média não ponderada entre todas as categorias
- **Precision/Recall/F1 (Micro)**: Agrega todos os TP, FP, FN de todas as categorias
- **Precision/Recall/F1 (Weighted)**: Média ponderada pelo suporte de cada categoria

### 3. Métricas de Priorização de Backlog

- **Correlação de Spearman**: Compara o ranking de categorias (ordem de prioridade)
  - Meta: > 0.7 (correlação forte)
  
- **Top-K Accuracy**: Porcentagem de categorias corretas nas top K posições
  - Calculado para K=3, 5, 10
  - Meta: Top-3 > 70%
  
- **MAP@K**: Mean Average Precision at K
  - Considera a posição das categorias corretas
  - Calculado para K=3, 5, 10
  - Meta: MAP@5 > 0.75
  
- **NDCG@K**: Normalized Discounted Cumulative Gain at K
  - Considera a ordem e relevância das categorias
  - Calculado para K=3, 5, 10
  - Meta: NDCG@5 > 0.8

## Como Usar

### Pré-requisitos

1. **Ground Truth**: Arquivo CSV com classificação manual
   - Deve conter colunas de categorias (PIX, Login/Autenticação, etc.)
   - Valores binários (0 ou 1) indicando se a categoria se aplica
   - Coluna `reviewId` ou `content` para fazer merge

2. **Classificação LLM**: Arquivo CSV gerado por `functional_correlation.py`
   - Contém as categorias classificadas automaticamente pelo LLM
   - Mesmo formato de colunas de categorias

### Execução Básica

```bash
python scripts/validate_functional_classification.py \
    --ground-truth data/ground_truth_dataset.csv \
    --llm functional_correlation_results.csv
```

### Parâmetros

- `--ground-truth`: Caminho para arquivo CSV com classificação manual (padrão: `data/ground_truth_dataset.csv`)
- `--llm`: Caminho para arquivo CSV com classificação do LLM (padrão: `functional_correlation_results.csv`)
- `--output`: Arquivo JSON de saída com todas as métricas (padrão: `validation_metrics.json`)
- `--merge-key`: Coluna para fazer merge (`reviewId` ou `content`, padrão: `reviewId`)

### Exemplo Completo

```bash
python scripts/validate_functional_classification.py \
    --ground-truth data/app_review_dataset_carol.csv \
    --llm functional_correlation_results.csv \
    --merge-key content \
    --output resultados_validacao.json
```

## Interpretação dos Resultados

### Métricas por Categoria

```
Categoria                 Precision    Recall       F1-Score     Suporte
-----------------------------------------------------------------------
Performance                   85.50%      92.30%       88.80%         52
Login/Autenticação            78.20%      88.10%       82.90%         21
PIX                           91.00%      75.00%       82.30%         20
```

**Interpretação**:
- **Performance**: LLM tem alta precisão (85.5%) e alto recall (92.3%), indicando boa qualidade
- **Login/Autenticação**: Boa precisão e recall, mas pode melhorar
- **PIX**: Alta precisão (91%) mas recall menor (75%), pode estar perdendo alguns casos

### Métricas Gerais

```
Exact Match Ratio (EMR): 45.50%
Hamming Loss: 0.0625
Jaccard Similarity: 68.30%
F1-Score (Macro): 78.20%
F1-Score (Micro): 82.10%
```

**Interpretação**:
- **EMR 45.5%**: 45.5% das avaliações têm todas as categorias corretas
- **Hamming Loss 0.0625**: Em média, 6.25% dos labels estão incorretos
- **Jaccard 68.3%**: Boa sobreposição entre predições e ground truth
- **F1-Score**: Métricas agregadas mostram desempenho geral bom

### Métricas de Priorização

```
Correlação de Spearman: 0.82
Top-3 Accuracy: 100.00%
MAP@5: 0.88
NDCG@5: 0.91
```

**Interpretação**:
- **Spearman 0.82**: Correlação forte entre rankings (meta > 0.7 atingida)
- **Top-3 100%**: As 3 categorias mais importantes estão corretas
- **MAP@5 0.88**: Boa precisão média nas top 5 posições (meta > 0.75 atingida)
- **NDCG@5 0.91**: Excelente ordenação considerando relevância (meta > 0.8 atingida)

## Critérios de Sucesso

### Categorização Automática
- ✅ F1-Score > 80% em pelo menos 80% das categorias
- ✅ Recall > 75% (não perder problemas importantes)
- ✅ Precision > 70% (não criar falsos positivos)
- ✅ Exact Match Ratio > 40% (pelo menos 40% das avaliações totalmente corretas)

### Priorização de Backlog
- ✅ Correlação de Spearman > 0.7
- ✅ Top-3 Accuracy > 70%
- ✅ MAP@5 > 0.75
- ✅ NDCG@5 > 0.8

## Solução de Problemas

### Poucas Avaliações em Comum

Se o merge encontrar poucas avaliações em comum:

1. Verifique se os datasets são do mesmo período
2. Verifique se a coluna de merge está correta (`reviewId` vs `content`)
3. Use `--merge-key content` se `reviewId` não estiver disponível

### Métricas Zeradas

Se todas as métricas estiverem zeradas:

1. Verifique se as colunas de categorias têm os nomes corretos
2. Verifique se os valores são binários (0 ou 1)
3. Verifique se há avaliações negativas nos datasets

### Erro ao Calcular Priorização

Se não conseguir calcular métricas de priorização:

1. Verifique se há coluna `score` ou similar para calcular severidade
2. Verifique se há avaliações negativas suficientes
3. Verifique se as categorias têm valores binários corretos

## Saída JSON

O script gera um arquivo JSON com todas as métricas calculadas:

```json
{
  "timestamp": "2026-01-08T11:47:10",
  "category_metrics": {
    "PIX": {
      "precision": 0.91,
      "recall": 0.75,
      "f1_score": 0.82,
      "support": 20
    }
  },
  "overall_metrics": {
    "exact_match_ratio": 0.455,
    "hamming_loss": 0.0625,
    "f1_macro": 0.782
  },
  "priorization_metrics": {
    "spearman_correlation": 0.82,
    "top_3_accuracy": 1.0,
    "map_at_5": 0.88
  }
}
```

## Próximos Passos

1. **Coletar mais dados**: Aumentar o dataset de ground truth para melhor validação
2. **Ajustar prompts**: Se métricas não atingirem meta, ajustar prompts do LLM
3. **Análise de erros**: Identificar categorias com pior desempenho e investigar causas
4. **Validação contínua**: Executar validação periodicamente para monitorar qualidade

## Referências

- Documentação: `docs/metodologia_validacao_modelo.md`
- Script de validação: `scripts/validate_functional_classification.py`
- Script de classificação: `scripts/functional_correlation.py`
