"""
Script para criar guia de anotação completo em formato Excel
com todas as 17 categorias e exemplos completos para todas as polaridades
"""

import pandas as pd

# ABA 1: TAXONOMIA COMPLETA DE CATEGORIAS (17 categorias)
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
        "Categoria": "Empréstimos/Crédito",
        "Descrição": "Questões sobre empréstimos, cartão de crédito, limites, financiamentos, parcelas",
        "Palavras-chave": "empréstimo, crédito, limite, cartão, financiamento, parcela, cheque especial",
        "Quando Usar": "Problemas ou questões relacionadas a crédito/empréstimos",
        "Quando NÃO Usar": "Se é reclamação sobre tarifa de empréstimo, usar Tarifas/Cobranças"
    },
    {
        "Categoria": "Pagamentos/Boletos",
        "Descrição": "Problemas com pagamento de contas, boletos, DDA, duplicidade de pagamento",
        "Palavras-chave": "boleto, pagamento, conta, DDA, duplicidade, não paga, conta de luz, água, telefone",
        "Quando Usar": "Problemas com pagamento de contas e boletos",
        "Quando NÃO Usar": "Se é PIX, usar categoria PIX. Se é lentidão, marcar também Performance"
    },
    {
        "Categoria": "Saldo/Extrato",
        "Descrição": "Visualização de saldo, extrato, transações, histórico, movimentações não aparecem",
        "Palavras-chave": "saldo, extrato, transação, histórico, movimentação, lançamento",
        "Quando Usar": "Problemas com visualização de informações financeiras",
        "Quando NÃO Usar": "Se é problema de transferência, usar PIX ou outra categoria"
    },
    {
        "Categoria": "Atendimento",
        "Descrição": "Suporte ao cliente, chat, SAC, atendimento ruim, não consegue falar com suporte",
        "Palavras-chave": "atendimento, suporte, ajuda, contato, SAC, chat, call center",
        "Quando Usar": "Problemas com canais de atendimento ou qualidade do atendimento",
        "Quando NÃO Usar": "Se não encontra ajuda no app, pode ser Interface/Usabilidade"
    },
    {
        "Categoria": "Cadastro/Conta",
        "Descrição": "Abertura de conta, atualização cadastral, documentos, dados pessoais",
        "Palavras-chave": "cadastro, abrir conta, dados, atualizar, documento, CPF, identidade",
        "Quando Usar": "Problemas com cadastro ou dados cadastrais",
        "Quando NÃO Usar": "Se é problema de login, usar Login/Autenticação"
    },
    {
        "Categoria": "Investimentos",
        "Descrição": "Aplicações financeiras, poupança, rendimentos, CDB, investimentos não aparecem",
        "Palavras-chave": "investimento, poupança, aplicação, rendimento, CDB, tesouro direto",
        "Quando Usar": "Problemas com funcionalidades de investimento",
        "Quando NÃO Usar": "Se é reclamação sobre rendimento baixo, não é problema funcional"
    },
    {
        "Categoria": "Segurança",
        "Descrição": "Fraudes, bloqueios indevidos, clonagem, segurança, suspeita de fraude",
        "Palavras-chave": "fraude, bloqueio, segurança, roubo, clonagem, hackeado, suspeita",
        "Quando Usar": "Problemas relacionados a segurança e fraudes",
        "Quando NÃO Usar": "Se é bloqueio por segurança, marcar também Login/Autenticação"
    },
    {
        "Categoria": "Notificações",
        "Descrição": "Alertas, push notifications, avisos, não recebe notificações",
        "Palavras-chave": "notificação, alerta, aviso, push, não recebe, aviso de transação",
        "Quando Usar": "Problemas com sistema de notificações",
        "Quando NÃO Usar": "Se menciona não receber notificação DE uma funcionalidade, marcar AMBOS"
    },
    {
        "Categoria": "Questões geográficas",
        "Descrição": "Problemas com acesso, transferências, pagamentos em outros países, bloqueio geográfico",
        "Palavras-chave": "exterior, fora do Brasil, outro país, bloqueio geográfico, viagem",
        "Quando Usar": "Problemas relacionados a localização geográfica",
        "Quando NÃO Usar": "Se não menciona questão geográfica, não usar esta categoria"
    },
    {
        "Categoria": "Placas/Veículos",
        "Descrição": "Problemas com IPVA, RENAVAM, licenciamento, multas, DETRAN, veículos",
        "Palavras-chave": "IPVA, RENAVAM, licenciamento, multa, DETRAN, veículo, carro, moto, placa",
        "Quando Usar": "Problemas com funcionalidades relacionadas a veículos",
        "Quando NÃO Usar": "Se não menciona veículos, não usar esta categoria"
    },
    {
        "Categoria": "Tarifas/Cobranças",
        "Descrição": "Reclamações sobre tarifas, taxas, juros cobrados indevidamente, cobranças não devidas",
        "Palavras-chave": "tarifa, taxa, juros, cobrança, cobrado indevidamente, tarifa alta",
        "Quando Usar": "Reclamações sobre cobranças e tarifas",
        "Quando NÃO Usar": "Se é problema funcional (ex: empréstimo não funciona), usar categoria funcional"
    },
    {
        "Categoria": "Outros",
        "Descrição": "Problemas identificáveis mas que não se encaixam em nenhuma categoria acima",
        "Palavras-chave": "problema específico não listado",
        "Quando Usar": "Problema específico e identificável, mas não se encaixa em categorias acima",
        "Quando NÃO Usar": "Se é comentário genérico, usar Não Identificado"
    },
    {
        "Categoria": "Não Identificado",
        "Descrição": "Comentários genéricos sem informação útil, sem especificidade",
        "Palavras-chave": "app ruim, não gostei, péssimo, horrível",
        "Quando Usar": "Comentários genéricos sem problema funcional identificável",
        "Quando NÃO Usar": "Se há problema específico identificável, usar categoria específica ou Outros"
    },
]

# ABA 2: EXEMPLOS PRÁTICOS COMPLETOS (todas as polaridades e categorias)
exemplos = [
    # ========== SENTIMENTO: NEUTRO ==========
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
    
    # ========== SENTIMENTO: POSITIVO ==========
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
    {
        "Comentário": "Bem dinâmica as operações através do aplicativo",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "Interface/Usabilidade",
        "Motivo": "Elogio relacionado à interface e usabilidade"
    },
    
    # ========== SENTIMENTO: NEGATIVO - PIX ==========
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
    {
        "Comentário": "PIX não está sendo processado",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "PIX",
        "Motivo": "Problema com processamento de PIX"
    },
    
    # ========== SENTIMENTO: NEGATIVO - LOGIN/AUTENTICAÇÃO ==========
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
    {
        "Comentário": "Esqueci minha senha e não consigo recuperar",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Login/Autenticação",
        "Motivo": "Problema com recuperação de senha"
    },
    
    # ========== SENTIMENTO: NEGATIVO - PERFORMANCE ==========
    {
        "Comentário": "O app trava toda hora, muito lento para abrir",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Problemas de performance: travamentos e lentidão"
    },
    {
        "Comentário": "App não abre",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Problema técnico: aplicativo não inicia"
    },
    {
        "Comentário": "Não estou gostando desse aplicativo do banco tá travando demora pra abrir",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Reclamação sobre travamentos e demora para abrir"
    },
    {
        "Comentário": "Fecha sozinho quando estou usando",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Performance",
        "Motivo": "Problema de estabilidade: app fecha inesperadamente"
    },
    
    # ========== SENTIMENTO: NEGATIVO - INTERFACE/USABILIDADE ==========
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
    {
        "Comentário": "Design ruim, difícil de usar",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Interface/Usabilidade",
        "Motivo": "Problema com design e usabilidade"
    },
    
    # ========== SENTIMENTO: NEGATIVO - EMPRÉSTIMOS/CRÉDITO ==========
    {
        "Comentário": "Não consigo solicitar empréstimo",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Empréstimos/Crédito",
        "Motivo": "Problema funcional com solicitação de empréstimo"
    },
    {
        "Comentário": "Limite de crédito não aparece",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Empréstimos/Crédito",
        "Motivo": "Problema com visualização de limite de crédito"
    },
    {
        "Comentário": "Achei o app muito bom de usar mas quero cartão com limite que eu não tenho",
        "Sentimento": "Positivo",
        "Categorias Funcionais": "Empréstimos/Crédito",
        "Motivo": "Solicitação de limite de crédito, não é problema funcional mas menciona crédito"
    },
    
    # ========== SENTIMENTO: NEGATIVO - PAGAMENTOS/BOLETOS ==========
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
    {
        "Comentário": "Boleto não aparece para pagamento",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Pagamentos/Boletos",
        "Motivo": "Problema com visualização de boletos"
    },
    
    # ========== SENTIMENTO: NEGATIVO - SALDO/EXTRATO ==========
    {
        "Comentário": "Saldo não está correto",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Saldo/Extrato",
        "Motivo": "Problema com visualização de saldo"
    },
    {
        "Comentário": "Extrato não atualiza",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Saldo/Extrato",
        "Motivo": "Problema com atualização de extrato"
    },
    {
        "Comentário": "Transações não aparecem",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Saldo/Extrato",
        "Motivo": "Problema com visualização de transações"
    },
    
    # ========== SENTIMENTO: NEGATIVO - ATENDIMENTO ==========
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
    {
        "Comentário": "SAC não responde",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Atendimento",
        "Motivo": "Problema com resposta do SAC"
    },
    
    # ========== SENTIMENTO: NEGATIVO - CADASTRO/CONTA ==========
    {
        "Comentário": "Não consigo abrir conta",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Cadastro/Conta",
        "Motivo": "Problema com abertura de conta"
    },
    {
        "Comentário": "Meu cartão não chegou estou esperando",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Cadastro/Conta",
        "Motivo": "Relata um problema concreto: serviço não entregue (cartão físico)"
    },
    {
        "Comentário": "Documentos não são aceitos",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Cadastro/Conta",
        "Motivo": "Problema com aceitação de documentos"
    },
    
    # ========== SENTIMENTO: NEGATIVO - INVESTIMENTOS ==========
    {
        "Comentário": "Investimentos não aparecem",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Investimentos",
        "Motivo": "Problema com visualização de investimentos"
    },
    {
        "Comentário": "Não consigo aplicar dinheiro",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Investimentos",
        "Motivo": "Problema funcional com aplicação de investimentos"
    },
    
    # ========== SENTIMENTO: NEGATIVO - SEGURANÇA ==========
    {
        "Comentário": "Minha conta foi hackeada",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Segurança",
        "Motivo": "Problema de segurança relacionado a fraude"
    },
    {
        "Comentário": "Bloqueio indevido por fraude",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Segurança, Login/Autenticação",
        "Motivo": "Bloqueio relacionado a segurança"
    },
    
    # ========== SENTIMENTO: NEGATIVO - NOTIFICAÇÕES ==========
    {
        "Comentário": "Não recebo notificações de PIX",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Notificações, PIX",
        "Motivo": "Problema com notificações DE uma funcionalidade específica"
    },
    {
        "Comentário": "Push notifications não funcionam",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Notificações",
        "Motivo": "Problema funcional com sistema de notificações"
    },
    
    # ========== SENTIMENTO: NEGATIVO - QUESTÕES GEOGRÁFICAS ==========
    {
        "Comentário": "Estou no exterior e não tenho mais acesso a minha conta",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Questões geográficas, Login/Autenticação",
        "Motivo": "Problema de acesso relacionado a localização geográfica"
    },
    {
        "Comentário": "Não consigo fazer transferência fora do Brasil",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Questões geográficas, PIX",
        "Motivo": "Problema geográfico afetando funcionalidade"
    },
    
    # ========== SENTIMENTO: NEGATIVO - PLACAS/VEÍCULOS ==========
    {
        "Comentário": "Não estou conseguindo pagar IPVA do meu carro",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Placas/Veículos",
        "Motivo": "Problema com pagamento de IPVA"
    },
    {
        "Comentário": "RENAVAM não aparece",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Placas/Veículos",
        "Motivo": "Problema com visualização de dados de veículo"
    },
    
    # ========== SENTIMENTO: NEGATIVO - TARIFAS/COBRANÇAS ==========
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
    
    # ========== SENTIMENTO: NEGATIVO - MÚLTIPLAS CATEGORIAS ==========
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
    {
        "Comentário": "Não encontro onde fazer PIX e quando encontro não funciona",
        "Sentimento": "Negativo",
        "Categorias Funcionais": "Interface/Usabilidade, PIX",
        "Motivo": "Dois problemas: navegação E funcionalidade"
    },
    
    # ========== SENTIMENTO: MIXED (MISTO) ==========
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
    
    # ========== SENTIMENTO: NEGATIVO - OUTROS/NÃO IDENTIFICADO ==========
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
]

# ABA 3: CASOS COMPLEXOS E RESOLUÇÃO
casos_complexos = [
    {
        "Caso": "Múltiplas Funcionalidades",
        "Exemplo": "App lento e não consigo fazer PIX",
        "Solução": "Performance + PIX (ambas)",
        "Motivo": "Dois problemas distintos: performance e funcionalidade específica"
    },
    {
        "Caso": "Interface vs. Funcionalidade",
        "Exemplo": "Não encontro onde fazer PIX",
        "Solução": "Interface/Usabilidade (problema é de navegação)",
        "Motivo": "Problema é de localização, não da funcionalidade em si"
    },
    {
        "Caso": "Interface vs. Funcionalidade",
        "Exemplo": "Não encontro onde fazer PIX e quando encontro não funciona",
        "Solução": "Interface/Usabilidade + PIX (ambos os problemas)",
        "Motivo": "Dois problemas: navegação E funcionalidade"
    },
    {
        "Caso": "Performance vs. Funcionalidade",
        "Exemplo": "PIX muito lento",
        "Solução": "Performance + PIX (ambas)",
        "Motivo": "Problema de performance afetando funcionalidade específica"
    },
    {
        "Caso": "Performance vs. Funcionalidade",
        "Exemplo": "PIX não funciona",
        "Solução": "Apenas PIX (sem menção a lentidão)",
        "Motivo": "Problema funcional sem menção a performance"
    },
    {
        "Caso": "Segurança vs. Login/Autenticação",
        "Exemplo": "Conta bloqueada por segurança",
        "Solução": "Segurança + Login/Autenticação (ambas)",
        "Motivo": "Bloqueio relacionado a segurança"
    },
    {
        "Caso": "Notificações vs. Funcionalidade",
        "Exemplo": "Não recebo notificação de PIX",
        "Solução": "Notificações + PIX (ambas)",
        "Motivo": "Problema com notificações DE uma funcionalidade específica"
    },
]

# Criar DataFrames
df_taxonomia = pd.DataFrame(taxonomia)
df_exemplos = pd.DataFrame(exemplos)
df_casos = pd.DataFrame(casos_complexos)

# Salvar em Excel com múltiplas abas
with pd.ExcelWriter('guia_anotacao_completo.xlsx', engine='openpyxl') as writer:
    df_taxonomia.to_excel(writer, sheet_name='1. Taxonomia', index=False)
    df_exemplos.to_excel(writer, sheet_name='2. Exemplos Práticos', index=False)
    df_casos.to_excel(writer, sheet_name='3. Casos Complexos', index=False)

print("✓ Guia completo criado: guia_anotacao_completo.xlsx")
print(f"\nAbas criadas:")
print(f"  1. Taxonomia: {len(df_taxonomia)} categorias (COMPLETO)")
print(f"  2. Exemplos Práticos: {len(df_exemplos)} exemplos (todas as polaridades e categorias)")
print(f"  3. Casos Complexos: {len(df_casos)} casos")

# Estatísticas
print(f"\nEstatísticas dos exemplos:")
sentimentos = df_exemplos['Sentimento'].value_counts()
for sent, count in sentimentos.items():
    print(f"  - {sent}: {count} exemplos")
