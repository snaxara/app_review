# Backlog Priorizado - Aplicativo Bancário

**Data de Geração:** 01/12/2025 13:22  
**Total de Avaliações Analisadas:** 20  
**Modelo LLM Utilizado:** gpt-4.1-mini

---

## Resumo Executivo

Este relatório apresenta a priorização de funcionalidades do aplicativo bancário baseada em **20 avaliações negativas** de usuários reais.

### Distribuição de Categorias

| Categoria | Quantidade | Porcentagem | Severidade Média | Prioridade |
|:----------|:-----------|:------------|:-----------------|:-----------|
| Performance | 3 | 15.0% | 1.33/5 | 🟠 ALTA |
| Login/Autenticação | 2 | 10.0% | 3.00/5 | 🟡 MÉDIA |
| Pagamentos/Boletos | 1 | 5.0% | 2.00/5 | 🟡 MÉDIA |
| Outros | 12 | 60.0% | 4.00/5 | 🟡 MÉDIA |
| Empréstimos/Crédito | 1 | 5.0% | 5.00/5 | 🟢 BAIXA |
| Atendimento | 1 | 5.0% | 5.00/5 | 🟢 BAIXA |

---

## Detalhamento por Categoria

### 3. Performance (Prioridade: ALTA)

**Métricas:**
- 📊 Frequência: 3 avaliações (15.0% do total)
- ⭐ Severidade Média: 1.33/5
- 🎯 Score de Prioridade: 0.55

**Amostras de Avaliações:**

- "Não estou gostando desse aplicativo do banco tá travando demora pra abrir tava bom agora tá muito ruim vou cancelar minha conta só passou raiva não ab..." (Score: 1/5)
- "Todas as vezes q preciso entrar no meu banco tenho q reiniciar o aparelho. Não sei o porque disso pois antes não era assim. Será do próprio aparelho o..." (Score: 2/5)
- "por q o APP tá horrível de abri" (Score: 1/5)

**Ação Recomendada:**
- Executar profiling do app. Otimizar tempo de inicialização e identificar memory leaks.

---

### 2. Login/Autenticação (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 2 avaliações (10.0% do total)
- ⭐ Severidade Média: 3.00/5
- 🎯 Score de Prioridade: 0.46

**Amostras de Avaliações:**

- "O aplicativo não está funcionando só fica dizendo que a senha expirou e o aplicativo nem abre." (Score: 1/5)
- "gosto muito desse banco mas não tava conseguindo fazer a senha mas consegui" (Score: 5/5)

**Ação Recomendada:**
- Analisar taxa de falha no login. Revisar fluxo de recuperação de senha e biometria.

---

### 1. Pagamentos/Boletos (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 1 avaliações (5.0% do total)
- ⭐ Severidade Média: 2.00/5
- 🎯 Score de Prioridade: 0.44

**Amostras de Avaliações:**

- "Péssimo! Os boletos DDA não são excluídos após o pagamento mensal. Por conta disso fiz um pagamento em duplicidade." (Score: 2/5)

**Ação Recomendada:**
- Revisar lógica de exclusão de boletos pagos no DDA. Implementar confirmação antes de pagamentos.

---

### 12. Outros (Prioridade: MÉDIA)

**Métricas:**
- 📊 Frequência: 12 avaliações (60.0% do total)
- ⭐ Severidade Média: 4.00/5
- 🎯 Score de Prioridade: 0.36

**Amostras de Avaliações:**

- "Muito bom" (Score: 4/5)
- "bom" (Score: 5/5)
- "bom" (Score: 5/5)

**Ação Recomendada:**
- Analisar casos específicos para identificar padrões.

---

### 1. Empréstimos/Crédito (Prioridade: BAIXA)

**Métricas:**
- 📊 Frequência: 1 avaliações (5.0% do total)
- ⭐ Severidade Média: 5.00/5
- 🎯 Score de Prioridade: 0.23

**Amostras de Avaliações:**

- "achei o app muito bom de usar mas quero cartão com limite q eu não tenho" (Score: 5/5)

**Ação Recomendada:**
- Melhorar comunicação sobre limites e condições. Revisar fluxo de solicitação.

---

## Próximos Passos

1. **Revisão Técnica:** Equipes técnicas devem analisar os problemas prioritários
2. **Planejamento de Sprint:** Incluir itens críticos no próximo ciclo de desenvolvimento
3. **Monitoramento Contínuo:** Acompanhar evolução das métricas após correções
4. **Comunicação com Usuários:** Responder avaliações negativas informando sobre correções

---

**Gerado automaticamente pelo sistema de Correlação Funcional de Sentimentos**  
**TCC: Simone Rossetti - Análise de Sentimentos em Apps Bancários**
