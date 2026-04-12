"""
Script para atualizar o guia de anotação Excel com exemplos de sentimento MIXED
"""

import pandas as pd

# Recriar o guia completo com mixed
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
    
    # SENTIMENTO: POSITIVO
    {
        "Comentário": "Bom",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "-",
        "Motivo": "Marcador lexical positivo, Intenção comunicativa"
    },
    {
        "Comentário": "Gostei muito do atendimento e na resolução do meu problema",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "-",
        "Motivo": "Elogio explícito com menção a experiência positiva"
    },
    
    # SENTIMENTO: NEGATIVO
    {
        "Comentário": "Não consigo fazer PIX, sempre dá erro quando tento transferir",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "PIX",
        "Motivo": "Problema específico com transferência PIX, erro ao executar operação"
    },
    {
        "Comentário": "O app trava toda hora, muito lento para abrir",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Problemas de performance: travamentos e lentidão"
    },
    
    # SENTIMENTO: MIXED (MISTO) - NOVO!
    {
        "Comentário": "Pra entrar no aplicativo tem que assistir uma novela mexicana, demora demaisssssss as vezes precisamos fazer algo rápido como passar um pix e tem uma introdução enorme antes de entrar, fora isso as configurações e a caixinha de rendimento são ótimas !",
        "Sentimento": "Mixed",
        "Categorias Funcionais": "Performance, Login/Autenticação, Investimentos",
        "Motivo": "Avaliação mista: aspectos negativos (lentidão, introdução longa) E positivos (configurações e investimentos ótimos)"
    },
    {
        "Comentário": "App lento mas interface boa",
        "Sentimento": "Mixed",
        "Categorias Funcionais": "Performance, Interface/Usabilidade",
        "Motivo": "Menciona problema (lentidão) E elogio (interface boa) simultaneamente"
    },
    {
        "Comentário": "Não gosto da lentidão mas o PIX funciona perfeitamente",
        "Sentimento": "Mixed",
        "Categorias Funcionais": "Performance, PIX",
        "Motivo": "Reclamação sobre performance mas elogio sobre funcionalidade PIX"
    },
    {
        "Comentário": "Interface confusa mas atendimento excelente",
        "Sentimento": "Mixed",
        "Categorias Funcionais": "Interface/Usabilidade, Atendimento",
        "Motivo": "Problema com interface mas elogio ao atendimento"
    },
    {
        "Comentário": "O app é bom mas demora muito para abrir",
        "Sentimento": "Mixed",
        "Categorias Funcionais": "Performance",
        "Motivo": "Elogio geral mas reclamação específica sobre performance"
    },
]

# Criar DataFrame
df_exemplos = pd.DataFrame(exemplos)

# Ler taxonomia existente
taxonomia = [
    {
        "Categoria": "PIX",
        "Descrição": "Problemas relacionados a transferências PIX, chave PIX, QR Code, agendamento PIX",
        "Palavras-chave": "PIX, transferência instantânea, chave pix, QR code, QR code PIX, agendamento PIX",
        "Quando Usar": "Problemas específicos com funcionalidade PIX",
        "Quando NÃO Usar": "Se o problema é de performance (lentidão) ou login, marque também essas categorias"
    },
    {
        "Categoria": "Login/Autenticação",
        "Descrição": "Dificuldades de acesso ao app, problemas com senha, biometria, reconhecimento facial, token, 2FA",
        "Palavras-chave": "login, senha, entrar, acesso, biometria, digital, reconhecimento facial, token, autenticação, bloqueado",
        "Quando Usar": "Problemas de acesso ao app, autenticação não funciona",
        "Quando NÃO Usar": "Se menciona segurança/fraude, marcar também Segurança"
    },
    {
        "Categoria": "Performance",
        "Descrição": "Lentidão, travamentos, crashes, app não abre, congela, demora para carregar",
        "Palavras-chave": "lento, trava, demora, carregando, não abre, fecha sozinho, congela, crash, bug, erro técnico",
        "Quando Usar": "Problemas técnicos de performance do app",
        "Quando NÃO Usar": "Se menciona problema funcional específico E lentidão, marcar AMBOS"
    },
    {
        "Categoria": "Interface/Usabilidade",
        "Descrição": "Navegação confusa, design difícil de usar, não encontra funcionalidades, menu confuso",
        "Palavras-chave": "confuso, difícil de usar, não encontro, complicado, interface, menu, navegação, design",
        "Quando Usar": "Problema é claramente de navegação/interface, não funcionalidade específica",
        "Quando NÃO Usar": "Se o problema é funcional específico (ex: PIX não funciona), não é Interface"
    },
    {
        "Categoria": "Investimentos",
        "Descrição": "Aplicações financeiras, poupança, rendimentos, CDB, investimentos não aparecem",
        "Palavras-chave": "investimento, poupança, aplicação, rendimento, CDB, tesouro direto",
        "Quando Usar": "Problemas com funcionalidades de investimento",
        "Quando NÃO Usar": "Se é reclamação sobre rendimento baixo, não é problema funcional"
    },
]

# Criar aba sobre MIXED
guia_mixed = [
    {
        "Conceito": "O que é Mixed?",
        "Explicação": "Avaliação que contém aspectos POSITIVOS E NEGATIVOS simultaneamente na mesma avaliação"
    },
    {
        "Conceito": "Quando usar Mixed?",
        "Explicação": "Quando a avaliação menciona problemas/insatisfações E elogios/satisfações ao mesmo tempo"
    },
    {
        "Conceito": "Exemplo Mixed",
        "Explicação": "\"App lento mas interface boa\" = MIXED (problema E elogio)"
    },
    {
        "Conceito": "Exemplo NÃO Mixed",
        "Explicação": "\"Não gostei\" = NEGATIVE (apenas negativo), \"Ótimo app\" = POSITIVE (apenas positivo)"
    },
    {
        "Conceito": "Categorias em Mixed",
        "Explicação": "Avaliações mixed podem ter categorias funcionais tanto dos aspectos negativos quanto positivos"
    },
]

df_taxonomia = pd.DataFrame(taxonomia)
df_guia_mixed = pd.DataFrame(guia_mixed)

# Salvar em Excel com múltiplas abas
with pd.ExcelWriter('guia_anotacao_completo.xlsx', engine='openpyxl') as writer:
    df_taxonomia.to_excel(writer, sheet_name='1. Taxonomia', index=False)
    df_exemplos.to_excel(writer, sheet_name='2. Exemplos Práticos', index=False)
    df_guia_mixed.to_excel(writer, sheet_name='3. Guia Mixed', index=False)

print("✓ Guia atualizado: guia_anotacao_completo.xlsx")
print(f"\nAbas criadas:")
print(f"  1. Taxonomia: {len(df_taxonomia)} categorias")
print(f"  2. Exemplos Práticos: {len(df_exemplos)} exemplos (incluindo {len([e for e in exemplos if e['Sentimento'] == 'Mixed'])} mixed)")
print(f"  3. Guia Mixed: {len(df_guia_mixed)} conceitos")

