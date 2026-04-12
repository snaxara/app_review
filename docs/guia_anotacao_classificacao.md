# Guia de Anotação para Classificação de Avaliações de Apps Bancários

## Objetivo

Este guia tem como objetivo padronizar a classificação de avaliações de aplicativos bancários, garantindo consistência entre diferentes anotadores e melhorando a qualidade do ground truth para treinamento e validação do modelo de categorização automática.

## Princípios Fundamentais

### 1. Classificação Multi-label
- **Uma avaliação pode ter MÚLTIPLAS categorias**
- Se o comentário menciona mais de uma funcionalidade com problema, marque TODAS elas
- Exemplo: "Não consigo entrar no app e quando consigo, o PIX não funciona" → Login/Autenticação + PIX

### 2. Foco em Problemas Funcionais
- Classifique apenas problemas relacionados a funcionalidades do app
- Ignore comentários genéricos sem especificidade (ex: "app ruim", "não gostei")
- Use "Não Identificado" apenas para comentários genéricos sem informação útil

### 3. Consistência
- Siga os critérios definidos para cada categoria
- Em caso de dúvida, consulte os exemplos e contra-exemplos
- Mantenha o mesmo critério ao longo de toda a classificação

## Processo de Classificação

### Passo 1: Análise de Sentimento
1. Leia a avaliação completa
2. Classifique o sentimento:
   - **Negativo**: Reclamação, problema, insatisfação
   - **Positivo**: Elogio, satisfação, recomendação
   - **Neutro**: Informativo, sem tom positivo ou negativo claro

### Passo 2: Identificação de Funcionalidades
1. Identifique TODAS as funcionalidades mencionadas com problemas
2. Para cada funcionalidade, verifique se se encaixa em alguma categoria
3. Se não se encaixar em nenhuma categoria específica, use "Outros" ou "Não Identificado"

### Passo 3: Classificação Multi-label
1. Marque todas as categorias que se aplicam (1 = sim, 0 = não)
2. Não limite a apenas uma categoria
3. Seja específico: prefira categorias específicas a "Outros"

## Taxonomia de Categorias

### 1. PIX
**Descrição**: Problemas relacionados a transferências PIX, chave PIX, QR Code, agendamento PIX.

**Palavras-chave**: PIX, transferência instantânea, chave pix, QR code, QR code PIX, agendamento PIX.

**Exemplos de INCLUSÃO**:
- "Não consigo fazer PIX, sempre dá erro"
- "O QR code não está funcionando"
- "PIX não está sendo processado"

**Exemplos de EXCLUSÃO**:
- "App lento" (é Performance, não PIX)
- "Não consigo entrar" (é Login/Autenticação, não PIX)

**Casos Especiais**:
- Se menciona PIX E outro problema (ex: login), marque AMBOS

---

### 2. Login/Autenticação
**Descrição**: Dificuldades de acesso ao app, problemas com senha, biometria, reconhecimento facial, token, 2FA.

**Palavras-chave**: login, senha, entrar, acesso, biometria, digital, reconhecimento facial, token, autenticação, bloqueado, conta bloqueada.

**Exemplos de INCLUSÃO**:
- "Não consigo fazer login"
- "Biometria não funciona"
- "Esqueci minha senha e não consigo recuperar"
- "App bloqueou minha conta sem motivo"

**Exemplos de EXCLUSÃO**:
- "App não abre" (é Performance, não Login)
- "Não recebo notificações" (é Notificações, não Login)

**Casos Especiais**:
- Problemas de acesso devido a bloqueio geográfico → marcar também "Questões geográficas"
- Problemas de acesso devido a segurança → marcar também "Segurança"

---

### 3. Performance
**Descrição**: Lentidão, travamentos, crashes, app não abre, congela, demora para carregar, fecha sozinho.

**Palavras-chave**: lento, trava, demora, carregando, não abre, fecha sozinho, congela, crash, bug, erro técnico, instável.

**Exemplos de INCLUSÃO**:
- "App muito lento"
- "Trava toda hora"
- "Não consegue abrir o app"
- "Fecha sozinho quando estou usando"
- "Demora muito para carregar"

**Exemplos de EXCLUSÃO**:
- "Não encontro a funcionalidade" (é Interface/Usabilidade)
- "PIX não funciona" (é PIX, não Performance - a menos que mencione lentidão/travamento)

**Casos Especiais**:
- Se menciona lentidão/travamento E problema funcional específico → marcar AMBOS
- "App lento para fazer PIX" → Performance + PIX

---

### 4. Interface/Usabilidade
**Descrição**: Navegação confusa, design difícil de usar, não encontra funcionalidades, menu confuso, interface ruim.

**Palavras-chave**: confuso, difícil de usar, não encontro, complicado, interface, menu, navegação, design, layout.

**Exemplos de INCLUSÃO**:
- "Interface muito confusa"
- "Não consigo encontrar onde pagar minhas contas"
- "Menu difícil de navegar"
- "Design ruim, difícil de usar"

**Exemplos de EXCLUSÃO**:
- "App lento" (é Performance)
- "Não funciona" (é problema funcional específico, não interface)

**Casos Especiais**:
- Se menciona dificuldade de encontrar funcionalidade E problema na funcionalidade → marcar AMBOS
- "Não encontro onde fazer PIX e quando encontro não funciona" → Interface/Usabilidade + PIX

**⚠️ ATENÇÃO**: Esta categoria teve muitas discrepâncias. Use apenas quando o problema é claramente de navegação/interface, não quando é problema funcional específico.

---

### 5. Empréstimos/Crédito
**Descrição**: Questões sobre empréstimos, cartão de crédito, limites, financiamentos, parcelas.

**Palavras-chave**: empréstimo, crédito, limite, cartão, financiamento, parcela, cheque especial.

**Exemplos de INCLUSÃO**:
- "Não consigo solicitar empréstimo"
- "Limite de crédito não aparece"
- "Problema com cartão de crédito"
- "Financiamento não está funcionando"

**Exemplos de EXCLUSÃO**:
- "Tarifa de empréstimo alta" (é Tarifas/Cobranças)
- "Não recebo notificação de empréstimo" (é Notificações)

---

### 6. Pagamentos/Boletos
**Descrição**: Problemas com pagamento de contas, boletos, DDA, duplicidade de pagamento, boletos não aparecem.

**Palavras-chave**: boleto, pagamento, conta, DDA, duplicidade, não paga, conta de luz, água, telefone.

**Exemplos de INCLUSÃO**:
- "Boletos DDA não são excluídos após pagamento"
- "Fiz pagamento em duplicidade"
- "Não consigo pagar minhas contas"
- "Boleto não aparece para pagamento"

**Exemplos de EXCLUSÃO**:
- "PIX não funciona" (é PIX, não Pagamentos/Boletos)
- "App lento para pagar" (é Performance, não Pagamentos/Boletos)

---

### 7. Saldo/Extrato
**Descrição**: Visualização de saldo, extrato, transações, histórico, movimentações não aparecem ou aparecem incorretamente.

**Palavras-chave**: saldo, extrato, transação, histórico, movimentação, lançamento.

**Exemplos de INCLUSÃO**:
- "Saldo não está correto"
- "Extrato não atualiza"
- "Transações não aparecem"
- "Histórico está errado"

**Exemplos de EXCLUSÃO**:
- "Não consigo fazer transferência" (é PIX ou outra funcionalidade)
- "App lento" (é Performance)

---

### 8. Atendimento
**Descrição**: Suporte ao cliente, chat, SAC, atendimento ruim, não consegue falar com suporte.

**Palavras-chave**: atendimento, suporte, ajuda, contato, SAC, chat, call center.

**Exemplos de INCLUSÃO**:
- "Atendimento muito ruim"
- "Chat não funciona"
- "Não consigo falar com suporte"
- "SAC não responde"

**Exemplos de EXCLUSÃO**:
- "App não funciona" (não é problema de atendimento)
- "Não encontro ajuda no app" (é Interface/Usabilidade)

---

### 9. Cadastro/Conta
**Descrição**: Abertura de conta, atualização cadastral, documentos, dados pessoais, verificação de identidade.

**Palavras-chave**: cadastro, abrir conta, dados, atualizar, documento, CPF, identidade, verificação.

**Exemplos de INCLUSÃO**:
- "Não consigo abrir conta"
- "Cadastro não atualiza"
- "Documentos não são aceitos"
- "Dados cadastrais errados"

**Exemplos de EXCLUSÃO**:
- "Não consigo fazer login" (é Login/Autenticação)
- "App lento" (é Performance)

---

### 10. Investimentos
**Descrição**: Aplicações financeiras, poupança, rendimentos, CDB, investimentos não aparecem ou não funcionam.

**Palavras-chave**: investimento, poupança, aplicação, rendimento, CDB, tesouro direto.

**Exemplos de INCLUSÃO**:
- "Investimentos não aparecem"
- "Não consigo aplicar dinheiro"
- "Rendimentos não atualizam"
- "Poupança não funciona"

**Exemplos de EXCLUSÃO**:
- "Rendimento baixo" (não é problema funcional)
- "App lento" (é Performance)

---

### 11. Segurança
**Descrição**: Fraudes, bloqueios indevidos, clonagem, segurança, suspeita de fraude, conta hackeada.

**Palavras-chave**: fraude, bloqueio, segurança, roubo, clonagem, hackeado, suspeita.

**Exemplos de INCLUSÃO**:
- "Minha conta foi hackeada"
- "Bloqueio indevido por fraude"
- "Suspeita de clonagem"
- "Problemas de segurança"

**Exemplos de EXCLUSÃO**:
- "App bloqueou minha conta" (pode ser Login/Autenticação, não Segurança)
- "Não consigo fazer login" (é Login/Autenticação)

**Casos Especiais**:
- Se menciona bloqueio por segurança → marcar Segurança + Login/Autenticação

---

### 12. Notificações
**Descrição**: Alertas, push notifications, avisos, não recebe notificações, notificações não funcionam.

**Palavras-chave**: notificação, alerta, aviso, push, não recebe, aviso de transação.

**Exemplos de INCLUSÃO**:
- "Não recebo notificações de PIX"
- "Push notifications não funcionam"
- "Não recebo alertas de transações"

**Exemplos de EXCLUSÃO**:
- "App não funciona" (não é problema de notificação)
- "PIX não funciona" (é PIX, não Notificações)

**Casos Especiais**:
- Se menciona não receber notificação DE uma funcionalidade → marcar Notificações + funcionalidade
- "Não recebo notificação de PIX" → Notificações + PIX

---

### 13. Questões geográficas
**Descrição**: Problemas com acesso a conta, transferências, pagamentos em outros países, fora do Brasil, exterior, bloqueio geográfico.

**Palavras-chave**: exterior, fora do Brasil, outro país, bloqueio geográfico, viagem, acesso fora do país.

**Exemplos de INCLUSÃO**:
- "Estou no exterior e não tenho acesso"
- "Não consigo fazer transferência fora do Brasil"
- "App bloqueado quando viajo"
- "Não funciona em outros países"

**Exemplos de EXCLUSÃO**:
- "App não funciona" (sem menção geográfica)
- "Não consigo fazer login" (sem menção geográfica)

**Casos Especiais**:
- Se menciona problema geográfico E problema funcional → marcar AMBOS
- "Estou no exterior e não consigo fazer login" → Questões geográficas + Login/Autenticação

---

### 14. Placas/Veículos
**Descrição**: Problemas com IPVA, RENAVAM, licenciamento, multas, DETRAN, veículos, cadastro de veículos.

**Palavras-chave**: IPVA, RENAVAM, licenciamento, multa, DETRAN, veículo, carro, moto, placa.

**Exemplos de INCLUSÃO**:
- "Não consigo pagar IPVA"
- "RENAVAM não aparece"
- "Veículos cadastrados incorretamente"
- "Multas não aparecem"

**Exemplos de EXCLUSÃO**:
- "App lento" (é Performance)
- "Não funciona" (sem menção a veículos)

---

### 15. Tarifas/Cobranças
**Descrição**: Reclamações sobre tarifas, taxas, juros cobrados indevidamente, cobranças não devidas, tarifas altas.

**Palavras-chave**: tarifa, taxa, juros, cobrança, cobrado indevidamente, tarifa alta, taxa abusiva.

**Exemplos de INCLUSÃO**:
- "Estão cobrando tarifa que não uso"
- "Juros cobrados indevidamente"
- "Taxa muito alta"
- "Cobrança não devida"

**Exemplos de EXCLUSÃO**:
- "Empréstimo não funciona" (é Empréstimos/Crédito)
- "App ruim" (genérico)

---

### 16. Outros
**Descrição**: Problemas identificáveis mas que não se encaixam em nenhuma categoria acima.

**Quando usar**:
- Problema específico e identificável
- Não se encaixa em nenhuma categoria acima
- Exemplo: "Problema com cartão de débito" (se não for crédito)

**Quando NÃO usar**:
- Comentários genéricos → use "Não Identificado"
- Problemas que se encaixam em categorias acima → use a categoria específica

---

### 17. Não Identificado
**Descrição**: Comentários genéricos sem informação útil, sem especificidade, apenas opinião sem problema funcional.

**Quando usar**:
- "App ruim"
- "Não gostei"
- "Péssimo"
- "Horrível"
- Comentários sem especificidade

**Quando NÃO usar**:
- Se há problema específico identificável → use categoria específica ou "Outros"
- Se há funcionalidade mencionada → use categoria específica

---

## Casos Complexos e Resolução de Conflitos

### Caso 1: Múltiplas Funcionalidades
**Exemplo**: "App lento e não consigo fazer PIX"
**Solução**: Performance + PIX (ambas)

### Caso 2: Problema de Interface vs. Funcionalidade
**Exemplo**: "Não encontro onde fazer PIX"
**Solução**: Interface/Usabilidade (problema é de navegação, não da funcionalidade)

**Exemplo**: "Não encontro onde fazer PIX e quando encontro não funciona"
**Solução**: Interface/Usabilidade + PIX (ambos os problemas)

### Caso 3: Problema de Performance vs. Funcionalidade
**Exemplo**: "PIX muito lento"
**Solução**: Performance + PIX (ambas)

**Exemplo**: "PIX não funciona"
**Solução**: Apenas PIX (sem menção a lentidão)

### Caso 4: Segurança vs. Login/Autenticação
**Exemplo**: "Conta bloqueada por segurança"
**Solução**: Segurança + Login/Autenticação (ambas)

**Exemplo**: "Não consigo fazer login"
**Solução**: Apenas Login/Autenticação (sem menção a segurança)

### Caso 5: Notificações vs. Funcionalidade
**Exemplo**: "Não recebo notificação de PIX"
**Solução**: Notificações + PIX (ambas)

**Exemplo**: "PIX não funciona"
**Solução**: Apenas PIX (sem menção a notificações)

---

## Checklist de Classificação

Antes de finalizar uma classificação, verifique:

- [ ] Sentimento classificado corretamente?
- [ ] Todas as funcionalidades com problemas foram identificadas?
- [ ] Múltiplas categorias marcadas quando necessário?
- [ ] Categoria específica preferida a "Outros"?
- [ ] "Não Identificado" usado apenas para comentários genéricos?
- [ ] Critérios seguidos consistentemente?

---

## Resolução de Discrepâncias

### Principais Discrepâncias Identificadas

1. **Interface/Usabilidade vs. Funcionalidades Específicas**
   - **Problema**: Muitas avaliações foram classificadas como Interface/Usabilidade quando na verdade eram problemas funcionais específicos
   - **Solução**: Use Interface/Usabilidade apenas quando o problema é claramente de navegação/interface, não quando é problema funcional específico

2. **Performance vs. Funcionalidades Específicas**
   - **Problema**: Alguns classificadores marcaram Performance quando havia problema funcional específico
   - **Solução**: Se menciona problema funcional específico E lentidão/travamento → marcar AMBOS

3. **Login/Autenticação vs. Segurança**
   - **Problema**: Confusão entre bloqueio por segurança e problema de login
   - **Solução**: Se menciona segurança/fraude → marcar Segurança + Login/Autenticação

---

## Referências

- Base de dados: `app_review_dataset_carol.csv` e `app_review_dataset_samuel.csv`
- Ground truth: `ground_truth_dataset.csv`
- Scripts de validação: `validate_model.py`, `calculate_inter_annotator_agreement.py`

---

## Contato e Dúvidas

Em caso de dúvidas sobre classificação, consulte este guia primeiro. Se ainda houver dúvida, documente o caso e discuta com a equipe antes de classificar.

