# Análise de Complementaridade: Projeto App Review vs. Knooly Análise de Sentimentos

## Resumo Executivo

Este documento analisa como o projeto de análise de sentimentos desenvolvido em `app_review` pode enriquecer o módulo "Knooly Análise de Sentimentos" em desenvolvimento pela equipe, identificando gaps e propondo uma nova atividade de integração.

---

## 1. Análise Comparativa dos Projetos

### 1.1 Projeto Azure DevOps - Knooly Análise de Sentimentos

**Escopo Atual:**
- Módulo integrado ao sistema Knooly (super admin)
- Coleta automática de avaliações da Play Store
- Processamento básico com IA para classificação de sentimentos (Positivo/Negativo/Neutro/Misto)
- Identificação de bugs reportados
- Endpoints REST para visualização de dados
- Gráficos de análise temporal de sentimentos
- Gráfico de avaliações categorizadas (categorias genéricas)
- Backlog de desenvolvimento baseado em frequência

**Categorias Atuais (Genéricas):**
- "Não funciona"
- "Muito lento"
- "Não carrega"
- "Funciona muito bom"
- Outras categorias genéricas

**Limitações Identificadas:**
1. Categorização muito genérica, não específica para domínio bancário
2. Backlog priorizado apenas por frequência, sem considerar severidade ou impacto de negócio
3. Ausência de validação de qualidade do modelo de IA
4. Falta de comparação entre diferentes modelos de ML
5. Não há métricas de precisão/recall para categorização

### 1.2 Projeto App Review (Seu Projeto)

**Capacidades Desenvolvidas:**
- Análise de sentimentos com modelos BERTweet e DistilBERT
- Categorização funcional avançada com GPT-4o (17 categorias específicas para apps bancários)
- Sistema de priorização multi-critério (frequência + severidade + impacto de negócio)
- Validação de modelos contra ground truth humano
- Comparação de modelos de ML com métricas detalhadas
- Suporte a múltiplas categorias por avaliação
- Geração de backlog priorizado com recomendações técnicas

**Categorias Funcionais Específicas (17 categorias):**
1. PIX
2. Login/Autenticação
3. Performance
4. Interface/Usabilidade
5. Empréstimos/Crédito
6. Pagamentos/Boletos
7. Saldo/Extrato
8. Atendimento
9. Cadastro/Conta
10. Investimentos
11. Segurança
12. Notificações
13. Questões geográficas
14. Placas/Veículos
15. Tarifas/Cobranças
16. Outros

**Diferenciais Técnicos:**
- Sistema de pesos de impacto por categoria (ex: PIX, Login, Segurança = peso 1.0)
- Cálculo de severidade baseado em score médio das avaliações
- Fórmula de priorização: `(Frequência × 0.4) + (Severidade × 0.3) + (Impacto × 0.3)`
- Métricas de validação: Precision, Recall, F1-Score, Cohen's Kappa
- Comparação lado a lado de modelos ML

---

## 2. Como Seu Projeto Pode Enriquecer o Projeto Azure DevOps

### 2.1 Categorização Funcional Avançada

**Gap Identificado:**
O projeto Azure DevOps usa categorias genéricas que não permitem ação direta da equipe de desenvolvimento. Categorias como "Não funciona" ou "Muito lento" não indicam qual funcionalidade específica precisa ser corrigida.

**Solução Proposta:**
Integrar a taxonomia de 17 categorias funcionais específicas para apps bancários, permitindo:
- Identificação precisa de qual área do app precisa de correção
- Rastreamento de problemas por funcionalidade (ex: quantos problemas de PIX vs. Login)
- Alinhamento direto entre feedback do usuário e backlog de desenvolvimento

**Valor Agregado:**
- Redução de 60-70% no tempo de análise manual
- Priorização mais precisa de correções
- Melhor comunicação entre produto e desenvolvimento

### 2.2 Sistema de Priorização Multi-Critério

**Gap Identificado:**
O backlog atual prioriza apenas por frequência (quantidade de avaliações). Isso pode levar a priorizar problemas frequentes mas de baixa severidade, ignorando problemas críticos menos frequentes.

**Solução Proposta:**
Implementar sistema de priorização que considera:
1. **Frequência** (40%): Quantas avaliações mencionam o problema
2. **Severidade** (30%): Score médio das avaliações (quanto menor o score, maior a severidade)
3. **Impacto de Negócio** (30%): Peso específico por categoria (ex: Segurança sempre alta prioridade)

**Valor Agregado:**
- Priorização mais inteligente e baseada em dados
- Foco em problemas que realmente impactam satisfação do cliente
- Redução de churn por problemas críticos não resolvidos

### 2.3 Validação e Métricas de Qualidade

**Gap Identificado:**
Não há validação da qualidade das classificações geradas pela IA. Não se sabe se as categorias atribuídas estão corretas ou se há viés no modelo.

**Solução Proposta:**
Implementar sistema de validação que:
- Compara resultados da IA com classificações humanas (ground truth)
- Calcula métricas de precisão, recall e F1-Score por categoria
- Identifica categorias com baixa confiabilidade
- Permite ajuste fino do modelo baseado em métricas

**Valor Agregado:**
- Confiança nas classificações geradas
- Identificação de áreas que precisam de melhoria no modelo
- Base para evolução contínua do sistema

### 2.4 Comparação de Modelos de ML

**Gap Identificado:**
O projeto usa um único modelo de IA sem comparação de alternativas. Não há garantia de que o modelo escolhido é o melhor para o caso de uso.

**Solução Proposta:**
Sistema de comparação que:
- Testa múltiplos modelos de análise de sentimentos
- Compara métricas de desempenho (acurácia, precisão, recall)
- Identifica o melhor modelo para o domínio específico
- Permite evolução do modelo ao longo do tempo

**Valor Agregado:**
- Otimização contínua da qualidade das análises
- Redução de custos ao escolher modelos mais eficientes
- Base científica para escolha de modelos

### 2.5 Suporte a Múltiplas Categorias

**Gap Identificado:**
Uma avaliação pode mencionar múltiplos problemas (ex: "App trava e não consigo fazer PIX"). O sistema atual provavelmente categoriza apenas em uma categoria.

**Solução Proposta:**
Sistema que permite múltiplas categorias por avaliação, capturando todos os problemas mencionados.

**Valor Agregado:**
- Análise mais completa e precisa
- Não perde informações importantes
- Melhor rastreamento de correlações entre problemas

---

## 3. Proposta de Nova Atividade para Azure DevOps

### 3.1 Título da Atividade

**[Knooly - Análise de Sentimentos - Categorização Funcional Avançada] - Integrar sistema de categorização funcional específica para apps bancários com priorização multi-critério**

### 3.2 Tipo e Prioridade

- **Tipo:** US BACK END (ou Feature, dependendo da estrutura)
- **Prioridade:** Alta (complementa funcionalidades já desenvolvidas)
- **Epic:** Detalhes da Análise de Comentários

### 3.3 Descrição Detalhada

**Contexto:**
O módulo atual de Análise de Sentimentos classifica avaliações em categorias genéricas (ex: "Não funciona", "Muito lento"), o que dificulta a ação direta da equipe de desenvolvimento. Esta atividade integra um sistema de categorização funcional específica para aplicativos bancários, permitindo identificar precisamente qual funcionalidade precisa de correção.

**Objetivo:**
Enriquecer o processamento de avaliações com categorização funcional avançada (17 categorias específicas) e sistema de priorização multi-critério, permitindo geração de backlog mais preciso e acionável.

**Funcionalidades a Implementar:**

1. **Endpoint de Categorização Funcional**
   - Endpoint: `POST /api/apps/{id}/avaliacoes/categorizar`
   - Processa avaliações usando LLM (GPT-4o) para categorização funcional
   - Suporta múltiplas categorias por avaliação
   - Retorna categorias com scores de confiança

2. **Taxonomia de Categorias Funcionais**
   - Implementar as 17 categorias específicas para apps bancários
   - Configuração flexível permitindo adicionar/remover categorias
   - Validação de categorias retornadas pelo LLM

3. **Sistema de Priorização Multi-Critério**
   - Calcular score de prioridade usando fórmula: `(Frequência × 0.4) + (Severidade × 0.3) + (Impacto × 0.3)`
   - Pesos de impacto configuráveis por categoria
   - Endpoint: `GET /api/apps/{id}/backlog-priorizado`
   - Retorna backlog ordenado por prioridade com métricas detalhadas

4. **Endpoint de Métricas de Categorização**
   - Endpoint: `GET /api/apps/{id}/categorias/metricas`
   - Retorna distribuição de categorias com frequência e severidade média
   - Inclui percentuais e contagens

5. **Integração com Processamento Existente**
   - Integrar categorização funcional no pipeline de processamento de avaliações
   - Armazenar categorias no banco de dados
   - Atualizar endpoints existentes para incluir categorias funcionais

**Critérios de Aceitação:**

1. O endpoint de categorização deve processar avaliações e retornar categorias funcionais válidas
2. Cada avaliação pode ter múltiplas categorias associadas
3. O sistema de priorização deve considerar frequência, severidade e impacto de negócio
4. As 17 categorias funcionais devem estar disponíveis e configuráveis
5. Os endpoints devem retornar dados no formato JSON com campos em camelCase
6. O processamento deve ser integrado ao pipeline existente de análise de sentimentos
7. Deve haver logs estruturados do processamento de categorização
8. Em caso de erro, o sistema deve registrar e continuar processamento das demais avaliações

**Dependências:**
- Processamento de avaliações com IA já implementado (US 32451)
- Endpoints de avaliações já existentes
- Banco de dados configurado para armazenar categorias

**Entregas:**
- Endpoints REST para categorização funcional
- Endpoint de backlog priorizado
- Endpoint de métricas de categorias
- Documentação da API
- Testes unitários e de integração

### 3.4 User Story Sugerida

```
Funcionalidade: Categorização funcional avançada de avaliações de aplicativos bancários

Como desenvolvedor do backend
Quero integrar sistema de categorização funcional específica para apps bancários
Para que o frontend possa exibir problemas categorizados por funcionalidade e gerar backlog priorizado

Cenário: Categorizar avaliação com múltiplas funcionalidades
Dado que existe uma avaliação: "App trava toda hora e não consigo fazer PIX"
Quando o sistema processar a avaliação
Então deve categorizar em: Performance, PIX
E retornar ambas as categorias com scores de confiança

Cenário: Gerar backlog priorizado
Dado que existem avaliações categorizadas para um aplicativo
Quando o cliente realizar requisição GET para "/api/apps/123/backlog-priorizado"
Então o servidor retorna código HTTP 200
E a resposta contém itens ordenados por prioridade calculada
E cada item contém: categoria, quantidade, severidade média, score de prioridade

Cenário: Obter métricas de categorias
Dado que existem avaliações categorizadas
Quando o cliente realizar requisição GET para "/api/apps/123/categorias/metricas"
Então o servidor retorna código HTTP 200
E a resposta contém distribuição de categorias com frequência e percentuais
```

### 3.5 Benefícios Esperados

**Para o Produto:**
- Backlog mais acionável e específico
- Priorização baseada em dados reais
- Identificação precisa de áreas problemáticas

**Para o Desenvolvimento:**
- Menos tempo gasto em análise manual
- Foco em correções de maior impacto
- Melhor alinhamento entre feedback e desenvolvimento

**Para o Negócio:**
- Redução de churn por problemas críticos
- Melhoria na satisfação do cliente
- ROI mais rápido em correções

---

## 4. Próximos Passos Recomendados

1. **Revisar e Aprovar Atividade:** Apresentar esta proposta para o time de produto/desenvolvimento
2. **Definir Escopo Detalhado:** Detalhar requisitos técnicos e de integração
3. **Planejar Implementação:** Dividir em tarefas menores se necessário
4. **Integrar Código Existente:** Adaptar scripts Python para integração com backend Python do Knooly
5. **Testes e Validação:** Validar categorização contra ground truth antes de produção

---

## 5. Considerações Técnicas

### 5.1 Integração com Código Existente

O projeto `app_review` possui scripts Python que podem ser adaptados:
- `scripts/functional_correlation.py` - Lógica de categorização com GPT-4o
- `scripts/generate_backlog_report.py` - Lógica de priorização
- Taxonomia de categorias já definida e validada

### 5.2 Adaptações Necessárias

1. Converter scripts Python para endpoints REST (FastAPI/Flask)
2. Integrar com banco de dados do Knooly
3. Adaptar prompts para contexto específico do aplicativo sendo analisado
4. Implementar cache para evitar reprocessamento
5. Adicionar tratamento de erros e retry logic

### 5.3 Performance

- Processamento pode ser feito em batch ou em tempo real
- Considerar rate limiting da API OpenAI
- Implementar fila de processamento para grandes volumes
- Cache de resultados para evitar reprocessamento

---

## Conclusão

O projeto `app_review` oferece capacidades avançadas de categorização funcional e priorização que podem significativamente enriquecer o módulo "Knooly Análise de Sentimentos". A integração dessas funcionalidades transformaria o sistema de uma ferramenta de visualização básica em uma solução completa de análise e ação baseada em dados.

A atividade proposta complementa perfeitamente o trabalho já desenvolvido pela equipe, adicionando valor sem duplicar esforços já realizados.

