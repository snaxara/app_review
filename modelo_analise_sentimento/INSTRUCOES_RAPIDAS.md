# Instruções Rápidas - Modelo de Análise de Sentimento

## Instalação Rápida

1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

2. Configure a chave da OpenAI:
   - Copie o arquivo `.env.example` para `.env`
   - Edite o arquivo `.env` e adicione sua chave da OpenAI

## Execução

Execute os scripts na seguinte ordem:

### 1. Coletar Avaliações
```bash
python collect_reviews.py
```
**Saída:** `app_review_dataset.csv`

### 2. Analisar Polarização
```bash
python sentiment_analysis.py
```
**Entrada:** `app_review_dataset.csv`  
**Saída:** `sentiment_results.csv`

### 3. Categorizar Funcionalmente
```bash
python functional_correlation.py
```
**Entrada:** `sentiment_results.csv`  
**Saída:** `functional_correlation_results.csv`

## Modelos Utilizados

- **BERTweet:** Para análise de polarização (executa localmente)
- **GPT-4o:** Para categorização funcional (requer API OpenAI)

## Resultados

- **Análise de Polarização:** 96.17% de acurácia
- **Categorização Funcional:** 15 categorias funcionais

## Dúvidas?

Consulte o `README.md` para documentação completa ou o `RESUMO_EXECUTIVO.md` para visão geral executiva.
