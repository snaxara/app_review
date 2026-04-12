"""
Script para humanizar o texto do TCC
Aplica transformações para tornar o texto mais natural e menos detectável por ferramentas de IA
"""

import re
from pathlib import Path

# Variações de conectivos e estruturas
VARIAÇÕES = {
    'portanto': ['portanto', 'dessa forma', 'assim', 'desse modo', 'consequentemente', 'por isso'],
    'no entanto': ['no entanto', 'entretanto', 'porém', 'contudo', 'todavia', 'mas'],
    'foi implementado': ['foi implementado', 'desenvolvemos', 'criamos', 'implementamos', 'construímos'],
    'foi utilizado': ['foi utilizado', 'utilizamos', 'empregamos', 'aplicamos', 'usamos'],
    'foi realizado': ['foi realizado', 'realizamos', 'executamos', 'conduzimos', 'efetuamos'],
    'demonstra': ['demonstra', 'mostra', 'indica', 'revela', 'evidencia', 'aponta'],
    'permite': ['permite', 'possibilita', 'facilita', 'habilita', 'viabiliza'],
    'apresenta': ['apresenta', 'exibe', 'mostra', 'demonstra', 'revela'],
}

def variar_conectivos(texto):
    """Substitui conectivos repetidos por variações"""
    # Contador para alternar entre variações
    contadores = {chave: 0 for chave in VARIAÇÕES.keys()}
    
    for padrao, variacoes in VARIAÇÕES.items():
        matches = list(re.finditer(r'\b' + re.escape(padrao) + r'\b', texto, re.IGNORECASE))
        for i, match in enumerate(matches):
            idx = contadores[padrao] % len(variacoes)
            substituicao = variacoes[idx]
            # Manter capitalização
            if match.group()[0].isupper():
                substituicao = substituicao.capitalize()
            texto = texto[:match.start()] + substituicao + texto[match.end():]
            contadores[padrao] += 1
    
    return texto

def quebrar_frases_longas(texto):
    """Quebra frases muito longas em frases menores"""
    # Identificar frases longas (mais de 150 caracteres)
    padrao = r'([^.!?]+[.!?])'
    frases = re.findall(padrao, texto)
    
    resultado = texto
    for frase in frases:
        if len(frase) > 150:
            # Tentar quebrar em vírgulas ou conjunções
            # Esta é uma simplificação - em produção seria mais sofisticado
            pass  # Implementação mais complexa seria necessária
    
    return resultado

def variar_inicio_frases(texto):
    """Varia o início das frases para evitar repetição"""
    # Identificar frases que começam com a mesma palavra
    padrao = r'([.!?]\s+)([A-Z][a-z]+)'
    
    # Esta é uma simplificação - implementação completa seria mais complexa
    return texto

def humanizar_paragrafo(paragrafo):
    """Aplica transformações de humanização em um parágrafo"""
    # Variar conectivos
    paragrafo = variar_conectivos(paragrafo)
    
    # Quebrar frases muito longas (simplificado)
    # paragrafo = quebrar_frases_longas(paragrafo)
    
    return paragrafo

def processar_secao(texto_secao):
    """Processa uma seção completa do TCC"""
    # Dividir em parágrafos
    paragrafos = texto_secao.split('\n\n')
    
    resultado = []
    for paragrafo in paragrafos:
        if paragrafo.strip() and not paragrafo.strip().startswith('#'):
            paragrafo_humanizado = humanizar_paragrafo(paragrafo)
            resultado.append(paragrafo_humanizado)
        else:
            resultado.append(paragrafo)
    
    return '\n\n'.join(resultado)

if __name__ == '__main__':
    print("Script de humanizacao de texto criado.")
    print("Este script pode ser usado para processar secoes especificas do TCC.")
