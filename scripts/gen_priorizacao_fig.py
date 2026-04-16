# -*- coding: utf-8 -*-
"""Gera Figura 12 a partir do relatório real backlog_priorizado.md (rodada piloto)."""
import re
from pathlib import Path

import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Arial", "DejaVu Sans", "Helvetica"]

root = Path(__file__).resolve().parents[1]
md_path = root / "Documentos" / "backlog_priorizado.md"
out = root / "Documentos" / "imagens_tcc" / "exemplo_documento_priorizacao_backlog.png"


def parse_resumo_table(text: str) -> list[list[str]]:
    lines = text.splitlines()
    rows_out: list[list[str]] = []
    in_table = False
    for line in lines:
        if line.strip().startswith("| Categoria |"):
            in_table = True
            continue
        if in_table:
            if not line.strip().startswith("|"):
                break
            if re.match(r"^\|[\s:-]+\|", line):
                continue
            cells = [c.strip() for c in line.strip().split("|")[1:-1]]
            if len(cells) >= 5:
                rows_out.append(cells[:5])
    return rows_out


def main() -> None:
    raw = md_path.read_text(encoding="utf-8")
    data = parse_resumo_table(raw)
    # Ordenar por quantidade (col1 int) e manter top 8 para caber na figura
    def qtd(row: list[str]) -> int:
        try:
            return int(row[1])
        except (IndexError, ValueError):
            return 0

    data_sorted = sorted(data, key=qtd, reverse=True)[:8]
    cols = ["Categoria", "Qtd.", "%", "Sev. média", "Prioridade"]
    rows = [[r[0], r[1], r[2], r[3], r[4]] for r in data_sorted]

    fig, ax = plt.subplots(figsize=(11, 3.8))
    ax.axis("off")
    ax.set_title(
        "Extrato do relatório de backlog priorizado (tabela-resumo por categoria)",
        fontsize=10,
        pad=12,
        loc="left",
        fontweight="normal",
    )
    table = ax.table(
        cellText=rows,
        colLabels=cols,
        loc="center",
        cellLoc="left",
        colColours=["#e8e8e8"] * len(cols),
    )
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.scale(1.05, 1.35)

    meta = re.search(r"Data:\s*(.+)", raw)
    total = re.search(r"Total de Avaliações:\s*(\d+)", raw)
    modelo = re.search(r"Modelo:\s*(.+)", raw)
    foot = "Fonte dos dados: arquivo backlog_priorizado.md"
    if meta:
        foot += f" ({meta.group(1).strip()})"
    if total and modelo:
        foot += f". Rodada piloto: {total.group(1)} avaliações negativas; {modelo.group(1).strip()}."
    fig.text(0.01, 0.02, foot, fontsize=7, style="italic", color="#333333")

    fig.tight_layout()
    out.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor="white")
    plt.close()
    print("Salvo:", out)


if __name__ == "__main__":
    main()
