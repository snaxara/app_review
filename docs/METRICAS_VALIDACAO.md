# Métricas de Validação da Classificação de Funcionalidades

Este documento explica as métricas utilizadas para validar a qualidade da classificação automática de funcionalidades.

## Métricas Principais

### 1. Métricas por Categoria (Multi-Label)

Para cada categoria funcional (PIX, Login/Autenticação, Performance, etc.):

#### Precision (Precisão)
- **Definição**: Das categorias preditas pelo LLM, quantas estão corretas
- **Fórmula**: TP / (TP + FP)
- **Interpretação**: Quanto maior, menos falsos positivos
- **Meta**: > 70%

#### Recall (Revocação)
- **Definição**: Das categorias reais (humanas), quantas foram identificadas pelo LLM
- **Fórmula**: TP / (TP + FN)
- **Interpretação**: Quanto maior, menos falsos negativos (não perder problemas importantes)
- **Meta**: > 75%

#### F1-Score
- **Definição**: Média harmônica entre Precision e Recall
- **Fórmula**: 2 × (Precision × Recall) / (Precision + Recall)
- **Interpretação**: Balanceia Precision e Recall
- **Meta**: > 80% em pelo menos 80% das categorias

#### Suporte
- **Definição**: Quantas avaliações realmente têm essa categoria no ground truth
- **Interpretação**: Indica quantos exemplos temos para validar essa categoria

### 2. Métricas Gerais Multi-Label

#### Exact Match Ratio (EMR)
- **Definição**: Porcentagem de avaliações com todas as categorias corretas
- **Interpretação**: Quanto maior, mais avaliações totalmente corretas
- **Meta**: > 40%

#### Hamming Loss
- **Definição**: Média da fração de labels incorretos
- **Interpretação**: Quanto menor, melhor (0 = perfeito, 1 = tudo errado)
- **Meta**: < 0.15

#### Jaccard Similarity
- **Definição**: Média da interseção sobre união por avaliação
- **Interpretação**: Quanto maior, mais similaridade entre predições e ground truth
- **Meta**: > 60%

#### Precision/Recall/F1 (Macro)
- **Definição**: Média não ponderada entre todas as categorias
- **Interpretação**: Trata todas as categorias igualmente
- **Meta**: F1-Macro > 75%

#### Precision/Recall/F1 (Micro)
- **Definição**: Agrega todos os TP, FP, FN de todas as categorias
- **Interpretação**: Considera o desempenho global
- **Meta**: F1-Micro > 80%

#### Precision/Recall/F1 (Weighted)
- **Definição**: Média ponderada pelo suporte de cada categoria
- **Interpretação**: Dá mais peso a categorias com mais exemplos
- **Meta**: F1-Weighted > 80%

### 3. Métricas de Priorização de Backlog

#### Correlação de Spearman
- **Definição**: Compara o ranking de categorias (ordem de prioridade)
- **Valor**: Entre -1 e 1
- **Interpretação**: Quanto maior, mais similar a ordem de priorização
- **Meta**: > 0.7 (correlação forte)

#### Top-K Accuracy
- **Definição**: Porcentagem de categorias corretas nas top K posições
- **K**: 3, 5, 10
- **Interpretação**: Verifica se as categorias mais importantes estão no topo
- **Meta**: Top-3 > 70%, Top-5 > 80%

#### MAP@K (Mean Average Precision at K)
- **Definição**: Considera a posição das categorias corretas
- **K**: 3, 5, 10
- **Interpretação**: Quanto maior, melhor a precisão média nas top K posições
- **Meta**: MAP@5 > 0.75

#### NDCG@K (Normalized Discounted Cumulative Gain)
- **Definição**: Considera a ordem e relevância das categorias
- **K**: 3, 5, 10
- **Interpretação**: Quanto maior, melhor a ordenação considerando relevância
- **Meta**: NDCG@5 > 0.8

## Como Executar

```bash
# Usando ground truth Excel e filtrando apenas Santander
python scripts/validate_functional_classification.py \
    --ground-truth ground_truth_dataset_std.xlsx \
    --llm functional_correlation_results.csv \
    --app-name Santander \
    --merge-key content
```

## Interpretação dos Resultados

### Excelente (> 85%)
- F1-Score por categoria > 85%
- EMR > 50%
- F1-Macro > 85%

### Bom (70-85%)
- F1-Score por categoria > 70%
- EMR > 40%
- F1-Macro > 75%

### Precisa Melhorar (< 70%)
- F1-Score por categoria < 70%
- EMR < 40%
- F1-Macro < 75%

## Relatório para o Gestor

As métricas principais para apresentar:

1. **F1-Score médio**: Desempenho geral da classificação
2. **Precision média**: Confiabilidade das predições
3. **Recall médio**: Cobertura dos problemas identificados
4. **Exact Match Ratio**: Porcentagem de avaliações totalmente corretas
5. **Correlação de Spearman**: Qualidade da priorização
