"""
Calcula matrizes de confusão (Negativo, Neutro, Positivo) para DistilBERT e BERTweet
sobre as 1.000 avaliações do ground truth (Carol/Samuel).

Saída: data/confusion_matrices_sentiment.json — consumida por generate_model_comparison_charts.py

Uso:
  python scripts/build_confusion_matrices_gt1000.py           # só BERTweet via sentiment_results + DistilBERT via modelo (demora)
  python scripts/build_confusion_matrices_gt1000.py --distil-from-comparison  # DistilBERT só onde há sentiment_comparison_final (366 linhas); demais linhas ficam sem DistilBERT no JSON (não usar)

Recomendado: rodar sem --distil-from-comparison para n=1000 completo nos dois modelos.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_recall_fscore_support,
    roc_auc_score,
)
from sklearn.preprocessing import label_binarize

ROOT = Path(__file__).resolve().parents[1]
GT_PATH = ROOT / "data" / "ground_truth_dataset.csv"
SR_PATH = ROOT / "data" / "sentiment_results.csv"
SC_PATH = ROOT / "data" / "sentiment_comparison_final.csv"
OUT_PATH = ROOT / "data" / "confusion_matrices_sentiment.json"

LABELS_EN = ["negative", "neutral", "positive"]


def _expand_from_cm(cm: np.ndarray) -> tuple[list[str], list[str]]:
    y_true: list[str] = []
    y_pred: list[str] = []
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            c = int(cm[i, j])
            y_true.extend([LABELS_EN[i]] * c)
            y_pred.extend([LABELS_EN[j]] * c)
    return y_true, y_pred


def _chart_metrics_from_cm(cm: np.ndarray) -> dict:
    y_true, y_pred = _expand_from_cm(cm)
    acc = float(accuracy_score(y_true, y_pred))
    p_w, r_w, f_w, _ = precision_recall_fscore_support(
        y_true, y_pred, labels=LABELS_EN, average="weighted", zero_division=0
    )
    yb = label_binarize(y_true, classes=LABELS_EN)
    y_score = np.full((len(y_pred), len(LABELS_EN)), 0.01)
    for k, lab in enumerate(y_pred):
        idx = LABELS_EN.index(lab)
        y_score[k, idx] = 0.98
    try:
        auc = float(
            roc_auc_score(yb, y_score, average="weighted", multi_class="ovr")
        )
    except ValueError:
        auc = float("nan")
    return {
        "accuracy_pct": round(acc * 100, 2),
        "precision_weighted_pct": round(float(p_w) * 100, 2),
        "recall_weighted_pct": round(float(r_w) * 100, 2),
        "f1_weighted_pct": round(float(f_w) * 100, 2),
        "roc_auc_weighted_ovr_pct": round(auc * 100, 2),
    }


def _expected_from_gt(row: pd.Series) -> str | None:
    if row.get("negative", 0) == 1:
        return "negative"
    if row.get("positive", 0) == 1:
        return "positive"
    if row.get("neutral", 0) == 1:
        return "neutral"
    return None


def _run_distilbert_on_texts(texts: list[str]) -> list[str]:
    from transformers import pipeline

    model_id = "lxyuan/distilbert-base-multilingual-cased-sentiments-student"
    pipe = pipeline(
        "sentiment-analysis",
        model=model_id,
        tokenizer=model_id,
        return_all_scores=False,
        device=-1,
    )
    labels: list[str] = []
    batch_size = 16
    for i in range(0, len(texts), batch_size):
        batch = texts[i : i + batch_size]
        out = pipe(batch)
        if not isinstance(out, list):
            out = [out]
        for item in out:
            lab = str(item.get("label", "")).lower()
            if "pos" in lab:
                labels.append("positive")
            elif "neg" in lab:
                labels.append("negative")
            elif "neu" in lab:
                labels.append("neutral")
            else:
                labels.append(lab)
    return labels


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--distil-from-comparison",
        action="store_true",
        help="Usa apenas as 366 linhas comuns ao sentiment_comparison_final (não recomendado para TCC n=1000)",
    )
    args = parser.parse_args()

    gt = pd.read_csv(GT_PATH, sep=";", encoding="utf-8")
    gt["expected"] = gt.apply(_expected_from_gt, axis=1)
    gt = gt.dropna(subset=["expected"])
    gt["reviewId"] = gt["reviewId"].astype(str)

    if len(gt) != 1000:
        print(f"Aviso: ground truth tem {len(gt)} linhas (esperado 1000)")

    # --- BERTweet: sentiment_results (mesmo modelo do pipeline do projeto) ---
    sr = pd.read_csv(SR_PATH, encoding="utf-8", on_bad_lines="skip")
    sr.columns = [c.strip() for c in sr.columns]
    sr["reviewId"] = sr["reviewId"].astype(str)
    mb = gt.merge(sr[["reviewId", "sentiment_label"]], on="reviewId", how="inner")
    if len(mb) != len(gt):
        print(f"Aviso: sentiment_results cobre {len(mb)}/{len(gt)} reviewIds")
    cm_bert = confusion_matrix(mb["expected"], mb["sentiment_label"], labels=LABELS_EN)
    acc_bert = float((mb["expected"] == mb["sentiment_label"]).mean())

    # --- DistilBERT ---
    if args.distil_from_comparison:
        sc = pd.read_csv(SC_PATH, sep=";", encoding="utf-8", on_bad_lines="skip")
        sc.columns = [c.strip() for c in sc.columns]
        sc["reviewId"] = sc["reviewId"].astype(str)
        col_d = "sentiment_label_DistilBERT_Multilíngue"
        md = gt.merge(sc[["reviewId", col_d]], on="reviewId", how="inner")
        cm_distil = confusion_matrix(md["expected"], md[col_d], labels=LABELS_EN)
        acc_distil = float((md["expected"] == md[col_d]).mean())
        n_distil = len(md)
    else:
        print("Executando DistilBERT Multilíngue nos textos do ground truth (CPU; pode levar alguns minutos)...")
        texts = gt.sort_values("reviewId")["content"].astype(str).tolist()
        preds = _run_distilbert_on_texts(texts)
        # alinhar predições à ordem de gt.sort_values
        gts = gt.sort_values("reviewId")["expected"].tolist()
        cm_distil = confusion_matrix(gts, preds, labels=LABELS_EN)
        acc_distil = float(np.mean(np.array(gts) == np.array(preds)))
        n_distil = len(gts)

    payload = {
        "n_samples": int(len(gt)),
        "labels_order": LABELS_EN,
        "distilbert": {
            "matrix": cm_distil.tolist(),
            "accuracy": round(acc_distil, 6),
            "n_evaluated": int(n_distil),
            "chart_metrics": _chart_metrics_from_cm(cm_distil),
        },
        "bertweet": {
            "matrix": cm_bert.tolist(),
            "accuracy": round(acc_bert, 6),
            "n_evaluated": int(len(mb)),
            "chart_metrics": _chart_metrics_from_cm(cm_bert),
        },
        "notes": "Matrizes no sklearn: linha=classe verdadeira, coluna=classe predita; ordem negative, neutral, positive. "
        "ROC AUC no JSON usa scores one-hot a partir das classes preditas (limite superior conservador se não houver probabilidades).",
    }

    OUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUT_PATH.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Salvo: {OUT_PATH}")
    print(json.dumps(payload, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
