# Melhorias no Mapeamento de Entidades para BusinessCapabilities

## Data: 16/01/2026

## Resumo

Ajustes realizados no mapeamento de entidades para BusinessCapabilities baseados na validação manual de 20 comentários processados pelos modelos GPT.

## Problemas Identificados e Correções

### 1. **Empréstimos e Crédito**
**Problema:** Entidades relacionadas a cartão de crédito e refinanciamento estavam sendo mapeadas incorretamente.

**Correções:**
- ✅ `cartão físico não chegou` → Empréstimos e Crédito (antes: Performance)
- ✅ `atraso na entrega do cartão` → Empréstimos e Crédito
- ✅ `não consigo refinanciar` → Empréstimos e Crédito (antes: Performance)
- ✅ `refinanciar` → Empréstimos e Crédito

### 2. **Atendimento ao Cliente**
**Problema:** Problemas de atendimento telefônico e comunicação estavam sendo classificados como Performance.

**Correções:**
- ✅ `telefone péssimo` → Atendimento ao Cliente (antes: Performance)
- ✅ `atendimento telefônico péssimo` → Atendimento ao Cliente
- ✅ `atendimento automatizado insatisfatório` → Atendimento ao Cliente
- ✅ `enrolada no chat` → Atendimento ao Cliente
- ✅ `problemas de comunicação` → Atendimento ao Cliente
- ✅ `espera sem atendimento` → Atendimento ao Cliente

### 3. **Investimentos**
**Problema:** Problemas relacionados a investimentos e resgates não estavam sendo identificados corretamente.

**Correções:**
- ✅ `problemas de resgate` → Investimentos (antes: Performance)
- ✅ `não dá pra resgatar` → Investimentos
- ✅ `setor de investimento não atualizado` → Investimentos
- ✅ `propostas de contratos indesejados` → Investimentos (antes: Sem BusinessCapability)

### 4. **Acesso Geográfico**
**Problema:** Ausência de agência não estava sendo mapeada.

**Correções:**
- ✅ `ausência de agência` → Questões geográficas (antes: Performance)
- ✅ `não tem agência` → Questões geográficas
- ✅ `agência na cidade` → Questões geográficas

### 5. **Performance e Estabilidade**
**Problema:** Alguns problemas técnicos específicos estavam sendo classificados incorretamente.

**Correções:**
- ✅ `app trava na hora de receber o pagamento` → Performance (antes: Pagamentos e Boletos)
- ✅ Melhorada lógica de distinção entre "app não abre" (Performance) vs "não abre conta" (Cadastro)

### 6. **Pagamentos e Boletos**
**Problema:** Problemas de compensação não estavam sendo identificados.

**Correções:**
- ✅ `atraso na compensação de ipva` → Pagamentos e Boletos (antes: Performance)
- ✅ `compensação de documento` → Pagamentos e Boletos
- ✅ `compensação` → Pagamentos e Boletos

### 7. **Gestão de Tarifas**
**Problema:** Comentários sobre custos e comparações não estavam sendo mapeados.

**Correções:**
- ✅ `comparação com custo de arroz` → Gestão de Tarifas (antes: Performance)
- ✅ `comparação com custo` → Gestão de Tarifas
- ✅ `desconto insuficiente` → Gestão de Tarifas

### 8. **Gestão de Cadastro e Conta**
**Problema:** Problemas de atualização de dados não estavam sendo identificados.

**Correções:**
- ✅ `não consegui atualizar meus dados` → Gestão de Cadastro e Conta (antes: Performance)
- ✅ `atualizar dados` → Gestão de Cadastro e Conta
- ✅ `atualizar cadastro` → Gestão de Cadastro e Conta

### 9. **Autenticação e Acesso**
**Problema:** Problemas de login e acesso não estavam sendo diferenciados de problemas de cadastro.

**Correções:**
- ✅ `dificuldade para logar` → Login/Autenticação (antes: Performance)
- ✅ `erro ao entrar na conta` → Login/Autenticação (antes: Cadastro)
- ✅ `falta de acesso para consulta` → Login/Autenticação

### 10. **Interface e Experiência do Usuário**
**Problema:** Problemas de interface e frustração do usuário não estavam sendo identificados.

**Correções:**
- ✅ `frustração dos usuários` → Interface e Experiência do Usuário (antes: Performance)
- ✅ `desativar contatos de agenda para fazer pix` → Interface e Experiência do Usuário (antes: Cadastro)

### 11. **Segurança e Proteção**
**Problema:** Problemas de privacidade e monitoramento não estavam sendo identificados.

**Correções:**
- ✅ `monitoramento` → Segurança e Proteção (antes: Performance)
- ✅ `privacidade` → Segurança e Proteção (antes: Performance)
- ✅ `espionam` → Segurança e Proteção

### 12. **Saldo e Extrato**
**Problema:** Problemas específicos de saldo não estavam sendo identificados.

**Correções:**
- ✅ `saldo incorreto` → Saldo/Extrato
- ✅ `não consigo acessar saldo` → Saldo/Extrato

## Melhorias na Lógica de Mapeamento

1. **Ordem de Prioridade:** Mapeamentos mais específicos (frases completas) são verificados antes de termos genéricos
2. **Contexto do Comentário:** Melhorada a lógica para distinguir "app não abre" (Performance) de "não abre conta" (Cadastro)
3. **Cobertura Expandida:** Adicionados mais de 50 novos mapeamentos baseados nos erros identificados

## Próximos Passos

1. Reprocessar os 20 comentários com o mapeamento atualizado
2. Validar se os erros foram corrigidos
3. Se necessário, ajustar ainda mais baseado em novos padrões identificados

## Arquivos Modificados

- `scripts/knowledge_graph/process_reviews_to_graph.py` - Função `map_entity_to_capability`
