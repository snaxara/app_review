"""
Script para gerar gráficos comparativos de modelos
1. Comparação de modelos de sentimentos (DistilBERT vs BERTweet)
2. Comparação de modelos GPT para categorização (4 modelos)
"""

import json
import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[1]
_CONFUSION_JSON = _REPO_ROOT / "data" / "confusion_matrices_sentiment.json"

# Configuração de estilo
plt.style.use("default")
plt.rcParams['figure.figsize'] = (16, 6)
plt.rcParams['font.size'] = 10
plt.rcParams['font.family'] = 'DejaVu Sans'

# Cores para gráficos (pastel discreto)
CORES = {
    'distilbert': '#BFD8B8',  # Verde sálvia
    'bertweet': '#9BB7D4',    # Azul pastel
    'gpt4o': '#9BB7D4',
    'gpt52': '#C9B6D8',       # Lilás pastel
    'gptoss': '#E8CFAF',      # Bege pastel
    'gptmini': '#D9A5A5',     # Rosa queimado suave
}

def criar_diretorio_imagens():
    """Cria diretório para armazenar imagens"""
    dir_imagens = Path('Documentos/imagens_tcc')
    dir_imagens.mkdir(exist_ok=True)
    return dir_imagens

def _curva_roc_esquematica(auc: float, n: int = 100) -> tuple[np.ndarray, np.ndarray]:
    """Curva ROC suave só para ilustração (AUC alvo aproximado); sem probabilidades por classe."""
    auc = float(np.clip(auc, 0.5, 1.0))
    fpr = np.linspace(0, 1, n)
    beta = (2 * auc - 1) / (2 * (1 - auc) + 1e-9)
    beta = float(np.clip(beta, 0.05, 15))
    tpr = fpr ** (1 / beta)
    return fpr, tpr


def grafico_comparacao_sentimentos(output_dir):
    """
    Três painéis (A/B/C), normas Tabela 8: sem grade, sem preenchimento de fundo,
    eixos pretos 1,5 pt, Arial 11, barras em paleta pastel discreta.
    Métricas alinhadas às matrizes n=1000 em data/confusion_matrices_sentiment.json.
    """
    _, _, meta = _carregar_matrizes_confusao()
    md = meta["distilbert"]["chart_metrics"]
    mb = meta["bertweet"]["chart_metrics"]

    cinza_claro = "#BFD8B8"
    cinza_escuro = "#9BB7D4"

    rc = {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.size": 11,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "text.color": "black",
    }
    with plt.rc_context(rc):
        fig, axes = plt.subplots(1, 3, figsize=(16, 5.2), facecolor="white")

        # --- A: ROC (esquemático; AUC coerente com métricas do JSON) ---
        ax1 = axes[0]
        auc_d = md["roc_auc_weighted_ovr_pct"] / 100.0
        auc_b = mb["roc_auc_weighted_ovr_pct"] / 100.0
        fpr_d, tpr_d = _curva_roc_esquematica(auc_d)
        fpr_b, tpr_b = _curva_roc_esquematica(auc_b)
        ax1.plot(
            fpr_d,
            tpr_d,
            color=cinza_escuro,
            linewidth=1.5,
            label=f"DistilBERT Multilíngue (AUC = {auc_d:.3f})",
        )
        ax1.plot(
            fpr_b,
            tpr_b,
            color="#7F95AD",
            linewidth=1.5,
            label=f"BERTweet (Twitter XLM-RoBERTa) (AUC = {auc_b:.3f})",
        )
        ax1.plot([0, 1], [0, 1], linestyle="--", color="#B8B8B8", linewidth=1.2, label="Classificador aleatório")
        ax1.set_xlabel("Taxa de falsos positivos", fontsize=11, fontweight="normal", labelpad=6)
        ax1.set_ylabel("Taxa de verdadeiros positivos", fontsize=11, fontweight="normal", labelpad=6)
        ax1.set_xlim(0, 1)
        ax1.set_ylim(0, 1)
        _esalq_axes_style(ax1, linewidth=1.5)
        _painel_letra_manual(ax1, "A")
        ax1.legend(loc="lower right", fontsize=9, frameon=True, edgecolor="0.5")

        # --- B: métricas ---
        ax2 = axes[1]
        metricas = ["ROC AUC", "Precisão", "Recall", "F1-Score"]
        distil_values = [
            md["roc_auc_weighted_ovr_pct"] / 100.0,
            md["precision_weighted_pct"] / 100.0,
            md["recall_weighted_pct"] / 100.0,
            md["f1_weighted_pct"] / 100.0,
        ]
        bertweet_values = [
            mb["roc_auc_weighted_ovr_pct"] / 100.0,
            mb["precision_weighted_pct"] / 100.0,
            mb["recall_weighted_pct"] / 100.0,
            mb["f1_weighted_pct"] / 100.0,
        ]
        x = np.arange(len(metricas))
        width = 0.35
        bars1 = ax2.bar(
            x - width / 2,
            distil_values,
            width,
            label="DistilBERT Multilíngue",
            color=cinza_claro,
            edgecolor="black",
            linewidth=0.6,
        )
        bars2 = ax2.bar(
            x + width / 2,
            bertweet_values,
            width,
            label="BERTweet (Twitter XLM-RoBERTa)",
            color=cinza_escuro,
            edgecolor="black",
            linewidth=0.6,
        )
        max_height = max(max(distil_values), max(bertweet_values))
        ax2.set_ylabel("Valor (%)", fontsize=11, fontweight="normal", labelpad=6)
        ax2.set_xticks(x)
        ax2.set_xticklabels(metricas, fontsize=11, fontweight="normal")
        ax2.set_ylim(0, min(1.0, max_height * 1.18))
        ax2.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v*100:.0f}"))
        _esalq_axes_style(ax2, linewidth=1.5)
        _painel_letra_manual(ax2, "B")
        ax2.legend(fontsize=8, loc="upper left", frameon=True, edgecolor="0.5")
        for bars in (bars1, bars2):
            for bar in bars:
                h = bar.get_height()
                ax2.text(
                    bar.get_x() + bar.get_width() / 2.0,
                    h + max_height * 0.02,
                    f"{h*100:.1f}",
                    ha="center",
                    va="bottom",
                    fontsize=9,
                    fontweight="normal",
                )

        # --- C: acurácia ---
        ax3 = axes[2]
        nomes = ["DistilBERT\nMultilíngue", "BERTweet\n(Twitter XLM-RoBERTa)"]
        accuracies = [md["accuracy_pct"] / 100.0, mb["accuracy_pct"] / 100.0]
        bars = ax3.bar(
            nomes,
            accuracies,
            color=[cinza_claro, cinza_escuro],
            edgecolor="black",
            linewidth=0.6,
        )
        max_acc = max(accuracies)
        ax3.set_ylabel("Acurácia (%)", fontsize=11, fontweight="normal", labelpad=6)
        ax3.set_ylim(0, max_acc * 1.2)
        ax3.yaxis.set_major_formatter(mpl.ticker.FuncFormatter(lambda v, _: f"{v*100:.0f}"))
        _esalq_axes_style(ax3, linewidth=1.5)
        _painel_letra_manual(ax3, "C")
        for bar, acc in zip(bars, accuracies):
            h = bar.get_height()
            ax3.text(
                bar.get_x() + bar.get_width() / 2.0,
                h + max_acc * 0.02,
                f"{acc*100:.2f}",
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="normal",
            )

        plt.tight_layout(pad=1.8)
        plt.savefig(
            output_dir / "comparacao_modelos_sentimentos.png",
            dpi=300,
            bbox_inches="tight",
            pad_inches=0.12,
            facecolor="white",
            edgecolor="none",
        )
        plt.close()

    print(f"Grafico salvo: {output_dir / 'comparacao_modelos_sentimentos.png'}")

def _annotate_confusion_matrix(ax, cm, cmap, vmax):
    """Números nas células com cor de texto contrastante (legibilidade em tons escuros)."""
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            val = int(cm[i, j])
            t = (val / vmax) if vmax > 0 else 0.0
            rgba = cmap(np.clip(t, 0, 1))
            luminance = 0.299 * rgba[0] + 0.587 * rgba[1] + 0.114 * rgba[2]
            color = "#ffffff" if luminance < 0.52 else "#111111"
            ax.text(
                j, i, str(val),
                ha="center", va="center",
                color=color, fontsize=12, fontweight="normal",
            )


def _esalq_axes_style(ax, linewidth=1.5):
    """Tabela 8: eixos principais em preto 1,5 pt; sem grade; sem borda extra."""
    ax.grid(False)
    ax.set_axisbelow(False)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    for s in ("bottom", "left"):
        ax.spines[s].set_visible(True)
        ax.spines[s].set_color("black")
        ax.spines[s].set_linewidth(linewidth)


def _painel_letra_manual(ax, letra: str):
    """Item figuras multipainel: letra maiúscula, canto superior esquerdo, sem parênteses nem ponto."""
    ax.text(
        0.02, 0.98, letra,
        transform=ax.transAxes,
        fontsize=12,
        fontweight="normal",
        color="black",
        ha="left",
        va="top",
    )


def _carregar_matrizes_confusao():
    """Lê data/confusion_matrices_sentiment.json (gerado por build_confusion_matrices_gt1000.py)."""
    if not _CONFUSION_JSON.is_file():
        raise FileNotFoundError(
            f"Arquivo ausente: {_CONFUSION_JSON}. Rode: python scripts/build_confusion_matrices_gt1000.py"
        )
    data = json.loads(_CONFUSION_JSON.read_text(encoding="utf-8"))
    distil = np.array(data["distilbert"]["matrix"], dtype=int)
    bert = np.array(data["bertweet"]["matrix"], dtype=int)
    return distil, bert, data


def grafico_matriz_confusao_sentimentos(output_dir):
    """
    Matrizes de confusão n=1000 (ground truth): paleta pastel suave,
    Arial 11 preto, sem título interno; painéis A e B conforme manual (sem parênteses).
    """
    distil_matrix, bertweet_matrix, meta = _carregar_matrizes_confusao()
    labels = ["Negativo", "Neutro", "Positivo"]
    vmax = float(max(distil_matrix.max(), bertweet_matrix.max()))
    cmap = mpl.colors.LinearSegmentedColormap.from_list(
        "pastel_blues",
        ["#FFFFFF", "#DCE8F6", "#9BB7D4"],
    )
    cmap.set_bad(color="white")

    rc = {
        "figure.facecolor": "white",
        "axes.facecolor": "white",
        "savefig.facecolor": "white",
        "font.size": 11,
        "font.family": "sans-serif",
        "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans"],
        "axes.edgecolor": "black",
        "axes.linewidth": 1.5,
        "text.color": "black",
    }
    with plt.rc_context(rc):
        fig, axes = plt.subplots(1, 2, figsize=(11.5, 5.0), facecolor="white")
        for ax, cm, letter in (
            (axes[0], distil_matrix, "A"),
            (axes[1], bertweet_matrix, "B"),
        ):
            im = ax.imshow(cm, cmap=cmap, vmin=0, vmax=vmax, interpolation="nearest", aspect="equal")
            _annotate_confusion_matrix(ax, cm, cmap, vmax)
            ax.set_xticks(np.arange(cm.shape[1]))
            ax.set_yticks(np.arange(cm.shape[0]))
            ax.set_xticklabels(labels, rotation=35, ha="right", fontsize=11, fontweight="normal")
            ax.set_yticklabels(labels, fontsize=11, fontweight="normal")
            ax.set_xlabel("Classe Predita", fontsize=11, labelpad=8, fontweight="normal")
            ax.set_ylabel("Classe Verdadeira", fontsize=11, labelpad=8, fontweight="normal")
            _esalq_axes_style(ax, linewidth=1.5)
            _painel_letra_manual(ax, letter)
            cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
            cbar.set_label("Número de Comentários", fontsize=11, fontweight="normal")
            cbar.ax.tick_params(labelsize=10)
        plt.tight_layout()
        out = output_dir / "matriz_confusao_sentimentos.png"
        plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")
        plt.close()

    print(f"Grafico salvo: {output_dir / 'matriz_confusao_sentimentos.png'}")
    print(
        f"  (matrizes n={meta.get('n_samples')}, "
        f"acurácias JSON DistilBERT={meta['distilbert']['accuracy']}, BERTweet={meta['bertweet']['accuracy']})"
    )

def grafico_comparacao_gpt_models(output_dir):
    """Duas figuras separadas (normas TCC): acurácia e distribuição em paleta pastel, sem grade."""
    try:
        from scripts.tcc_chart_style import (
            CINZA_CLARO,
            CINZA_ESCURO,
            CINZA_MEDIO,
            aplicar_eixos_principais,
            contexto,
            formatador_eixo_percent,
        )
    except ImportError:
        from tcc_chart_style import (
            CINZA_CLARO,
            CINZA_ESCURO,
            CINZA_MEDIO,
            aplicar_eixos_principais,
            contexto,
            formatador_eixo_percent,
        )

    modelos_gpt = {
        "GPT-4o-2024-08-06": {
            "accuracy": 63.6,
            "corretos": 14,
            "incorretos": 0,
            "nao_encontrados": 8,
        },
        "GPT-5.2-2025-12-11": {
            "accuracy": 63.6,
            "corretos": 14,
            "incorretos": 0,
            "nao_encontrados": 8,
        },
        "GPT-OSS-20B": {
            "accuracy": 59.1,
            "corretos": 13,
            "incorretos": 0,
            "nao_encontrados": 9,
        },
        "GPT-4o-mini": {
            "accuracy": 54.5,
            "corretos": 12,
            "incorretos": 0,
            "nao_encontrados": 10,
        },
    }
    modelos_nomes = list(modelos_gpt.keys())
    cinzas = [CINZA_ESCURO, CINZA_MEDIO, CINZA_CLARO, "#6E6E6E"]

    with contexto():
        # Figura única: acurácia
        fig1, ax1 = plt.subplots(figsize=(10, 4.8), facecolor="white")
        accuracies = [m["accuracy"] / 100 for m in modelos_gpt.values()]
        bars = ax1.bar(
            range(len(modelos_nomes)),
            accuracies,
            color=cinzas[: len(modelos_nomes)],
            edgecolor="black",
            linewidth=0.6,
        )
        ax1.set_xticks(range(len(modelos_nomes)))
        ax1.set_xticklabels(modelos_nomes, rotation=18, ha="right", fontsize=9)
        ax1.set_ylabel("Acurácia (%)", fontsize=11, fontweight="normal", labelpad=6)
        max_acc = max(accuracies)
        ax1.set_ylim(0, max_acc * 1.22)
        formatador_eixo_percent(ax1, "y")
        aplicar_eixos_principais(ax1)
        for bar, acc in zip(bars, accuracies):
            h = bar.get_height()
            ax1.text(
                bar.get_x() + bar.get_width() / 2,
                h + max_acc * 0.02,
                f"{acc*100:.1f}",
                ha="center",
                va="bottom",
                fontsize=10,
                fontweight="normal",
            )
        plt.tight_layout()
        p1 = output_dir / "figura3A_gpt_accuracy.png"
        fig1.savefig(p1, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")
        plt.close(fig1)

        # Figura única: distribuição
        fig2, ax2 = plt.subplots(figsize=(11, 5.0), facecolor="white")
        x = np.arange(len(modelos_nomes))
        width = 0.24
        corretos = [m["corretos"] for m in modelos_gpt.values()]
        incorretos = [m["incorretos"] for m in modelos_gpt.values()]
        nao_encontrados = [m["nao_encontrados"] for m in modelos_gpt.values()]
        ax2.bar(
            x - width,
            corretos,
            width,
            label="Corretos",
            color=CINZA_ESCURO,
            edgecolor="black",
            linewidth=0.5,
        )
        ax2.bar(
            x,
            incorretos,
            width,
            label="Incorretos",
            color=CINZA_MEDIO,
            edgecolor="black",
            linewidth=0.5,
        )
        ax2.bar(
            x + width,
            nao_encontrados,
            width,
            label="Não encontrados",
            color=CINZA_CLARO,
            edgecolor="black",
            linewidth=0.5,
        )
        ax2.set_xticks(x)
        ax2.set_xticklabels(modelos_nomes, rotation=18, ha="right", fontsize=9)
        ax2.set_ylabel("Quantidade (n)", fontsize=11, fontweight="normal", labelpad=6)
        max_value = max(max(corretos), max(incorretos), max(nao_encontrados))
        ax2.set_ylim(0, max_value * 1.35)
        aplicar_eixos_principais(ax2)
        ax2.legend(fontsize=9, loc="upper left", frameon=True, edgecolor="0.5")
        for bars in ax2.containers:
            for bar in bars:
                h = bar.get_height()
                if h > 0:
                    ax2.text(
                        bar.get_x() + bar.get_width() / 2,
                        h + 0.35,
                        f"{int(h)}",
                        ha="center",
                        va="bottom",
                        fontsize=8,
                        fontweight="normal",
                    )
        plt.tight_layout()
        p2 = output_dir / "figura3B_gpt_distribuicao.png"
        fig2.savefig(p2, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")
        plt.close(fig2)

    # Legado: uma figura combinada opcional
    print(f"Graficos salvos: {p1} e {p2}")

def gerar_todos_graficos():
    """Gera todos os gráficos comparativos"""
    print("Gerando graficos comparativos de modelos...")
    
    output_dir = criar_diretorio_imagens()
    
    print("\n1. Gerando comparacao de modelos de sentimentos...")
    grafico_comparacao_sentimentos(output_dir)
    
    print("\n2. Gerando matrizes de confusao de sentimentos...")
    grafico_matriz_confusao_sentimentos(output_dir)
    
    print("\n3. Gerando comparacao de modelos GPT...")
    grafico_comparacao_gpt_models(output_dir)
    
    print("\nTodos os graficos comparativos foram gerados com sucesso!")
    print(f"Arquivos salvos em: {output_dir}")

if __name__ == '__main__':
    gerar_todos_graficos()
