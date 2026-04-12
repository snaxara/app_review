# Estrutura do Projeto - App Review Analysis

## 📁 Organização de Pastas

### `scripts/` - Scripts Principais
Scripts principais de processamento do pipeline:

- **`sentiment_analysis.py`** - Análise de sentimentos usando modelo BERTweet (cardiffnlp/twitter-xlm-roberta-base-sentiment)
- **`functional_correlation.py`** - Categorização funcional usando LLM (GPT-4o)
- **`validate_model.py`** - Validação do modelo contra ground truth humano
- **`generate_backlog_report.py`** - Geração de relatório de backlog priorizado

### `scripts/analysis/` - Análise e Comparação
Scripts para análise de dados e comparação de modelos:

- **`analyze_human_classification.py`** - Análise de classificações humanas (Carol/Samuel)
- **`compare_human_vs_llm.py`** - Comparação entre classificações humanas e LLM
- **`calculate_inter_annotator_agreement.py`** - Cálculo de acordo inter-anotadores (Cohen's Kappa)
- **`analyze_other_categories.py`** - Análise de outras categorias
- **`compare_models.py`** - Comparação entre modelos

### `scripts/utils/` - Utilitários
Scripts utilitários auxiliares:

- **`read_pptx.py`** - Leitura e extração de conteúdo de apresentações PowerPoint
- **`get_real_stats.py`** - Extração de estatísticas reais dos datasets
- **`show_negative_without_category.py`** - Identifica avaliações negativas sem categoria
- **`generate_training_dataset.py`** - Geração de datasets para treino/teste

### `scripts/mixed/` - Sentimento Misto
Scripts relacionados a detecção de sentimento misto (mixed):

- **`adicionar_sentimento_mixed.py`** - Adiciona coluna `mixed` aos datasets
- **`identificar_mixed_exemplo.py`** - Identifica exemplos de mixed usando LLM
- **`atualizar_guia_mixed.py`** - Atualiza guia de anotação com exemplos mixed

### `scripts/guia/` - Guias de Anotação
Scripts para criação de guias de anotação:

- **`criar_guia_anotacao_completo_excel.py`** - Cria guia completo em Excel (17 categorias, todas polaridades)
- **`criar_guia_anotacao_excel.py`** - Versão simplificada do guia

### `scripts/presentation/` - Apresentações
Scripts para atualização de apresentações PowerPoint:

- **`update_presentation_v2.py`** - Atualiza apresentação principal (v2)
- **`update_presentation.py`** - Versão anterior
- **`add_validation_section.py`** - Adiciona seção de validação à apresentação

### `data/` - Datasets e Dados
Todos os arquivos CSV com dados:

**Datasets de Classificação Humana:**
- `app_review_dataset_carol.csv` - Classificações da Carol (1000 avaliações)
- `app_review_dataset_samuel.csv` - Classificações do Samuel (1000 avaliações)
- `ground_truth_dataset.csv` - Ground truth consolidado (maioria entre Carol e Samuel)

**Resultados de Processamento:**
- `sentiment_results.csv` - Resultados da análise de sentimentos
- `functional_correlation_results.csv` - Resultados da categorização funcional (LLM)

**Outros:**
- `training_dataset.csv` - Dataset para treino/teste
- `app_review_dataset_ex.csv` - Dataset exemplo
- `app_review_dataset.csv` - Dataset original
- `app_review_apple_2025.csv` - Dataset Apple 2025
- `sentiment_comparison_final.csv` - Comparação final de sentimentos
- `avaliacoes_negativas_sem_categoria.csv` - Avaliações negativas sem categoria

### `docs/` - Documentação
Documentação do projeto:

- **`guia_anotacao_classificacao.md`** - Guia completo de anotação em Markdown
- **`guia_anotacao_completo.xlsx`** - Guia completo de anotação em Excel (3 abas: Taxonomia, Exemplos, Casos Complexos)
- **`guia_anotacao_exemplos.xlsx`** - Versão simplificada do guia
- **`metodologia_validacao_modelo.md`** - Metodologia de validação
- **`resumo_validacao_completa.md`** - Resumo completo da validação

### `reports/` - Relatórios Gerados
Relatórios e análises gerados:

- **`sentiment_report.md`** - Relatório de análise de sentimentos
- **`backlog_priorizado.md`** - Backlog priorizado
- **`Backlog Priorizado - Aplicativo Bancário.md`** - Versão formatada do backlog
- **`analise_classificacao_carol.md`** - Análise das classificações da Carol
- **`avaliacoes_negativas_sem_categoria.md`** - Análise de avaliações negativas sem categoria
- **`comparacao_antes_depois.md`** - Comparação antes/depois
- **`report_daily_hoje.md`** - Relatório diário (hoje)
- **`report_daily_amanha.md`** - Relatório diário (amanhã)
- **`inter_annotator_final.txt`** - Resultados finais de acordo inter-anotadores
- **`inter_annotator_results.txt`** - Resultados de acordo inter-anotadores

## 🔄 Fluxo de Trabalho Principal

### 1. Análise de Sentimentos
```bash
python scripts/sentiment_analysis.py
```
- **Entrada**: `data/app_review_dataset_ex.csv` (ou outro dataset)
- **Saída**: `data/sentiment_results.csv`
- **Modelo**: cardiffnlp/twitter-xlm-roberta-base-sentiment
- **Detecção Mixed**: Opcional (usa GPT-4o para identificar avaliações mistas)

### 2. Categorização Funcional
```bash
python scripts/functional_correlation.py
```
- **Entrada**: `data/sentiment_results.csv`
- **Saída**: `data/functional_correlation_results.csv`
- **Modelo**: GPT-4o
- **Processa**: Apenas avaliações negativas (ou mixed, se configurado)

### 3. Validação do Modelo
```bash
python scripts/validate_model.py --human data/ground_truth_dataset.csv --llm data/functional_correlation_results.csv
```
- **Compara**: Resultados do LLM vs. Ground Truth humano
- **Métricas**: Precision, Recall, F1-Score (por categoria e macro)
- **Priorização**: Spearman's Rank Correlation, Top-K Accuracy, MAP@K

### 4. Geração de Backlog
```bash
python scripts/generate_backlog_report.py
```
- **Entrada**: `data/functional_correlation_results.csv`
- **Saída**: `reports/backlog_priorizado.md`
- **Priorização**: Baseada em frequência e severidade

## 📊 Categorias Funcionais (17)

1. PIX
2. Login/Autenticação
3. Performance
4. Interface/Usabilidade
5. Empréstimos/Crédito
6. Pagamentos/Boletos
7. Saldo/Extrato
8. Atendimento
9. Cadastro/Conta
10. Investimentos
11. Segurança
12. Notificações
13. Questões geográficas
14. Placas/Veículos
15. Tarifas/Cobranças
16. Outros
17. Não Identificado

## 🎯 Sentimentos

- **Positive** - Elogios, satisfação
- **Negative** - Reclamações, problemas
- **Neutral** - Informativo, sem polaridade clara
- **Mixed** - Aspectos positivos E negativos simultaneamente (apenas em avaliações negativas)

## 📝 Notas

- **Backup/**: Contém versões antigas de scripts (pode ser removido se não necessário)
- **Documentos/**: Contém apresentações PowerPoint e documentação adicional
- **modelo_student/**: Contém código de modelo estudante (pode ser mantido ou removido conforme necessário)

## 🔧 Configuração

Certifique-se de ter um arquivo `.env` na raiz do projeto com:
```
OPENAI_API_KEY=sua_chave_aqui
```

## 📚 Referências

- Guia de Anotação: `docs/guia_anotacao_completo.xlsx`
- Ground Truth: `data/ground_truth_dataset.csv`
- Validação: `scripts/validate_model.py`

