"""
Script para testar o modelo text-embedding-3-large da OpenAI
usando embeddings + classificador para análise de polarização.

Este é um teste separado, não afeta o código principal do projeto.
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from openai import OpenAI
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix, roc_curve, roc_auc_score
from sklearn.preprocessing import label_binarize
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Carregar variáveis de ambiente do .env do projeto principal
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# Configurações
CSV_PATH = '../data/app_review_dataset_ex.csv'
GROUND_TRUTH_PATH = '../data/ground_truth_dataset.csv'
OUTPUT_CSV_PATH = 'results_embedding_model.csv'
OUTPUT_CLASSIFICATIONS_CSV = 'classifications_embedding_model.csv'

TEXT_COLUMN = 'content'
LIMIT_REVIEWS = 1000

# Configuração OpenAI
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("ERRO: OPENAI_API_KEY não encontrada no ambiente.")
    print("Configure a variável OPENAI_API_KEY no arquivo .env ou no ambiente.")
    sys.exit(1)

client = OpenAI(api_key=api_key)

def load_data(path, limit=None):
    """Carrega o dataset de avaliações."""
    try:
        df = pd.read_csv(path, sep=';', quotechar='"', encoding='utf-8', on_bad_lines='skip', header=0)
        df.columns = [col.strip() for col in df.columns]
        
        if TEXT_COLUMN not in df.columns:
            print(f"Aviso: Coluna '{TEXT_COLUMN}' não encontrada.")
            return None
        
        df.dropna(subset=[TEXT_COLUMN], inplace=True)
        
        if limit and len(df) > limit:
            df = df.tail(limit)
            
        print(f"Dataset carregado: {len(df)} avaliações.")
        return df
    except Exception as e:
        print(f"Erro ao carregar o CSV: {e}")
        return None

def load_ground_truth(gt_path):
    """Carrega o ground truth criado pela classificação manual."""
    try:
        df_gt = pd.read_csv(gt_path, sep=';', encoding='utf-8', on_bad_lines='skip')
        df_gt.columns = [col.strip() for col in df_gt.columns]
        
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

def get_embeddings(texts, batch_size=100):
    """Gera embeddings usando text-embedding-3-large."""
    embeddings = []
    
    print(f"Gerando embeddings para {len(texts)} textos...")
    
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i+batch_size]
        
        try:
            response = client.embeddings.create(
                model="text-embedding-3-large",
                input=batch
            )
            
            batch_embeddings = [item.embedding for item in response.data]
            embeddings.extend(batch_embeddings)
            
            if (i + batch_size) % 200 == 0:
                print(f"   Processados: {min(i + batch_size, len(texts))}/{len(texts)}")
                
        except Exception as e:
            print(f"Erro ao gerar embeddings para batch {i}: {e}")
            # Em caso de erro, adiciona embeddings zeros
            embeddings.extend([[0] * 3072] * len(batch))
    
    return np.array(embeddings)

def train_classifier(embeddings, labels):
    """Treina um classificador SVM usando os embeddings."""
    print("Treinando classificador SVM...")
    
    # Normalizar embeddings
    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(embeddings)
    
    # Treinar SVM
    classifier = SVC(kernel='rbf', probability=True, random_state=42)
    classifier.fit(embeddings_scaled, labels)
    
    return classifier, scaler

def predict_with_classifier(classifier, scaler, embeddings):
    """Faz predições usando o classificador treinado."""
    embeddings_scaled = scaler.transform(embeddings)
    predictions = classifier.predict(embeddings_scaled)
    probabilities = classifier.predict_proba(embeddings_scaled)
    
    return predictions, probabilities

def calculate_metrics(df, predictions, probabilities, expected_labels, model_name):
    """Calcula métricas de desempenho."""
    
    # Remover casos onde não temos predição ou ground truth válido
    valid_mask = ~pd.isna(predictions) & ~pd.isna(expected_labels)
    predictions_valid = predictions[valid_mask]
    expected_valid = expected_labels[valid_mask]
    
    if len(predictions_valid) == 0:
        print(f"  [{model_name}] Nenhuma predição válida para calcular métricas.")
        return None
    
    # Accuracy
    accuracy = accuracy_score(expected_valid, predictions_valid)
    
    # Precision, Recall, F1-Score
    precision, recall, f1, _ = precision_recall_fscore_support(
        expected_valid, predictions_valid, 
        average='weighted', zero_division=0
    )
    
    # ROC AUC (precisa binarizar para multiclasse)
    classes = sorted(set(expected_valid) | set(predictions_valid))
    if len(classes) > 1:
        y_true_binary = label_binarize(expected_valid, classes=classes)
        
        # Ajustar probabilidades para as classes presentes
        y_prob = np.zeros((len(expected_valid), len(classes)))
        if len(probabilities) > 0 and len(probabilities[0]) == len(classes):
            y_prob = probabilities[valid_mask]
        else:
            # Se as probabilidades não correspondem, calcular manualmente
            for i, cls in enumerate(classes):
                y_prob[:, i] = (predictions_valid == cls).astype(float)
        
        try:
            if y_true_binary.shape[1] == 2:
                roc_auc = roc_auc_score(y_true_binary[:, 1], y_prob[:, 1])
            else:
                roc_aucs = []
                for idx, cls in enumerate(classes):
                    if np.sum(y_true_binary[:, idx]) > 0:
                        auc = roc_auc_score(y_true_binary[:, idx], y_prob[:, idx])
                        roc_aucs.append(auc)
                roc_auc = np.mean(roc_aucs) if roc_aucs else 0.0
        except:
            roc_auc = 0.0
    else:
        roc_auc = 0.0
    
    # Matriz de confusão
    cm = confusion_matrix(expected_valid, predictions_valid, labels=classes)
    
    metrics = {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1,
        'roc_auc': roc_auc,
        'confusion_matrix': cm,
        'n_samples': len(predictions_valid)
    }
    
    return metrics

def main():
    """Função principal."""
    print("="*70)
    print("TESTE: text-embedding-3-large + SVM Classifier")
    print("="*70)
    
    # 1. Carregar dados
    print("\n1. Carregando dados...")
    df = load_data(CSV_PATH, limit=LIMIT_REVIEWS)
    if df is None:
        print("Erro ao carregar dados.")
        return
    
    # 2. Carregar ground truth
    print("\n2. Carregando ground truth...")
    df_gt = load_ground_truth(GROUND_TRUTH_PATH)
    if df_gt is None:
        print("Aviso: Ground truth não encontrado. Usando scores originais.")
        df_gt = None
    
    # 3. Fazer merge com ground truth
    if df_gt is not None:
        if 'reviewId' in df.columns and 'reviewId' in df_gt.columns:
            df_merged = df.merge(df_gt[['reviewId', 'expected_sentiment']], on='reviewId', how='inner')
        elif 'content' in df.columns and 'content' in df_gt.columns:
            df_merged = df.merge(df_gt[['content', 'expected_sentiment']], on='content', how='inner')
        else:
            df_merged = df.copy()
            df_merged['expected_sentiment'] = None
    else:
        df_merged = df.copy()
        df_merged['expected_sentiment'] = None
    
    # Filtrar apenas casos com ground truth
    df_valid = df_merged[df_merged['expected_sentiment'].notna()].copy()
    
    if len(df_valid) == 0:
        print("Erro: Nenhum caso com ground truth encontrado.")
        return
    
    print(f"   Casos com ground truth: {len(df_valid)}")
    
    # 4. Gerar embeddings
    print("\n3. Gerando embeddings com text-embedding-3-large...")
    texts = df_valid[TEXT_COLUMN].tolist()
    embeddings = get_embeddings(texts)
    
    # 5. Preparar labels
    expected_labels = df_valid['expected_sentiment'].values
    
    # 6. Dividir em treino e teste (80/20)
    print("\n4. Dividindo em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(
        embeddings, expected_labels, test_size=0.2, random_state=42, stratify=expected_labels
    )
    
    print(f"   Treino: {len(X_train)} casos")
    print(f"   Teste: {len(X_test)} casos")
    
    # 7. Treinar classificador
    print("\n5. Treinando classificador...")
    classifier, scaler = train_classifier(X_train, y_train)
    
    # 8. Fazer predições no conjunto de teste
    print("\n6. Fazendo predições...")
    predictions, probabilities = predict_with_classifier(classifier, scaler, X_test)
    
    # 9. Calcular métricas
    print("\n7. Calculando métricas...")
    metrics = calculate_metrics(
        df_valid.iloc[len(X_train):], 
        predictions, 
        probabilities,
        y_test,
        'text-embedding-3-large + SVM'
    )
    
    if metrics:
        print("\n" + "="*70)
        print("RESULTADOS - text-embedding-3-large + SVM Classifier")
        print("="*70)
        print(f"Acurácia: {metrics['accuracy']:.2%}")
        print(f"Precisão: {metrics['precision']:.2%}")
        print(f"Recall: {metrics['recall']:.2%}")
        print(f"F1-Score: {metrics['f1_score']:.2%}")
        print(f"ROC AUC: {metrics['roc_auc']:.2%}")
        print(f"Amostras testadas: {metrics['n_samples']}")
        print("\nMatriz de Confusão:")
        print(metrics['confusion_matrix'])
        
        # Salvar resultados agregados
        results_df = pd.DataFrame({
            'Modelo': ['text-embedding-3-large + SVM'],
            'Acurácia': [metrics['accuracy']],
            'Precisão': [metrics['precision']],
            'Recall': [metrics['recall']],
            'F1-Score': [metrics['f1_score']],
            'ROC AUC': [metrics['roc_auc']],
            'Amostras': [metrics['n_samples']]
        })
        results_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
        print(f"\nResultados agregados salvos em: {OUTPUT_CSV_PATH}")
        
        # Salvar classificações individuais
        test_df = df_valid.iloc[len(X_train):].reset_index(drop=True).copy()
        test_df['predicted_sentiment'] = predictions
        test_df['expected_sentiment'] = y_test
        
        # Adicionar probabilidades
        classes = sorted(set(y_test))
        prob_df = pd.DataFrame(probabilities, columns=classes)
        for col in classes:
            test_df[f'prob_{col}'] = prob_df[col].values
        
        # Selecionar colunas relevantes para salvar
        cols_to_save = ['content', 'expected_sentiment', 'predicted_sentiment']
        if 'reviewId' in test_df.columns:
            cols_to_save.insert(0, 'reviewId')
        if 'score' in test_df.columns:
            cols_to_save.append('score')
        
        # Adicionar colunas de probabilidade
        for col in classes:
            cols_to_save.append(f'prob_{col}')
        
        classifications_df = test_df[cols_to_save].copy()
        classifications_df.to_csv(OUTPUT_CLASSIFICATIONS_CSV, index=False, encoding='utf-8', sep=';')
        print(f"Classificações individuais salvas em: {OUTPUT_CLASSIFICATIONS_CSV}")
        print(f"   Total de classificações: {len(classifications_df)}")
    
    print("\n" + "="*70)
    print("Teste concluído!")
    print("="*70)

if __name__ == '__main__':
    main()
