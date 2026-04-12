"""
Script para corrigir encoding de arquivo CSV sem reprocessar

Corrige caracteres especiais que aparecem malformados no Excel
e salva o arquivo com UTF-8 com BOM (compatível com Excel).

Uso:
    python scripts/fix_csv_encoding.py
"""

import pandas as pd
import os

def detect_separator(filepath):
    """Detecta o separador do CSV."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        semicolon_count = first_line.count(';')
        comma_count = first_line.count(',')
        return ';' if semicolon_count > comma_count else ','
    except Exception:
        return ';'

def fix_encoding(text):
    """Corrige problemas de encoding em texto."""
    if pd.isna(text):
        return ""
    
    text = str(text)
    
    # Se o texto já está correto, retornar como está
    # Verificar se há caracteres malformados comuns (encoding duplo)
    if 'Ã§' in text or 'Ã£' in text or 'Ã¡' in text or 'Ã©' in text:
        # Tentar corrigir encoding duplo (UTF-8 interpretado como Latin-1)
        try:
            # Se foi salvo como UTF-8 mas lido como Latin-1, precisa re-encode
            text_bytes = text.encode('latin-1', errors='ignore')
            text = text_bytes.decode('utf-8', errors='ignore')
        except:
            # Se não funcionar, tentar outras correções
            pass
    
    # Garantir que está em UTF-8 válido
    try:
        text.encode('utf-8')
    except:
        # Se não conseguir codificar, tentar corrigir
        text = text.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
    
    return text

def fix_csv_encoding(input_file, output_file=None):
    """Corrige encoding de um arquivo CSV."""
    if output_file is None:
        output_file = input_file
    
    print(f"Corrigindo encoding do arquivo: {input_file}")
    
    if not os.path.exists(input_file):
        print(f"ERRO: Arquivo não encontrado: {input_file}")
        return False
    
    # Detectar separador
    separator = detect_separator(input_file)
    print(f"Separador detectado: {separator}")
    
    # Ler arquivo tentando diferentes encodings
    df = None
    encodings = ['utf-8-sig', 'utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            df = pd.read_csv(
                input_file,
                sep=separator,
                encoding=encoding,
                on_bad_lines='skip',
                quotechar='"',
                low_memory=False
            )
            print(f"Arquivo lido com encoding: {encoding}")
            
            # Verificar se os caracteres estão corretos
            if len(df) > 0 and 'content' in df.columns:
                sample = str(df['content'].iloc[0])
                # Se tem caracteres malformados, tentar corrigir
                if 'Ã§' in sample or 'Ã£' in sample:
                    # Tentar ler novamente como latin-1 e converter
                    try:
                        df_latin = pd.read_csv(
                            input_file,
                            sep=separator,
                            encoding='latin-1',
                            on_bad_lines='skip',
                            quotechar='"',
                            low_memory=False
                        )
                        # Converter colunas de texto
                        for col in df_latin.select_dtypes(include=['object']).columns:
                            df_latin[col] = df_latin[col].apply(
                                lambda x: x.encode('latin-1').decode('utf-8') if pd.notna(x) and isinstance(x, str) else x
                            )
                        df = df_latin
                        print(f"  Correção aplicada: encoding duplo corrigido")
                    except:
                        pass
            break
        except Exception as e:
            continue
    
    if df is None:
        print("ERRO: Não foi possível ler o arquivo com nenhum encoding")
        return False
    
    print(f"Total de linhas: {len(df)}")
    print(f"Colunas: {len(df.columns)}")
    
    # Corrigir encoding das colunas de texto
    text_columns = ['content']
    if 'content' in df.columns:
        print("\nCorrigindo encoding da coluna 'content'...")
        initial_sample = df['content'].iloc[0] if len(df) > 0 else ""
        print(f"  Antes (primeira linha): {str(initial_sample)[:80]}...")
        
        # Aplicar correção
        df['content'] = df['content'].apply(fix_encoding)
        
        final_sample = df['content'].iloc[0] if len(df) > 0 else ""
        print(f"  Depois (primeira linha): {str(final_sample)[:80]}...")
    
    # Verificar se há outras colunas de texto que precisam correção
    for col in df.columns:
        if df[col].dtype == 'object' and col not in text_columns:
            # Verificar se tem caracteres malformados
            sample = str(df[col].iloc[0]) if len(df) > 0 else ""
            if 'Ã' in sample or 'Ã§' in sample or 'Ã£' in sample:
                print(f"\nCorrigindo encoding da coluna '{col}'...")
                df[col] = df[col].apply(fix_encoding)
    
    # Salvar com UTF-8 com BOM (compatível com Excel)
    print(f"\nSalvando arquivo corrigido: {output_file}")
    print("  Encoding: UTF-8 com BOM (compatível com Excel)")
    
    # Salvar com UTF-8-BOM
    with open(output_file, 'w', encoding='utf-8-sig', newline='') as f:
        df.to_csv(f, index=False, sep=separator, lineterminator='\n')
    
    print(f"\nArquivo corrigido salvo: {output_file}")
    print(f"Total de linhas processadas: {len(df)}")
    
    return True

if __name__ == "__main__":
    import sys
    
    # Arquivo padrão
    input_file = 'functional_correlation_results.csv'
    
    # Permitir especificar arquivo via argumento
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    
    # Arquivo de saída (mesmo nome, sobrescreve)
    output_file = input_file
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    
    print("="*80)
    print("CORREÇÃO DE ENCODING DE ARQUIVO CSV")
    print("="*80)
    
    success = fix_csv_encoding(input_file, output_file)
    
    if success:
        print("\n" + "="*80)
        print("CORREÇÃO CONCLUÍDA")
        print("="*80)
        print("\nPróximos passos:")
        print("1. Abra o arquivo no Excel")
        print("2. Verifique se os caracteres estão corretos")
        print("3. Se ainda houver problemas, tente abrir com 'Dados > Obter Dados > De Texto/CSV'")
    else:
        print("\n" + "="*80)
        print("ERRO NA CORREÇÃO")
        print("="*80)
