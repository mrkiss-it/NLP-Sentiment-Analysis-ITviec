"""Ablation ghép điểm khía cạnh vào TF-IDF (TV2 - Feature Engineering).

Lặp lại đúng giao thức đã dùng trong 01_data_exploration_eda.ipynb: chia
development/final test bằng random_state=2026, chỉ đánh giá bằng 5-fold
Stratified CV trên development, vectorizer và scaler fit lại trong từng fold.

Khác biệt so với ablation cũ: báo cáo thêm F1 từng lớp và Recall lớp Negative,
vì đó là hai chỉ số nhóm đang muốn cải thiện (Neutral F1, Recall Negative).

Cập nhật: chạy lại sau khi TV1 thay thuật toán Lexicon bằng Greedy Longest
Phrase Matching (độ bao phủ 12,26% -> 99,54%), bổ sung nhóm `Text + lexicon`.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.model_selection import StratifiedKFold, train_test_split
from sklearn.preprocessing import MinMaxScaler

import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.features import (  # noqa: E402
    ASPECT_RATING_FEATURES,
    LEXICON_FEATURES,
    deduplicate_modeling_rows,
)

SOURCE = PROJECT_ROOT / "data" / "processed" / "reviews_cleaned.xlsx"
REPORTS_DIR = PROJECT_ROOT / "reports"
RANDOM_STATE = 2026
NGRAM_RANGE = (1, 2)
MAX_FEATURES = 5000
MIN_DF = 2
LABELS = ["Negative", "Neutral", "Positive"]


def build_vectorizer() -> TfidfVectorizer:
    return TfidfVectorizer(
        max_features=MAX_FEATURES,
        ngram_range=NGRAM_RANGE,
        min_df=MIN_DF,
        sublinear_tf=True,
    )


def scaled_block(scaler: MinMaxScaler, frame: pd.DataFrame, columns, fit: bool):
    values = frame.loc[:, list(columns)].apply(pd.to_numeric, errors="coerce").fillna(0.0)
    matrix = scaler.fit_transform(values) if fit else scaler.transform(values)
    return sparse.csr_matrix(matrix)


def main() -> None:
    data = pd.read_excel(SOURCE)
    modeling_df, audit = deduplicate_modeling_rows(data)
    print(f"Dòng nguồn: {len(data)} | Dòng modeling: {len(modeling_df)} | Audit: {audit}")

    missing = modeling_df[list(ASPECT_RATING_FEATURES)].isna().mean().mul(100).round(2)
    print("\nTỷ lệ thiếu điểm khía cạnh (%):")
    print(missing.to_string())

    development_idx, _ = train_test_split(
        modeling_df.index,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=modeling_df["sentiment"],
    )
    development_df = modeling_df.loc[development_idx]
    print(f"\nDevelopment: {len(development_df)} dòng (final test khóa, không đánh giá).")

    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
    group_names = [
        "Text-only",
        "Text + lexicon",
        "Text + aspect",
        "Text + lexicon + aspect",
        "Aspect ratings only",
    ]
    records = {name: [] for name in group_names}

    for fold, (train_pos, valid_pos) in enumerate(
        cv.split(development_df, development_df["sentiment"]), start=1
    ):
        fold_train = development_df.iloc[train_pos]
        fold_valid = development_df.iloc[valid_pos]

        vectorizer = build_vectorizer()
        X_text_train = vectorizer.fit_transform(fold_train["clean_advance_text"].fillna(""))
        X_text_valid = vectorizer.transform(fold_valid["clean_advance_text"].fillna(""))

        lex_scaler, aspect_scaler = MinMaxScaler(), MinMaxScaler()
        X_lex_train = scaled_block(lex_scaler, fold_train, LEXICON_FEATURES, fit=True)
        X_lex_valid = scaled_block(lex_scaler, fold_valid, LEXICON_FEATURES, fit=False)
        X_asp_train = scaled_block(aspect_scaler, fold_train, ASPECT_RATING_FEATURES, fit=True)
        X_asp_valid = scaled_block(aspect_scaler, fold_valid, ASPECT_RATING_FEATURES, fit=False)

        feature_sets = {
            "Text-only": (X_text_train, X_text_valid),
            "Text + lexicon": (
                sparse.hstack([X_text_train, X_lex_train], format="csr"),
                sparse.hstack([X_text_valid, X_lex_valid], format="csr"),
            ),
            "Text + aspect": (
                sparse.hstack([X_text_train, X_asp_train], format="csr"),
                sparse.hstack([X_text_valid, X_asp_valid], format="csr"),
            ),
            "Text + lexicon + aspect": (
                sparse.hstack([X_text_train, X_lex_train, X_asp_train], format="csr"),
                sparse.hstack([X_text_valid, X_lex_valid, X_asp_valid], format="csr"),
            ),
            "Aspect ratings only": (X_asp_train, X_asp_valid),
        }

        for name, (X_tr, X_va) in feature_sets.items():
            model = LogisticRegression(
                max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE
            )
            model.fit(X_tr, fold_train["sentiment"])
            pred = model.predict(X_va)
            truth = fold_valid["sentiment"]
            per_class_f1 = f1_score(truth, pred, average=None, labels=LABELS)
            per_class_recall = recall_score(truth, pred, average=None, labels=LABELS)
            records[name].append(
                {
                    "accuracy": accuracy_score(truth, pred),
                    "macro_f1": f1_score(truth, pred, average="macro"),
                    "neutral_f1": per_class_f1[1],
                    "negative_f1": per_class_f1[0],
                    "negative_recall": per_class_recall[0],
                    "positive_f1": per_class_f1[2],
                }
            )
        print(f"  fold {fold}/5 xong")

    rows = []
    for name in group_names:
        frame = pd.DataFrame(records[name])
        row = {"feature_group": name}
        for column in frame.columns:
            row[column] = frame[column].mean()
            row[f"{column}_std"] = frame[column].std(ddof=0)
        rows.append(row)
    results = pd.DataFrame(rows)

    output = REPORTS_DIR / "aspect_hybrid_ablation.csv"
    results.to_csv(output, index=False)

    display_columns = [
        "feature_group",
        "macro_f1",
        "neutral_f1",
        "negative_recall",
        "negative_f1",
        "accuracy",
    ]
    print("\n===== KẾT QUẢ 5-FOLD CV TRÊN DEVELOPMENT =====")
    print(results[display_columns].round(4).to_string(index=False))
    print(f"\nĐã lưu: {output}")

    baseline = pd.DataFrame(records["Text-only"])
    print("\n===== SO SÁNH THEO CẶP FOLD VỚI TEXT-ONLY =====")
    print("(cùng fold, cùng seed nên chênh lệch từng fold so sánh trực tiếp được)")
    for name in group_names[1:]:
        frame = pd.DataFrame(records[name])
        delta = frame["macro_f1"] - baseline["macro_f1"]
        wins = int((delta > 0).sum())
        print(
            f"  {name:<24} Macro F1 delta = {delta.mean():+.4f} "
            f"(std {delta.std(ddof=0):.4f}, thắng {wins}/5 fold, "
            f"min {delta.min():+.4f}, max {delta.max():+.4f})"
        )

    per_fold = pd.concat(
        [pd.DataFrame(records[name]).assign(feature_group=name, fold=range(1, 6))
         for name in group_names],
        ignore_index=True,
    )
    per_fold_path = REPORTS_DIR / "aspect_hybrid_ablation_per_fold.csv"
    per_fold.to_csv(per_fold_path, index=False)
    print(f"\nĐã lưu chi tiết từng fold: {per_fold_path}")


if __name__ == "__main__":
    main()
