"""
Script para testar classificação funcional (BusinessCapabilities) 
usando text-embedding-3-large + classificador multi-label.

Este é um teste separado, não afeta o código principal do projeto.
"""

import pandas as pd
import numpy as np
import os
import sys
from pathlib import Path
from openai import OpenAI
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, hamming_loss, jaccard_score
from sklearn.multioutput import MultiOutputClassifier
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, MultiLabelBinarizer
from dotenv import load_dotenv
import warnings
warnings.filterwarnings('ignore')

# Carregar variáveis de ambiente
env_path = Path(__file__).parent.parent / '.env'
if env_path.exists():
    load_dotenv(env_path)
else:
    load_dotenv()

# Configurações
CSV_PATH = '../data/app_review_dataset_ex.csv'
OUTPUT_CSV_PATH = 'results_functional_classification_embedding.csv'
OUTPUT_CLASSIFICATIONS_CSV = 'classifications_functional_embedding.csv'

TEXT_COLUMN = 'content'
LIMIT_REVIEWS = 1000

# Categorias funcionais (BusinessCapabilities)
CATEGORIES = [
    "PIX", "Login/Autenticação", "Performance", "Interface/Usabilidade",
    "Empréstimos/Crédito", "Pagamentos/Boletos", "Saldo/Extrato",
    "Atendimento", "Cadastro/Conta", "Investimentos", "Segurança",
    "Notificações", "Questões geográficas", "Tarifas/Cobranças", "Outros"
]

# Configuração OpenAI
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    print("ERRO: OPENAI_API_KEY não encontrada no ambiente.")
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
            embeddings.extend([[0] * 3072] * len(batch))
    
    return np.array(embeddings)

def prepare_labels_from_categories(df):
    """
    Prepara labels multi-label a partir das colunas de categoria no DataFrame.
    Se não existirem, cria labels dummy baseados em palavras-chave.
    """
    labels_list = []
    
    # Verificar se existem colunas de categoria no DataFrame
    category_cols = [cat for cat in CATEGORIES if cat in df.columns]
    
    if category_cols:
        print(f"   Usando {len(category_cols)} colunas de categoria do DataFrame")
        for idx, row in df.iterrows():
            row_labels = []
            for cat in category_cols:
                if row.get(cat, 0) == 1:
                    row_labels.append(cat)
            labels_list.append(row_labels)
    else:
        # Fallback: criar labels baseados em palavras-chave simples
        print("   Nenhuma coluna de categoria encontrada. Usando palavras-chave simples.")
        keywords_map = {
            'PIX': ['pix', 'transferência', 'transferencia'],
            'Login/Autenticação': ['login', 'senha', 'biometria', 'autenticação', 'acesso'],
            'Performance': ['lento', 'lentidão', 'travando', 'trava', 'bug', 'erro'],
            'Interface/Usabilidade': ['interface', 'tela', 'design', 'usabilidade'],
            'Empréstimos/Crédito': ['empréstimo', 'crédito', 'limite', 'cartão'],
            'Pagamentos/Boletos': ['boleto', 'pagamento', 'conta'],
            'Atendimento': ['atendimento', 'suporte', 'chat'],
            'Segurança': ['segurança', 'seguranca', 'privacidade'],
        }
        
        for idx, row in df.iterrows():
            text = str(row.get(TEXT_COLUMN, '')).lower()
            row_labels = []
            for cat, keywords in keywords_map.items():
                if any(kw in text for kw in keywords):
                    row_labels.append(cat)
            # Se não encontrou nenhuma, adiciona "Outros"
            if not row_labels:
                row_labels.append('Outros')
            labels_list.append(row_labels)
    
    return labels_list

def train_multilabel_classifier(embeddings, labels_binary):
    """Treina um classificador multi-label usando SVM."""
    print("Treinando classificador multi-label SVM...")
    
    # Normalizar embeddings
    scaler = StandardScaler()
    embeddings_scaled = scaler.fit_transform(embeddings)
    
    # Criar classificador multi-label
    base_classifier = SVC(kernel='rbf', probability=True, random_state=42)
    classifier = MultiOutputClassifier(base_classifier)
    
    classifier.fit(embeddings_scaled, labels_binary)
    
    return classifier, scaler

def predict_multilabel(classifier, scaler, embeddings):
    """Faz predições multi-label usando o classificador treinado."""
    embeddings_scaled = scaler.transform(embeddings)
    predictions_binary = classifier.predict(embeddings_scaled)
    probabilities = []
    
    # Obter probabilidades de cada classificador
    for i, estimator in enumerate(classifier.estimators_):
        prob = estimator.predict_proba(embeddings_scaled)
        probabilities.append(prob[:, 1] if prob.shape[1] > 1 else prob[:, 0])
    
    probabilities = np.array(probabilities).T
    
    return predictions_binary, probabilities

def calculate_multilabel_metrics(y_true, y_pred):
    """Calcula métricas para classificação multi-label."""
    # Exact Match Ratio (EMR)
    emr = accuracy_score(y_true, y_pred)
    
    # Hamming Loss
    hamming = hamming_loss(y_true, y_pred)
    
    # Jaccard Similarity
    jaccard = jaccard_score(y_true, y_pred, average='macro', zero_division=0)
    
    # Precision, Recall, F1 (macro)
    precision, recall, f1, _ = precision_recall_fscore_support(
        y_true, y_pred, average='macro', zero_division=0
    )
    
    # Precision, Recall, F1 (micro)
    precision_micro, recall_micro, f1_micro, _ = precision_recall_fscore_support(
        y_true, y_pred, average='micro', zero_division=0
    )
    
    metrics = {
        'exact_match_ratio': emr,
        'hamming_loss': hamming,
        'jaccard_similarity': jaccard,
        'precision_macro': precision,
        'recall_macro': recall,
        'f1_macro': f1,
        'precision_micro': precision_micro,
        'recall_micro': recall_micro,
        'f1_micro': f1_micro
    }
    
    return metrics

def main():
    """Função principal."""
    print("="*70)
    print("TESTE: Classificação Funcional com text-embedding-3-large + Multi-label SVM")
    print("="*70)
    
    # 1. Carregar dados
    print("\n1. Carregando dados...")
    df = load_data(CSV_PATH, limit=LIMIT_REVIEWS)
    if df is None:
        print("Erro ao carregar dados.")
        return
    
    # Filtrar apenas comentários negativos (score <= 2)
    if 'score' in df.columns:
        df_negative = df[df['score'] <= 2].copy()
        print(f"   Comentários negativos: {len(df_negative)}")
    else:
        df_negative = df.copy()
        print("   Aviso: Coluna 'score' não encontrada. Usando todos os comentários.")
    
    if len(df_negative) == 0:
        print("Erro: Nenhum comentário negativo encontrado.")
        return
    
    # 2. Preparar labels multi-label
    print("\n2. Preparando labels multi-label...")
    labels_list = prepare_labels_from_categories(df_negative)
    
    # Converter para formato binário
    mlb = MultiLabelBinarizer(classes=CATEGORIES)
    labels_binary = mlb.fit_transform(labels_list)
    
    print(f"   Total de categorias: {len(CATEGORIES)}")
    print(f"   Distribuição de labels por categoria:")
    for i, cat in enumerate(CATEGORIES):
        count = labels_binary[:, i].sum()
        if count > 0:
            print(f"      {cat}: {count} comentários")
    
    # 3. Gerar embeddings
    print("\n3. Gerando embeddings com text-embedding-3-large...")
    texts = df_negative[TEXT_COLUMN].tolist()
    embeddings = get_embeddings(texts)
    
    # 4. Filtrar categorias com pelo menos 2 classes no dataset completo
    print("\n4. Filtrando categorias válidas...")
    valid_categories = []
    valid_indices = []
    for i, cat in enumerate(CATEGORIES):
        if labels_binary[:, i].sum() > 0 and labels_binary[:, i].sum() < len(labels_binary):
            valid_categories.append(cat)
            valid_indices.append(i)
    
    if len(valid_categories) == 0:
        print("Erro: Nenhuma categoria válida encontrada.")
        return
    
    print(f"   Categorias válidas: {len(valid_categories)}/{len(CATEGORIES)}")
    labels_binary_filtered = labels_binary[:, valid_indices]
    
    # 5. Dividir em treino e teste (80/20)
    print("\n5. Dividindo em treino e teste...")
    X_train, X_test, y_train, y_test = train_test_split(
        embeddings, labels_binary_filtered, test_size=0.2, random_state=42
    )
    
    print(f"   Treino: {len(X_train)} casos")
    print(f"   Teste: {len(X_test)} casos")
    
    # 6. Treinar classificador
    print("\n6. Treinando classificador multi-label...")
    classifier, scaler = train_multilabel_classifier(X_train, y_train)
    
    # 7. Fazer predições
    print("\n7. Fazendo predições...")
    predictions_binary, probabilities = predict_multilabel(classifier, scaler, X_test)
    
    # 8. Calcular métricas
    print("\n8. Calculando métricas...")
    metrics = calculate_multilabel_metrics(y_test, predictions_binary)
    
    print("\n" + "="*70)
    print("RESULTADOS - Classificação Funcional")
    print("="*70)
    print(f"Exact Match Ratio (EMR): {metrics['exact_match_ratio']:.2%}")
    print(f"Hamming Loss: {metrics['hamming_loss']:.4f} (menor é melhor)")
    print(f"Jaccard Similarity: {metrics['jaccard_similarity']:.2%}")
    print(f"\nMétricas Macro (média não ponderada):")
    print(f"  Precisão: {metrics['precision_macro']:.2%}")
    print(f"  Recall: {metrics['recall_macro']:.2%}")
    print(f"  F1-Score: {metrics['f1_macro']:.2%}")
    print(f"\nMétricas Micro (agregadas):")
    print(f"  Precisão: {metrics['precision_micro']:.2%}")
    print(f"  Recall: {metrics['recall_micro']:.2%}")
    print(f"  F1-Score: {metrics['f1_micro']:.2%}")
    
    # Salvar resultados agregados
    results_df = pd.DataFrame({
        'Modelo': ['text-embedding-3-large + Multi-label SVM'],
        'EMR': [metrics['exact_match_ratio']],
        'Hamming_Loss': [metrics['hamming_loss']],
        'Jaccard_Similarity': [metrics['jaccard_similarity']],
        'Precision_Macro': [metrics['precision_macro']],
        'Recall_Macro': [metrics['recall_macro']],
        'F1_Macro': [metrics['f1_macro']],
        'Precision_Micro': [metrics['precision_micro']],
        'Recall_Micro': [metrics['recall_micro']],
        'F1_Micro': [metrics['f1_micro']]
    })
    results_df.to_csv(OUTPUT_CSV_PATH, index=False, encoding='utf-8')
    print(f"\nResultados agregados salvos em: {OUTPUT_CSV_PATH}")
    
    # Salvar classificações individuais
    test_df = df_negative.iloc[len(X_train):].reset_index(drop=True).copy()
    
    # Criar novo MultiLabelBinarizer apenas com categorias válidas
    mlb_valid = MultiLabelBinarizer(classes=valid_categories)
    
    # Converter predições binárias de volta para lista de categorias
    # Precisamos reconstruir o formato completo primeiro
    predictions_full = np.zeros((len(predictions_binary), len(CATEGORIES)))
    y_test_full = np.zeros((len(y_test), len(CATEGORIES)))
    
    for i, idx in enumerate(valid_indices):
        predictions_full[:, idx] = predictions_binary[:, i]
        y_test_full[:, idx] = y_test[:, i]
    
    predicted_labels = mlb.inverse_transform(predictions_full)
    expected_labels = mlb.inverse_transform(y_test_full)
    
    test_df['predicted_categories'] = [', '.join(labels) if labels else 'Nenhuma' for labels in predicted_labels]
    test_df['expected_categories'] = [', '.join(labels) if labels else 'Nenhuma' for labels in expected_labels]
    
    # Adicionar probabilidades por categoria (apenas válidas)
    for i, cat in enumerate(valid_categories):
        test_df[f'prob_{cat}'] = probabilities[:, i]
    
    # Selecionar colunas para salvar
    cols_to_save = ['content', 'expected_categories', 'predicted_categories']
    if 'reviewId' in test_df.columns:
        cols_to_save.insert(0, 'reviewId')
    if 'score' in test_df.columns:
        cols_to_save.append('score')
    
    # Adicionar colunas de probabilidade (apenas válidas)
    for cat in valid_categories:
        cols_to_save.append(f'prob_{cat}')
    
    classifications_df = test_df[cols_to_save].copy()
    classifications_df.to_csv(OUTPUT_CLASSIFICATIONS_CSV, index=False, encoding='utf-8', sep=';')
    print(f"Classificações individuais salvas em: {OUTPUT_CLASSIFICATIONS_CSV}")
    print(f"   Total de classificações: {len(classifications_df)}")
    
    print("\n" + "="*70)
    print("Teste concluído!")
    print("="*70)

if __name__ == '__main__':
    main()
