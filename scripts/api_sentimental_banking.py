"""
API SentimentalBanking
Correlação Funcional e Priorização de Backlog em Apps Bancários

Esta API permite:
- Processar avaliações de apps bancários
- Obter análise de sentimentos
- Obter categorização funcional
- Obter backlog priorizado
- Obter métricas de validação
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.responses import JSONResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import pandas as pd
import os
from datetime import datetime
import json

# Importar funções dos scripts existentes
import sys
import importlib.util

# Caminho base dos scripts
SCRIPTS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPTS_DIR)

# Função auxiliar para importar módulos
def load_module(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

# Importar módulos
sentiment_module = load_module('sentiment_analysis', os.path.join(SCRIPTS_DIR, 'sentiment_analysis.py'))
functional_module = load_module('functional_correlation', os.path.join(SCRIPTS_DIR, 'functional_correlation.py'))
backlog_module = load_module('generate_backlog_report', os.path.join(SCRIPTS_DIR, 'generate_backlog_report.py'))

# Extrair funções e constantes
load_data = sentiment_module.load_data
analyze_sentiment = sentiment_module.analyze_sentiment
load_sentiment_results = functional_module.load_sentiment_results
CATEGORIES = functional_module.CATEGORIES
calculate_priorities = backlog_module.calculate_priorities
IMPACT_WEIGHTS = backlog_module.IMPACT_WEIGHTS
RECOMMENDATIONS = backlog_module.RECOMMENDATIONS

app = FastAPI(
    title="API SentimentalBanking",
    description="API para correlação funcional e priorização de backlog em apps bancários",
    version="1.0.0"
)

# Configurações - usar caminhos absolutos
SENTIMENT_RESULTS_PATH = os.path.join(PROJECT_ROOT, 'sentiment_results.csv')
FUNCTIONAL_CORRELATION_PATH = os.path.join(PROJECT_ROOT, 'functional_correlation_results.csv')
GROUND_TRUTH_PATH = os.path.join(PROJECT_ROOT, 'data', 'ground_truth_dataset.csv')

# Modelos Pydantic para validação
class Review(BaseModel):
    content: str
    score: Optional[int] = None
    date: Optional[str] = None
    version: Optional[str] = None
    app_name: Optional[str] = None

class ReviewBatch(BaseModel):
    reviews: List[Review]

class BacklogRequest(BaseModel):
    app_name: Optional[str] = None
    min_priority: Optional[float] = 0.0
    limit: Optional[int] = None

# Endpoints

@app.get("/")
async def root():
    """Endpoint raiz com informações da API."""
    return {
        "api": "SentimentalBanking",
        "version": "1.0.0",
        "description": "API para correlação funcional e priorização de backlog",
        "endpoints": {
            "/docs": "Documentação interativa (Swagger)",
            "/health": "Status da API",
            "/sentiment/analyze": "Analisar sentimentos de avaliações",
            "/sentiment/results": "Obter resultados de análise de sentimentos",
            "/functional/categorize": "Categorizar avaliações por funcionalidade",
            "/functional/results": "Obter resultados de categorização funcional",
            "/backlog/prioritized": "Obter backlog priorizado",
            "/metrics/validation": "Obter métricas de validação"
        }
    }

@app.get("/health")
async def health_check():
    """Verifica o status da API e arquivos necessários."""
    status = {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "files": {
            "sentiment_results": os.path.exists(SENTIMENT_RESULTS_PATH),
            "functional_correlation": os.path.exists(FUNCTIONAL_CORRELATION_PATH),
            "ground_truth": os.path.exists(GROUND_TRUTH_PATH)
        }
    }
    return status

@app.post("/sentiment/analyze")
async def analyze_sentiments_endpoint(reviews: ReviewBatch):
    """
    Analisa sentimentos de um lote de avaliações.
    
    Retorna análise de sentimentos (positive/negative/neutral) para cada avaliação.
    """
    try:
        # Converter para DataFrame
        reviews_data = []
        for review in reviews.reviews:
            reviews_data.append({
                'content': review.content,
                'score': review.score,
                'date': review.date,
                'version': review.version,
                'app_name': review.app_name
            })
        
        df = pd.DataFrame(reviews_data)
        
        # Executar análise de sentimentos
        df_result = analyze_sentiment(df)
        
        if df_result is None:
            raise HTTPException(status_code=500, detail="Erro ao analisar sentimentos")
        
        # Converter para formato JSON
        results = []
        for _, row in df_result.iterrows():
            results.append({
                'content': row['content'],
                'sentiment_label': row.get('sentiment_label', 'unknown'),
                'sentiment_score': float(row.get('sentiment_score', 0.0)),
                'score': int(row.get('score', 0)) if pd.notna(row.get('score')) else None
            })
        
        return {
            "total_reviews": len(results),
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao processar: {str(e)}")

@app.get("/sentiment/results")
async def get_sentiment_results(
    format: str = Query("json", regex="^(json|csv)$"),
    app_name: Optional[str] = None,
    sentiment: Optional[str] = Query(None, regex="^(positive|negative|neutral)$"),
    limit: Optional[int] = Query(None, ge=1)
):
    """
    Obtém resultados de análise de sentimentos já processados.
    
    Parâmetros:
    - format: Formato de retorno (json ou csv)
    - app_name: Filtrar por nome do app
    - sentiment: Filtrar por sentimento (positive/negative/neutral)
    - limit: Limitar número de resultados retornados
    """
    try:
        if not os.path.exists(SENTIMENT_RESULTS_PATH):
            raise HTTPException(status_code=404, detail="Arquivo de resultados não encontrado")
        
        df = load_data(SENTIMENT_RESULTS_PATH)
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")
        
        # Aplicar filtros
        if app_name:
            df = df[df['app_name'] == app_name]
        
        if sentiment:
            df = df[df['sentiment_label'] == sentiment]
        
        # Aplicar limite se especificado
        if limit:
            df = df.head(limit)
        
        if df.empty:
            return {"message": "Nenhum resultado encontrado com os filtros aplicados", "results": []}
        
        # Retornar no formato solicitado
        if format == "csv":
            csv_path = os.path.join(PROJECT_ROOT, "temp_sentiment_results.csv")
            df.to_csv(csv_path, index=False, sep=';', encoding='utf-8')
            return FileResponse(csv_path, filename="sentiment_results.csv", media_type="text/csv")
        else:
            results = df.to_dict(orient='records')
            return {
                "total": len(results),
                "filters": {
                    "app_name": app_name,
                    "sentiment": sentiment,
                    "limit": limit
                },
                "results": results
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter resultados: {str(e)}")

@app.get("/functional/results")
async def get_functional_results(
    format: str = Query("json", regex="^(json|csv)$"),
    app_name: Optional[str] = None,
    category: Optional[str] = None
):
    """
    Obtém resultados de categorização funcional.
    
    Parâmetros:
    - format: Formato de retorno (json ou csv)
    - app_name: Filtrar por nome do app
    - category: Filtrar por categoria funcional
    """
    try:
        if not os.path.exists(FUNCTIONAL_CORRELATION_PATH):
            raise HTTPException(status_code=404, detail="Arquivo de resultados não encontrado")
        
        df = load_sentiment_results(FUNCTIONAL_CORRELATION_PATH)
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")
        
        # Aplicar filtros
        if app_name:
            df = df[df['app_name'] == app_name]
        
        if category and category in df.columns:
            df = df[df[category] == 1]
        
        if df.empty:
            return {"message": "Nenhum resultado encontrado com os filtros aplicados", "results": []}
        
        # Retornar no formato solicitado
        if format == "csv":
            csv_path = os.path.join(PROJECT_ROOT, "temp_functional_results.csv")
            df.to_csv(csv_path, index=False, sep=';', encoding='utf-8')
            return FileResponse(csv_path, filename="functional_results.csv", media_type="text/csv")
        else:
            results = df.to_dict(orient='records')
            return {
                "total": len(results),
                "filters": {
                    "app_name": app_name,
                    "category": category
                },
                "results": results
            }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao obter resultados: {str(e)}")

@app.get("/backlog/prioritized")
async def get_prioritized_backlog(
    app_name: Optional[str] = None,
    min_priority: float = Query(0.0, ge=0.0, le=1.0),
    limit: Optional[int] = Query(None, ge=1)
):
    """
    Obtém backlog priorizado baseado em frequência, severidade e impacto.
    
    Parâmetros:
    - app_name: Filtrar por nome do app
    - min_priority: Prioridade mínima (0.0 a 1.0)
    - limit: Limitar número de categorias retornadas
    """
    try:
        if not os.path.exists(FUNCTIONAL_CORRELATION_PATH):
            raise HTTPException(status_code=404, detail="Arquivo de resultados não encontrado")
        
        df = load_sentiment_results(FUNCTIONAL_CORRELATION_PATH)
        
        if df is None or df.empty:
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")
        
        # Filtrar por app se especificado
        if app_name:
            df = df[df['app_name'] == app_name]
        
        if df.empty:
            return {"message": "Nenhum resultado encontrado", "backlog": []}
        
        # Calcular prioridades
        sorted_priorities, category_counts, category_severity = calculate_priorities(df)
        
        # Filtrar por prioridade mínima e limitar
        backlog_items = []
        for category, priority in sorted_priorities:
            if priority >= min_priority:
                count = category_counts[category]
                severity = category_severity.get(category, 0)
                
                # Determinar nível de prioridade
                if priority >= 0.7:
                    priority_level = "CRITICA"
                elif priority >= 0.5:
                    priority_level = "ALTA"
                elif priority >= 0.3:
                    priority_level = "MEDIA"
                else:
                    priority_level = "BAIXA"
                
                backlog_items.append({
                    "category": category,
                    "priority_score": round(priority, 4),
                    "priority_level": priority_level,
                    "frequency": count,
                    "frequency_percentage": round((count / len(df)) * 100, 2),
                    "average_severity": round(severity, 2),
                    "recommendation": RECOMMENDATIONS.get(category, "Análise detalhada necessária.")
                })
                
                if limit and len(backlog_items) >= limit:
                    break
        
        return {
            "total_categories": len(backlog_items),
            "total_reviews": len(df),
            "filters": {
                "app_name": app_name,
                "min_priority": min_priority
            },
            "backlog": backlog_items
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao gerar backlog: {str(e)}")

@app.get("/metrics/validation")
async def get_validation_metrics():
    """
    Obtém métricas de validação do modelo comparando com ground truth.
    
    Retorna métricas de acurácia, precisão, recall e F1-Score.
    """
    try:
        if not os.path.exists(GROUND_TRUTH_PATH):
            raise HTTPException(status_code=404, detail="Ground truth não encontrado")
        
        # Carregar ground truth e resultados
        df_gt = pd.read_csv(GROUND_TRUTH_PATH, sep=';', encoding='utf-8')
        df_results = load_sentiment_results(SENTIMENT_RESULTS_PATH)
        
        if df_results is None or df_results.empty:
            raise HTTPException(status_code=404, detail="Resultados não encontrados")
        
        # Fazer merge
        if 'reviewId' in df_results.columns and 'reviewId' in df_gt.columns:
            df_merged = df_results.merge(df_gt[['reviewId', 'expected_sentiment']], on='reviewId', how='inner')
        elif 'content' in df_results.columns and 'content' in df_gt.columns:
            df_merged = df_results.merge(df_gt[['content', 'expected_sentiment']], on='content', how='inner')
        else:
            raise HTTPException(status_code=400, detail="Não foi possível fazer merge dos dados")
        
        if df_merged.empty:
            return {"message": "Nenhuma avaliação em comum encontrada", "metrics": {}}
        
        # Calcular métricas básicas
        from sklearn.metrics import accuracy_score, precision_recall_fscore_support
        
        expected = df_merged['expected_sentiment'].tolist()
        predicted = df_merged['sentiment_label'].tolist()
        
        accuracy = accuracy_score(expected, predicted)
        precision, recall, f1, _ = precision_recall_fscore_support(
            expected, predicted, average='weighted', zero_division=0
        )
        
        # Contagem por classe
        from collections import Counter
        expected_counts = Counter(expected)
        predicted_counts = Counter(predicted)
        
        return {
            "total_samples": len(df_merged),
            "metrics": {
                "accuracy": round(accuracy, 4),
                "precision": round(precision, 4),
                "recall": round(recall, 4),
                "f1_score": round(f1, 4)
            },
            "distribution": {
                "expected": dict(expected_counts),
                "predicted": dict(predicted_counts)
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao calcular métricas: {str(e)}")

@app.get("/categories/list")
async def list_categories():
    """Lista todas as categorias funcionais disponíveis."""
    return {
        "total_categories": len(CATEGORIES),
        "categories": CATEGORIES,
        "impact_weights": IMPACT_WEIGHTS
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

