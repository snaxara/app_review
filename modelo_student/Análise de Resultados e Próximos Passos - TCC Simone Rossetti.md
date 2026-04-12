# Análise de Resultados e Próximos Passos - TCC Simone Rossetti

## 1. Resumo Executivo

A execução do modelo **DistilBERT Multilíngue** para análise de sentimentos foi concluída com sucesso. O modelo processou **1.000 avaliações** do aplicativo bancário Santander, gerando classificações de polaridade (positive, negative, neutral) com scores de confiança associados.

---

## 2. Análise dos Resultados Obtidos

### 2.1 Distribuição de Sentimentos

| Sentimento | Contagem | Porcentagem |
|:-----------|:---------|:------------|
| **Positive** | 633 | **63.30%** |
| **Negative** | 331 | **33.10%** |
| **Neutral** | 36 | **3.60%** |

**Interpretação:**
- A maioria das avaliações (63,3%) foi classificada como positiva, o que é esperado considerando que muitas avaliações curtas como "ótimo", "excelente" e "muito bom" são naturalmente positivas.
- Aproximadamente um terço das avaliações (33,1%) foi classificada como negativa, indicando uma quantidade significativa de insatisfação dos usuários.
- A categoria neutral é minoritária (3,6%), o que é comum em modelos de análise de sentimentos treinados para polaridade binária.

### 2.2 Observações Críticas sobre a Qualidade das Predições

#### ⚠️ **Problema Identificado: Falsos Negativos**

Ao analisar as amostras do relatório e do CSV de resultados, identificamos **inconsistências significativas** nas predições do modelo:

| Texto da Avaliação | Score Original | Predição do Modelo | Confiança | Análise |
|:-------------------|:---------------|:-------------------|:----------|:--------|
| "Muito bom" | 5 | **negative** | 0.6788 | ❌ **Erro claro** - Texto positivo classificado como negativo |
| "bom" | 5 | **negative** | 0.6141 | ❌ **Erro claro** - Texto positivo classificado como negativo |
| "gostei muito do atendimento e na resolução do meu problema" | 5 | **negative** | 0.5440 | ❌ **Erro claro** - Texto positivo classificado como negativo |
| "bom de mais" | 5 | **negative** | 0.7004 | ❌ **Erro claro** - Texto positivo classificado como negativo |
| "bom." | 4 | **negative** | 0.7522 | ❌ **Erro claro** - Texto positivo classificado como negativo |

#### 🔍 **Hipóteses para os Erros**

1. **Limitação do Modelo Base:** O modelo `lxyuan/distilbert-base-multilingual-cased-sentiments-student` foi treinado em um corpus genérico e pode não ter sido otimizado especificamente para o português brasileiro coloquial usado em avaliações de apps.

2. **Textos Muito Curtos:** Avaliações extremamente curtas ("bom", "ótimo") podem não fornecer contexto suficiente para o modelo, levando a predições inconsistentes.

3. **Viés de Treinamento:** O modelo pode ter sido treinado com dados onde palavras simples como "bom" aparecem em contextos negativos (ex: "não é bom", "poderia ser bom"), criando um viés.

4. **Pontuação e Formatação:** A presença de pontos finais, emojis ou formatação pode influenciar a predição de forma inesperada.

#### ✅ **Predições Corretas Observadas**

| Texto da Avaliação | Score Original | Predição do Modelo | Confiança | Análise |
|:-------------------|:---------------|:-------------------|:----------|:--------|
| "Não estou gostando desse aplicativo do banco tá travando demora pra abrir tava bom agora tá muito ruim vou cancelar minha conta só passou raiva não abre" | 1 | **negative** | 0.6252 | ✅ Correto |
| "excelente 👏" | 5 | **positive** | 0.9728 | ✅ Correto |
| "muito eficiente" | 5 | **positive** | 0.8195 | ✅ Correto |
| "Péssimo! Os boletos DDA não são excluídos após o pagamento mensal. Por conta disso fiz um pagamento em duplicidade." | 2 | **negative** | 0.5427 | ✅ Correto |

**Observação:** O modelo tem melhor desempenho em textos mais longos e com contexto mais rico.

---

## 3. Implicações para o TCC

### 3.1 Pontos Positivos

✅ **Infraestrutura Funcional:** O pipeline de análise de sentimentos está operacional e pode processar grandes volumes de dados.

✅ **Identificação de Sentimentos Negativos Complexos:** O modelo consegue identificar corretamente avaliações negativas detalhadas, que são justamente as mais relevantes para o objetivo do TCC (correlação funcional e priorização de backlog).

✅ **Escalabilidade:** O código está preparado para processar o dataset completo (30.000+ avaliações).

### 3.2 Limitações Identificadas

⚠️ **Baixa Acurácia em Textos Curtos:** Avaliações muito curtas ("bom", "ótimo") apresentam alta taxa de erro.

⚠️ **Necessidade de Validação Manual:** É essencial validar uma amostra representativa das predições para calcular métricas de desempenho reais (acurácia, precisão, recall, F1-score).

⚠️ **Falta de Fine-Tuning:** O modelo não foi ajustado especificamente para o domínio de avaliações de aplicativos bancários em português brasileiro.

---

## 4. Recomendações e Próximos Passos

### 4.1 Curto Prazo (Próximas 1-2 Semanas)

#### **Passo 1: Validação Manual e Cálculo de Métricas**

**Objetivo:** Calcular a acurácia real do modelo comparando as predições com os scores originais das avaliações.

**Ação:**
1. Criar um script Python para converter os scores originais (1-5 estrelas) em sentimentos (1-2 = negative, 3 = neutral, 4-5 = positive).
2. Comparar com as predições do modelo.
3. Calcular métricas: **Acurácia, Precisão, Recall, F1-Score** e **Matriz de Confusão**.
4. Documentar os resultados no TCC.

**Código sugerido:**
```python
# Adicionar ao script sentiment_analysis.py
def evaluate_model(df):
    """Avalia o modelo comparando com os scores originais."""
    # Converter score original (1-5) para sentimento esperado
    def score_to_sentiment(score):
        if score <= 2:
            return 'negative'
        elif score == 3:
            return 'neutral'
        else:  # 4 ou 5
            return 'positive'
    
    df['expected_sentiment'] = df['score'].apply(score_to_sentiment)
    
    # Calcular métricas
    from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix
    
    accuracy = accuracy_score(df['expected_sentiment'], df['sentiment_label'])
    precision, recall, f1, _ = precision_recall_fscore_support(
        df['expected_sentiment'], 
        df['sentiment_label'], 
        average='weighted'
    )
    
    print(f"\n📊 Métricas de Desempenho:")
    print(f"   Acurácia: {accuracy:.2%}")
    print(f"   Precisão: {precision:.2%}")
    print(f"   Recall: {recall:.2%}")
    print(f"   F1-Score: {f1:.2%}")
    
    return accuracy, precision, recall, f1
```

#### **Passo 2: Testar Modelos Alternativos**

**Objetivo:** Comparar o desempenho do DistilBERT com outros modelos especializados em português.

**Modelos sugeridos:**
1. **`neuralmind/bert-base-portuguese-cased`** - BERT treinado especificamente para português brasileiro.
2. **`cardiffnlp/twitter-xlm-roberta-base-sentiment`** - XLM-RoBERTa multilíngue treinado em dados de redes sociais (mais próximo do contexto de avaliações).
3. **`lxyuan/distilbert-base-multilingual-cased-sentiments-student`** (atual) - Manter como baseline.

**Ação:**
- Modificar o script para testar cada modelo.
- Comparar as métricas de desempenho.
- Documentar os resultados no TCC.

#### **Passo 3: Implementar Pré-processamento Avançado**

**Objetivo:** Melhorar a qualidade dos dados de entrada para o modelo.

**Ações:**
1. **Normalização de Texto:**
   - Remover emojis (ou convertê-los em texto descritivo).
   - Normalizar pontuação excessiva ("!!!!" → "!").
   - Corrigir erros de digitação comuns.

2. **Filtro de Textos Muito Curtos:**
   - Avaliações com menos de 3 palavras podem ser marcadas como "inconclusivas" ou tratadas separadamente.

3. **Enriquecimento de Contexto:**
   - Combinar o texto da avaliação com o score original como entrada adicional para o modelo.

### 4.2 Médio Prazo (Próximas 3-4 Semanas)

#### **Passo 4: Integração com LLM para Correlação Funcional**

**Objetivo:** Adicionar a camada de **correlação funcional** usando um LLM (GPT-4, Gemini ou Llama) para categorizar as avaliações negativas por funcionalidade (PIX, Login, Empréstimos, etc.).

**Abordagem:**
1. **Filtrar Avaliações Negativas:** Selecionar apenas as avaliações classificadas como "negative" pelo modelo de sentimentos.
2. **Prompt Engineering:** Criar prompts estruturados para o LLM categorizar as avaliações.
3. **Categorias Funcionais Sugeridas:**
   - PIX
   - Login/Autenticação
   - Empréstimos/Crédito
   - Interface/Usabilidade
   - Performance/Lentidão
   - Bugs/Erros Técnicos
   - Atendimento ao Cliente
   - Outros

**Exemplo de Prompt:**
```
Você é um especialista em análise de feedbacks de aplicativos bancários. 
Analise a avaliação abaixo e identifique a funcionalidade principal mencionada.

Avaliação: "Não estou gostando desse aplicativo do banco tá travando demora pra abrir tava bom agora tá muito ruim vou cancelar minha conta só passou raiva não abre"

Categorias possíveis: PIX, Login, Empréstimos, Interface, Performance, Bugs, Atendimento, Outros.

Responda APENAS com a categoria principal.
```

**Implementação:**
- Usar a API da OpenAI (GPT-4) ou Google Gemini.
- Processar as avaliações negativas em lote.
- Gerar um novo CSV com a coluna `functional_category`.

#### **Passo 5: Desenvolvimento da API REST**

**Objetivo:** Criar uma API REST para integração com a plataforma KnoolyIa.

**Tecnologia Sugerida:** FastAPI (Python)

**Endpoints Principais:**
1. `POST /analyze` - Recebe uma avaliação e retorna sentimento + categoria funcional.
2. `GET /backlog` - Retorna o backlog priorizado baseado nas avaliações negativas.
3. `GET /metrics` - Retorna métricas agregadas (distribuição de sentimentos, categorias mais problemáticas).

**Estrutura do Projeto:**
```
api/
├── main.py              # FastAPI app
├── models/
│   ├── sentiment.py     # Modelo de sentimentos
│   └── functional.py    # Categorização funcional (LLM)
├── routes/
│   ├── analyze.py       # Endpoint de análise
│   └── backlog.py       # Endpoint de backlog
└── requirements.txt
```

### 4.3 Longo Prazo (Próximas 5-8 Semanas)

#### **Passo 6: Integração com Azure DevOps e Jira**

**Objetivo:** Conectar a API com as ferramentas de gestão de projetos da empresa.

**Funcionalidades:**
- Criar automaticamente issues no Jira baseadas em avaliações negativas.
- Vincular commits do Azure DevOps com categorias funcionais.
- Gerar relatórios de impacto de deploys baseados em feedback dos usuários.

#### **Passo 7: Documentação Acadêmica Completa**

**Objetivo:** Finalizar o TCC com todos os capítulos e seções.

**Estrutura Sugerida:**
1. **Introdução** - Contexto, problema, justificativa.
2. **Revisão Bibliográfica** - Análise de sentimentos, NLP, CRISP-DM.
3. **Metodologia** - Detalhamento técnico (modelos, datasets, pipeline).
4. **Resultados** - Métricas, comparações, análises.
5. **Discussão** - Limitações, implicações práticas.
6. **Conclusão** - Contribuições, trabalhos futuros.
7. **Referências** - Citações acadêmicas.

---

## 5. Checklist de Ações Imediatas

Para a próxima sessão de trabalho, sugiro focar em:

- [ ] **Implementar o script de avaliação de métricas** (Passo 1)
- [ ] **Testar o modelo `neuralmind/bert-base-portuguese-cased`** (Passo 2)
- [ ] **Analisar manualmente 50 avaliações** para validar a qualidade das predições
- [ ] **Documentar os resultados** em uma seção de "Resultados Preliminares" no TCC
- [ ] **Preparar o prompt para o LLM** (categorização funcional)

---

## 6. Conclusão

A execução inicial do modelo DistilBERT foi bem-sucedida e demonstrou a viabilidade técnica do projeto. No entanto, as inconsistências identificadas (especialmente em textos curtos) indicam a necessidade de:

1. **Validação rigorosa** das predições com métricas quantitativas.
2. **Exploração de modelos alternativos** especializados em português.
3. **Implementação da camada de correlação funcional** com LLM para agregar valor ao projeto.

O próximo passo crítico é **calcular as métricas de desempenho** para fundamentar a discussão metodológica no TCC e justificar a escolha (ou troca) do modelo de sentimentos.

---

**Preparado por:** Manus AI  
**Data:** 01 de Dezembro de 2025  
**Projeto:** TCC - Correlação Funcional de Sentimentos em Apps Bancários
