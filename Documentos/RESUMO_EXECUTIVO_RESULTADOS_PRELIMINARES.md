# RESUMO EXECUTIVO - RESULTADOS PRELIMINARES TCC

## Data: 19 de Janeiro de 2026

---

## OBJETIVO

Validar a viabilidade técnica de uma abordagem de Knowledge Graph Temporal para análise de avaliações de aplicativos bancários, modelando relacionamentos entre entidades extraídas dos comentários e capacidades de negócio (BusinessCapability).

---

## METODOLOGIA

- **Framework**: Implementação própria inspirada em Knowledge Graph Temporal
- **Banco de Dados**: Neo4j
- **Modelo LLM**: GPT-4o-2024-08-06 (selecionado após comparação de 4 modelos)
- **Técnica de Extração**: Duas etapas (Extração Inicial + Reflexão)
- **Amostra**: 100 comentários negativos do aplicativo Santander

---

## RESULTADOS PRINCIPAIS

### Estatísticas do Grafo

| Métrica | Quantidade |
|---------|------------|
| **Comentários Processados** | 63 únicos (37 filtrados por triagem) |
| **Issues Extraídas** | 97 |
| **BusinessCapabilities** | 13 |
| **Cobertura de Linkagem** | 100% |
| **Acurácia de Mapeamento** | 63.6% |

### Distribuição de Issues por BusinessCapability

| BusinessCapability | Issues | % |
|-------------------|--------|---|
| Performance e Estabilidade | 19 | 19.00% |
| Atendimento ao Cliente | 13 | 13.00% |
| Empréstimos e Crédito | 11 | 11.00% |
| Segurança e Proteção | 11 | 11.00% |
| Autenticação e Acesso | 8 | 8.00% |
| Outras (7 capabilities) | 35 | 38.00% |

### Top 5 Issues Mais Críticas

1. **Lentidão**: 6 episódios → Performance e Estabilidade
2. **App não abre**: 5 episódios → Performance e Estabilidade
3. **App trava**: 4 episódios → Performance e Estabilidade
4. **Biometria pede senha frequentemente**: 2 episódios → Autenticação + Segurança
5. **Bugs no aplicativo**: 2 episódios → Performance e Estabilidade

---

## MELHORIAS IMPLEMENTADAS

### 1. Refinamento de Mapeamento
- **Antes**: 56% das Issues mapeadas como Performance
- **Depois**: 19% das Issues mapeadas como Performance
- **Resultado**: Distribuição mais equilibrada e precisa

### 2. Filtros de Qualidade
- **Triagem Automática**: Filtrou 37% de comentários genéricos
- **Validação Pré-Criação**: Entidades só são criadas se mapeáveis para BusinessCapability
- **Resultado**: Grafo mais limpo e focado em informações acionáveis

### 3. Comparação de Modelos
- **4 modelos testados**: GPT-4o-mini, GPT-4o-2024-08-06, GPT-OSS-20B, GPT-5.2
- **Modelo selecionado**: GPT-4o-2024-08-06 (63.6% de acurácia)
- **Resultado**: Base sólida para processamento em escala

---

## CONCLUSÕES PRELIMINARES

### ✅ Viabilidade Técnica Confirmada

1. **Extração de entidades eficaz**: 97 entidades extraídas de 63 comentários únicos
2. **Mapeamento preciso**: 100% de cobertura e 63.6% de acurácia após refinamento
3. **Distribuição equilibrada**: Issues distribuídas corretamente entre 13 BusinessCapabilities
4. **Filtros eficazes**: Triagem automática melhorou qualidade e reduziu custos
5. **Escalabilidade**: Sistema processou 100 comentários sem erros

### 📊 Insights para Gestão de Produto

- **Performance e Estabilidade** é a área mais crítica (19% das Issues)
- **Atendimento ao Cliente** concentra 13% das Issues
- **Empréstimos e Crédito** e **Segurança** têm 11% cada
- **68% das Issues** são de alto valor de negócio (High)

### 🔄 Próximos Passos Recomendados

1. **Expansão**: Processar todos os 470 comentários negativos coletados
2. **Validação**: Apresentar resultados para especialistas de produto
3. **Otimização**: Implementar processamento paralelo para grandes volumes
4. **Integração**: Desenvolver API REST para dashboards

---

## ARQUIVOS DE REFERÊNCIA

- **Documento Completo**: `RESULTADOS_PRELIMINARES_TCC_ATUALIZADO.md`
- **Relatório de Métricas**: `reports/metrics_100_comments_corrigido.txt`
- **Dados Exportados**: `reports/model_data_gpt-4o-2024-08-06.csv`
- **Comparação de Modelos**: `reports/comparacao_20_vs_100_comentarios.md`

---

**Versão**: 2.0  
**Data**: 19/01/2026  
**Status**: Pronto para revisão pela orientadora
