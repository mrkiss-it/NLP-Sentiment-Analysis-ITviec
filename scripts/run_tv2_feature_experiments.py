"""Ba thí nghiệm còn thiếu của phần trích xuất đặc trưng.

1. Thống kê token rỗng và review quá ngắn sau tiền xử lý.
2. So sánh hai phương pháp vector hóa TF-IDF và Bag-of-Words.
3. So sánh hai chiến lược cân bằng lớp: class_weight='balanced' và SMOTE.

Giao thức giống các thí nghiệm trước: 5-fold Stratified CV trên tập phát triển,
random_state=2026, vectorizer fit lại trong từng fold. SMOTE chỉ áp dụng trên
phần huấn luyện của mỗi fold, không bao giờ trên phần kiểm định.
"""

import sys
from pathlib import Path

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, recall_score
from sklearn.model_selection import StratifiedKFold, train_test_split

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.features import apply_smote, deduplicate_modeling_rows  # noqa: E402

SOURCE = PROJECT_ROOT / "data" / "processed" / "reviews_cleaned.xlsx"
REPORTS_DIR = PROJECT_ROOT / "reports"
RANDOM_STATE = 2026
NGRAM_RANGE = (1, 2)
MAX_FEATURES = 5000
MIN_DF = 2
LABELS = ["Negative", "Neutral", "Positive"]


def score(truth, pred) -> dict:
    per_class_f1 = f1_score(truth, pred, average=None, labels=LABELS)
    per_class_recall = recall_score(truth, pred, average=None, labels=LABELS)
    return {
        "accuracy": accuracy_score(truth, pred),
        "macro_f1": f1_score(truth, pred, average="macro"),
        "neutral_f1": per_class_f1[1],
        "negative_f1": per_class_f1[0],
        "negative_recall": per_class_recall[0],
    }


def summarise(records: dict[str, list[dict]], names: list[str]) -> pd.DataFrame:
    rows = []
    for name in names:
        frame = pd.DataFrame(records[name])
        row = {"config": name}
        for column in frame.columns:
            row[column] = frame[column].mean()
            row[f"{column}_std"] = frame[column].std(ddof=0)
        rows.append(row)
    return pd.DataFrame(rows)


def empty_token_stats(modeling_df: pd.DataFrame) -> pd.DataFrame:
    text = modeling_df["clean_advance_text"].fillna("")
    counts = text.str.split().apply(len)
    rows = [
        ("Chuỗi rỗng hoàn toàn", int((text.str.strip() == "").sum())),
        ("Dưới 3 token", int((counts < 3).sum())),
        ("Dưới 5 token", int((counts < 5).sum())),
        ("Dưới 10 token", int((counts < 10).sum())),
    ]
    total = len(modeling_df)
    frame = pd.DataFrame(rows, columns=["nhom", "so_review"])
    frame["ty_le_phan_tram"] = (frame["so_review"] / total * 100).round(2)
    print("\n===== 1. THỐNG KÊ TOKEN RỖNG VÀ REVIEW NGẮN =====")
    print(f"Tổng số review dùng cho mô hình: {total}")
    print(frame.to_string(index=False))
    print(f"\nSố token trung bình: {counts.mean():.2f} | trung vị: {counts.median():.0f} "
          f"| nhỏ nhất: {counts.min()} | lớn nhất: {counts.max()}")
    return frame


def main() -> None:
    data = pd.read_excel(SOURCE)
    modeling_df, _ = deduplicate_modeling_rows(data)

    empty_stats = empty_token_stats(modeling_df)
    empty_stats.to_csv(REPORTS_DIR / "tv2_empty_token_stats.csv", index=False)

    development_idx, _ = train_test_split(
        modeling_df.index,
        test_size=0.2,
        random_state=RANDOM_STATE,
        stratify=modeling_df["sentiment"],
    )
    development_df = modeling_df.loc[development_idx]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)

    vector_names = ["TF-IDF (sublinear)", "Bag-of-Words"]
    balance_names = ["class_weight='balanced'", "SMOTE (không trọng số lớp)", "Không xử lý"]
    vector_records = {name: [] for name in vector_names}
    balance_records = {name: [] for name in balance_names}

    for fold, (train_pos, valid_pos) in enumerate(
        cv.split(development_df, development_df["sentiment"]), start=1
    ):
        fold_train = development_df.iloc[train_pos]
        fold_valid = development_df.iloc[valid_pos]
        train_text = fold_train["clean_advance_text"].fillna("")
        valid_text = fold_valid["clean_advance_text"].fillna("")
        y_train, y_valid = fold_train["sentiment"], fold_valid["sentiment"]

        options = dict(max_features=MAX_FEATURES, ngram_range=NGRAM_RANGE, min_df=MIN_DF)
        vectorizers = {
            "TF-IDF (sublinear)": TfidfVectorizer(**options, sublinear_tf=True),
            "Bag-of-Words": CountVectorizer(**options),
        }
        matrices = {}
        for name, vectorizer in vectorizers.items():
            X_tr = vectorizer.fit_transform(train_text)
            X_va = vectorizer.transform(valid_text)
            matrices[name] = (X_tr, X_va)
            model = LogisticRegression(
                max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE
            )
            model.fit(X_tr, y_train)
            vector_records[name].append(score(y_valid, model.predict(X_va)))

        X_tr, X_va = matrices["TF-IDF (sublinear)"]
        for name in balance_names:
            if name == "class_weight='balanced'":
                model = LogisticRegression(
                    max_iter=1000, class_weight="balanced", random_state=RANDOM_STATE
                )
                model.fit(X_tr, y_train)
            elif name == "Không xử lý":
                model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
                model.fit(X_tr, y_train)
            else:
                X_res, y_res = apply_smote(X_tr, y_train, random_state=RANDOM_STATE)
                model = LogisticRegression(max_iter=1000, random_state=RANDOM_STATE)
                model.fit(X_res, y_res)
            balance_records[name].append(score(y_valid, model.predict(X_va)))
        print(f"  fold {fold}/5 xong")

    columns = ["config", "macro_f1", "neutral_f1", "negative_recall", "negative_f1", "accuracy"]

    vector_results = summarise(vector_records, vector_names)
    vector_results.to_csv(REPORTS_DIR / "tv2_vectorizer_comparison.csv", index=False)
    print("\n===== 2. TF-IDF SO VỚI BAG-OF-WORDS =====")
    print(vector_results[columns].round(4).to_string(index=False))

    balance_results = summarise(balance_records, balance_names)
    balance_results.to_csv(REPORTS_DIR / "tv2_balancing_comparison.csv", index=False)
    print("\n===== 3. CHIẾN LƯỢC CÂN BẰNG LỚP =====")
    print(balance_results[columns].round(4).to_string(index=False))

    base = pd.DataFrame(vector_records["TF-IDF (sublinear)"])["macro_f1"]
    bow = pd.DataFrame(vector_records["Bag-of-Words"])["macro_f1"]
    delta = bow - base
    print(f"\nBag-of-Words so với TF-IDF: {delta.mean():+.4f} Macro F1, "
          f"thắng {int((delta > 0).sum())}/5 fold")

    weighted = pd.DataFrame(balance_records["class_weight='balanced'"])["macro_f1"]
    smote = pd.DataFrame(balance_records["SMOTE (không trọng số lớp)"])["macro_f1"]
    delta = smote - weighted
    print(f"SMOTE so với class_weight: {delta.mean():+.4f} Macro F1, "
          f"thắng {int((delta > 0).sum())}/5 fold")


if __name__ == "__main__":
    main()
