"""
Gera apresentação PowerPoint do TCC - 20 minutos
Baseado em TCC_COMPLETO_ATUALIZADO.md
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import os

# Caminhos
BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
IMAGENS = os.path.join(BASE, "Documentos", "imagens_tcc")
OUTPUT = os.path.join(BASE, "tcc", "Apresentacao_TCC_20min.pptx")


def slide_titulo(prs, titulo, subtitulo="", autor="Simone Rossetti Nobre Naxara", orientador="Dra. Anna Carolina Martins"):
    """Slide de capa."""
    slide_layout = prs.slide_layouts[6]  # Blank
    slide = prs.slides.add_slide(slide_layout)
    # Título
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(2), Inches(9), Inches(1.5))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = titulo
    p.font.size = Pt(28)
    p.font.bold = True
    p.alignment = PP_ALIGN.CENTER
    # Subtítulo
    if subtitulo:
        tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(3.8), Inches(9), Inches(0.8))
        tf2 = tb2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = subtitulo
        p2.font.size = Pt(14)
        p2.alignment = PP_ALIGN.CENTER
    # Autora e orientadora
    tb3 = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(9), Inches(1.2))
    tf3 = tb3.text_frame
    tf3.word_wrap = True
    p3 = tf3.paragraphs[0]
    p3.text = f"Autora: {autor}\nOrientadora: {orientador}"
    p3.font.size = Pt(14)
    p3.alignment = PP_ALIGN.CENTER
    return slide


def slide_titulo_secao(prs, titulo, subtitulo=""):
    """Slide com título de seção."""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(2.5), Inches(9), Inches(1))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = titulo
    p.font.size = Pt(32)
    p.font.bold = True
    if subtitulo:
        tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(3.8), Inches(9), Inches(0.8))
        tf2 = tb2.text_frame
        p2 = tf2.paragraphs[0]
        p2.text = subtitulo
        p2.font.size = Pt(16)
    return slide


def slide_conteudo(prs, titulo, bullets, nota="", fonte="elaboração própria"):
    """Slide com título e bullets."""
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    # Título
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    tf = tb.text_frame
    p = tf.paragraphs[0]
    p.text = titulo
    p.font.size = Pt(24)
    p.font.bold = True
    # Bullets
    tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(1.1), Inches(9), Inches(4.5))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    for i, b in enumerate(bullets):
        if i == 0:
            para = tf2.paragraphs[0]
        else:
            para = tf2.add_paragraph()
        para.text = f"• {b}" if not b.startswith("•") else b
        para.font.size = Pt(14)
        para.space_before = Pt(6)
    if nota:
        tb3 = slide.shapes.add_textbox(Inches(0.5), Inches(5.8), Inches(9), Inches(0.5))
        tf3 = tb3.text_frame
        p3 = tf3.paragraphs[0]
        p3.text = nota
        p3.font.size = Pt(10)
        p3.font.italic = True
    return slide


def adicionar_imagem(slide, img_path, left=0.5, top=1.2, width=9):
    """Adiciona imagem ao slide se existir."""
    if os.path.exists(img_path):
        slide.shapes.add_picture(img_path, Inches(left), Inches(top), width=Inches(width))
        return True
    return False


def main():
    prs = Presentation()
    prs.slide_width = Inches(10)
    prs.slide_height = Inches(7.5)

    # 1. Capa
    slide_titulo(
        prs,
        "Priorização de Backlog em Apps Bancários via Knowledge Graph e Feedback do Usuário",
        "MBA USP/ESALQ – Data Science e Analytics"
    )

    # 2. Contexto
    slide_conteudo(
        prs,
        "Contexto – Mobile banking no Brasil",
        [
            "FEBRABAN: mais de 75% das transações via mobile",
            "Dependência tecnológica → qualidade é questão estratégica",
            "Impacto de problemas: perda de confiança, migração, prejuízos financeiros"
        ],
        "FEBRABAN (2024); Anouze et al. (2019)"
    )

    # 3. O problema
    slide_conteudo(
        prs,
        "O problema – Lacuna nos testes tradicionais",
        [
            "Testes ISTQB não cobrem cenários reais de produção",
            "Em produção: dispositivos diversos, rede instável, padrões imprevistos",
            "Avaliações das lojas = termômetro em tempo real, mas pouco exploradas",
            "Nota 1–5 estrelas é insuficiente (mesmo negativa pode esconder problemas muito diferentes)"
        ]
    )

    # 4. Objetivo
    slide_conteudo(
        prs,
        "Objetivo e proposta",
        [
            "Objetivo: transformar feedback textual das lojas em documentos estruturados de priorização",
            "Abordagem além da esteira tradicional → testes em produção",
            "Pipeline: coleta → polarização → extração → Knowledge Graph → priorização"
        ]
    )

    # 5. Pipeline (com imagem)
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    tb.text_frame.paragraphs[0].text = "Arquitetura – Pipeline em dois estágios"
    tb.text_frame.paragraphs[0].font.size = Pt(24)
    tb.text_frame.paragraphs[0].font.bold = True
    bullets = [
        "Estágio 1: BERTweet (XLM-RoBERTa) → polarização",
        "Estágio 2: GPT-4o → extração de entidades → Neo4j",
        "Filtro: apenas comentários negativos passam ao estágio 2"
    ]
    tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(5.5), Inches(9), Inches(1.2))
    for i, b in enumerate(bullets):
        p = tb2.text_frame.paragraphs[i] if i == 0 else tb2.text_frame.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(12)
    img_path = os.path.join(IMAGENS, "pipeline_processamento.png")
    adicionar_imagem(slide, img_path, top=1.1, width=8)

    # 6. Metodologia – Coleta
    slide_conteudo(
        prs,
        "Metodologia – Coleta e dataset",
        [
            "Google Play Store, app CAIXA",
            "Coleta jan/2026: 2.451 aval., média ~188/dia",
            "Higienização: remoção de vazios e < 3 palavras",
            "Atributos: texto, nota 1–5, data, versão"
        ]
    )

    # 7. Metodologia – Modelos
    slide_conteudo(
        prs,
        "Metodologia – Modelos",
        [
            "Estágio 1: XLM-RoBERTa (BERTweet) – polarização",
            "Estágio 2: GPT-4o – extração (temperature 0,1)",
            "Etapa de reflexão: segunda passada recupera 5–10% de entidades perdidas",
            "Mapeamento para 15 BusinessCapabilities"
        ]
    )

    # 8. Knowledge Graph
    slide_conteudo(
        prs,
        "Knowledge Graph temporal",
        [
            "Estrutura: App → Version → Episode → Issue → BusinessCapability",
            "Três subgrafos: Episódico, Semântico, Comunidade",
            "Neo4j para armazenamento",
            "Uma Issue pode relacionar-se a várias BusinessCapabilities (natureza transversal)"
        ]
    )

    # 9. Resultados – Amostra
    slide_conteudo(
        prs,
        "Resultados – Amostra processada",
        [
            "2.451 avaliações (5–18 jan/2026)",
            "878 negativas (35,82%) → filtro → 763 válidas",
            "100 comentários processados → 103 episódios, 85 issues",
            "15 BusinessCapabilities, 91 relacionamentos (91 > 85 = transversalidade)"
        ]
    )

    # 10. Figuras GPT
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    tb.text_frame.paragraphs[0].text = "Resultados – Comparação de modelos GPT (Figura 2)"
    tb.text_frame.paragraphs[0].font.size = Pt(24)
    tb.text_frame.paragraphs[0].font.bold = True
    tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(9), Inches(1.5))
    for i, b in enumerate([
        "GPT-4o-2024-08-06: 63,6% acurácia (14/22 corretos)",
        "Refinamento: 54,5% → 63,6%",
        "Erros: gírias, sarcasmo, múltiplos problemas, referências implícitas"
    ]):
        p = tb2.text_frame.paragraphs[i] if i == 0 else tb2.text_frame.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(12)
    adicionar_imagem(slide, os.path.join(IMAGENS, "comparacao_modelos_gpt.png"), top=1, width=8)

    # 11. Modelos polarização
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    tb.text_frame.paragraphs[0].text = "Resultados – Modelos de polarização"
    tb.text_frame.paragraphs[0].font.size = Pt(24)
    tb.text_frame.paragraphs[0].font.bold = True
    tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(5), Inches(9), Inches(1.5))
    for i, b in enumerate([
        "BERTweet: 96,17% acurácia vs 74,32% DistilBERT",
        "ROC AUC: 98,97% vs 78,98%",
        "Melhor interpretação de ironias e expressões do domínio"
    ]):
        p = tb2.text_frame.paragraphs[i] if i == 0 else tb2.text_frame.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(12)
    adicionar_imagem(slide, os.path.join(IMAGENS, "comparacao_modelos_sentimentos.png"), top=1, width=8)

    # 12. Estatísticas do grafo
    slide_conteudo(
        prs,
        "Resultados – Estatísticas do Knowledge Graph",
        [
            "103 episódios | 85 issues | 15 BusinessCapabilities | 91 relacionamentos",
            "91 > 85 → issues associadas a múltiplas capacidades",
            "Exemplo: 'Bloqueio de Senha' → Autenticação + Segurança",
            "Cobertura 100% para mapeamento em BusinessCapability"
        ]
    )

    # 13. Distribuição e Top 10
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    tb.text_frame.paragraphs[0].text = "Resultados – Distribuição e Top 10 Issues"
    tb.text_frame.paragraphs[0].font.size = Pt(24)
    tb.text_frame.paragraphs[0].font.bold = True
    tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(9), Inches(1.5))
    for i, b in enumerate([
        "Performance e Estabilidade: 23,53% (20 de 85)",
        "Top 3: Performance, Gestão de Cadastro, Autenticação",
        "'Lentidão' em 7 episódios – issue mais crítica",
        "65% das issues em capacidades de alto valor de negócio"
    ]):
        p = tb2.text_frame.paragraphs[i] if i == 0 else tb2.text_frame.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(12)
    adicionar_imagem(slide, os.path.join(IMAGENS, "distribuicao_issues_capabilities.png"), top=1, width=7)
    adicionar_imagem(slide, os.path.join(IMAGENS, "top_10_issues.png"), left=5, top=1, width=4)

    # 14. SNA
    slide_layout = prs.slide_layouts[6]
    slide = prs.slides.add_slide(slide_layout)
    tb = slide.shapes.add_textbox(Inches(0.5), Inches(0.3), Inches(9), Inches(0.6))
    tb.text_frame.paragraphs[0].text = "Resultados – Métricas de Social Network Analysis"
    tb.text_frame.paragraphs[0].font.size = Pt(24)
    tb.text_frame.paragraphs[0].font.bold = True
    tb2 = slide.shapes.add_textbox(Inches(0.5), Inches(5.2), Inches(9), Inches(1.5))
    for i, b in enumerate([
        "93% das issues com degree 1; 6 issues (senha) com degree 2",
        "Clustering de senha: 0,91 → cluster denso",
        "Betweenness e Closeness Centrality para 'pontes' e impacto amplo"
    ]):
        p = tb2.text_frame.paragraphs[i] if i == 0 else tb2.text_frame.add_paragraph()
        p.text = f"• {b}"
        p.font.size = Pt(12)
    adicionar_imagem(slide, os.path.join(IMAGENS, "sna_metricas_combinadas.png"), top=1, width=8)

    # 15. Exemplo qualitativo
    slide_conteudo(
        prs,
        "Exemplo qualitativo",
        [
            "Comentário: 'Depois que atualizou o app, não reconhece a biometria, tem que ficar colocando a senha'",
            "Entidades: 'Não reconhece biometria', 'Inserir senha'",
            "Mapeamento: Login/Autenticação + Segurança e Proteção"
        ]
    )

    # 16. Conclusão
    slide_conteudo(
        prs,
        "Conclusão",
        [
            "Viabilidade demonstrada para transformar feedback em documentos estruturados",
            "85 issues extraídas | 63,6% acurácia | 100% cobertura",
            "Triagem: 13,1% comentários genéricos removidos",
            "Reflexão: +5–10% entidades recuperadas",
            "Potencial de escala e integração com BI/Jira"
        ]
    )

    # 17. Limitações e próximos passos
    slide_conteudo(
        prs,
        "Limitações e próximos passos",
        [
            "Limitações: amostra 100 comentários; validação temporal pendente; processamento sequencial",
            "Próximos: expandir amostra, validação com especialistas, processamento paralelo, templates automáticos"
        ]
    )

    # 18. Fechamento
    slide_titulo(prs, "Obrigada!", "Perguntas?", autor="Simone Rossetti Nobre Naxara\nsimone-rossetti@usp.br", orientador="")

    # Salvar
    os.makedirs(os.path.dirname(OUTPUT), exist_ok=True)
    prs.save(OUTPUT)
    print(f"OK - Apresentacao gerada: {OUTPUT}")
    print(f"  Total de slides: {len(prs.slides)}")
    if not os.path.exists(IMAGENS):
        print(f"  AVISO - Pasta de imagens nao encontrada: {IMAGENS}")
        print("    Adicione as imagens e execute novamente para incluí-las nos slides.")


if __name__ == "__main__":
    main()
