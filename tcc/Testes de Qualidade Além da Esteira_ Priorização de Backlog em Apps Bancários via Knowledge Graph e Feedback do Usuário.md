# Testes de Qualidade Além da Esteira: Priorização de Backlog em Apps Bancários via Knowledge Graph e Feedback do Usuário

**Trabalho de Conclusão de Curso apresentado para obtenção do título de especialista em Data Science e Analytics - 2025**

**Autora:** Simone Rossetti Nobre Naxara¹*  
**Orientadora:** Dra. Anna Carolina Martins²  
¹ *autor correspondente: simone-rossetti@usp.br*  
² *Técnica em Redes de computadores pelo Senac, Economista graduada pela Unimontes, Mestre em Economia Aplicada pela UFOP e doutoranda em Economia na Unicamp.*

---

## Resumo

A garantia de qualidade em aplicativos bancários requer identificação proativa de falhas técnicas que emergem em produção, após o ciclo tradicional de testes. O volume massivo de avaliações não estruturadas nas lojas de aplicativos representa uma fonte valiosa de feedback do usuário final, mas permanece subutilizada para priorização de backlog. O objetivo deste trabalho foi desenvolver uma abordagem de testes de qualidade além da esteira de desenvolvimento, utilizando **Knowledge Graph** e **Inteligência Artificial** para automatizar a extração de issues de comentários de usuários, correlacioná-los com capacidades de negócio (**BusinessCapability**) e identificar bugs associados a versões específicas do aplicativo, gerando documentos de priorização de backlog baseados em dados reais de produção.

A solução utiliza uma arquitetura híbrida em dois estágios: o modelo **XLM-RoBERTa (BERTweet)** para análise de polarização e o LLM **GPT-4o** para extração de entidades (issues). As entidades são modeladas em um Knowledge Graph temporal no **Neo4j**. O estudo de caso utilizou dados do aplicativo **CAIXA** na Google Play Store (2.451 avaliações). Os resultados preliminares demonstram que a solução é capaz de extrair 87 issues únicas com taxa de cobertura de 100% para mapeamento em BusinessCapability.

**Palavras-chave:** Testes de Qualidade; Mobile Banking; Análise de Polarização; Knowledge Graph; Priorização de Backlog; QA; Feedback do Usuário Final; NLP; LLM; Social Network Analysis.

---

## Introdução

A transformação digital do setor financeiro consolidou os aplicativos móveis como o principal canal de relacionamento bancário no Brasil. Segundo a FEBRABAN (2024), o mobile banking responde por mais de 75% das transações realizadas no país. Garantir qualidade torna-se essencial para a continuidade dos negócios, pois problemas técnicos podem levar à perda de confiança dos usuários e impactos financeiros consideráveis [1].

Os testes de qualidade tradicionais (unitários, integração, sistema e aceitação) são fundamentais, mas não capturam todos os cenários de uso real. Em produção, problemas emergem devido à diversidade de dispositivos e condições de rede variáveis. As lojas de aplicativos funcionam como termômetros em tempo real dessa experiência, mas o monitoramento manual é insuficiente. Existe uma lacuna na ausência de sistemas automatizados que realizem a extração estruturada de issues e as correlacionem com versões do app e capacidades de negócio.

---

## Material e Métodos

A pesquisa classifica-se como aplicada e quantitativa, estruturada em seis etapas: coleta de dados, análise de polarização, extração de entidades, modelagem em Knowledge Graph, análise de métricas de rede (SNA) e geração de documentos de priorização.

### Arquitetura Híbrida de Modelagem

Desenvolveu-se uma arquitetura em dois estágios:
1.  **Estágio 1:** Classificação de polarização (positivo, negativo, neutro) usando **XLM-RoBERTa**.
2.  **Estágio 2:** Extração de entidades e modelagem em Knowledge Graph usando **GPT-4o**.

### Coleta e Definição do Dataset

Os dados foram extraídos da Google Play Store (app CAIXA, `br.com.gabba.Caixa`) via biblioteca `google-play-scraper`. O período de coleta abrangeu uma janela de 30 dias, capturando conteúdo textual, nota, data e versão do app.

### Seleção de Modelo

Comparou-se o **DistilBERT Multilíngue** com o **BERTweet (XLM-RoBERTa)**. O XLM-RoBERTa apresentou superioridade estatística com acurácia de **96.17%** e F1-Score de **96.92%**.

### Modelagem em Knowledge Graph Temporal

A arquitetura é composta por três subgrafos:
*   **Subgrafo Episódico (Gₑ):** Preserva o conteúdo bruto original (memória episódica).
*   **Subgrafo Semântico (Gₛ):** Contém entidades e fatos com metadados bi-temporais.
*   **Subgrafo de Comunidade (Gᴄ):** Agrupa entidades em comunidades de alto nível.

### Business Capability e Modelagem de Domínio

Foram mapeadas 15 capacidades de negócio, incluindo: Autenticação e Acesso, Performance e Estabilidade, Transferências PIX, entre outras. A modelagem segue os princípios de *Domain-Driven Design* (DDD).

---

## Resultados Preliminares

### Amostra Processada

Foram processados 100 comentários negativos do aplicativo CAIXA (janeiro/2026). A triagem automática removeu 13.1% de comentários genéricos.

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

### Validação com Dados Reais de Defeitos

A análise de 6.644 defeitos reais da Caixa indicou que **67.6%** dos defeitos chegam em produção antes de serem detectados pelos testes tradicionais. Identificou-se uma taxa de correspondência de **25.7%** entre as issues extraídas dos comentários e os defeitos reais registrados.

---

## Considerações Finais

A implementação demonstrou viabilidade técnica para transformar feedback de usuários em documentos estruturados de priorização de backlog. A extração de entidades mostrou-se eficaz, e o mapeamento para BusinessCapability alcançou 100% de cobertura. A solução fornece uma visão adicional da qualidade do produto em ambiente de produção real, complementando os testes tradicionais.

---

## Referências

1.  ANOUZE, A. L.; ALAMRO, A. S.; AWWAD, A. A. The effect of complaint handling on customer satisfaction and loyalty in the banking sector. *International Journal of Bank Marketing*, v. 37, n. 4, p. 893-912, 2019.
2.  FEBRABAN. *Pesquisa FEBRABAN de Tecnologia Bancária 2024*. São Paulo: Federação Brasileira de Bancos, 2024.
3.  ISTQB. *ISTQB® Certified Tester Foundation Level Syllabus*. Version 4.0, 2023.
4.  NEWMAN, M. E. J. *Networks: An Introduction*. New York: Oxford University Press, 2010.
5.  PINHEIRO, C. A. R. *Social Network Analysis in Telecommunications*. USA: John Wiley & Sons, 2011.
6.  FÁVERO, L. P.; BELFIORE, P. *Manual de Análise de Dados*. 2. ed. Rio de Janeiro: GEN LTC, 2024.
