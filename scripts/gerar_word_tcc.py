#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para gerar arquivo Word formatado conforme normas USP/ESALQ
a partir do documento Markdown do TCC.
"""

import re
import os
from pathlib import Path

try:
    from docx import Document
    from docx.shared import Pt, Cm, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement
except ImportError:
    print("Instalando python-docx...")
    import subprocess
    subprocess.check_call(["pip", "install", "python-docx"])
    from docx import Document
    from docx.shared import Pt, Cm, Inches, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_LINE_SPACING
    from docx.enum.style import WD_STYLE_TYPE
    from docx.oxml.ns import qn
    from docx.oxml import OxmlElement


def add_page_number(doc):
    """Adiciona numeração de páginas no rodapé"""
    section = doc.sections[0]
    footer = section.footer
    
    paragraph = footer.paragraphs[0]
    paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    run = paragraph.add_run()
    fldChar1 = OxmlElement('w:fldChar')
    fldChar1.set(qn('w:fldCharType'), 'begin')
    
    instrText = OxmlElement('w:instrText')
    instrText.set(qn('xml:space'), 'preserve')
    instrText.text = 'PAGE'
    
    fldChar2 = OxmlElement('w:fldChar')
    fldChar2.set(qn('w:fldCharType'), 'end')
    
    run._element.append(fldChar1)
    run._element.append(instrText)
    run._element.append(fldChar2)


def setup_document_formatting(doc):
    """Configura formatação conforme normas USP/ESALQ"""
    # Configurar margens (3cm superior/inferior, 2cm esquerda/direita)
    sections = doc.sections
    for section in sections:
        section.top_margin = Cm(3)
        section.bottom_margin = Cm(3)
        section.left_margin = Cm(2)
        section.right_margin = Cm(2)
    
    # Configurar estilo Normal (Times New Roman 12pt, espaçamento 1,5)
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Times New Roman'
    font.size = Pt(12)
    paragraph_format = style.paragraph_format
    paragraph_format.line_spacing_rule = WD_LINE_SPACING.MULTIPLE
    paragraph_format.line_spacing = 1.5
    paragraph_format.space_after = Pt(0)
    
    # Criar estilo para títulos de seção
    try:
        heading_style = doc.styles['Heading 1']
    except:
        heading_style = doc.styles.add_style('Heading 1', WD_STYLE_TYPE.PARAGRAPH)
    
    heading_font = heading_style.font
    heading_font.name = 'Times New Roman'
    heading_font.size = Pt(12)
    heading_font.bold = True
    heading_format = heading_style.paragraph_format
    heading_format.space_before = Pt(12)
    heading_format.space_after = Pt(6)
    heading_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Criar estilo para subtítulos
    try:
        subheading_style = doc.styles['Heading 2']
    except:
        subheading_style = doc.styles.add_style('Heading 2', WD_STYLE_TYPE.PARAGRAPH)
    
    subheading_font = subheading_style.font
    subheading_font.name = 'Times New Roman'
    subheading_font.size = Pt(12)
    subheading_font.bold = True
    subheading_format = subheading_style.paragraph_format
    subheading_format.space_before = Pt(12)
    subheading_format.space_after = Pt(6)
    subheading_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    
    # Criar estilo para título principal
    try:
        title_style = doc.styles['Title']
    except:
        title_style = doc.styles.add_style('Title', WD_STYLE_TYPE.PARAGRAPH)
    
    title_font = title_style.font
    title_font.name = 'Times New Roman'
    title_font.size = Pt(14)
    title_font.bold = True
    title_format = title_style.paragraph_format
    title_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
    title_format.space_after = Pt(12)


def parse_markdown_table(table_text):
    """Converte tabela markdown para lista de linhas"""
    lines = table_text.strip().split('\n')
    if len(lines) < 2:
        return None
    
    # Remover separador de cabeçalho
    data_lines = [line for line in lines if not re.match(r'^\|[\s:|-]+\|$', line)]
    
    rows = []
    for line in data_lines:
        if line.strip().startswith('|'):
            cells = [cell.strip() for cell in line.split('|')[1:-1]]
            rows.append(cells)
    
    return rows if rows else None


def process_markdown_to_word(md_file_path, output_path):
    """Processa arquivo Markdown e gera Word formatado"""
    
    with open(md_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    doc = Document()
    setup_document_formatting(doc)
    
    lines = content.split('\n')
    i = 0
    in_table = False
    table_lines = []
    current_table_title = None
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Pular linhas vazias excessivas
        if not line and i > 0 and lines[i-1].strip() == '':
            i += 1
            continue
        
        # Processar folha de rosto
        if 'Trabalho de Conclusão de Curso' in line and i < 5:
            p = doc.add_paragraph(line)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_format = p.paragraph_format
            p_format.space_after = Pt(12)
            i += 1
            continue
        
        # Processar título principal
        if line.startswith('# ') and not line.startswith('##'):
            title = line[2:].strip()
            p = doc.add_paragraph(title, style='Title')
            p_format = p.paragraph_format
            p_format.space_after = Pt(12)
            i += 1
            continue
        
        # Processar autores
        if 'Simone Rossetti' in line or 'Dra. Anna Carolina' in line:
            p = doc.add_paragraph(line)
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_format = p.paragraph_format
            p_format.space_after = Pt(6)
            i += 1
            continue
        
        # Processar seções principais (##)
        if line.startswith('## '):
            if in_table:
                # Finalizar tabela anterior se houver
                if table_lines:
                    rows = parse_markdown_table('\n'.join(table_lines))
                    if rows:
                        table = doc.add_table(rows=len(rows), cols=len(rows[0]))
                        # Usar estilo de tabela simples sem bordas laterais (conforme normas)
                        table.style = 'Table Grid'
                        
                        for row_idx, row_data in enumerate(rows):
                            for col_idx, cell_data in enumerate(row_data):
                                # Remover formatação markdown
                                cell_data = re.sub(r'\*\*(.*?)\*\*', r'\1', cell_data)
                                cell_data = cell_data.strip()
                                
                                # Limpar célula e adicionar texto
                                cell = table.rows[row_idx].cells[col_idx]
                                cell.text = cell_data
                                
                                # Formatação das células
                                cell_paragraph = cell.paragraphs[0]
                                cell_paragraph.paragraph_format.space_after = Pt(0)
                                cell_paragraph.paragraph_format.space_before = Pt(0)
                                
                                # Formatar fonte
                                for run in cell_paragraph.runs:
                                    run.font.name = 'Times New Roman'
                                    run.font.size = Pt(12)
                                
                                # Primeira linha em negrito (cabeçalho)
                                if row_idx == 0:
                                    for run in cell_paragraph.runs:
                                        run.font.bold = True
                        
                        # Adicionar título da tabela se houver
                        if current_table_title:
                            title_p = doc.paragraphs[-1].insert_paragraph_before(current_table_title)
                            title_p.style = 'Normal'
                            title_p.runs[0].font.bold = True
                            current_table_title = None
                
                in_table = False
                table_lines = []
            
            section_title = line[3:].strip()
            p = doc.add_paragraph(section_title, style='Heading 1')
            i += 1
            continue
        
        # Processar subtítulos (###)
        if line.startswith('### '):
            if in_table:
                if table_lines:
                    rows = parse_markdown_table('\n'.join(table_lines))
                    if rows:
                        table = doc.add_table(rows=len(rows), cols=len(rows[0]))
                        table.style = 'Light Grid Accent 1'
                        
                        for row_idx, row_data in enumerate(rows):
                            for col_idx, cell_data in enumerate(row_data):
                                cell_data = re.sub(r'\*\*(.*?)\*\*', r'\1', cell_data)
                                table.rows[row_idx].cells[col_idx].text = cell_data
                                
                                cell_paragraph = table.rows[row_idx].cells[col_idx].paragraphs[0]
                                cell_paragraph.paragraph_format.space_after = Pt(0)
                                cell_run = cell_paragraph.runs[0] if cell_paragraph.runs else cell_paragraph.add_run(cell_data)
                                cell_run.font.name = 'Times New Roman'
                                cell_run.font.size = Pt(12)
                        
                        if current_table_title:
                            title_p = doc.paragraphs[-1].insert_paragraph_before(current_table_title)
                            title_p.style = 'Normal'
                            title_p.runs[0].font.bold = True
                            current_table_title = None
                
                in_table = False
                table_lines = []
            
            subtitle = line[4:].strip()
            p = doc.add_paragraph(subtitle, style='Heading 2')
            i += 1
            continue
        
        # Processar título de tabela/quadro
        if line.startswith('**Tabela') or line.startswith('**Quadro'):
            # Se já temos uma tabela em processamento, finalizar primeiro
            if in_table and table_lines:
                rows = parse_markdown_table('\n'.join(table_lines))
                if rows:
                    # Adicionar título antes da tabela
                    if current_table_title:
                        title_p = doc.add_paragraph(current_table_title)
                        title_p.style = 'Normal'
                        title_p.runs[0].font.bold = True
                        title_p_format = title_p.paragraph_format
                        title_p_format.space_after = Pt(6)
                    
                    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
                    table.style = 'Table Grid'
                    
                    for row_idx, row_data in enumerate(rows):
                        for col_idx, cell_data in enumerate(row_data):
                            cell_data = re.sub(r'\*\*(.*?)\*\*', r'\1', cell_data)
                            cell_data = cell_data.strip()
                            
                            cell = table.rows[row_idx].cells[col_idx]
                            cell.text = cell_data
                            
                            cell_paragraph = cell.paragraphs[0]
                            cell_paragraph.paragraph_format.space_after = Pt(0)
                            cell_paragraph.paragraph_format.space_before = Pt(0)
                            
                            for run in cell_paragraph.runs:
                                run.font.name = 'Times New Roman'
                                run.font.size = Pt(12)
                            
                            if row_idx == 0:
                                for run in cell_paragraph.runs:
                                    run.font.bold = True
                    
                    current_table_title = None
                    in_table = False
                    table_lines = []
            
            # Armazenar novo título
            current_table_title = line.replace('**', '').strip()
            i += 1
            continue
        
        # Processar título de figura
        if line.startswith('**Figura') or line.startswith('**Quadro'):
            # Adicionar título da figura
            p = doc.add_paragraph(line.replace('**', '').strip())
            p_format = p.paragraph_format
            p_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_format.space_before = Pt(6)
            p_format.space_after = Pt(6)
            p.runs[0].font.bold = True
            
            # Adicionar espaço para imagem (será inserida manualmente)
            p_img = doc.add_paragraph('[IMAGEM A SER INSERIDA]')
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img_format = p_img.paragraph_format
            p_img_format.space_after = Pt(6)
            p_img.runs[0].font.italic = True
            p_img.runs[0].font.color.rgb = RGBColor(128, 128, 128)
            
            i += 1
            continue
        
        # Processar fonte de tabela/figura
        if line.startswith('Fonte:'):
            # Se temos tabela em processamento, finalizar primeiro
            if in_table and table_lines:
                rows = parse_markdown_table('\n'.join(table_lines))
                if rows:
                    if current_table_title:
                        title_p = doc.add_paragraph(current_table_title)
                        title_p.style = 'Normal'
                        title_p.runs[0].font.bold = True
                        title_p_format = title_p.paragraph_format
                        title_p_format.space_after = Pt(6)
                    
                    table = doc.add_table(rows=len(rows), cols=len(rows[0]))
                    table.style = 'Table Grid'
                    
                    for row_idx, row_data in enumerate(rows):
                        for col_idx, cell_data in enumerate(row_data):
                            cell_data = re.sub(r'\*\*(.*?)\*\*', r'\1', cell_data)
                            cell_data = cell_data.strip()
                            
                            cell = table.rows[row_idx].cells[col_idx]
                            cell.text = cell_data
                            
                            cell_paragraph = cell.paragraphs[0]
                            cell_paragraph.paragraph_format.space_after = Pt(0)
                            cell_paragraph.paragraph_format.space_before = Pt(0)
                            
                            for run in cell_paragraph.runs:
                                run.font.name = 'Times New Roman'
                                run.font.size = Pt(12)
                            
                            if row_idx == 0:
                                for run in cell_paragraph.runs:
                                    run.font.bold = True
                    
                    current_table_title = None
                    in_table = False
                    table_lines = []
            
            # Adicionar fonte
            p = doc.add_paragraph(line)
            p_format = p.paragraph_format
            p_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_format.space_after = Pt(12)
            p.runs[0].font.size = Pt(10)
            p.runs[0].font.italic = True
            i += 1
            continue
        
        # Processar tabelas markdown
        if line.startswith('|'):
            if '---' in line or re.match(r'^\|[\s:|-]+\|$', line):
                # Separador de tabela - pular
                i += 1
                continue
            else:
                # Linha de dados da tabela
                if not in_table:
                    in_table = True
                    table_lines = []
                table_lines.append(line)
                i += 1
                continue
        
        # Processar código/quadro (com bordas)
        if line.startswith('```'):
            # Verificar se há título de quadro antes
            quadro_title = None
            if i > 0 and lines[i-1].strip().startswith('**Quadro'):
                quadro_title = lines[i-1].strip().replace('**', '').strip()
            
            # Pular linha de abertura
            i += 1
            code_lines = []
            while i < len(lines) and not lines[i].strip().startswith('```'):
                code_lines.append(lines[i])
                i += 1
            # Pular linha de fechamento
            i += 1
            
            # Adicionar título do quadro se houver
            if quadro_title:
                title_p = doc.add_paragraph(quadro_title)
                title_p.style = 'Normal'
                title_p.runs[0].font.bold = True
                title_p_format = title_p.paragraph_format
                title_p_format.space_after = Pt(6)
            
            # Adicionar código como texto formatado em caixa (quadro)
            if code_lines:
                code_text = '\n'.join(code_lines)
                p = doc.add_paragraph(code_text)
                p_format = p.paragraph_format
                p_format.left_indent = Cm(0.5)
                p_format.right_indent = Cm(0.5)
                p_format.space_before = Pt(6)
                p_format.space_after = Pt(6)
                
                # Adicionar borda ao parágrafo (simulando quadro)
                pPr = p._element.get_or_add_pPr()
                pBdr = OxmlElement('w:pBdr')
                for side in ['top', 'left', 'bottom', 'right']:
                    border = OxmlElement(f'w:{side}')
                    border.set(qn('w:val'), 'single')
                    border.set(qn('w:sz'), '4')
                    border.set(qn('w:space'), '1')
                    border.set(qn('w:color'), '000000')
                    pBdr.append(border)
                pPr.append(pBdr)
                
                for run in p.runs:
                    run.font.name = 'Courier New'
                    run.font.size = Pt(10)
            
            # Verificar se há fonte após o código
            if i < len(lines) and lines[i].strip().startswith('Fonte:'):
                fonte_line = lines[i].strip()
                p_fonte = doc.add_paragraph(fonte_line)
                p_fonte_format = p_fonte.paragraph_format
                p_fonte_format.alignment = WD_ALIGN_PARAGRAPH.CENTER
                p_fonte_format.space_after = Pt(12)
                p_fonte.runs[0].font.size = Pt(10)
                p_fonte.runs[0].font.italic = True
                i += 1
            continue
        
        # Processar listas
        if line.startswith('- ') or line.startswith('* '):
            text = line[2:].strip()
            # Remover formatação markdown
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            p = doc.add_paragraph(text, style='List Bullet')
            p_format = p.paragraph_format
            p_format.left_indent = Cm(1)
            p_format.space_after = Pt(0)
            i += 1
            continue
        
        # Processar listas numeradas
        if re.match(r'^\d+\.\s', line):
            text = re.sub(r'^\d+\.\s', '', line)
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            p = doc.add_paragraph(text, style='List Number')
            p_format = p.paragraph_format
            p_format.left_indent = Cm(1)
            p_format.space_after = Pt(0)
            i += 1
            continue
        
        # Processar texto normal
        if line and not line.startswith('---') and not line.startswith('!['):
            # Remover formatação markdown
            text = line
            text = re.sub(r'\*\*(.*?)\*\*', r'\1', text)
            text = re.sub(r'\*(.*?)\*', r'\1', text)
            text = re.sub(r'`(.*?)`', r'\1', text)
            
            # Processar citações
            if text.startswith('> '):
                text = text[2:]
                p = doc.add_paragraph(text)
                p_format = p.paragraph_format
                p_format.left_indent = Cm(1)
                p_format.space_after = Pt(6)
                p.runs[0].font.italic = True
            else:
                p = doc.add_paragraph(text)
                p_format = p.paragraph_format
                p_format.space_after = Pt(6)
            
            i += 1
            continue
        
        # Processar imagens (apenas referência)
        if line.startswith('!['):
            # Já processado junto com título de figura
            i += 1
            continue
        
        i += 1
    
    # Finalizar última tabela se houver
    if in_table and table_lines:
        rows = parse_markdown_table('\n'.join(table_lines))
        if rows:
            # Adicionar título antes da tabela
            if current_table_title:
                title_p = doc.add_paragraph(current_table_title)
                title_p.style = 'Normal'
                title_p.runs[0].font.bold = True
                title_p_format = title_p.paragraph_format
                title_p_format.space_after = Pt(6)
            
            table = doc.add_table(rows=len(rows), cols=len(rows[0]))
            table.style = 'Table Grid'
            
            for row_idx, row_data in enumerate(rows):
                for col_idx, cell_data in enumerate(row_data):
                    cell_data = re.sub(r'\*\*(.*?)\*\*', r'\1', cell_data)
                    cell_data = cell_data.strip()
                    
                    cell = table.rows[row_idx].cells[col_idx]
                    cell.text = cell_data
                    
                    cell_paragraph = cell.paragraphs[0]
                    cell_paragraph.paragraph_format.space_after = Pt(0)
                    cell_paragraph.paragraph_format.space_before = Pt(0)
                    
                    for run in cell_paragraph.runs:
                        run.font.name = 'Times New Roman'
                        run.font.size = Pt(12)
                    
                    if row_idx == 0:
                        for run in cell_paragraph.runs:
                            run.font.bold = True
    
    # Adicionar numeração de páginas
    add_page_number(doc)
    
    # Salvar documento
    doc.save(output_path)
    print(f"Documento Word gerado com sucesso: {output_path}")


if __name__ == '__main__':
    # Caminhos
    base_dir = Path(__file__).parent.parent
    md_file = base_dir / 'Documentos' / 'TCC_COMPLETO_ATUALIZADO.md'
    output_file = base_dir / 'Documentos' / 'TCC_FORMATADO_USP_ESALQ.docx'
    
    if not md_file.exists():
        print(f"Erro: Arquivo não encontrado: {md_file}")
        exit(1)
    
    print(f"Processando: {md_file}")
    print(f"Gerando: {output_file}")
    
    process_markdown_to_word(md_file, output_file)
    
    print("\nFormatação aplicada:")
    print("- Fonte: Times New Roman 12pt")
    print("- Espaçamento: 1,5 entre linhas")
    print("- Margens: 3cm superior/inferior, 2cm esquerda/direita")
    print("- Numeração de páginas no rodapé")
    print("- Títulos formatados conforme normas")
    print("\nIMPORTANTE: As imagens precisam ser inseridas manualmente no Word.")
    print("Os locais estão marcados com '[IMAGEM A SER INSERIDA]'.")
