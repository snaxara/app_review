"""
Resume estatísticas de um CSV de avaliações (data mínima/máxima, contagem, média diária).
Uso:
  python scripts/validate_collection_stats.py sentiment_results.csv
  python scripts/validate_collection_stats.py data/collections/v2/app_review_dataset.csv --date-col date
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd


def main() -> None:
    p = argparse.ArgumentParser(description="Valida período e volume de um CSV de avaliações.")
    p.add_argument("csv_path", type=Path)
    p.add_argument(
        "--date-col",
        default="date",
        help="Nome da coluna de data (padrão: date)",
    )
    args = p.parse_args()

    df = pd.read_csv(args.csv_path, sep=";", engine="python", on_bad_lines="skip")
    if args.date_col not in df.columns:
        raise SystemExit(f"Coluna '{args.date_col}' não encontrada. Colunas: {list(df.columns)}")

    d = pd.to_datetime(df[args.date_col], errors="coerce")
    valid = d.notna()
    n = int(valid.sum())
    if n == 0:
        raise SystemExit("Nenhuma data válida.")

    d = d[valid]
    dmin, dmax = d.min(), d.max()
    span_days = (dmax - dmin).total_seconds() / 86400.0

    print(f"Arquivo: {args.csv_path.resolve()}")
    print(f"Linhas com data válida: {n}")
    print(f"Data mínima: {dmin}")
    print(f"Data máxima: {dmax}")
    print(f"Amplitude (max - min): {span_days:.2f} dias")
    print(f"Média simples (n / amplitude): {n / max(span_days, 1e-9):.1f} avaliações/dia")
    print()
    print("Extrapolações lineares (indicativas):")
    print(f"  ~{int(round(n / max(span_days, 1e-9) * 7))} em 7 dias")
    print(f"  ~{int(round(n / max(span_days, 1e-9) * 30))} em 30 dias")


if __name__ == "__main__":
    main()
