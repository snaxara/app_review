"""
Script para gerar visualizações de métricas SNA (normas TCC: fundo branco, sem grade, paleta pastel discreta).
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

try:
    from scripts.tcc_chart_style import (
        CINZA_CLARO,
        CINZA_ESCURO,
        CINZA_MEDIO,
        aplicar_eixos_principais,
        contexto,
    )
except ImportError:
    from tcc_chart_style import (
        CINZA_CLARO,
        CINZA_ESCURO,
        CINZA_MEDIO,
        aplicar_eixos_principais,
        contexto,
    )


def criar_diretorio_imagens():
    dir_imagens = Path("Documentos/imagens_tcc")
    dir_imagens.mkdir(exist_ok=True)
    return dir_imagens


def grafico_degree_centrality(dados, output_dir):
    with open(dados, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    issues_degree = metrics.get("degree", {}).get("issues", [])
    capabilities_degree = metrics.get("degree", {}).get("capabilities", [])

    with contexto():
        fig, axes = plt.subplots(1, 2, figsize=(13, 6.5), facecolor="white")

        if issues_degree:
            top_issues = sorted(
                issues_degree, key=lambda x: x.get("DegreeCentrality", 0), reverse=True
            )[:15]
            issues_names = [i["Issue"] for i in top_issues]
            degrees = [i["DegreeCentrality"] for i in top_issues]
            axes[0].barh(
                range(len(issues_names)),
                degrees,
                color=CINZA_ESCURO,
                edgecolor="black",
                linewidth=0.5,
            )
            axes[0].set_yticks(range(len(issues_names)))
            axes[0].set_yticklabels(issues_names, fontsize=8)
            axes[0].set_xlabel("Degree centrality", fontsize=11, fontweight="normal", labelpad=6)
            axes[0].set_title("Issues (15 maiores graus)", fontsize=11, fontweight="normal", pad=10)
            aplicar_eixos_principais(axes[0])
            axes[0].invert_yaxis()
            for i, deg in enumerate(degrees):
                axes[0].text(
                    float(deg) + 0.04,
                    i,
                    f"{deg:g}",
                    va="center",
                    fontsize=8,
                    fontweight="normal",
                )

        if capabilities_degree:
            top_caps = sorted(
                capabilities_degree, key=lambda x: x.get("DegreeCentrality", 0), reverse=True
            )[:15]
            caps_names = [c["BusinessCapability"] for c in top_caps]
            degrees = [c["DegreeCentrality"] for c in top_caps]
            axes[1].barh(
                range(len(caps_names)),
                degrees,
                color=CINZA_MEDIO,
                edgecolor="black",
                linewidth=0.5,
            )
            axes[1].set_yticks(range(len(caps_names)))
            axes[1].set_yticklabels(caps_names, fontsize=8)
            axes[1].set_xlabel("Degree centrality", fontsize=11, fontweight="normal", labelpad=6)
            axes[1].set_title(
                "BusinessCapabilities (15 maiores graus)", fontsize=11, fontweight="normal", pad=10
            )
            aplicar_eixos_principais(axes[1])
            axes[1].invert_yaxis()
            for i, deg in enumerate(degrees):
                axes[1].text(
                    float(deg) + 0.15,
                    i,
                    f"{deg:g}",
                    va="center",
                    fontsize=8,
                    fontweight="normal",
                )

        plt.tight_layout()
        p = output_dir / "sna_degree_centrality.png"
        fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")
        plt.close(fig)

    print(f"Grafico salvo: {p}")


def grafico_metricas_combinadas(dados, output_dir):
    with open(dados, "r", encoding="utf-8") as f:
        metrics = json.load(f)

    density = metrics.get("density", {})

    with contexto():
        fig, axes = plt.subplots(2, 2, figsize=(12, 10), facecolor="white")

        ax1 = axes[0, 0]
        if density and density.get("total_links") is not None:
            total_links = density.get("total_links", 0)
            max_links = density.get("max_possible_links", 0)
            density_value = density.get("Density", 0)
            if max_links > 0:
                labels = ["Links existentes", "Links possíveis (não usados)"]
                values = [total_links, max_links - total_links]
                ax1.pie(
                    values,
                    labels=labels,
                    autopct="%1.1f%%",
                    colors=[CINZA_ESCURO, CINZA_CLARO],
                    startangle=90,
                    textprops={"fontsize": 9, "fontweight": "normal"},
                    wedgeprops={"edgecolor": "black", "linewidth": 0.6},
                )
                ax1.set_title(
                    f"Densidade da rede: {density_value:.4f}",
                    fontsize=11,
                    fontweight="normal",
                    pad=10,
                )
            else:
                ax1.text(0.5, 0.5, "Dados de densidade indisponíveis", ha="center", va="center")
                aplicar_eixos_principais(ax1)
        else:
            ax1.text(0.5, 0.5, "Dados de densidade indisponíveis", ha="center", va="center")
            aplicar_eixos_principais(ax1)

        ax2 = axes[0, 1]
        issues_degree = metrics.get("degree", {}).get("issues", [])
        if issues_degree:
            degrees = [i.get("DegreeCentrality", 0) for i in issues_degree]
            unique_degrees = sorted(set(degrees))
            bins = unique_degrees + [max(unique_degrees) + 1] if unique_degrees else [0, 1, 2]
            counts, _, patches = ax2.hist(
                degrees,
                bins=bins,
                color=CINZA_MEDIO,
                edgecolor="black",
                linewidth=0.6,
                align="left",
            )
            for count, patch in zip(counts, patches):
                if count > 0:
                    h = patch.get_height()
                    ax2.text(
                        patch.get_x() + patch.get_width() / 2.0,
                        h,
                        f"{int(count)}",
                        ha="center",
                        va="bottom",
                        fontsize=9,
                        fontweight="normal",
                    )
            ax2.set_xlabel("Degree centrality", fontsize=11, fontweight="normal", labelpad=6)
            ax2.set_ylabel("Frequência (n)", fontsize=11, fontweight="normal", labelpad=6)
            ax2.set_title(
                "Distribuição de degree centrality — Issues",
                fontsize=11,
                fontweight="normal",
                pad=10,
            )
            ax2.set_xticks(unique_degrees)
            aplicar_eixos_principais(ax2)

        ax3 = axes[1, 0]
        clustering = metrics.get("clustering", {}).get("issues", [])
        if clustering:
            top_clustering = sorted(
                clustering, key=lambda x: x.get("ClusteringCoefficient", 0), reverse=True
            )[:10]
            issues_names = [c["Issue"] for c in top_clustering]
            coeffs = [c.get("ClusteringCoefficient", 0) for c in top_clustering]
            ax3.barh(
                range(len(issues_names)),
                coeffs,
                color=CINZA_ESCURO,
                edgecolor="black",
                linewidth=0.5,
            )
            ax3.set_yticks(range(len(issues_names)))
            ax3.set_yticklabels(issues_names, fontsize=8)
            ax3.set_xlabel("Clustering coefficient", fontsize=11, fontweight="normal", labelpad=6)
            ax3.set_title(
                "Dez issues com maior clustering",
                fontsize=11,
                fontweight="normal",
                pad=10,
            )
            ax3.set_xlim(0, 1)
            aplicar_eixos_principais(ax3)
            ax3.invert_yaxis()
            for i, coeff in enumerate(coeffs):
                ax3.text(
                    coeff + 0.015,
                    i,
                    f"{coeff:.2f}",
                    va="center",
                    fontsize=8,
                    fontweight="normal",
                )

        ax4 = axes[1, 1]
        ax4.axis("off")
        total_issues = len(metrics.get("degree", {}).get("issues", []))
        total_capabilities = len(metrics.get("degree", {}).get("capabilities", []))
        total_links = density.get("total_links", 0) if density else 0
        max_links = density.get("max_possible_links", 0) if density else 0
        density_value = density.get("Density", 0) if density else 0
        summary_text = (
            f"Resumo da rede\n\n"
            f"Issues: {total_issues}\n"
            f"BusinessCapabilities: {total_capabilities}\n"
            f"Links: {total_links}\n"
            f"Links máx. possíveis: {max_links}\n"
            f"Densidade: {density_value:.4f} ({density_value*100:.2f}%)\n"
        )
        ax4.text(
            0.08,
            0.55,
            summary_text,
            fontsize=10,
            verticalalignment="center",
            family="sans-serif",
            transform=ax4.transAxes,
            bbox=dict(boxstyle="round", facecolor="white", edgecolor="0.4", linewidth=0.8),
        )

        plt.tight_layout()
        p = output_dir / "sna_metricas_combinadas.png"
        fig.savefig(p, dpi=300, bbox_inches="tight", facecolor="white", edgecolor="none")
        plt.close(fig)

    print(f"Grafico salvo: {p}")


def gerar_todos_graficos_sna():
    print("Gerando visualizacoes de metricas SNA...")
    output_dir = criar_diretorio_imagens()
    dados_json = "reports/sna_metrics.json"
    grafico_degree_centrality(dados_json, output_dir)
    grafico_metricas_combinadas(dados_json, output_dir)
    print("Todos os graficos SNA foram gerados com sucesso!")
    print(f"Arquivos salvos em: {output_dir}")


if __name__ == "__main__":
    gerar_todos_graficos_sna()
