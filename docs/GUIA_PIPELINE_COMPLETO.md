# Guia Completo do Pipeline - Processamento de Reviews

Este documento descreve a sequência completa de comandos para processar comentários da Play Store até o Knowledge Graph.

---

## 1. COLETA DE DADOS

### Comando:
```bash
python scripts/collect_reviews.py
```

Nova rodada sem sobrescrever a raiz (ex.: janela 7 dias → pasta `v2`):

```bash
python scripts/collect_reviews.py --days 7 --run v2
```

Ver também `docs/PIPELINE_RODADA_V2.md`.

### Funcionalidade:
- **O que faz**: Coleta avaliações do aplicativo **Caixa** (`br.com.gabba.Caixa`) na Google Play Store
- **Período**: Janela deslizante em dias (padrão **15**; altere com `--days` ou `DAYS_WINDOW`)
- **Saída**: `app_review_dataset.csv` na raiz, ou `data/collections/<run>/app_review_dataset.csv` com `--run`, com colunas:
  - `reviewId`: ID único da avaliação
  - `content`: Texto do comentário
  - `date`: Data da avaliação
  - `version`: Versão do app mencionada
  - `app_name`: Nome do aplicativo (Caixa)
  - `score`: Nota de 1 a 5 estrelas

### Observações:
- Usa paginação para coletar todas as avaliações do período
- Gera `reviewId` único baseado em hash se não existir
- Salva em formato CSV com separador `;`

---

## 2. ANÁLISE DE SENTIMENTO

### Comando:
```bash
python scripts/sentiment_analysis.py
```

### Funcionalidade:
- **O que faz**: Classifica a polaridade (positivo/negativo/neutro) de cada comentário
- **Modelo**: `cardiffnlp/twitter-xlm-roberta-base-sentiment` (multilíngue)
- **Entrada**: `app_review_dataset.csv`
- **Saída**: `sentiment_results.csv` com colunas adicionais:
  - `sentiment_label`: "positive", "negative" ou "neutral"
  - `sentiment_score`: Score de confiança (0.0 a 1.0)

### Observações:
- Processa todos os comentários coletados
- Usa modelo pré-treinado (não requer treinamento)
- Detecta automaticamente separador do CSV (`,` ou `;`)

---

## 3. INICIALIZAÇÃO DO GRAFO

### Comando:
```bash
python scripts/knowledge_graph/init_graph.py
```

**OU para limpar dados existentes:**
```bash
python scripts/knowledge_graph/init_graph.py --reset
```

### Funcionalidade:
- **O que faz**: Inicializa o Neo4j com estrutura do Knowledge Graph Temporal
- **Cria**:
  - Índices para otimização de queries
  - 16 nós `BusinessCapability` (hierarquia de funcionalidades):
    - Nível 1: Autenticação e Acesso, Performance e Estabilidade, Interface e UX, Segurança
    - Nível 2: PIX, Empréstimos, Pagamentos, Saldo/Extrato, Atendimento, etc.
    - Nível 3: Serviços de Veículos, Outras Funcionalidades
- **Estrutura**: 3 subgrafos (Episodic, Semantic, Community) + modelo bi-temporal

### Observações:
- Execute apenas uma vez (ou quando precisar resetar)
- Requer conexão com Neo4j configurada
- `--reset` remove TODOS os dados antes de criar estrutura

---

## 4. PROCESSAMENTO NO GRAFO

### Comando Básico:
```bash
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --limit 10
```

### Comando com Offset (Processamento Incremental):
```bash
# Primeiros 10 comentários
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --limit 10

# Próximos 10 comentários (11-20)
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --offset 10 --limit 10

# Próximos 20 comentários (21-40)
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --offset 20 --limit 20
```

### Parâmetros Disponíveis:
- `--input`: Arquivo CSV com sentimentos (padrão: `sentiment_results.csv`)
- `--limit`: Quantidade de comentários para processar (padrão: todos)
- `--offset`: Índice inicial para começar (padrão: 0)
- `--batch-size`: Tamanho do lote para processamento (padrão: 10)
- `--keep-temp`: Mantém arquivo temporário após processamento

### Funcionalidade:
- **O que faz**: Processa comentários negativos e cria Knowledge Graph
- **Etapas automáticas**:
  1. **Triagem**: Remove comentários genéricos ("péssimo", "horrível", etc.)
  2. **Extração de Entidades**: Usa LLM (GPT-4o) para extrair:
     - Features (funcionalidades): PIX, Login, Transferências, etc.
     - Issues (problemas): Lentidão, Travamento, Erro, etc.
     - Versões mencionadas
  3. **Reflexão**: Segunda passada LLM para recuperar entidades perdidas (~5-10%)
  4. **Criação de Episódios**: Preserva conteúdo original do comentário
  5. **Linking**: Conecta entidades a BusinessCapability e versões
  6. **Modelo Temporal**: Adiciona timestamps (t_valid, t_invalid, t_created, t_expired)

### Saída no Grafo:
- **Episódios**: Nós com conteúdo original dos comentários
- **Entidades**: Features, Issues, Versões, App
- **Relacionamentos**:
  - `CONTAINS_ENTITY`: Episódio → Entidade
  - `RELATES_TO_CAPABILITY`: Entidade → BusinessCapability
  - `RELATED_TO_VERSION`: Issue → Versão (com contagem)
  - `BELONGS_TO`: Versão → App
  - `HAS_VERSION`: Episódio → Versão

### Observações:
- Processa apenas comentários **negativos** automaticamente
- Evita reprocessar: se episódio já existe, pula automaticamente
- Mostra estatísticas finais: episódios, entidades, relacionamentos criados

---

## 5. SCRIPTS AUXILIARES

### 5.1. Corrigir Issues sem BusinessCapability

### Comando:
```bash
python scripts/knowledge_graph/fix_missing_capabilities.py
```

### Funcionalidade:
- **O que faz**: Linka issues que não foram conectadas a nenhuma BusinessCapability
- **Quando usar**: Após processamento inicial, se houver issues órfãs
- **Método**: Usa mapeamento por palavras-chave e regras de fallback

---

### 5.2. Visualizar Grafo no Neo4j Browser

### Arquivo:
`scripts/knowledge_graph/queries_visualizacao.cypher`

### Funcionalidade:
- **O que faz**: Contém queries Cypher prontas para visualização
- **Queries disponíveis**:
  1. Visualização completa do grafo
  2. Versões com mais problemas (alertas)
  3. Issues por BusinessCapability
  4. Issues sem BusinessCapability (para correção)
  5. Contagem de episódios por versão

### Como usar:
1. Abra Neo4j Browser
2. Copie e cole as queries do arquivo `.cypher`
3. Execute para visualizar diferentes perspectivas do grafo

---

## FLUXO COMPLETO RECOMENDADO

```bash
# 1. Coletar dados (15 dias)
python scripts/collect_reviews.py

# 2. Classificar sentimento
python scripts/sentiment_analysis.py

# 3. Inicializar grafo (apenas primeira vez ou para resetar)
python scripts/knowledge_graph/init_graph.py --reset

# 4. Processar comentários incrementalmente
# Primeira carga (10 comentários)
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --limit 10

# Segunda carga (próximos 10)
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --offset 10 --limit 10

# Continuar conforme necessário...
python scripts/knowledge_graph/process_negative_reviews.py --input sentiment_results.csv --offset 20 --limit 20

# 5. (Opcional) Corrigir issues sem capability
python scripts/knowledge_graph/fix_missing_capabilities.py

# 6. Visualizar no Neo4j Browser usando queries_visualizacao.cypher
```

---

## ARQUIVOS GERADOS

| Arquivo | Descrição | Quando é criado |
|---------|-----------|-----------------|
| `app_review_dataset.csv` | Comentários coletados da Play Store | Após `collect_reviews.py` |
| `sentiment_results.csv` | Comentários com classificação de sentimento | Após `sentiment_analysis.py` |
| `negative_reviews_temp.csv` | Arquivo temporário com comentários filtrados | Durante `process_negative_reviews.py` (removido ao final) |

---

## CONFIGURAÇÕES IMPORTANTES

### Variáveis de Ambiente (.env):
- `NEO4J_URI`: URI de conexão Neo4j (ex: `bolt://localhost:7687`)
- `NEO4J_USER`: Usuário Neo4j
- `NEO4J_PASSWORD`: Senha Neo4j
- `OPENAI_API_KEY`: Chave da API OpenAI (para extração de entidades)

### Configurações em Código:
- `DAYS_WINDOW` (collect_reviews.py): Janela de dias para coleta (padrão: 15)
- `BATCH_SIZE` (collect_reviews.py): Tamanho do lote de coleta (padrão: 200)
- `MODEL_NAME` (sentiment_analysis.py): Modelo de sentimento (padrão: cardiffnlp/twitter-xlm-roberta-base-sentiment)

---

## DICAS E TROUBLESHOOTING

1. **Processamento incremental**: Use `--offset` para continuar de onde parou
2. **Evitar reprocessamento**: O sistema detecta automaticamente episódios já processados
3. **Triagem automática**: Comentários genéricos são filtrados antes do processamento (economiza custos de API)
4. **Estatísticas**: Sempre verifique as estatísticas finais para validar processamento
5. **Neo4j Browser**: Use as queries de visualização para explorar o grafo criado
