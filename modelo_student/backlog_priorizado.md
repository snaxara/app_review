# Backlog Priorizado

Data: 01/12/2025 17:33  
Total de Avaliações: 200  
Modelo: gpt-4o

---

## Resumo

Priorização de funcionalidades baseada em 200 avaliações negativas de usuários.

### Distribuição de Categorias

| Categoria | Quantidade | Porcentagem | Severidade Média | Prioridade |
|:----------|:-----------|:------------|:-----------------|:-----------|
| Segurança | 2 | 1.0% | 1.00/5 | ALTA |
| Performance | 44 | 22.0% | 2.14/5 | ALTA |
| Login/Autenticação | 18 | 9.0% | 1.83/5 | ALTA |
| Pagamentos/Boletos | 1 | 0.5% | 2.00/5 | MEDIA |
| Cadastro/Conta | 6 | 3.0% | 1.67/5 | MEDIA |
| Saldo/Extrato | 3 | 1.5% | 2.67/5 | MEDIA |
| Empréstimos/Crédito | 13 | 6.5% | 3.77/5 | MEDIA |
| PIX | 2 | 1.0% | 5.00/5 | MEDIA |
| Outros | 100 | 50.0% | 4.33/5 | MEDIA |
| Atendimento | 8 | 4.0% | 3.00/5 | BAIXA |
| Interface/Usabilidade | 1 | 0.5% | 5.00/5 | BAIXA |
| Notificações | 2 | 1.0% | 4.00/5 | BAIXA |

---

## Detalhamento por Categoria

### 2. Segurança (Prioridade: ALTA)

**Métricas:**
- Frequência: 2 avaliações (1.0% do total)
- Severidade Média: 1.00/5
- Score de Prioridade: 0.54

**Amostras de Avaliações:**

- "um lixo... bloqueio de poupança sem autorização e etc.." (Score: 1/5)
- "Pessimo app sempre trava e pede confirmação de senha de cartão deixando assim com duvidas se é o banco ou golpe !" (Score: 1/5)

**Recomendações:**
- Revisar políticas de bloqueio. Implementar notificações proativas de segurança.

---

### 44. Performance (Prioridade: ALTA)

**Métricas:**
- Frequência: 44 avaliações (22.0% do total)
- Severidade Média: 2.14/5
- Score de Prioridade: 0.53

**Amostras de Avaliações:**

- "Não estou gostando desse aplicativo do banco tá travando demora pra abrir tava bom agora tá muito ruim vou cancelar minha conta só passou raiva não ab..." (Score: 1/5)
- "Todas as vezes q preciso entrar no meu banco tenho q reiniciar o aparelho. Não sei o porque disso pois antes não era assim. Será do próprio aparelho o..." (Score: 2/5)
- "por q o APP tá horrível de abri" (Score: 1/5)

**Recomendações:**
- Executar profiling do app. Otimizar tempo de inicialização e identificar memory leaks.

---

### 18. Login/Autenticação (Prioridade: ALTA)

**Métricas:**
- Frequência: 18 avaliações (9.0% do total)
- Severidade Média: 1.83/5
- Score de Prioridade: 0.53

**Amostras de Avaliações:**

- "O aplicativo não está funcionando só fica dizendo que a senha expirou e o aplicativo nem abre." (Score: 1/5)
- "gosto muito desse banco mas não tava conseguindo fazer a senha mas consegui" (Score: 5/5)
- "Não estou conseguindo acessar a minha conta está horrível" (Score: 3/5)

**Recomendações:**
- Analisar taxa de falha no login. Revisar fluxo de recuperação de senha e biometria.

---

### 1. Pagamentos/Boletos (Prioridade: MÉDIA)

**Métricas:**
- Frequência: 1 avaliações (0.5% do total)
- Severidade Média: 2.00/5
- Score de Prioridade: 0.42

**Amostras de Avaliações:**

- "Péssimo! Os boletos DDA não são excluídos após o pagamento mensal. Por conta disso fiz um pagamento em duplicidade." (Score: 2/5)

**Recomendações:**
- Revisar lógica de exclusão de boletos pagos no DDA. Implementar confirmação antes de pagamentos.

---

### 6. Cadastro/Conta (Prioridade: MÉDIA)

**Métricas:**
- Frequência: 6 avaliações (3.0% do total)
- Severidade Média: 1.67/5
- Score de Prioridade: 0.36

**Amostras de Avaliações:**

- "Faz tempo q espero ser cliente de vcs é vcs não me aprovam" (Score: 1/5)
- "Acabei de baixar o aplicativo e não consigo abrir uma conta salário" (Score: 1/5)
- "Eu estou de saco cheio com esse Banco uma hora estou aprovado outra hora não nada tempo de tentativa encerrado ou hora meu cpf não combina com o CPF d..." (Score: 5/5)

**Recomendações:**
- Análise detalhada necessária.

---

## Próximos Passos

1. Revisão técnica dos problemas prioritários
2. Planejamento de sprint com itens críticos
3. Monitoramento das métricas após correções
4. Comunicação com usuários sobre correções

---
