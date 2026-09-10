import json
from pathlib import Path
import subprocess
import sys

import pandas as pd
import numpy as np
import pytest

from src.app_services import (
    apply_negative_threshold,
    REVIEWS_PATH,
    company_summary,
    get_model_status,
    load_reviews,
    sentiment_summary,
    top_terms,
    predict_review,
)


def test_negative_threshold_overrides_only_scores_at_or_above_policy():
    labels = ["Neutral", "Positive", "Negative"]
    probabilities = np.array(
        [
            [0.30, 0.40, 0.30],
            [0.29, 0.10, 0.61],
            [0.52, 0.20, 0.28],
        ]
    )

    adjusted = apply_negative_threshold(
        labels,
        probabilities,
        classes=["Negative", "Neutral", "Positive"],
    )

    assert adjusted.tolist() == ["Negative", "Positive", "Negative"]


def test_negative_threshold_rejects_invalid_probability_contract():
    with pytest.raises(ValueError, match="Negative"):
        apply_negative_threshold(
            ["Positive"],
            np.array([[0.4, 0.6]]),
            classes=["Neutral", "Positive"],
        )


def test_predict_review_applies_negative_policy_and_reports_policy_confidence():
    class FakePreprocessor:
        @staticmethod
        def clean_advance_text(text):
            return text.strip().lower()

    class FakeExtractor:
        @staticmethod
        def transform(texts):
            assert texts == ["review hỗn hợp"]
            return np.ones((1, 2))

    class FakeModel:
        n_features_in_ = 2
        classes_ = np.array(["Negative", "Neutral", "Positive"])

        @staticmethod
        def predict(features):
            return np.array(["Positive"])

        @staticmethod
        def predict_proba(features):
            return np.array([[0.30, 0.10, 0.60]])

    result = predict_review(
        "Review hỗn hợp", FakeModel(), FakeExtractor(), FakePreprocessor()
    )

    assert result.label == "Negative"
    assert result.confidence == pytest.approx(0.30)
    assert result.negative_probability == pytest.approx(0.30)
    assert result.threshold_applied
    assert result.baseline_label == "Positive"
    assert dict(result.class_probabilities) == {"Negative": 0.30, "Neutral": 0.10, "Positive": 0.60}
    assert result.feature_count == 2
    assert result.active_features == 2


def test_prediction_diagnostics_use_fitted_tfidf_weights():
    from sklearn.feature_extraction.text import TfidfVectorizer

    class Preprocessor:
        def clean_advance_text(self, text):
            return text

    class Extractor:
        vectorizer = TfidfVectorizer().fit(["good team work", "poor management work"])

        def transform(self, texts):
            return self.vectorizer.transform(texts)

    class Model:
        classes_ = np.array(["Positive", "Negative", "Neutral"])

        def predict(self, features):
            return ["Positive"]

        def predict_proba(self, features):
            return [[0.7, 0.2, 0.1]]

    extractor = Extractor()
    result = predict_review("good team", Model(), extractor, Preprocessor())
    vector = extractor.transform(["good team"])
    names = extractor.vectorizer.get_feature_names_out()
    expected = {str(names[i]): float(v) for i, v in zip(vector.indices, vector.data)}
    assert dict(result.top_features) == expected
    assert result.active_features == vector.count_nonzero()
    assert result.negative_probability == pytest.approx(0.2)
    assert not result.threshold_applied


def test_predict_review_hybrid_on_complex_negation():
    """Complex negation remains covered by the merged Hybrid decision path."""
    from src.app_services import load_inference_bundle
    from src.preprocessing import TextPreprocessor

    status = get_model_status()
    if not status.ready:
        pytest.skip("Model chưa sẵn sàng để test.")

    model, extractor = load_inference_bundle(status)
    result = predict_review(
        "Môi trường làm việc không được thân thiện, đồng nghiệp không hỗ trợ và ít cơ hội học hỏi.",
        model,
        extractor,
        TextPreprocessor(),
    )

    assert result.label == "Negative"
    assert result.confidence is not None and result.confidence >= 0.5
    assert result.decision_type in {"ml", "threshold", "hybrid"}
    assert result.probabilities is not None
    assert result.probabilities["Negative"] > result.probabilities["Positive"]


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def sample_reviews() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Company Name": ["Alpha", "Alpha", "Alpha", "Beta"],
            "Rating": [5, 4, 1, 3],
            "sentiment": ["Positive", "Positive", "Negative", "Neutral"],
            "clean_advance_text": [
                "môi_trường tốt",
                "phúc_lợi tốt",
                "quản_lý tệ",
                "bình_thường",
            ],
        }
    )


def test_sentiment_summary_keeps_all_three_classes():
    summary = sentiment_summary(sample_reviews().iloc[:2])

    assert summary["sentiment"].tolist() == ["Positive", "Neutral", "Negative"]
    assert summary["reviews"].tolist() == [2, 0, 0]
    assert summary["share"].tolist() == [100.0, 0.0, 0.0]


def test_dashboard_uses_fast_csv_source_with_normalized_newlines():
    reviews = load_reviews()

    assert REVIEWS_PATH.suffix == ".csv"
    assert len(reviews) == 8_417
    assert set(reviews.columns).issuperset(
        {"Company Name", "Rating", "clean_advance_text", "sentiment"}
    )
    assert not reviews["What I liked"].dropna().str.contains("\r\n", regex=False).any()


def test_company_summary_applies_sample_threshold_and_percentages():
    result = company_summary(sample_reviews(), min_reviews=2)

    assert result["Company Name"].tolist() == ["Alpha"]
    assert result.loc[0, "reviews"] == 3
    assert result.loc[0, "positive_share"] == pytest.approx(200 / 3)
    assert result.loc[0, "negative_share"] == pytest.approx(100 / 3)


def test_top_terms_counts_preprocessed_tokens():
    terms = top_terms(["môi_trường tốt", "phúc_lợi tốt"], limit=2)

    assert terms.to_dict("records") == [
        {"term": "tốt", "count": 2},
        {"term": "môi_trường", "count": 1},
    ]


def test_model_status_fails_closed_when_model_is_missing(tmp_path):
    models = tmp_path / "models"
    models.mkdir()
    (models / "text_feature_extractor.joblib").write_bytes(b"placeholder")
    (models / "artifact_manifest.json").write_text(
        json.dumps({"feature_contract": {"feature_mode": "text_only"}}),
        encoding="utf-8",
    )

    status = get_model_status(tmp_path)

    assert not status.ready
    assert status.model_path is None
    assert "TV3" in status.message


def test_dashboard_services_do_not_eagerly_import_nlp_stack():
    script = """
import sys
import src.app_services

assert "src.features" not in sys.modules
assert "src.preprocessing" not in sys.modules
assert "underthesea" not in sys.modules

import src.preprocessing
assert "underthesea" not in sys.modules
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )

    assert result.returncode == 0, result.stderr
