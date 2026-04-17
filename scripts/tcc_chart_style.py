"""Estilo de figuras do TCC: fundo branco, eixos 1,5 pt e paleta pastel discreta."""

from __future__ import annotations

import matplotlib as mpl
import matplotlib.pyplot as plt

RC_ESALQ = {
    "figure.facecolor": "white",
    "axes.facecolor": "white",
    "savefig.facecolor": "white",
    "font.size": 11,
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
    "text.color": "black",
}

# Mantemos os nomes por compatibilidade com scripts existentes,
# mas agora aplicando tons pastel suaves (não chamativos).
CINZA_CLARO = "#E8CFAF"   # bege pastel
CINZA_MEDIO = "#BFD8B8"   # verde sálvia pastel
CINZA_ESCURO = "#9BB7D4"  # azul pastel


def aplicar_eixos_principais(ax, linewidth: float = 1.5) -> None:
    ax.grid(False)
    ax.set_axisbelow(False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_visible(True)
        ax.spines[s].set_color("black")
        ax.spines[s].set_linewidth(linewidth)


def painel_letra(ax, letra: str) -> None:
    ax.text(
        0.02,
        0.98,
        letra,
        transform=ax.transAxes,
        fontsize=12,
        fontweight="normal",
        color="black",
        ha="left",
        va="top",
    )


def contexto():
    return plt.rc_context(RC_ESALQ)


def formatador_eixo_percent(ax, axis="y"):
    fmt = mpl.ticker.FuncFormatter(lambda v, _: f"{v*100:.0f}")
    if axis == "y":
        ax.yaxis.set_major_formatter(fmt)
    else:
        ax.xaxis.set_major_formatter(fmt)
