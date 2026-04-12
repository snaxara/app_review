# Comparação: Antes vs. Depois dos Ajustes

## 📊 Inter-Annotator Agreement

### Métricas Gerais

| Métrica | Antes | Depois | Mudança |
|---------|-------|--------|---------|
| **Kappa Médio** | 0.456 | 0.521 | +0.065 ✅ |
| **Categorias com Kappa ≥ 0.6** | 5/16 (31%) | 7/16 (44%) | +2 categorias ✅ |
| **Total de Discrepâncias** | 456 | 299 | -157 (-34%) ✅ |

### Melhorias por Categoria

**Melhorias Significativas:**

1. **Login/Autenticação:**
   - Antes: Kappa 0.399 (Razoável)
   - Depois: Kappa 0.711 (Substancial) ✅
   - Mudança: +0.312

2. **Performance:**
   - Antes: Kappa 0.534 (Moderada)
   - Depois: Kappa 0.727 (Substancial) ✅
   - Mudança: +0.193

3. **PIX:**
   - Antes: Kappa 0.841 (Quase perfeita)
   - Depois: Kappa 0.915 (Quase perfeita) ✅
   - Mudança: +0.074

**Categorias que Mantiveram Boa Concordância:**
- Notificações: Kappa 1.000 (mantido)
- Empréstimos/Crédito: Kappa 0.822 → 0.835 (melhorou)
- Tarifas/Cobranças: Kappa 0.749 (mantido)
- Atendimento: Kappa 0.735 → 0.743 (melhorou)

**Categorias que Ainda Precisam Atenção:**
- Interface/Usabilidade: Kappa 0.175 → 0.383 (melhorou, mas ainda baixo)
- Pagamentos/Boletos: Kappa 0.219 → 0.150 (piorou)
- Outros: Kappa 0.000 → -0.004 (ainda problemático)

### Redução de Discrepâncias

**Principais Reduções:**

1. **Interface/Usabilidade:**
   - Antes: 247 discrepâncias
   - Depois: 102 discrepâncias
   - Redução: -145 (-59%) ✅

2. **Performance:**
   - Antes: 66 discrepâncias
   - Depois: 60 discrepâncias
   - Redução: -6 (-9%)

3. **Login/Autenticação:**
   - Antes: 42 discrepâncias
   - Depois: 28 discrepâncias
   - Redução: -14 (-33%) ✅

## 📈 Ground Truth Atualizado

### Distribuição de Categorias (Apenas Negativas)

| Categoria | Antes | Depois | Mudança |
|-----------|-------|--------|---------|
| **Performance** | 96 (32.8%) | 142 (48.5%) | +46 (+15.7%) ⬆️ |
| **Login/Autenticação** | 55 (18.8%) | 63 (21.5%) | +8 (+2.7%) ⬆️ |
| **Interface/Usabilidade** | 166 (56.7%) | 19 (6.5%) | -147 (-50.2%) ⬇️ |
| **Empréstimos/Crédito** | 28 (9.6%) | 27 (9.2%) | -1 (-0.4%) |
| **PIX** | 24 (8.2%) | 24 (8.2%) | 0 |
| **Outros** | 18 (6.1%) | 20 (6.8%) | +2 (+0.7%) |

**Observações Importantes:**

1. **Performance** agora é a categoria #1 (48.5% das negativas)
2. **Interface/Usabilidade** teve redução drástica (de 56.7% para 6.5%)
   - Isso indica que muitos casos foram reclassificados corretamente
3. **Login/Autenticação** aumentou ligeiramente (de 18.8% para 21.5%)

## 🎯 Próximos Passos

1. ✅ **Inter-Annotator Agreement calculado** - Melhorou significativamente
2. ✅ **Ground Truth atualizado** - Reflete melhor a realidade após alinhamentos
3. 🔄 **Validação do Modelo LLM** - Executar com novo ground truth
4. 📊 **Análise de Resultados** - Comparar métricas antes/depois
5. 🔧 **Ajustes de Prompts** - Se necessário, baseado em erros identificados

## 📋 Status Atual

- ✅ Kappa Médio melhorou: 0.456 → 0.521
- ✅ Discrepâncias reduziram: 456 → 299 (-34%)
- ✅ 7 categorias com concordância substancial (vs. 5 antes)
- ✅ Ground truth atualizado e pronto para validação
- ⚠️ Ainda abaixo da meta de Kappa > 0.7, mas em direção correta

