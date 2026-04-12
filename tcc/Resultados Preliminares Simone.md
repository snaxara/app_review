# Testes de Qualidade Além da Esteira: Priorização de Backlog em Apps Bancários via Knowledge Graph e Feedback do Usuário

**Trabalho de Conclusão de Curso apresentado para obtenção do título de especialista em Data Science e Analytics - 2025**

**Autora:** Simone Rossetti Nobre Naxara¹*  
**Orientadora:** Dra. Anna Carolina Martins²  
¹ *xxxx*  
² *USP/ESALQ. Doutora em Economia, professora orientadora. Rua Alexandre Herculano 120, Piracicaba, SP, 13418-445, Brasil.*  
*autor correspondente: simone-rossetti@usp.br*

---

## Resumo

A garantia de qualidade em aplicativos bancários requer identificação proativa de falhas técnicas que emergem em produção, após o ciclo tradicional de testes. O volume massivo de avaliações não estruturadas nas lojas de aplicativos representa uma fonte valiosa de feedback do usuário final, mas permanece subutilizada para priorização de backlog. O objetivo deste trabalho foi desenvolver uma abordagem de testes de qualidade além da esteira de desenvolvimento, utilizando **Knowledge Graph** e **Inteligência Artificial** para automatizar a extração de issues de comentários de usuários, correlacioná-los com capacidades de negócio (**BusinessCapability**) e identificar bugs associados a versões específicas do aplicativo, gerando documentos de priorização de backlog baseados em dados reais de produção.

Diferente de abordagens tradicionais de testes que se limitam ao ciclo de desenvolvimento, esta solução propõe uma forma complementar de testes de qualidade que ocorre além do final da esteira, utilizando feedback real de usuários em produção. A solução utiliza uma arquitetura híbrida em dois estágios: o modelo **XLM-RoBERTa (BERTweet)** para análise de polarização do comentário e o LLM **GPT-4o** para extração de entidades (issues) dos comentários. As entidades extraídas são modeladas em um Knowledge Graph temporal utilizando uma implementação própria e armazenadas no **Neo4j**, permitindo estabelecer relacionamentos entre issues, versões do aplicativo e BusinessCapability, gerando documentos estruturados de priorização de backlog.

O estudo de caso utilizou dados recentes (janela de 15 dias) do aplicativo **CAIXA** na Google Play Store. Foram coletadas 2.451 avaliações, das quais 878 foram classificadas como negativas (35.82%). Após filtro de triagem automática que removeu 13.1% de comentários genéricos sem informação útil, foram processados 100 comentários negativos representativos. Os resultados preliminares demonstram que a solução é capaz de extrair 87 issues únicas de comentários com taxa de cobertura de 100% para mapeamento em BusinessCapability. A estrutura do Knowledge Graph permite análises multidimensionais que identificam não apenas problemas isolados, mas padrões sistemáticos de bugs associados a versões específicas, com distribuição equilibrada entre 13 BusinessCapabilities diferentes. As issues mais críticas identificadas foram relacionadas a Performance e Estabilidade (21.51%), Gestão de Cadastro e Conta (17.20%), Autenticação e Acesso (9.68%), Transferências PIX (9.68%) e Segurança e Proteção (7.53%), gerando documentos de priorização de backlog acionáveis para equipes de qualidade e desenvolvimento.

**Palavras-chave:** Testes de Qualidade; Mobile Banking; Análise de Polarização; Knowledge Graph; Priorização de Backlog; QA; Feedback do Usuário Final; NLP; LLM; Social Network Analysis.

---

## Introdução

A transformação digital do setor financeiro consolidou os aplicativos móveis como o principal canal de relacionamento bancário no Brasil. Segundo a **FEBRABAN (2024)**, o mobile banking responde por mais de 75% das transações realizadas no país. Diante dessa alta dependência tecnológica, garantir qualidade torna-se essencial para a continuidade dos negócios. Problemas técnicos podem levar à perda de confiança dos usuários, abandono do aplicativo e impactos financeiros consideráveis (Anouze et al., 2019).

Os testes de qualidade tradicionais, executados durante o ciclo de desenvolvimento conforme definido pelo **ISTQB** (testes unitários, integração, sistema e aceitação) (ISTQB, 2023), são fundamentais, mas não conseguem capturar todos os cenários de uso real. Em produção, problemas emergem devido à diversidade de dispositivos, condições de rede variáveis, padrões de uso não previstos e interações complexas que não são reproduzíveis em ambientes controlados.

As lojas de aplicativos (Google Play e Apple Store) funcionam como termômetros em tempo real dessa experiência em produção, acumulando um volume massivo de dados textuais não estruturados que representam feedback direto do usuário final. Entretanto, o monitoramento manual ou baseado apenas em métricas quantitativas (nota de 1 a 5 estrelas) mostra-se insuficiente para extrair insights acionáveis.

Trabalhos recentes em Engenharia de Software têm demonstrado que a análise de avaliações de aplicativos pode fornecer insights valiosos sobre problemas técnicos e funcionais (Guzman & Maalej, 2014; Pagano & Maalej, 2013). Estudos nacionais têm contribuído para o avanço do conhecimento em qualidade de software e testes, incluindo pesquisas sobre qualidade em métodos ágeis (Oliveira, 2014), práticas de teste em empresas brasileiras (Nascimento, 2005) e priorização de backlog no setor bancário (Lima & Costa, 2024).

---

## Material e Métodos

A presente pesquisa classifica-se como aplicada e quantitativa. A abordagem técnica foi estruturada em seis etapas sequenciais: coleta de dados, análise de polarização do comentário, extração de entidades, modelagem em Knowledge Graph, análise de métricas de rede (Social Network Analysis) e geração de documentos de priorização.

### Arquitetura Híbrida de Modelagem

Para balancear custo computacional e precisão semântica, desenvolveu-se uma arquitetura híbrida em dois estágios principais:
- **Estágio 1:** Utiliza modelos Transformer pré-treinados (**XLM-RoBERTa**) para classificação de polarização.
- **Estágio 2:** Emprega Large Language Models (**LLMs**) para extração estruturada de entidades e modelagem em Knowledge Graph.

### Coleta e Definição do Dataset

A base de dados foi constituída por avaliações públicas extraídas da Google Play Store, referentes ao aplicativo **CAIXA**. A extração foi automatizada via script em linguagem Python, utilizando a biblioteca `google-play-scraper`. O período de coleta abrangeu uma janela recente de 30 dias.

### Seleção de Modelo e Estudo Comparativo

Os testes preliminares demonstraram que o **XLM-RoBERTa** apresentou superioridade estatística na classificação de polarização de comentários bancários, alcançando acurácia de **96.17%** contra 74.32% do DistilBERT, ROC AUC de 98.97% contra 78.98%, e F1-Score de 96.92% contra 75.26%. O modelo BERTweet lidou melhor com ironias e jargões do setor.

### Modelagem em Knowledge Graph Temporal

A implementação utiliza uma arquitetura de Knowledge Graph temporal composta por três subgrafos interconectados:
- **Subgrafo Episódico (Gₑ):** Preserva o conteúdo bruto original dos comentários ("memória episódica").
- **Subgrafo Semântico (Gₛ):** Contém entidades (nós) conectadas por fatos (edges) com metadados bi-temporais.
- **Subgrafo de Comunidade (Gᴄ):** Agrupa entidades fortemente conectadas em comunidades de alto nível.

O banco de dados **Neo4j** foi escolhido para armazenar o grafo devido à sua capacidade nativa de modelagem de relacionamentos.

---

## Resultados e Discussões

### Amostra Processada

Para validação preliminar, foram processados 100 comentários negativos do aplicativo CAIXA, coletados entre 5 e 18 de janeiro de 2026.

### Estatísticas do Grafo

| Métrica | Quantidade |
| :--- | :--- |
| Episódios (comentários processados) | 103 |
| Entidades extraídas (Issues) | 87 |
| BusinessCapability | 13 |
| Relacionamentos Issue ↔ BusinessCapability | 93 |

### Distribuição de Issues por BusinessCapability

| BusinessCapability | Quantidade de Issues | % do Total | Episódios |
| :--- | :--- | :--- | :--- |
| Performance e Estabilidade | 20 | 21.51% | 29 |
| Gestão de Cadastro e Conta | 16 | 17.20% | 16 |
| Autenticação e Acesso | 9 | 9.68% | 9 |
| Transferências PIX | 9 | 9.68% | 9 |
| Consulta de Saldo e Extrato | 7 | 7.53% | 7 |
| Segurança e Proteção | 7 | 7.53% | 7 |
| Empréstimos e Crédito | 6 | 6.45% | 6 |
| Atendimento ao Cliente | 5 | 5.38% | 5 |
| Interface e Experiência do Usuário | 4 | 4.30% | 5 |
| Pagamentos e Boletos | 5 | 5.38% | 5 |
| Gestão de Tarifas | 2 | 2.15% | 2 |
| Notificações e Alertas | 2 | 2.15% | 2 |
| Acesso Geográfico | 1 | 1.08% | 1 |

---

## Integração no Fluxo Produtivo (API)

A entrega final consiste em uma API desenvolvida em Python que processa as avaliações periodicamente e disponibiliza os resultados em formato estruturado (JSON/CSV). Esta API alimentará um painel de Business Intelligence ou ferramenta de gestão como o **Jira/Knooly**, permitindo que o Product Owner visualize um "Backlog Inteligente".

---

## Considerações Finais

A implementação preliminar demonstrou viabilidade técnica para transformar feedback de usuários em produção em documentos estruturados de priorização de backlog. Os resultados indicam que a extração de entidades é eficaz e o mapeamento para BusinessCapability funciona com alta cobertura (100%). O sistema de triagem filtrou automaticamente 13.1% dos comentários genéricos, melhorando a qualidade do grafo.

---

## Referências

- **ANOUZE, A. L.; ALAMRO, A. S.; AWWAD, A. A.** The effect of complaint handling on customer satisfaction and loyalty in the banking sector. *International Journal of Bank Marketing*, v. 37, n. 4, p. 893-912, 2019.
- **CHEN, J. et al.** Knowledge graph-based bug localization in software systems. *IEEE Transactions on Software Engineering*, v. 48, n. 8, p. 3125-3142, 2022.
- **DEVLIN, J. et al.** BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding. In: *NAACL-HLT 2019*. Minneapolis: Association for Computational Linguistics, 2019. p. 4171-4186.
- **FÁVERO, L. P.; BELFIORE, P.** *Manual de Análise de Dados: Estatística e Machine Learning com Excel®, SPSS®, Stata®, R® e Python®*. 2. ed. Rio de Janeiro: GEN LTC, 2024.
- **FEBRABAN.** *Pesquisa FEBRABAN de Tecnologia Bancária 2024*. São Paulo: Federação Brasileira de Bancos, 2024.
- **LIU, B.** *Sentiment Analysis and Opinion Mining*. Morgan & Claypool Publishers, 2012.
- **ROBINSON, I.; WEBBER, J.; EIFREM, E.** *Graph Databases: New Opportunities for Connected Data*. 2. ed. Sebastopol: O'Reilly Media, 2015.
- **ISTQB.** *ISTQB® Certified Tester Foundation Level Syllabus*. Version 4.0, 2023.
- **NEWMAN, M. E. J.** *Networks: An Introduction*. New York: Oxford University Press, 2010.
- **PINHEIRO, C. A. R.** *Social Network Analysis in Telecommunications*. USA: John Wiley & Sons, 2011.
