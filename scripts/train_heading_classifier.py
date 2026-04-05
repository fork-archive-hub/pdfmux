#!/usr/bin/env python3
"""Train a heading classifier using doc-level cross-validation.

Uses gradient boosted trees on font features. Validates with 5-fold
doc-level CV to prevent overfitting (never train on lines from a doc
you test on).

Output: src/pdfmux/models/heading_classifier.pkl
"""

import json
import os
import pickle
import sys
from pathlib import Path

import numpy as np
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.model_selection import GroupKFold
from sklearn.metrics import classification_report, f1_score, precision_score, recall_score
from sklearn.calibration import CalibratedClassifierCV

DATA_PATH = Path(__file__).parent.parent / "heading_features.jsonl"
MODEL_DIR = Path(__file__).parent.parent / "src/pdfmux/models"
MODEL_PATH = MODEL_DIR / "heading_classifier.pkl"

FEATURE_COLS = [
    "size_ratio",
    "is_bold",
    "text_length",
    "word_count",
    "has_period",
    "is_all_caps",
    "is_numeric",
    "starts_with_number",
    "y_position_pct",
    "char_density",
    "has_colon",
    "has_question_mark",
]


def load_data():
    """Load features from JSONL file."""
    records = []
    with open(DATA_PATH) as f:
        for line in f:
            records.append(json.loads(line))

    X = np.array([[r[col] for col in FEATURE_COLS] for r in records], dtype=np.float32)
    y = np.array([r["label"] for r in records], dtype=np.int32)
    groups = np.array([r["doc_id"] for r in records])
    texts = [r["text"] for r in records]

    return X, y, groups, texts


def cross_validate(X, y, groups):
    """5-fold doc-level cross-validation."""
    gkf = GroupKFold(n_splits=5)

    all_preds = np.zeros(len(y))
    all_probs = np.zeros(len(y))

    for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups)):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # Handle class imbalance with sample weights
        n_pos = y_train.sum()
        n_neg = len(y_train) - n_pos
        weight_pos = n_neg / n_pos if n_pos > 0 else 1.0
        sample_weights = np.where(y_train == 1, weight_pos, 1.0)

        clf = GradientBoostingClassifier(
            n_estimators=100,
            max_depth=4,
            min_samples_leaf=10,
            learning_rate=0.1,
            subsample=0.8,
            random_state=42,
        )
        clf.fit(X_train, y_train, sample_weight=sample_weights)

        preds = clf.predict(X_test)
        probs = clf.predict_proba(X_test)[:, 1]

        all_preds[test_idx] = preds
        all_probs[test_idx] = probs

        fold_f1 = f1_score(y_test, preds)
        fold_prec = precision_score(y_test, preds, zero_division=0)
        fold_rec = recall_score(y_test, preds)
        n_test_docs = len(set(groups[test_idx]))

        print(f"Fold {fold+1}: F1={fold_f1:.3f} P={fold_prec:.3f} R={fold_rec:.3f} "
              f"({n_test_docs} docs, {y_test.sum()} headings)")

    print("\n=== Overall CV Results ===")
    print(classification_report(y, all_preds, target_names=["body", "heading"]))

    # Show false positives and false negatives
    return all_preds, all_probs


def train_final_model(X, y):
    """Train final model on ALL data for production use."""
    n_pos = y.sum()
    n_neg = len(y) - n_pos
    weight_pos = n_neg / n_pos if n_pos > 0 else 1.0
    sample_weights = np.where(y == 1, weight_pos, 1.0)

    clf = GradientBoostingClassifier(
        n_estimators=100,
        max_depth=4,
        min_samples_leaf=10,
        learning_rate=0.1,
        subsample=0.8,
        random_state=42,
    )
    clf.fit(X, y, sample_weight=sample_weights)

    return clf


def main():
    print("Loading data...")
    X, y, groups, texts = load_data()
    print(f"  {len(X)} samples, {y.sum()} headings, {len(set(groups))} docs")
    print(f"  Features: {FEATURE_COLS}")
    print()

    print("=== 5-Fold Doc-Level Cross-Validation ===")
    preds, probs = cross_validate(X, y, groups)

    # Show errors
    print("\n=== False Positives (body text classified as heading) ===")
    fp_mask = (preds == 1) & (y == 0)
    fp_indices = np.where(fp_mask)[0]
    for idx in fp_indices[:10]:
        print(f"  [{groups[idx]}] prob={probs[idx]:.3f}: {texts[idx][:60]}")

    print(f"\n=== False Negatives (headings missed) ===")
    fn_mask = (preds == 0) & (y == 1)
    fn_indices = np.where(fn_mask)[0]
    for idx in fn_indices[:10]:
        print(f"  [{groups[idx]}] prob={probs[idx]:.3f}: {texts[idx][:60]}")

    # Feature importance
    print("\n=== Feature Importance (from final fold) ===")
    # Train one more model to get importances
    clf_temp = GradientBoostingClassifier(
        n_estimators=100, max_depth=4, min_samples_leaf=10,
        learning_rate=0.1, subsample=0.8, random_state=42
    )
    n_pos = y.sum()
    n_neg = len(y) - n_pos
    weights = np.where(y == 1, n_neg / n_pos, 1.0)
    clf_temp.fit(X, y, sample_weight=weights)
    importances = clf_temp.feature_importances_
    for name, imp in sorted(zip(FEATURE_COLS, importances), key=lambda x: -x[1]):
        print(f"  {name:25s} {imp:.4f}")

    # Train final model
    print("\n=== Training Final Model ===")
    model = train_final_model(X, y)

    # Save
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump({
            "model": model,
            "feature_cols": FEATURE_COLS,
            "threshold": 0.5,
            "version": "v1",
            "n_samples": len(X),
            "n_headings": int(y.sum()),
        }, f)

    model_size = os.path.getsize(MODEL_PATH)
    print(f"  Model saved: {MODEL_PATH} ({model_size / 1024:.1f} KB)")

    # Verify
    test_probs = model.predict_proba(X)[:, 1]
    test_preds = (test_probs >= 0.5).astype(int)
    train_f1 = f1_score(y, test_preds)
    print(f"  Train F1: {train_f1:.3f} (full dataset — expect higher than CV)")


if __name__ == "__main__":
    main()
