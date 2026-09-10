"""Shared data and inference helpers for the Streamlit demo."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Iterable

import numpy as np
import pandas as pd

if TYPE_CHECKING:
    from src.features import FeatureExtractor
    from src.preprocessing import TextPreprocessor


PROJECT_ROOT = Path(__file__).resolve().parents[1]
REVIEWS_PATH = PROJECT_ROOT / "data" / "processed" / "reviews_cleaned.csv"
MANIFEST_PATH = PROJECT_ROOT / "models" / "artifact_manifest.json"
EXTRACTOR_PATH = PROJECT_ROOT / "models" / "text_feature_extractor.joblib"
MODEL_CANDIDATES = (
    PROJECT_ROOT / "models" / "best_sentiment_model.joblib",
    PROJECT_ROOT / "models" / "best_text_sentiment_model.joblib",
)

SENTIMENT_ORDER = ("Positive", "Neutral", "Negative")
NEGATIVE_THRESHOLD = 0.30
SENTIMENT_LABELS = {
    "Positive": "Tích cực",
    "Neutral": "Trung tính",
    "Negative": "Tiêu cực",
}

REQUIRED_REVIEW_COLUMNS = {
    "Company Name",
    "Rating",
    "clean_advance_text",
    "sentiment",
}

DASHBOARD_REVIEW_COLUMNS = (
    "Company Name",
    "Rating",
    "clean_advance_text",
    "sentiment",
    "Cmt_day",
    "Title",
    "What I liked",
    "Suggestions for improvement",
)


@dataclass(frozen=True)
class ModelStatus:
    """Readiness state of the deployable text-only inference pipeline."""

    ready: bool
    model_path: Path | None
    extractor_path: Path
    message: str


@dataclass(frozen=True)
class PredictionResult:
    """A model prediction with optional model probability and policy metadata."""

    label: str
    processed_text: str
    confidence: float | None
    negative_probability: float | None = None
    threshold_applied: bool = False
    baseline_label: str | None = None
    class_probabilities: tuple[tuple[str, float], ...] = ()
    feature_count: int = 0
    active_features: int = 0
    top_features: tuple[tuple[str, float], ...] = ()


def apply_negative_threshold(
    baseline_labels: Iterable[str],
    probabilities: np.ndarray,
    classes: Iterable[str],
    threshold: float = NEGATIVE_THRESHOLD,
) -> np.ndarray:
    """Override predictions when Negative probability reaches the policy threshold."""
    if not 0.0 <= threshold <= 1.0:
        raise ValueError("Ngưỡng Negative phải nằm trong đoạn [0, 1].")

    labels = np.asarray(list(baseline_labels), dtype=object)
    scores = np.asarray(probabilities)
    class_names = [str(value) for value in classes]
    if scores.ndim != 2 or scores.shape[0] != labels.shape[0]:
        raise ValueError("Ma trận xác suất không khớp với số lượng dự đoán.")
    if "Negative" not in class_names or scores.shape[1] != len(class_names):
        raise ValueError("Model không cung cấp xác suất hợp lệ cho lớp Negative.")

    negative_index = class_names.index("Negative")
    labels[scores[:, negative_index] >= threshold] = "Negative"
    return labels.astype(str)


def load_reviews(path: str | Path = REVIEWS_PATH) -> pd.DataFrame:
    """Load and validate the cleaned review dataset used by the dashboard."""
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu sạch: {source}")

    usecols = list(DASHBOARD_REVIEW_COLUMNS) if source == REVIEWS_PATH else None
    if source.suffix.lower() == ".csv":
        reviews = pd.read_csv(source, usecols=usecols)
        text_columns = reviews.select_dtypes(include=["object", "string"]).columns
        reviews[text_columns] = reviews[text_columns].apply(
            lambda values: values.str.replace("\r\n", "\n", regex=False)
        )
    else:
        reviews = pd.read_excel(source, usecols=usecols)
    missing = REQUIRED_REVIEW_COLUMNS.difference(reviews.columns)
    if missing:
        raise ValueError("Dữ liệu thiếu cột bắt buộc: " + ", ".join(sorted(missing)))

    reviews = reviews.copy()
    reviews["Company Name"] = (
        reviews["Company Name"].fillna("Không xác định").astype(str).str.strip()
    )
    reviews["sentiment"] = reviews["sentiment"].astype(str).str.strip()
    reviews["Rating"] = pd.to_numeric(reviews["Rating"], errors="coerce")
    if "Cmt_day" in reviews.columns:
        reviews["review_month"] = pd.to_datetime(
            reviews["Cmt_day"], format="%B %Y", errors="coerce"
        )
    else:
        reviews["review_month"] = pd.NaT
    return reviews


def sentiment_summary(reviews: pd.DataFrame) -> pd.DataFrame:
    """Return stable three-class counts and shares for a review slice."""
    counts = reviews["sentiment"].value_counts().reindex(SENTIMENT_ORDER, fill_value=0)
    total = int(counts.sum())
    shares = counts.div(total).mul(100) if total else counts.astype(float)
    return pd.DataFrame(
        {
            "sentiment": counts.index,
            "label": [SENTIMENT_LABELS[label] for label in counts.index],
            "reviews": counts.to_numpy(dtype=int),
            "share": shares.to_numpy(dtype=float),
        }
    )


def company_summary(reviews: pd.DataFrame, min_reviews: int = 30) -> pd.DataFrame:
    """Aggregate sentiment and rating metrics for sufficiently sampled companies."""
    grouped = reviews.groupby("Company Name", dropna=False)
    totals = grouped.size().rename("reviews")
    average_rating = grouped["Rating"].mean().rename("average_rating")
    counts = pd.crosstab(reviews["Company Name"], reviews["sentiment"]).reindex(
        columns=SENTIMENT_ORDER, fill_value=0
    )
    result = pd.concat([totals, average_rating, counts], axis=1).reset_index()

    for sentiment in SENTIMENT_ORDER:
        result[f"{sentiment.lower()}_share"] = (
            result[sentiment].div(result["reviews"]).mul(100)
        )

    return (
        result[result["reviews"] >= min_reviews]
        .sort_values(["reviews", "Company Name"], ascending=[False, True])
        .reset_index(drop=True)
    )


def monthly_sentiment(reviews: pd.DataFrame) -> pd.DataFrame:
    """Aggregate sentiment counts by month for trend charts."""
    valid = reviews.dropna(subset=["review_month"])
    if valid.empty:
        return pd.DataFrame(columns=["review_month", "sentiment", "reviews"])
    return (
        valid.groupby(["review_month", "sentiment"], observed=True)
        .size()
        .rename("reviews")
        .reset_index()
        .sort_values("review_month")
    )


def top_terms(texts: Iterable[str], limit: int = 15) -> pd.DataFrame:
    """Count the most frequent pre-tokenized terms in cleaned review text."""
    tokens: list[str] = []
    for text in texts:
        tokens.extend(
            token
            for token in str(text).split()
            if len(token) > 1 and not token.isnumeric()
        )
    return pd.DataFrame(Counter(tokens).most_common(limit), columns=["term", "count"])


def get_model_status(project_root: str | Path = PROJECT_ROOT) -> ModelStatus:
    """Inspect the model handoff without loading untrusted or incomplete artifacts."""
    root = Path(project_root)
    extractor_path = root / "models" / EXTRACTOR_PATH.name
    model_path = next(
        (
            root / "models" / candidate.name
            for candidate in MODEL_CANDIDATES
            if (root / "models" / candidate.name).exists()
        ),
        None,
    )
    manifest_path = root / "models" / MANIFEST_PATH.name

    if not extractor_path.exists():
        return ModelStatus(
            False,
            model_path,
            extractor_path,
            "Thiếu bộ trích xuất đặc trưng text-only.",
        )
    if not manifest_path.exists():
        return ModelStatus(False, model_path, extractor_path, "Thiếu artifact manifest.")

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return ModelStatus(False, model_path, extractor_path, f"Manifest không hợp lệ: {exc}")

    feature_mode = manifest.get("feature_contract", {}).get("feature_mode")
    if feature_mode != "text_only":
        return ModelStatus(
            False,
            model_path,
            extractor_path,
            "Artifact không tuân theo feature contract text-only.",
        )
    if model_path is None:
        return ModelStatus(
            False,
            None,
            extractor_path,
            "Mô hình đang chờ TV3 huấn luyện và bàn giao.",
        )

    return ModelStatus(True, model_path, extractor_path, "Pipeline dự đoán sẵn sàng.")


def load_inference_bundle(status: ModelStatus) -> tuple[Any, FeatureExtractor]:
    """Load model and extractor only after the handoff contract is ready."""
    if not status.ready or status.model_path is None:
        raise RuntimeError(status.message)

    import joblib

    from src.features import FeatureExtractor

    model = joblib.load(status.model_path)
    extractor = FeatureExtractor.load_bundle(status.extractor_path)
    return model, extractor


def predict_review(
    text: str,
    model: Any,
    extractor: FeatureExtractor,
    preprocessor: TextPreprocessor,
) -> PredictionResult:
    """Run the text-only inference path and avoid inventing confidence values."""
    processed = preprocessor.clean_advance_text(text)
    if not processed:
        raise ValueError("Review không còn nội dung hợp lệ sau tiền xử lý.")

    features = extractor.transform([processed])
    expected_width = getattr(model, "n_features_in_", None)
    if expected_width is not None and int(expected_width) != features.shape[1]:
        raise ValueError(
            "Model và feature extractor không cùng số chiều đặc trưng."
        )

    baseline_label = str(model.predict(features)[0])
    label = baseline_label
    confidence: float | None = None
    negative_probability: float | None = None
    threshold_applied = False
    class_probabilities: tuple[tuple[str, float], ...] = ()
    if hasattr(model, "predict_proba"):
        probabilities = np.asarray(model.predict_proba(features))[0]
        classes = [str(value) for value in getattr(model, "classes_", [])]
        class_probabilities = tuple(zip(classes, map(float, probabilities)))
        if "Negative" in classes:
            negative_probability = float(probabilities[classes.index("Negative")])
            label = str(
                apply_negative_threshold(
                    [baseline_label],
                    probabilities.reshape(1, -1),
                    classes,
                )[0]
            )
            threshold_applied = label == "Negative" and baseline_label != "Negative"
        if label in classes:
            confidence = float(probabilities[classes.index(label)])

    # These weights describe the input vector, not causal model attribution.
    vectorizer = getattr(extractor, "vectorizer", None)
    top_features: tuple[tuple[str, float], ...] = ()
    if hasattr(features, "getrow"):
        row = features.getrow(0)
        active_features = int(row.count_nonzero())
        if vectorizer is not None and hasattr(vectorizer, "get_feature_names_out"):
            names = vectorizer.get_feature_names_out()
            order = np.argsort(-row.data, kind="stable")[:10]
            top_features = tuple(
                (str(names[row.indices[i]]), float(row.data[i])) for i in order
            )
    else:
        active_features = int(np.count_nonzero(features))

    return PredictionResult(
        label=label,
        processed_text=processed,
        confidence=confidence,
        negative_probability=negative_probability,
        threshold_applied=threshold_applied,
        baseline_label=baseline_label,
        class_probabilities=class_probabilities,
        feature_count=int(features.shape[1]),
        active_features=active_features,
        top_features=top_features,
    )
