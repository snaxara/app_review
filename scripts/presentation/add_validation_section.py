"""
Script para adicionar seção completa de validação do modelo na apresentação
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import MSO_ANCHOR
import pandas as pd

# Carregar dados
df = pd.read_csv('app_review_dataset_carol.csv', encoding='utf-8', sep=';')
total = len(df)
neg = df['negative'].sum()

# Calcular divisão treino/teste (80/20)
n_train = int(total * 0.8)
n_test = total - n_train

print("Carregando apresentação...")
prs = Presentation("Documentos/Correlação Funcional de Feedbacks em Apps Bancários v2 - ATUALIZADA.pptx")

def add_text_box(slide, text, left, top, width, height, font_size=11):
    """Adiciona uma nova text box ao slide."""
    textbox = slide.shapes.add_textbox(left, top, width, height)
    text_frame = textbox.text_frame
    text_frame.word_wrap = True
    text_frame.vertical_anchor = MSO_ANCHOR.TOP
    p = text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    return textbox

# Slide 6: Avaliação - SUBSTITUIR com validação completa
if len(prs.slides) > 5:
    slide6 = prs.slides[5]
    print("  - Slide 6: Adicionando validação completa do modelo...")
    
    # Limpar conteúdo anterior e adicionar novo
    validation_content = (
        "📊 ESTRATÉGIA DE VALIDAÇÃO DO MODELO\n\n"
        "1. DIVISÃO TREINO/TESTE:\n"
        f"   • Treino: {n_train} avaliações (80%)\n"
        f"   • Teste: {n_test} avaliações (20%)\n"
        "   • Base Humana: 2 classificadores independentes\n\n"
        "2. VALIDAÇÃO DA CATEGORIZAÇÃO AUTOMÁTICA:\n"
        "   • Comparar: LLM (GPT-4o) vs. Classificação Humana\n"
        "   • Métricas por categoria:\n"
        "     - Precision: Categorias corretas / Total predito\n"
        "     - Recall: Categorias corretas / Total real\n"
        "     - F1-Score: Média harmônica (Precision + Recall)\n"
        "   • Meta: F1-Score > 80% por categoria\n\n"
        "3. VALIDAÇÃO DA PRIORIZAÇÃO DE BACKLOG:\n"
        "   • Comparar: Backlog gerado vs. Backlog esperado (humano)\n"
        "   • Métricas:\n"
        "     - Correlação de Spearman: Ordem das prioridades\n"
        "     - Acurácia Top-K: % de categorias corretas no top 3/5\n"
        "     - MAP@K: Mean Average Precision\n"
        "   • Meta: Correlação > 0.7, Top-3 Acurácia > 70%\n\n"
        "4. INTER-ANNOTATOR AGREEMENT:\n"
        "   • Cohen's Kappa: Concordância entre classificadores humanos\n"
        "   • Meta: Kappa > 0.7 (concordância substancial)\n\n"
        "✅ Status Atual:\n"
        f"   • {total} avaliações classificadas por Carol\n"
        "   • Aguardando segunda classificação\n"
        "   • Próximo passo: Calcular métricas de validação"
    )
    
    # Adicionar novo conteúdo
    add_text_box(slide6, validation_content,
                Inches(0.5), Inches(1), Inches(9), Inches(5.5), font_size=9)

# Salvar
output_file = "Documentos/Correlação Funcional de Feedbacks em Apps Bancários v2 - ATUALIZADA.pptx"
prs.save(output_file)

print(f"\n✓ Apresentação atualizada com validação completa!")
print(f"  Arquivo: {output_file}")

