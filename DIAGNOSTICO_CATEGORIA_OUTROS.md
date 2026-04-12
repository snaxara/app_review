# Diagnóstico: Categoria "Outros" / "Outras Funcionalidades"

## Data: 28 de Janeiro de 2026

## Status Atual Identificado

### ✅ Dados Encontrados

1. **Arquivo de Classificação Funcional** (`functional_correlation_results.csv`):
   - Total de comentários: **3.019**
   - Comentários classificados como "Outros": **334 (11.06%)**
   - ✅ Categoria "Outros" existe e está sendo usada

2. **Métricas do Knowledge Graph** (`reports/metrics_caixa_refinado.csv`):
   - Total de Issues Extraídas: **87**
   - Total de Relacionamentos: **93**
   - BusinessCapabilities: **13**
   - Issues em "Outras Funcionalidades": **0** ❌

### ❌ Problema Identificado

**Nenhuma issue está mapeada para "Outras Funcionalidades" no Knowledge Graph**, mesmo que:
- A categoria "Outros" existe na classificação funcional
- 334 comentários (11.06%) foram classificados como "Outros"
- A BusinessCapability "Outras Funcionalidades" deveria existir no grafo

### 🔍 Possíveis Causas

1. **Comentários "Outros" não foram processados**: Os 100 comentários selecionados para processamento podem não ter incluído comentários classificados como "Outros"
2. **Filtragem pré-processamento**: Comentários "Outros" podem ter sido filtrados antes do processamento no Knowledge Graph
3. **Mapeamento não funciona**: O mapeamento "Outros" → "Outras Funcionalidades" pode não estar funcionando corretamente
4. **BusinessCapability não existe**: A BusinessCapability "Outras Funcionalidades" pode não ter sido criada no Neo4j

## Cálculo Atual de Cobertura

Com base nos dados atuais:
- **Total de Issues Extraídas**: 87
- **Issues em "Outras Funcionalidades"**: 0
- **Issues Mapeadas para Capabilities Específicas**: 87
- **Percentual de Cobertura**: **100%** (87/87)

⚠️ **PROBLEMA**: Este cálculo está incorreto porque:
- Não sabemos quantos comentários "Outros" foram processados
- Se houver comentários "Outros" processados mas não mapeados, o percentual real seria menor

## Próximos Passos para Reprocessamento

### 1. Verificar Dados no Neo4j
- [ ] Conectar ao Neo4j e verificar se BusinessCapability "Outras Funcionalidades" existe
- [ ] Verificar se há issues sem BusinessCapability associada
- [ ] Verificar quais comentários foram processados (103 episódios mencionados no TCC)

### 2. Identificar Comentários "Outros" Processados
- [ ] Verificar quais dos 100 comentários processados foram classificados como "Outros"
- [ ] Verificar se esses comentários geraram issues no grafo
- [ ] Verificar se essas issues foram mapeadas para alguma BusinessCapability

### 3. Corrigir Mapeamento (se necessário)
- [ ] Garantir que BusinessCapability "Outras Funcionalidades" existe no Neo4j
- [ ] Verificar/corrigir mapeamento "Outros" → "Outras Funcionalidades"
- [ ] Testar mapeamento com amostra pequena

### 4. Reprocessar (se necessário)
- [ ] Se houver issues não mapeadas → Mapear para "Outras Funcionalidades"
- [ ] Se houver comentários "Outros" não processados → Decidir se devem ser processados
- [ ] Recalcular métricas incluindo "Outras Funcionalidades"

### 5. Calcular Percentual Real
- [ ] Contar total de issues extraídas (incluindo "Outras Funcionalidades")
- [ ] Calcular: (issues mapeadas - issues em "Outras") / total × 100
- [ ] Atualizar TCC com percentual correto

## Observações Importantes

1. **Transparência**: Incluir "Outras Funcionalidades" nas tabelas e gráficos para transparência, mas excluir do cálculo de cobertura conforme solicitado.

2. **Dados do TCC**: O documento menciona:
   - 87 issues extraídas ✅ (confere com `metrics_caixa_refinado.csv`)
   - 93 relacionamentos ✅ (confere)
   - 13 BusinessCapabilities ✅ (confere)
   - 103 episódios processados (precisa verificar)

3. **Discrepância**: O arquivo `metrics_caixa_100_comments.csv` tem 176 issues, mas o TCC usa `metrics_caixa_refinado.csv` com 87 issues. O arquivo refinado é o correto.

## Recomendação

**Antes de reprocessar tudo**, recomendo:

1. ✅ Verificar no Neo4j se há issues sem BusinessCapability ou mapeadas para "Outras Funcionalidades"
2. ✅ Verificar quais dos 100 comentários foram classificados como "Outros"
3. ✅ Se houver issues não mapeadas → Mapear para "Outras Funcionalidades"
4. ✅ Recalcular métricas e percentual de cobertura
5. ✅ Atualizar TCC com números corretos

**Se não houver issues em "Outras Funcionalidades"** após verificação:
- O percentual de 100% está correto (87/87)
- Mas é importante documentar que comentários "Outros" não foram incluídos na amostra processada
- Ou que foram filtrados antes do processamento
