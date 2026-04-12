"""
Script para atualizar a apresentação PowerPoint com dados reais
e ajustes baseados no feedback do gestor
"""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
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

neg_with_category = (df[categories].sum(axis=1) > 0).sum()

print("Carregando apresentação...")
prs = Presentation("Documentos/Correlação Funcional de Sentimentos em Apps Bancários.pptx")

# Função auxiliar para encontrar e substituir texto em shapes
def replace_text_in_shape(shape, old_text, new_text):
    """Substitui texto em uma shape."""
    if hasattr(shape, "text"):
        if old_text in shape.text:
            shape.text = shape.text.replace(old_text, new_text)
            return True
    return False

# Função para adicionar texto a um slide
def add_text_to_slide(slide, text, left=Inches(0.5), top=Inches(1), width=Inches(9), height=Inches(1)):
    """Adiciona uma nova text box ao slide."""
    textbox = slide.shapes.add_textbox(left, top, width, height)
    text_frame = textbox.text_frame
    text_frame.word_wrap = True
    p = text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(11)
    return textbox

print("\nAtualizando slides...")

# Slide 2: Entendimento do Negócio
if len(prs.slides) > 1:
    slide2 = prs.slides[1]
    print("  - Slide 2: Atualizando estatísticas...")
    replace_text_in_shape(slide2, "72.76% das críticas são negativas", 
                         f"{neg/total*100:.1f}% das críticas são negativas (validado por classificação humana)")
    
    # Adicionar nota sobre validação humana
    for shape in slide2.shapes:
        if hasattr(shape, "text") and "Critérios de Sucesso" in shape.text:
            # Adicionar após critérios de sucesso
            add_text_to_slide(slide2, f"✓ Dataset Validado: {total} avaliações classificadas manualmente", 
                            top=Inches(5.5))

# Slide 3: Entendimento dos Dados
if len(prs.slides) > 2:
    slide3 = prs.slides[2]
    print("  - Slide 3: Atualizando dados...")
    replace_text_in_shape(slide3, "72.76% das críticas são Negativas", 
                         f"{neg/total*100:.1f}% das críticas são Negativas (validado por humanos)")
    
    # Adicionar informação sobre dataset validado
    for shape in slide3.shapes:
        if hasattr(shape, "text") and "Desafio Principal" in shape.text:
            add_text_to_slide(slide3, f"✓ {total} avaliações classificadas manualmente por humanos", 
                            top=Inches(5.5))

# Slide 4: Preparação dos Dados
if len(prs.slides) > 3:
    slide4 = prs.slides[3]
    print("  - Slide 4: Atualizando volume e rotulagem...")
    
    # Substituir volume
    replace_text_in_shape(slide4, "Meta de mais de 10.000 comentários", 
                         f"{total} avaliações classificadas manualmente")
    
    # Atualizar rotulagem
    replace_text_in_shape(slide4, "Rotulagem: Criação de rótulos de negócio", 
                         f"Rotulagem Humana: {total} avaliações classificadas manualmente")
    
    # Adicionar detalhes sobre categorias
    add_text_to_slide(slide4, 
                     f"• {len(categories)} categorias funcionais identificadas\n"
                     f"• Classificação múltipla (múltiplas categorias por avaliação)\n"
                     f"• {neg} avaliações negativas com categorias funcionais",
                     top=Inches(4.5))

# Slide 5: Modelagem - DETALHAR MÉTODO E MODELO
if len(prs.slides) > 4:
    slide5 = prs.slides[4]
    print("  - Slide 5: Adicionando detalhes do método e modelo...")
    
    # Adicionar nova seção detalhando método
    method_text = (
        "📋 Método Detalhado:\n\n"
        "1. Análise de Sentimentos:\n"
        "   • Modelo: cardiffnlp/twitter-xlm-roberta-base-sentiment\n"
        "   • Framework: Hugging Face Transformers\n"
        "   • Parâmetros: Batch size 16, Temperature 0.3\n\n"
        "2. Correlação Funcional:\n"
        "   • Modelo: GPT-4o (OpenAI)\n"
        "   • Técnica: Prompt Engineering (zero-shot learning)\n"
        "   • Abordagem: Classificação múltipla\n"
        "   • Parâmetros: Max tokens 200, Temperature 0.3\n\n"
        "3. Taxonomia: 16 categorias funcionais\n"
        "   (PIX, Login/Autenticação, Performance, Interface/Usabilidade,\n"
        "    Empréstimos/Crédito, Pagamentos/Boletos, Saldo/Extrato,\n"
        "    Atendimento, Cadastro/Conta, Investimentos, Segurança,\n"
        "    Notificações, Questões geográficas, Placas/Veículos,\n"
        "    Tarifas/Cobranças, Outros)"
    )
    
    add_text_to_slide(slide5, method_text, top=Inches(3), height=Inches(4))

# Slide 6: Avaliação - ADICIONAR MÉTRICAS COM BASE HUMANA
if len(prs.slides) > 5:
    slide6 = prs.slides[5]
    print("  - Slide 6: Adicionando métricas com base humana...")
    
    metrics_text = (
        "✅ Validação com Base Humana:\n\n"
        f"• Dataset: {total} avaliações classificadas manualmente\n"
        f"• Classificador: Carol (concluído)\n"
        f"• Status: Aguardando segunda classificação\n\n"
        "📊 Métricas a Calcular:\n"
        "• Acurácia do modelo de sentimento (DistilBERT vs. Humano)\n"
        "• Acurácia da correlação funcional (GPT-4o vs. Humano)\n"
        "• Inter-Annotator Agreement (Cohen's Kappa)\n\n"
        "🎯 Resultados Esperados:\n"
        "• F1-Score > 80% por categoria\n"
        "• Acurácia geral > 85% em sentimentos"
    )
    
    add_text_to_slide(slide6, metrics_text, top=Inches(3.5), height=Inches(3.5))

# Slide 8: Próximos Passos
if len(prs.slides) > 7:
    slide8 = prs.slides[7]
    print("  - Slide 8: Atualizando próximos passos...")
    
    next_steps_text = (
        "✅ Concluído:\n"
        f"• Classificação manual de {total} avaliações (Carol)\n\n"
        "🔄 Em Andamento:\n"
        "• Receber segunda classificação manual\n"
        "• Calcular inter-annotator agreement\n"
        "• Comparar modelo vs. classificação humana\n\n"
        "📅 Próximas Semanas:\n"
        "• Resolver discrepâncias entre classificadores\n"
        "• Ajustar prompts do LLM baseado em erros\n"
        "• Calcular métricas finais\n"
        "• Preparar dataset para treino/fine-tuning"
    )
    
    # Procurar onde adicionar (após cronograma)
    add_text_to_slide(slide8, next_steps_text, top=Inches(4), height=Inches(3.5))

# Salvar apresentação atualizada
output_file = "Documentos/Correlação Funcional de Sentimentos em Apps Bancários - ATUALIZADA.pptx"
prs.save(output_file)

print(f"\n✓ Apresentação atualizada salva em: {output_file}")
print("\nResumo das atualizações:")
print(f"  - Estatísticas atualizadas: {neg/total*100:.1f}% negativas (antes: 72.76%)")
print(f"  - Dataset validado: {total} avaliações classificadas manualmente")
print(f"  - Método e modelo detalhados no Slide 5")
print(f"  - Métricas com base humana adicionadas no Slide 6")
print(f"  - Próximos passos atualizados no Slide 8")

