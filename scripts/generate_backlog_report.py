"""
Script para gerar relatório completo de backlog priorizado
baseado nos resultados da correlação funcional

Uso:
    python generate_backlog_report.py
    
    ou especificando arquivos:
    python generate_backlog_report.py --input functional_correlation_results.csv --output "Backlog Priorizado - Aplicativo Bancário.md"
"""

import pandas as pd
from collections import Counter
from datetime import datetime
import argparse
import os

# Configurações padrão
DEFAULT_INPUT_CSV = 'functional_correlation_results.csv'
DEFAULT_OUTPUT_MD = 'Backlog Priorizado - Aplicativo Bancário.md'
DEFAULT_MODEL = 'gpt-4o'

# Categorias disponíveis
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

# Pesos de impacto para categorias críticas
IMPACT_WEIGHTS = {
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

# Recomendações por categoria
RECOMMENDATIONS = {
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


def load_correlation_results(filepath):
    """Carrega os resultados da correlação funcional."""
    try:
        df = pd.read_csv(filepath, encoding='utf-8')
        print(f"Carregado: {len(df)} avaliações do arquivo {filepath}")
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado: {filepath}")
        return None
    except Exception as e:
        print(f"Erro ao carregar arquivo: {e}")
        return None


def calculate_priorities(df):
    """Calcula as prioridades das categorias baseado em frequência, severidade e impacto."""
    # Conta quantas avaliações têm cada categoria marcada
    category_counts = {}
    for category in CATEGORIES:
        if category in df.columns:
            category_counts[category] = int(df[category].sum())
        else:
            category_counts[category] = 0
    
    df['score'] = pd.to_numeric(df['score'], errors='coerce')
    
    # Calcula a severidade média por categoria
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
    
    # Calcula o score de prioridade para cada categoria
    priorities = {}
    for category in CATEGORIES:
        freq = category_counts[category]
        if freq == 0:
            continue
            
        freq_normalized = freq / len(df)
        
        severity = category_severity.get(category, 3)
        severity_normalized = (5 - severity) / 5
        
        impact = IMPACT_WEIGHTS.get(category, 0.5)
        
        priority_score = (freq_normalized * 0.4) + (severity_normalized * 0.3) + (impact * 0.3)
        priorities[category] = priority_score
    
    return sorted(priorities.items(), key=lambda x: x[1], reverse=True), category_counts, category_severity


def get_priority_level(priority_score):
    """Retorna o nível de prioridade."""
    if priority_score >= 0.5:
        return "ALTA", "ALTA"
    elif priority_score >= 0.3:
        return "MÉDIA", "MÉDIA"
    else:
        return "BAIXA", "BAIXA"


def generate_backlog_report(df, model_name=DEFAULT_MODEL):
    """Gera relatório completo de backlog priorizado."""
    
    sorted_priorities, category_counts, category_severity = calculate_priorities(df)
    
    # Cabeçalho do relatório
    report = f"""# Backlog Priorizado - Aplicativo Bancário

**Data de Geração:** {datetime.now().strftime("%d/%m/%Y %H:%M")}  
**Total de Avaliações Analisadas:** {len(df)}  
**Modelo LLM Utilizado:** {model_name}

---

## Resumo Executivo

Este relatório apresenta a priorização de funcionalidades do aplicativo bancário baseada em **{len(df)} avaliações negativas** de usuários reais.

### Distribuição de Categorias

| Categoria | Quantidade | Porcentagem | Severidade Média | Prioridade |
|:----------|:-----------|:------------|:-----------------|:-----------|
"""
    
    # Tabela de distribuição de categorias
    for category, priority in sorted_priorities:
        count = category_counts[category]
        percentage = (count / len(df)) * 100
        severity = category_severity.get(category, 0)
        _, priority_level = get_priority_level(priority)
        
        report += f"| {category} | {count} | {percentage:.1f}% | {severity:.2f}/5 | {priority_level} |\n"
    
    report += "\n---\n\n## Detalhamento por Categoria\n\n"
    
    # Detalhamento de todas as categorias
    for idx, (category, priority) in enumerate(sorted_priorities, 1):
        count = category_counts[category]
        percentage = (count / len(df)) * 100
        severity = category_severity.get(category, 0)
        _, priority_level = get_priority_level(priority)
        
        report += f"""### {count}. {category} (Prioridade: {priority_level})

**Métricas:**
- Frequência: {count} avaliações ({percentage:.1f}% do total)
- Severidade Média: {severity:.2f}/5
- Score de Prioridade: {priority:.2f}

**Amostras de Avaliações:**

"""
        
        # Adiciona até 3 exemplos de avaliações dessa categoria
        if category in df.columns:
            samples = df[df[category] == 1].head(3)
            for _, row in samples.iterrows():
                text_preview = row['content'][:200] + "..." if len(str(row['content'])) > 200 else str(row['content'])
                score = int(row['score']) if pd.notna(row['score']) else 'N/A'
                report += f"- \"{text_preview}\" (Score: {score}/5)\n"
        
        report += f"\n**Ação Recomendada:**\n"
        report += f"- {RECOMMENDATIONS.get(category, 'Análise detalhada necessária.')}\n\n"
        report += "---\n\n"
    
    # Próximos passos
    report += """## Próximos Passos

1. **Revisão Técnica:** Equipes técnicas devem analisar os problemas prioritários
2. **Planejamento de Sprint:** Incluir itens críticos no próximo ciclo de desenvolvimento
3. **Monitoramento Contínuo:** Acompanhar evolução das métricas após correções
4. **Comunicação com Usuários:** Responder avaliações negativas informando sobre correções

---

**Gerado automaticamente pelo sistema de Correlação Funcional de Sentimentos**  
**TCC: Simone Rossetti - Análise de Sentimentos em Apps Bancários**
"""
    
    return report


def main():
    """Função principal."""
    parser = argparse.ArgumentParser(
        description='Gera relatório de backlog priorizado baseado na correlação funcional'
    )
    parser.add_argument(
        '--input',
        type=str,
        default=DEFAULT_INPUT_CSV,
        help=f'Arquivo CSV com resultados da correlação funcional (padrão: {DEFAULT_INPUT_CSV})'
    )
    parser.add_argument(
        '--output',
        type=str,
        default=DEFAULT_OUTPUT_MD,
        help=f'Arquivo Markdown de saída (padrão: {DEFAULT_OUTPUT_MD})'
    )
    parser.add_argument(
        '--model',
        type=str,
        default=DEFAULT_MODEL,
        help=f'Nome do modelo LLM utilizado (padrão: {DEFAULT_MODEL})'
    )
    
    args = parser.parse_args()
    
    print("\n" + "="*60)
    print("GERAÇÃO DE RELATÓRIO DE BACKLOG PRIORIZADO")
    print("="*60)
    
    # Carregar dados
    df = load_correlation_results(args.input)
    if df is None:
        return
    
    if df.empty:
        print("Erro: Arquivo CSV está vazio.")
        return
    
    # Verificar se tem pelo menos uma coluna de categoria
    has_categories = any(cat in df.columns for cat in CATEGORIES)
    if not has_categories:
        print("Erro: Nenhuma coluna de categoria encontrada no CSV.")
        print(f"   Colunas disponíveis: {', '.join(df.columns[:10])}...")
        print(f"   Esperado: colunas com nomes das categorias ({', '.join(CATEGORIES[:5])}...)")
        return
    
    # Gerar relatório
    print(f"\nGerando relatório...")
    report = generate_backlog_report(df, args.model)
    
    # Salvar relatório
    try:
        with open(args.output, 'w', encoding='utf-8') as f:
            f.write(report)
        print(f"Relatório salvo em: {args.output}")
    except Exception as e:
        print(f"Erro ao salvar relatório: {e}")
        return
    
    # Estatísticas finais
    print("\n" + "="*60)
    print("ESTATÍSTICAS FINAIS")
    print("="*60)
    
    # Contar categorias
    print(f"\nTotal de avaliações: {len(df)}")
    print("\nDistribuição de Categorias:")
    for category in CATEGORIES:
        if category in df.columns:
            count = int(df[category].sum())
            if count > 0:
                percentage = (count / len(df)) * 100
                print(f"   {category}: {count} ({percentage:.1f}%)")
    
    print("\n" + "="*60)
    print("PROCESSO CONCLUÍDO")
    print("="*60)


if __name__ == "__main__":
    main()

