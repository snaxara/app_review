# Backlog Priorizado

Data: 02/12/2025 11:09  
Total de Avaliações: 200  
Modelo: gpt-4o

---

## Resumo

Priorização de funcionalidades baseada em 200 avaliações negativas de usuários.

### Distribuição de Categorias

| Categoria | Quantidade | Porcentagem | Severidade Média | Prioridade |
|:----------|:-----------|:------------|:-----------------|:-----------|
| Performance | 88 | 44.0% | 1.86/5 | ALTA |
| Login/Autenticação | 28 | 14.0% | 1.79/5 | ALTA |
| Segurança | 4 | 2.0% | 1.00/5 | ALTA |
| Pagamentos/Boletos | 2 | 1.0% | 1.50/5 | MEDIA |
| PIX | 4 | 2.0% | 2.75/5 | MEDIA |
| Empréstimos/Crédito | 8 | 4.0% | 1.50/5 | MEDIA |
| Atendimento | 9 | 4.5% | 1.00/5 | MEDIA |
| Cadastro/Conta | 5 | 2.5% | 1.00/5 | MEDIA |
| Outros | 39 | 19.5% | 1.51/5 | MEDIA |
| Interface/Usabilidade | 4 | 2.0% | 2.50/5 | MEDIA |
| Saldo/Extrato | 3 | 1.5% | 2.67/5 | MEDIA |
| Notificações | 4 | 2.0% | 2.50/5 | BAIXA |
| Investimentos | 2 | 1.0% | 3.50/5 | BAIXA |

---

## Detalhamento por Categoria

### 88. Performance (Prioridade: ALTA)

**Métricas:**
- Frequência: 88 avaliações (44.0% do total)
- Severidade Média: 1.86/5
- Score de Prioridade: 0.63

**Amostras de Avaliações:**

- "Não estou gostando desse aplicativo do banco tá travando demora pra abrir tava bom agora tá muito ruim vou cancelar minha conta só passou raiva não ab..." (Score: 1/5)
- "Por muitas vezes trava. Como nesse momento. Tenho que fazer pagamento e.nào.consigo." (Score: 4/5)
- "Não fecha. Que saco" (Score: 2/5)

**Recomendações:**
- Executar profiling do app. Otimizar tempo de inicialização e identificar memory leaks.

---

### 28. Login/Autenticação (Prioridade: ALTA)

**Métricas:**
- Frequência: 28 avaliações (14.0% do total)
- Severidade Média: 1.79/5
- Score de Prioridade: 0.55

**Amostras de Avaliações:**

- "O aplicativo não está funcionando só fica dizendo que a senha expirou e o aplicativo nem abre." (Score: 1/5)
- "Não consigo entrar na minha conta" (Score: 1/5)
- "Não estou conseguindo acessar a minha conta está horrível" (Score: 3/5)

**Recomendações:**
- Analisar taxa de falha no login. Revisar fluxo de recuperação de senha e biometria.

---

### 4. Segurança (Prioridade: ALTA)

**Métricas:**
- Frequência: 4 avaliações (2.0% do total)
- Severidade Média: 1.00/5
- Score de Prioridade: 0.55

**Amostras de Avaliações:**

- "um lixo... bloqueio de poupança sem autorização e etc.." (Score: 1/5)
- "Pessimo app sempre trava e pede confirmação de senha de cartão deixando assim com duvidas se é o banco ou golpe !" (Score: 1/5)
- "O pior está roubando meu dinheiro cobrando oq eu não devo esse AP e um roubo" (Score: 1/5)

**Recomendações:**
- Revisar políticas de bloqueio. Implementar notificações proativas de segurança.

---

### 2. Pagamentos/Boletos (Prioridade: MÉDIA)

**Métricas:**
- Frequência: 2 avaliações (1.0% do total)
- Severidade Média: 1.50/5
- Score de Prioridade: 0.45

**Amostras de Avaliações:**

- "Péssimo! Os boletos DDA não são excluídos após o pagamento mensal. Por conta disso fiz um pagamento em duplicidade." (Score: 2/5)
- "Agora mesmo estou precisando efetuar o pagamento e não estou conseguindo isso vêm acontecendo toda noite" (Score: 1/5)

**Recomendações:**
- Revisar lógica de exclusão de boletos pagos no DDA. Implementar confirmação antes de pagamentos.

---

### 4. PIX (Prioridade: MÉDIA)

**Métricas:**
- Frequência: 4 avaliações (2.0% do total)
- Severidade Média: 2.75/5
- Score de Prioridade: 0.44

**Amostras de Avaliações:**

- "Um lixo...A gente precisa fazer um pix urgente o banco funciona...." (Score: 1/5)
- "Tá um lixo o app de vcs não consigo fazer pix de mizeros 5 reais" (Score: 5/5)
- "As vezes que mais preciso fazer um pix está fora do ar" (Score: 3/5)

**Recomendações:**
- Investigar logs de erro nas transações PIX. Revisar integração com BACEN e timeout de confirmação.

---

## Próximos Passos

1. Revisão técnica dos problemas prioritários
2. Planejamento de sprint com itens críticos
3. Monitoramento das métricas após correções
4. Comunicação com usuários sobre correções

---
