"""
Script de comparação entre modelos de análise de sentimentos.

Este script compara dois modelos pré-treinados:
- DistilBERT Multilíngue: modelo mais leve e rápido
- BERTweet: modelo treinado especificamente em dados de redes sociais

O objetivo é avaliar qual modelo tem melhor desempenho na análise de sentimentos
de avaliações de aplicativos bancários, usando o ground truth criado pela
classificação manual da Carol e Samuel.
"""

import pandas as pd
import csv
from transformers import pipeline, XLMRobertaTokenizer, XLMRobertaForSequenceClassification
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, roc_curve, roc_auc_score
from sklearn.preprocessing import label_binarize
import matplotlib.pyplot as plt
import numpy as np
import os




# --- Configurações ---
CSV_PATH = 'data/app_review_dataset_ex.csv'
GROUND_TRUTH_PATH = 'data/ground_truth_dataset.csv'  # Base da Carol e Samuel
OUTPUT_CSV_PATH = 'data/sentiment_comparison_final.csv'

TEXT_COLUMN = 'content'
LIMIT_REVIEWS = 1000  # Amostra para comparação

# Modelos para comparar
MODELS = [
    {
        'name': 'DistilBERT Multilíngue',
        'id': 'lxyuan/distilbert-base-multilingual-cased-sentiments-student',
        'type': 'standard'
    },
    {
        'name': 'BERTweet (Twitter XLM-RoBERTa)',
        'id': 'cardiffnlp/twitter-xlm-roberta-base-sentiment',
        'type': 'xlm_roberta'
    }
]

# --- Funções ---

def load_data(path, limit=None):
    """
    Carrega o dataset de avaliações do arquivo CSV.
    
    Pega as últimas N avaliações (se limit for especificado) para garantir
    que estamos testando com dados mais recentes.
    """
    try:
        # O CSV usa ponto e vírgula como separador
        df = pd.read_csv(path, sep=';', quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
        df.columns = [col.strip() for col in df.columns]
        
        # Verifica se a coluna de texto existe
        if TEXT_COLUMN not in df.columns:
            print(f"Aviso: Coluna '{TEXT_COLUMN}' não encontrada.")
            return None
        
        # Remove avaliações sem texto (não dá pra analisar sentimento sem texto)
        df.dropna(subset=[TEXT_COLUMN], inplace=True)
        
        # Se especificou um limite, pega as últimas avaliações
        if limit and len(df) > limit:
            df = df.tail(limit)
            
        print(f"Dataset carregado: {len(df)} avaliações.")
        return df
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        return None

def analyze_with_model(df, model_config):
    """
    Executa a análise de sentimentos usando um modelo específico.
    
    Esta função carrega o modelo, processa todos os textos do dataset e retorna
    as predições de sentimento junto com as probabilidades de cada classe.
    Isso é necessário para calcular métricas como ROC AUC depois.
    """
    model_name = model_config['name']
    model_id = model_config['id']
    model_type = model_config['type']
    
    print(f"\n{'='*60}")
    print(f"Testando: {model_name}")
    print(f"Modelo: {model_id}")
    print(f"{'='*60}")
    
    try:
        # BERTweet precisa de um tokenizer especial (SentencePiece)
        # DistilBERT usa o tokenizer padrão do HuggingFace
        if model_type == 'xlm_roberta':
            print("Carregando tokenizer SentencePiece...")
            tokenizer = XLMRobertaTokenizer.from_pretrained(model_id)
            print("Carregando modelo...")
            model = XLMRobertaForSequenceClassification.from_pretrained(model_id)
            print("Criando pipeline...")
            pipeline_obj = pipeline(
                "sentiment-analysis",
                model=model,
                tokenizer=tokenizer,
                return_all_scores=True,  # Precisamos de todas as probabilidades para ROC
                device=-1  # Usa CPU
            )
        else:
            # DistilBERT é mais simples, só precisa passar o ID do modelo
            print("Carregando modelo...")
            pipeline_obj = pipeline(
                "sentiment-analysis",
                model=model_id,
                tokenizer=model_id,
                return_all_scores=True  # Precisamos de todas as probabilidades para ROC
            )
        
        print("Pipeline criado!")
        
        # Converte a coluna de texto para uma lista
        texts = df[TEXT_COLUMN].tolist()
        print(f"Processando {len(texts)} textos...")
        
        # Processa em lotes (batches) para não sobrecarregar a memória
        # e para ter uma barra de progresso mais útil
        results = []
        batch_size = 16  # Processa 16 textos por vez
        
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            batch_results = pipeline_obj(batch)
            results.extend(batch_results)
            
            # Mostra progresso a cada 50 textos processados
            if (i + batch_size) % 50 == 0:
                print(f"   Processadas: {min(i + batch_size, len(texts))}/{len(texts)}")
        
        # Extrair e normalizar labels, scores e probabilidades
        labels = []
        scores = []
        all_probs = []  # Probabilidades de todas as classes
        
        # Os modelos retornam apenas 3 classes: positive, negative, neutral
        
        for res in results:
            if isinstance(res, list):
                # return_all_scores=True retorna lista de dicts
                best_item = max(res, key=lambda x: x.get('score', 0))
                label = best_item.get('label', 'unknown')
                score = best_item.get('score', 0.0)
                
                # Criar dicionário de probabilidades por classe normalizada
                prob_dict = {}
                for item in res:
                    item_label = item.get('label', '').lower()
                    item_score = item.get('score', 0.0)
                    
                    # Normalizar o label retornado pelo modelo para nosso padrão
                    # Os modelos podem retornar labels em diferentes formatos (POSITIVE, positive, etc)
                    if 'pos' in item_label or 'posit' in item_label:
                        norm_label = 'positive'
                    elif 'neg' in item_label:
                        norm_label = 'negative'
                    elif 'neu' in item_label:
                        norm_label = 'neutral'
                    else:
                        # Se não reconhecer, mantém o label original
                        norm_label = item_label
                    
                    prob_dict[norm_label] = item_score
                
                all_probs.append(prob_dict)
            elif isinstance(res, dict):
                label = res.get('label', 'unknown')
                score = res.get('score', 0.0)
                prob_dict = {label.lower(): score}
                all_probs.append(prob_dict)
            else:
                label = 'unknown'
                score = 0.0
                all_probs.append({})
            
            # Normalizar o label escolhido (o de maior confiança) para nosso padrão
            label_lower = label.lower()
            if 'pos' in label_lower or 'posit' in label_lower:
                normalized_label = 'positive'
            elif 'neg' in label_lower:
                normalized_label = 'negative'
            elif 'neu' in label_lower:
                normalized_label = 'neutral'
            else:
                # Se não reconhecer, mantém o label original
                normalized_label = label
            
            labels.append(normalized_label)
            scores.append(score)
        
        print(f"Análise concluída!")
        print(f"  Distribuição: {pd.Series(labels).value_counts().to_dict()}")
        print(f"  Score médio: {sum(scores)/len(scores):.4f}")
        
        return {
            'labels': labels,
            'scores': scores,
            'all_probs': all_probs,  # Probabilidades de todas as classes
            'model_name': model_name,
            'model_id': model_id
        }
        
    except Exception as e:
        print(f"Erro: {e}")
        import traceback
        traceback.print_exc()
        return None

def load_ground_truth(gt_path):
    """
    Carrega o ground truth criado pela classificação manual da Carol e Samuel.
    
    O ground truth tem as avaliações classificadas manualmente, então sabemos
    qual é a resposta "correta" para cada avaliação. Isso permite comparar
    as predições do modelo com o que realmente deveria ser classificado.
    """
    try:
        df_gt = pd.read_csv(gt_path, sep=';', encoding='utf-8')
        df_gt.columns = [col.strip() for col in df_gt.columns]
        
        # O ground truth usa formato one-hot (colunas separadas: negative, positive, neutral)
        # Precisamos converter isso para um único label
        def get_sentiment_from_onehot(row):
            if row.get('negative', 0) == 1:
                return 'negative'
            elif row.get('positive', 0) == 1:
                return 'positive'
            elif row.get('neutral', 0) == 1:
                return 'neutral'
            else:
                return None
        
        df_gt['expected_sentiment'] = df_gt.apply(get_sentiment_from_onehot, axis=1)
        return df_gt
    except Exception as e:
        print(f"Erro ao carregar ground truth: {e}")
        return None

def calculate_metrics(df, predictions, all_probs, model_name, use_ground_truth=True):
    """
    Calcula as métricas de desempenho do modelo.
    
    Compara as predições do modelo com o ground truth (classificação manual da Carol e Samuel)
    ou com os scores originais das avaliações (fallback).
    
    Métricas calculadas:
    - Accuracy: porcentagem de predições corretas
    - Precision: das predições positivas, quantas eram realmente positivas
    - Recall: das avaliações realmente positivas, quantas foram identificadas
    - F1-Score: média harmônica entre precision e recall (balanceia os dois)
    - ROC AUC: área sob a curva ROC (quanto maior, melhor o modelo distingue as classes)
    
    Essas métricas nos dizem se o modelo "aprendeu" bem a tarefa de classificação.
    """
    
    if use_ground_truth:
        print(f"  [{model_name}] Usando ground truth da Carol e Samuel para validação...")
        # Tenta carregar o ground truth primeiro
        df_gt = load_ground_truth(GROUND_TRUTH_PATH)
        if df_gt is not None:
            # Faz o merge dos dados com o ground truth usando reviewId ou content
            # Isso permite comparar predição vs. classificação manual
            if 'reviewId' in df.columns and 'reviewId' in df_gt.columns:
                df_temp = df.merge(df_gt[['reviewId', 'expected_sentiment']], on='reviewId', how='inner')
            elif 'content' in df.columns and 'content' in df_gt.columns:
                df_temp = df.merge(df_gt[['content', 'expected_sentiment']], on='content', how='inner')
            else:
                # Se não conseguir fazer merge, usa fallback
                use_ground_truth = False
        else:
            use_ground_truth = False
    
    if not use_ground_truth:
        # Fallback: converte os scores originais (1-5) em sentimentos
        # Score 1-2 = negativo, 3 = neutro, 4-5 = positivo
        def score_to_sentiment(score):
            if pd.isna(score):
                return None
            score = float(score)
            if score <= 2:
                return 'negative'
            elif score == 3:
                return 'neutral'
            else:  # 4 ou 5
                return 'positive'
        
        df_temp = df.copy()
        df_temp['expected_sentiment'] = df_temp['score'].apply(score_to_sentiment)
    
    # Garantir que predictions tem o mesmo tamanho de df_temp
    if len(predictions) != len(df_temp):
        # Se fez merge, precisa ajustar predictions
        if use_ground_truth and df_gt is not None:
            # Criar dicionário de predictions por reviewId ou content
            if 'reviewId' in df.columns:
                pred_dict = dict(zip(df['reviewId'], predictions))
                df_temp['predicted_sentiment'] = df_temp['reviewId'].map(pred_dict)
            elif 'content' in df.columns:
                pred_dict = dict(zip(df['content'], predictions))
                df_temp['predicted_sentiment'] = df_temp['content'].map(pred_dict)
            else:
                df_temp['predicted_sentiment'] = predictions[:len(df_temp)]
        else:
            df_temp['predicted_sentiment'] = predictions[:len(df_temp)]
    else:
        df_temp['predicted_sentiment'] = predictions
    
    # Remove avaliações onde não temos ground truth ou predição válida
    # Só podemos calcular métricas onde temos ambos (esperado e predito)
    valid_mask = df_temp['expected_sentiment'].notna() & df_temp['predicted_sentiment'].notna()
    valid_df = df_temp[valid_mask].reset_index(drop=True)
    
    if len(valid_df) == 0:
        return None
    
    # Mapeia as probabilidades para as avaliações válidas
    # Isso é necessário porque após o merge pode ter menos linhas
    if use_ground_truth and df_gt is not None and len(all_probs) == len(df):
        # Se fez merge, precisa mapear probabilidades pelo reviewId ou content
        if 'reviewId' in df.columns:
            prob_dict = dict(zip(df['reviewId'], all_probs))
            valid_probs = [prob_dict.get(rid, {}) for rid in valid_df['reviewId']]
        elif 'content' in df.columns:
            prob_dict = dict(zip(df['content'], all_probs))
            valid_probs = [prob_dict.get(cont, {}) for cont in valid_df['content']]
        else:
            valid_probs = [all_probs[i] for i in range(len(all_probs)) if valid_mask.iloc[i]]
    else:
        valid_probs = [all_probs[i] for i in range(len(all_probs)) if valid_mask.iloc[i]]
    
    # Separa as listas de esperado (ground truth) e predito (modelo)
    expected = valid_df['expected_sentiment'].tolist()
    predicted = valid_df['predicted_sentiment'].tolist()
    
    # Calcula as métricas básicas de classificação
    # Accuracy: quantas predições estão corretas (mais simples de entender)
    accuracy = accuracy_score(expected, predicted)
    
    # Precision, Recall e F1: métricas mais detalhadas que consideram cada classe
    # average='weighted' significa que calcula para cada classe e faz média ponderada
    # Isso é importante porque pode ter classes desbalanceadas (mais positivos que negativos, etc)
    precision, recall, f1, _ = precision_recall_fscore_support(
        expected, predicted, average='weighted', zero_division=0
    )
    
    # Matriz de confusão: mostra quantas vezes cada classe foi classificada corretamente ou incorretamente
    # Útil para entender onde o modelo está errando mais
    cm = confusion_matrix(expected, predicted, labels=['positive', 'negative', 'neutral'])
    
    # Calcula ROC AUC - métrica importante que mostra quão bem o modelo distingue as classes
    # ROC AUC usa as probabilidades (não só o label escolhido), então é mais informativo
    # Valores próximos de 1.0 = modelo muito bom, 0.5 = aleatório, < 0.5 = pior que aleatório
    roc_auc = None
    roc_data = None
    try:
        # Identifica quais classes realmente aparecem nos dados
        all_classes = ['positive', 'negative', 'neutral']
        classes_present = sorted(set(expected) & set(all_classes))
        
        # Precisa de pelo menos 2 classes e probabilidades válidas para calcular ROC
        if len(classes_present) >= 2 and len(valid_probs) > 0:
            # Converte labels para formato binário (one-hot encoding)
            # Exemplo: se temos 3 classes, cada avaliação vira [0, 1, 0] se for classe 2
            y_true_binary = label_binarize(expected, classes=classes_present)
            
            # Cria matriz de probabilidades: uma linha por avaliação, uma coluna por classe
            # Cada célula tem a probabilidade que o modelo deu para aquela classe
            y_prob = np.zeros((len(valid_probs), len(classes_present)))
            for i, prob_dict in enumerate(valid_probs):
                for j, cls in enumerate(classes_present):
                    y_prob[i, j] = prob_dict.get(cls, 0.0)
            
            # Calcula ROC AUC de duas formas dependendo do número de classes
            if y_true_binary.shape[1] == 2:
                # Caso binário (só 2 classes): cálculo direto
                roc_auc = roc_auc_score(y_true_binary[:, 1], y_prob[:, 1])
                fpr, tpr, _ = roc_curve(y_true_binary[:, 1], y_prob[:, 1])
                roc_data = {'fpr': fpr, 'tpr': tpr}
            else:
                # Caso multiclasse (3 classes): calcula ROC para cada classe separadamente
                # usando estratégia "one-vs-rest" (uma classe vs todas as outras)
                # Depois faz a média das AUCs de cada classe
                roc_aucs = []
                roc_curves = {}
                for idx, cls in enumerate(classes_present):
                    # Só calcula se a classe aparece pelo menos uma vez
                    if np.sum(y_true_binary[:, idx]) > 0:
                        auc = roc_auc_score(y_true_binary[:, idx], y_prob[:, idx])
                        roc_aucs.append(auc)
                        # Guarda a curva ROC também para plotar depois
                        fpr, tpr, _ = roc_curve(y_true_binary[:, idx], y_prob[:, idx])
                        roc_curves[cls] = {'fpr': fpr, 'tpr': tpr}
                
                # Média macro das AUCs (trata todas as classes igualmente)
                if roc_aucs:
                    roc_auc = np.mean(roc_aucs)
                    roc_data = roc_curves
    except Exception as e:
        print(f"Erro ao calcular ROC AUC: {e}")
        roc_auc = None
        roc_data = None
    
    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'roc_data': roc_data,
        'confusion_matrix': cm,
        'n_samples': len(valid_df)
    }

def generate_plots(metrics_dict, output_dir='data'):
    """
    Gera os gráficos comparativos entre os modelos.
    
    Cria 3 gráficos lado a lado:
    1. Curva ROC: mostra quão bem cada modelo distingue as classes
    2. Comparação de métricas: barras comparando ROC AUC, Precision, Recall e F1
    3. Comparação de acurácia: barras simples mostrando qual modelo acerta mais
    """
    if len(metrics_dict) < 2:
        print("Erro: É necessário pelo menos 2 modelos para gerar gráficos comparativos.")
        return
    
    model_names = list(metrics_dict.keys())
    if len(model_names) != 2:
        print("Atenção: Função otimizada para 2 modelos. Usando os 2 primeiros.")
        model_names = model_names[:2]
    
    model1_name = model_names[0]
    model2_name = model_names[1]
    model1_metrics = metrics_dict[model1_name]
    model2_metrics = metrics_dict[model2_name]
    
    # Criar figura com subplots
    fig = plt.figure(figsize=(15, 5))
    
    # 1. ROC Curve Comparison
    ax1 = plt.subplot(1, 3, 1)
    
    # Modelo 1
    if model1_metrics.get('roc_data') is not None:
        roc_data1 = model1_metrics['roc_data']
        auc1 = model1_metrics.get('roc_auc', 0)
        
        if isinstance(roc_data1, dict):
            # Multiclasse - plotar todas as classes com transparência e média
            all_fpr = []
            all_tpr = []
            for cls, curve in roc_data1.items():
                ax1.plot(curve['fpr'], curve['tpr'], alpha=0.2, linewidth=1, color='blue')
                all_fpr.append(curve['fpr'])
                all_tpr.append(curve['tpr'])
            # Plotar primeira classe como representativa
            if roc_data1:
                first_key = list(roc_data1.keys())[0]
                ax1.plot(roc_data1[first_key]['fpr'], roc_data1[first_key]['tpr'], 
                        label=f'{model1_name} (AUC = {auc1:.3f})', linewidth=2, color='blue')
        else:
            ax1.plot(roc_data1['fpr'], roc_data1['tpr'], 
                    label=f'{model1_name} (AUC = {auc1:.3f})', linewidth=2, color='blue')
    
    # Modelo 2
    if model2_metrics.get('roc_data') is not None:
        roc_data2 = model2_metrics['roc_data']
        auc2 = model2_metrics.get('roc_auc', 0)
        
        if isinstance(roc_data2, dict):
            # Multiclasse - plotar todas as classes com transparência
            for cls, curve in roc_data2.items():
                ax1.plot(curve['fpr'], curve['tpr'], alpha=0.2, linewidth=1, color='green')
            if roc_data2:
                first_key = list(roc_data2.keys())[0]
                ax1.plot(roc_data2[first_key]['fpr'], roc_data2[first_key]['tpr'], 
                        label=f'{model2_name} (AUC = {auc2:.3f})', linewidth=2, color='green')
        else:
            ax1.plot(roc_data2['fpr'], roc_data2['tpr'], 
                    label=f'{model2_name} (AUC = {auc2:.3f})', linewidth=2, color='green')
    
    # Linha de referência (random classifier)
    ax1.plot([0, 1], [0, 1], 'k--', label='Random Classifier', linewidth=1)
    
    ax1.set_xlabel('False Positive Rate')
    ax1.set_ylabel('True Positive Rate')
    ax1.set_title('ROC Curve Comparison')
    ax1.legend(loc='lower right')
    ax1.grid(True, alpha=0.3)
    
    # 2. Metrics Comparison (bar chart)
    ax2 = plt.subplot(1, 3, 2)
    
    metrics_to_plot = ['roc_auc', 'precision', 'recall', 'f1_score']
    metric_labels = ['ROC AUC', 'Precision', 'Recall', 'F1-Score']
    
    # Filtrar métricas disponíveis
    available_metrics = []
    available_labels = []
    model1_values = []
    model2_values = []
    
    for metric, label in zip(metrics_to_plot, metric_labels):
        val1 = model1_metrics.get(metric)
        val2 = model2_metrics.get(metric)
        if val1 is not None and val2 is not None:
            available_metrics.append(metric)
            available_labels.append(label)
            model1_values.append(val1)
            model2_values.append(val2)
    
    if available_metrics:
        x = np.arange(len(available_labels))
        width = 0.35
        
        bars1 = ax2.bar(x - width/2, model1_values, width, label=model1_name)
        bars2 = ax2.bar(x + width/2, model2_values, width, label=model2_name)
        
        ax2.set_ylabel('Score')
        ax2.set_title('Metrics Comparison')
        ax2.set_xticks(x)
        ax2.set_xticklabels(available_labels)
        ax2.legend()
        ax2.set_ylim(0, 1.1)
        ax2.grid(True, alpha=0.3, axis='y')
    
    # 3. Accuracy Comparison (adicional)
    ax3 = plt.subplot(1, 3, 3)
    
    acc1 = model1_metrics.get('accuracy', 0)
    acc2 = model2_metrics.get('accuracy', 0)
    
    bars = ax3.bar([model1_name, model2_name], [acc1, acc2], 
                   color=['#1f77b4', '#2ca02c'], alpha=0.7)
    ax3.set_ylabel('Accuracy')
    ax3.set_title('Accuracy Comparison')
    ax3.set_ylim(0, 1.1)
    ax3.grid(True, alpha=0.3, axis='y')
    
    # Adicionar valores nas barras
    for bar in bars:
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.2%}', ha='center', va='bottom')
    
    plt.tight_layout()
    plot_path = f'{output_dir}/model_comparison_plots.png'
    plt.savefig(plot_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Gráficos salvos em: {plot_path}")
    return plot_path

def generate_confusion_matrices(metrics_dict, output_dir='data'):
    """
    Gera e salva as matrizes de confusão de ambos os modelos.
    
    A matriz de confusão mostra visualmente onde o modelo está acertando e errando.
    Cada célula mostra quantas avaliações de uma classe foram classificadas como outra classe.
    """
    if len(metrics_dict) < 1:
        print("Erro: É necessário pelo menos 1 modelo para gerar matriz de confusão.")
        return
    
    # Cria uma figura com subplots lado a lado
    fig, axes = plt.subplots(1, len(metrics_dict), figsize=(6 * len(metrics_dict), 5))
    
    # Se só tem um modelo, axes não é uma lista
    if len(metrics_dict) == 1:
        axes = [axes]
    
    classes = ['positive', 'negative', 'neutral']
    
    for idx, (model_name, metrics) in enumerate(metrics_dict.items()):
        cm = metrics.get('confusion_matrix')
        
        if cm is not None:
            ax = axes[idx]
            
            # Cria heatmap usando matplotlib (sem dependência do seaborn)
            im = ax.imshow(cm, interpolation='nearest', cmap='Blues')
            
            # Adiciona barra de cores
            plt.colorbar(im, ax=ax, label='Quantidade')
            
            # Configura os labels dos eixos
            ax.set_xticks(np.arange(len(classes)))
            ax.set_yticks(np.arange(len(classes)))
            ax.set_xticklabels(classes)
            ax.set_yticklabels(classes)
            
            # Adiciona os valores numéricos em cada célula
            thresh = cm.max() / 2.
            for i in range(len(classes)):
                for j in range(len(classes)):
                    text = ax.text(j, i, cm[i, j],
                                 ha="center", va="center",
                                 color="white" if cm[i, j] > thresh else "black")
            
            ax.set_xlabel('Predito pelo Modelo')
            ax.set_ylabel('Esperado (Ground Truth)')
            ax.set_title(f'Matriz de Confusão - {model_name}')
        else:
            axes[idx].text(0.5, 0.5, 'Matriz de confusão\nnão disponível', 
                          ha='center', va='center', transform=axes[idx].transAxes)
            axes[idx].set_title(f'{model_name}')
    
    plt.tight_layout()
    confusion_path = f'{output_dir}/confusion_matrices.png'
    plt.savefig(confusion_path, dpi=150, bbox_inches='tight')
    plt.close()
    
    print(f"Matrizes de confusão salvas em: {confusion_path}")
    return confusion_path

def print_comparison_summary(df, results_dict, metrics_dict):
    """Imprime resumo comparativo no terminal."""
    
    print("\n" + "="*60)
    print("RESUMO COMPARATIVO DOS MODELOS")
    print("="*60)
    
    gt_loaded = load_ground_truth(GROUND_TRUTH_PATH) is not None
    print(f"\nData: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
    print(f"Total de Avaliações Analisadas: {len(df)}")
    if gt_loaded:
        print("Validação: Usando Ground Truth da Carol e Samuel")
    else:
        print("Validação: Usando scores originais das avaliações")
    
    print("\n--- Resultados por Modelo ---\n")
    
    for model_name, result in results_dict.items():
        labels = result['labels']
        scores = result['scores']
        
        label_counts = pd.Series(labels).value_counts()
        avg_score = sum(scores) / len(scores) if scores else 0
        
        print(f"{model_name}:")
        print(f"  Modelo: {result['model_id']}")
        print(f"  Distribuição de Sentimentos:")
        
        for label in ['positive', 'negative', 'neutral']:
            count = label_counts.get(label, 0)
            percentage = (count / len(labels)) * 100
            print(f"    {label.capitalize()}: {count} ({percentage:.2f}%)")
        
        print(f"  Score Médio de Confiança: {avg_score:.4f}")
        
        if model_name in metrics_dict:
            metrics = metrics_dict[model_name]
            print(f"  Métricas de Desempenho:")
            print(f"    Acurácia: {metrics['accuracy']:.2%}")
            print(f"    Precisão: {metrics['precision']:.2%}")
            print(f"    Recall: {metrics['recall']:.2%}")
            print(f"    F1-Score: {metrics['f1_score']:.2%}")
            if metrics.get('roc_auc') is not None:
                print(f"    ROC AUC: {metrics['roc_auc']:.2%}")
            print(f"    Amostras Validadas: {metrics['n_samples']}")
        
        print()
    
    # Comparação lado a lado
    if len(metrics_dict) >= 2:
        print("--- Comparação Lado a Lado ---\n")
        
        model_names = list(metrics_dict.keys())
        if len(model_names) >= 2:
            model1_name = model_names[0]
            model2_name = model_names[1]
            model1_metrics = metrics_dict[model1_name]
            model2_metrics = metrics_dict[model2_name]
            
            print("Métricas de Desempenho:")
            print(f"{'Métrica':<15} {model1_name[:25]:<25} {model2_name[:25]:<25} {'Vencedor':<10}")
            print("-" * 80)
            
            metrics_to_compare = [
                ('Acurácia', 'accuracy'),
                ('Precisão', 'precision'),
                ('Recall', 'recall'),
                ('F1-Score', 'f1_score'),
                ('ROC AUC', 'roc_auc')
            ]
            
            for metric_name, metric_key in metrics_to_compare:
                val1 = model1_metrics.get(metric_key)
                val2 = model2_metrics.get(metric_key)
                
                if val1 is not None and val2 is not None:
                    if val2 > val1:
                        winner = model2_name[:10]
                    elif val1 > val2:
                        winner = model1_name[:10]
                    else:
                        winner = "Empate"
                    
                    val1_str = f"{val1:.2%}" if val1 is not None else "N/A"
                    val2_str = f"{val2:.2%}" if val2 is not None else "N/A"
                    print(f"{metric_name:<15} {val1_str:<25} {val2_str:<25} {winner:<10}")
            
            print()
            
            # Taxa de concordância
            if len(results_dict) == 2:
                labels1 = list(results_dict.values())[0]['labels']
                labels2 = list(results_dict.values())[1]['labels']
                
                agreements = sum(1 for l1, l2 in zip(labels1, labels2) if l1 == l2)
                agreement_rate = (agreements / len(labels1)) * 100
                
                print(f"Taxa de Concordância entre Modelos: {agreement_rate:.1f}% ({agreements}/{len(labels1)} avaliações)")
                
                if agreement_rate >= 80:
                    print("Alta Concordância: Modelos concordam na maioria dos casos")
                elif agreement_rate >= 60:
                    print("Concordância Moderada: Algumas diferenças esperadas entre modelos")
                else:
                    print("Baixa Concordância: Diferenças significativas entre modelos")
                
                print()
            
            # Recomendação
            if model2_metrics.get('accuracy', 0) > model1_metrics.get('accuracy', 0):
                print(f"Modelo Recomendado: {model2_name}")
                print("Este modelo apresenta melhor desempenho geral")
            else:
                print(f"Modelo Recomendado: {model1_name}")
                print("Este modelo apresenta melhor desempenho geral")

# --- Execução Principal ---

if __name__ == "__main__":
    """
    Fluxo principal do script:
    1. Carrega as avaliações do dataset
    2. Testa cada modelo (DistilBERT e BERTweet)
    3. Compara as predições com o ground truth (Carol e Samuel)
    4. Calcula métricas para avaliar o desempenho dos modelos
    5. Gera gráficos comparativos
    6. Imprime resumo comparativo no terminal
    """
    print("="*60)
    print("COMPARACAO FINAL DE MODELOS DE ANALISE DE SENTIMENTOS")
    print("="*60)
    
    # Passo 1: Carrega o dataset de avaliações
    print(f"\nCarregando dados de: {CSV_PATH}")
    df_reviews = load_data(CSV_PATH, limit=LIMIT_REVIEWS)
    
    if df_reviews is not None and not df_reviews.empty:
        # Passo 2: Testa cada modelo configurado
        # Cada modelo processa todas as avaliações e retorna predições + probabilidades
        results_dict = {}
        
        for model_config in MODELS:
            result = analyze_with_model(df_reviews, model_config)
            if result:
                results_dict[result['model_name']] = result
        
        # Só continua se ambos os modelos rodaram com sucesso
        if len(results_dict) >= 2:
            # Passo 3: Salva um CSV com todas as predições de ambos os modelos
            # Bom para análise posterior ou para ver casos específicos
            print(f"\nSalvando resultados comparativos...")
            
            df_comparison = df_reviews.copy()
            
            # Adiciona colunas com as predições de cada modelo
            for model_name, result in results_dict.items():
                # Normaliza o nome do modelo para usar como nome de coluna
                col_name = model_name.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')
                df_comparison[f'sentiment_label_{col_name}'] = result['labels']
                df_comparison[f'sentiment_score_{col_name}'] = result['scores']
            
            # Salva o CSV com tratamento correto de quebras de linha
            # Usa aspas duplas para campos que contêm quebras de linha ou vírgulas
            # Isso evita que o CSV seja quebrado incorretamente
            df_comparison.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8', 
                               sep=';', quoting=csv.QUOTE_ALL, quotechar='"', 
                               escapechar=None, doublequote=True)
            print(f"Resultados salvos em: {OUTPUT_CSV_PATH}")
            
            # Passo 4: Calcula as métricas comparando com o ground truth
            # Para descobrir se o modelo realmente aprendeu
            print(f"\nCalculando métricas usando ground truth (base da Carol e Samuel)...")
            metrics_dict = {}
            for model_name, result in results_dict.items():
                labels = result['labels']
                all_probs = result.get('all_probs', [])
                metrics = calculate_metrics(df_reviews, labels, all_probs, model_name, use_ground_truth=True)
                if metrics:
                    metrics_dict[model_name] = metrics
            
            # Passo 5: Gera os gráficos comparativos
            # Vai ajudar a entender qual modelo é melhor
            if len(metrics_dict) >= 2:
                print(f"\nGerando gráficos comparativos...")
                try:
                    plot_path = generate_plots(metrics_dict, output_dir='data')
                except Exception as e:
                    print(f"Erro ao gerar gráficos: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Passo 5b: Gera as matrizes de confusão
            # Mostra visualmente onde cada modelo está acertando e errando
            if len(metrics_dict) >= 1:
                print(f"\nGerando matrizes de confusão...")
                try:
                    confusion_path = generate_confusion_matrices(metrics_dict, output_dir='data')
                except Exception as e:
                    print(f"Erro ao gerar matrizes de confusão: {e}")
                    import traceback
                    traceback.print_exc()
            
            # Passo 6: Imprime resumo comparativo no terminal
            print(f"\nGerando resumo comparativo...")
            print_comparison_summary(df_reviews, results_dict, metrics_dict)
            
            # Resumo final
            print("\n" + "="*60)
            print("COMPARACAO CONCLUIDA")
            print("="*60)
            print(f"\nArquivos gerados:")
            print(f"   {OUTPUT_CSV_PATH}")
            if len(metrics_dict) >= 2:
                print(f"   data/model_comparison_plots.png")
            if len(metrics_dict) >= 1:
                print(f"   data/confusion_matrices.png")
        else:
            print("\nNão foi possível comparar: nem todos os modelos foram executados com sucesso.")
    else:
        print("\nFalha no carregamento dos dados.")

