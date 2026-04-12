# Guia de Uso da API SentimentalBanking

Este guia mostra como usar os endpoints da API para consultar dados de análise de sentimentos e backlog priorizado.

## Acesso à Documentação Interativa

A forma mais fácil de testar a API é através da documentação interativa Swagger:
- **URL**: http://localhost:8000/docs
- Permite testar todos os endpoints diretamente no navegador
- Mostra exemplos de requisições e respostas

## Endpoints Disponíveis

### 1. Informações da API (Root)

**GET** `/`

Retorna informações básicas sobre a API e lista de endpoints disponíveis.

**Exemplo com Python:**
```python
import requests

response = requests.get("http://localhost:8000/")
print(response.json())
```

**Exemplo com curl:**
```bash
curl http://localhost:8000/
```

---

### 2. Health Check

**GET** `/health`

Verifica o status da API e se os arquivos de dados necessários existem.

**Exemplo com Python:**
```python
import requests

response = requests.get("http://localhost:8000/health")
data = response.json()
print(f"Status: {data['status']}")
print(f"Arquivos encontrados: {data['files']}")
```

**Resposta esperada:**
```json
{
  "status": "healthy",
  "timestamp": "2026-01-06T18:57:06.095582",
  "files": {
    "sentiment_results": true,
    "functional_correlation": true,
    "ground_truth": true
  }
}
```

---

### 3. Listar Categorias Funcionais

**GET** `/categories/list`

Retorna todas as categorias funcionais disponíveis e seus pesos de impacto.

**Exemplo com Python:**
```python
import requests

response = requests.get("http://localhost:8000/categories/list")
data = response.json()
print(f"Total de categorias: {data['total_categories']}")
print(f"Categorias: {data['categories']}")
```

**Resposta esperada:**
```json
{
  "total_categories": 16,
  "categories": [
    "PIX",
    "Login/Autenticação",
    "Performance",
    ...
  ],
  "impact_weights": {
    "PIX": 1.0,
    "Login/Autenticação": 1.0,
    ...
  }
}
```

---

### 4. Obter Resultados de Análise de Sentimentos

**GET** `/sentiment/results`

Retorna os resultados da análise de sentimentos já processados.

**Parâmetros:**
- `format` (opcional): Formato de retorno - `json` (padrão) ou `csv`
- `app_name` (opcional): Filtrar por nome do app (ex: "Santander", "Bradesco")
- `sentiment` (opcional): Filtrar por sentimento - `positive`, `negative` ou `neutral`
- `limit` (opcional): Limitar número de resultados retornados

**Exemplos:**

**Obter todas as avaliações negativas do Santander:**
```python
import requests

url = "http://localhost:8000/sentiment/results"
params = {
    "app_name": "Santander",
    "sentiment": "negative",
    "format": "json"
}

response = requests.get(url, params=params)
data = response.json()
print(f"Total: {data['total']} avaliações")
for review in data['results'][:5]:  # Primeiras 5
    print(f"- {review['content'][:50]}... ({review['sentiment_label']})")
```

**Obter apenas 10 avaliações positivas:**
```python
import requests

url = "http://localhost:8000/sentiment/results"
params = {
    "sentiment": "positive",
    "limit": 10
}

response = requests.get(url, params=params)
data = response.json()
print(f"Total retornado: {data['total']}")
```

**Baixar resultados em CSV:**
```python
import requests

url = "http://localhost:8000/sentiment/results"
params = {"format": "csv"}

response = requests.get(url, params=params)
with open("sentiment_results.csv", "wb") as f:
    f.write(response.content)
print("Arquivo CSV salvo!")
```

**Exemplo com curl:**
```bash
# JSON com filtros
curl "http://localhost:8000/sentiment/results?app_name=Santander&sentiment=negative&limit=5"

# CSV
curl "http://localhost:8000/sentiment/results?format=csv" -o sentiment_results.csv
```

**Resposta esperada (JSON):**
```json
{
  "total": 136,
  "filters": {
    "app_name": "Santander",
    "sentiment": "negative",
    "limit": null
  },
  "results": [
    {
      "content": "atualização do aplicativo está muito pesada.",
      "score": 2,
      "date": "2026-01-05 16:37:04",
      "version": "25.5.1.0",
      "app_name": "Santander",
      "sentiment_label": "negative",
      "sentiment_score": 0.9218244552612304
    },
    ...
  ]
}
```

---

### 5. Obter Resultados de Categorização Funcional

**GET** `/functional/results`

Retorna os resultados da categorização funcional das avaliações negativas.

**Parâmetros:**
- `format` (opcional): Formato de retorno - `json` (padrão) ou `csv`
- `app_name` (opcional): Filtrar por nome do app
- `category` (opcional): Filtrar por categoria funcional (ex: "PIX", "Performance")

**Exemplos:**

**Obter todas as avaliações categorizadas como "Performance":**
```python
import requests

url = "http://localhost:8000/functional/results"
params = {
    "category": "Performance",
    "format": "json"
}

response = requests.get(url, params=params)
data = response.json()
print(f"Total de avaliações de Performance: {data['total']}")
```

**Obter avaliações do Bradesco relacionadas a "PIX":**
```python
import requests

url = "http://localhost:8000/functional/results"
params = {
    "app_name": "Bradesco",
    "category": "PIX"
}

response = requests.get(url, params=params)
data = response.json()
print(f"Total: {data['total']}")
```

---

### 6. Obter Backlog Priorizado

**GET** `/backlog/prioritized`

Retorna o backlog priorizado baseado em frequência, severidade e impacto.

**Parâmetros:**
- `app_name` (opcional): Filtrar por nome do app
- `min_priority` (opcional): Prioridade mínima (0.0 a 1.0) - padrão: 0.0
- `limit` (opcional): Limitar número de categorias retornadas

**Exemplos:**

**Obter top 5 categorias prioritárias:**
```python
import requests

url = "http://localhost:8000/backlog/prioritized"
params = {"limit": 5}

response = requests.get(url, params=params)
data = response.json()

print(f"Total de categorias: {data['total_categories']}")
print(f"Total de avaliações: {data['total_reviews']}")
print("\nTop 5 Categorias Prioritárias:")
for item in data['backlog']:
    print(f"\n{item['category']} ({item['priority_level']})")
    print(f"  Score: {item['priority_score']}")
    print(f"  Frequência: {item['frequency']} ({item['frequency_percentage']}%)")
    print(f"  Severidade média: {item['average_severity']}/5")
    print(f"  Recomendação: {item['recommendation']}")
```

**Obter apenas categorias críticas (prioridade >= 0.7):**
```python
import requests

url = "http://localhost:8000/backlog/prioritized"
params = {
    "min_priority": 0.7
}

response = requests.get(url, params=params)
data = response.json()
print(f"Categorias críticas: {data['total_categories']}")
```

**Obter backlog apenas do Santander:**
```python
import requests

url = "http://localhost:8000/backlog/prioritized"
params = {
    "app_name": "Santander",
    "limit": 10
}

response = requests.get(url, params=params)
data = response.json()
```

**Exemplo com curl:**
```bash
curl "http://localhost:8000/backlog/prioritized?limit=5"
```

**Resposta esperada:**
```json
{
  "total_categories": 5,
  "total_reviews": 218,
  "filters": {
    "app_name": null,
    "min_priority": 0.0
  },
  "backlog": [
    {
      "category": "Performance",
      "priority_score": 0.6368,
      "priority_level": "ALTA",
      "frequency": 93,
      "frequency_percentage": 42.66,
      "average_severity": 1.73,
      "recommendation": "Executar profiling do app. Otimizar tempo de inicialização e identificar memory leaks."
    },
    ...
  ]
}
```

---

### 7. Analisar Sentimentos de Novas Avaliações

**POST** `/sentiment/analyze`

Analisa sentimentos de um lote de avaliações fornecidas.

**Exemplo com Python:**
```python
import requests

url = "http://localhost:8000/sentiment/analyze"

data = {
    "reviews": [
        {
            "content": "App muito lento, trava constantemente",
            "score": 1,
            "app_name": "Santander"
        },
        {
            "content": "Excelente aplicativo, muito fácil de usar",
            "score": 5,
            "app_name": "Bradesco"
        }
    ]
}

response = requests.post(url, json=data)
result = response.json()
print(f"Total analisado: {result['total_reviews']}")
for review in result['results']:
    print(f"- {review['content'][:50]}... -> {review['sentiment_label']}")
```

---

## Script Completo de Exemplo

Aqui está um script Python completo que demonstra o uso de vários endpoints:

```python
"""
Exemplo completo de uso da API SentimentalBanking
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
    response = requests.get(f"{BASE_URL}/health")
    health = response.json()
    print(f"   Status: {health['status']}")
    print(f"   Arquivos: {health['files']}")
    
    # 2. Listar categorias
    print("\n2. Listando categorias funcionais...")
    response = requests.get(f"{BASE_URL}/categories/list")
    categories = response.json()
    print(f"   Total de categorias: {categories['total_categories']}")
    print(f"   Primeiras 5: {categories['categories'][:5]}")
    
    # 3. Obter avaliações negativas do Santander
    print("\n3. Obtendo avaliações negativas do Santander...")
    params = {
        "app_name": "Santander",
        "sentiment": "negative",
        "limit": 5
    }
    response = requests.get(f"{BASE_URL}/sentiment/results", params=params)
    sentiment_data = response.json()
    print(f"   Total encontrado: {sentiment_data['total']}")
    print(f"   Primeiras 3 avaliações:")
    for review in sentiment_data['results'][:3]:
        print(f"     - {review['content'][:60]}...")
    
    # 4. Obter backlog priorizado
    print("\n4. Obtendo backlog priorizado (top 3)...")
    params = {"limit": 3}
    response = requests.get(f"{BASE_URL}/backlog/prioritized", params=params)
    backlog = response.json()
    print(f"   Total de categorias: {backlog['total_categories']}")
    print(f"   Top 3 categorias:")
    for item in backlog['backlog']:
        print(f"     - {item['category']}: {item['priority_level']} "
              f"({item['frequency_percentage']}%)")
    
    # 5. Obter avaliações de uma categoria específica
    print("\n5. Obtendo avaliações da categoria 'Performance'...")
    params = {"category": "Performance", "limit": 3}
    response = requests.get(f"{BASE_URL}/functional/results", params=params)
    functional_data = response.json()
    print(f"   Total encontrado: {functional_data['total']}")
    
    print("\n" + "="*60)
    print("EXEMPLO CONCLUÍDO")
    print("="*60)

if __name__ == "__main__":
    exemplo_completo()
```

---

## Casos de Uso Comuns

### Caso 1: Dashboard de Métricas

```python
import requests

def obter_metricas_dashboard():
    """Obtém métricas para exibir em um dashboard."""
    
    # Estatísticas gerais
    health = requests.get("http://localhost:8000/health").json()
    
    # Total de avaliações por sentimento
    sentiment_stats = {}
    for sentiment in ["positive", "negative", "neutral"]:
        response = requests.get(
            "http://localhost:8000/sentiment/results",
            params={"sentiment": sentiment}
        )
        sentiment_stats[sentiment] = response.json()['total']
    
    # Top 5 categorias prioritárias
    backlog = requests.get(
        "http://localhost:8000/backlog/prioritized",
        params={"limit": 5}
    ).json()
    
    return {
        "health": health,
        "sentiment_distribution": sentiment_stats,
        "top_priorities": backlog['backlog']
    }
```

### Caso 2: Relatório por App

```python
import requests

def relatorio_por_app(app_name):
    """Gera relatório completo para um app específico."""
    
    # Avaliações por sentimento
    sentimentos = {}
    for sentiment in ["positive", "negative", "neutral"]:
        response = requests.get(
            "http://localhost:8000/sentiment/results",
            params={"app_name": app_name, "sentiment": sentiment}
        )
        sentimentos[sentiment] = response.json()['total']
    
    # Backlog priorizado do app
    backlog = requests.get(
        "http://localhost:8000/backlog/prioritized",
        params={"app_name": app_name}
    ).json()
    
    return {
        "app": app_name,
        "sentimentos": sentimentos,
        "backlog": backlog['backlog']
    }
```

---

## Tratamento de Erros

Sempre verifique o status code da resposta:

```python
import requests

response = requests.get("http://localhost:8000/sentiment/results")

if response.status_code == 200:
    data = response.json()
    print("Sucesso!")
elif response.status_code == 404:
    print("Arquivo não encontrado")
elif response.status_code == 500:
    print(f"Erro do servidor: {response.json()['detail']}")
else:
    print(f"Erro: {response.status_code}")
```

---

## Documentação Interativa

A forma mais fácil de explorar e testar a API é através da documentação Swagger:

1. Acesse: http://localhost:8000/docs
2. Clique em qualquer endpoint para expandir
3. Clique em "Try it out"
4. Preencha os parâmetros desejados
5. Clique em "Execute"
6. Veja a resposta diretamente na página

---

## Próximos Passos

- Explore a documentação interativa em `/docs`
- Teste os endpoints com seus próprios dados
- Integre a API com suas aplicações
- Use os filtros para análises específicas

