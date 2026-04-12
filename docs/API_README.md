# API SentimentalBanking - Documentação

## Visão Geral

A API SentimentalBanking é uma API REST desenvolvida em Python usando FastAPI que permite processar avaliações de aplicativos bancários, realizar análise de sentimentos, categorização funcional e geração de backlog priorizado.

## Instalação

### Requisitos

```bash
pip install fastapi uvicorn pandas scikit-learn transformers
```

Ou instale todas as dependências do projeto:

```bash
pip install -r requirements.txt
```

### Executar a API

```bash
cd scripts
python api_sentimental_banking.py
```

A API estará disponível em: `http://localhost:8000`

### Documentação Interativa

Acesse a documentação Swagger em: `http://localhost:8000/docs`

Ou a documentação ReDoc em: `http://localhost:8000/redoc`

## Endpoints Disponíveis

### 1. GET `/`
Informações gerais da API e lista de endpoints disponíveis.

**Resposta:**
```json
{
  "api": "SentimentalBanking",
  "version": "1.0.0",
  "description": "API para correlação funcional e priorização de backlog",
  "endpoints": {...}
}
```

### 2. GET `/health`
Verifica o status da API e arquivos necessários.

**Resposta:**
```json
{
  "status": "healthy",
  "timestamp": "2025-12-17T20:00:00",
  "files": {
    "sentiment_results": true,
    "functional_correlation": true,
    "ground_truth": true
  }
}
```

### 3. POST `/sentiment/analyze`
Analisa sentimentos de um lote de avaliações.

**Request Body:**
```json
{
  "reviews": [
    {
      "content": "O app está travando muito",
      "score": 1,
      "date": "2025-12-17",
      "version": "25.9.1.3",
      "app_name": "Santander"
    }
  ]
}
```

**Resposta:**
```json
{
  "total_reviews": 1,
  "results": [
    {
      "content": "O app está travando muito",
      "sentiment_label": "negative",
      "sentiment_score": 0.85,
      "score": 1
    }
  ]
}
```

### 4. GET `/sentiment/results`
Obtém resultados de análise de sentimentos já processados.

**Parâmetros de Query:**
- `format` (opcional): `json` ou `csv` (padrão: `json`)
- `app_name` (opcional): Filtrar por nome do app
- `sentiment` (opcional): Filtrar por sentimento (`positive`, `negative`, `neutral`)

**Exemplo:**
```
GET /sentiment/results?format=json&app_name=Santander&sentiment=negative
```

### 5. GET `/functional/results`
Obtém resultados de categorização funcional.

**Parâmetros de Query:**
- `format` (opcional): `json` ou `csv` (padrão: `json`)
- `app_name` (opcional): Filtrar por nome do app
- `category` (opcional): Filtrar por categoria funcional

**Exemplo:**
```
GET /functional/results?format=csv&category=PIX
```

### 6. GET `/backlog/prioritized`
Obtém backlog priorizado baseado em frequência, severidade e impacto.

**Parâmetros de Query:**
- `app_name` (opcional): Filtrar por nome do app
- `min_priority` (opcional): Prioridade mínima entre 0.0 e 1.0 (padrão: 0.0)
- `limit` (opcional): Limitar número de categorias retornadas

**Exemplo:**
```
GET /backlog/prioritized?app_name=Santander&min_priority=0.5&limit=10
```

**Resposta:**
```json
{
  "total_categories": 10,
  "total_reviews": 500,
  "filters": {
    "app_name": "Santander",
    "min_priority": 0.5
  },
  "backlog": [
    {
      "category": "PIX",
      "priority_score": 0.85,
      "priority_level": "CRITICA",
      "frequency": 120,
      "frequency_percentage": 24.0,
      "average_severity": 1.5,
      "recommendation": "Investigar logs de erro nas transações PIX..."
    }
  ]
}
```

### 7. GET `/metrics/validation`
Obtém métricas de validação do modelo comparando com ground truth.

**Resposta:**
```json
{
  "total_samples": 1000,
  "metrics": {
    "accuracy": 0.9617,
    "precision": 0.9817,
    "recall": 0.9617,
    "f1_score": 0.9692
  },
  "distribution": {
    "expected": {"positive": 500, "negative": 400, "neutral": 100},
    "predicted": {"positive": 510, "negative": 390, "neutral": 100}
  }
}
```

### 8. GET `/categories/list`
Lista todas as categorias funcionais disponíveis.

**Resposta:**
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

## Exemplos de Uso

### Exemplo 1: Analisar sentimentos de novas avaliações

```python
import requests

url = "http://localhost:8000/sentiment/analyze"
data = {
    "reviews": [
        {
            "content": "App muito lento, não consigo fazer PIX",
            "score": 1,
            "app_name": "Santander"
        }
    ]
}

response = requests.post(url, json=data)
print(response.json())
```

### Exemplo 2: Obter backlog priorizado

```python
import requests

url = "http://localhost:8000/backlog/prioritized"
params = {
    "app_name": "Santander",
    "min_priority": 0.5,
    "limit": 5
}

response = requests.get(url, params=params)
backlog = response.json()

for item in backlog["backlog"]:
    print(f"{item['category']}: {item['priority_level']} (Score: {item['priority_score']})")
```

### Exemplo 3: Obter resultados em CSV

```python
import requests

url = "http://localhost:8000/functional/results"
params = {"format": "csv", "category": "PIX"}

response = requests.get(url, params=params)
with open("pix_reviews.csv", "wb") as f:
    f.write(response.content)
```

## Integração com Ferramentas de Gestão

### Jira/Knooly

A API pode ser integrada com ferramentas de gestão de backlog usando webhooks ou scripts periódicos:

```python
import requests
import schedule
import time

def sync_backlog():
    response = requests.get("http://localhost:8000/backlog/prioritized")
    backlog = response.json()
    
    # Criar issues no Jira/Knooly baseado no backlog
    for item in backlog["backlog"]:
        if item["priority_level"] == "CRITICA":
            # Criar issue crítica
            pass

# Executar a cada hora
schedule.every().hour.do(sync_backlog)

while True:
    schedule.run_pending()
    time.sleep(60)
```

## Tratamento de Erros

A API retorna códigos HTTP apropriados:

- `200`: Sucesso
- `400`: Erro na requisição (parâmetros inválidos)
- `404`: Recurso não encontrado
- `500`: Erro interno do servidor

Exemplo de resposta de erro:

```json
{
  "detail": "Arquivo de resultados não encontrado"
}
```

## Limitações e Considerações

1. **Performance**: A análise de sentimentos pode ser lenta para grandes volumes (processa em batches)
2. **Dependências**: Requer arquivos CSV pré-processados para alguns endpoints
3. **Memória**: Carrega datasets completos em memória
4. **Concorrência**: Não otimizado para múltiplas requisições simultâneas de análise

## Próximos Passos

- [ ] Adicionar autenticação/autorização
- [ ] Implementar cache para resultados frequentes
- [ ] Adicionar suporte a processamento assíncrono
- [ ] Melhorar tratamento de erros
- [ ] Adicionar logging estruturado
- [ ] Implementar rate limiting

## Suporte

Para questões ou problemas, consulte a documentação do projeto ou abra uma issue no repositório.

