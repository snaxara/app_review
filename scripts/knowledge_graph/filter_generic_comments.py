"""
Filtro de triagem para remover comentários genéricos sem informação útil
Evita processar comentários que não podem ser relacionados a BusinessCapability
"""

import re
from typing import List, Dict


# Padrões de comentários genéricos que não trazem informação útil
GENERIC_PATTERNS = [
    # Expressões genéricas de insatisfação
    r'^péssimo$',
    r'^péssima$',
    r'^horrível$',
    r'^horrivel$',
    r'^ruim$',
    r'^ruim demais$',
    r'^muito ruim$',
    r'^um lixo$',
    r'^uma porcaria$',
    r'^lixo$',
    r'^terrível$',
    r'^terrivel$',
    
    # Avaliações numéricas sem contexto
    r'^nota 0$',
    r'^nota zero$',
    r'^0 estrelas$',
    r'^zero estrelas$',
    r'^1 estrela$',
    
    # Comentários muito curtos e genéricos
    r'^precisa melhorar$',
    r'^melhorar$',
    r'^fujam$',
    r'^fujam desse banco$',
    r'^não recomendo$',
    r'^não recomendo$',
    r'^nunca mais$',
    r'^pior app$',
    r'^pior aplicativo$',
    
    # Apenas emojis ou pontuação
    r'^[!?\.]+$',
    r'^[😡👎💩🤮]+$',
]

# Palavras-chave que indicam comentário genérico (se for o único conteúdo significativo)
GENERIC_KEYWORDS = [
    'péssimo', 'péssima', 'horrível', 'horrivel', 'ruim', 'lixo', 'terrível', 'terrivel',
    'nota 0', 'nota zero', 'zero estrelas', '0 estrelas', '1 estrela',
    'precisa melhorar', 'fujam', 'não recomendo', 'nunca mais', 'pior app', 'pior aplicativo',
    'muito ruim', 'ruim demais', 'uma porcaria'
]

    # Comentários muito curtos (menos de 30 caracteres) são geralmente genéricos
    # A menos que mencionem funcionalidades específicas
MIN_LENGTH_THRESHOLD = 30

# Comentários que mencionam funcionalidades específicas são válidos
# NOTA: "app" e "aplicativo" NÃO estão aqui pois são genéricos demais
FUNCTIONALITY_KEYWORDS = [
    'pix', 'login', 'senha', 'transferência', 'transferencia', 'pagamento', 'boleto',
    'saldo', 'extrato', 'cartão', 'cartao', 'empréstimo', 'emprestimo', 'crédito', 'credito',
    'investimento', 'notificação', 'notificacao', 'atendimento', 'atendente', 'suporte',
    'cadastro', 'conta', 'versão', 'versao', 'atualização', 'atualizacao',
    'travou', 'travando', 'lento', 'lentidão', 'lentidao', 'erro', 'bug', 'problema',
    'segurança', 'seguranca', 'bloqueio', 'desbloqueio', 'biometria', 'token', 'chave',
    'wi-fi', 'wifi', 'internet', 'conexão', 'conexao', 'carregamento', 'carregando'
]


def is_generic_comment(content: str) -> bool:
    """
    Verifica se um comentário é genérico demais para processar no grafo.
    
    Um comentário é considerado genérico se:
    1. É muito curto (< 20 caracteres) E não menciona funcionalidades
    2. É apenas uma expressão genérica de insatisfação sem contexto
    3. Não menciona nenhuma funcionalidade específica do app
    
    Args:
        content: Texto do comentário
        
    Returns:
        True se o comentário é genérico (deve ser filtrado)
    """
    if not content or not isinstance(content, str):
        return True
    
    content_clean = content.strip().lower()
    
    # Remover pontuação excessiva e espaços múltiplos
    content_clean = re.sub(r'[!?\.]{2,}', '', content_clean)
    content_clean = re.sub(r'\s+', ' ', content_clean).strip()
    
    # Verificar padrões exatos genéricos
    for pattern in GENERIC_PATTERNS:
        if re.match(pattern, content_clean, re.IGNORECASE):
            return True
    
    # Se for muito curto, verificar se menciona funcionalidades
    if len(content_clean) < MIN_LENGTH_THRESHOLD:
        # Verificar se menciona alguma funcionalidade específica
        has_functionality = any(
            keyword in content_clean 
            for keyword in FUNCTIONALITY_KEYWORDS
        )
        
        # Verificar se contém apenas palavras genéricas
        is_only_generic = any(
            keyword in content_clean 
            for keyword in GENERIC_KEYWORDS
        )
        
        # Se não menciona funcionalidade OU é apenas palavras genéricas, filtrar
        if not has_functionality or (is_only_generic and not has_functionality):
            return True
    
    # Verificar se é apenas palavras genéricas sem contexto adicional
    words = content_clean.split()
    if len(words) <= 3:
        # Palavras genéricas comuns
        generic_words_list = ['péssimo', 'péssima', 'horrível', 'horrivel', 'ruim', 'lixo', 
                             'terrível', 'terrivel', 'nota', 'zero', 'um', 'uma', 'precisa',
                             'melhorar', 'fujam', 'não', 'recomendo', 'nunca', 'mais', 'pior']
        
        # Verificar se contém palavras genéricas
        has_generic = any(gen in content_clean for gen in generic_words_list)
        
        # Verificar se menciona funcionalidades específicas
        has_functionality = any(keyword in content_clean for keyword in FUNCTIONALITY_KEYWORDS)
        
        # Se tem palavra genérica mas não menciona funcionalidade específica, filtrar
        if has_generic and not has_functionality:
            return True
    
    # Se passou todas as verificações, não é genérico
    return False


def filter_generic_comments(df, content_column: str = 'content') -> tuple:
    """
    Filtra comentários genéricos de um DataFrame.
    
    Args:
        df: DataFrame com comentários
        content_column: Nome da coluna com o conteúdo
        
    Returns:
        Tuple (df_filtered, stats) onde:
        - df_filtered: DataFrame sem comentários genéricos
        - stats: Dicionário com estatísticas do filtro
    """
    if content_column not in df.columns:
        print(f"AVISO: Coluna '{content_column}' não encontrada!")
        return df, {'total': len(df), 'filtered': 0, 'remaining': len(df)}
    
    total = len(df)
    generic_mask = df[content_column].apply(is_generic_comment)
    filtered_count = generic_mask.sum()
    
    df_filtered = df[~generic_mask].copy()
    
    stats = {
        'total': total,
        'filtered': filtered_count,
        'remaining': len(df_filtered),
        'filter_percentage': (filtered_count / total * 100) if total > 0 else 0
    }
    
    return df_filtered, stats


if __name__ == "__main__":
    import pandas as pd
    
    # Testes
    test_comments = [
        "péssimo",
        "horrível",
        "nota 0",
        "um lixo",
        "fujam desse banco!",
        "precisa melhorar",
        "O app está travando muito no PIX",
        "Não consigo fazer login",
        "Lentidão ao abrir o aplicativo",
        "péssimo app",
        "ruim",
        "O aplicativo está muito lento para fazer transferências",
        "Problema no login com biometria",
        "péssimo",
        "Horrível",
        "Nota zero",
    ]
    
    print("Testando filtro de comentários genéricos:")
    print("=" * 60)
    
    for comment in test_comments:
        is_generic = is_generic_comment(comment)
        status = "FILTRAR" if is_generic else "PROCESSAR"
        print(f"{status:10} | {comment}")
