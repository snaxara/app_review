# Comparação: 20 vs 100 Comentários Processados

## Data: 16/01/2026
## Modelo: gpt-4o-2024-08-06 (vencedor)

---

## Resumo Executivo

Processamento de **100 comentários negativos** do Santander concluído com sucesso usando o modelo vencedor (`gpt-4o-2024-08-06`). Comparação com resultados anteriores de 20 comentários mostra escalabilidade e consistência do pipeline.

---

## Comparação de Métricas

### Escala de Processamento

| Métrica | 20 Comentários | 100 Comentários | Variação |
|---------|----------------|-----------------|----------|
| **Comentários Processados** | 20 | 91* | +355% |
| **Issues Extraídas** | 52-57 | 202 | +255% |
| **BusinessCapabilities** | 12-13 | 14 | +7% |
| **Episódios** | 53-58 | 237 | +308% |
| **Erros** | 0 | 0 | ✅ |

*Nota: 91 comentários únicos após filtro de triagem (9 comentários genéricos foram filtrados)

---

## Distribuição por BusinessCapability

### Top 5 BusinessCapabilities (100 comentários)

1. **Performance e Estabilidade**: 115 issues (56.10%) | 143 episódios (60.34%)
2. **Atendimento ao Cliente**: 14 issues (6.83%) | 14 episódios (5.91%)
3. **Pagamentos e Boletos**: 13 issues (6.34%) | 13 episódios (5.49%)
4. **Autenticação e Acesso**: 12 issues (5.85%) | 12 episódios (5.06%)
5. **Segurança e Proteção**: 12 issues (5.85%) | 12 episódios (5.06%)

### Comparação com 20 Comentários

**Padrões Mantidos:**
- ✅ **Performance e Estabilidade** continua sendo a BusinessCapability mais crítica (56% vs 41% anterior)
- ✅ Distribuição proporcional similar entre outras capabilities
- ✅ Zero erros em ambos os processamentos

**Diferenças Observadas:**
- Mais diversidade de Issues em 100 comentários (202 vs 52-57)
- "Problemas de Abertura do App" aparece como Issue mais frequente (16 episódios)
- Maior cobertura de BusinessCapabilities (14 vs 12-13)

---

## Top 10 Issues Mais Críticas (100 comentários)

1. **Problemas de Abertura do App**: 16 episódios → Performance e Estabilidade
2. **Lentidão**: 6 episódios → Performance e Estabilidade
3. **Erro ao fazer PIX**: 4 episódios → Transferências PIX
4. **Bug**: 3 episódios → Performance e Estabilidade
5. **Acesso com biometria pede senha**: 2 episódios → Autenticação e Acesso / Segurança
6. **Atualização do aplicativo**: 2 episódios → Performance e Estabilidade
7. **Bugs frequentes**: 2 episódios → Performance e Estabilidade
8. **Frustração do Usuário**: 2 episódios → Performance e Estabilidade
9. **Funcionamento do App**: 2 episódios → Performance e Estabilidade
10. **Insatisfação com o Banco**: 2 episódios → Performance e Estabilidade

---

## Análise de Distribuição

### Por Nível de Capability

**100 Comentários:**
- **Nível 1**: 138 issues (68.32%) | 169 episódios (71.31%)
- **Nível 2**: 64 issues (31.68%) | 68 episódios (28.69%)

**20 Comentários:**
- **Nível 1**: 35 issues (58.33%) | 35 episódios (57.38%)
- **Nível 2**: 25 issues (41.67%) | 26 episódios (42.62%)

**Observação:** Padrão similar, com leve aumento na proporção de Nível 1 em escala maior.

### Por Tipo de Capability

**100 Comentários:**
- **Core**: 53 issues (26.24%) | 59 episódios (24.89%)
- **Strategic**: 4 issues (1.98%) | 4 episódios (1.69%)
- **Supporting**: 145 issues (71.78%) | 174 episódios (73.42%)

**20 Comentários:**
- **Core**: 14 issues (23.33%) | 15 episódios (24.59%)
- **Strategic**: 3 issues (5.00%) | 3 episódios (4.92%)
- **Supporting**: 43 issues (71.67%) | 43 episódios (70.49%)

**Observação:** Distribuição muito consistente entre escalas.

### Por Valor de Negócio

**100 Comentários:**
- **High**: 172 issues (85.15%) | 206 episódios (86.92%)
- **Medium**: 29 issues (14.36%) | 30 episódios (12.66%)
- **Low**: 1 issue (0.50%) | 1 episódio (0.42%)

**20 Comentários:**
- **High**: 42 issues (70.00%) | 43 episódios (70.49%)
- **Medium**: 18 issues (30.00%) | 18 episódios (29.51%)

**Observação:** Aumento na proporção de Issues de alto valor de negócio em escala maior.

---

## Insights e Observações

### ✅ Pontos Positivos

1. **Escalabilidade Confirmada**: Pipeline processou 100 comentários sem erros
2. **Consistência**: Padrões de distribuição se mantêm entre 20 e 100 comentários
3. **Cobertura**: 14 BusinessCapabilities diferentes identificadas
4. **Qualidade**: Zero erros de processamento

### 📊 Padrões Identificados

1. **Performance e Estabilidade** é consistentemente a área mais crítica
2. **"Problemas de Abertura do App"** aparece como Issue mais frequente em escala maior
3. **PIX** continua sendo uma área crítica (4 episódios de erro)
4. **Issues de alto valor de negócio** representam 85% do total

### 🔍 Áreas de Atenção

1. **Performance e Estabilidade** concentra 56% das Issues - área prioritária
2. **PIX** tem 4 episódios de erro - funcionalidade crítica
3. **Autenticação e Acesso** + **Segurança** juntas têm 24 issues - área sensível

---

## Arquivos Gerados

- `reports/model_data_gpt-4o-2024-08-06.csv` - Dados completos dos 100 comentários
- `reports/metrics_100_comments_gpt4o.txt` - Relatório de métricas detalhado
- `reports/metrics_100_comments_gpt4o.csv` - Dados em formato tabular
- `reports/metrics_100_comments_gpt4o.json` - Dados estruturados em JSON

---

## Conclusões

1. ✅ **Pipeline validado em escala**: 100 comentários processados com sucesso
2. ✅ **Modelo vencedor confirmado**: `gpt-4o-2024-08-06` mantém boa performance
3. ✅ **Padrões consistentes**: Distribuição similar entre 20 e 100 comentários
4. ✅ **Pronto para produção**: Sistema pode processar volumes maiores

---

## Próximos Passos Recomendados

1. **Processar todos os 470 comentários negativos** coletados
2. **Análise temporal**: Correlacionar Issues com versões do app
3. **Dashboard**: Criar visualizações interativas das métricas
4. **Priorização automática**: Desenvolver algoritmo de backlog baseado nas métricas

---

**Última atualização:** 16/01/2026
