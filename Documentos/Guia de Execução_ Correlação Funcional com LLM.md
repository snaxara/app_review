# Guia de Execução: Correlação Funcional com LLM

## Objetivo

Este guia fornece instruções detalhadas para executar o script `functional_correlation.py` no seu computador Windows com a IDE Cursor.

---

## Pré-requisitos

Antes de iniciar, certifique-se de que você completou:

- ✅ **Passo 1-4 do guia anterior** (Python instalado, bibliotecas instaladas, sentiment_analysis.py executado)
- ✅ **Arquivo `sentiment_results.csv`** gerado e salvo em `C:\codigos\app_review`
- ✅ **Chave de API da OpenAI** configurada (veja instruções abaixo)

---

## Passo 1: Configurar a Chave de API da OpenAI

O script `functional_correlation.py` usa a API da OpenAI para categorizar as avaliações. Você precisa configurar sua chave de API.

### Opção A: Variável de Ambiente (Recomendado)

**No Windows:**

1. Pressione `Win + R`, digite `sysdm.cpl` e pressione Enter
2. Vá para a aba **"Avançado"**
3. Clique em **"Variáveis de Ambiente"**
4. Em **"Variáveis do usuário"**, clique em **"Novo"**
5. Configure:
   - **Nome da variável:** `OPENAI_API_KEY`
   - **Valor da variável:** Sua chave de API (ex: `sk-proj-...`)
6. Clique em **OK** e reinicie o terminal/IDE

**Verificar se funcionou:**
```bash
echo %OPENAI_API_KEY%
```

### Opção B: Arquivo .env (Alternativa)

1. Instale a biblioteca `python-dotenv`:
```bash
pip install python-dotenv
```

2. Crie um arquivo `.env` em `C:\codigos\app_review`:
```
OPENAI_API_KEY=sk-proj-sua-chave-aqui
```

3. Adicione no início do script `functional_correlation.py`:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Passo 2: Preparar os Arquivos

### 2.1 Verificar Estrutura de Diretórios

Certifique-se de que sua pasta está organizada assim:

```
C:\codigos\app_review\
├── app_review_ex.csv
├── sentiment_analysis.py
├── sentiment_results.csv          ← Gerado pelo script anterior
├── functional_correlation.py      ← Novo script
```

### 2.2 Copiar o Script Python

Salve o arquivo `functional_correlation.py` (fornecido anteriormente) em `C:\codigos\app_review\`.

### 2.3 Ajustar Configurações (Opcional)

Abra `functional_correlation.py` e ajuste as seguintes configurações conforme necessário:

```python
# Linha 15-16: Arquivos de entrada e saída
INPUT_CSV = 'sentiment_results.csv'  # Arquivo gerado pelo sentiment_analysis.py
OUTPUT_CSV = 'functional_correlation_results.csv'
BACKLOG_REPORT = 'backlog_priorizado.md'

# Linha 19: Modelo LLM
MODEL_NAME = 'gpt-4.1-mini'  # Opções: 'gpt-4.1-mini', 'gpt-4.1-nano', 'gemini-2.5-flash'

# Linha 22: Filtro de avaliações
PROCESS_ONLY_NEGATIVE = True  # True = apenas negativas, False = todas

# Linha 25: Limite de avaliações para teste
LIMIT_REVIEWS = 100  # Altere para None para processar todas (331 negativas)
```

**Recomendação para o primeiro teste:** Mantenha `LIMIT_REVIEWS = 100` para validar o funcionamento.

---

## Passo 3: Executar o Script

### 3.1 Abrir o Terminal na IDE Cursor

1. Abra a pasta `C:\codigos\app_review` na IDE Cursor
2. Abra o terminal integrado (`Terminal > New Terminal` ou `` Ctrl+` ``)

### 3.2 Navegar até o Diretório

```bash
cd C:\codigos\app_review
```

### 3.3 Executar o Script

```bash
python functional_correlation.py
```

### 3.4 Acompanhar a Execução

Você verá mensagens como:

```
============================================================
CORRELAÇÃO FUNCIONAL DE AVALIAÇÕES - TCC SIMONE ROSSETTI
============================================================

1️⃣ Carregando resultados de sentimentos...
✅ Carregado: 1000 avaliações do arquivo sentiment_results.csv

2️⃣ Filtrando avaliações...
📊 Filtradas 331 avaliações negativas
⚠️ Limitado a 100 avaliações para teste inicial

3️⃣ Categorizando com LLM...
============================================================
INICIANDO CORRELAÇÃO FUNCIONAL COM LLM
============================================================

📝 Processando 100 avaliações...
🤖 Modelo: gpt-4.1-mini
⏱️ Tempo estimado: ~200 segundos

   Processadas: 10/100 (10.0%)
   Processadas: 20/100 (20.0%)
   ...
   Processadas: 100/100 (100.0%)

✅ Processamento concluído!

4️⃣ Salvando resultados...
✅ Resultados salvos em: functional_correlation_results.csv

5️⃣ Gerando relatório de backlog...
✅ Relatório de backlog gerado: backlog_priorizado.md

============================================================
📊 ESTATÍSTICAS FINAIS
============================================================

Distribuição de Categorias:
   Performance: 28 (28.0%)
   Login/Autenticação: 15 (15.0%)
   PIX: 12 (12.0%)
   Interface/Usabilidade: 10 (10.0%)
   Pagamentos/Boletos: 8 (8.0%)
   Outros: 27 (27.0%)

============================================================
✅ PROCESSO CONCLUÍDO COM SUCESSO!
============================================================

📁 Arquivos gerados:
   • functional_correlation_results.csv
   • backlog_priorizado.md

💡 Próximo passo: Revise o relatório de backlog e valide as categorizações.
```

**⏱️ Tempo estimado:**
- **100 avaliações:** ~3-5 minutos
- **331 avaliações (todas negativas):** ~10-15 minutos

---

## Passo 4: Validar os Resultados

### 4.1 Arquivos Gerados

Após a execução bem-sucedida, você terá dois novos arquivos:

#### **1. `functional_correlation_results.csv`**

Contém todas as avaliações processadas com uma nova coluna: `functional_category`

**Colunas principais:**
- `reviewId`: ID único da avaliação
- `content`: Texto da avaliação
- `score`: Nota original (1-5 estrelas)
- `sentiment_label`: Sentimento (negative/positive/neutral)
- `sentiment_score`: Confiança do modelo de sentimentos
- **`functional_category`**: Categoria funcional atribuída pelo LLM ✨

**Exemplo:**
```csv
reviewId,content,score,sentiment_label,sentiment_score,functional_category
abc123,"O app trava toda hora",1,negative,0.85,Performance
def456,"Não consigo fazer PIX",2,negative,0.78,PIX
```

#### **2. `backlog_priorizado.md`**

Relatório em Markdown com:
- **Resumo Executivo:** Total de avaliações analisadas
- **Distribuição de Categorias:** Tabela com frequência e prioridade
- **Detalhamento por Categoria:** Top 5 categorias com:
  - Métricas (frequência, severidade, score de prioridade)
  - Amostras de avaliações
  - Ações recomendadas

**Visualize no Cursor:** O Cursor renderiza automaticamente arquivos `.md` com formatação.

---

## Passo 5: Análise e Validação Manual

### 5.1 Validar Categorizações

Abra o arquivo `functional_correlation_results.csv` e valide manualmente uma amostra de 20-30 avaliações.

**Perguntas para validação:**
1. A categoria atribuída faz sentido para o texto da avaliação?
2. Há avaliações categorizadas como "Outros" que deveriam ter uma categoria específica?
3. Há inconsistências nas categorizações de textos similares?

### 5.2 Calcular Métricas de Qualidade

**Crie um script simples para calcular a taxa de acerto:**

```python
import pandas as pd

df = pd.read_csv('functional_correlation_results.csv')

# Validação manual: marque as categorizações corretas
# Exemplo: adicione uma coluna 'validacao_manual' com 'correto' ou 'incorreto'

# Calcular acurácia
correct = df[df['validacao_manual'] == 'correto'].shape[0]
total = df.shape[0]
accuracy = (correct / total) * 100

print(f"Acurácia: {accuracy:.2f}%")
```

---

## Passo 6: Processar o Dataset Completo

Após validar os resultados com 100 avaliações, processe todas as 331 avaliações negativas.

### 6.1 Ajustar Configuração

No arquivo `functional_correlation.py`, altere a linha 25:

```python
LIMIT_REVIEWS = None  # Processar todas as avaliações negativas
```

### 6.2 Executar Novamente

```bash
python functional_correlation.py
```

**⏱️ Tempo estimado:** ~10-15 minutos

---

## Solução de Problemas Comuns

### ❌ Erro: "No module named 'openai'"

**Solução:** Instale a biblioteca OpenAI:
```bash
pip install openai
```

### ❌ Erro: "AuthenticationError: Invalid API key"

**Solução:** Verifique se a chave de API está configurada corretamente:
```bash
echo %OPENAI_API_KEY%
```

Se não aparecer nada, revise o **Passo 1** deste guia.

### ❌ Erro: "FileNotFoundError: sentiment_results.csv"

**Solução:** Certifique-se de que você executou o `sentiment_analysis.py` primeiro e que o arquivo `sentiment_results.csv` está no mesmo diretório.

### ❌ Erro: "RateLimitError: You exceeded your current quota"

**Solução:** Você atingiu o limite de uso da API OpenAI. Opções:
1. Aguarde alguns minutos (limite de requisições por minuto)
2. Verifique seu saldo de créditos na OpenAI
3. Use um modelo mais barato: `MODEL_NAME = 'gpt-4.1-nano'`

### ❌ Processo muito lento

**Solução:** Ajuste o `time.sleep()` na linha 189:
```python
time.sleep(0.2)  # Reduzir de 0.5 para 0.2 segundos
```

**Atenção:** Reduzir muito pode causar erros de rate limiting.

---

## Próximos Passos

Após executar com sucesso a correlação funcional:

1. ✅ **Revisar o relatório de backlog** (`backlog_priorizado.md`)
2. ✅ **Validar manualmente** uma amostra de categorizações
3. ✅ **Documentar os resultados** no TCC (seção de Resultados)
4. ✅ **Preparar visualizações** (gráficos de distribuição de categorias)
5. ✅ **Implementar melhorias** sugeridas no documento de Best Practices

---

## Estimativa de Custos

**Para 331 avaliações negativas:**

| Modelo | Custo Estimado | Tempo Estimado |
|:-------|:---------------|:---------------|
| `gpt-4.1-mini` | $0.15 - $0.20 USD | ~10-15 minutos |
| `gpt-4.1-nano` | $0.05 - $0.08 USD | ~10-15 minutos |
| `gemini-2.5-flash` | Gratuito (com limites) | ~10-15 minutos |

**Recomendação:** Use `gpt-4.1-mini` para melhor qualidade. O custo é mínimo para um TCC.

---

## Checklist de Validação

Antes de prosseguir, confirme:

- [ ] Chave de API da OpenAI configurada
- [ ] Arquivo `sentiment_results.csv` presente no diretório
- [ ] Script `functional_correlation.py` salvo e ajustado
- [ ] Script executado sem erros
- [ ] Arquivo `functional_correlation_results.csv` gerado
- [ ] Arquivo `backlog_priorizado.md` gerado
- [ ] Validação manual de 20-30 categorizações realizada
- [ ] Resultados documentados

---

**Preparado por:** Manus AI  
**Data:** 01 de Dezembro de 2025  
**Projeto:** TCC - Correlação Funcional de Sentimentos em Apps Bancários
