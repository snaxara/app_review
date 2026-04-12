"""
Correlação Funcional de Avaliações de Apps Bancários
Data: Dezembro 2025
Este script categoriza avaliações de aplicativos bancários por funcionalidade
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
BACKLOG_REPORT = 'backlog_priorizado.md'

# Configuração do modelo LLM
MODEL_NAME = 'gpt-4o'

# Filtro: processar apenas avaliações negativas
PROCESS_ONLY_NEGATIVE = True

# Limite de avaliações para teste inicial (None = processar todas)
LIMIT_REVIEWS = None # Altere para None para processar todas

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
    "Outros"
]

# --- Sistema de Prompts ---

SYSTEM_PROMPT = """Categorize avaliações de aplicativos bancários brasileiros em categorias funcionais."""

def create_categorization_prompt(review_text):
    """Cria o prompt de categorização para uma avaliação."""
    
    prompt = f"""Categorize a avaliação do usuário em UMA categoria funcional principal.

CATEGORIAS DISPONÍVEIS:
- PIX: Problemas com transferências PIX, chave PIX, QR Code
- Login/Autenticação: Dificuldades de acesso, senha, biometria, reconhecimento facial
- Performance: Lentidão, travamentos, crashes, app não abre, congela
- Interface/Usabilidade: Navegação confusa, design difícil, não encontra funcionalidades
- Empréstimos/Crédito: Questões sobre empréstimos, cartão de crédito, limites
- Pagamentos/Boletos: Problemas com pagamento de contas, boletos, DDA, duplicidade
- Saldo/Extrato: Visualização de saldo, extrato, transações, histórico
- Atendimento: Suporte ao cliente, chat, SAC, atendimento ruim
- Cadastro/Conta: Abertura de conta, atualização cadastral, documentos
- Investimentos: Aplicações financeiras, poupança, rendimentos
- Segurança: Fraudes, bloqueios indevidos, clonagem
- Notificações: Alertas, push notifications, avisos
- Questões geográficas: Problemas com acesso a conta, transferências, pagamentos, etc. em outros países.
- Placas/Veículos: Problemas com IPVA, REVAVAN, licenciamento, multas, DETRAN, veículos
- Outros: Problemas não categorizados acima

EXEMPLOS:

Avaliação: "Não consigo fazer PIX, sempre dá erro quando tento transferir"
Categoria: PIX

Avaliação: "O app trava toda hora, muito lento para abrir"
Categoria: Performance

Avaliação: "Não consigo entrar no app, sempre pede para redefinir senha"
Categoria: Login/Autenticação

Avaliação: "Os boletos DDA não são excluídos após o pagamento, fiz pagamento em duplicidade"
Categoria: Pagamentos/Boletos

Avaliação: "Interface muito confusa, não consigo encontrar onde pagar minhas contas"
Categoria: Interface/Usabilidade

AVALIAÇÃO PARA CATEGORIZAR:
"{review_text}"

Responda apenas com o nome exato da categoria. Se mencionar múltiplas funcionalidades, escolha a mais relevante."""

    return prompt

# --- Funções Principais ---

def load_sentiment_results(filepath):
    """Carrega os resultados da análise de sentimentos."""
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        print(f"Carregado: {len(df)} avaliações do arquivo {filepath}")
        return df
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None

def filter_reviews(df, only_negative=True, limit=None):
    """Filtra as avaliações para processamento."""
    
    if only_negative:
        df_filtered = df[df['sentiment_label'] == 'negative'].copy()
        print(f"Filtradas {len(df_filtered)} avaliações negativas")
    else:
        df_filtered = df.copy()
    
    if limit and len(df_filtered) > limit:
        df_filtered = df_filtered.head(limit)
        print(f"Limitado a {limit} avaliações para teste inicial")
    
    return df_filtered

def categorize_review(client, review_text, model_name):
    """Categoriza uma avaliação usando o LLM."""
    
    try:
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": create_categorization_prompt(review_text)}
            ],
            temperature=0.3,  # Baixa temperatura para respostas mais consistentes
            max_tokens=50
        )
        
        category = response.choices[0].message.content.strip()
        
        # Validação: garantir que a categoria retornada está na lista
        if category not in CATEGORIES:
            # Tentar encontrar correspondência parcial
            for valid_cat in CATEGORIES:
                if valid_cat.lower() in category.lower() or category.lower() in valid_cat.lower():
                    category = valid_cat
                    break
            else:
                category = "Outros"
        
        return category
    
    except Exception as e:
        print(f"Erro ao categorizar: {e}")
        return "Erro"

def process_reviews(df, model_name):
    """Processa todas as avaliações e adiciona categorias funcionais."""
    
    print("\n" + "="*60)
    print("INICIANDO CORRELAÇÃO FUNCIONAL COM LLM")
    print("="*60)
    
    # Inicializar cliente OpenAI
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Erro: OPENAI_API_KEY não encontrada.")
        print("Configure a variável de ambiente OPENAI_API_KEY ou crie um arquivo .env")
        exit(1)
    client = OpenAI(api_key=api_key)
    
    categories = []
    total = len(df)
    
    print(f"\nProcessando {total} avaliações...")
    print(f"Modelo: {model_name}")
    print(f"Tempo estimado: ~{total * 2} segundos\n")
    
    for idx, row in df.iterrows():
        review_text = row['content']
        
        # Categorizar usando LLM
        category = categorize_review(client, review_text, model_name)
        categories.append(category)
        
        # Feedback de progresso
        if (idx + 1) % 10 == 0:
            print(f"   Processadas: {idx + 1}/{total} ({((idx + 1)/total)*100:.1f}%)")
        
        # Rate limiting (evitar exceder limites da API)
        time.sleep(0.5)  # 0.5 segundos entre requisições
    
    df['functional_category'] = categories
    
    print(f"\nProcessamento concluído!")
    return df

def generate_backlog_report(df):
    """Gera relatório de backlog priorizado."""
    
    # Estatísticas por categoria
    category_counts = Counter(df['functional_category'])
    
    # Converter score para numérico (caso esteja como string)
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    
    # Severidade média por categoria (baseada no score original)
    category_severity = df.groupby('functional_category')['score'].mean()
    
    # Calcular prioridade
    # Fórmula: (Frequência * 0.4) + ((5 - Severidade) * 0.3) + (Peso_Impacto * 0.3)
    
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
        "Outros": 0.2
    }
    
    priorities = {}
    for category in category_counts.keys():
        if category == "Erro":
            continue
            
        freq = category_counts[category]
        freq_normalized = freq / len(df)  # Normalizar entre 0-1
        
        severity = category_severity.get(category, 3)
        severity_normalized = (5 - severity) / 5  # Inverter: score baixo = alta severidade
        
        impact = impact_weights.get(category, 0.5)
        
        priority_score = (freq_normalized * 0.4) + (severity_normalized * 0.3) + (impact * 0.3)
        priorities[category] = priority_score
    
    # Ordenar por prioridade
    sorted_priorities = sorted(priorities.items(), key=lambda x: x[1], reverse=True)
    
    # Gerar relatório em Markdown
    report = f"""# Backlog Priorizado

Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}  
Total de Avaliações: {len(df)}  
Modelo: {MODEL_NAME}

---

## Resumo

Priorização de funcionalidades baseada em {len(df)} avaliações negativas de usuários.

### Distribuição de Categorias

| Categoria | Quantidade | Porcentagem | Severidade Média | Prioridade |
|:----------|:-----------|:------------|:-----------------|:-----------|
"""
    
    for category, priority in sorted_priorities:
        count = category_counts[category]
        percentage = (count / len(df)) * 100
        severity = category_severity.get(category, 0)
        
        # Definir nível de prioridade
        if priority >= 0.7:
            priority_level = "CRITICA"
        elif priority >= 0.5:
            priority_level = "ALTA"
        elif priority >= 0.3:
            priority_level = "MEDIA"
        else:
            priority_level = "BAIXA"
        
        report += f"| {category} | {count} | {percentage:.1f}% | {severity:.2f}/5 | {priority_level} |\n"
    
    report += "\n---\n\n## Detalhamento por Categoria\n\n"
    
    # Detalhamento de cada categoria
    for category, priority in sorted_priorities[:5]:  # Top 5 categorias
        count = category_counts[category]
        percentage = (count / len(df)) * 100
        severity = category_severity.get(category, 0)
        
        if priority >= 0.7:
            priority_level = "CRÍTICA"
        elif priority >= 0.5:
            priority_level = "ALTA"
        elif priority >= 0.3:
            priority_level = "MÉDIA"
        else:
            priority_level = "BAIXA"
        
        report += f"""### {count}. {category} (Prioridade: {priority_level})

**Métricas:**
- Frequência: {count} avaliações ({percentage:.1f}% do total)
- Severidade Média: {severity:.2f}/5
- Score de Prioridade: {priority:.2f}

**Amostras de Avaliações:**

"""
        
        # Adicionar 3 exemplos de avaliações dessa categoria
        samples = df[df['functional_category'] == category].head(3)
        for idx, row in samples.iterrows():
            text_preview = row['content'][:150] + "..." if len(row['content']) > 150 else row['content']
            report += f"- \"{text_preview}\" (Score: {row['score']}/5)\n"
        
        report += "\n**Recomendações:**\n"
        
        # Recomendações específicas por categoria
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
            "Outros": "Analisar casos específicos para identificar padrões."
        }
        
        report += f"- {recommendations.get(category, 'Análise detalhada necessária.')}\n\n"
        report += "---\n\n"
    
    report += """## Próximos Passos

1. Revisão técnica dos problemas prioritários
2. Planejamento de sprint com itens críticos
3. Monitoramento das métricas após correções
4. Comunicação com usuários sobre correções

---
"""
    
    return report

def main():
    """Função principal que executa o processo de correlação funcional."""
    
    # 1. Carregar resultados da análise de sentimentos
    print(f"\nCarregando resultados de sentimentos...")
    df = load_sentiment_results(INPUT_CSV)
    
    if df is None or df.empty:
        print("Erro: Não foi possível carregar os dados.")
        exit(1)
    
    # 2. Filtrar avaliações
    print(f"\nFiltrando avaliações...")
    df_filtered = filter_reviews(df, only_negative=PROCESS_ONLY_NEGATIVE, limit=LIMIT_REVIEWS)
    
    if df_filtered.empty:
        print("Erro: Nenhuma avaliação para processar após filtros.")
        exit(1)
    
    # 3. Processar com LLM
    print(f"\nCategorizando com LLM...")
    df_results = process_reviews(df_filtered, MODEL_NAME)
    
    # 4. Salvar resultados
    print(f"\nSalvando resultados...")
    df_results.to_csv(OUTPUT_CSV, index=False, encoding='utf-8')
    print(f"Resultados salvos em: {OUTPUT_CSV}")
    
    # 5. Gerar relatório de backlog
    print(f"\nGerando relatório de backlog...")
    backlog_report = generate_backlog_report(df_results)
    
    with open(BACKLOG_REPORT, 'w', encoding='utf-8') as f:
        f.write(backlog_report)
    
    print(f"Relatório de backlog gerado: {BACKLOG_REPORT}")
    
    # 6. Estatísticas finais
    print("\n" + "="*60)
    print("ESTATISTICAS FINAIS")
    print("="*60)
    
    category_counts = Counter(df_results['functional_category'])
    print("\nDistribuição de Categorias:")
    for category, count in category_counts.most_common():
        percentage = (count / len(df_results)) * 100
        print(f"   {category}: {count} ({percentage:.1f}%)")
    
    print("\n" + "="*60)
    print("PROCESSO CONCLUIDO")
    print("="*60)
    print(f"\nArquivos gerados:")
    print(f"   {OUTPUT_CSV}")
    print(f"   {BACKLOG_REPORT}")

if __name__ == "__main__":
    main()
