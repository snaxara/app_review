# Resumo Executivo - Métricas de Validação da Classificação de Funcionalidades

## Objetivo

Validar a qualidade da classificação automática de funcionalidades realizada pelo LLM (GPT-4o), comparando com classificação manual validada.

## Base de Validação

- **Dataset**: 834 avaliações do app Santander
- **Ground Truth**: Classificação manual validada
- **Classificação Automática**: Resultados do LLM (GPT-4o)

## Métricas Calculadas

### 1. Métricas por Categoria Funcional

Para cada uma das 16 categorias funcionais, calculamos:

- **Precision**: Das categorias preditas pelo LLM, quantas estão corretas
- **Recall**: Das categorias reais (humanas), quantas foram identificadas pelo LLM  
- **F1-Score**: Média harmônica entre Precision e Recall (balanceia os dois)
- **Suporte**: Quantas avaliações realmente têm essa categoria

**Meta**: F1-Score > 80% em pelo menos 80% das categorias

### 2. Métricas Gerais de Classificação

- **Exact Match Ratio (EMR)**: Porcentagem de avaliações com todas as categorias corretas
- **Hamming Loss**: Média da fração de labels incorretos (menor é melhor)
- **Jaccard Similarity**: Média da interseção sobre união por avaliação
- **F1-Score (Macro/Micro/Weighted)**: Diferentes formas de agregar o desempenho

**Meta**: EMR > 40%, F1-Score > 75%

### 3. Métricas de Priorização de Backlog

- **Correlação de Spearman**: Compara o ranking de categorias (ordem de prioridade)
- **Top-K Accuracy**: Porcentagem de categorias corretas nas top K posições
- **MAP@K**: Mean Average Precision at K (considera posição das categorias corretas)
- **NDCG@K**: Normalized Discounted Cumulative Gain (considera ordem e relevância)

**Meta**: Spearman > 0.7, Top-3 > 70%, MAP@5 > 0.75

## Como Executar a Validação

**PowerShell:**
```powershell
python scripts/validate_functional_classification.py --ground-truth ground_truth_dataset_std.xlsx --llm functional_correlation_results.csv --app-name Santander --merge-key content
```

**Bash/Linux:**
```bash
python scripts/validate_functional_classification.py \
    --ground-truth ground_truth_dataset_std.xlsx \
    --llm functional_correlation_results.csv \
    --app-name Santander \
    --merge-key content
```

## Interpretação para Apresentação

### Métricas Principais para o Gestor

1. **F1-Score Médio**: Desempenho geral da classificação
   - > 85%: Excelente
   - 70-85%: Bom
   - < 70%: Precisa melhorar

2. **Exact Match Ratio**: Porcentagem de avaliações totalmente corretas
   - > 50%: Excelente
   - 40-50%: Bom
   - < 40%: Precisa melhorar

3. **Correlação de Spearman**: Qualidade da priorização
   - > 0.8: Excelente correlação
   - 0.7-0.8: Boa correlação
   - < 0.7: Precisa melhorar

4. **Top-3 Accuracy**: Categorias mais importantes estão corretas?
   - > 80%: Excelente
   - 70-80%: Bom
   - < 70%: Precisa melhorar

## Próximos Passos

1. Executar validação com o ground truth completo (700 comentários validados)
2. Analisar categorias com menor desempenho
3. Ajustar prompts do LLM se necessário
4. Apresentar resultados ao gestor
