# Resumo da Validação Completa do Modelo

## 📊 Inter-Annotator Agreement (Carol vs. Samuel)

### Resultados por Categoria:

**Concordância Quase Perfeita (Kappa ≥ 0.8):**
- ✅ Notificações: Kappa 1.000 (8 casos ambos)
- ✅ PIX: Kappa 0.841 (19 ambos, 1 discrepância)
- ✅ Empréstimos/Crédito: Kappa 0.822 (29 ambos, 12 discrepâncias)

**Concordância Substancial (Kappa 0.6-0.8):**
- ✅ Tarifas/Cobranças: Kappa 0.749 (3 ambos, 2 discrepâncias)
- ✅ Atendimento: Kappa 0.735 (34 ambos, 23 discrepâncias)
- ✅ Saldo/Extrato: Kappa 0.598 (3 ambos, 4 discrepâncias)

**Concordância Moderada/Razoável (Kappa 0.3-0.6):**
- Performance: Kappa 0.534 (43 ambos, 66 discrepâncias)
- Cadastro/Conta: Kappa 0.440 (4 ambos, 10 discrepâncias)
- Login/Autenticação: Kappa 0.399 (15 ambos, 42 discrepâncias)
- Investimentos: Kappa 0.330 (2 ambos, 8 discrepâncias)
- Pagamentos/Boletos: Kappa 0.219 (1 ambos, 7 discrepâncias)

**Concordância Baixa (Kappa < 0.3):**
- ⚠️ Interface/Usabilidade: Kappa 0.175 (40 ambos, 247 discrepâncias)
- ⚠️ Outros: Kappa 0.000 (0 ambos, 18 discrepâncias)
- ⚠️ Segurança: Kappa -0.003 (0 ambos, 8 discrepâncias)

### Principais Discrepâncias:

1. **Interface/Usabilidade:** 
   - Carol marcou 237 que Samuel não marcou
   - Samuel marcou 10 que Carol não marcou
   - Taxa de acordo: 75.3%

2. **Performance:**
   - Carol marcou 9 que Samuel não marcou
   - Samuel marcou 57 que Carol não marcou
   - Taxa de acordo: 93.4%

3. **Login/Autenticação:**
   - Carol marcou 6 que Samuel não marcou
   - Samuel marcou 36 que Carol não marcou
   - Taxa de acordo: 95.8%

## ✅ Ground Truth Criado

**Estratégia:** Majority (se pelo menos um classificador marcou, marca)

**Estatísticas:**
- Total: 1000 avaliações
- Negativas: 293 avaliações
- 16 categorias funcionais

**Top 5 Categorias no Ground Truth:**
1. Interface/Usabilidade: 166 casos (56.7%)
2. Performance: 96 casos (32.8%)
3. Login/Autenticação: 55 casos (18.8%)
4. Empréstimos/Crédito: 28 casos (9.6%)
5. Outros: 18 casos (6.1%)

## 📈 Validação do Modelo LLM vs. Ground Truth

### Categorização Automática:

**Categorias com Excelente Desempenho (F1-Score ≥ 90%):**
- ✅ PIX: F1-Score 100% (3 casos)
- ✅ Notificações: F1-Score 100% (2 casos)
- ✅ Login/Autenticação: F1-Score 91.67% (11 casos)

**Categorias com Bom Desempenho (F1-Score 70-90%):**
- ✅ Atendimento: F1-Score 85.71% (3 casos)
- ✅ Performance: F1-Score 77.27% (18 casos)

**Categorias que Precisam Melhorar:**
- ⚠️ Interface/Usabilidade: F1-Score 16.67% (33 casos) - Recall muito baixo (9.09%)
- ⚠️ Saldo/Extrato: F1-Score 40% (2 casos)
- ⚠️ Cadastro/Conta: F1-Score 50% (3 casos)

**Métricas Gerais:**
- Média F1-Score: 46.54%
- Categorias com F1-Score > 80%: 4/16 (25%)
- Meta: F1-Score > 80% em 80% das categorias
- **Status: ❌ NÃO ATINGIDO**

### Priorização de Backlog:

**Comparação Top 5:**

| Posição | Ground Truth (Humano) | LLM | Match |
|---------|---------------------|-----|-------|
| 1 | Interface/Usabilidade | Performance | ✗ |
| 2 | Login/Autenticação | Login/Autenticação | ✓ |
| 3 | Performance | Segurança | ✗ |
| 4 | Segurança | Outros | ✗ |
| 5 | Atendimento | Atendimento | ✓ |

**Métricas:**
- Correlação de Spearman: 0.664 (p-value: 0.007)
- Meta: > 0.7
- **Status: ❌ NÃO ATINGIDO** (muito próximo, apenas 0.036 abaixo)

- Top-3 Acurácia: 66.7%
- Meta: > 70%
- **Status: ❌ NÃO ATINGIDO** (muito próximo, apenas 3.3% abaixo)

## 🎯 Análise e Próximos Passos

### Pontos Positivos:

1. ✅ Inter-Annotator Agreement: 5 categorias com concordância substancial/quase perfeita
2. ✅ Categorias críticas (PIX, Login/Autenticação) têm bom desempenho no LLM
3. ✅ Correlação de Spearman próxima da meta (0.664 vs. 0.7)
4. ✅ Top-3 Acurácia próxima da meta (66.7% vs. 70%)

### Pontos a Melhorar:

1. ⚠️ Interface/Usabilidade: Grande discrepância entre classificadores e baixo recall no LLM
2. ⚠️ Performance: Discrepância entre classificadores (Samuel marcou muito mais)
3. ⚠️ Média F1-Score baixa: Precisa ajustar prompts para melhorar categorização geral

### Ações Recomendadas:

1. **Revisar discrepâncias críticas:**
   - Interface/Usabilidade: 247 discrepâncias - revisar critérios de classificação
   - Performance: 66 discrepâncias - alinhar entendimento entre classificadores

2. **Ajustar prompts do LLM:**
   - Melhorar detecção de Interface/Usabilidade (recall muito baixo)
   - Refinar categorização de Performance
   - Adicionar mais exemplos no prompt

3. **Re-executar validação após ajustes:**
   ```bash
   python validate_model.py --human ground_truth_dataset.csv --llm functional_correlation_results.csv
   ```

4. **Considerar fine-tuning:**
   - Se ajustes de prompt não melhorarem suficientemente
   - Usar ground truth para treinar modelo específico

## 📋 Status Atual

- ✅ Ground truth criado: 1000 avaliações
- ✅ Inter-annotator agreement calculado
- ✅ Validação inicial do modelo executada
- ⚠️ Métricas abaixo da meta, mas próximas
- 🔄 Próximo passo: Ajustar prompts e re-validar

