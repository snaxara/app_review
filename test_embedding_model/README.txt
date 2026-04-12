TESTE: text-embedding-3-large + SVM Classifier
===============================================

Este é um teste separado do projeto principal para avaliar o desempenho
do modelo text-embedding-3-large da OpenAI usando embeddings + classificador SVM.

Como executar:
--------------
1. Certifique-se de ter a variável OPENAI_API_KEY configurada no ambiente
2. Execute: python test_embedding_model.py

O script irá:
- Carregar os dados de avaliações
- Carregar o ground truth (classificação manual)
- Gerar embeddings usando text-embedding-3-large
- Treinar um classificador SVM
- Calcular métricas de acurácia, precisão, recall, F1-Score e ROC AUC
- Salvar resultados em results_embedding_model.csv

Nota: Este teste não altera nenhum código do projeto principal.
