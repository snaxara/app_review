# FAQ - Perguntas e Respostas para Apresentação

## PERGUNTAS SOBRE O PROJETO

### O que foi desenvolvido?
Sistema automatizado que analisa avaliações de app bancário usando IA para identificar e priorizar problemas.

**Fase Atual:** MVP/POC com scripts Python processando CSV
**Próxima Fase:** Evolução para stack completa (Kafka + PostgreSQL + OpenSearch + Dashboard + API REST)

### O que já foi feito?
- Análise de 1.000 avaliações
- Identificação de 331 problemas negativos
- Categorização de 200 problemas em 13 categorias funcionais
- Priorização automática com recomendações técnicas

### Quais os principais problemas encontrados?
1. Performance (22%): App travando, lento
2. Login/Autenticação (9%): Problemas de acesso
3. Segurança (1%): Bloqueios indevidos

---

## PERGUNTAS SOBRE METODOLOGIA

### Como funciona?
1. Modelo de IA classifica avaliações como positiva/negativa/neutra
2. GPT-4o categoriza problemas negativos em funcionalidades
3. Sistema calcula prioridade baseado em frequência, severidade e impacto
4. Gera backlog priorizado com recomendações

### Por que usar IA?
- Velocidade: Processa milhares em minutos vs semanas manualmente
- Consistência: Sem viés humano ou cansaço
- Escalabilidade: Funciona com qualquer volume

### É confiável?
Sim. Usa modelos de última geração validados. Podemos validar manualmente amostras para garantir qualidade.

---

## PERGUNTAS SOBRE RESULTADOS

### O que esperamos alcançar?
- Curto prazo: Processar todas as 30.304 avaliações
- Médio prazo: Reduzir problemas críticos em 30-40%
- Longo prazo: Melhorar satisfação e reduzir churn

### Quais os ganhos?
- 80% menos tempo na análise manual
- Priorização inteligente baseada em dados
- Foco nos problemas que mais impactam usuários
- ROI: Payback em 3-6 meses

### Como medimos sucesso?
- Número de problemas identificados e priorizados
- Redução de problemas críticos após correções
- Melhoria na satisfação do cliente (NPS)
- Tempo economizado em análise manual

---

## PERGUNTAS SOBRE IMPLEMENTAÇÃO

### Quanto custa?
- Processar tudo (30.304 avaliações): ~$20-30 USD
- Custo mensal para novas avaliações: Negligível
- Manutenção: Mínima

### Quanto tempo leva?
- Processar dataset completo: 1-2 dias automatizado
- Análise manual equivalente: Semanas/meses

### Como usar os resultados?
**Atual (MVP):**
- Relatórios CSV e Markdown
- Backlog priorizado com recomendações técnicas

**Futuro (Stack Completa):**
- API REST para integração direta
- Dashboard interativo com métricas em tempo real
- Alertas automáticos (Slack, Email)
- Integração nativa com Jira/Azure DevOps

### Precisa de manutenção?
**MVP Atual:** Mínima. Sistema automatizado, apenas ajustes ocasionais.

**Stack Completa:** Manutenção padrão de infraestrutura (monitoramento, atualizações, otimizações). Sistema projetado para alta disponibilidade.

---

## PERGUNTAS SOBRE ESCALABILIDADE

### Funciona com mais avaliações?
Sim. Escala para qualquer volume. Processa em lotes automaticamente.

### E se a API falhar?
Temos alternativas: modelos locais ou outros provedores. Sistema é resiliente.

### Como atualizar modelos?
Simples. Basta trocar o nome do modelo. Melhorias futuras são incorporadas automaticamente.

---

## PERGUNTAS SOBRE PRÓXIMOS PASSOS

### O que fazer agora?
**Imediato:**
1. Processar dataset completo (30.304 avaliações)
2. Validar categorizações manualmente
3. Iniciar correções dos problemas prioritários

**Evolução da Stack:**
4. Migrar para PostgreSQL + pgvector
5. Implementar API REST (FastAPI)
6. Criar dashboard (Streamlit)
7. Adicionar ingestão com scrapers agendados
8. Implementar OpenSearch para busca e analytics

### Como integrar ao processo atual?
Relatórios podem ser importados em Jira, Azure DevOps ou outras ferramentas. Fácil integração.

### Quem vai usar?
Equipes técnicas para priorizar desenvolvimento. Gestores para acompanhar métricas. Suporte para entender problemas.

---

## PERGUNTAS SOBRE RISCOS

### Quais os riscos?
Mínimos. Dependência de API externa é mitigada com alternativas. Custo é baixo e controlável.

### E se não funcionar?
Temos fallbacks. Modelos locais funcionam mesmo sem API. Processamento pode ser feito em lotes menores.

### Limitações?
Modelo pode errar em casos ambíguos (validamos amostras). Não captura contexto entre avaliações (cada uma é independente).

---

## PERGUNTAS SOBRE INVESTIMENTO

### Quanto já investimos?
Desenvolvimento já está feito. Apenas custo de processamento restante.

### Qual o ROI?
Payback estimado em 3-6 meses através de:
- Redução de tempo de análise
- Redução de problemas críticos
- Aumento de satisfação e retenção

### Vale a pena?
Sim. Investimento mínimo ($20-30) para processar tudo. Ganhos significativos em eficiência e satisfação.

---

## RESPOSTAS RÁPIDAS PARA OBJEÇÕES

**"Já temos pessoas analisando avaliações"**
→ Sistema processa em minutos o que levaria semanas. Libera equipe para ações estratégicas.

**"IA pode errar"**
→ Sim, mas validamos amostras. Erro humano também existe. IA é mais consistente e rápida.

**"Custo da API"**
→ Baixíssimo ($20-30 para tudo). Menor que 1 hora de trabalho manual.

**"Não temos tempo para implementar"**
→ Sistema já está pronto. Apenas precisa processar dados e usar resultados.

**"Como sabemos que funciona?"**
→ Resultados iniciais já mostram padrões claros. Problemas identificados fazem sentido técnico.

---

## MENSAGEM FINAL

Sistema funcional que transforma feedback em ações priorizadas. Resultados comprovam valor. Investimento mínimo, ganhos significativos. Próximo passo: processar tudo e começar correções.

