# Resumo Executivo - Modelo de Análise de Sentimento

**Data:** Janeiro 2026  
**Responsável:** Simone Rossetti Nobre Naxara

## Objetivo

Este documento apresenta o modelo desenvolvido para análise de sentimentos de comentários de aplicativos bancários, incluindo os scripts, metodologia e resultados obtidos.

## O Que Foi Desenvolvido

Foi implementado um pipeline completo de análise de comentários de aplicativos bancários que realiza três etapas principais:

### 1. Coleta de Dados (`collect_reviews.py`)

- **O que faz:** Coleta avaliações da Google Play Store automaticamente
- **Período:** Últimos 15 dias (configurável)
- **Saída:** Arquivo CSV com avaliações coletadas
- **Dependências:** Biblioteca `google-play-scraper`

### 2. Análise de Polarização (`sentiment_analysis.py`)

- **O que faz:** Classifica cada comentário como positivo, negativo ou neutro
- **Modelo utilizado:** BERTweet (`cardiffnlp/twitter-xlm-roberta-base-sentiment`)
- **Por que este modelo:**
  - Pré-treinado com dados de redes sociais
  - Funciona bem com português brasileiro
  - Executa localmente (não requer API externa)
  - Alta acurácia: 96.17% validado com dados reais
  
- **Métricas de desempenho:**
  - Acurácia: 96.17%
  - Precisão: 98.17%
  - Recall: 96.17%
  - F1-Score: 96.92%
  - ROC AUC: 98.97%

- **Saída:** Arquivo CSV com colunas `sentiment_label` e `sentiment_score`

### 3. Categorização Funcional (`functional_correlation.py`)

- **O que faz:** Categoriza avaliações negativas em funcionalidades específicas do aplicativo
- **Modelo utilizado:** GPT-4o (configurável via variável de ambiente)
- **Categorias:** 15 categorias funcionais (PIX, Login/Autenticação, Performance, etc.)
- **Características:**
  - Suporta múltiplas categorias por avaliação
  - Processa apenas avaliações negativas
  - Reutiliza resultados anteriores (não reprocessa avaliações já categorizadas)

## Modelo de Dados

### Estrutura de Entrada (Coleta)

```
app_review_dataset.csv
├── reviewId: ID único da avaliação
├── content: Texto do comentário
├── date: Data da avaliação
├── version: Versão do app mencionada
├── app_name: Nome do aplicativo
└── rating: Nota de 1 a 5 estrelas
```

### Estrutura de Saída (Análise de Polarização)

```
sentiment_results.csv
├── [todas as colunas anteriores]
├── sentiment_label: "positive", "negative" ou "neutral"
└── sentiment_score: Score de confiança (0.0 a 1.0)
```

### Estrutura de Saída (Categorização Funcional)

```
functional_correlation_results.csv
├── [todas as colunas anteriores]
├── PIX: 0 ou 1 (problemas com PIX)
├── Login/Autenticação: 0 ou 1
├── Performance: 0 ou 1
├── Interface/Usabilidade: 0 ou 1
├── Empréstimos/Crédito: 0 ou 1
├── Pagamentos/Boletos: 0 ou 1
├── Saldo/Extrato: 0 ou 1
├── Atendimento: 0 ou 1
├── Cadastro/Conta: 0 ou 1
├── Investimentos: 0 ou 1
├── Segurança: 0 ou 1
├── Notificações: 0 ou 1
├── Questões geográficas: 0 ou 1
├── Placas/Veículos: 0 ou 1
├── Tarifas/Cobranças: 0 ou 1
└── Outros: 0 ou 1
```

## Categorias Funcionais Definidas

1. **PIX:** Problemas com transferências PIX, chave PIX, QR Code
2. **Login/Autenticação:** Dificuldades de acesso, senha, biometria
3. **Performance:** Lentidão, travamentos, crashes, consumo de recursos
4. **Interface/Usabilidade:** Navegação confusa, design difícil
5. **Empréstimos/Crédito:** Questões sobre crédito e empréstimos
6. **Pagamentos/Boletos:** Problemas com pagamento de contas e boletos
7. **Saldo/Extrato:** Visualização de saldo e histórico
8. **Atendimento:** Suporte ao cliente, chat, SAC
9. **Cadastro/Conta:** Abertura e atualização de conta
10. **Investimentos:** Aplicações financeiras, poupança
11. **Segurança:** Fraudes, bloqueios indevidos, adesões não autorizadas
12. **Notificações:** Alertas e push notifications
13. **Questões geográficas:** Problemas de acesso no exterior
14. **Placas/Veículos:** IPVA, RENAVAM, multas, DETRAN
15. **Tarifas/Cobranças:** Reclamações sobre tarifas e taxas
16. **Outros:** Problemas não categorizados

## Como Usar

### Requisitos

1. Python 3.8 ou superior
2. Bibliotecas Python (instalar via `pip install`):
   - pandas
   - transformers
   - openai
   - google-play-scraper
   - python-dotenv

3. Chave de API OpenAI (para categorização funcional)
   - Criar arquivo `.env` com: `OPENAI_API_KEY=sua_chave_aqui`

### Execução

1. **Coletar avaliações:**
   ```bash
   python collect_reviews.py
   ```

2. **Analisar polarização:**
   ```bash
   python sentiment_analysis.py
   ```

3. **Categorizar funcionalmente:**
   ```bash
   python functional_correlation.py
   ```

## Resultados Obtidos

- **Validação realizada:** 366 avaliações classificadas manualmente
- **Modelo BERTweet:** 96.17% de acurácia na classificação de polarização
- **Modelo GPT-4o:** 63.6% de acurácia no mapeamento entidade → BusinessCapability

## Próximos Passos para Desenvolvimento

1. **Integração com sistema de produção:**
   - Automatizar coleta periódica de avaliações
   - Criar pipeline de processamento automatizado
   - Implementar alertas para categorias críticas

2. **Melhorias no modelo:**
   - Ajustar prompts de categorização funcional
   - Treinar modelo específico para domínio bancário (opcional)
   - Implementar feedback loop para melhorar precisão

3. **Dashboard e visualizações:**
   - Criar interface para visualização dos resultados
   - Implementar gráficos de tendências
   - Relatórios automáticos de backlog priorizado

## Arquivos Incluídos

- `collect_reviews.py`: Script de coleta de dados
- `sentiment_analysis.py`: Script de análise de polarização
- `functional_correlation.py`: Script de categorização funcional
- `README.md`: Documentação completa do projeto
- `RESUMO_EXECUTIVO.md`: Este documento

## Contato

Para dúvidas sobre o modelo ou scripts, entre em contato com a equipe de desenvolvimento.
