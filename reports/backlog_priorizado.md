# Backlog Priorizado

Data: 04/12/2025 15:52  
Total de Avaliações: 828  
Modelo: gpt-4o

---

## Resumo

Priorização de funcionalidades baseada em 828 avaliações negativas de usuários.

### Distribuição de Categorias

| Categoria | Quantidade | Porcentagem | Severidade Média | Prioridade |
|:----------|:-----------|:------------|:-----------------|:-----------|
| Performance | 489 | 59.1% | 1.46/5 | CRITICA |
| Login/Autenticação | 224 | 27.1% | 1.42/5 | ALTA |
| Segurança | 22 | 2.7% | 1.32/5 | ALTA |
| PIX | 68 | 8.2% | 1.75/5 | ALTA |
| Pagamentos/Boletos | 57 | 6.9% | 1.53/5 | MEDIA |
| Questões geográficas | 12 | 1.4% | 1.00/5 | MEDIA |
| Interface/Usabilidade | 151 | 18.2% | 1.72/5 | MEDIA |
| Empréstimos/Crédito | 56 | 6.8% | 1.48/5 | MEDIA |
| Placas/Veículos | 1 | 0.1% | 1.00/5 | MEDIA |
| Atendimento | 85 | 10.3% | 1.22/5 | MEDIA |
| Saldo/Extrato | 39 | 4.7% | 1.38/5 | MEDIA |
| Cadastro/Conta | 25 | 3.0% | 1.32/5 | MEDIA |
| Investimentos | 17 | 2.1% | 1.65/5 | MEDIA |
| Outros | 79 | 9.5% | 1.38/5 | MEDIA |
| Notificações | 19 | 2.3% | 2.11/5 | BAIXA |

---

## Detalhamento por Categoria

### 489. Performance (Prioridade: CRÍTICA)

**Métricas:**
- Frequência: 489 avaliações (59.1% do total)
- Severidade Média: 1.46/5
- Score de Prioridade: 0.72

**Amostras de Avaliações:**

- "Não estou gostando desse aplicativo do banco tá travando demora pra abrir tava bom agora tá muito ruim vou cancelar minha conta só passou raiva não ab..." (Score: 1/5)
- "Por muitas vezes trava. Como nesse momento. Tenho que fazer pagamento e.nào.consigo." (Score: 4/5)
- "O aplicativo não está funcionando só fica dizendo que a senha expirou e o aplicativo nem abre." (Score: 1/5)

**Recomendações:**
- Executar profiling do app. Otimizar tempo de inicialização e identificar memory leaks.

---

### 224. Login/Autenticação (Prioridade: ALTA)

**Métricas:**
- Frequência: 224 avaliações (27.1% do total)
- Severidade Média: 1.42/5
- Score de Prioridade: 0.62

**Amostras de Avaliações:**

- "O aplicativo não está funcionando só fica dizendo que a senha expirou e o aplicativo nem abre." (Score: 1/5)
- "Não consigo entrar na minha conta" (Score: 1/5)
- "Não estou conseguindo acessar a minha conta está horrível" (Score: 3/5)

**Recomendações:**
- Analisar taxa de falha no login. Revisar fluxo de recuperação de senha e biometria.

---

### 22. Segurança (Prioridade: ALTA)

**Métricas:**
- Frequência: 22 avaliações (2.7% do total)
- Severidade Média: 1.32/5
- Score de Prioridade: 0.53

**Amostras de Avaliações:**

- "Este aplicativo está impedindo de eu abrir uma conta no Santander primeira que é sobrepor aos outros aplicativos depois quer vasculhar o celular da ge..." (Score: 1/5)
- "um lixo... bloqueio de poupança sem autorização e etc.." (Score: 1/5)
- "Pessimo app sempre trava e pede confirmação de senha de cartão deixando assim com duvidas se é o banco ou golpe !" (Score: 1/5)

**Recomendações:**
- Revisar políticas de bloqueio. Implementar notificações proativas de segurança.

---

### 68. PIX (Prioridade: ALTA)

**Métricas:**
- Frequência: 68 avaliações (8.2% do total)
- Severidade Média: 1.75/5
- Score de Prioridade: 0.53

**Amostras de Avaliações:**

- "Bota a opção de persona as cores o tema do app. Ou deixa todo vermelho. Está feito. Como vou compartilhar meu Pix não tem a opção. Deixa o app melhor ..." (Score: 2/5)
- "App simplesmente parou de funcionar não consigo receber e nem mandar pix não consigo sacar dinheiro na poupança e nem nda por favor arrume isso logo m..." (Score: 5/5)
- "Não recebo nenhuma notificação de pix" (Score: 1/5)

**Recomendações:**
- Investigar logs de erro nas transações PIX. Revisar integração com BACEN e timeout de confirmação.

---

### 57. Pagamentos/Boletos (Prioridade: MÉDIA)

**Métricas:**
- Frequência: 57 avaliações (6.9% do total)
- Severidade Média: 1.53/5
- Score de Prioridade: 0.48

**Amostras de Avaliações:**

- "Por muitas vezes trava. Como nesse momento. Tenho que fazer pagamento e.nào.consigo." (Score: 4/5)
- "Péssimo! Os boletos DDA não são excluídos após o pagamento mensal. Por conta disso fiz um pagamento em duplicidade." (Score: 2/5)
- "Muita dificuldade para conseguir falar com atendente presencial Não tem suporte Péssimo atendimento online A gente liga nunca consegue resultado Não c..." (Score: 1/5)

**Recomendações:**
- Revisar lógica de exclusão de boletos pagos no DDA. Implementar confirmação antes de pagamentos.

---

## Próximos Passos

1. Revisão técnica dos problemas prioritários
2. Planejamento de sprint com itens críticos
3. Monitoramento das métricas após correções
4. Comunicação com usuários sobre correções

---
