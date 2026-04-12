# Comparação Final de Modelos de Análise de Sentimentos

Data: 12/12/2025 14:16
Total de Avaliações Analisadas: 1000
**Validação:** Usando Ground Truth da Carol e Samuel (1000 avaliações classificadas manualmente)

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
| negative | 567 | 56.70% |
| positive | 354 | 35.40% |
| neutral | 79 | 7.90% |

**Score Médio de Confiança:** 0.6203

**Métricas de Desempenho (vs Scores Originais):**

- **Acurácia:** 74.32%
- **Precisão:** 76.43%
- **Recall:** 74.32%
- **F1-Score:** 75.26%
- **ROC AUC:** 78.98%
- **Amostras Validadas:** 366

---

### BERTweet (Twitter XLM-RoBERTa)

**Modelo:** `cardiffnlp/twitter-xlm-roberta-base-sentiment`

**Distribuição de Sentimentos:**

| Sentimento | Contagem | Porcentagem |
|:-----------|:---------|:------------|
| negative | 690 | 69.00% |
| positive | 247 | 24.70% |
| neutral | 63 | 6.30% |

**Score Médio de Confiança:** 0.7927

**Métricas de Desempenho (vs Scores Originais):**

- **Acurácia:** 96.17%
- **Precisão:** 98.17%
- **Recall:** 96.17%
- **F1-Score:** 96.92%
- **ROC AUC:** 98.97%
- **Amostras Validadas:** 366

---

## Comparação Lado a Lado

### Métricas de Desempenho

| Métrica | DistilBERT Multilíngue | BERTweet | Vencedor |
|:--------|:----------------------|:---------|:---------|
| Acurácia | 74.32% | 96.17% | BERTweet |
| Precisão | 76.43% | 98.17% | BERTweet |
| Recall | 74.32% | 96.17% | BERTweet |
| F1-Score | 75.26% | 96.92% | BERTweet |
| ROC AUC | 78.98% | 98.97% | BERTweet |

### Distribuição de Sentimentos

| Sentimento | DistilBERT | BERTweet | Diferença |
|:-----------|:-----------|:---------|:----------|
| negative | 56.7% | 69.0% | +12.3% |
| neutral | 7.9% | 6.3% | -1.6% |
| positive | 35.4% | 24.7% | -10.7% |

## Amostras de Comparação

| Texto | Score Original | DistilBERT | BERTweet | Concordância |
|:------|:---------------|:-----------|:---------|:-------------|
| Uma droga este aplicativo vive travando quando mais preciso ... | 1 | negative | negative | Sim |
| ótimo | 5 | positive | positive | Sim |
| O app não funciona | 1 | negative | negative | Sim |
| bom | 3 | negative | positive | Nao |
| Good app | 5 | positive | positive | Sim |
| muito boa | 5 | positive | positive | Sim |
| Uma dificuldade pra abrir o aplicativo | 1 | positive | negative | Nao |
| Estou com dificuldade para acessar o APP | 1 | negative | negative | Sim |
| maravilhosa app super indico 😜 | 5 | positive | positive | Sim |
| banco ladrão | 1 | positive | negative | Nao |
| bom d+ | 5 | negative | positive | Nao |
| bom | 5 | negative | positive | Nao |
| QUANDO CHEGA A NOITE NÃO CONSIGO ENTRAR NO APP NEM FAZER PIX... | 4 | positive | negative | Nao |
| ótimo 😁 | 5 | positive | positive | Sim |
| O app para de funcionar e me da o erro lclrp0005 e não me de... | 1 | negative | negative | Sim |

## Taxa de Concordância entre Modelos

**Taxa de Concordância:** 69.8% (698/1000 avaliações)

**Concordância Moderada:** Algumas diferenças esperadas entre modelos.

## Conclusão e Recomendação

###  Modelo Recomendado: BERTweet

O modelo **BERTweet** apresenta melhor desempenho geral:

-  Maior acurácia
-  Melhor F1-Score
-  Treinado especificamente em dados de redes sociais (mais adequado para avaliações)
-  Melhor classificação de textos neutros

**Recomendação:** Use o BERTweet como modelo principal para análise de sentimentos de avaliações de apps.


---

*Relatório gerado automaticamente pela comparação de modelos.*
