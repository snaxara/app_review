"""
Script de teste simples para a API SentimentalBanking
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_health():
    """Testa o endpoint de health check."""
    print("Testando /health...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    print()

def test_root():
    """Testa o endpoint raiz."""
    print("Testando /...")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Resposta: {json.dumps(response.json(), indent=2)}")
    print()

def test_categories():
    """Testa o endpoint de categorias."""
    print("Testando /categories/list...")
    response = requests.get(f"{BASE_URL}/categories/list")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total de categorias: {data['total_categories']}")
        print(f"Primeiras 5 categorias: {data['categories'][:5]}")
    else:
        print(f"Erro: {response.json()}")
    print()

def test_sentiment_results():
    """Testa o endpoint de resultados de sentimentos."""
    print("Testando /sentiment/results...")
    response = requests.get(f"{BASE_URL}/sentiment/results?format=json&limit=5")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total de resultados: {data.get('total', 0)}")
        if data.get('results'):
            print(f"Primeiro resultado: {data['results'][0]}")
    else:
        print(f"Erro: {response.json()}")
    print()

def test_backlog():
    """Testa o endpoint de backlog priorizado."""
    print("Testando /backlog/prioritized...")
    response = requests.get(f"{BASE_URL}/backlog/prioritized?limit=5")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total de categorias no backlog: {data['total_categories']}")
        print(f"Total de reviews: {data['total_reviews']}")
        if data.get('backlog'):
            print("\nTop 3 categorias prioritárias:")
            for item in data['backlog'][:3]:
                print(f"  - {item['category']}: {item['priority_level']} (Score: {item['priority_score']})")
    else:
        print(f"Erro: {response.json()}")
    print()

def test_metrics():
    """Testa o endpoint de métricas."""
    print("Testando /metrics/validation...")
    response = requests.get(f"{BASE_URL}/metrics/validation")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Total de amostras: {data['total_samples']}")
        print(f"Métricas: {json.dumps(data['metrics'], indent=2)}")
    else:
        print(f"Erro: {response.json()}")
    print()

if __name__ == "__main__":
    print("="*60)
    print("TESTES DA API SENTIMENTALBANKING")
    print("="*60)
    print()
    
    try:
        test_root()
        test_health()
        test_categories()
        test_sentiment_results()
        test_backlog()
        test_metrics()
        
        print("="*60)
        print("TESTES CONCLUÍDOS")
        print("="*60)
    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar à API.")
        print("Certifique-se de que a API está rodando em http://localhost:8000")
        print("Execute: python scripts/api_sentimental_banking.py")
    except Exception as e:
        print(f"ERRO: {e}")

