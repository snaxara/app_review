# Refinamento do Projeto TCC Baseado em Dados Reais da Caixa

## Análise dos Dados de Defeitos

### Estatísticas Principais

- **Defeitos em Produção**: 4.489 (67.6%)
- **Defeitos Não Produção**: 2.155 (32.4%)
- **Total de Sistemas**: 51 sistemas mapeados
- **Defeitos relacionados ao App Móvel em Produção**: 98 defeitos
  - SINBC (Internet Banking): 39
  - SIACC (PIX): 37
  - SIGLM (Gestão de Limites): 11
  - SIPPG (Meios de Pagamento): 10
  - SIGMP (Sou Caixa app): 1

### Top Comunidades com Mais Defeitos em Produção

1. Crédito Comercial e Agronegócio: 452
2. Depósitos e Captação: 445
3. Meios de Pagamento: 380
4. Clientes: 305
5. Câmbio, Investimentos e Mercado de Capitais: 279

### Distribuição por Criticidade (Produção)

- **Q3** (Mais Crítica): 1.506 defeitos (33.5%)
- **Q1**: 1.486 defeitos (33.1%)
- **Q2**: 925 defeitos (20.6%)
- **Q4**: 571 defeitos (12.7%)

---

## Propostas de Refinamento

### 1. Mapeamento Sistema → BusinessCapability

Criar um mapeamento dos sistemas da Caixa para BusinessCapabilities baseado nas comunidades:

**Mapeamento Proposto:**

| Sistema | Comunidade | BusinessCapability Proposta |
|---------|-----------|----------------------------|
| SINBC | Box Relacionamento Digital | Autenticação e Acesso, Interface e Experiência do Usuário |
| SIACC | Arrecadação e Convênios | Transferências PIX, Pagamentos e Boletos |
| SIGLM | Estruturantes de TI | Empréstimos e Crédito |
| SIPPG | Meios de Pagamento | Pagamentos e Boletos |
| SIGMP | Pessoas | Interface e Experiência do Usuário |
| SID52 | Depósitos e Captação | Consulta de Saldo e Extrato |
| SILCR | Depósitos e Captação | Empréstimos e Crédito |
| SIACI | Administração do Crédito Imobiliário | Empréstimos e Crédito |
| SIIFX | Câmbio, Investimentos | Investimentos |
| SISOU | Clientes | Atendimento ao Cliente |

### 2. Validação Cruzada: Comentários vs Defeitos em Produção

**Objetivo**: Validar se os problemas identificados nos comentários do app correspondem aos defeitos reais registrados.

**Metodologia**:
- Extrair keywords dos nomes dos defeitos em produção relacionados ao app
- Comparar com issues extraídas dos comentários
- Identificar:
  - **Correspondências**: Problemas mencionados nos comentários que têm defeitos registrados
  - **Lacunas**: Problemas nos comentários sem defeitos registrados (oportunidade de melhoria)
  - **Defeitos sem feedback**: Defeitos registrados que não aparecem nos comentários (pode indicar baixa visibilidade ou baixo impacto)

### 3. Priorização Baseada em Criticidade Real

**Ajuste Proposto**: Incorporar a criticidade Q1-Q4 dos defeitos reais no algoritmo de priorização:

- **Q1**: Alta criticidade → Multiplicador 1.5x na priorização
- **Q2**: Média-Alta → Multiplicador 1.2x
- **Q3**: Média → Multiplicador 1.0x (padrão)
- **Q4**: Baixa → Multiplicador 0.8x

### 4. Refinamento de BusinessCapabilities Baseado em Comunidades

**Ajustes Propostos**:

1. **Adicionar BusinessCapability "Crédito Comercial e Agronegócio"** (nível 2, Core, High)
   - Baseado na comunidade com mais defeitos (452)
   - Diferente de "Empréstimos e Crédito" que é mais focado em PF

2. **Expandir "Meios de Pagamento"** 
   - Incluir sistemas como SIPPG, SIACC
   - 380 defeitos em produção indicam alta criticidade

3. **Adicionar "Câmbio e Investimentos"** como capability separada
   - 279 defeitos em produção
   - Diferente de "Investimentos" que é mais genérico

### 5. Análise de Taxa de Captura de Defeitos

**Insight Crítico**: 
- 67.6% dos defeitos chegam em produção
- Apenas 32.4% são capturados antes de produção

**Implicação para o Projeto**:
- O projeto propõe uma forma adicional de captura de defeitos **além da esteira**
- Os comentários do app podem identificar problemas que não foram capturados nem em testes nem em produção inicial
- Validar se há correlação entre defeitos em produção e comentários negativos

### 6. Mapeamento de Siglas para Contexto

**Proposta**: Criar um dicionário de siglas da Caixa para melhorar o entendimento do contexto:

- SINBC = Sistema Internet Banking Caixa
- SIACC = Sistema de Agendamento de Compromissos de Cliente (PIX)
- SIGLM = Sistema de Gestão de Limites
- SIPPG = Sistema de Pagamentos
- SIGMP = Sou Caixa app

Isso pode ajudar a:
- Correlacionar comentários com sistemas específicos
- Entender melhor o contexto dos problemas
- Mapear para BusinessCapabilities mais precisamente

---

## Próximos Passos Sugeridos

1. **Criar script de validação cruzada**: Comparar issues dos comentários com defeitos em produção
2. **Ajustar BusinessCapabilities**: Adicionar capabilities baseadas nas comunidades reais
3. **Refinar algoritmo de priorização**: Incorporar criticidade Q1-Q4
4. **Criar mapeamento Sistema → BusinessCapability**: Baseado nas siglas e comunidades
5. **Análise de lacunas**: Identificar problemas nos comentários sem defeitos registrados
6. **Atualizar documento TCC**: Incluir análise comparativa com dados reais da Caixa

---

## Impacto Esperado

- **Maior precisão** no mapeamento de issues para BusinessCapabilities
- **Validação empírica** da abordagem proposta
- **Priorização mais precisa** baseada em criticidade real
- **Identificação de lacunas** no processo de QA atual
- **Demonstração de valor** da abordagem de testes além da esteira
