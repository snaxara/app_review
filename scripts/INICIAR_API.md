# Como Iniciar a API SentimentalBanking

## Passo 1: Verificar Dependências

Certifique-se de que todas as dependências estão instaladas:

```bash
pip install fastapi uvicorn pandas scikit-learn transformers
```

## Passo 2: Executar a API

No diretório raiz do projeto (`app_review`), execute:

```bash
python scripts/api_sentimental_banking.py
```

Ou usando uvicorn diretamente:

```bash
uvicorn scripts.api_sentimental_banking:app --reload --host 0.0.0.0 --port 8000
```

## Passo 3: Verificar se está funcionando

A API estará disponível em: `http://localhost:8000`

Teste o endpoint de health:
```bash
curl http://localhost:8000/health
```

Ou abra no navegador: http://localhost:8000/health

## Passo 4: Acessar Documentação Interativa

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## Passo 5: Testar Endpoints

Execute o script de teste:

```bash
python scripts/test_api.py
```

## Troubleshooting

### Erro: "Module not found"
Certifique-se de estar no diretório raiz do projeto, não dentro de `scripts/`.

### Erro: "File not found"
Certifique-se de que os arquivos CSV existem:
- `sentiment_results.csv` (raiz do projeto)
- `functional_correlation_results.csv` (raiz do projeto)
- `data/ground_truth_dataset.csv`

### Porta já em uso
Se a porta 8000 estiver ocupada, altere no código:
```python
uvicorn.run(app, host="0.0.0.0", port=8001)  # Use outra porta
```

## Próximos Passos

1. Teste os endpoints principais
2. Integre com suas ferramentas (Jira/Knooly)
3. Configure processamento periódico se necessário

