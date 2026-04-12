"""
Script para atualizar a apresentação v2 com dados reais
e ajustes baseados no feedback do gestor
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import pandas as pd

# Carregar dados reais
df = pd.read_csv('app_review_dataset_carol.csv', encoding='utf-8', sep=';')
total = len(df)
pos = df['positive'].sum()
neg = df['negative'].sum()
neu = df['neutral'].sum()

categories = ["PIX", "Login/Autenticação", "Performance", "Interface/Usabilidade", 
              "Empréstimos/Crédito", "Pagamentos/Boletos", "Saldo/Extrato", 
              "Atendimento", "Cadastro/Conta", "Investimentos", "Segurança", 
              "Notificações", "Questões geográficas", "Placas/Veículos", 
              "Tarifas/Cobranças", "Outros"]

# Calcular estatísticas reais
neg_with_category = (df[df['negative'] == 1][categories].sum(axis=1) > 0).sum()
total_categories = len(categories)

# Distribuição de categorias (apenas negativas)
df_neg = df[df['negative'] == 1]
category_counts = {}
for cat in categories:
    if cat in df.columns:
        category_counts[cat] = int(df_neg[cat].sum())

# Ordenar por frequência
sorted_categories = sorted(category_counts.items(), key=lambda x: x[1], reverse=True)
top3_categories = sorted_categories[:3]

print("Carregando apresentação v2...")
prs = Presentation("Documentos/Correlação Funcional de Feedbacks em Apps Bancários v2.pptx")

def replace_text_in_shape(shape, old_text, new_text):
    """Substitui texto em uma shape."""
    if hasattr(shape, "text"):
        if old_text in shape.text:
            shape.text = shape.text.replace(old_text, new_text)
            return True
    return False

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

print("\nAtualizando slides...")

# Slide 2: Entendimento do Negócio
if len(prs.slides) > 1:
    slide2 = prs.slides[1]
    print("  - Slide 2: Atualizando estatísticas...")
    
    # Atualizar porcentagem de correlação
    correlation_pct = (neg_with_category / neg * 100) if neg > 0 else 0
    replace_text_in_shape(slide2, "83,5%", f"{correlation_pct:.1f}%")
    
    # Adicionar nota sobre validação humana
    add_text_box(slide2, 
                f"✓ Dataset Validado: {total} avaliações classificadas manualmente por humanos",
                Inches(0.5), Inches(5.5), Inches(9), Inches(0.5), font_size=10)

# Slide 3: Entendimento dos Dados
if len(prs.slides) > 2:
    slide3 = prs.slides[2]
    print("  - Slide 3: Atualizando números e distribuição...")
    
    # Atualizar números principais
    replace_text_in_shape(slide3, "1.000", f"{total}")
    replace_text_in_shape(slide3, "266", f"{neg}")
    replace_text_in_shape(slide3, "13", f"{total_categories}")
    
    # Atualizar distribuição de polaridade
    replace_text_in_shape(slide3, "Distribuição de Polaridade", 
                         f"Distribuição de Polaridade (Validado por Humanos)")
    
    # Atualizar Top 3 Problemas
    if len(top3_categories) >= 3:
        cat1_name, cat1_count = top3_categories[0]
        cat2_name, cat2_count = top3_categories[1]
        cat3_name, cat3_count = top3_categories[2]
        
        cat1_pct = (cat1_count / neg * 100) if neg > 0 else 0
        cat2_pct = (cat2_count / neg * 100) if neg > 0 else 0
        cat3_pct = (cat3_count / neg * 100) if neg > 0 else 0
        
        # Atualizar Performance
        replace_text_in_shape(slide3, "1. Performance\n42%", 
                             f"1. {cat1_name}\n{cat1_pct:.1f}%")
        replace_text_in_shape(slide3, "App travando, lentidão no carregamento, fechamento inesperado.", 
                             f"{cat1_count} casos identificados.")
        
        # Atualizar Login/Autenticação
        replace_text_in_shape(slide3, "2. Login/Autenticação\n15%", 
                             f"2. {cat2_name}\n{cat2_pct:.1f}%")
        replace_text_in_shape(slide3, "Problemas de acesso, recuperação de senha, biometria.", 
                             f"{cat2_count} casos identificados.")
        
        # Atualizar PIX
        replace_text_in_shape(slide3, "3. PIX\n3,8%", 
                             f"3. {cat3_name}\n{cat3_pct:.1f}%")
        replace_text_in_shape(slide3, "Erro nas transações de PIX e tetimeout de confirmação.", 
                             f"{cat3_count} casos identificados.")

# Slide 4: Preparação dos Dados
if len(prs.slides) > 3:
    slide4 = prs.slides[3]
    print("  - Slide 4: Adicionando informação sobre validação humana...")
    
    # Adicionar nota sobre rotulagem humana
    add_text_box(slide4,
                f"✓ Rotulagem Humana: {total} avaliações classificadas manualmente\n"
                f"✓ {total_categories} categorias funcionais identificadas\n"
                f"✓ Classificação múltipla (múltiplas categorias por avaliação)",
                Inches(0.5), Inches(5.5), Inches(9), Inches(1), font_size=10)

# Slide 5: Modelagem - DETALHAR MÉTODO E MODELO
if len(prs.slides) > 4:
    slide5 = prs.slides[4]
    print("  - Slide 5: Adicionando detalhes do método e modelo...")
    
    # Adicionar seção detalhada sobre método
    method_detail = (
        "📋 Detalhamento do Método:\n\n"
        "1. Análise de Sentimentos:\n"
        "   • Modelo: cardiffnlp/twitter-xlm-roberta-base-sentiment\n"
        "   • Framework: Hugging Face Transformers\n"
        "   • Parâmetros: Batch size 16, Device CPU\n"
        "   • Técnica: Fine-tuning em dados de redes sociais\n\n"
        "2. Categorização Funcional:\n"
        "   • Modelo: GPT-4o (OpenAI)\n"
        "   • Técnica: Prompt Engineering (zero-shot learning)\n"
        "   • Abordagem: Classificação múltipla\n"
        "   • Parâmetros: Temperature 0.3, Max tokens 200\n\n"
        "3. Taxonomia: 16 categorias funcionais\n"
        "   (PIX, Login/Autenticação, Performance, Interface/Usabilidade,\n"
        "    Empréstimos/Crédito, Pagamentos/Boletos, Saldo/Extrato,\n"
        "    Atendimento, Cadastro/Conta, Investimentos, Segurança,\n"
        "    Notificações, Questões geográficas, Placas/Veículos,\n"
        "    Tarifas/Cobranças, Outros)"
    )
    
    add_text_box(slide5, method_detail, 
                Inches(0.5), Inches(3.5), Inches(9), Inches(3.5), font_size=9)

# Slide 6: Avaliação - ADICIONAR MÉTRICAS COM BASE HUMANA
if len(prs.slides) > 5:
    slide6 = prs.slides[5]
    print("  - Slide 6: Adicionando métricas com base humana...")
    
    # Adicionar seção de validação humana
    human_validation = (
        "✅ Validação com Base Humana:\n\n"
        f"• Dataset: {total} avaliações classificadas manualmente\n"
        f"• Classificador: Carol (concluído)\n"
        f"• Status: Aguardando segunda classificação para inter-annotator agreement\n\n"
        "📊 Métricas a Calcular:\n"
        "• Acurácia do modelo de sentimento (DistilBERT vs. Humano)\n"
        "• Acurácia da correlação funcional (GPT-4o vs. Humano) por categoria\n"
        "• Inter-Annotator Agreement (Cohen's Kappa)\n\n"
        "🎯 Resultados Esperados:\n"
        "• F1-Score > 80% por categoria\n"
        "• Acurácia geral > 85% em sentimentos"
    )
    
    add_text_box(slide6, human_validation,
                Inches(0.5), Inches(4), Inches(9), Inches(2.5), font_size=9)

# Slide 7: Resultado - Backlog Priorizado
if len(prs.slides) > 6:
    slide7 = prs.slides[6]
    print("  - Slide 7: Atualizando backlog priorizado...")
    
    # Calcular severidade média por categoria (apenas negativas)
    df_neg = df[df['negative'] == 1].copy()
    df_neg['score'] = pd.to_numeric(df_neg['score'], errors='coerce')
    
    # Atualizar Performance
    perf_count = category_counts.get('Performance', 0)
    perf_severity = df_neg[df_neg['Performance'] == 1]['score'].mean() if perf_count > 0 else 0
    perf_pct = (perf_count / neg * 100) if neg > 0 else 0
    
    replace_text_in_shape(slide7, "Performance\n42%\n112 Casos\n1.86", 
                         f"Performance\n{perf_pct:.1f}%\n{perf_count} Casos\n{perf_severity:.2f}")
    
    # Atualizar Login/Auth
    login_count = category_counts.get('Login/Autenticação', 0)
    login_severity = df_neg[df_neg['Login/Autenticação'] == 1]['score'].mean() if login_count > 0 else 0
    login_pct = (login_count / neg * 100) if neg > 0 else 0
    
    replace_text_in_shape(slide7, "Login/Auth\n15%\n41 Casos\n1.79", 
                         f"Login/Auth\n{login_pct:.1f}%\n{login_count} Casos\n{login_severity:.2f}")
    
    # Atualizar Segurança
    seg_count = category_counts.get('Segurança', 0)
    seg_severity = df_neg[df_neg['Segurança'] == 1]['score'].mean() if seg_count > 0 else 0
    seg_pct = (seg_count / neg * 100) if neg > 0 else 0
    
    if seg_count > 0:
        replace_text_in_shape(slide7, "Segurança\n4%\n4 Casos\n1.00", 
                             f"Segurança\n{seg_pct:.1f}%\n{seg_count} Casos\n{seg_severity:.2f}")
    
    # Atualizar PIX
    pix_count = category_counts.get('PIX', 0)
    pix_severity = df_neg[df_neg['PIX'] == 1]['score'].mean() if pix_count > 0 else 0
    pix_pct = (pix_count / neg * 100) if neg > 0 else 0
    
    replace_text_in_shape(slide7, "PIX\n2%\n4 Casos\n2.75", 
                         f"PIX\n{pix_pct:.1f}%\n{pix_count} Casos\n{pix_severity:.2f}")
    
    # Atualizar Empréstimos
    emp_count = category_counts.get('Empréstimos/Crédito', 0)
    emp_severity = df_neg[df_neg['Empréstimos/Crédito'] == 1]['score'].mean() if emp_count > 0 else 0
    emp_pct = (emp_count / neg * 100) if neg > 0 else 0
    
    replace_text_in_shape(slide7, "Empréstimos\n4%\n8 Casos\n1.50", 
                         f"Empréstimos\n{emp_pct:.1f}%\n{emp_count} Casos\n{emp_severity:.2f}")

# Slide 8: Deep Dive Login/Autenticação
if len(prs.slides) > 7:
    slide8 = prs.slides[7]
    print("  - Slide 8: Atualizando deep dive...")
    
    login_count = category_counts.get('Login/Autenticação', 0)
    login_pct = (login_count / neg * 100) if neg > 0 else 0
    login_severity = df_neg[df_neg['Login/Autenticação'] == 1]['score'].mean() if login_count > 0 else 0
    
    replace_text_in_shape(slide8, "14%", f"{login_pct:.1f}%")
    replace_text_in_shape(slide8, "(28 Avaliações)", f"({login_count} Avaliações)")
    replace_text_in_shape(slide8, "1.79/5", f"{login_severity:.2f}/5")

# Salvar apresentação atualizada
output_file = "Documentos/Correlação Funcional de Feedbacks em Apps Bancários v2 - ATUALIZADA.pptx"
prs.save(output_file)

print(f"\n✓ Apresentação atualizada salva em: {output_file}")
print("\nResumo das atualizações:")
print(f"  - Dataset validado: {total} avaliações classificadas manualmente")
print(f"  - Avaliações negativas: {neg} ({neg/total*100:.1f}%)")
print(f"  - Categorias funcionais: {total_categories}")
print(f"  - Top 3 problemas atualizados com dados reais")
print(f"  - Método e modelo detalhados no Slide 5")
print(f"  - Métricas com base humana adicionadas no Slide 6")
print(f"  - Backlog priorizado atualizado no Slide 7")

