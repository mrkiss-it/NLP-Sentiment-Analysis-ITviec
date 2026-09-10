import hashlib
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.linear_model import LogisticRegression

from src.features import (
    ASPECT_RATING_FEATURES,
    LEXICON_FEATURES,
    FeatureExtractor,
    apply_smote,
    deduplicate_modeling_rows,
    load_feature_split,
    prepare_feature_split,
    save_feature_split,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODELS_DIR = PROJECT_ROOT / "models"


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sample_reviews() -> pd.DataFrame:
    rows = []
    labels = ["Positive"] * 10 + ["Neutral"] * 6 + ["Negative"] * 4
    for index, label in enumerate(labels):
        tone = {
            "Positive": "môi_trường tốt phúc_lợi tốt",
            "Neutral": "môi_trường bình_thường",
            "Negative": "quản_lý tệ áp_lực cao",
        }[label]
        rows.append(
            {
                "clean_advance_text": f"{tone} mẫu_{index}",
                "pos_w": 2 if label == "Positive" else 0,
                "neg_w": 2 if label == "Negative" else 0,
                "sentiment_ratio": {
                    "Positive": 1.0,
                    "Neutral": 0.0,
                    "Negative": -1.0,
                }[label],
                "Salary & benefits": 5 if label == "Positive" else 3,
                "sentiment": label,
            }
        )
    return pd.DataFrame(rows)


def test_hybrid_features_combine_text_and_scaled_numeric_columns():
    data = sample_reviews()
    extractor = FeatureExtractor(
        max_features=100,
        min_df=1,
        numeric_features=("pos_w", "neg_w", "sentiment_ratio"),
    )

    matrix = extractor.fit_transform_hybrid(data)

    assert sparse.issparse(matrix)
    assert matrix.shape[0] == len(data)
    assert matrix.shape[1] == len(extractor.get_feature_names_out())
    numeric = matrix[:, -3:].toarray()
    assert np.all(numeric >= 0.0)
    assert np.all(numeric <= 1.0)
    assert extractor.get_feature_names_out()[-3:].tolist() == [
        "num__pos_w",
        "num__neg_w",
        "num__sentiment_ratio",
    ]


def test_default_extractor_is_text_only_for_deployable_nlp_contract():
    data = sample_reviews()
    extractor = FeatureExtractor(max_features=100, min_df=1)

    matrix = extractor.fit_transform_hybrid(data)

    assert extractor.numeric_features == ()
    assert matrix.shape[1] == len(extractor.vectorizer.get_feature_names_out())
    assert not any(name.startswith("num__") for name in extractor.get_feature_names_out())
    assert set(LEXICON_FEATURES).isdisjoint(ASPECT_RATING_FEATURES)


def test_prepare_feature_split_is_stratified_and_fits_on_train_only():
    data = sample_reviews()
    extractor = FeatureExtractor(max_features=100, min_df=1)

    split = prepare_feature_split(
        data,
        extractor=extractor,
        numeric_columns=("pos_w", "neg_w", "sentiment_ratio"),
        random_state=42,
    )

    assert split.X_train.shape[0] == 16
    assert split.X_test.shape[0] == 4
    assert split.y_train.value_counts().to_dict() == {
        "Positive": 8,
        "Neutral": 5,
        "Negative": 3,
    }
    assert split.y_test.value_counts().to_dict() == {
        "Positive": 2,
        "Neutral": 1,
        "Negative": 1,
    }
    held_out_tokens = {
        f"mẫu_{index}" for index in split.test_indices
    }
    assert held_out_tokens.isdisjoint(extractor.vectorizer.vocabulary_)


def test_bundle_round_trip_preserves_hybrid_transform(tmp_path):
    data = sample_reviews()
    extractor = FeatureExtractor(
        max_features=100,
        min_df=1,
        numeric_features=("pos_w", "neg_w", "sentiment_ratio"),
    )
    expected = extractor.fit_transform_hybrid(data)
    bundle_path = tmp_path / "feature_extractor.joblib"

    extractor.save_bundle(bundle_path)
    loaded = FeatureExtractor.load_bundle(bundle_path)
    actual = loaded.transform_hybrid(data)

    np.testing.assert_allclose(actual.toarray(), expected.toarray())


def test_vectorizer_only_load_has_an_explicit_api(tmp_path):
    data = sample_reviews()
    extractor = FeatureExtractor(max_features=100, min_df=1)
    expected = extractor.fit_transform(data["clean_advance_text"])
    path = tmp_path / "tfidf_vectorizer.joblib"
    extractor.save_vectorizer(path)

    loaded = FeatureExtractor.load_vectorizer(path)
    actual = loaded.transform(data["clean_advance_text"])

    np.testing.assert_allclose(actual.toarray(), expected.toarray())


def test_smote_balances_only_the_training_matrix():
    data = sample_reviews()
    extractor = FeatureExtractor(max_features=100, min_df=1)
    split = prepare_feature_split(
        data,
        extractor=extractor,
        numeric_columns=("pos_w", "neg_w", "sentiment_ratio"),
        random_state=42,
    )

    X_resampled, y_resampled = apply_smote(
        split.X_train,
        split.y_train,
        random_state=42,
        k_neighbors=2,
    )

    assert sparse.issparse(X_resampled)
    assert pd.Series(y_resampled).value_counts().nunique() == 1
    assert split.X_test.shape[0] == 4


def test_duplicate_resolution_drops_conflicts_and_keeps_one_same_label_row():
    data = sample_reviews().iloc[:6].copy()
    duplicate = data.iloc[[0]].copy()
    same_label = pd.concat([data, duplicate], ignore_index=True)
    conflict = duplicate.assign(sentiment="Negative")
    with_conflict = pd.concat([same_label, conflict], ignore_index=True)

    cleaned, audit = deduplicate_modeling_rows(with_conflict)

    assert audit == {
        "input_rows": 8,
        "output_rows": 5,
        "duplicate_rows_removed": 3,
        "conflicting_groups_removed": 1,
    }
    assert cleaned["clean_advance_text"].is_unique


def test_saved_split_contains_feature_contract_and_load_validates_width(tmp_path):
    data = sample_reviews()
    extractor = FeatureExtractor(max_features=100, min_df=1)
    split = prepare_feature_split(data, extractor=extractor, random_state=2026)
    path = tmp_path / "text_features.joblib"

    save_feature_split(
        split,
        path,
        extractor=extractor,
        metadata={"split_seed": 2026, "feature_mode": "text_only"},
    )
    artifact = load_feature_split(path)

    assert artifact["schema_version"] == 2
    assert artifact["metadata"]["feature_mode"] == "text_only"
    assert artifact["feature_names"].shape[0] == artifact["X_train"].shape[1]
    assert artifact["X_train"].shape[1] == artifact["X_test"].shape[1]


def test_artifacts_have_a_text_only_contract_and_matching_checksums():
    manifest = json.loads(
        (MODELS_DIR / "artifact_manifest.json").read_text(encoding="utf-8")
    )
    artifact = load_feature_split(MODELS_DIR / "train_test_features.joblib")

    assert artifact["metadata"]["feature_mode"] == "text_only"
    assert artifact["metadata"]["final_test_policy"] == (
        "locked_not_evaluated_by_tv2"
    )
    assert manifest["feature_count"] == artifact["X_train"].shape[1]
    assert manifest["feature_count"] == artifact["X_test"].shape[1]
    for filename, contract in manifest["artifacts"].items():
        assert sha256_file(MODELS_DIR / filename) == contract["sha256"]


def test_model_can_train_and_predict_with_the_text_feature_width():
    artifact = load_feature_split(MODELS_DIR / "train_test_features.joblib")
    train_rows = artifact["train_indices"][:1200]
    source = pd.read_excel(
        PROJECT_ROOT / "data" / "processed" / "reviews_cleaned.xlsx"
    )
    extractor = FeatureExtractor.load_bundle(
        MODELS_DIR / "text_feature_extractor.joblib"
    )
    transformed = extractor.transform(source.loc[train_rows, "clean_advance_text"])
    expected = artifact["X_train"][:1200]

    assert transformed.shape is not None
    assert transformed.shape[1] == expected.shape[1]
    model = LogisticRegression(max_iter=500, class_weight="balanced", random_state=2026)
    model.fit(expected, artifact["y_train"].iloc[:1200])
    prediction = model.predict(transformed[:10])
    assert len(prediction) == 10


def test_modeling_notebook_consumes_artifact_without_refitting_tfidf():
    notebook = json.loads(
        (PROJECT_ROOT / "notebooks" / "03_sentiment_modeling_ml.ipynb").read_text(
            encoding="utf-8"
        )
    )
    source = "\n".join(
        "".join(cell.get("source", [])) for cell in notebook["cells"]
    )

    assert "train_test_features.joblib" in source
    assert "load_feature_split" in source
    assert "processed_text" not in source
    assert "fit_transform" not in source
    assert "tfidf_vectorizer.joblib" not in source
