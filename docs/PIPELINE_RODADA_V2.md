# Pipeline — nova rodada (v2) sem sobrescrever a v1

A **v1** corresponde aos ficheiros na raiz (`sentiment_results.csv`, métricas já usadas no TCC). A **v2** grava em `data/collections/v2/`.

## 0. Validar estatísticas de um CSV existente

```powershell
cd c:\codigos\app_review
python scripts/validate_collection_stats.py sentiment_results.csv
```

Mostra datas mín/máx, quantidade e extrapolações lineares para 7 e 30 dias.

## 1. Coleta (ex.: janela de 7 dias)

```powershell
python scripts/collect_reviews.py --days 7 --run v2
```

Saída: `data/collections/v2/app_review_dataset.csv`

- `--days N` define a janela deslizante (em relação ao momento em que o script roda).
- Sem `--run`, o padrão continua sendo `app_review_dataset.csv` na raiz (**sobrescreve** a coleta anterior da raiz — use só se for intencional).

Variável de ambiente opcional: `DAYS_WINDOW` (usada se não passar `--days`).

## 2. Análise de sentimento

```powershell
python scripts/sentiment_analysis.py --input data/collections/v2/app_review_dataset.csv --output data/collections/v2/sentiment_results.csv
```

## 3. Knowledge Graph (Neo4j) — negativos + tag de rodada

As **BusinessCapability** continuam um único catálogo (`MERGE` por id). Cada nova carga cria **Episode**, **Version** e ligações a entidades; o campo **`Episode.ingestion_run`** identifica a rodada (ex.: `v2`) para filtrar métricas SNA sem duplicar capacidades.

**Carga dos negativos a partir do sentimento v2:**

```powershell
cd c:\codigos\app_review
python scripts/knowledge_graph/process_negative_reviews.py `
  --input data/collections/v2/sentiment_results.csv `
  --ingestion-run v2
```

- Omitir `--ingestion-run` grava episódio **sem** tag (equivalente a cargas antigas; no SNA use `--ingestion-run v1` para incluir `NULL` e `v1`).
- CSV temporário: `negative_reviews_temp_v2.csv` (por rodada, evita colisão).

**Métricas SNA só na v2, só legado ou em tudo:**

```powershell
python scripts/knowledge_graph/calculate_sna_metrics.py --ingestion-run v2 --output-report reports/v2/sna_metrics_report.txt
python scripts/knowledge_graph/calculate_sna_metrics.py --ingestion-run v1 --output-report reports/sna_v1_only.txt
python scripts/knowledge_graph/calculate_sna_metrics.py --ingestion-run all --output-report reports/sna_all.txt
```

- **`v1`:** episódios com `ingestion_run` nulo **ou** `v1` (cargas antigas antes da propriedade).
- **`all`:** comportamento anterior do script (sem filtrar por episódio).

**Opcional — marcar episódios antigos como v1 no Neo4j** (uma vez, se quiser consultas uniformes):

```cypher
MATCH (ep:Episode) WHERE ep.ingestion_run IS NULL SET ep.ingestion_run = 'v1';
```

Repita o mesmo princípio para **GPT** e relatórios: entradas/saídas sob `data/collections/v2/` e `reports/v2/`, sem apagar os da raiz.

## 4. O que documentar no TCC

- Para a **v1**: use os números validados no CSV da raiz (período **5 a 18/01/2026**, **2.451** avaliações; média diária e extrapolações vêm do `validate_collection_stats.py`).
- Para a **v2**: depois de rodar, execute de novo o `validate_collection_stats.py` no novo `sentiment_results.csv` e atualize apenas a secção da “nova rodada” ou anexo.
