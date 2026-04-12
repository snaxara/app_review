# Backlog Priorizado - Aplicativo Bancário

**Data de Geração:** 02/12/2025 23:23  
**Total de Avaliações Analisadas:** 266  
**Modelo LLM Utilizado:** gpt-4o

---

## Resumo Executivo

Este relatório apresenta a priorização de funcionalidades do aplicativo bancário baseada em **266 avaliações negativas** de usuários reais.

### Distribuição de Categorias

| Categoria | Quantidade | Porcentagem | Severidade Média | Prioridade |
|:----------|:-----------|:------------|:-----------------|:-----------|
| Performance | 112 | 42.1% | 2.01/5 | 🟠 ALTA |
| Login/Autenticação | 41 | 15.4% | 1.80/5 | 🟠 ALTA |
| Segurança | 5 | 1.9% | 1.20/5 | 🟠 ALTA |
| PIX | 10 | 3.8% | 1.70/5 | 🟠 ALTA |
| Pagamentos/Boletos | 3 | 1.1% | 1.33/5 | 🟡 MÉDIA |
| Empréstimos/Crédito | 12 | 4.5% | 1.67/5 | 🟡 MÉDIA |
| Atendimento | 10 | 3.8% | 1.00/5 | 🟡 MÉDIA |
| Cadastro/Conta | 7 | 2.6% | 1.57/5 | 🟡 MÉDIA |
| Interface/Usabilidade | 10 | 3.8% | 2.50/5 | 🟡 MÉDIA |
| Outros | 44 | 16.5% | 1.45/5 | 🟡 MÉDIA |
| Saldo/Extrato | 3 | 1.1% | 2.67/5 | 🟡 MÉDIA |
| Investimentos | 3 | 1.1% | 2.67/5 | 🟢 BAIXA |
| Notificações | 6 | 2.3% | 2.33/5 | 🟢 BAIXA |

---

## Detalhamento por Categoria

### 112. Performance (Prioridade: ALTA)

**Métricas:**
- 📊 Frequência: 112 avaliações (42.1% do total)
- ⭐ Severidade Média: 2.01/5
- 🎯 Score de Prioridade: 0.62

**Amostras de Avaliações:**

- "Não estou gostando desse aplicativo do banco tá travando demora pra abrir tava bom agora tá muito ruim vou cancelar minha conta só passou raiva não abre" (Score: 1/5)
- "Por muitas vezes trava. Como nesse momento. Tenho que fazer pagamento e.nào.consigo." (Score: 4/5)
- "Não fecha. Que saco" (Score: 2/5)

**Ação Recomendada:**
- Executar profiling do app. Otimizar tempo de inicialização e identificar memory leaks.

---

### 41. Login/Autenticação (Prioridade: ALTA)

**Métricas:**
- 📊 Frequência: 41 avaliações (15.4% do total)
- ⭐ Severidade Média: 1.80/5
- 🎯 Score de Prioridade: 0.55

**Amostras de Avaliações:**

- "O aplicativo não está funcionando só fica dizendo que a senha expirou e o aplicativo nem abre." (Score: 1/5)
- "Não consigo entrar na minha conta" (Score: 1/5)
- "Não estou conseguindo acessar a minha conta está horrível" (Score: 3/5)

**Ação Recomendada:**
- Analisar taxa de falha no login. Revisar fluxo de recuperação de senha e biometria.

---

### 5. Segurança (Prioridade: ALTA)

**Métricas:**
- 📊 Frequência: 5 avaliações (1.9% do total)
- ⭐ Severidade Média: 1.20/5
- 🎯 Score de Prioridade: 0.54

**Amostras de Avaliações:**

- "um lixo... bloqueio de poupança sem autorização e etc.." (Score: 1/5)
- "O pior está roubando meu dinheiro cobrando oq eu não devo esse AP e um roubo" (Score: 1/5)
- "O App bloqueou meu ID me impossibilitado fazer transações após atualização." (Score: 1/5)

**Ação Recomendada:**
- Revisar políticas de bloqueio. Implementar notificações proativas de segurança.

---

### 10. PIX (Prioridade: ALTA)

**Métricas:**
- 📊 Frequência: 10 avaliações (3.8% do total)
- ⭐ Severidade Média: 1.70/5
- 🎯 Score de Prioridade: 0.51

**Amostras de Avaliações:**

- "Um lixo...A gente precisa fazer um pix urgente o banco funciona...." (Score: 1/5)
- "Tá um lixo o app de vcs não consigo fazer pix de mizeros 5 reais" (Score: 5/5)
- "As vezes que mais preciso fazer um pix está fora do ar" (Score: 3/5)

**Ação Recomendada:**
- Investigar logs de erro nas transações PIX. Revisar integração com BACEN e timeout de confirmação.

---

### 3. Pagamentos/Boletos (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 3 avaliações (1.1% do total)
- ⭐ Severidade Média: 1.33/5
- 🎯 Score de Prioridade: 0.46

**Amostras de Avaliações:**

- "Péssimo! Os boletos DDA não são excluídos após o pagamento mensal. Por conta disso fiz um pagamento em duplicidade." (Score: 2/5)
- "Agora mesmo estou precisando efetuar o pagamento e não estou conseguindo isso vêm acontecendo toda noite" (Score: 1/5)
- "Paguei a conta da fatura e ainda parece que eu não paguei Outra coisa quando faço compra não chega notificação na mesma hora e no app não mostra a compra só depois de horas" (Score: 1/5)

**Ação Recomendada:**
- Revisar lógica de exclusão de boletos pagos no DDA. Implementar confirmação antes de pagamentos.

---

### 12. Empréstimos/Crédito (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 12 avaliações (4.5% do total)
- ⭐ Severidade Média: 1.67/5
- 🎯 Score de Prioridade: 0.43

**Amostras de Avaliações:**

- "Ruim 👎até hoje não recebi meu cartão." (Score: 1/5)
- "libera nunca o cartão de crédito" (Score: 4/5)
- "Um lixo o nubank foi o único que libera cartão de crédito com limite na hora e não tem essas frescura." (Score: 2/5)

**Ação Recomendada:**
- Melhorar comunicação sobre limites e condições. Revisar fluxo de solicitação.

---

### 10. Atendimento (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 10 avaliações (3.8% do total)
- ⭐ Severidade Média: 1.00/5
- 🎯 Score de Prioridade: 0.41

**Amostras de Avaliações:**

- "Péssimo Atendimento." (Score: 1/5)
- "Péssimo os telefones não funcionam e os atendentes educados" (Score: 1/5)
- "Muita dificuldade para conseguir falar com atendente presencial Não tem suporte Péssimo atendimento online A gente liga nunca consegue resultado Não consigo emitir boleto de renegociação tentando fala..." (Score: 1/5)

**Ação Recomendada:**
- Treinar equipe de suporte. Melhorar tempo de resposta no chat.

---

### 7. Cadastro/Conta (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 7 avaliações (2.6% do total)
- ⭐ Severidade Média: 1.57/5
- 🎯 Score de Prioridade: 0.37

**Amostras de Avaliações:**

- "Faz tempo q espero ser cliente de vcs é vcs não me aprovam" (Score: 1/5)
- "Acabei de baixar o aplicativo e não consigo abrir uma conta salário" (Score: 1/5)
- "Esse aplicativo é muito ruim não tem nenhuma opção de encerramento de conta e o banco parece q fica obrigando o usuário a ficar com a conta e o usuário fica preso no aplicativo sem saber o q que fazer..." (Score: 1/5)

**Ação Recomendada:**
- Revisar fluxo de abertura de conta. Melhorar validação de documentos.

---

### 10. Interface/Usabilidade (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 10 avaliações (3.8% do total)
- ⭐ Severidade Média: 2.50/5
- 🎯 Score de Prioridade: 0.35

**Amostras de Avaliações:**

- "Bota a opção de persona as cores o tema do app. Ou deixa todo vermelho. Está feito. Como vou compartilhar meu Pix não tem a opção. Deixa o app melhor pelo amor de Deus" (Score: 2/5)
- "Quero normaliza meu app" (Score: 5/5)
- "Quando vamos cancelar um.servico o aplicativo nao funciona ." (Score: 1/5)

**Ação Recomendada:**
- Realizar testes de usabilidade com usuários reais. Revisar arquitetura de informação.

---

### 44. Outros (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 44 avaliações (16.5% do total)
- ⭐ Severidade Média: 1.45/5
- 🎯 Score de Prioridade: 0.34

**Amostras de Avaliações:**

- "péssimo" (Score: 1/5)
- "banco horrível tenho é ódio" (Score: 1/5)
- "Ruim demais" (Score: 1/5)

**Ação Recomendada:**
- Analisar casos específicos para identificar padrões.

---

### 3. Saldo/Extrato (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 3 avaliações (1.1% do total)
- ⭐ Severidade Média: 2.67/5
- 🎯 Score de Prioridade: 0.32

**Amostras de Avaliações:**

- "Simplesmente coloco dinheiro na conta e some do nada coloquei um dinheiro ontem pra pagar o cartão de crédito e o dinheiro sumiu e o pior tô só me individando" (Score: 1/5)
- "o dinhero esta sumido da conta" (Score: 3/5)
- "os extratos não atualizam" (Score: 4/5)

**Ação Recomendada:**
- Otimizar carregamento de histórico. Implementar cache local.

---

### 3. Investimentos (Prioridade: BAIXA)

**Métricas:**
- 📊 Frequência: 3 avaliações (1.1% do total)
- ⭐ Severidade Média: 2.67/5
- 🎯 Score de Prioridade: 0.26

**Amostras de Avaliações:**

- "Não consigo resgatar e reaplicar meus investimentos desde sexta-feira Aplicativo instável" (Score: 3/5)
- "o extrato de investimento não atende as minhas expectativas" (Score: 4/5)
- "Tem um bug que não consigo mais acessar meus investimentos" (Score: 1/5)

**Ação Recomendada:**
- Melhorar interface de investimentos. Revisar comunicação de rendimentos.

---

### 6. Notificações (Prioridade: BAIXA)

**Métricas:**
- 📊 Frequência: 6 avaliações (2.3% do total)
- ⭐ Severidade Média: 2.33/5
- 🎯 Score de Prioridade: 0.26

**Amostras de Avaliações:**

- "Não recebo nenhuma notificação de pix" (Score: 1/5)
- "É bom gostei só as notificações de Pix não tem jeito já fiz de tudo e não resolve" (Score: 4/5)
- "Muito fraco não dá alerta de pix" (Score: 1/5)

**Ação Recomendada:**
- Revisar sistema de notificações push. Melhorar configurações de alertas.

---

## Próximos Passos

1. **Revisão Técnica:** Equipes técnicas devem analisar os problemas prioritários
2. **Planejamento de Sprint:** Incluir itens críticos no próximo ciclo de desenvolvimento
3. **Monitoramento Contínuo:** Acompanhar evolução das métricas após correções
4. **Comunicação com Usuários:** Responder avaliações negativas informando sobre correções

---

**Gerado automaticamente pelo sistema de Correlação Funcional de Sentimentos**  
**TCC: Simone Rossetti - Análise de Sentimentos em Apps Bancários**
