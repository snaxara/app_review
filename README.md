# Sistema de Análise de Comentários de Aplicativos Bancários

Este projeto implementa um pipeline completo para análise de comentários de aplicativos bancários, desde a coleta de dados até a criação de um Knowledge Graph temporal para priorização de backlog.

## Visão Geral

O sistema processa avaliações de aplicativos bancários coletadas da Google Play Store, realiza análise de sentimentos e categorização funcional, e constrói um Knowledge Graph temporal no Neo4j para identificar problemas críticos e priorizar ações de correção.

### Modelos Utilizados

- **BERTweet** (`cardiffnlp/twitter-xlm-roberta-base-sentiment`): Modelo pré-treinado para análise de polarização de comentários (positivo/negativo/neutro)
- **GPT-4o**: Modelo de linguagem para categorização funcional e extração de entidades (escolhido na execução)

## Estrutura do Projeto

```
app_review/
├── scripts/                          # Scripts principais
│   ├── sentiment_analysis.py         # Análise de polarização com BERTweet
│   ├── functional_correlation.py     # Categorização funcional com GPT-4o
│   ├── collect_reviews.py            # Coleta de avaliações da Play Store
│   ├── knowledge_graph/               # Scripts do Knowledge Graph
│   │   ├── init_graph.py             # Inicialização do grafo Neo4j
│   │   ├── create_capabilities.py    # Criação de BusinessCapabilities
│   │   ├── entity_extraction.py      # Extração de entidades com GPT-4o
│   │   ├── process_reviews_to_graph.py # Processamento completo para o grafo
│   │   └── graph_manager.py           # Gerenciador de conexão Neo4j
│   └── analysis/                      # Scripts de análise e validação
├── data/                              # Datasets e resultados
│   ├── app_review_dataset.csv         # Avaliações coletadas
│   ├── sentiment_results.csv          # Resultados da análise de sentimentos
│   └── functional_correlation_results.csv # Resultados da categorização
└── Documentos/                        # Documentação e TCC
```

## Requisitos

### Dependências Python

- `pandas`: Manipulação de dados
- `transformers`: Biblioteca Hugging Face para modelos BERTweet
- `openai`: Cliente OpenAI para GPT-4o
- `neo4j`: Driver para conexão com Neo4j
- `python-dotenv`: Carregamento de variáveis de ambiente

Instale as dependências:

```bash
pip install pandas transformers openai neo4j python-dotenv
```

### Configuração de Ambiente

Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
# OpenAI API Key (obrigatório para categorização funcional)
OPENAI_API_KEY=sua_chave_openai_aqui

# Modelo GPT a ser usado (opcional, padrão: gpt-4o)
OPENAI_MODEL=gpt-4o

# Neo4j Connection (obrigatório para Knowledge Graph)
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=sua_senha_neo4j
```

### Pré-requisitos

1. **Neo4j**: Instale e configure o Neo4j (versão 4.x ou superior)
   - Download: https://neo4j.com/download/
   - Ou use Docker: `docker run -p 7474:7474 -p 7687:7687 neo4j:latest`

2. **OpenAI API Key**: Obtenha uma chave de API em https://platform.openai.com/

## Fluxo de Trabalho

### 1. Coleta de Avaliações

Coleta avaliações do aplicativo Santander da Google Play Store:

```bash
python scripts/collect_reviews.py
```

**Saída**: `app_review_dataset.csv` com colunas:
- `reviewId`: ID único da avaliação
- `content`: Texto do comentário
- `date`: Data da avaliação
- `version`: Versão do app mencionada
- `app_name`: Nome do aplicativo
- `rating`: Nota de 1 a 5 estrelas

### 2. Análise de Polarização

Classifica cada comentário como positivo, negativo ou neutro usando o modelo BERTweet:

```bash
python scripts/sentiment_analysis.py
```

**Entrada**: `app_review_dataset.csv`  
**Saída**: `sentiment_results.csv` com colunas adicionais:
- `sentiment_label`: "positive", "negative" ou "neutral"
- `sentiment_score`: Score de confiança (0.0 a 1.0)

**Modelo**: BERTweet (`cardiffnlp/twitter-xlm-roberta-base-sentiment`)
- Modelo pré-treinado multilíngue treinado com dados de redes sociais
- Executa localmente (não requer API)
- Primeira execução baixa o modelo automaticamente (~500MB)

### 3. Categorização Funcional

Categoriza avaliações negativas em funcionalidades do aplicativo usando GPT-4o:

```bash
python scripts/functional_correlation.py
```

**Entrada**: `sentiment_results.csv`  
**Saída**: `functional_correlation_results.csv` com colunas binárias para cada categoria:
- `PIX`: Problemas com transferências PIX
- `Login/Autenticação`: Dificuldades de acesso
- `Performance`: Lentidão, travamentos, crashes
- `Interface/Usabilidade`: Problemas de navegação e design
- `Empréstimos/Crédito`: Questões sobre crédito e empréstimos
- `Pagamentos/Boletos`: Problemas com pagamentos
- `Saldo/Extrato`: Visualização de saldo e histórico
- `Atendimento`: Suporte ao cliente
- `Cadastro/Conta`: Abertura e atualização de conta
- `Investimentos`: Aplicações financeiras
- `Segurança`: Fraudes e bloqueios indevidos
- `Notificações`: Alertas e push notifications
- `Questões geográficas`: Problemas de acesso no exterior
- `Placas/Veículos`: IPVA, RENAVAM, multas
- `Tarifas/Cobranças`: Reclamações sobre tarifas
- `Outros`: Problemas não categorizados

**Modelo**: GPT-4o (configurável via variável de ambiente `OPENAI_MODEL`)
- Suporta múltiplas categorias por avaliação
- Processa apenas avaliações negativas
- Reutiliza resultados anteriores (não reprocessa avaliações já categorizadas)

**Configuração do Modelo**:

O modelo GPT pode ser escolhido na execução através da variável de ambiente `OPENAI_MODEL`. Por padrão, usa `gpt-4o`. Para usar outro modelo:

```bash
# Windows PowerShell
$env:OPENAI_MODEL="gpt-4o-mini"
python scripts/functional_correlation.py

# Linux/Mac
export OPENAI_MODEL="gpt-4o-mini"
python scripts/functional_correlation.py
```

Ou edite o arquivo `.env`:

```env
OPENAI_MODEL=gpt-4o-mini
```

### 4. Inicialização do Knowledge Graph

Prepara o Neo4j com a estrutura do Knowledge Graph:

```bash
python scripts/knowledge_graph/init_graph.py
```

**O que faz**:
- Cria índices para otimização de queries
- Configura constraints e propriedades do grafo
- Prepara estrutura para armazenar entidades e relacionamentos

**Para limpar dados existentes**:

```bash
python scripts/knowledge_graph/init_graph.py --reset
```

### 5. Criação de BusinessCapabilities

Cria os nós de BusinessCapability no grafo baseado nas categorias funcionais:

```bash
python scripts/knowledge_graph/create_capabilities.py
```

**O que faz**:
- Cria 15 BusinessCapabilities correspondentes às categorias funcionais
- Define níveis hierárquicos, tipos, maturidade e valor de negócio
- Estabelece relacionamentos entre capacidades quando aplicável

### 6. Processamento para Knowledge Graph

Processa avaliações e cria o Knowledge Graph completo:

```bash
python scripts/knowledge_graph/process_reviews_to_graph.py
```

**Entrada**: `functional_correlation_results.csv`  
**O que faz**:
1. Filtra comentários genéricos sem informação útil
2. Seleciona avaliações negativas do aplicativo Santander
3. Extrai entidades de cada comentário usando GPT-4o (técnica de reflexão)
4. Cria nós no grafo: App, Version, Episode, Entities
5. Mapeia entidades para BusinessCapabilities
6. Cria relacionamentos entre entidades, versões e capacidades

**Modelo para Extração de Entidades**: Configurável via `OPENAI_MODEL` (padrão: `gpt-4o-mini`)

**Parâmetros opcionais**:

```bash
# Limitar número de avaliações processadas
python scripts/knowledge_graph/process_reviews_to_graph.py --limit 100

# Ajustar tamanho do lote de processamento
python scripts/knowledge_graph/process_reviews_to_graph.py --batch-size 5
```

## Scripts de Análise e Validação

### Validação de Modelos

Compara resultados dos modelos com ground truth humano:

```bash
python scripts/validate_model.py
```

### Análise de BusinessCapabilities

Analisa distribuição de Issues por BusinessCapability:

```bash
python scripts/analyze_business_capabilities.py
```

### Comparação de Modelos

Compara desempenho de diferentes modelos de análise de sentimentos:

```bash
python scripts/analysis/compare_models.py
```

## Categorias Funcionais

O sistema utiliza 15 categorias funcionais baseadas em análise de avaliações reais:

1. **PIX**: Transferências PIX, chave PIX, QR Code
2. **Login/Autenticação**: Acesso, senha, biometria, reconhecimento facial
3. **Performance**: Lentidão, travamentos, crashes, consumo de recursos
4. **Interface/Usabilidade**: Navegação, design, localização de funcionalidades
5. **Empréstimos/Crédito**: Limites, cartão de crédito, empréstimos
6. **Pagamentos/Boletos**: Pagamento de contas, boletos, DDA
7. **Saldo/Extrato**: Visualização de saldo, extrato, histórico
8. **Atendimento**: Suporte ao cliente, chat, SAC
9. **Cadastro/Conta**: Abertura de conta, atualização cadastral
10. **Investimentos**: Aplicações financeiras, poupança, rendimentos
11. **Segurança**: Fraudes, bloqueios indevidos, adesões não autorizadas
12. **Notificações**: Alertas, push notifications
13. **Questões geográficas**: Acesso no exterior, bloqueio geográfico
14. **Placas/Veículos**: IPVA, RENAVAM, multas, DETRAN
15. **Tarifas/Cobranças**: Tarifas, taxas, juros indevidos

## Estrutura do Knowledge Graph

O Knowledge Graph temporal armazena:

- **App**: Aplicativo (ex: Santander)
- **Version**: Versões do aplicativo mencionadas nas avaliações
- **Episode**: Avaliações individuais (comentários)
- **Issue**: Problemas técnicos ou funcionais extraídos
- **BusinessCapability**: Capacidades de negócio (15 categorias)
- **Relacionamentos**:
  - `BELONGS_TO`: Issue → BusinessCapability
  - `REPORTS`: Episode → Issue
  - `OCCURS_IN`: Issue → Version
  - `HAS_VERSION`: App → Version

## Métricas de Desempenho

### Análise de Polarização (BERTweet)

- **Acurácia**: 96.17%
- **Precisão**: 98.17%
- **Recall**: 96.17%
- **F1-Score**: 96.92%
- **ROC AUC**: 98.97%

Validação realizada com 366 avaliações classificadas manualmente.

### Categorização Funcional (GPT-4o)

- **Acurácia no Mapeamento Entidade → BusinessCapability**: 63.6%
- Suporta múltiplas categorias por avaliação
- Processamento incremental (reutiliza resultados anteriores)

## Troubleshooting

### Erro: "OPENAI_API_KEY não encontrada"

Configure a variável de ambiente ou crie arquivo `.env` com `OPENAI_API_KEY=sua_chave`.

### Erro: "Senha do Neo4j não fornecida"

Configure `NEO4J_PASSWORD` no arquivo `.env` ou como variável de ambiente.

### Erro: "Modelo não encontrado" (BERTweet)

O modelo será baixado automaticamente na primeira execução. Certifique-se de ter conexão com internet e espaço em disco (~500MB).

### Processamento muito lento

- Para categorização funcional: Ajuste `LIMIT_REVIEWS` em `functional_correlation.py` para testar com menos dados
- Para Knowledge Graph: Use `--limit` para processar apenas um subconjunto inicial

### CSV com encoding incorreto

Os scripts detectam automaticamente separadores (`;` ou `,`) e lidam com encoding UTF-8. Se houver problemas, verifique se o arquivo está salvo em UTF-8.

## Próximos Passos

1. **Coleta Automatizada**: Configurar coleta periódica de avaliações
2. **Dashboard**: Criar interface visual para análise do Knowledge Graph
3. **Alertas**: Implementar alertas para categorias críticas
4. **Integração**: Conectar com ferramentas de gestão de backlog (Jira, Azure DevOps)

## Contato e Suporte

Para dúvidas ou problemas, consulte a documentação técnica em `Documentos/` ou entre em contato com a equipe de desenvolvimento.
