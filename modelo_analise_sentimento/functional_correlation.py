"""
Script de categorização funcional de avaliações de aplicativos bancários.

Este script usa um modelo de linguagem (GPT-4o) para categorizar avaliações
negativas em funcionalidades específicas do aplicativo. Cada avaliação pode
ser classificada em múltiplas categorias simultaneamente.

O modelo GPT pode ser escolhido na execução através da variável de ambiente
OPENAI_MODEL. Por padrão, usa gpt-4o.
"""

import pandas as pd
from openai import OpenAI
import json
import time
from collections import Counter
from datetime import datetime
import os

# Carregar variáveis de ambiente do arquivo .env se existir
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# --- Configurações ---
INPUT_CSV = 'sentiment_results.csv'  # Arquivo gerado pelo sentiment_analysis.py
OUTPUT_CSV = 'functional_correlation_results.csv'

# Modelo GPT a ser usado para categorização
# Pode ser alterado via variável de ambiente OPENAI_MODEL
# Exemplos: 'gpt-4o', 'gpt-4o-mini', 'gpt-4-turbo'
MODEL_NAME = 'gpt-4o'

# Processar apenas avaliações negativas (recomendado)
# Avaliações positivas geralmente não têm problemas funcionais para categorizar
PROCESS_ONLY_NEGATIVE = True

# Limite de avaliações para processar (None = processar todas)
# Útil para testes iniciais ou quando há muitas avaliações
LIMIT_REVIEWS = None

# --- Taxonomia de Categorias ---
CATEGORIES = [
    "PIX",
    "Login/Autenticação",
    "Performance",
    "Interface/Usabilidade",
    "Empréstimos/Crédito",
    "Pagamentos/Boletos",
    "Saldo/Extrato",
    "Atendimento",
    "Cadastro/Conta",
    "Investimentos",
    "Segurança",
    "Notificações",
    "Questões geográficas",
    "Placas/Veículos",
    "Tarifas/Cobranças",
    "Outros"
]

# --- Sistema de Prompts ---

SYSTEM_PROMPT = """Categorize avaliações de aplicativos bancários brasileiros em categorias funcionais."""

def create_categorization_prompt(review_text):
    """Cria o prompt de categorização para uma avaliação com suporte a múltiplas categorias."""
    
    prompt = f"""Categorize a avaliação do usuário em TODAS as categorias funcionais que se aplicam.
Se uma avaliação menciona múltiplas funcionalidades com problemas, marque TODAS elas.
IMPORTANTE: Use "Outros" APENAS quando NENHUMA categoria específica se aplicar. Se identificar pelo menos uma categoria específica (PIX, Login, Performance, etc.), NÃO marque "Outros", mesmo que haja reclamações gerais no comentário.

CATEGORIAS DISPONÍVEIS:
- PIX: Problemas com transferências PIX, chave PIX, QR Code. NÃO incluir apenas menções a PIX sem problema funcional específico (ex: "vou tirar chave PIX" sem mencionar problema atual). NÃO incluir problemas de manutenção/horários do sistema (isso é Outros)
- Login/Autenticação: Dificuldades de acesso (não consegue fazer login, senha não funciona, biometria não funciona), senha, biometria, reconhecimento facial. NÃO incluir "sem acesso" quando é consequência de travamentos/crashes do app (isso é Performance)
- Performance: Lentidão do aplicativo, app trava/congela, crashes, app não abre, demora para carregar, consumo excessivo de bateria, uso excessivo de recursos em background (mesmo com app fechado), app não funciona de forma geral (ex: "não tá funcionando", "sempre que preciso não funciona", "não funciona quando preciso"). NÃO incluir bloqueios de funcionalidades (isso é Segurança). NÃO incluir comentários genéricos sobre bugs sem especificar problema de performance. NÃO incluir problemas de compatibilidade de versão do sistema operacional (isso é Outros). NÃO incluir comentários genéricos sobre "problemas" ou "dando problema" sem especificar tipo de problema técnico (isso é Outros)
- Interface/Usabilidade: Navegação confusa, design difícil, não encontra funcionalidades. NÃO incluir problemas de adesão/assinatura não autorizada (isso é Segurança). NÃO incluir comentários genéricos sobre bugs sem especificar problema de interface
- Empréstimos/Crédito: Questões sobre empréstimos, cartão de crédito, limites de crédito/empréstimo. NÃO incluir problemas gerais com limite de transação ou serviços do banco
- Pagamentos/Boletos: Problemas com pagamento de contas, boletos, DDA, duplicidade
- Saldo/Extrato: Visualização de saldo, extrato, transações, histórico
- Atendimento: Suporte ao cliente, chat, SAC, atendimento ruim
- Cadastro/Conta: Abertura de conta, atualização cadastral, documentos
- Investimentos: Aplicações financeiras, poupança, rendimentos
- Segurança: Fraudes, bloqueios indevidos de funcionalidades (ex: bloqueio de ligações legítimas, bloqueio de transações legítimas), clonagem, funcionalidades de segurança muito restritivas que impedem uso legítimo, adesões/assinaturas não autorizadas (ex: aderir a serviços/produtos sem consentimento explícito do usuário). Quando menciona "travar ligações" ou "bloquear ligações" = Segurança (não Performance). Quando menciona "aderiu sem autorização" ou "sem minha autorização" = Segurança
- Notificações: Alertas, push notifications, avisos
- Questões geográficas: Problemas com acesso a conta, transferências, pagamentos em outros países, fora do Brasil, exterior, bloqueio geográfico
- Placas/Veículos: Problemas com IPVA, RENAVAM, licenciamento, multas, DETRAN, veículos
- Tarifas/Cobranças: Reclamações sobre tarifas, taxas, juros cobrados indevidamente, cobranças não devidas, tarifas altas
- Outros: Problemas não categorizados acima, reclamações gerais sobre serviços do banco (não específicas do app mobile), problemas com versão web/site do banco, questões sobre agências físicas, problemas administrativos do banco que não são funcionalidades do app (ex: horários de manutenção, políticas do banco), comentários muito genéricos sobre bugs sem especificar funcionalidade ou tipo de problema (ex: "cada dia um bug diferente", "app cheio de bugs", "muitos erros"), problemas de compatibilidade de versão do sistema operacional (ex: "não será mais compatível com Android X", "vão cancelar acesso por incompatibilidade"), comentários genéricos sobre "problemas" ou "dando problema" sem especificar tipo de problema técnico ou funcionalidade (ex: "anda dando muito problema", "tá me prejudicando"). NÃO incluir comentários sobre "não funciona" de forma geral (isso é Performance)

EXEMPLOS:

Avaliação: "Não consigo fazer PIX, sempre dá erro quando tento transferir"
Categorias: PIX

Avaliação: "O banco só faz manutenção durante o dia, vou tirar minha chave PIX"
Categorias: Outros

Avaliação: "Não consigo cadastrar minha chave PIX no app"
Categorias: PIX

Avaliação: "O app trava toda hora, muito lento para abrir"
Categorias: Performance

Avaliação: "Não consigo entrar no app e quando consigo, o PIX não funciona"
Categorias: Login/Autenticação, PIX

Avaliação: "Os boletos DDA não são excluídos após o pagamento, fiz pagamento em duplicidade"
Categorias: Pagamentos/Boletos

Avaliação: "Interface muito confusa, não consigo encontrar onde pagar minhas contas"
Categorias: Interface/Usabilidade

Avaliação: "Estou no exterior e não tenho mais acesso a minha conta. Deveriam ter modo de acesso sem precisar ir ao caixa eletrônico"
Categorias: Questões geográficas

Avaliação: "O app bloqueia todas as ligações como golpe, mas são ligações legítimas de parentes e trabalho"
Categorias: Segurança

Avaliação: "Quando cliquei em negociar dívida, o app me aderiu ao clube sem minha autorização e agora não consigo cancelar"
Categorias: Segurança

Avaliação: "O aplicativo trava muito, demora para abrir e congela"
Categorias: Performance

Avaliação: "cada dia um bug diferente"
Categorias: Outros

Avaliação: "O app está cheio de bugs e erros"
Categorias: Outros

Avaliação: "O app trava muito e tem muitos bugs"
Categorias: Performance

Avaliação: "meu android é 8.0 e em breve vão cancelar o acesso no aplicativo pois não será mais compatível"
Categorias: Outros

Avaliação: "O app fica coletando localização mesmo fechado, drenando bateria e recursos"
Categorias: Performance

Avaliação: "Ultimamente anda dando muito problema, tá me prejudicando"
Categorias: Outros

Avaliação: "O app trava muito e está me prejudicando"
Categorias: Performance

Avaliação: "não tá funcionando"
Categorias: Performance

Avaliação: "sempre que preciso não funciona"
Categorias: Performance

Avaliação: "fora o dia inteiro cheio de coisa para resolver péssima"
Categorias: Outros

Avaliação: "O app trava toda hora e hoje sem acesso"
Categorias: Performance

Avaliação: "Não consigo fazer login, minha senha não funciona"
Categorias: Login/Autenticação

Avaliação: "O app trava e não consigo fazer login"
Categorias: Performance, Login/Autenticação

Avaliação: "serviço desse banco é péssimo, se for usar no computador é pior, não consigo aumentar limite de transação, tiraram a agência perto de casa"
Categorias: Outros

Avaliação: "O app trava muito e o banco está ultrapassado"
Categorias: Performance

Avaliação: "O banco está ultrapassado e o serviço é péssimo"
Categorias: Outros

Avaliação: "O app não permite aumentar o limite do cartão de crédito"
Categorias: Empréstimos/Crédito

Avaliação: "Não consigo aumentar limite de transação PIX no app"
Categorias: PIX

Avaliação: "Não estou conseguindo pagar IPVA do meu carro. Tenho 3 veículos cadastrados e quando vou pagar o App traz dados de um quarto veículo (nome/CPF/RENAVAM) que nem sei quem são"
Categorias: Placas/Veículos, Interface/Usabilidade

Avaliação: "O banco está me cobrando tarifa de algo que não uso, péssimo"
Categorias: Tarifas/Cobranças

Avaliação: "Estão cobrando juros sem eu estar usando o cheque especial, isso é um roubo"
Categorias: Tarifas/Cobranças

Avaliação: "O app está travando muito e não consigo fazer login. Além disso, não recebo notificações de PIX"
Categorias: Performance, Login/Autenticação, Notificações, PIX

AVALIAÇÃO PARA CATEGORIZAR:
"{review_text}"

Responda com uma lista separada por vírgulas das categorias que se aplicam. Se houver múltiplas funcionalidades com problemas, inclua todas elas. 
Lembre-se: Use "Outros" SOMENTE quando nenhuma categoria específica se aplicar. Se identificar qualquer categoria específica, não inclua "Outros".
Formato: Categoria1, Categoria2, Categoria3"""

    return prompt

# --- Funções Principais ---

def load_sentiment_results(filepath):
    """Carrega os resultados da análise de sentimentos."""
    try:
        # Tenta primeiro com ponto e vírgula, depois com vírgula
        try:
            df = pd.read_csv(filepath, sep=';', quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
            print(f"Carregado: {len(df)} avaliações do arquivo {filepath} (separador: ponto e vírgula)")
        except:
            df = pd.read_csv(filepath, sep=',', quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
            print(f"Carregado: {len(df)} avaliações do arquivo {filepath} (separador: vírgula)")
        
        # Remove sufixos estranhos das colunas se existirem
        df.columns = [col.split(';;;;')[0] for col in df.columns]
        
        return df
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        import traceback
        traceback.print_exc()
        return None

def load_existing_results(filepath):
    """Carrega resultados já processados para aproveitar processamento anterior."""
    if not os.path.exists(filepath):
        print(f"Arquivo {filepath} não existe. Processando tudo do zero.")
        return None
    
    try:
        # Detectar separador lendo primeira linha
        with open(filepath, 'r', encoding='utf-8') as f:
            first_line = f.readline()
        
        # Contar separadores na primeira linha (ignorando dentro de aspas)
        semicolon_count = first_line.count(';')
        comma_count = first_line.count(',')
        
        # Usar o separador que aparece mais vezes (mas verificar se a leitura foi bem-sucedida)
        if semicolon_count > comma_count:
            separator = ';'
            separator_used = 'ponto e vírgula'
        else:
            separator = ','
            separator_used = 'vírgula'
        
        df = pd.read_csv(filepath, sep=separator, quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
        
        # Verificar se a leitura foi bem-sucedida (deve ter mais de 1 coluna)
        if len(df.columns) == 1:
            # Se só tem 1 coluna, tentar o outro separador
            other_separator = ',' if separator == ';' else ';'
            df = pd.read_csv(filepath, sep=other_separator, quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
            separator_used = 'vírgula' if other_separator == ',' else 'ponto e vírgula'
        
        print(f"Arquivo existente carregado com separador {separator_used}")
        
        # Remove sufixos estranhos das colunas
        df.columns = [col.split(';;;;')[0] for col in df.columns]
        
        # Normalizar nomes de colunas para lidar com problemas de encoding
        # Criar mapeamento de colunas com problemas de encoding
        column_mapping = {}
        for col in df.columns:
            # Tentar encontrar correspondência nas categorias mesmo com encoding errado
            for cat in CATEGORIES:
                if cat.lower().replace('/', '') in col.lower().replace('/', '').replace('��', ''):
                    column_mapping[col] = cat
                    break
        
        # Renomear colunas se necessário
        if column_mapping:
            df = df.rename(columns=column_mapping)
        
        # Verificar se tem colunas de categorias (indicando que foi processado)
        # Verificar se tem pelo menos uma coluna que corresponde a uma categoria
        has_categories = False
        category_cols_found = []
        for cat in CATEGORIES:
            # Verificar correspondência exata primeiro
            if cat in df.columns:
                has_categories = True
                category_cols_found.append(cat)
            else:
                # Verificar correspondência parcial (para lidar com encoding)
                for col in df.columns:
                    col_normalized = col.lower().replace('/', '').replace('ã', 'a').replace('ç', 'c').replace('õ', 'o')
                    cat_normalized = cat.lower().replace('/', '')
                    if cat_normalized in col_normalized or col_normalized in cat_normalized:
                        has_categories = True
                        category_cols_found.append(cat)
                        # Renomear para o nome correto
                        df = df.rename(columns={col: cat})
                        break
        
        if has_categories:
            # Garantir que só tem negativas
            if 'sentiment_label' in df.columns:
                initial_count = len(df)
                df = df[df['sentiment_label'] == 'negative'].copy()
                if initial_count != len(df):
                    print(f"Filtrado arquivo existente: {len(df)} negativas (removidas {initial_count - len(df)} não-negativas)")
            
            print(f"Arquivo de resultados existente encontrado: {len(df)} avaliações já processadas")
            print(f"  Colunas de categorias encontradas: {len(category_cols_found)}")
            if len(category_cols_found) > 0:
                print(f"  Exemplos: {', '.join(category_cols_found[:5])}")
            
            # Verificar se tem conteúdo válido
            if 'content' not in df.columns:
                print("ERRO: Arquivo não tem coluna 'content'. Processando tudo do zero.")
                return None
            
            return df
        else:
            print("Arquivo existe mas não tem categorias processadas. Processando tudo do zero.")
            return None
    except Exception as e:
        print(f"Erro ao carregar resultados existentes: {e}")
        import traceback
        traceback.print_exc()
        return None

def filter_reviews(df, only_negative=True, limit=None):
    """Filtra as avaliações para processamento."""
    
    # Verificar se a coluna sentiment_label existe
    if 'sentiment_label' not in df.columns:
        print("Aviso: coluna 'sentiment_label' não encontrada. Processando todas as avaliações.")
        df_filtered = df.copy()
    elif only_negative:
        # Filtrar apenas negativas
        df_filtered = df[df['sentiment_label'] == 'negative'].copy()
        print(f"Filtradas {len(df_filtered)} avaliações negativas (de {len(df)} total)")
        
        if len(df_filtered) == 0:
            print("ERRO: Nenhuma avaliação negativa encontrada!")
            print(f"Valores únicos em sentiment_label: {df['sentiment_label'].unique()}")
    else:
        df_filtered = df.copy()
        print(f"Processando todas as {len(df_filtered)} avaliações (positivas, negativas e neutras)")
    
    if limit and len(df_filtered) > limit:
        df_filtered = df_filtered.head(limit)
        print(f"Limitado a {limit} avaliações para teste inicial")
    
    return df_filtered

def categorize_review(client, review_text, model_name):
    """
    Categoriza uma avaliação usando o modelo GPT com suporte a múltiplas categorias.
    
    Uma avaliação pode ser classificada em várias categorias ao mesmo tempo.
    Por exemplo, "O app trava muito e não consigo fazer PIX" seria categorizado
    como Performance e PIX.
    """
    
    try:
        # Chama a API do OpenAI para categorizar a avaliação
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": create_categorization_prompt(review_text)}
            ],
            # Temperatura baixa para respostas mais consistentes e previsíveis
            temperature=0.3,
            # Tokens suficientes para retornar múltiplas categorias
            max_tokens=200
        )
        
        categories_text = response.choices[0].message.content.strip()
        
        # Processa múltiplas categorias separadas por vírgula
        categories_list = []
        for cat in categories_text.split(','):
            cat = cat.strip()
            # Valida se a categoria retornada existe na nossa lista
            if cat in CATEGORIES:
                categories_list.append(cat)
            else:
                # Tenta encontrar correspondência parcial (caso o modelo retorne variação)
                for valid_cat in CATEGORIES:
                    if valid_cat.lower() in cat.lower() or cat.lower() in valid_cat.lower():
                        categories_list.append(valid_cat)
                        break
        
        # Se não encontrou nenhuma categoria válida, usa "Outros" como padrão
        if not categories_list:
            categories_list = ["Outros"]
        
        # Remove duplicatas e retorna
        return list(set(categories_list))
    
    except Exception as e:
        print(f"Erro ao categorizar: {e}")
        return ["Erro"]

def process_reviews(df, model_name):
    """
    Processa todas as avaliações e adiciona categorias funcionais.
    
    Cada avaliação pode receber múltiplas categorias. O script cria uma coluna
    binária (0 ou 1) para cada categoria, indicando se a avaliação se encaixa
    naquela categoria ou não.
    """
    
    print("\n" + "="*60)
    print("INICIANDO CORRELAÇÃO FUNCIONAL COM LLM")
    print("="*60)
    
    # Inicializa o cliente OpenAI usando a chave de API do ambiente
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Erro: OPENAI_API_KEY não encontrada.")
        print("Configure a variável de ambiente OPENAI_API_KEY ou crie um arquivo .env")
        exit(1)
    client = OpenAI(api_key=api_key)
    
    # Cria uma coluna binária para cada categoria funcional
    # Inicializa todas com 0 (não categorizado)
    for category in CATEGORIES:
        df[f'{category}'] = 0
    
    total = len(df)
    
    print(f"\nProcessando {total} avaliações...")
    print(f"Modelo: {model_name}")
    print(f"Modo: Classificação múltipla (múltiplas categorias por avaliação)")
    print(f"Tempo estimado: ~{total * 2} segundos\n")
    
    # Processa cada avaliação uma por uma
    for count, (idx, row) in enumerate(df.iterrows(), start=1):
        review_text = row['content']
        
        # Categoriza usando o modelo GPT (retorna lista de categorias)
        categories_list = categorize_review(client, review_text, model_name)
        
        # Marca cada categoria encontrada com 1 na coluna correspondente
        for category in categories_list:
            if category in CATEGORIES:
                df.at[idx, category] = 1
        
        # Mostra progresso a cada 10 avaliações processadas
        if count % 10 == 0:
            percentage = (count / total) * 100 if total > 0 else 0
            percentage = min(percentage, 100.0)
            print(f"   Processadas: {count}/{total} ({percentage:.1f}%) - Categorias: {len(categories_list)}")
        
        # Aguarda um pouco entre requisições para não exceder limites da API
        time.sleep(0.5)
    
    print(f"\nProcessamento concluído!")
    return df

def print_backlog_summary(df):
    """Imprime resumo de backlog priorizado no terminal."""
    
    # Estatísticas por categoria
    category_counts = {}
    for category in CATEGORIES:
        if category in df.columns:
            category_counts[category] = int(df[category].sum())
        else:
            category_counts[category] = 0
    
    # Converter score para numérico
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    
    # Severidade média por categoria
    category_severity = {}
    for category in CATEGORIES:
        if category in df.columns:
            mask = df[category] == 1
            if mask.sum() > 0:
                category_severity[category] = df[mask]['score'].mean()
            else:
                category_severity[category] = 0
        else:
            category_severity[category] = 0
    
    # Pesos de impacto para categorias críticas
    impact_weights = {
        "PIX": 1.0,
        "Login/Autenticação": 1.0,
        "Performance": 0.9,
        "Segurança": 1.0,
        "Pagamentos/Boletos": 0.8,
        "Empréstimos/Crédito": 0.7,
        "Saldo/Extrato": 0.6,
        "Interface/Usabilidade": 0.6,
        "Atendimento": 0.5,
        "Cadastro/Conta": 0.5,
        "Investimentos": 0.4,
        "Notificações": 0.3,
        "Questões geográficas": 0.7,
        "Placas/Veículos": 0.6,
        "Tarifas/Cobranças": 0.9,
        "Outros": 0.2
    }
    
    # Calcular prioridade
    priorities = {}
    for category in category_counts.keys():
        if category == "Erro":
            continue
        
        freq = category_counts[category]
        if freq == 0:
            continue
            
        freq_normalized = freq / len(df)
        severity = category_severity.get(category, 3)
        severity_normalized = (5 - severity) / 5
        impact = impact_weights.get(category, 0.5)
        
        priority_score = (freq_normalized * 0.4) + (severity_normalized * 0.3) + (impact * 0.3)
        priorities[category] = priority_score
    
    # Ordenar por prioridade
    sorted_priorities = sorted(priorities.items(), key=lambda x: x[1], reverse=True)
    
    # Imprimir resumo
    print("\n" + "="*60)
    print("BACKLOG PRIORIZADO")
    print("="*60)
    print(f"\nData: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"Total de Avaliações: {len(df)}")
    print(f"Modelo: {MODEL_NAME}")
    
    print("\n--- Distribuição de Categorias ---\n")
    print(f"{'Categoria':<25} {'Quantidade':<12} {'Porcentagem':<12} {'Severidade':<12} {'Prioridade':<12}")
    print("-" * 80)
    
    for category, priority in sorted_priorities:
        count = category_counts[category]
        percentage = (count / len(df)) * 100
        severity = category_severity.get(category, 0)
        
        if priority >= 0.7:
            priority_level = "CRITICA"
        elif priority >= 0.5:
            priority_level = "ALTA"
        elif priority >= 0.3:
            priority_level = "MEDIA"
        else:
            priority_level = "BAIXA"
        
        print(f"{category:<25} {count:<12} {percentage:>6.1f}%     {severity:>5.2f}/5    {priority_level:<12}")
    
    # Top 5 categorias com detalhamento
    print("\n--- Top 5 Categorias Prioritárias ---\n")
    
    recommendations = {
        "PIX": "Investigar logs de erro nas transações PIX. Revisar integração com BACEN e timeout de confirmação.",
        "Login/Autenticação": "Analisar taxa de falha no login. Revisar fluxo de recuperação de senha e biometria.",
        "Performance": "Executar profiling do app. Otimizar tempo de inicialização e identificar memory leaks.",
        "Interface/Usabilidade": "Realizar testes de usabilidade com usuários reais. Revisar arquitetura de informação.",
        "Pagamentos/Boletos": "Revisar lógica de exclusão de boletos pagos no DDA. Implementar confirmação antes de pagamentos.",
        "Empréstimos/Crédito": "Melhorar comunicação sobre limites e condições. Revisar fluxo de solicitação.",
        "Saldo/Extrato": "Otimizar carregamento de histórico. Implementar cache local.",
        "Atendimento": "Treinar equipe de suporte. Melhorar tempo de resposta no chat.",
        "Segurança": "Revisar políticas de bloqueio. Implementar notificações proativas de segurança.",
        "Cadastro/Conta": "Revisar fluxo de abertura de conta. Melhorar validação de documentos.",
        "Investimentos": "Melhorar interface de investimentos. Revisar comunicação de rendimentos.",
        "Notificações": "Revisar sistema de notificações push. Melhorar configurações de alertas.",
        "Questões geográficas": "Implementar modo de acesso para usuários no exterior. Revisar políticas de bloqueio geográfico.",
        "Placas/Veículos": "Revisar integração com DETRAN. Melhorar validação de dados de veículos e RENAVAM.",
        "Tarifas/Cobranças": "Revisar políticas de cobrança de tarifas. Melhorar transparência sobre taxas e juros. Implementar notificações antes de cobranças.",
        "Outros": "Analisar casos específicos para identificar padrões."
    }
    
    for idx, (category, priority) in enumerate(sorted_priorities[:5], 1):
        count = category_counts[category]
        percentage = (count / len(df)) * 100
        severity = category_severity.get(category, 0)
        
        if priority >= 0.7:
            priority_level = "CRITICA"
        elif priority >= 0.5:
            priority_level = "ALTA"
        elif priority >= 0.3:
            priority_level = "MEDIA"
        else:
            priority_level = "BAIXA"
        
        print(f"{idx}. {category} (Prioridade: {priority_level})")
        print(f"   Frequência: {count} avaliações ({percentage:.1f}% do total)")
        print(f"   Severidade Média: {severity:.2f}/5")
        print(f"   Score de Prioridade: {priority:.2f}")
        
        # Amostras de avaliações
        if category in df.columns:
            samples = df[df[category] == 1].head(3)
            if not samples.empty:
                print(f"   Amostras de Avaliações:")
                for _, row in samples.iterrows():
                    text_preview = row['content'][:100] + "..." if len(str(row['content'])) > 100 else str(row['content'])
                    print(f"     - \"{text_preview}\" (Score: {row['score']}/5)")
        
        print(f"   Recomendação: {recommendations.get(category, 'Análise detalhada necessária.')}")
        print()
    
    print("--- Próximos Passos ---")
    print("1. Revisão técnica dos problemas prioritários")
    print("2. Planejamento de sprint com itens críticos")
    print("3. Monitoramento das métricas após correções")
    print("4. Comunicação com usuários sobre correções")

def main():
    """Função principal que executa o processo de correlação funcional."""
    
    # 1. Carregar resultados da análise de sentimentos
    print(f"\nCarregando resultados de sentimentos...")
    df = load_sentiment_results(INPUT_CSV)
    
    if df is None or df.empty:
        print("Erro: Não foi possível carregar os dados.")
        exit(1)
    
    # 2. Verificar se há resultados já processados
    df_existing = load_existing_results(OUTPUT_CSV)
    
    # 3. Filtrar avaliações
    print(f"\nFiltrando avaliações...")
    df_filtered = filter_reviews(df, only_negative=PROCESS_ONLY_NEGATIVE, limit=LIMIT_REVIEWS)
    
    if df_filtered.empty:
        print("Erro: Nenhuma avaliação para processar após filtros.")
        exit(1)
    
    # 4. Se há resultados existentes, verificar quais já foram processados
    skip_llm_processing = False
    if df_existing is not None and not df_existing.empty:
        # Normalizar conteúdo para comparação (remover espaços extras, normalizar encoding)
        def normalize_content(text):
            if pd.isna(text):
                return ""
            return str(text).strip().lower()
        
        # Criar chave única para identificar avaliações (usando content normalizado)
        df_existing['_key'] = df_existing['content'].apply(normalize_content)
        df_filtered['_key'] = df_filtered['content'].apply(normalize_content)
        
        # Identificar quais já foram processadas
        already_processed = set(df_existing['_key'].unique())
        to_process = df_filtered[~df_filtered['_key'].isin(already_processed)].copy()
        
        print(f"\n{'='*60}")
        print("VERIFICANDO PROCESSAMENTO ANTERIOR")
        print(f"{'='*60}")
        print(f"Total de avaliações negativas no arquivo de entrada: {len(df_filtered)}")
        print(f"Avaliações já processadas encontradas: {len(already_processed)}")
        print(f"Avaliações novas para processar: {len(to_process)}")
        
        # Debug: mostrar algumas chaves para verificar
        if len(already_processed) > 0:
            sample_keys = list(already_processed)[:3]
            print(f"\nExemplo de chaves já processadas (primeiras 3):")
            for key in sample_keys:
                print(f"  - '{key[:50]}...'")
        
        if len(to_process) > 0:
            sample_new = list(to_process['_key'].head(3))
            print(f"\nExemplo de chaves novas (primeiras 3):")
            for key in sample_new:
                print(f"  - '{key[:50]}...'")
        
        if len(to_process) == 0:
            print("\n" + "="*60)
            print("✓ TODAS AS AVALIAÇÕES JÁ FORAM PROCESSADAS!")
            print("="*60)
            print(f"Reutilizando {len(df_existing)} avaliações já processadas.")
            print("Nenhuma chamada à API será feita.")
            df_results = df_existing.copy()
            # Remover coluna temporária
            if '_key' in df_results.columns:
                df_results = df_results.drop(columns=['_key'])
            
            # Pular processamento com LLM
            skip_llm_processing = True
        else:
            # Processar apenas as novas
            print(f"\n{'='*60}")
            print(f"PROCESSANDO {len(to_process)} NOVAS AVALIAÇÕES")
            print(f"{'='*60}")
            print(f"Economia: {len(already_processed)} avaliações já processadas serão reutilizadas")
            print(f"Novas avaliações a processar: {len(to_process)}")
            print(f"\nIniciando processamento com LLM...")
            
            df_new = process_reviews(to_process, MODEL_NAME)
            
            # Remover coluna temporária antes de combinar
            if '_key' in df_existing.columns:
                df_existing = df_existing.drop(columns=['_key'])
            if '_key' in df_new.columns:
                df_new = df_new.drop(columns=['_key'])
            
            # Combinar resultados
            df_results = pd.concat([df_existing, df_new], ignore_index=True)
            print(f"\n✓ Total combinado: {len(df_results)} avaliações")
            skip_llm_processing = False
    else:
        # Processar todas
        print(f"\n{'='*60}")
        print("NENHUM RESULTADO ANTERIOR ENCONTRADO")
        print(f"{'='*60}")
        print(f"Processando todas as {len(df_filtered)} avaliações negativas...")
        df_results = process_reviews(df_filtered, MODEL_NAME)
        skip_llm_processing = False
    
    # 5. Garantir que só tem negativas no resultado final
    if 'sentiment_label' in df_results.columns:
        initial_count = len(df_results)
        df_results = df_results[df_results['sentiment_label'] == 'negative'].copy()
        if initial_count != len(df_results):
            print(f"\nFiltrado para garantir apenas negativas: {len(df_results)} avaliações (removidas {initial_count - len(df_results)} não-negativas)")
    
    # Remover coluna temporária se existir
    if '_key' in df_results.columns:
        df_results = df_results.drop(columns=['_key'])
    
    # 6. Salvar resultados
    print(f"\nSalvando resultados...")
    df_results.to_csv(OUTPUT_CSV, index=False, sep=';', encoding='utf-8')
    print(f"Resultados salvos em: {OUTPUT_CSV}")
    print(f"Total de avaliações salvas: {len(df_results)} (apenas negativas)")
    
    # 7. Imprimir resumo de backlog
    print(f"\nGerando resumo de backlog...")
    print_backlog_summary(df_results)
    
    # 8. Estatísticas finais
    print("\n" + "="*60)
    print("ESTATISTICAS FINAIS")
    print("="*60)
    
    # Contar categorias (soma das colunas de categoria)
    print("\nDistribuição de Categorias:")
    for category in CATEGORIES:
        if category in df_results.columns:
            count = int(df_results[category].sum())
            if count > 0:
                percentage = (count / len(df_results)) * 100
                print(f"   {category}: {count} ({percentage:.1f}%)")
    
    print("\n" + "="*60)
    print("PROCESSO CONCLUIDO")
    print("="*60)
    print(f"\nArquivo gerado:")
    print(f"   {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
