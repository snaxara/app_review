"""
Exemplo completo de uso da API SentimentalBanking
Execute este script para ver exemplos práticos de como usar os endpoints
"""
import requests
import json

BASE_URL = "http://localhost:8000"

def exemplo_completo():
    """Demonstra o uso de vários endpoints da API."""
    
    print("="*60)
    print("EXEMPLO DE USO DA API SENTIMENTALBANKING")
    print("="*60)
    
    # 1. Verificar saúde da API
    print("\n1. Verificando saúde da API...")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        health = response.json()
        print(f"   Status: {health['status']}")
        print(f"   Arquivos encontrados:")
        for file, exists in health['files'].items():
            status = "OK" if exists else "NÃO ENCONTRADO"
            print(f"     - {file}: {status}")
    except Exception as e:
        print(f"   ERRO: Não foi possível conectar à API: {e}")
        print("   Certifique-se de que a API está rodando em http://localhost:8000")
        return
    
    # 2. Listar categorias
    print("\n2. Listando categorias funcionais...")
    response = requests.get(f"{BASE_URL}/categories/list")
    categories = response.json()
    print(f"   Total de categorias: {categories['total_categories']}")
    print(f"   Primeiras 5 categorias: {', '.join(categories['categories'][:5])}")
    
    # 3. Obter avaliações negativas do Santander
    print("\n3. Obtendo avaliações negativas do Santander...")
    params = {
        "app_name": "Santander",
        "sentiment": "negative",
        "limit": 5
    }
    response = requests.get(f"{BASE_URL}/sentiment/results", params=params)
    sentiment_data = response.json()
    print(f"   Total encontrado: {sentiment_data['total']} avaliações")
    if sentiment_data['results']:
        print(f"   Primeiras 3 avaliações:")
        for idx, review in enumerate(sentiment_data['results'][:3], 1):
            content_preview = review['content'][:60] + "..." if len(review['content']) > 60 else review['content']
            print(f"     {idx}. {content_preview} (Score: {review['score']}/5)")
    
    # 4. Obter backlog priorizado
    print("\n4. Obtendo backlog priorizado (top 5)...")
    params = {"limit": 5}
    response = requests.get(f"{BASE_URL}/backlog/prioritized", params=params)
    backlog = response.json()
    print(f"   Total de categorias: {backlog['total_categories']}")
    print(f"   Total de avaliações analisadas: {backlog['total_reviews']}")
    print(f"   Top 5 categorias prioritárias:")
    for idx, item in enumerate(backlog['backlog'], 1):
        print(f"     {idx}. {item['category']}")
        print(f"        Prioridade: {item['priority_level']} (Score: {item['priority_score']:.4f})")
        print(f"        Frequência: {item['frequency']} avaliações ({item['frequency_percentage']}%)")
        print(f"        Severidade média: {item['average_severity']}/5")
        print(f"        Recomendação: {item['recommendation'][:80]}...")
    
    # 5. Comparar apps
    print("\n5. Comparando avaliações entre apps...")
    apps = ["Santander", "Bradesco"]
    comparacao = {}
    for app in apps:
        for sentiment in ["positive", "negative", "neutral"]:
            try:
                response = requests.get(
                    f"{BASE_URL}/sentiment/results",
                    params={"app_name": app, "sentiment": sentiment}
                )
                if response.status_code == 200:
                    data = response.json()
                    count = data.get('total', 0)
                    if app not in comparacao:
                        comparacao[app] = {}
                    comparacao[app][sentiment] = count
                else:
                    print(f"   Erro ao obter dados para {app} - {sentiment}: {response.status_code}")
            except Exception as e:
                print(f"   Erro ao processar {app} - {sentiment}: {e}")
    
    if comparacao:
        print("   Distribuição de sentimentos por app:")
        for app, sentimentos in comparacao.items():
            total = sum(sentimentos.values())
            if total > 0:
                print(f"   {app}:")
                for sentiment, count in sentimentos.items():
                    pct = (count / total * 100) if total > 0 else 0
                    print(f"     {sentiment.capitalize()}: {count} ({pct:.1f}%)")
    
    print("\n" + "="*60)
    print("EXEMPLO CONCLUÍDO")
    print("="*60)
    print("\nDica: Acesse http://localhost:8000/docs para documentação interativa!")

if __name__ == "__main__":
    exemplo_completo()

