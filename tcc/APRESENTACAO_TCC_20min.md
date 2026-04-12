# Roteiro de Apresentação TCC – 20 minutos

**Título:** Priorização de Backlog em Apps Bancários via Knowledge Graph e Feedback do Usuário  

**Autora:** Simone Rossetti Nobre Naxara | **Orientadora:** Dra. Anna Carolina Martins

---

## Regra de timing (20 min total)

| Bloco | Tempo | Acumulado |
|-------|-------|-----------|
| Capa + Introdução | 2 min | 2 min |
| Contexto e problema | 2 min | 4 min |
| Objetivos e proposta | 1 min | 5 min |
| Metodologia | 5 min | 10 min |
| Resultados e discussões | 7 min | 17 min |
| Conclusão e próximos passos | 2 min | 19 min |
| Buffer / transição | 1 min | 20 min |

---

## Slide 1: Capa (30 s)

**Conteúdo:**
- Título: Priorização de Backlog em Apps Bancários via Knowledge Graph e Feedback do Usuário
- Autora: Simone Rossetti Nobre Naxara
- Orientadora: Dra. Anna Carolina Martins
- MBA USP/ESALQ – Data Science e Analytics
- Data da apresentação

**Fala sugerida:**
> Bom dia/tarde. O tema da minha apresentação é o uso de Knowledge Graph e IA para priorizar backlog a partir de avaliações de usuários em apps bancários.

---

## Slide 2: Contexto – Mobile banking no Brasil (1 min)

**Conteúdo:**
- Dado FEBRABAN: mais de 75% das transações via mobile
- Dependência tecnológica → qualidade é questão estratégica
- Impacto de problemas: perda de confiança, migração, prejuízos

**Fala sugerida:**
> O mobile banking representa mais de 75% das transações no Brasil. Quando surgem problemas técnicos, as consequências vão além da frustração do usuário: perda de confiança, migração para concorrentes e prejuízos financeiros.

---

## Slide 3: O problema – Lacuna nos testes tradicionais (1 min)

**Conteúdo:**
- Testes ISTQB (unitários, integração, sistema, aceitação) não cobrem cenários de produção
- Em produção aparecem: diversidade de dispositivos, rede, padrões imprevistos
- Avaliações das lojas = termômetro em tempo real, mas pouco exploradas
- Nota de 1–5 estrelas é insuficiente (mesmo negativa pode esconder problemas muito diferentes)

**Fala sugerida:**
> Os testes tradicionais não conseguem reproduzir o ambiente real de produção. As lojas de apps recebem milhares de avaliações textuais, mas monitorar só as notas não basta: uma avaliação negativa pode esconder lentidão, falha no PIX ou cobrança indevida — cada um exigindo equipes diferentes.

---

## Slide 4: Objetivo e proposta (1 min)

**Conteúdo:**
- **Objetivo:** Transformar feedback textual das lojas em documentos estruturados de priorização de backlog
- **Proposta:** Abordagem além da esteira tradicional → testes em produção
- Pipeline: coleta → polarização → extração de entidades → Knowledge Graph → priorização

**Fala sugerida:**
> O objetivo é transformar esse feedback não estruturado em documentos que orientem a priorização do backlog. A proposta é uma abordagem de testes que opera além da esteira de desenvolvimento, usando dados reais de produção.

---

## Slide 5: Arquitetura – Pipeline (visual) (~1 min)

**Conteúdo:**
- **Figura 1** – Pipeline completo
- Dois estágios: (1) Transformer para polarização, (2) LLM para extração e grafo
- Foco visual: fluxo Coleta → BERTweet → GPT-4o → Neo4j → Documentos

**Fala sugerida:**
> A arquitetura é híbrida em dois estágios. Primeiro, o BERTweet classifica polaridade e filtra comentários negativos. Depois, o GPT-4o extrai entidades e modela tudo em um Knowledge Graph no Neo4j, que alimenta os documentos de priorização.

---

## Slide 6: Metodologia – Coleta e dataset (1 min)

**Conteúdo:**
- Google Play Store, app CAIXA
- Coleta validada: 5–18/01/2026 (~13 dias de amplitude), 2.451 avaliações; média ~188/dia (extrap. ~1,3 mil em 7 d.; ~5,6 mil em 30 d.)
- Higienização: remoção de vazios e < 3 palavras (com justificativa breve)
- Atributos: texto, nota 1–5, data, versão

**Fala sugerida:**
> Coletamos avaliações públicas do app CAIXA na Google Play. Foram removidos comentários vazios ou com menos de três palavras, pois não trazem informação suficiente para extrair problemas específicos. A nota do usuário foi usada apenas para severidade, não para validar polaridade.

---

## Slide 7: Metodologia – Modelos (1 min)

**Conteúdo:**
- **Estágio 1:** XLM-RoBERTa (BERTweet) – polarização
- **Estágio 2:** GPT-4o – extração de entidades (temperature 0,1)
- Etapa de reflexão: segunda passada para recuperar entidades perdidas (5–10% a mais)
- Mapeamento para BusinessCapabilities (15 capacidades)

**Fala sugerida:**
> O BERTweet classifica polaridade; o GPT-4o extrai entidades com temperatura 0,1 para consistência. Uma etapa de reflexão faz uma segunda passada e recupera 5 a 10% de entidades que seriam perdidas, especialmente as implícitas ou referenciadas por pronomes.

---

## Slide 8: Metodologia – Knowledge Graph temporal (1 min)

**Conteúdo:**
- Quadro 1 – Estrutura do grafo (App → Version → Episode → Issue → BusinessCapability)
- Três subgrafos: Episódico, Semântico, Comunidade
- Neo4j para armazenamento
- Relacionamentos múltiplos (Issue ↔ várias BusinessCapabilities)

**Fala sugerida:**
> O grafo modela App, Versão, Episódio, Issue e BusinessCapability. Uma mesma issue pode ligar-se a várias capacidades de negócio — por exemplo, “Bloqueio de senha” ligada a Autenticação e Segurança. Isso reflete a natureza transversal dos problemas bancários.

---

## Slide 9: Resultados – Amostra processada (1 min)

**Conteúdo:**
- 2.451 avaliações (5–18 jan/2026)
- 878 negativas (35,82%) → filtro → 763 válidas
- 100 comentários selecionados para processamento completo
- 103 episódios, 85 issues, 15 BusinessCapabilities, 91 relacionamentos

**Fala sugerida:**
> Foram coletadas 2.451 avaliações; o BERTweet classificou 878 como negativas. Após filtrar comentários genéricos, processamos 100 representativos. O resultado: 103 episódios, 85 issues distintas e 91 relacionamentos — mais relacionamentos do que issues, mostrando que várias issues conectam-se a múltiplas capacidades.

---

## Slide 10: Resultados – Comparação de modelos (Figura 2) (1 min)

**Conteúdo:**
- Figura 2 – Comparação GPT (acurácia e distribuição)
- GPT-4o-2024-08-06: 63,6% acurácia, melhor custo-benefício
- Refinamento: 54,5% → 63,6%
- 14 corretos em 22 tentativas

**Fala sugerida:**
> Foram avaliados quatro modelos GPT. O GPT-4o alcançou 63,6% de acurácia após refinamento, equivalente a 14 mapeamentos corretos em 22. Os erros concentram-se em gírias, sarcasmo, múltiplos problemas em um único comentário e referências implícitas.

---

## Slide 11: Resultados – Modelos de polarização (Figuras 3 e 4) (~1 min)

**Conteúdo:**
- BERTweet: 96,17% acurácia vs 74,32% DistilBERT
- ROC AUC: 98,97% vs 78,98%
- Matrizes de confusão
- Boa interpretação de ironias e expressões do domínio

**Fala sugerida:**
> Na polarização, o BERTweet superou claramente o DistilBERT: 96% de acurácia contra 74%, com melhor interpretação de ironias e expressões típicas do setor bancário.

---

## Slide 12: Resultados – Estatísticas do grafo (Tabela 1) (~1 min)

**Conteúdo:**
- Tabela 1: 103 episódios, 85 issues, 15 BCs, 91 relacionamentos
- Achado principal: 91 > 85 → natureza transversal
- Exemplo: “Bloqueio de Senha” → Autenticação + Segurança
- Cobertura de 100% para mapeamento em BusinessCapability

**Fala sugerida:**
> O fato de termos 91 relacionamentos para 85 issues mostra que o modelo captura problemas transversais. Por exemplo, “Bloqueio de Senha” conecta Autenticação e Segurança, permitindo que equipes diferentes entendam o impacto completo.

---

## Slide 13: Resultados – Distribuição e Top 10 (2 min)

**Conteúdo:**
- Figura 5 – Distribuição por BusinessCapability
- Performance e Estabilidade: 23,53% (20 de 85)
- Top 3: Performance, Gestão de Cadastro, Autenticação
- Figura 6 – Top 10 issues (Lentidão em 7 episódios)

**Fala sugerida:**
> Performance e Estabilidade concentra 23,5% das issues — lentidão, travamentos, indisponibilidade. Em seguida vêm Gestão de Cadastro e Autenticação. “Lentidão” aparece em 7 episódios, sendo a issue mais crítica. Cerca de 65% das issues estão em capacidades de alto valor de negócio.

---

## Slide 14: Resultados – SNA e centralidade (1 min)

**Conteúdo:**
- Figura 8 e 9 – Degree Centrality, Clustering Coefficient
- 93% das issues com degree 1; 6 issues com degree 2 (todas ligadas a senha)
- Clustering de senha: 0,91 → cluster denso
- Métricas: Betweenness e Closeness para “pontes” e impacto amplo

**Fala sugerida:**
> As métricas de SNA revelam que as issues de senha formam um cluster denso, com clustering coefficient de 0,91. São problemas transversais que conectam Autenticação e Segurança e tendem a ocorrer em conjunto, sugerindo que uma correção pode impactar várias áreas.

---

## Slide 15: Exemplo qualitativo (30 s)

**Conteúdo:**
- Comentário: *“Depois que atualizou o app, não reconhece a biometria, tem que ficar colocando a senha”*
- Entidades extraídas: “Não reconhece biometria”, “Inserir senha”
- Mapeamento: Login/Autenticação + Segurança e Proteção

**Fala sugerida:**
> Um exemplo rápido: do comentário “não reconhece biometria, tem que ficar colocando a senha”, o sistema extraiu duas issues e mapeou para Login e Segurança, mostrando como a abordagem opera na prática.

---

## Slide 16: Conclusão (1 min)

**Conteúdo:**
- Viabilidade demonstrada para transformar feedback em documentos estruturados
- 85 issues extraídas, 63,6% acurácia no mapeamento, 100% cobertura
- Triagem automática: 13,1% de comentários genéricos removidos
- Reflexão: +5–10% de entidades recuperadas
- Potencial de escala e integração com BI/Jira

**Fala sugerida:**
> Os resultados obtidos indicam viabilidade técnica. O sistema extraiu 85 issues, alcançou 63,6% de acurácia no mapeamento e cobertura total para BusinessCapability. A triagem eliminou 13% de comentários genéricos e a etapa de reflexão recuperou de 5 a 10% de entidades adicionais. A abordagem tem potencial para escalar e se integrar com BI ou Jira.

---

## Slide 17: Limitações e próximos passos (1 min)

**Conteúdo:**
- **Limitações:** Amostra de 100 comentários; validação temporal ainda não feita; processamento sequencial
- **Próximos passos:** Expandir amostra, validação com especialistas, processamento paralelo, templates automáticos de priorização

**Fala sugerida:**
> As limitações incluem a amostra preliminar e a validação temporal ainda pendente. Nos próximos passos, planejo expandir a amostra, validar com especialistas de produto e implementar processamento paralelo e templates automáticos de priorização.

---

## Slide 18: Obrigada / Perguntas

**Conteúdo:**
- Obrigada
- Perguntas?
- Contato: simone-rossetti@usp.br

---

## Checklist de imagens para slides

Incluir no PowerPoint (de `Documentos/imagens_tcc/`):
- [ ] `pipeline_processamento.png` – Slide 5
- [ ] `comparacao_modelos_gpt.png` – Slide 10
- [ ] `comparacao_modelos_sentimentos.png` – Slide 11
- [ ] `matriz_confusao_sentimentos.png` – Slide 11
- [ ] `distribuicao_issues_capabilities.png` – Slide 13
- [ ] `top_10_issues.png` – Slide 13
- [ ] `sna_degree_centrality.png` – Slide 14
- [ ] `sna_metricas_combinadas.png` – Slide 14

---

## Dicas para apresentação

1. **Ensaio:** Pratique 2–3 vezes com cronômetro; deixe 1–2 min de folga para imprevistos.
2. **Ritmo:** Slides 9–14 concentram os resultados; não ultrapasse ~1 min por slide.
3. **Figuras:** Explique o que cada gráfico mostra antes de comentar os valores.
4. **Transições:** Use frases curtas entre slides (ex.: “Com isso, vamos aos resultados”).
5. **Perguntas:** Tenha em mente respostas curtas sobre: amostra, escolha dos modelos, natureza transversal do grafo e limitações.
