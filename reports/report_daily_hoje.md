# Report Daily - O que foi feito hoje

## Data: 09/12/2025

## Resumo Executivo

Hoje foquei em analisar as discrepâncias entre as classificações da Carol e do Samuel, e em criar um guia de anotação detalhado para padronizar o processo de classificação. O objetivo é melhorar a qualidade do ground truth e garantir consistência entre diferentes anotadores.

---

## Atividades Realizadas

### 1. Análise de Discrepâncias entre Classificadores

**Objetivo**: Identificar e entender as principais diferenças entre as classificações da Carol e do Samuel para criar um guia de anotação que resolva essas inconsistências.

**Resultados**:

- **Total de discrepâncias**: 299 casos (reduzido de 456 após ajustes iniciais)
- **Kappa Médio**: 0.521 (melhorou de 0.456)
- **Categorias com concordância substancial (Kappa ≥ 0.6)**: 7 de 16 categorias

**Principais Discrepâncias Identificadas**:

1. **Interface/Usabilidade** (102 discrepâncias)
   - Problema: Muitas avaliações foram classificadas como Interface/Usabilidade quando na verdade eram problemas funcionais específicos
   - Kappa: 0.383 (ainda baixo, mas melhorou de 0.175)
   - Taxa de acordo: 89.8%

2. **Performance** (60 discrepâncias)
   - Problema: Alguns classificadores marcaram Performance quando havia problema funcional específico mencionado
   - Kappa: 0.727 (melhorou significativamente de 0.534)
   - Taxa de acordo: 94.0%

3. **Login/Autenticação** (28 discrepâncias)
   - Problema: Confusão entre bloqueio por segurança e problema de login
   - Kappa: 0.711 (melhorou significativamente de 0.399)
   - Taxa de acordo: 97.2%

**Categorias com Excelente Concordância**:
- Notificações: Kappa 1.000 (concordância perfeita)
- PIX: Kappa 0.915 (quase perfeita)
- Empréstimos/Crédito: Kappa 0.835 (quase perfeita)
- Atendimento: Kappa 0.743 (substancial)
- Tarifas/Cobranças: Kappa 0.749 (substancial)

---

### 2. Criação do Guia de Anotação

**Objetivo**: Criar um documento completo e detalhado que padronize o processo de classificação, resolvendo as discrepâncias identificadas.

**Conteúdo do Guia**:

1. **Princípios Fundamentais**:
   - Classificação multi-label (múltiplas categorias por avaliação)
   - Foco em problemas funcionais
   - Consistência entre classificadores

2. **Processo de Classificação**:
   - Passo 1: Análise de sentimento
   - Passo 2: Identificação de funcionalidades
   - Passo 3: Classificação multi-label

3. **Taxonomia Completa de 17 Categorias**:
   - Descrição detalhada de cada categoria
   - Palavras-chave
   - Exemplos de inclusão e exclusão
   - Casos especiais

4. **Casos Complexos e Resolução de Conflitos**:
   - Múltiplas funcionalidades
   - Interface vs. Funcionalidade
   - Performance vs. Funcionalidade
   - Segurança vs. Login/Autenticação
   - Notificações vs. Funcionalidade

5. **Checklist de Classificação**:
   - Lista de verificação antes de finalizar
   - Resolução de discrepâncias principais

**Arquivo Criado**: `guia_anotacao_classificacao.md`

---

### 3. Atualização do Ground Truth

**Resultado**: Ground truth atualizado com base nos alinhamentos realizados:
- Total: 1000 avaliações
- Negativas: 293 avaliações
- Estratégia: Majority (se pelo menos um classificador marcou, marca)

**Distribuição Atualizada**:
- Performance: 142 casos (48.5%) - agora é a categoria #1
- Login/Autenticação: 63 casos (21.5%)
- Interface/Usabilidade: 19 casos (6.5%) - redução significativa após reclassificação

---

## Métricas de Qualidade

### Inter-Annotator Agreement

| Métrica | Valor Atual | Meta | Status |
|---------|-------------|------|--------|
| Kappa Médio | 0.521 | > 0.7 | ⚠️ Abaixo da meta, mas melhorando |
| Categorias com Kappa ≥ 0.6 | 7/16 (44%) | 80% | ⚠️ Abaixo da meta |
| Total de Discrepâncias | 299 | - | ✅ Reduzido em 34% |

### Validação do Modelo LLM

**Categorização**:
- Média F1-Score: 57.06%
- Categorias com F1 > 80%: 5/16 (31%)
- Status: ⚠️ Abaixo da meta (80% das categorias com F1 > 80%)

**Priorização**:
- Correlação Spearman: 0.821 ✅ (meta: > 0.7)
- Top-3 Acurácia: 100.0% ✅ (meta: > 70%)

---

## Entregas

1. ✅ **Guia de Anotação Completo** (`guia_anotacao_classificacao.md`)
   - 17 categorias detalhadas
   - Exemplos e contra-exemplos
   - Casos complexos resolvidos
   - Checklist de classificação

2. ✅ **Análise de Discrepâncias**
   - Identificação das principais inconsistências
   - Métricas de concordância por categoria
   - Redução de 34% nas discrepâncias

3. ✅ **Ground Truth Atualizado** (`ground_truth_dataset.csv`)
   - 1000 avaliações classificadas
   - Base consolidada para validação do modelo

---

## Próximos Passos (Amanhã)

1. Revisar o guia de anotação com a equipe
2. Aplicar o guia em novas classificações
3. Validar se o guia reduz discrepâncias
4. Preparar apresentação dos resultados para o gestor
5. Alinhar expectativas sobre resultados similares ao AppFollow

---

## Observações

- O gestor mencionou que espera resultados similares ao AppFollow (https://watch.appfollow.io/apps/my-first-workspace/app/591111)
- Isso sugere necessidade de dashboards visuais, análises de tendências e métricas de negócio
- O guia de anotação criado hoje é fundamental para garantir qualidade dos dados que alimentarão essas análises

---

## Bloqueadores / Riscos

- Nenhum bloqueador identificado
- Risco: Se o guia não for seguido consistentemente, as discrepâncias podem aumentar novamente
- Mitigação: Revisar o guia com a equipe antes de aplicar em novas classificações

