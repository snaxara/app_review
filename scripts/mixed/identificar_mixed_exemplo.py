"""
Script para identificar se o exemplo fornecido pelo usuário é mixed
e demonstrar como funciona
"""

from openai import OpenAI
import os

# Carregar variáveis de ambiente
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Inicializar cliente OpenAI
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

exemplo = "Pra entrar no aplicativo tem que assistir uma novela mexicana, demora demaisssssss as vezes precisamos fazer algo rápido como passar um pix e tem uma introdução enorme antes de entrar, fora isso as configurações e a caixinha de rendimento são ótimas !"

def identificar_sentimento_mixed(review_text):
    """Identifica sentimento incluindo mixed."""
    
    prompt = f"""Analise a seguinte avaliação de app bancário e determine o sentimento.

OPÇÕES:
- POSITIVE: Apenas aspectos positivos (elogios, satisfação)
- NEGATIVE: Apenas aspectos negativos (reclamações, problemas)
- NEUTRAL: Sem polaridade clara, informativo
- MIXED: Aspectos positivos E negativos simultaneamente na mesma avaliação

Uma avaliação é MISTA quando menciona problemas/insatisfações E elogios/satisfações ao mesmo tempo.

Exemplos:
- "App lento mas interface boa" = MIXED
- "Não gostei" = NEGATIVE
- "Ótimo app" = POSITIVE
- "OK" = NEUTRAL

Avaliação: "{review_text}"

Responda APENAS com: POSITIVE, NEGATIVE, NEUTRAL ou MIXED"""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você é um especialista em análise de sentimentos de avaliações de apps bancários."},
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
        print(f"Erro: {e}")
        return 'unknown'

def categorizar_funcionalidades(review_text):
    """Categoriza funcionalidades mencionadas (pode ter positivas e negativas)."""
    
    prompt = f"""Categorize a avaliação em TODAS as categorias funcionais mencionadas.
Se menciona problemas, marque as categorias dos problemas.
Se menciona elogios, marque as categorias dos elogios.

CATEGORIAS:
- PIX: Transferências PIX, chave PIX, QR Code
- Login/Autenticação: Acesso, senha, biometria, login
- Performance: Lentidão, travamentos, demora, não abre
- Interface/Usabilidade: Navegação, design, menu, confuso
- Investimentos: Aplicações, poupança, rendimento, caixinha
- Outros: Outras funcionalidades

Avaliação: "{review_text}"

Responda com lista separada por vírgulas das categorias. Se não mencionar funcionalidades específicas, responda "Nenhuma"."""

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Você categoriza avaliações de apps bancários."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=100
        )
        
        return response.choices[0].message.content.strip()
            
    except Exception as e:
        return f"Erro: {e}"

print("="*70)
print("ANÁLISE DO EXEMPLO FORNECIDO")
print("="*70)
print(f"\nAvaliação:\n{exemplo}\n")

sentimento = identificar_sentimento_mixed(exemplo)
print(f"Sentimento identificado: {sentimento.upper()}")

categorias = categorizar_funcionalidades(exemplo)
print(f"\nCategorias funcionais: {categorias}")

print("\n" + "="*70)
print("ANÁLISE DETALHADA")
print("="*70)

# Análise manual
aspectos_negativos = [
    "demora demais",
    "introdução enorme antes de entrar",
    "tem que assistir uma novela mexicana"
]

aspectos_positivos = [
    "configurações são ótimas",
    "caixinha de rendimento são ótimas"
]

print("\nAspectos NEGATIVOS identificados:")
for aspecto in aspectos_negativos:
    print(f"  - {aspecto}")

print("\nAspectos POSITIVOS identificados:")
for aspecto in aspectos_positivos:
    print(f"  - {aspecto}")

print("\n✓ Esta avaliação é MIXED porque contém aspectos positivos E negativos simultaneamente.")
print("✓ Categorias funcionais:")
print("  - Performance (lentidão, demora)")
print("  - Login/Autenticação (introdução antes de entrar)")
print("  - Investimentos (caixinha de rendimento - positivo)")

