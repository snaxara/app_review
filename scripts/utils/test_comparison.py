"""
Script de teste para verificar a comparação de avaliações já processadas
"""

import pandas as pd
import os

# Arquivos
SENTIMENT_CSV = 'sentiment_results.csv'
FUNCTIONAL_CSV = 'functional_correlation_results.csv'

print("="*60)
print("TESTE DE COMPARAÇÃO DE AVALIAÇÕES")
print("="*60)

# Carregar sentiment results
print("\n1. Carregando sentiment_results.csv...")
try:
    df_sent = pd.read_csv(SENTIMENT_CSV, sep=';', encoding='utf-8')
    print(f"   Total de avaliações: {len(df_sent)}")
    
    if 'sentiment_label' in df_sent.columns:
        negativas = df_sent[df_sent['sentiment_label'] == 'negative']
        print(f"   Avaliações negativas: {len(negativas)}")
    else:
        print("   ERRO: Coluna 'sentiment_label' não encontrada")
        negativas = df_sent
except Exception as e:
    print(f"   ERRO ao carregar: {e}")
    exit(1)

# Carregar functional results
print("\n2. Carregando functional_correlation_results.csv...")
if os.path.exists(FUNCTIONAL_CSV):
    try:
        # Detectar separador
        with open(FUNCTIONAL_CSV, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        
        semicolon_count = first_line.count(';')
        comma_count = first_line.count(',')
        
        if semicolon_count > comma_count:
            separator = ';'
            separator_name = 'ponto e vírgula'
        else:
            separator = ','
            separator_name = 'vírgula'
        
        df_func = pd.read_csv(FUNCTIONAL_CSV, sep=separator, encoding='utf-8')
        
        # Verificar se leitura foi bem-sucedida
        if len(df_func.columns) == 1:
            # Tentar outro separador
            other_sep = ',' if separator == ';' else ';'
            df_func = pd.read_csv(FUNCTIONAL_CSV, sep=other_sep, encoding='utf-8')
            separator_name = 'vírgula' if other_sep == ',' else 'ponto e vírgula'
        
        print(f"   Carregado com separador {separator_name}")
        print(f"   Número de colunas: {len(df_func.columns)}")
        
        print(f"   Total de avaliações processadas: {len(df_func)}")
        
        if 'content' in df_func.columns:
            print(f"   Tem coluna 'content': Sim")
        else:
            print(f"   ERRO: Coluna 'content' não encontrada")
            print(f"   Colunas disponíveis: {list(df_func.columns)[:10]}")
    except Exception as e:
        print(f"   ERRO ao carregar: {e}")
        df_func = None
else:
    print(f"   Arquivo não existe")
    df_func = None

# Comparar
if df_func is not None and 'content' in df_func.columns and 'content' in negativas.columns:
    print("\n3. Comparando avaliações...")
    
    # Normalizar conteúdo
    def normalize(text):
        if pd.isna(text):
            return ""
        return str(text).strip().lower()
    
    func_keys = set(df_func['content'].apply(normalize).unique())
    sent_keys = set(negativas['content'].apply(normalize).unique())
    
    print(f"   Chaves únicas em functional: {len(func_keys)}")
    print(f"   Chaves únicas em sentiment (negativas): {len(sent_keys)}")
    
    # Verificar interseção
    common = func_keys & sent_keys
    only_in_sent = sent_keys - func_keys
    
    print(f"\n   Avaliações em comum: {len(common)}")
    print(f"   Avaliações novas (só em sentiment): {len(only_in_sent)}")
    print(f"   Avaliações só em functional: {len(func_keys - sent_keys)}")
    
    if len(only_in_sent) > 0:
        print(f"\n   Exemplo de avaliações novas (primeiras 3):")
        for i, key in enumerate(list(only_in_sent)[:3]):
            print(f"     {i+1}. '{key[:80]}...'")
    
    print(f"\n4. CONCLUSÃO:")
    if len(only_in_sent) == 0:
        print("   OK: Todas as avaliações negativas já foram processadas!")
        print("   O script deve reutilizar os resultados existentes.")
    else:
        print(f"   ATENCAO: Há {len(only_in_sent)} avaliações novas para processar")
        print(f"   O script deve processar apenas essas {len(only_in_sent)} avaliações.")
else:
    print("\n3. Não foi possível comparar (arquivo não existe ou falta coluna 'content')")

print("\n" + "="*60)

