# Ajustes Necessários na Apresentação - Feedback do Gestor

## 📋 Feedback Recebido

1. **Falta detalhar o método** - Precisa explicar melhor como funciona
2. **Falta detalhar o modelo** - Especificar qual modelo, versão, parâmetros
3. **Estava enviesado** - Não tinha base humana para validação

## ✅ O que foi feito

- ✅ Duas pessoas do time classificaram 1000 avaliações
- ✅ Carol já entregou suas classificações (polaridade + categorias)
- ✅ Dataset validado e corrigido

## 📊 Dados Reais para Atualizar

### Slide 2 e 3: Estatísticas de Sentimentos

**ANTES (enviesado):**
- "72.76% das críticas são negativas"

**DEPOIS (com base humana - Carol):**
- **Total:** 1000 avaliações classificadas manualmente
- **Positivas:** 676 (67.6%)
- **Negativas:** 294 (29.4%)
- **Neutras:** 29 (2.9%)

**Observação:** O número anterior estava enviesado porque vinha apenas do modelo de sentimento. Agora temos validação humana.

### Slide 4: Preparação dos Dados

**ANTES:**
- "Meta de mais de 10.000 comentários para treinamento e validação"
- "Rotulagem: Criação de rótulos de negócio"

**DEPOIS:**
- **Dataset de Treino/Validação:** 1000 avaliações classificadas manualmente por humanos
- **Rotulagem Humana:** 
  - Polaridade (positive/negative/neutral) classificada manualmente
  - Categorias funcionais (16 categorias) classificadas manualmente
  - Classificação múltipla (uma avaliação pode ter múltiplas categorias)
- **Validação:** 294 avaliações negativas com categorias funcionais identificadas

### Slide 5: Modelagem - DETALHAR MÉTODO E MODELO

**ADICIONAR:**

#### Método Detalhado:

1. **Análise de Sentimentos:**
   - **Modelo:** `cardiffnlp/twitter-xlm-roberta-base-sentiment`
   - **Framework:** Hugging Face Transformers
   - **Técnica:** Fine-tuning em dados de redes sociais (tweets)
   - **Saída:** Sentimento (positive/negative/neutral) + score de confiança

2. **Correlação Funcional:**
   - **Modelo:** GPT-4o (OpenAI)
   - **Técnica:** Prompt Engineering com zero-shot learning
   - **Abordagem:** Classificação múltipla (múltiplas categorias por avaliação)
   - **Taxonomia:** 16 categorias funcionais:
     - PIX, Login/Autenticação, Performance, Interface/Usabilidade
     - Empréstimos/Crédito, Pagamentos/Boletos, Saldo/Extrato
     - Atendimento, Cadastro/Conta, Investimentos, Segurança
     - Notificações, Questões geográficas, Placas/Veículos
     - Tarifas/Cobranças, Outros

3. **Pipeline de Processamento:**
   ```
   Avaliação → Análise Sentimento → Filtro (negativas) → Correlação Funcional → Categorias Múltiplas
   ```

#### Parâmetros do Modelo:

- **GPT-4o:**
  - Temperature: 0.3 (baixa para consistência)
  - Max Tokens: 200 (suporta múltiplas categorias)
  - Prompt Engineering: Instruções detalhadas com exemplos

- **DistilBERT:**
  - Batch Size: 16
  - Device: CPU
  - Normalização de labels: positive/negative/neutral

### Slide 6: Avaliação - ADICIONAR MÉTRICAS COM BASE HUMANA

**ADICIONAR:**

#### Validação com Base Humana:

- **Dataset de Validação:** 1000 avaliações classificadas manualmente
- **Classificador:** Carol (primeira pessoa)
- **Status:** Aguardando segunda classificação para cálculo de inter-annotator agreement

#### Métricas a Calcular:

1. **Acurácia do Modelo de Sentimento:**
   - Comparação: Modelo DistilBERT vs. Classificação Humana (Carol)
   - Dataset: 1000 avaliações

2. **Acurácia da Correlação Funcional:**
   - Comparação: LLM GPT-4o vs. Classificação Humana (Carol)
   - Métricas por categoria: Precision, Recall, F1-Score
   - Dataset: 294 avaliações negativas

3. **Inter-Annotator Agreement:**
   - Coeficiente de concordância entre dois classificadores humanos
   - Métrica: Cohen's Kappa ou similar
   - Status: Aguardando segunda classificação

#### Resultados Esperados:

- **F1-Score > 80%** por categoria funcional
- **Acurácia geral > 85%** na classificação de sentimentos
- **Inter-Annotator Agreement > 0.7** (concordância substancial)

### Slide 8: Próximos Passos - ATUALIZAR

**ANTES:**
- Cronograma genérico

**DEPOIS:**

#### Próximos Passos Imediatos:

1. **✅ Concluído:** Classificação manual de 1000 avaliações (Carol)
2. **🔄 Em andamento:** 
   - Receber segunda classificação manual
   - Calcular inter-annotator agreement
   - Comparar modelo LLM vs. classificação humana
3. **📅 Próximas semanas:**
   - Resolver discrepâncias entre classificadores
   - Ajustar prompts do LLM baseado em erros identificados
   - Calcular métricas finais de acurácia
   - Preparar dataset final para treino/fine-tuning (se necessário)

#### Cronograma Revisado:

- **Mês 1:** ✅ Coleta e Preparação de Dados + Classificação Humana
- **Mês 2:** Validação e Ajuste do Modelo (com base humana)
- **Mês 3:** Treinamento e Validação Final
- **Mês 4:** Desenvolvimento e Integração da API
- **Mês 5-6:** Entrega Final do TCC

## 🎯 Ajustes Específicos por Slide

### Slide 2: Entendimento do Negócio
- [ ] Atualizar: "29.4% das críticas são negativas" (com nota sobre validação humana)
- [ ] Adicionar: "1000 avaliações validadas manualmente"

### Slide 3: Entendimento dos Dados
- [ ] Atualizar estatísticas com dados reais
- [ ] Adicionar: "Dataset validado por classificadores humanos"

### Slide 4: Preparação dos Dados
- [ ] Atualizar: "1000 avaliações classificadas manualmente"
- [ ] Adicionar: "16 categorias funcionais identificadas"
- [ ] Adicionar: "Classificação múltipla (múltiplas categorias por avaliação)"

### Slide 5: Modelagem
- [ ] **DETALHAR MÉTODO:** Adicionar seção completa sobre método
- [ ] **DETALHAR MODELO:** Especificar modelos, versões, parâmetros
- [ ] Adicionar: Taxonomia completa de 16 categorias
- [ ] Adicionar: Explicação de classificação múltipla

### Slide 6: Avaliação
- [ ] Adicionar: Métricas com base humana
- [ ] Adicionar: Status da validação (Carol concluída, segunda pessoa pendente)
- [ ] Adicionar: Métricas esperadas (F1-Score > 80%)

### Slide 8: Próximos Passos
- [ ] Atualizar cronograma com status atual
- [ ] Adicionar: Próximos passos imediatos (segunda classificação, métricas)

## 📝 Notas Importantes

1. **Remover viés:** Todos os números agora têm base em classificação humana
2. **Transparência:** Deixar claro que o modelo será validado contra classificação humana
3. **Metodologia:** Detalhar completamente método e modelo para evitar ambiguidades

