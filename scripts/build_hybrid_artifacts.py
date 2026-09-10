"""Dựng artifact hybrid TF-IDF + điểm khía cạnh (TV2 bàn giao cho TV3).

Giữ nguyên artifact text-only đang dùng cho Web Demo; mọi file mới đều có
tiền tố `hybrid_`. Split và seed trùng khớp text-only để TV3 so sánh trực tiếp.
"""

import hashlib
import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from src.features import (  # noqa: E402
    ASPECT_RATING_FEATURES,
    LEXICON_FEATURES,
    STRUCTURED_FEATURES,
    FeatureExtractor,
    deduplicate_modeling_rows,
    prepare_feature_split,
    save_feature_split,
)

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


def main() -> None:
    data = pd.read_excel(SOURCE)
    modeling_df, audit = deduplicate_modeling_rows(data)

    extractor = FeatureExtractor(
        method="tfidf",
        max_features=MAX_FEATURES,
        ngram_range=NGRAM_RANGE,
        min_df=MIN_DF,
        numeric_features=STRUCTURED_FEATURES,
    )
    split = prepare_feature_split(
        modeling_df,
        extractor=extractor,
        text_column="clean_advance_text",
        label_column="sentiment",
        numeric_columns=STRUCTURED_FEATURES,
        test_size=0.2,
        random_state=RANDOM_STATE,
    )

    print(f"X_train: {split.X_train.shape} | X_test: {split.X_test.shape}")
    print(f"Cột số cuối ma trận: {list(extractor.get_feature_names_out()[-10:])}")

    extractor_path = MODELS_DIR / "hybrid_feature_extractor.joblib"
    split_path = MODELS_DIR / "hybrid_train_test_features.joblib"
    extractor.save_bundle(extractor_path)
    save_feature_split(
        split,
        split_path,
        extractor,
        metadata={
            "feature_mode": "text_plus_structured",
            "lexicon_columns": list(LEXICON_FEATURES),
            "aspect_columns": list(ASPECT_RATING_FEATURES),
        },
    )

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
        "feature_contract": {
            "feature_mode": "text_plus_structured",
            "text_column": "clean_advance_text",
            "label_column": "sentiment",
            "numeric_columns": list(STRUCTURED_FEATURES),
            "numeric_scaler": "MinMaxScaler(0,1) fit trên train",
            "split_seed": RANDOM_STATE,
            "test_size": 0.2,
            "ngram_range": list(NGRAM_RANGE),
            "max_features": MAX_FEATURES,
            "min_df": MIN_DF,
            "duplicate_audit": audit,
            "inference_requirement": (
                "Cần đủ 5 điểm khía cạnh 1-5 lúc dự đoán (lexicon thì tính "
                "được từ text). Web Demo text-only không có điểm khía cạnh nên "
                "phải dùng artifact text-only."
            ),
        },
        "artifacts": {
            path.name: {"sha256": sha256_of(path), "bytes": path.stat().st_size}
            for path in (extractor_path, split_path)
        },
    }
    manifest_path = MODELS_DIR / "hybrid_artifact_manifest.json"
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    print(f"Đã lưu manifest tại: {manifest_path}")


if __name__ == "__main__":
    main()
