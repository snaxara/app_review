# Estratégia de Prompt Engineering para Correlação Funcional

## 1. Objetivo

Desenvolver um sistema de prompts para categorizar avaliações de aplicativos bancários em **categorias funcionais específicas**, permitindo a priorização de backlog baseada em feedback real dos usuários.

---

## 2. Taxonomia de Categorias Funcionais

### 2.1 Categorias Principais

Baseado na análise de aplicativos bancários (Santander, Bradesco, etc.), definimos as seguintes categorias:

| Categoria | Descrição | Exemplos de Palavras-Chave |
|:----------|:----------|:---------------------------|
| **PIX** | Problemas relacionados a transferências PIX | pix, transferência instantânea, chave pix, qr code |
| **Login/Autenticação** | Dificuldades de acesso, senha, biometria | login, senha, entrar, acesso, biometria, reconhecimento facial, digital |
| **Performance** | Lentidão, travamentos, crashes | lento, trava, demora, carregando, não abre, fecha sozinho, congela |
| **Interface/Usabilidade** | Problemas de navegação, design confuso | confuso, difícil de usar, não encontro, complicado, interface, menu |
| **Empréstimos/Crédito** | Questões sobre empréstimos, cartão de crédito, limites | empréstimo, crédito, limite, cartão, financiamento, parcela |
| **Pagamentos/Boletos** | Problemas com pagamentos de contas e boletos | boleto, pagamento, conta, DDA, duplicidade, não paga |
| **Saldo/Extrato** | Visualização de saldo, extrato, transações | saldo, extrato, transação, histórico, movimentação |
| **Atendimento** | Suporte ao cliente, chat, SAC | atendimento, suporte, ajuda, contato, SAC, chat |
| **Cadastro/Conta** | Abertura de conta, atualização cadastral | cadastro, abrir conta, dados, atualizar, documento |
| **Investimentos** | Aplicações financeiras, poupança | investimento, poupança, aplicação, rendimento, CDB |
| **Segurança** | Fraudes, bloqueios, segurança | fraude, bloqueio, segurança, roubo, clonagem |
| **Notificações** | Alertas, push notifications | notificação, alerta, aviso, push |
| **Outros** | Problemas não categorizados acima | - |

### 2.2 Categorias Secundárias (Opcional para Análise Avançada)

- **Bug Técnico** - Erros específicos de software
- **Funcionalidade Ausente** - Recursos que o usuário esperava encontrar
- **Atualização** - Problemas após atualização do app

---

## 3. Estratégia de Prompt Engineering

### 3.1 Abordagem: Few-Shot Learning

Utilizaremos **few-shot prompting** com exemplos representativos para guiar o LLM na categorização.

### 3.2 Estrutura do Prompt

```
SISTEMA: Você é um especialista em análise de feedbacks de aplicativos bancários.

TAREFA: Categorize a avaliação do usuário em UMA categoria funcional principal.

CATEGORIAS DISPONÍVEIS:
- PIX
- Login/Autenticação
- Performance
- Interface/Usabilidade
- Empréstimos/Crédito
- Pagamentos/Boletos
- Saldo/Extrato
- Atendimento
- Cadastro/Conta
- Investimentos
- Segurança
- Notificações
- Outros

EXEMPLOS:

Avaliação: "Não consigo fazer PIX, sempre dá erro quando tento transferir"
Categoria: PIX

Avaliação: "O app trava toda hora, muito lento para abrir"
Categoria: Performance

Avaliação: "Não consigo entrar no app, sempre pede para redefinir senha"
Categoria: Login/Autenticação

Avaliação: "Os boletos DDA não são excluídos após o pagamento, fiz pagamento em duplicidade"
Categoria: Pagamentos/Boletos

AVALIAÇÃO PARA CATEGORIZAR:
"{texto_avaliacao}"

RESPONDA APENAS COM O NOME DA CATEGORIA (sem explicações adicionais).
```

### 3.3 Prompt Otimizado para JSON Output

Para facilitar o processamento automatizado, utilizaremos um prompt que retorna JSON estruturado:

```json
{
  "categoria_principal": "Performance",
  "confianca": "alta",
  "subcategorias": ["Travamento", "Lentidão"],
  "palavras_chave_identificadas": ["trava", "lento", "demora"]
}
```

---

## 4. Estratégia de Processamento

### 4.1 Filtro de Avaliações

**Critério:** Processar apenas avaliações com sentimento **negative** ou **neutral** com score baixo de confiança.

**Justificativa:** Avaliações positivas geralmente não contêm informações acionáveis para o backlog de correções.

### 4.2 Processamento em Lote

- **Batch Size:** 50 avaliações por chamada à API (para otimizar custos e tempo)
- **Rate Limiting:** Respeitar limites da API (ex: 3 requisições por minuto)
- **Retry Logic:** Implementar retry automático em caso de falhas

### 4.3 Validação de Qualidade

- **Amostragem Manual:** Validar manualmente 10% das categorizações
- **Métricas de Confiança:** Registrar o nível de confiança do LLM em cada categorização
- **Categorias Ambíguas:** Marcar avaliações que mencionam múltiplas funcionalidades

---

## 5. Geração de Backlog Priorizado

### 5.1 Critérios de Priorização

| Critério | Peso | Descrição |
|:---------|:-----|:----------|
| **Frequência** | 40% | Número de avaliações negativas na categoria |
| **Severidade** | 30% | Score médio das avaliações (1-2 = alta severidade) |
| **Impacto** | 20% | Categorias críticas (PIX, Login) têm peso maior |
| **Tendência** | 10% | Aumento de reclamações nas últimas semanas |

### 5.2 Formato do Backlog

```markdown
# Backlog Priorizado - Aplicativo Bancário

## 1. Performance (Prioridade: CRÍTICA)
- **Frequência:** 45 avaliações negativas (13.6%)
- **Severidade Média:** 1.8/5
- **Principais Problemas:**
  - App trava ao abrir (23 menções)
  - Lentidão no carregamento (15 menções)
  - Fechamento inesperado (7 menções)
- **Ação Recomendada:** Investigar logs de crash e otimizar performance de inicialização

## 2. PIX (Prioridade: ALTA)
- **Frequência:** 38 avaliações negativas (11.5%)
- **Severidade Média:** 2.1/5
- **Principais Problemas:**
  - Erro ao enviar PIX (20 menções)
  - Demora na confirmação (12 menções)
  - Problemas com QR Code (6 menções)
- **Ação Recomendada:** Revisar integração com BACEN e timeout de transações
```

---

## 6. Integração com Azure DevOps / Jira

### 6.1 Mapeamento de Categorias para Componentes

| Categoria Funcional | Componente no Azure DevOps | Squad Responsável |
|:--------------------|:---------------------------|:------------------|
| PIX | `payments-pix` | Squad Pagamentos |
| Login/Autenticação | `auth-service` | Squad Segurança |
| Performance | `mobile-app-core` | Squad Mobile |
| Interface/Usabilidade | `mobile-app-ui` | Squad UX/UI |

### 6.2 Criação Automática de Issues

**Template de Issue:**
```
Título: [Feedback Usuário] {Categoria} - {Resumo do Problema}

Descrição:
- **Origem:** Análise de avaliações do Google Play Store
- **Categoria:** {Categoria}
- **Frequência:** {N} avaliações similares
- **Severidade:** {Score médio}
- **Exemplos de Avaliações:**
  1. "{Texto da avaliação 1}"
  2. "{Texto da avaliação 2}"

Labels: user-feedback, {categoria}, priority-{nivel}
```

---

## 7. Considerações Técnicas

### 7.1 Modelos LLM Recomendados

1. **GPT-4-mini** (OpenAI) - Melhor custo-benefício para categorização
2. **Gemini 2.5 Flash** (Google) - Alternativa gratuita com boa performance
3. **GPT-4.1-nano** - Para processamento em larga escala

### 7.2 Estimativa de Custos

Para 30.000 avaliações (dataset completo):
- **Tokens de entrada:** ~50 tokens/avaliação × 30.000 = 1.5M tokens
- **Tokens de saída:** ~10 tokens/resposta × 30.000 = 300K tokens
- **Custo estimado (GPT-4-mini):** ~$0.50 - $1.00 USD

### 7.3 Otimizações

- **Cache de Resultados:** Armazenar categorizações para evitar reprocessamento
- **Batch Processing:** Agrupar avaliações similares
- **Filtro Inteligente:** Processar apenas avaliações com mais de 10 palavras

---

## 8. Próximos Passos de Implementação

1. ✅ Definir taxonomia de categorias (concluído)
2. ✅ Desenvolver estratégia de prompts (concluído)
3. ⏳ Implementar script Python com integração LLM
4. ⏳ Testar com amostra de 100 avaliações
5. ⏳ Validar manualmente a qualidade das categorizações
6. ⏳ Processar dataset completo
7. ⏳ Gerar backlog priorizado
8. ⏳ Documentar resultados no TCC

---

**Preparado por:** Manus AI  
**Data:** 01 de Dezembro de 2025  
**Projeto:** TCC - Correlação Funcional de Sentimentos em Apps Bancários
