# Decisão: Issue vs Feature na Classificação de Entidades

## Contexto

Durante a análise dos resultados de classificação, identificamos uma confusão sobre quando classificar uma entidade como **Issue** ou **Feature**. Após análise, decidimos simplificar o modelo removendo o tipo Feature.

## Problema Identificado

Nos comentários analisados, encontramos casos onde funcionalidades mencionadas em contexto negativo foram classificadas como **Feature** quando deveriam ser **Issue**:

- "Acesso a Saldo" → Classificado como Feature, mas o comentário dizia "não consigo acessar nada"
- "Refinanciamento" → Classificado como Feature, mas o comentário dizia "não consigo... refinanciar"
- "Atualização de Dados" → Classificado como Feature, mas o comentário dizia "não consegui atualizar"
- "Chat de Suporte" → Classificado como Feature, mas mencionado em contexto negativo

## Decisão Tomada

### **Simplificação: Remover Feature, usar apenas Issue**

Decidimos simplificar o modelo removendo completamente o tipo **Feature** e tratando todas as entidades extraídas de comentários negativos como **Issue**.

### Justificativa da Simplificação

1. **Foco no Objetivo**: O objetivo do sistema é identificar **problemas** para priorizar o backlog de desenvolvimento. Não há necessidade de distinguir entre funcionalidades positivas e problemas.

2. **Comentários Negativos**: Estamos processando apenas comentários **negativos** (avaliações de 1-2 estrelas). Neste contexto, todas as menções são problemas.

3. **Redução de Complexidade**: Remover a distinção Issue/Feature simplifica:
   - O prompt de extração (menos ambiguidade)
   - As queries Cypher (menos condições)
   - A análise de dados (mais direto)

4. **Precisão**: Elimina erros de classificação onde funcionalidades mencionadas como problema eram classificadas como Feature.

## Justificativa

1. **Propósito do Sistema**: O objetivo é identificar **problemas** para priorizar o backlog de desenvolvimento. Portanto, precisamos focar em Issues.

2. **Análise de Sentimento**: Comentários negativos já passaram por análise de sentimento. Se o sentimento é negativo, as entidades mencionadas são problemas.

3. **Precisão na Classificação**: Classificar "Acesso a Saldo" como Feature quando o usuário diz "não consigo acessar" gera ruído na análise e pode mascarar problemas reais.

4. **Consistência**: Manter consistência entre o sentimento do comentário e a classificação da entidade melhora a qualidade dos dados no grafo.

## Implementação

### Ajustes no Prompt de Extração

O prompt foi simplificado para:

1. **Remover referências a Feature** completamente
2. **Classificar todas as entidades como Issue**
3. **Focar em problemas e dificuldades** mencionados

### Exemplos de Classificação

| Entidade | Contexto | Classificação |
|----------|----------|---------------|
| "Acesso a Saldo" | "não consigo acessar saldo" | **Issue** |
| "Refinanciamento" | "não consigo fazer refinanciamento" | **Issue** |
| "Chat de Suporte" | "chat não resolve nada" | **Issue** |
| "Problemas de Abertura" | "não abre conta" | **Issue** (Cadastro/Conta) |
| "Problemas de Abertura" | "app não abre" | **Issue** (Performance) |

## Impacto nos Resultados

Com essa mudança:

- ✅ **Maior precisão** na identificação de problemas
- ✅ **Melhor correlação** entre Issues e BusinessCapabilities
- ✅ **Análise mais focada** em problemas reais do usuário
- ✅ **Redução de ruído** no grafo de conhecimento
- ✅ **Simplificação** do modelo e das queries
- ✅ **Eliminação de ambiguidade** na classificação

## Mudanças Implementadas

1. ✅ Removido tipo Feature do prompt de extração
2. ✅ Todas as entidades são classificadas como Issue
3. ✅ Atualizadas todas as queries Cypher para usar apenas Issue
4. ✅ Atualizado código Python para remover referências a Feature
5. ✅ Documentação atualizada

## Próximos Passos

1. ✅ Ajustar prompt de extração de entidades
2. ✅ Melhorar mapeamento de entidades para BusinessCapability
3. ⏳ Re-processar comentários com o novo prompt
4. ⏳ Calcular métricas de correlação Issues ↔ BusinessCapabilities
5. ⏳ Apresentar resultados ao gestor

## Decisão Final

**Tratar tudo como Issue em comentários negativos e remover o tipo Feature completamente.**

Esta decisão simplifica o modelo, elimina ambiguidade e mantém o foco no objetivo principal: identificar problemas para priorização do backlog.
