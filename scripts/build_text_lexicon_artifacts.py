"""Xây dựng artifact Text + Lexicon (Hướng 2) — 5.005 chiều.

Pipeline:
    TF-IDF (5.000 chiều) || MinMaxScaler(5 Lexicon Features) -> 5.005 chiều
    -> Stacking Classifier (NB + LR + SVM) -> best_text_lexicon_model.joblib

Nguyen tac:
  - Khong sua artifact text-only dang dung cho Web Demo mac dinh.
  - Split va seed (2026) giong het text-only de ket qua so sanh truc tiep duoc.
  - Khong dung Aspect Ratings (5 cot) de tranh data shortcut khi deploy.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

# Fix UnicodeEncodeError tren Windows console (cp1252 khong encode duoc tieng Viet)
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.features import (  # noqa: E402
    LEXICON_FEATURES,
    FeatureExtractor,
    deduplicate_modeling_rows,
    prepare_feature_split,
    save_feature_split,
)
from src.models import SentimentModelTrainer  # noqa: E402
from src.preprocessing import TextPreprocessor  # noqa: E402

SOURCE = PROJECT_ROOT / "data" / "processed" / "reviews_cleaned.xlsx"
MODELS_DIR = PROJECT_ROOT / "models"
RANDOM_STATE = 2026
NGRAM_RANGE = (1, 2)
MAX_FEATURES = 5000
MIN_DF = 2


def sha256_of(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args], cwd=PROJECT_ROOT, capture_output=True, text=True
    ).stdout.strip()


def build_lexicon_columns(data: pd.DataFrame) -> pd.DataFrame:
    """Dam bao 5 cot Lexicon ton tai trong DataFrame.

    reviews_cleaned.xlsx da co san cac cot pos_w, neg_w, pos_e, neg_e, sentiment_ratio
    (tinh boi pipeline tien xu ly). Chi tinh lai neu co cot nao bi thieu.
    """
    from src.features import LEXICON_FEATURES  # noqa: PLC0415

    missing = [col for col in LEXICON_FEATURES if col not in data.columns]
    if not missing:
        print(f"  Cac cot Lexicon da co san: {list(LEXICON_FEATURES)}")
        return data.copy()

    print(f"  Tinh {len(missing)} cot Lexicon con thieu: {missing}")
    preprocessor = TextPreprocessor()
    raw_col = "clean_basic_text" if "clean_basic_text" in data.columns else "clean_advance_text"
    records = []
    for text in data[raw_col].fillna(""):
        feats = preprocessor.calc_sentiment_features(text)
        records.append({col: feats.get(col, 0.0) for col in missing})
    lex_df = pd.DataFrame(records, index=data.index)
    return pd.concat([data, lex_df], axis=1)


def main() -> None:
    print("=" * 60)
    print("Xây dựng artifact Text + Lexicon (Hướng 2 — 5.005 chiều)")
    print("=" * 60)

    # 1. Tải và làm sạch dữ liệu
    print(f"\nĐọc dữ liệu từ: {SOURCE}")
    data = pd.read_excel(SOURCE)
    modeling_df, audit = deduplicate_modeling_rows(data)
    print(f"  Nguồn: {len(data)} hàng → Mô hình: {len(modeling_df)} hàng (audit: {audit})")

    # 2. Tính 5 đặc trưng Lexicon và ghép vào DataFrame
    modeling_df = build_lexicon_columns(modeling_df)
    missing_lex = [col for col in LEXICON_FEATURES if col not in modeling_df.columns]
    if missing_lex:
        raise RuntimeError(f"Thiếu cột Lexicon sau khi tính: {missing_lex}")
    print(f"  Đặc trưng Lexicon đã tính: {list(LEXICON_FEATURES)}")

    # 3. Tạo FeatureExtractor với 5 đặc trưng Lexicon (5.005 chiều tổng)
    extractor = FeatureExtractor(
        method="tfidf",
        max_features=MAX_FEATURES,
        ngram_range=NGRAM_RANGE,
        min_df=MIN_DF,
        numeric_features=LEXICON_FEATURES,  # CHỈ Lexicon, không có Aspect Ratings
    )

    # 4. Chia train/test và trích xuất đặc trưng
    print("\nChia train/test (80/20, seed=2026, stratified)...")
    split = prepare_feature_split(
        modeling_df,
        extractor=extractor,
        text_column="clean_advance_text",
        label_column="sentiment",
        numeric_columns=LEXICON_FEATURES,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )
    print(f"  X_train: {split.X_train.shape} | X_test: {split.X_test.shape}")
    print(f"  5 cột cuối: {list(extractor.get_feature_names_out()[-5:])}")

    # 5. Lưu artifact feature split và extractor
    extractor_path = MODELS_DIR / "text_lexicon_feature_extractor.joblib"
    split_path = MODELS_DIR / "text_lexicon_train_test_features.joblib"

    extractor.save_bundle(extractor_path)
    save_feature_split(
        split,
        split_path,
        extractor,
        metadata={
            "feature_mode": "text_plus_lexicon",
            "lexicon_columns": list(LEXICON_FEATURES),
            "note": "Không dùng Aspect Ratings để tránh data shortcut khi deploy.",
        },
    )

    # 6. Huấn luyện Stacking Classifier
    print("\nHuấn luyện Stacking Classifier (NB + LR + SVM)...")
    trainer = SentimentModelTrainer()

    # Tune siêu tham số trên tập train (5-fold CV)
    print("  Bước 6a: GridSearchCV tune siêu tham số (có thể mất vài phút)...")
    tuning_df = trainer.tune_hyperparameters(
        split.X_train, split.y_train, cv=5, scoring="f1_macro", n_jobs=-1
    )
    print(tuning_df[["Model", "CV Macro F1 Mean"]].to_string(index=False))

    # Xây Stacking từ các mô hình đã tune
    print("  Bước 6b: Huấn luyện Stacking Classifier...")
    stacking = trainer.get_stacking_model(base_estimators=trainer.trained_models, cv=5)
    stacking.fit(split.X_train, split.y_train)

    # Đánh giá sơ bộ trên test
    from sklearn.metrics import classification_report, f1_score  # noqa: PLC0415

    y_pred = stacking.predict(split.X_test)
    macro_f1 = f1_score(split.y_test, y_pred, average="macro")
    print(f"\n  [Text + Lexicon] Final Test Macro F1: {macro_f1:.4f}")
    print(classification_report(split.y_test, y_pred))

    # 7. Lưu model
    import joblib  # noqa: PLC0415

    model_path = MODELS_DIR / "best_text_lexicon_model.joblib"
    MODELS_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(stacking, model_path)
    print(f"\nĐã lưu model tại: {model_path}")

    # 8. Viết manifest
    manifest = {
        "schema_version": 1,
        "git_sha": git("rev-parse", "HEAD"),
        "git_branch": git("rev-parse", "--abbrev-ref", "HEAD"),
        "data_file": "data/processed/reviews_cleaned.xlsx",
        "data_sha256": sha256_of(SOURCE),
        "source_rows": int(len(data)),
        "modeling_rows": int(len(modeling_df)),
        "train_rows": int(split.X_train.shape[0]),
        "test_rows": int(split.X_test.shape[0]),
        "feature_count": int(split.X_train.shape[1]),
        "final_test_macro_f1": round(float(macro_f1), 4),
        "feature_contract": {
            "feature_mode": "text_plus_lexicon",
            "text_column": "clean_advance_text",
            "label_column": "sentiment",
            "numeric_columns": list(LEXICON_FEATURES),
            "numeric_scaler": "MinMaxScaler(0,1) fit trên train",
            "split_seed": RANDOM_STATE,
            "test_size": 0.2,
            "ngram_range": list(NGRAM_RANGE),
            "max_features": MAX_FEATURES,
            "min_df": MIN_DF,
            "aspect_ratings_excluded": True,
            "reason": "Aspect Ratings không có tại inference → data shortcut nếu đưa vào.",
            "duplicate_audit": audit,
        },
        "artifacts": {
            path.name: {"sha256": sha256_of(path), "bytes": path.stat().st_size}
            for path in (extractor_path, split_path, model_path)
        },
    }
    manifest_path = MODELS_DIR / "text_lexicon_artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Đã lưu manifest tại: {manifest_path}")
    print("\n✅ Hoàn thành! Artifact Hướng 2 (5.005 chiều) đã sẵn sàng.")


if __name__ == "__main__":
    main()
