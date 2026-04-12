"""
Script para criar guia de anotação em formato Excel
com exemplos práticos de classificação
"""

import pandas as pd
from openai import OpenAI
import os

# Exemplos práticos de classificação
exemplos = [
    # SENTIMENTO: NEUTRO
    {
        "Comentário": "OK",
        "Sentimento": "Neutro",
        "Categorias Funcionais": "-",
        "Motivo": "Ambiguidade contextual, Princípio da incerteza, Ausência de marcadores de polaridade"
    },
    {
        "Comentário": "Sou novata aqui, não tenho muito conhecimento",
        "Sentimento": "Neutro",
        "Categorias Funcionais": "-",
        "Motivo": "Declaração puramente informativa sobre status de usuário"
    },
    {
        "Comentário": "Como estou recém usando, estou conhecendo",
        "Sentimento": "Neutro",
        "Categorias Funcionais": "-",
        "Motivo": "Indica fase de teste/avaliação sem posicionamento claro"
    },
    {
        "Comentário": "Exatamente",
        "Sentimento": "Neutro",
        "Categorias Funcionais": "-",
        "Motivo": "Resposta ambígua, sem contexto suficiente para determinar polaridade"
    },
    
    # SENTIMENTO: POSITIVO
    {
        "Comentário": "Estou conhecendo, pretendo trabalhar com ele",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "-",
        "Motivo": "Indica intenção positiva e disposição para engajamento futuro"
    },
    {
        "Comentário": "Bom",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "-",
        "Motivo": "Marcador lexical positivo, Intenção comunicativa"
    },
    {
        "Comentário": "Ótimo",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "-",
        "Motivo": "Marcador lexical positivo explícito"
    },
    {
        "Comentário": "Gostei muito do atendimento e na resolução do meu problema",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "-",
        "Motivo": "Elogio explícito com menção a experiência positiva"
    },
    {
        "Comentário": "Muito eficiente",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Elogio relacionado a performance do app"
    },
    
    # SENTIMENTO: NEGATIVO - PIX
    {
        "Comentário": "Não consigo fazer PIX, sempre dá erro quando tento transferir",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "PIX",
        "Motivo": "Problema específico com transferência PIX, erro ao executar operação"
    },
    {
        "Comentário": "O QR code não está funcionando",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "PIX",
        "Motivo": "Problema com QR code PIX, funcionalidade específica não funciona"
    },
    
    # SENTIMENTO: NEGATIVO - LOGIN/AUTENTICAÇÃO
    {
        "Comentário": "Não consigo entrar no app",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Login/Autenticação",
        "Motivo": "Problema de acesso ao app, dificuldade de login"
    },
    {
        "Comentário": "Biometria não funciona",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Login/Autenticação",
        "Motivo": "Problema com método de autenticação biométrica"
    },
    {
        "Comentário": "App bloqueou minha conta sem motivo",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Login/Autenticação, Segurança",
        "Motivo": "Bloqueio de conta mencionado, pode envolver segurança também"
    },
    
    # SENTIMENTO: NEGATIVO - PERFORMANCE
    {
        "Comentário": "O app trava toda hora, muito lento para abrir",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Problemas de performance: travamentos e lentidão"
    },
    {
        "Comentário": "Não estou gostando desse aplicativo do banco tá travando demora pra abrir",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Reclamação sobre travamentos e demora para abrir"
    },
    {
        "Comentário": "App não abre",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Problema técnico: aplicativo não inicia"
    },
    
    # SENTIMENTO: NEGATIVO - INTERFACE/USABILIDADE
    {
        "Comentário": "Interface muito confusa, não consigo encontrar onde pagar minhas contas",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Interface/Usabilidade",
        "Motivo": "Problema de navegação e localização de funcionalidades"
    },
    {
        "Comentário": "Menu difícil de navegar",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Interface/Usabilidade",
        "Motivo": "Dificuldade de navegação no menu"
    },
    
    # SENTIMENTO: NEGATIVO - MÚLTIPLAS CATEGORIAS
    {
        "Comentário": "Não consigo entrar no app e quando consigo, o PIX não funciona",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Login/Autenticação, PIX",
        "Motivo": "Múltiplos problemas: acesso e funcionalidade PIX"
    },
    {
        "Comentário": "O app está travando muito e não consigo fazer login. Além disso, não recebo notificações de PIX",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance, Login/Autenticação, Notificações, PIX",
        "Motivo": "Múltiplos problemas: performance, acesso, notificações e PIX"
    },
    {
        "Comentário": "App lento para fazer PIX",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance, PIX",
        "Motivo": "Problema de performance afetando funcionalidade PIX"
    },
    
    # SENTIMENTO: NEGATIVO - PAGAMENTOS/BOLETOS
    {
        "Comentário": "Os boletos DDA não são excluídos após o pagamento, fiz pagamento em duplicidade",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Pagamentos/Boletos",
        "Motivo": "Problema com boletos DDA e pagamento duplicado"
    },
    {
        "Comentário": "Não consigo pagar minhas contas",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Pagamentos/Boletos",
        "Motivo": "Dificuldade para realizar pagamento de contas"
    },
    
    # SENTIMENTO: NEGATIVO - EMPRÉSTIMOS/CRÉDITO
    {
        "Comentário": "Achei o app muito bom de usar mas quero cartão com limite que eu não tenho",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "Empréstimos/Crédito",
        "Motivo": "Solicitação de limite de crédito, não é problema funcional mas menciona crédito"
    },
    {
        "Comentário": "Não consigo solicitar empréstimo",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Empréstimos/Crédito",
        "Motivo": "Problema funcional com solicitação de empréstimo"
    },
    
    # SENTIMENTO: NEGATIVO - ATENDIMENTO
    {
        "Comentário": "Atendimento muito ruim",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Atendimento",
        "Motivo": "Reclamação sobre qualidade do atendimento"
    },
    {
        "Comentário": "Chat não funciona",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Atendimento",
        "Motivo": "Problema funcional com canal de atendimento"
    },
    
    # SENTIMENTO: NEGATIVO - QUESTÕES GEOGRÁFICAS
    {
        "Comentário": "Estou no exterior e não tenho mais acesso a minha conta",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Questões geográficas, Login/Autenticação",
        "Motivo": "Problema de acesso relacionado a localização geográfica"
    },
    
    # SENTIMENTO: NEGATIVO - PLACAS/VEÍCULOS
    {
        "Comentário": "Não estou conseguindo pagar IPVA do meu carro",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Placas/Veículos",
        "Motivo": "Problema com pagamento de IPVA"
    },
    
    # SENTIMENTO: NEGATIVO - TARIFAS/COBRANÇAS
    {
        "Comentário": "O banco está me cobrando tarifa de algo que não uso",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Tarifas/Cobranças",
        "Motivo": "Reclamação sobre cobrança indevida de tarifa"
    },
    {
        "Comentário": "Estão cobrando juros sem eu estar usando o cheque especial",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Tarifas/Cobranças",
        "Motivo": "Reclamação sobre cobrança indevida de juros"
    },
    
    # SENTIMENTO: NEGATIVO - OUTROS / NÃO IDENTIFICADO
    {
        "Comentário": "App ruim",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Não Identificado",
        "Motivo": "Comentário genérico sem especificidade, sem problema funcional identificável"
    },
    {
        "Comentário": "Não gostei",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Não Identificado",
        "Motivo": "Opinião genérica sem informação útil sobre problema específico"
    },
    {
        "Comentário": "Meu cartão não chegou estou esperando",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Cadastro/Conta",
        "Motivo": "Relata um problema concreto: serviço não entregue (cartão físico)"
    },
]

# Criar DataFrame
df = pd.DataFrame(exemplos)

# Reordenar colunas
df = df[['Comentário', 'Sentimento', 'Categorias Funcionais', 'Motivo']]

# Salvar como CSV (compatível com Excel)
df.to_csv('guia_anotacao_exemplos.csv', index=False, encoding='utf-8-sig', sep=';')

# Tentar salvar como Excel se openpyxl estiver disponível
try:
    df.to_excel('guia_anotacao_exemplos.xlsx', index=False, engine='openpyxl')
    print("✓ Arquivo Excel criado: guia_anotacao_exemplos.xlsx")
except ImportError:
    print("⚠️ openpyxl não instalado. Instale com: pip install openpyxl")
    print("✓ Arquivo CSV criado: guia_anotacao_exemplos.csv (pode ser aberto no Excel)")

print(f"\n✓ Total de exemplos: {len(df)}")
print(f"  - Neutro: {len(df[df['Sentimento'] == 'Neutro'])}")
print(f"  - Positivo: {len(df[df['Sentimento'] == 'Positivo'])}")
print(f"  - Negativo: {len(df[df['Sentimento'] == 'Negativo'])}")

