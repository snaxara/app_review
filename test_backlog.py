"""
Teste específico para o endpoint de Backlog Priorizado
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def test_backlog_basico():
    """Testa o backlog básico sem filtros."""
    print("="*70)
    print("TESTE 1: Backlog Priorizado - Todos os Apps")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/backlog/prioritized")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal de categorias: {data['total_categories']}")
        print(f"Total de avaliações analisadas: {data['total_reviews']}")
        print(f"\nFiltros aplicados: {data['filters']}")
        
        # Criar tabela formatada
        print("\n" + "-" * 100)
        print(f"{'Categoria':<25} {'Prioridade':<12} {'Score':<10} {'Freq.':<8} {'%':<8} {'Severidade':<10}")
        print("-" * 100)
        for item in data['backlog']:
            print(f"{item['category']:<25} {item['priority_level']:<12} "
                  f"{item['priority_score']:<10.4f} {item['frequency']:<8} "
                  f"{item['frequency_percentage']:<8.2f} {item['average_severity']:<10.2f}")
        print("-" * 100)
        
        return data
    else:
        print(f"ERRO: Status {response.status_code}")
        print(response.text)
        return None

def test_backlog_limitado():
    """Testa o backlog com limite de categorias."""
    print("\n" + "="*70)
    print("TESTE 2: Backlog Priorizado - Top 5 Categorias")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/backlog/prioritized?limit=5")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal de categorias retornadas: {data['total_categories']}")
        
        print("\nTop 5 Categorias Prioritárias:")
        print("-" * 70)
        for idx, item in enumerate(data['backlog'], 1):
            print(f"\n{idx}. {item['category']} ({item['priority_level']})")
            print(f"   Score de Prioridade: {item['priority_score']:.4f}")
            print(f"   Frequência: {item['frequency']} avaliações ({item['frequency_percentage']:.2f}%)")
            print(f"   Severidade Média: {item['average_severity']:.2f}/5")
            print(f"   Recomendação: {item['recommendation']}")
        
        return data
    else:
        print(f"ERRO: Status {response.status_code}")
        return None

def test_backlog_por_app(app_name):
    """Testa o backlog filtrado por app."""
    print("\n" + "="*70)
    print(f"TESTE 3: Backlog Priorizado - {app_name}")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/backlog/prioritized?app_name={app_name}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal de categorias: {data['total_categories']}")
        print(f"Total de avaliações do {app_name}: {data['total_reviews']}")
        
        if data['backlog']:
            print(f"\nCategorias Prioritárias para {app_name}:")
            print("-" * 70)
            for idx, item in enumerate(data['backlog'][:5], 1):
                print(f"\n{idx}. {item['category']} ({item['priority_level']})")
                print(f"   Frequência: {item['frequency']} ({item['frequency_percentage']:.2f}%)")
                print(f"   Severidade: {item['average_severity']:.2f}/5")
        else:
            print(f"Nenhuma categoria encontrada para {app_name}")
        
        return data
    else:
        print(f"ERRO: Status {response.status_code}")
        print(response.text)
        return None

def test_backlog_prioridade_minima():
    """Testa o backlog com prioridade mínima."""
    print("\n" + "="*70)
    print("TESTE 4: Backlog Priorizado - Apenas Categorias Críticas (>= 0.5)")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/backlog/prioritized?min_priority=0.5")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nTotal de categorias com prioridade >= 0.5: {data['total_categories']}")
        
        if data['backlog']:
            print("\nCategorias de Alta Prioridade:")
            print("-" * 70)
            for item in data['backlog']:
                print(f"\n{item['category']} ({item['priority_level']})")
                print(f"  Score: {item['priority_score']:.4f}")
                print(f"  Frequência: {item['frequency']} ({item['frequency_percentage']:.2f}%)")
        else:
            print("Nenhuma categoria com prioridade >= 0.5 encontrada")
        
        return data
    else:
        print(f"ERRO: Status {response.status_code}")
        return None

def test_backlog_combinado():
    """Testa o backlog com múltiplos filtros."""
    print("\n" + "="*70)
    print("TESTE 5: Backlog Priorizado - Filtros Combinados")
    print("="*70)
    
    # Top 3 categorias críticas do Santander
    response = requests.get(
        f"{BASE_URL}/backlog/prioritized",
        params={
            "app_name": "Santander",
            "min_priority": 0.4,
            "limit": 3
        }
    )
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nFiltros aplicados:")
        print(f"  - App: {data['filters']['app_name']}")
        print(f"  - Prioridade mínima: {data['filters']['min_priority']}")
        print(f"  - Limite: 3")
        print(f"\nTotal de categorias retornadas: {data['total_categories']}")
        print(f"Total de avaliações: {data['total_reviews']}")
        
        if data['backlog']:
            print("\nTop 3 Categorias:")
            for idx, item in enumerate(data['backlog'], 1):
                print(f"\n{idx}. {item['category']}")
                print(f"   Prioridade: {item['priority_level']} (Score: {item['priority_score']:.4f})")
                print(f"   Frequência: {item['frequency']} avaliações")
        
        return data
    else:
        print(f"ERRO: Status {response.status_code}")
        return None

def comparar_apps():
    """Compara o backlog entre os dois apps."""
    print("\n" + "="*70)
    print("TESTE 6: Comparação de Backlog entre Apps")
    print("="*70)
    
    apps = ["Santander", "Bradesco"]
    resultados = {}
    
    for app in apps:
        response = requests.get(f"{BASE_URL}/backlog/prioritized?app_name={app}&limit=5")
        if response.status_code == 200:
            resultados[app] = response.json()
    
    if len(resultados) == 2:
        print("\nComparação das Top 5 Categorias por App:\n")
        
        # Criar tabela comparativa
        print("\n" + "-" * 80)
        print(f"{'Posição':<10} {'Santander':<35} {'Bradesco':<35}")
        print("-" * 80)
        
        max_categories = max(len(r['backlog']) for r in resultados.values())
        for i in range(max_categories):
            row = []
            for app in apps:
                if i < len(resultados[app]['backlog']):
                    item = resultados[app]['backlog'][i]
                    row.append(f"{item['category']} ({item['priority_level']}, {item['frequency']} aval.)")
                else:
                    row.append("-")
            
            print(f"{i+1:<10} {row[0]:<35} {row[1]:<35}")
        print("-" * 80)
    
    return resultados

def estatisticas_gerais():
    """Mostra estatísticas gerais do backlog."""
    print("\n" + "="*70)
    print("TESTE 7: Estatísticas Gerais do Backlog")
    print("="*70)
    
    response = requests.get(f"{BASE_URL}/backlog/prioritized")
    
    if response.status_code == 200:
        data = response.json()
        
        # Calcular estatísticas
        total_reviews = data['total_reviews']
        total_categories = data['total_categories']
        
        # Distribuição por nível de prioridade
        priority_levels = {}
        for item in data['backlog']:
            level = item['priority_level']
            if level not in priority_levels:
                priority_levels[level] = {'count': 0, 'total_freq': 0}
            priority_levels[level]['count'] += 1
            priority_levels[level]['total_freq'] += item['frequency']
        
        print(f"\nTotal de Avaliações Analisadas: {total_reviews}")
        print(f"Total de Categorias Identificadas: {total_categories}")
        
        print("\nDistribuição por Nível de Prioridade:")
        print("-" * 70)
        for level in ['CRITICA', 'ALTA', 'MEDIA', 'BAIXA']:
            if level in priority_levels:
                info = priority_levels[level]
                pct = (info['total_freq'] / total_reviews * 100) if total_reviews > 0 else 0
                print(f"{level:10} - {info['count']:2} categorias, "
                      f"{info['total_freq']:3} avaliações ({pct:5.2f}%)")
        
        # Categoria mais frequente
        if data['backlog']:
            mais_frequente = max(data['backlog'], key=lambda x: x['frequency'])
            print(f"\nCategoria Mais Frequente: {mais_frequente['category']}")
            print(f"  - {mais_frequente['frequency']} avaliações ({mais_frequente['frequency_percentage']:.2f}%)")
        
        # Categoria mais severa
        if data['backlog']:
            mais_severa = min(data['backlog'], key=lambda x: x['average_severity'])
            print(f"\nCategoria Mais Severa: {mais_severa['category']}")
            print(f"  - Severidade média: {mais_severa['average_severity']:.2f}/5")
        
        return data
    else:
        print(f"ERRO: Status {response.status_code}")
        return None

def main():
    """Executa todos os testes."""
    print("\n" + "="*70)
    print("TESTES DO ENDPOINT DE BACKLOG PRIORIZADO")
    print("="*70)
    
    try:
        # Verificar se API está rodando
        health = requests.get(f"{BASE_URL}/health", timeout=5)
        if health.status_code != 200:
            print("ERRO: API não está respondendo corretamente")
            return
    except Exception as e:
        print(f"ERRO: Não foi possível conectar à API: {e}")
        print("Certifique-se de que a API está rodando em http://localhost:8000")
        return
    
    # Executar testes
    test_backlog_basico()
    test_backlog_limitado()
    test_backlog_por_app("Santander")
    test_backlog_por_app("Bradesco")
    test_backlog_prioridade_minima()
    test_backlog_combinado()
    comparar_apps()
    estatisticas_gerais()
    
    print("\n" + "="*70)
    print("TODOS OS TESTES CONCLUÍDOS")
    print("="*70)
    print("\nDica: Acesse http://localhost:8000/docs para testar interativamente!")

if __name__ == "__main__":
    main()

