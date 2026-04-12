# Metodologia de Validação do Modelo

## Como Validar se a Categorização Automática e Priorização Funcionam

### 1. Divisão Treino/Teste

**Estratégia:**
- **Treino:** 80% das avaliações (800 avaliações)
- **Teste:** 20% das avaliações (200 avaliações)
- **Base Humana:** 2 classificadores independentes classificam o mesmo dataset

**Objetivo:** Garantir que o modelo não está apenas decorando, mas generalizando.

---

### 2. Validação da Categorização Automática

**Como funciona:**
1. **Treino:** Usar 800 avaliações para ajustar/validar o prompt do LLM
2. **Teste:** Aplicar o LLM nas 200 avaliações de teste
3. **Comparação:** Comparar categorias do LLM vs. categorias humanas (ground truth)

**Métricas por Categoria:**

```
Precision = Categorias Corretas Preditas / Total de Categorias Preditas pelo LLM
Recall = Categorias Corretas Preditas / Total de Categorias Reais (Humanas)
F1-Score = 2 × (Precision × Recall) / (Precision + Recall)
```

**Exemplo Prático:**

Avaliação: "O app está travando muito e não consigo fazer login"

- **Humano:** Performance, Login/Autenticação
- **LLM:** Performance, Login/Autenticação, Interface/Usabilidade

**Cálculo:**
- Precision = 2 corretas / 3 preditas = 0.67
- Recall = 2 corretas / 2 reais = 1.0
- F1-Score = 2 × (0.67 × 1.0) / (0.67 + 1.0) = 0.80

**Meta:** F1-Score > 80% por categoria

---

### 3. Validação da Priorização de Backlog

**Como funciona:**
1. **Backlog Esperado (Humano):** Ordenar categorias por frequência + severidade (baseado em classificação humana)
2. **Backlog Gerado (Modelo):** Ordenar categorias usando algoritmo de priorização (frequência + severidade do LLM)
3. **Comparação:** Verificar se a ordem está correta

**Métricas:**

**a) Correlação de Spearman:**
- Compara a ordem/ranking das categorias
- Valor entre -1 e 1
- Meta: > 0.7 (correlação forte)

**b) Top-K Acurácia:**
- Verifica se as categorias mais importantes estão no topo
- Exemplo: Top-3 Acurácia = % de categorias corretas nas 3 primeiras posições
- Meta: Top-3 Acurácia > 70%

**c) MAP@K (Mean Average Precision):**
- Considera a posição das categorias corretas
- Meta: MAP@5 > 0.75

**Exemplo Prático:**

**Backlog Esperado (Humano):**
1. Performance (52 casos, severidade 1.86)
2. Login/Autenticação (21 casos, severidade 1.79)
3. Interface/Usabilidade (X casos, severidade Y)

**Backlog Gerado (Modelo):**
1. Performance (50 casos, severidade 1.88) ✓
2. Login/Autenticação (20 casos, severidade 1.80) ✓
3. Outros (Z casos, severidade W) ✗

**Avaliação:**
- Top-2 Acurácia: 100% (2 de 2 corretas)
- Top-3 Acurácia: 66% (2 de 3 corretas)

---

### 4. Inter-Annotator Agreement

**Objetivo:** Validar que a classificação humana é confiável

**Como funciona:**
- 2 pessoas classificam o mesmo dataset
- Calcular Cohen's Kappa (concordância entre classificadores)

**Interpretação:**
- Kappa < 0: Concordância pior que aleatória
- Kappa 0-0.2: Concordância insignificante
- Kappa 0.21-0.40: Concordância razoável
- Kappa 0.41-0.60: Concordância moderada
- Kappa 0.61-0.80: Concordância substancial ✓ (Meta)
- Kappa 0.81-1.0: Concordância quase perfeita

**Meta:** Kappa > 0.7

---

### 5. Pipeline de Validação Completo

```
1. Coletar Dataset (1000 avaliações)
   ↓
2. Divisão Treino/Teste (80/20)
   ↓
3. Classificação Humana (2 pessoas)
   ↓
4. Calcular Inter-Annotator Agreement
   ↓
5. Resolver Discrepâncias (criar ground truth)
   ↓
6. Treinar/Validar LLM (usar treino)
   ↓
7. Testar LLM (usar teste)
   ↓
8. Calcular Métricas de Categorização
   ↓
9. Gerar Backlog Priorizado (LLM)
   ↓
10. Comparar Backlog (LLM vs. Humano)
    ↓
11. Calcular Métricas de Priorização
    ↓
12. Decidir: Modelo OK ou precisa ajuste?
```

---

### 6. Critérios de Sucesso

**Categorização Automática:**
- ✅ F1-Score > 80% em pelo menos 80% das categorias
- ✅ Recall > 75% (não perder problemas importantes)
- ✅ Precision > 70% (não criar falsos positivos)

**Priorização de Backlog:**
- ✅ Correlação de Spearman > 0.7
- ✅ Top-3 Acurácia > 70%
- ✅ MAP@5 > 0.75

**Validação Humana:**
- ✅ Inter-Annotator Agreement (Kappa) > 0.7

---

### 7. Próximos Passos Práticos

1. **Receber segunda classificação manual**
2. **Calcular inter-annotator agreement**
3. **Criar ground truth** (resolver discrepâncias)
4. **Dividir em treino/teste** (800/200)
5. **Processar teste com LLM** (usar functional_correlation.py)
6. **Comparar resultados** (usar compare_human_vs_llm.py)
7. **Calcular métricas** (Precision, Recall, F1-Score)
8. **Gerar backlog** (usar generate_backlog_report.py)
9. **Comparar priorização** (LLM vs. Humano)
10. **Decidir se precisa ajuste** ou se está pronto

