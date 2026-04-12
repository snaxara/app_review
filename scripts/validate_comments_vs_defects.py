"""
Validação cruzada: Compara issues extraídas dos comentários com defeitos reais em produção
Mantém abordagem genérica, aplicável a qualquer app bancário
"""

import pandas as pd
from collections import Counter
import re
import os

def normalize_text(text):
    """Normaliza texto para comparação"""
    if pd.isna(text):
        return ""
    text = str(text).lower()
    # Remove acentos básicos e caracteres especiais
    text = re.sub(r'[^\w\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def extract_keywords(text):
    """Extrai palavras-chave relevantes do texto"""
    if pd.isna(text):
        return []
    
    text = normalize_text(text)
    
    # Palavras-chave relevantes para problemas técnicos
    keywords = []
    words = text.split()
    
    # Filtrar palavras muito comuns
    stop_words = {'o', 'a', 'de', 'do', 'da', 'em', 'no', 'na', 'para', 'com', 'que', 'não', 'nao', 'defeito', 'sistema'}
    
    for word in words:
        if len(word) > 3 and word not in stop_words:
            keywords.append(word)
    
    return keywords

def load_issues_from_graph():
    """Carrega issues do grafo de conhecimento (se disponível)"""
    # Tentar carregar issues do CSV exportado ou do grafo
    issues_file = 'reports/model_data_gpt-4o-2024-08-06.csv'
    
    if os.path.exists(issues_file):
        try:
            # Tentar diferentes separadores
            for sep in [';', ',', '\t']:
                try:
                    df_issues = pd.read_csv(issues_file, encoding='utf-8', sep=sep)
                    if 'issue' in df_issues.columns:
                        return df_issues['issue'].dropna().unique().tolist()
                except:
                    continue
        except Exception as e:
            print(f"Erro ao carregar issues: {e}")
            return []
    
    # Tentar carregar diretamente do Neo4j se disponível
    try:
        from scripts.knowledge_graph.graph_manager import GraphManager
        graph = GraphManager()
        query = """
        MATCH (e)
        WHERE 'Issue' IN labels(e)
        RETURN DISTINCT e.name AS issue
        """
        result = graph.execute_query(query)
        if result:
            return [r.get('issue', '') for r in result if r.get('issue')]
    except Exception as e:
        print(f"Erro ao carregar do grafo: {e}")
    
    return []

def validate_cross_reference():
    """Valida cruzada entre comentários e defeitos - abordagem genérica"""
    
    print("=" * 80)
    print("VALIDACAO CRUZADA: COMENTARIOS vs DEFEITOS EM PRODUCAO")
    print("Abordagem generica - aplicavel a qualquer app bancario")
    print("=" * 80)
    
    # Carregar dados
    df_prod = pd.read_csv('tcc/defeitos_producao.csv', sep=';', encoding='utf-8')
    
    # Filtrar APENAS defeitos relacionados ao app móvel
    # Sistemas que são especificamente do app móvel (não sistemas internos)
    app_systems = ['SINBC', 'SIACC', 'SIGLM', 'SIPPG', 'SIGMP', 'SIGPM']
    df_app_defects = df_prod[df_prod['Sistema'].isin(app_systems)].copy()
    
    print(f"\n1. DEFEITOS RELACIONADOS AO APP MOVEL EM PRODUCAO: {len(df_app_defects)}")
    print("-" * 80)
    
    # Extrair keywords dos defeitos (sem mencionar siglas específicas)
    defect_keywords = []
    defect_descriptions = []
    
    for idx, row in df_app_defects.iterrows():
        nome = normalize_text(row['Nome'])
        # Remover siglas específicas para manter genérico
        nome = re.sub(r'\b(sinbc|siacc|siglm|sippg|sigmp|sigpm|gecar|gesat)\b', '', nome, flags=re.IGNORECASE)
        keywords = extract_keywords(nome)
        defect_keywords.extend(keywords)
        defect_descriptions.append(nome)
    
    # Contar frequência de keywords
    keyword_counts = Counter(defect_keywords)
    
    print("\nTop 20 palavras-chave mais frequentes nos defeitos do app:")
    for word, count in keyword_counts.most_common(20):
        print(f"  {word}: {count}")
    
    # Análise de criticidade
    print("\n2. DISTRIBUICAO DE CRITICIDADE DOS DEFEITOS DO APP")
    print("-" * 80)
    crit_app = df_app_defects['Criticidade'].value_counts()
    print(crit_app)
    
    # Análise por comunidade (genérica)
    print("\n3. DISTRIBUICAO POR AREA FUNCIONAL (DEFEITOS DO APP)")
    print("-" * 80)
    comm_app = df_app_defects['Comunidade'].value_counts()
    print(comm_app)
    
    # Carregar issues dos comentários (se disponível)
    print("\n4. COMPARACAO COM ISSUES EXTRAIDAS DOS COMENTARIOS")
    print("-" * 80)
    
    issues_from_comments = load_issues_from_graph()
    
    if issues_from_comments:
        print(f"Issues extraidas dos comentarios: {len(issues_from_comments)}")
        
        # Normalizar issues dos comentários
        comment_keywords = []
        for issue in issues_from_comments:
            if pd.notna(issue):
                keywords = extract_keywords(str(issue))
                comment_keywords.extend(keywords)
        
        comment_keyword_counts = Counter(comment_keywords)
        
        print("\nTop 20 palavras-chave mais frequentes nas issues dos comentarios:")
        for word, count in comment_keyword_counts.most_common(20):
            print(f"  {word}: {count}")
        
        # Encontrar correspondências
        print("\n5. CORRESPONDENCIAS ENCONTRADAS")
        print("-" * 80)
        
        common_keywords = set(keyword_counts.keys()) & set(comment_keyword_counts.keys())
        
        print(f"Palavras-chave em comum: {len(common_keywords)}")
        print("\nTop 10 palavras-chave em comum (problemas identificados tanto em defeitos quanto em comentarios):")
        common_with_counts = [(kw, keyword_counts[kw] + comment_keyword_counts[kw]) 
                             for kw in common_keywords]
        common_with_counts.sort(key=lambda x: x[1], reverse=True)
        
        for word, total_count in common_with_counts[:10]:
            defect_count = keyword_counts[word]
            comment_count = comment_keyword_counts[word]
            print(f"  {word}: {defect_count} defeitos + {comment_count} comentarios = {total_count} total")
        
        # Calcular métricas de correspondência
        print("\n6. METRICAS DE VALIDACAO")
        print("-" * 80)
        
        total_defect_keywords = len(set(defect_keywords))
        total_comment_keywords = len(set(comment_keywords))
        overlap = len(common_keywords)
        
        if total_defect_keywords > 0:
            precision = (overlap / total_comment_keywords * 100) if total_comment_keywords > 0 else 0
            recall = (overlap / total_defect_keywords * 100) if total_defect_keywords > 0 else 0
            
            print(f"Total keywords unicas em defeitos: {total_defect_keywords}")
            print(f"Total keywords unicas em comentarios: {total_comment_keywords}")
            print(f"Keywords em comum: {overlap}")
            print(f"Taxa de correspondencia (comentarios): {precision:.1f}%")
            print(f"Taxa de cobertura (defeitos): {recall:.1f}%")
    else:
        print("Arquivo de issues dos comentarios nao encontrado.")
        print("Execute primeiro o processamento dos comentarios para gerar o arquivo.")
    
    # Salvar análise
    print("\n7. GERANDO RELATORIOS")
    print("-" * 80)
    
    # Defeitos do app por criticidade
    app_analysis = df_app_defects.groupby(['Criticidade']).size().reset_index(name='Quantidade')
    app_analysis.to_csv('reports/defeitos_app_por_criticidade.csv', sep=';', index=False, encoding='utf-8')
    print("OK - Relatorio: reports/defeitos_app_por_criticidade.csv")
    
    # Keywords dos defeitos (genérico)
    keywords_df = pd.DataFrame(keyword_counts.most_common(50), columns=['Keyword', 'Frequencia'])
    keywords_df.to_csv('reports/keywords_defeitos_app_generico.csv', sep=';', index=False, encoding='utf-8')
    print("OK - Relatorio: reports/keywords_defeitos_app_generico.csv")
    
    # Descriptions dos defeitos (sem siglas)
    descriptions_df = pd.DataFrame({
        'Descricao': defect_descriptions[:100]  # Primeiros 100
    })
    descriptions_df.to_csv('reports/descricoes_defeitos_app_generico.csv', sep=';', index=False, encoding='utf-8')
    print("OK - Relatorio: reports/descricoes_defeitos_app_generico.csv")
    
    print("\n" + "=" * 80)
    print("VALIDACAO CONCLUIDA")
    print("=" * 80)
    print("\nNOTA: Esta analise mantem abordagem generica, aplicavel a qualquer app bancario.")
    print("Nao cria mapeamentos especificos de siglas ou sistemas internos.")
    
    return df_app_defects, keyword_counts

if __name__ == "__main__":
    validate_cross_reference()
