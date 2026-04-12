"""
Script para adicionar coluna 'mixed' aos datasets existentes
e identificar avaliações que têm aspectos positivos e negativos simultaneamente
"""

import pandas as pd
import argparse
from openai import OpenAI
import os

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def identify_mixed_sentiment(review_text):
    """Identifica se uma avaliação tem sentimento misto usando LLM."""
    
    prompt = f"""Analise a seguinte avaliação de app bancário e determine se ela contém aspectos POSITIVOS E NEGATIVOS simultaneamente.

Uma avaliação é MISTA (mixed) quando:
- Menciona problemas/insatisfações E elogios/satisfações na mesma avaliação
- Exemplo: "App lento mas interface boa" = MISTA
- Exemplo: "Não gostei" = NEGATIVA (apenas negativo)
- Exemplo: "Ótimo app" = POSITIVA (apenas positivo)

Avaliação: "{review_text}"

Responda APENAS com uma das opções:
- POSITIVE (apenas aspectos positivos)
- NEGATIVE (apenas aspectos negativos)
- NEUTRAL (sem polaridade clara)
- MIXED (aspectos positivos E negativos simultaneamente)"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de sentimentos de avaliações de apps."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=50
        )
        
        result = response.choices[0].message.content.strip().upper()
        
        # Normalizar resposta
        if 'MIXED' in result or 'MISTA' in result:
            return 'mixed'
        elif 'POSITIVE' in result or 'POSITIVO' in result:
            return 'positive'
        elif 'NEGATIVE' in result or 'NEGATIVO' in result:
            return 'negative'
        else:
            return 'neutral'
            
    except Exception as e:
        print(f"Erro ao processar: {e}")
        return 'neutral'

def add_mixed_column(input_file, output_file, sample_size=None):
    """Adiciona coluna mixed ao dataset."""
    
    print(f"Carregando {input_file}...")
    df = pd.read_csv(input_file, encoding='utf-8', sep=';')
    
    # Inicializar coluna mixed se não existir
    if 'mixed' not in df.columns:
        df['mixed'] = 0
    
    # Identificar avaliações que já têm positive=1 E negative=1 (já são mixed)
    already_mixed = (df['positive'] == 1) & (df['negative'] == 1)
    df.loc[already_mixed, 'mixed'] = 1
    
    print(f"✓ {already_mixed.sum()} avaliações já marcadas como mixed (positive=1 e negative=1)")
    
    # Para avaliações que não são claramente mixed, usar LLM para identificar
    # Filtrar avaliações que podem ser mixed (não são claramente apenas positive ou negative)
    potential_mixed = df[
        (df['mixed'] == 0) & 
        (df['positive'] == 0) & 
        (df['negative'] == 0) &
        (df['neutral'] == 0)
    ]
    
    if len(potential_mixed) > 0:
        print(f"\nVerificando {len(potential_mixed)} avaliações sem classificação clara...")
        
        # Se sample_size especificado, usar apenas uma amostra
        if sample_size and len(potential_mixed) > sample_size:
            potential_mixed = potential_mixed.sample(n=sample_size, random_state=42)
            print(f"  (Limitado a {sample_size} para teste)")
        
        for idx, row in potential_mixed.iterrows():
            sentiment = identify_mixed_sentiment(row['content'])
            if sentiment == 'mixed':
                df.loc[idx, 'mixed'] = 1
                print(f"  ✓ Identificado como mixed: {row['content'][:60]}...")
    
    # Salvar
    df.to_csv(output_file, index=False, encoding='utf-8-sig', sep=';')
    print(f"\n✓ Dataset atualizado salvo em: {output_file}")
    print(f"  Total de avaliações mixed: {df['mixed'].sum()}")
    
    return df

def main():
    parser = argparse.ArgumentParser(
        description='Adiciona coluna mixed ao dataset'
    )
    parser.add_argument(
        '--input',
        type=str,
        default='ground_truth_dataset.csv',
        help='Arquivo CSV de entrada'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=None,
        help='Arquivo CSV de saída (padrão: sobrescreve input)'
    )
    parser.add_argument(
        '--sample',
        type=int,
        default=None,
        help='Tamanho da amostra para verificação com LLM (opcional)'
    )
    
    args = parser.parse_args()
    
    output_file = args.output if args.output else args.input
    
    df = add_mixed_column(args.input, output_file, args.sample)
    
    print("\n" + "="*60)
    print("RESUMO")
    print("="*60)
    print(f"Total de avaliações: {len(df)}")
    print(f"  - Positive: {df['positive'].sum()}")
    print(f"  - Negative: {df['negative'].sum()}")
    print(f"  - Neutral: {df['neutral'].sum()}")
    print(f"  - Mixed: {df['mixed'].sum()}")

if __name__ == "__main__":
    main()

