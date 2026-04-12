"""
Teste simples da API SentimentalBanking
"""
import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_endpoint(name, url, method="GET", data=None):
    """Testa um endpoint da API."""
    print(f"\n{'='*60}")
    print(f"Testando: {name}")
    print(f"URL: {url}")
    print(f"{'='*60}")
    
    try:
        if method == "GET":
            response = requests.get(url, timeout=10)
        else:
            response = requests.post(url, json=data, timeout=10)
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            try:
                result = response.json()
                print(f"Resposta (primeiros 500 caracteres):")
                print(json.dumps(result, indent=2, ensure_ascii=False)[:500])
            except:
                print(f"Resposta (texto): {response.text[:500]}")
        else:
            print(f"Erro: {response.text[:500]}")
            
    except requests.exceptions.ConnectionError:
        print("ERRO: Não foi possível conectar à API.")
        print("Certifique-se de que a API está rodando em http://localhost:8000")
        return False
    except Exception as e:
        print(f"ERRO: {e}")
        return False
    
    return True

if __name__ == "__main__":
    print("="*60)
    print("TESTES DA API SENTIMENTALBANKING")
    print("="*60)
    
    # Aguardar API iniciar
    print("\nAguardando API iniciar...")
    time.sleep(3)
    
    # Testar endpoints
    tests = [
        ("Root", f"{BASE_URL}/"),
        ("Health", f"{BASE_URL}/health"),
        ("Categorias", f"{BASE_URL}/categories/list"),
        ("Resultados Sentimentos (JSON)", f"{BASE_URL}/sentiment/results?format=json&limit=3"),
        ("Backlog Priorizado", f"{BASE_URL}/backlog/prioritized?limit=5"),
    ]
    
    results = []
    for name, url in tests:
        success = test_endpoint(name, url)
        results.append((name, success))
        time.sleep(1)
    
    # Resumo
    print("\n" + "="*60)
    print("RESUMO DOS TESTES")
    print("="*60)
    for name, success in results:
        status = "OK" if success else "FALHOU"
        print(f"{name}: {status}")
    
    print("\n" + "="*60)
    print("TESTES CONCLUÍDOS")
    print("="*60)

