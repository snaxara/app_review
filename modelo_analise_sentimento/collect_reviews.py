"""
Script de Coleta de Dados - Google Play Store
TCC MBA Data Science USP/Esalq
Autora: Simone Rossetti Nobre Naxara

Preferir a cópia mantida em `scripts/collect_reviews.py` (CLI com --days e --run).
Esta pasta pode ficar desatualizada em relação à raiz do projeto.
"""

import pandas as pd
from google_play_scraper import Sort, reviews
from datetime import datetime, timedelta
import time
import hashlib

# Configurações
APPS = {
    'Caixa': 'br.com.gabba.Caixa'
}

LANG = 'pt'
COUNTRY = 'br'
BATCH_SIZE = 200 # Tamanho do lote por requisição (máximo recomendado)
DAYS_WINDOW = 15 # Janela de dias para coletar avaliações

def collect_reviews(app_name, app_id):
    """Coleta todas as avaliações dos últimos DAYS_WINDOW dias usando paginação."""
    print(f"Iniciando coleta para: {app_name} ({app_id})...")
    
    cutoff_date = datetime.now() - timedelta(days=DAYS_WINDOW)
    all_reviews_data = []
    continuation_token = None
    batch_count = 0
    empty_batches = 0
    max_empty_batches = 3  # Para após 3 lotes vazios consecutivos
    
    print(f"  Coletando avaliações dos últimos {DAYS_WINDOW} dias...")
    print(f"  Data de corte: {cutoff_date.strftime('%d/%m/%Y %H:%M')}")
    
    while True:
        try:
            # Fazer requisição com ou sem continuation_token
            if continuation_token:
                result, continuation_token = reviews(
                    app_id,
                    lang=LANG,
                    country=COUNTRY,
                    sort=Sort.NEWEST,
                    count=BATCH_SIZE,
                    continuation_token=continuation_token
                )
            else:
                result, continuation_token = reviews(
                    app_id,
                    lang=LANG,
                    country=COUNTRY,
                    sort=Sort.NEWEST,
                    count=BATCH_SIZE
                )
            
            # Se não há resultado, para
            if not result:
                print(f"  Nenhum resultado retornado. Parando coleta.")
                break
            
            # Converter avaliações e verificar datas
            batch_reviews = []
            oldest_date_in_batch = None
            found_outside_window = False
            
            for r in result:
                review_date = r['at']
                
                # Se a avaliação está dentro da janela, adiciona
                if review_date >= cutoff_date:
                    # Garantir que versão não seja None ou vazio
                    version = r.get('reviewCreatedVersion') or r.get('appVersion') or 'N/A'
                    if version is None or str(version).strip() == '':
                        version = 'N/A'
                    
                    # Gerar ID único baseado em hash do conteúdo + data para garantir unicidade
                    review_id_string = f"{r['content']}_{review_date}_{app_name}"
                    review_id = hashlib.md5(review_id_string.encode('utf-8')).hexdigest()
                    
                    batch_reviews.append({
                        'reviewId': review_id,
                        'content': r['content'],
                        'score': r['score'],
                        'date': review_date,
                        'version': str(version).strip(),
                        'app_name': app_name
                    })
                    
                    if oldest_date_in_batch is None or review_date < oldest_date_in_batch:
                        oldest_date_in_batch = review_date
                else:
                    # Se encontrou avaliação fora da janela, marca para parar
                    # (pois está ordenado por mais recentes)
                    found_outside_window = True
                    break
            
            # Se encontrou avaliação fora da janela, para
            if found_outside_window:
                print(f"  Avaliações mais antigas que {DAYS_WINDOW} dias encontradas. Parando coleta.")
                break
            
            # Se não coletou nenhuma avaliação neste lote
            if len(batch_reviews) == 0:
                empty_batches += 1
                if empty_batches >= max_empty_batches:
                    print(f"  {max_empty_batches} lotes vazios consecutivos. Parando coleta.")
                    break
            else:
                empty_batches = 0  # Reset contador se coletou algo
                all_reviews_data.extend(batch_reviews)
            
            batch_count += 1
            
            if len(batch_reviews) > 0:
                print(f"  Lote {batch_count}: {len(batch_reviews)} avaliações coletadas (total: {len(all_reviews_data)})")
            
            # Se não há mais continuation_token, para
            if not continuation_token:
                print(f"  Não há mais páginas disponíveis. Parando coleta.")
                break
            
            # Pausa entre requisições para não sobrecarregar
            time.sleep(0.5)
            
        except KeyboardInterrupt:
            print(f"\n  Coleta interrompida pelo usuário.")
            break
        except Exception as e:
            print(f"  Erro ao coletar lote {batch_count + 1}: {e}")
            break
    
    print(f"  Total coletado: {len(all_reviews_data)} avaliações em {batch_count} lotes")
    return all_reviews_data

def main():
    all_reviews = []
    
    for name, app_id in APPS.items():
        try:
            app_data = collect_reviews(name, app_id)
            all_reviews.extend(app_data)
            time.sleep(1) # Pausa respeitosa para não bloquear a API
        except Exception as e:
            print(f"Erro ao coletar {name}: {e}")

    # Criar DataFrame
    df = pd.DataFrame(all_reviews)
    
    # Converter data para datetime e validar
    if 'date' in df.columns and len(df) > 0:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Remover linhas sem data válida
        initial_count = len(df)
        df = df[df['date'].notna()].copy()
        if initial_count != len(df):
            print(f"Removidas {initial_count - len(df)} avaliações sem data válida")
        
        # Filtrar por janela de dias (filtro adicional de segurança)
        cutoff_date = datetime.now() - timedelta(days=DAYS_WINDOW)
        initial_count = len(df)
        df = df[df['date'] >= cutoff_date].copy()
        
        if initial_count != len(df):
            print(f"Filtro adicional: removidas {initial_count - len(df)} avaliações fora da janela de {DAYS_WINDOW} dias")
    
    # Garantir que todas as linhas tenham versão
    if 'version' in df.columns:
        df['version'] = df['version'].fillna('N/A')
        df['version'] = df['version'].astype(str).str.strip()
        df.loc[df['version'] == '', 'version'] = 'N/A'
    
    # Filtragem básica (Remove vazios)
    print("Aplicando limpeza básica...")
    initial_len = len(df)
    df = df.dropna(subset=['content'])
    df = df[df['content'].str.strip().str.len() > 3] # Remove comentários muito curtos (ex: "bom", "ok")
    
    print(f"Total final de registros: {len(df)} (Removidos: {initial_len - len(df)})")
    
    # Mostrar período coberto
    if 'date' in df.columns and len(df) > 0:
        min_date = df['date'].min()
        max_date = df['date'].max()
        print(f"Período coberto: {min_date.strftime('%d/%m/%Y')} a {max_date.strftime('%d/%m/%Y')}")
    
    # Verificar se todas as linhas têm data e versão
    if len(df) > 0:
        missing_date = df['date'].isna().sum()
        missing_version = (df['version'].isna() | (df['version'] == 'N/A')).sum()
        
        if missing_date > 0:
            print(f"AVISO: {missing_date} avaliações sem data válida")
        if missing_version > 0:
            print(f"AVISO: {missing_version} avaliações sem versão (marcadas como 'N/A')")
        
        print(f"\nEstatísticas finais:")
        print(f"  Total de avaliações: {len(df)}")
        print(f"  Com data válida: {len(df) - missing_date}")
        print(f"  Com versão: {len(df) - missing_version}")
    
    # Salvar para uso no sentiment_analysis.py
    # O arquivo de saída terá as colunas que seu outro script espera
    output_file = 'app_review_dataset.csv'
    df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(f"\nArquivo gerado com sucesso: {output_file}")

if __name__ == "__main__":
    main()