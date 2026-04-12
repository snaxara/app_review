# Coletas por rodada (`data/collections/`)

## v1 (resultados já usados no TCC)

Arquivos na **raiz** do projeto (`sentiment_results.csv`, etc.): coleta **jan/2026** (2.451 avaliações, datas 5–18/01/2026 no arquivo de sentimento). **Não sobrescrever** se quiser preservar essa versão.

## v2 — segunda rodada (15 dias)

- **Comando:** `python scripts/collect_reviews.py --days 15 --run v2`
- **Saída:** `v2/app_review_dataset.csv`
- **Última execução (ambiente local):** 2.410 registros após limpeza; datas no arquivo entre **2026-03-22** e **2026-04-04** (conferir no Word/API se alguma data futura for artefato da loja).
- **Sentimento (BERTweet),** saída `v2/sentiment_results.csv`: positivo 43,24%, negativo 47,84%, neutro 8,92%; nota média ~3,29 estrelas.
- **Grafo:** `python scripts/knowledge_graph/process_negative_reviews.py --input data/collections/v2/sentiment_results.csv --ingestion-run v2` (marca `Episode.ingestion_run` para filtrar SNA). Métricas: `calculate_sna_metrics.py --ingestion-run v2|v1|all`. Ver `docs/PIPELINE_RODADA_V2.md`.

Ver `docs/PIPELINE_RODADA_V2.md`.
