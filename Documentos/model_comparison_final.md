# Comparação Final de Modelos de Análise de Sentimentos

Data: 01/12/2025 20:27
Total de Avaliações Analisadas: 200

---

## Modelos Comparados

1. **DistilBERT Multilíngue** (`lxyuan/distilbert-base-multilingual-cased-sentiments-student`)
2. **BERTweet** (`cardiffnlp/twitter-xlm-roberta-base-sentiment`)

---

## Resultados por Modelo

### DistilBERT Multilíngue

**Modelo:** `lxyuan/distilbert-base-multilingual-cased-sentiments-student`

**Distribuição de Sentimentos:**

| Sentimento | Contagem | Porcentagem |
|:-----------|:---------|:------------|
| positive | 146 | 73.00% |
| negative | 50 | 25.00% |
| neutral | 4 | 2.00% |

**Score Médio de Confiança:** 0.6433

**Métricas de Desempenho (vs Scores Originais):**

- **Acurácia:** 77.00%
- **Precisão:** 81.06%
- **Recall:** 77.00%
- **F1-Score:** 78.34%
- **Amostras Validadas:** 200

---

### BERTweet (Twitter XLM-RoBERTa)

**Modelo:** `cardiffnlp/twitter-xlm-roberta-base-sentiment`

**Distribuição de Sentimentos:**

| Sentimento | Contagem | Porcentagem |
|:-----------|:---------|:------------|
| positive | 146 | 73.00% |
| negative | 33 | 16.50% |
| neutral | 21 | 10.50% |

**Score Médio de Confiança:** 0.7125

**Métricas de Desempenho (vs Scores Originais):**

- **Acurácia:** 87.00%
- **Precisão:** 93.34%
- **Recall:** 87.00%
- **F1-Score:** 89.74%
- **Amostras Validadas:** 200

---

## Comparação Lado a Lado

### Métricas de Desempenho

| Métrica | DistilBERT Multilíngue | BERTweet | Vencedor |
|:--------|:----------------------|:---------|:---------|
| Acurácia | 77.00% | 87.00% | BERTweet |
| Precisão | 81.06% | 93.34% | BERTweet |
| Recall | 77.00% | 87.00% | BERTweet |
| F1-Score | 78.34% | 89.74% | BERTweet |

### Distribuição de Sentimentos

| Sentimento | DistilBERT | BERTweet | Diferença |
|:-----------|:-----------|:---------|:----------|
| negative | 25.0% | 16.5% | -8.5% |
| neutral | 2.0% | 10.5% | +8.5% |
| positive | 73.0% | 73.0% | +0.0% |

## Amostras de Comparação

| Texto | Score Original | DistilBERT | BERTweet | Concordância |
|:------|:---------------|:-----------|:---------|:-------------|
| Exatamente | 5 | positive | neutral | ✗ |
| ótimo ☺️ | 4 | positive | positive | ✓ |
| ótima | 5 | positive | positive | ✓ |
| muito eficiente | 5 | positive | positive | ✓ |
| ótimo | 5 | positive | positive | ✓ |
| Muito bom | 4 | negative | positive | ✗ |
| bom | 5 | negative | positive | ✗ |
| ótimo | 5 | positive | positive | ✓ |
| bem dinâmica as operações através do aplicativo. | 5 | positive | positive | ✓ |
| gostei muito do atendimento e na resolução do meu problema | 5 | negative | positive | ✗ |
| ótimo | 5 | positive | positive | ✓ |
| bom | 5 | negative | positive | ✗ |
| Não estou gostando desse aplicativo do banco tá travando dem... | 1 | negative | negative | ✓ |
| ótimo | 5 | positive | positive | ✓ |
| Nenhuma | 4 | positive | neutral | ✗ |

## Taxa de Concordância entre Modelos

**Taxa de Concordância:** 71.0% (142/200 avaliações)

🟡 **Concordância Moderada:** Algumas diferenças esperadas entre modelos.

## Conclusão e Recomendação

### 🏆 Modelo Recomendado: BERTweet

O modelo **BERTweet** apresenta melhor desempenho geral:

- ✅ Maior acurácia
- ✅ Melhor F1-Score
- ✅ Treinado especificamente em dados de redes sociais (mais adequado para avaliações)
- ✅ Melhor classificação de textos neutros

**Recomendação:** Use o BERTweet como modelo principal para análise de sentimentos de avaliações de apps.


---

*Relatório gerado automaticamente pela comparação de modelos.*
