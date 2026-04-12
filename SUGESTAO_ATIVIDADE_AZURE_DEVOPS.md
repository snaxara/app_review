# Sugestão de Nova Atividade - Azure DevOps

## Título da Atividade

**[Knooly - Análise de Sentimentos - Categorização Funcional Avançada] - Integrar sistema de categorização funcional específica para apps bancários com priorização multi-critério**

---

## Informações Básicas

- **Tipo:** US BACK END
- **Epic:** Detalhes da Análise de Comentários
- **Prioridade:** Alta
- **Sprint:** A definir (recomendado: Sprint 3 ou 4)
- **Estimativa:** 8-13 pontos (dependendo da complexidade de integração)

---

## Descrição

O módulo atual de Análise de Sentimentos classifica avaliações em categorias genéricas (ex: "Não funciona", "Muito lento", "Não carrega"), o que dificulta a ação direta da equipe de desenvolvimento. Esta atividade integra um sistema de categorização funcional específica para aplicativos bancários, permitindo identificar precisamente qual funcionalidade precisa de correção e gerar backlog priorizado baseado em múltiplos critérios (frequência, severidade e impacto de negócio).

**Contexto:**
Atualmente, o sistema processa avaliações e identifica sentimentos (Positivo/Negativo/Neutro/Misto) e categorias genéricas. No entanto, categorias genéricas não permitem ação direta - saber que algo "não funciona" não indica qual funcionalidade específica precisa ser corrigida.

**Solução:**
Integrar sistema de categorização funcional avançada com 17 categorias específicas para apps bancários (PIX, Login/Autenticação, Performance, etc.) e sistema de priorização que considera não apenas frequência, mas também severidade das avaliações e impacto de negócio de cada categoria.

---

## Critérios de Aceitação

### 1. Endpoint de Categorização Funcional

**Requisição bem-sucedida (HTTP 200)**
- Endpoint: `POST /api/apps/{id}/avaliacoes/categorizar`
- Quando uma requisição POST for realizada com um ID de aplicativo válido e lista de avaliações:
  - O servidor deve retornar código HTTP 200
  - Cada avaliação deve ser processada usando LLM (GPT-4o) para identificar categorias funcionais
  - A resposta deve conter para cada avaliação: lista de categorias identificadas e scores de confiança
  - Uma avaliação pode ter múltiplas categorias (ex: "App trava e não consigo fazer PIX" → Performance + PIX)

**Formato da resposta:**
```json
{
  "avaliacoes": [
    {
      "id": "123",
      "categorias": [
        {"nome": "Performance", "confianca": 0.95},
        {"nome": "PIX", "confianca": 0.88}
      ]
    }
  ]
}
```

### 2. Taxonomia de Categorias Funcionais

- O sistema deve suportar as seguintes 17 categorias funcionais:
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

- As categorias devem ser configuráveis (permitir adicionar/remover via configuração)
- O sistema deve validar que categorias retornadas pelo LLM estão na lista válida

### 3. Endpoint de Backlog Priorizado

**Requisição bem-sucedida (HTTP 200)**
- Endpoint: `GET /api/apps/{id}/backlog-priorizado?dataInicio=YYYY-MM-DD&dataFim=YYYY-MM-DD`
- Quando uma requisição GET for realizada com ID de aplicativo válido e intervalo de datas:
  - O servidor deve retornar código HTTP 200
  - A resposta deve conter itens do backlog ordenados por score de prioridade (maior primeiro)
  - Cada item deve conter: categoria, quantidade de avaliações, severidade média, score de prioridade, percentual

**Cálculo de Prioridade:**
- Fórmula: `(Frequência × 0.4) + (Severidade × 0.3) + (Impacto × 0.3)`
- Frequência: quantidade de avaliações com a categoria / total de avaliações (normalizado 0-1)
- Severidade: (5 - score médio) / 5 (quanto menor o score, maior a severidade)
- Impacto: peso pré-definido por categoria (ex: PIX=1.0, Segurança=1.0, Notificações=0.3)

**Formato da resposta:**
```json
[
  {
    "categoria": "Performance",
    "quantidade": 489,
    "percentual": "59.1%",
    "severidadeMedia": 1.46,
    "scorePrioridade": 0.72,
    "nivelPrioridade": "CRITICA"
  },
  {
    "categoria": "Login/Autenticação",
    "quantidade": 224,
    "percentual": "27.1%",
    "severidadeMedia": 1.42,
    "scorePrioridade": 0.65,
    "nivelPrioridade": "ALTA"
  }
]
```

### 4. Endpoint de Métricas de Categorias

**Requisição bem-sucedida (HTTP 200)**
- Endpoint: `GET /api/apps/{id}/categorias/metricas?dataInicio=YYYY-MM-DD&dataFim=YYYY-MM-DD`
- Quando uma requisição GET for realizada com ID de aplicativo válido:
  - O servidor deve retornar código HTTP 200
  - A resposta deve conter distribuição de todas as categorias com: quantidade, percentual, severidade média

**Formato da resposta:**
```json
{
  "totalAvaliacoes": 828,
  "categorias": [
    {
      "nome": "Performance",
      "quantidade": 489,
      "percentual": 59.1,
      "severidadeMedia": 1.46
    }
  ]
}
```

### 5. Integração com Processamento Existente

- A categorização funcional deve ser integrada ao pipeline de processamento de avaliações
- Categorias devem ser armazenadas no banco de dados junto com os dados de avaliação
- Endpoints existentes de resumo e gráficos devem poder filtrar/agrupar por categoria funcional

### 6. Tratamento de Erros

- Em caso de erro na comunicação com LLM, o sistema deve registrar o erro em log e continuar processamento das demais avaliações
- Avaliações que não puderam ser categorizadas devem ser marcadas com categoria "Outros"
- Erros devem ser retornados com código HTTP apropriado (400 para parâmetros inválidos, 500 para erros internos)

### 7. Performance e Escalabilidade

- Processamento pode ser feito em batch para grandes volumes
- Deve haver cache para evitar reprocessamento de avaliações já categorizadas
- Rate limiting deve ser respeitado para API OpenAI
- Logs estruturados devem ser gerados para monitoramento

---

## User Story (Formato BDD)

```
Funcionalidade: Categorização funcional avançada de avaliações de aplicativos bancários

Como desenvolvedor do backend do módulo de Análise de Sentimentos
Quero integrar sistema de categorização funcional específica para apps bancários
Para que o frontend possa exibir problemas categorizados por funcionalidade e gerar backlog priorizado baseado em múltiplos critérios

Contexto:
Dado que existem avaliações coletadas da Play Store para um aplicativo
E que o sistema já processa sentimentos (Positivo/Negativo/Neutro/Misto)

Cenário: Categorizar avaliação com múltiplas funcionalidades
Dado que existe uma avaliação: "App trava toda hora e não consigo fazer PIX"
Quando o sistema processar a avaliação através do endpoint POST /api/apps/123/avaliacoes/categorizar
Então o servidor retorna código HTTP 200
E a resposta contém a avaliação categorizada em: Performance, PIX
E ambas as categorias têm scores de confiança acima de 0.8

Cenário: Gerar backlog priorizado
Dado que existem avaliações categorizadas para o aplicativo com ID "123"
E o usuário seleciona intervalo de datas de "2025-08-01" até "2025-08-20"
Quando o cliente realizar requisição GET para "/api/apps/123/backlog-priorizado?dataInicio=2025-08-01&dataFim=2025-08-20"
Então o servidor retorna código HTTP 200
E a resposta contém itens ordenados por score de prioridade (maior primeiro)
E cada item contém: categoria, quantidade, severidade média, score de prioridade, nível de prioridade
E o item com maior score de prioridade é "Performance" com nível "CRITICA"

Cenário: Obter métricas de categorias
Dado que existem avaliações categorizadas para o aplicativo com ID "123"
Quando o cliente realizar requisição GET para "/api/apps/123/categorias/metricas?dataInicio=2025-08-01&dataFim=2025-08-20"
Então o servidor retorna código HTTP 200
E a resposta contém distribuição de todas as categorias
E cada categoria contém: nome, quantidade, percentual, severidade média
E a soma dos percentuais é aproximadamente 100%

Cenário: Aplicativo inválido ou não encontrado
Dado que não existe um aplicativo com ID "999"
Quando o cliente realizar requisição GET para "/api/apps/999/backlog-priorizado"
Então o servidor retorna código HTTP 404
E a resposta contém mensagem informando que o aplicativo não foi encontrado

Cenário: Intervalo de datas inválido
Dado que o cliente não fornece data de início ou data de fim
Quando o cliente realizar requisição GET para "/api/apps/123/backlog-priorizado"
Então o servidor retorna código HTTP 400
E a resposta contém mensagem informando que o intervalo de datas é obrigatório
```

---

## Dependências

- Processamento de avaliações com IA já implementado (US 32451)
- Endpoints de avaliações já existentes (listagem, resumo geral)
- Banco de dados configurado para armazenar categorias funcionais
- Integração com API OpenAI (GPT-4o) configurada

---

## Entregas

1. **Endpoints REST:**
   - `POST /api/apps/{id}/avaliacoes/categorizar` - Categorização funcional
   - `GET /api/apps/{id}/backlog-priorizado` - Backlog priorizado
   - `GET /api/apps/{id}/categorias/metricas` - Métricas de categorias

2. **Modelo de Dados:**
   - Tabela/coleção para armazenar categorias funcionais por avaliação
   - Índices para consultas eficientes

3. **Lógica de Negócio:**
   - Sistema de categorização usando GPT-4o
   - Sistema de priorização multi-critério
   - Validação de categorias

4. **Documentação:**
   - Documentação da API (Swagger/OpenAPI)
   - Guia de configuração de categorias
   - Exemplos de uso

5. **Testes:**
   - Testes unitários para lógica de priorização
   - Testes de integração para endpoints
   - Testes de validação de categorias

---

## Benefícios Esperados

**Para o Produto:**
- Backlog mais acionável e específico por funcionalidade
- Priorização inteligente baseada em dados reais
- Identificação precisa de áreas problemáticas do aplicativo

**Para o Desenvolvimento:**
- Redução de 60-70% no tempo de análise manual de avaliações
- Foco em correções de maior impacto no negócio
- Melhor alinhamento entre feedback do usuário e backlog de desenvolvimento

**Para o Negócio:**
- Redução de churn por problemas críticos não resolvidos
- Melhoria na satisfação do cliente (NPS)
- ROI mais rápido em correções priorizadas corretamente

---

## Notas Técnicas

### Integração com Código Existente

O projeto `app_review` possui scripts Python que podem ser adaptados:
- Lógica de categorização com GPT-4o já implementada e validada
- Taxonomia de 17 categorias já definida e testada
- Sistema de priorização multi-critério já funcional

### Adaptações Necessárias

1. Converter scripts Python para endpoints REST (FastAPI/Flask)
2. Integrar com banco de dados do Knooly (PostgreSQL/MongoDB)
3. Adaptar prompts para contexto específico do aplicativo sendo analisado
4. Implementar cache para evitar reprocessamento
5. Adicionar tratamento de erros robusto e retry logic

### Performance

- Processamento pode ser feito em batch ou em tempo real
- Considerar rate limiting da API OpenAI (implementar fila se necessário)
- Cache de resultados para evitar reprocessamento
- Processamento assíncrono para grandes volumes

---

## Referências

- Projeto `app_review`: `c:\codigos\app_review`
- Scripts de referência:
  - `scripts/functional_correlation.py` - Categorização funcional
  - `scripts/generate_backlog_report.py` - Geração de backlog priorizado
- Documentação: `ANALISE_COMPLEMENTARIDADE.md`

