"""
Script de Coleta de Dados - Google Play Store
TCC MBA Data Science USP/Esalq
Autora: Simone Rossetti Nobre Naxara

Saída padrão: app_review_dataset.csv (raiz do projeto), compatível com sentiment_analysis.py.

Nova rodada sem sobrescrever a anterior:
  python scripts/collect_reviews.py --days 7 --run v2
  → grava data/collections/v2/app_review_dataset.csv
"""

import argparse
import hashlib
import os
import time
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd
from google_play_scraper import Sort, reviews

# Configurações
APPS = {
    'Caixa': 'br.com.gabba.Caixa'
}

LANG = 'pt'
COUNTRY = 'br'
BATCH_SIZE = 200  # Tamanho do lote por requisição (máximo recomendado)
DEFAULT_DAYS_WINDOW = 15  # Padrão histórico do repositório; sobrescreva com --days ou DAYS_WINDOW

def collect_reviews(app_name, app_id, days_window: int):
    """Coleta avaliações dos últimos `days_window` dias (janela deslizante a partir de agora)."""
    print(f"Iniciando coleta para: {app_name} ({app_id})...")
    
    cutoff_date = datetime.now() - timedelta(days=days_window)
    all_reviews_data = []
    continuation_token = None
    batch_count = 0
    empty_batches = 0
    max_empty_batches = 3  # Para após 3 lotes vazios consecutivos
    
    print(f"  Coletando avaliações dos últimos {days_window} dias...")
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
                print(f"  Avaliações mais antigas que {days_window} dias encontradas. Parando coleta.")
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
    parser = argparse.ArgumentParser(description="Coleta avaliações da Google Play (Caixa).")
    parser.add_argument(
        "--days",
        type=int,
        default=int(os.environ.get("DAYS_WINDOW", DEFAULT_DAYS_WINDOW)),
        help=f"Janela deslizante em dias (padrão: {DEFAULT_DAYS_WINDOW} ou env DAYS_WINDOW).",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Caminho do CSV de saída (sobrescreve --run).",
    )
    parser.add_argument(
        "--run",
        type=str,
        default=None,
        help="Ex.: v2 → salva em data/collections/v2/app_review_dataset.csv sem tocar na raiz.",
    )
    args = parser.parse_args()
    days_window = args.days

    if args.output:
        output_file = Path(args.output)
    elif args.run:
        output_file = Path("data") / "collections" / args.run / "app_review_dataset.csv"
        output_file.parent.mkdir(parents=True, exist_ok=True)
    else:
        output_file = Path("app_review_dataset.csv")

    all_reviews = []
    
    for name, app_id in APPS.items():
        try:
            app_data = collect_reviews(name, app_id, days_window)
            all_reviews.extend(app_data)
            time.sleep(1) # Pausa respeitosa para não bloquear a API
        except Exception as e:
            print(f"Erro ao coletar {name}: {e}")

    # Criar DataFrame
    df = pd.DataFrame(all_reviews)
    if len(df) == 0 or "content" not in df.columns:
        print("Nenhuma avaliação coletada ou DataFrame inválido. Verifique a rede e o app_id.")
        return

    # Converter data para datetime e validar
    if 'date' in df.columns and len(df) > 0:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        
        # Remover linhas sem data válida
        initial_count = len(df)
        df = df[df['date'].notna()].copy()
        if initial_count != len(df):
            print(f"Removidas {initial_count - len(df)} avaliações sem data válida")
        
        # Filtrar por janela de dias (filtro adicional de segurança)
        cutoff_date = datetime.now() - timedelta(days=days_window)
        initial_count = len(df)
        df = df[df['date'] >= cutoff_date].copy()
        
        if initial_count != len(df):
            print(f"Filtro adicional: removidas {initial_count - len(df)} avaliações fora da janela de {days_window} dias")
    
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
    
    df.to_csv(output_file, index=False, sep=';', encoding='utf-8')
    print(f"\nArquivo gerado com sucesso: {output_file.resolve()}")

if __name__ == "__main__":
    main()