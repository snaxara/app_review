"""
Script para gerar visualizações para o TCC
Gera gráficos e tabelas formatadas para inserção no documento
"""

import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

try:
    from scripts.tcc_chart_style import (
        CINZA_CLARO,
        CINZA_ESCURO,
        CINZA_MEDIO,
        aplicar_eixos_principais,
        contexto,
        painel_letra,
    )
except ImportError:
    from tcc_chart_style import (
        CINZA_CLARO,
        CINZA_ESCURO,
        CINZA_MEDIO,
        aplicar_eixos_principais,
        contexto,
        painel_letra,
    )

def carregar_dados_metricas():
    """Carrega dados das métricas do grafo"""
    with open('reports/metrics_caixa_refinado.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def criar_diretorio_imagens():
    """Cria diretório para armazenar imagens"""
    dir_imagens = Path('Documentos/imagens_tcc')
    dir_imagens.mkdir(exist_ok=True)
    return dir_imagens

def grafico_distribuicao_issues_por_capability(dados, output_dir):
    """Gera gráfico de barras horizontal com distribuição de issues por BusinessCapability"""
    capabilities = []
    issues_count = []
    episodios_count = []

    for cap_name, stats in dados["capability_statistics"].items():
        capabilities.append(cap_name)
        issues_count.append(stats["total_issues"])
        episodios_count.append(stats["total_episodes"])

    df = pd.DataFrame(
        {
            "BusinessCapability": capabilities,
            "Issues": issues_count,
            "Episódios": episodios_count,
        }
    )
    df = df.sort_values("Issues", ascending=True)

    with contexto():
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 7.5), facecolor="white")
        ax1.barh(
            df["BusinessCapability"],
            df["Issues"],
            color=CINZA_ESCURO,
            edgecolor="black",
            linewidth=0.5,
        )
        ax1.set_xlabel("Quantidade de issues (n)", fontsize=11, fontweight="normal", labelpad=6)
        aplicar_eixos_principais(ax1)
        xmax = df["Issues"].max()
        ax1.set_xlim(0, xmax * 1.12 + 0.5)
        for i, v in enumerate(df["Issues"]):
            ax1.text(v + 0.35, i, str(int(v)), va="center", fontsize=9, fontweight="normal")

        ax2.barh(
            df["BusinessCapability"],
            df["Episódios"],
            color=CINZA_MEDIO,
            edgecolor="black",
            linewidth=0.5,
        )
        ax2.set_xlabel("Quantidade de episódios (n)", fontsize=11, fontweight="normal", labelpad=6)
        aplicar_eixos_principais(ax2)
        xmax2 = df["Episódios"].max()
        ax2.set_xlim(0, xmax2 * 1.12 + 0.5)
        for i, v in enumerate(df["Episódios"]):
            ax2.text(v + 0.35, i, str(int(v)), va="center", fontsize=9, fontweight="normal")

        plt.tight_layout()
        plt.savefig(
            output_dir / "distribuicao_issues_capabilities.png",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
        )
        plt.close()

    print(f"Grafico salvo: {output_dir / 'distribuicao_issues_capabilities.png'}")

def grafico_top_10_issues(dados, output_dir):
    """Gera gráfico com top 10 issues mais críticas"""
    todas_issues = []

    for cap_name, stats in dados["capability_statistics"].items():
        for issue in stats["top_issues"]:
            todas_issues.append(
                {
                    "Issue": issue["Issue"],
                    "Episódios": issue["TotalEpisodes"],
                    "Capability": cap_name,
                }
            )

    df = pd.DataFrame(todas_issues)
    df = df.sort_values("Episódios", ascending=False).head(10)

    with contexto():
        fig, ax = plt.subplots(figsize=(11, 6.5), facecolor="white")
        ax.barh(
            range(len(df)),
            df["Episódios"],
            color=CINZA_ESCURO,
            edgecolor="black",
            linewidth=0.5,
        )
        ax.set_yticks(range(len(df)))
        ax.set_yticklabels(df["Issue"], fontsize=9)
        ax.set_xlabel("Número de episódios (n)", fontsize=11, fontweight="normal", labelpad=6)
        aplicar_eixos_principais(ax)
        xmax = df["Episódios"].max()
        ax.set_xlim(0, xmax * 1.15 + 0.3)
        for i, v in enumerate(df["Episódios"]):
            ax.text(float(v) + 0.12, i, str(int(v)), va="center", fontsize=9, fontweight="normal")
        ax.invert_yaxis()
        plt.tight_layout()
        plt.savefig(
            output_dir / "top_10_issues.png",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
        )
        plt.close()

    print(f"Grafico salvo: {output_dir / 'top_10_issues.png'}")

def grafico_distribuicao_por_nivel_tipo(dados, output_dir):
    """Gera gráficos de pizza para distribuição por nível, tipo e valor de negócio"""
    nivel_stats = {"Nível 1": 0, "Nível 2": 0}
    tipo_stats = {"Core": 0, "Supporting": 0, "Strategic": 0}
    valor_stats = {"High": 0, "Medium": 0, "Low": 0}

    for cap_name, stats in dados["capability_statistics"].items():
        nivel = f"Nível {stats['level']}"
        tipo = stats["capability_type"]
        valor = stats["business_value"]
        nivel_stats[nivel] += stats["total_issues"]
        tipo_stats[tipo] += stats["total_issues"]
        valor_stats[valor] += stats["total_issues"]

    pie_kw = dict(
        startangle=90,
        textprops={"fontsize": 10, "fontweight": "normal", "color": "black"},
        wedgeprops={"edgecolor": "black", "linewidth": 0.6},
    )

    with contexto():
        fig, axes = plt.subplots(1, 3, figsize=(15, 5.2), facecolor="white")
        nivel_labels = list(nivel_stats.keys())
        nivel_values = list(nivel_stats.values())
        axes[0].pie(
            nivel_values,
            labels=nivel_labels,
            autopct="%1.1f%%",
            colors=[CINZA_ESCURO, CINZA_CLARO],
            **pie_kw,
        )
        axes[0].set_title("Nível hierárquico", fontsize=11, fontweight="normal", pad=12)
        painel_letra(axes[0], "A")

        tipo_labels = [k for k, v in tipo_stats.items() if v > 0]
        tipo_values = [tipo_stats[k] for k in tipo_labels]
        cinzas_tipo = [CINZA_ESCURO, CINZA_MEDIO, CINZA_CLARO][: len(tipo_labels)]
        axes[1].pie(
            tipo_values,
            labels=tipo_labels,
            autopct="%1.1f%%",
            colors=cinzas_tipo,
            **pie_kw,
        )
        axes[1].set_title("Tipo de BusinessCapability", fontsize=11, fontweight="normal", pad=12)
        painel_letra(axes[1], "B")

        valor_labels = [k for k, v in valor_stats.items() if v > 0]
        valor_values = [valor_stats[k] for k in valor_labels]
        cinzas_val = [CINZA_ESCURO, CINZA_MEDIO, CINZA_CLARO][: len(valor_labels)]
        axes[2].pie(
            valor_values,
            labels=valor_labels,
            autopct="%1.1f%%",
            colors=cinzas_val,
            **pie_kw,
        )
        axes[2].set_title("Valor de negócio", fontsize=11, fontweight="normal", pad=12)
        painel_letra(axes[2], "C")

        plt.tight_layout()
        plt.savefig(
            output_dir / "distribuicao_nivel_tipo_valor.png",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
        )
        plt.close()

    print(f"Grafico salvo: {output_dir / 'distribuicao_nivel_tipo_valor.png'}")

def grafico_pipeline_processamento(output_dir):
    """Gera diagrama do pipeline de processamento"""
    etapas = [
        "Coleta de\navaliações",
        "Análise de\nsentimentos",
        "Triagem\nautomática",
        "Extração de\nentidades",
        "Modelagem em\nKnowledge Graph",
        "Geração de\ndocumentos",
    ]
    x_positions = [1, 2.5, 4, 5.5, 7, 8.5]

    with contexto():
        fig, ax = plt.subplots(figsize=(13, 4.2), facecolor="white")
        for i, (etapa, x) in enumerate(zip(etapas, x_positions)):
            rect = plt.Rectangle(
                (x - 0.4, 0.28),
                0.8,
                0.44,
                facecolor=CINZA_CLARO,
                edgecolor="black",
                linewidth=1.5,
            )
            ax.add_patch(rect)
            ax.text(
                x,
                0.5,
                etapa,
                ha="center",
                va="center",
                fontsize=9,
                fontweight="normal",
                color="black",
            )
            if i < len(etapas) - 1:
                ax.arrow(
                    x + 0.4,
                    0.5,
                    0.48,
                    0,
                    head_width=0.055,
                    head_length=0.09,
                    fc="black",
                    ec="black",
                    linewidth=1.2,
                )
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 1)
        ax.set_title(
            "Pipeline de processamento de avaliações",
            fontsize=11,
            fontweight="normal",
            pad=14,
        )
        ax.axis("off")
        plt.tight_layout()
        plt.savefig(
            output_dir / "pipeline_processamento.png",
            dpi=300,
            bbox_inches="tight",
            facecolor="white",
            edgecolor="none",
        )
        plt.close()

    print(f"Grafico salvo: {output_dir / 'pipeline_processamento.png'}")

def gerar_todas_visualizacoes():
    """Gera todas as visualizações"""
    print("Gerando visualizacoes para o TCC...")
    
    # Criar diretório
    output_dir = criar_diretorio_imagens()
    
    # Carregar dados
    dados = carregar_dados_metricas()
    
    # Gerar gráficos
    print("\n1. Gerando grafico de distribuicao de issues por capability...")
    grafico_distribuicao_issues_por_capability(dados, output_dir)
    
    print("\n2. Gerando grafico top 10 issues...")
    grafico_top_10_issues(dados, output_dir)
    
    print("\n3. Gerando graficos de distribuicao por nivel/tipo/valor...")
    grafico_distribuicao_por_nivel_tipo(dados, output_dir)
    
    print("\n4. Gerando diagrama do pipeline...")
    grafico_pipeline_processamento(output_dir)
    
    print("\nTodas as visualizacoes foram geradas com sucesso!")
    print(f"Arquivos salvos em: {output_dir}")

if __name__ == '__main__':
    gerar_todas_visualizacoes()
