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
    """A model prediction with optional calibrated probability and explainability."""

    label: str
    processed_text: str
    confidence: float | None
    probabilities: dict[str, float] | None = None
    lexicon_stats: dict[str, Any] | None = None
    decision_type: str = "ml"
    explanation: str = ""
    raw_ml_label: str | None = None
    raw_ml_probabilities: dict[str, float] | None = None



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

    # Tương thích ngược: bổ sung multi_class cho LogisticRegression khi unpickle từ scikit-learn mới
    for est in getattr(model, "estimators_", []):
        if hasattr(est, "C") and not hasattr(est, "multi_class"):
            setattr(est, "multi_class", "auto")
    named = getattr(model, "named_estimators_", {})
    if isinstance(named, dict):
        for est in named.values():
            if hasattr(est, "C") and not hasattr(est, "multi_class"):
                setattr(est, "multi_class", "auto")
    final_est = getattr(model, "final_estimator_", None)
    if final_est is not None and hasattr(final_est, "C") and not hasattr(final_est, "multi_class"):
        setattr(final_est, "multi_class", "auto")

    extractor = FeatureExtractor.load_bundle(status.extractor_path)
    return model, extractor



def predict_review(
    text: str,
    model: Any,
    extractor: FeatureExtractor,
    preprocessor: TextPreprocessor,
) -> PredictionResult:
    """Run text-only inference with hybrid lexicon-guided calibration for edge cases."""
    processed = preprocessor.clean_advance_text(text)
    if not processed:
        raise ValueError("Review không còn nội dung hợp lệ sau tiền xử lý.")

    features = extractor.transform([processed])
    expected_width = getattr(model, "n_features_in_", None)
    if expected_width is not None and int(expected_width) != features.shape[1]:
        raise ValueError(
            "Model và feature extractor không cùng số chiều đặc trưng."
        )

    # 1. Dự đoán từ mô hình học máy cơ sở
    raw_label = str(model.predict(features)[0])
    prob_dict: dict[str, float] = {}
    classes = [str(value) for value in getattr(model, "classes_", [])]
    if hasattr(model, "predict_proba"):
        probabilities = np.asarray(model.predict_proba(features))[0]
        prob_dict = {cls: float(p) for cls, p in zip(classes, probabilities)}
    raw_ml_probabilities = dict(prob_dict) if prob_dict else None

    # 2. Trích xuất đặc trưng Lexicon và xử lý phạm vi phủ định (Negation Scope)
    lex_stats = preprocessor.calc_sentiment_features(text, raw_text=text)
    pos_w = lex_stats.get("pos_w", 0)
    neg_w = lex_stats.get("neg_w", 0)
    ratio = lex_stats.get("sentiment_ratio", 0.0)

    # 3. Chiến lược Hybrid Decision:
    # Tập dữ liệu gốc mất cân bằng nặng (Positive 73.8%, Negative chỉ 6.8%),
    # khiến mô hình ML dễ thiên lệch về Neutral/Positive khi gặp câu phủ định ghép.
    final_label = raw_label
    decision_type = "ml"
    explanation = f"Dự đoán dựa trên mô hình học máy ({SENTIMENT_LABELS.get(raw_label, raw_label)})."

    neg_prob = prob_dict.get("Negative", 0.0)
    neu_prob = prob_dict.get("Neutral", 0.0)
    pos_prob = prob_dict.get("Positive", 0.0)

    # Trường hợp A: Tín hiệu tiêu cực từ vựng rất rõ ràng (từ phủ định đi kèm từ tích cực, hoặc nhiều cụm chê)
    if neg_w >= 2 and ratio <= -0.4:
        if raw_label != "Negative":
            final_label = "Negative"
            decision_type = "hybrid"
            phrases_str = ", ".join(f"'{p}'" for p in lex_stats.get("neg_phrases", [])[:3])
            explanation = (
                f"Hiệu chỉnh Hybrid: Phát hiện {neg_w} cụm từ tiêu cực/phủ định ({phrases_str}) "
                f"với tỷ lệ sắc thái {ratio:.2f}, khắc phục độ lệch lớp của mô hình ML."
            )
            if prob_dict:
                prob_dict["Negative"] = max(0.65, neg_prob + 0.35)
                remaining = 1.0 - prob_dict["Negative"]
                tot_other = neu_prob + pos_prob
                if tot_other > 0:
                    prob_dict["Neutral"] = remaining * (neu_prob / tot_other)
                    prob_dict["Positive"] = remaining * (pos_prob / tot_other)
                else:
                    prob_dict["Neutral"] = remaining * 0.5
                    prob_dict["Positive"] = remaining * 0.5
    # Trường hợp B: ML phân vân giữa Neutral và Negative (hoặc Negative bám sát) và Lexicon xác nhận tiêu cực
    elif neg_w > pos_w and ratio <= -0.2 and (raw_label == "Neutral" or (neu_prob > 0 and abs(neu_prob - neg_prob) < 0.15)):
        final_label = "Negative"
        decision_type = "hybrid"
        phrases_str = ", ".join(f"'{p}'" for p in lex_stats.get("neg_phrases", [])[:3])
        explanation = (
            f"Hiệu chỉnh Hybrid: Mô hình ML phân vân vùng ranh giới; từ điển ngữ nghĩa xác nhận "
            f"{neg_w} cụm tiêu cực ({phrases_str})."
        )
        if prob_dict:
            prob_dict["Negative"] = max(0.55, neg_prob + 0.20)
            remaining = 1.0 - prob_dict["Negative"]
            tot_other = neu_prob + pos_prob
            if tot_other > 0:
                prob_dict["Neutral"] = remaining * (neu_prob / tot_other)
                prob_dict["Positive"] = remaining * (pos_prob / tot_other)
    # Trường hợp C: Tín hiệu tích cực áp đảo nhưng ML rơi vào Neutral
    elif pos_w >= 2 and ratio >= 0.5 and raw_label == "Neutral":
        final_label = "Positive"
        decision_type = "hybrid"
        phrases_str = ", ".join(f"'{p}'" for p in lex_stats.get("pos_phrases", [])[:3])
        explanation = (
            f"Hiệu chỉnh Hybrid: Xác nhận {pos_w} cụm từ khen ngợi ({phrases_str}) với tỷ lệ sắc thái +{ratio:.2f}."
        )
        if prob_dict:
            prob_dict["Positive"] = max(0.60, pos_prob + 0.25)
            remaining = 1.0 - prob_dict["Positive"]
            tot_other = neu_prob + neg_prob
            if tot_other > 0:
                prob_dict["Neutral"] = remaining * (neu_prob / tot_other)
                prob_dict["Negative"] = remaining * (neg_prob / tot_other)

    confidence: float | None = prob_dict.get(final_label) if prob_dict else None

    return PredictionResult(
        label=final_label,
        processed_text=processed,
        confidence=confidence,
        probabilities=prob_dict if prob_dict else None,
        lexicon_stats=lex_stats,
        decision_type=decision_type,
        explanation=explanation,
        raw_ml_label=raw_label,
        raw_ml_probabilities=raw_ml_probabilities,
    )


# ── Hướng 2: Text + Lexicon (5.005 chiều) ──────────────────────────────────
# Các hằng số và hàm bổ sung cho pipeline thứ hai song song với text-only.
# Không sửa bất kỳ code phía trên.

LEXICON_MANIFEST_PATH = PROJECT_ROOT / "models" / "text_lexicon_artifact_manifest.json"
LEXICON_EXTRACTOR_PATH = PROJECT_ROOT / "models" / "text_lexicon_feature_extractor.joblib"
LEXICON_MODEL_PATH = PROJECT_ROOT / "models" / "best_text_lexicon_model.joblib"


@dataclass(frozen=True)
class LexiconModelStatus:
    """Readiness state của pipeline Text + Lexicon (Hướng 2 — 5.005 chiều)."""

    ready: bool
    model_path: Path | None
    extractor_path: Path
    message: str


def get_lexicon_model_status(project_root: str | Path = PROJECT_ROOT) -> LexiconModelStatus:
    """Kiểm tra artifact Hướng 2 mà không load dữ liệu không tin cậy."""
    root = Path(project_root)
    extractor_path = root / "models" / LEXICON_EXTRACTOR_PATH.name
    model_path = root / "models" / LEXICON_MODEL_PATH.name
    manifest_path = root / "models" / LEXICON_MANIFEST_PATH.name

    if not extractor_path.exists():
        return LexiconModelStatus(
            False,
            None,
            extractor_path,
            "Thiếu text_lexicon_feature_extractor.joblib. Chạy scripts/build_text_lexicon_artifacts.py.",
        )
    if not manifest_path.exists():
        return LexiconModelStatus(
            False,
            None,
            extractor_path,
            "Thiếu text_lexicon_artifact_manifest.json.",
        )

    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        return LexiconModelStatus(False, None, extractor_path, f"Manifest không hợp lệ: {exc}")

    feature_mode = manifest.get("feature_contract", {}).get("feature_mode")
    if feature_mode != "text_plus_lexicon":
        return LexiconModelStatus(
            False,
            None,
            extractor_path,
            f"Artifact không tuân theo feature contract text_plus_lexicon (thực tế: {feature_mode}).",
        )
    if not model_path.exists():
        return LexiconModelStatus(
            False,
            None,
            extractor_path,
            "Thiếu best_text_lexicon_model.joblib. Chạy scripts/build_text_lexicon_artifacts.py.",
        )

    return LexiconModelStatus(
        True,
        model_path,
        extractor_path,
        "Pipeline Text + Lexicon (5.005 chiều) sẵn sàng.",
    )


def load_lexicon_inference_bundle(
    status: LexiconModelStatus,
) -> "tuple[Any, FeatureExtractor]":
    """Load model và extractor Hướng 2 sau khi kiểm tra handoff contract."""
    if not status.ready or status.model_path is None:
        raise RuntimeError(status.message)

    import joblib

    from src.features import FeatureExtractor

    model = joblib.load(status.model_path)

    # Tương thích ngược: bổ sung multi_class cho LogisticRegression khi unpickle từ scikit-learn mới
    for est in getattr(model, "estimators_", []):
        if hasattr(est, "C") and not hasattr(est, "multi_class"):
            setattr(est, "multi_class", "auto")
    named = getattr(model, "named_estimators_", {})
    if isinstance(named, dict):
        for est in named.values():
            if hasattr(est, "C") and not hasattr(est, "multi_class"):
                setattr(est, "multi_class", "auto")
    final_est = getattr(model, "final_estimator_", None)
    if final_est is not None and hasattr(final_est, "C") and not hasattr(final_est, "multi_class"):
        setattr(final_est, "multi_class", "auto")

    extractor = FeatureExtractor.load_bundle(status.extractor_path)
    return model, extractor


def predict_review_lexicon(
    text: str,
    model: Any,
    extractor: "FeatureExtractor",
    preprocessor: "TextPreprocessor",
) -> PredictionResult:
    """Chạy inference Hướng 2 (Text + Lexicon 5.005 chiều) với Hybrid Decision Gate.

    Điểm khác biệt so với predict_review (text-only):
    - Tính 5 đặc trưng Lexicon từ văn bản gốc rồi ghép vào vector TF-IDF.
    - Dùng extractor.transform_hybrid() thay vì extractor.transform().
    - Logic Hybrid Decision Gate giữ nguyên để tận dụng tín hiệu phủ định từ vựng.
    """
    from src.features import LEXICON_FEATURES  # noqa: PLC0415

    processed = preprocessor.clean_advance_text(text)
    if not processed:
        raise ValueError("Review không còn nội dung hợp lệ sau tiền xử lý.")

    # Tính 5 đặc trưng Lexicon từ văn bản gốc
    lex_stats = preprocessor.calc_sentiment_features(text, raw_text=text)
    lex_values = {col: lex_stats.get(col, 0.0) for col in LEXICON_FEATURES}

    # Xây DataFrame 1 hàng gồm văn bản đã xử lý + 5 cột lexicon
    row_df = pd.DataFrame([{"clean_advance_text": processed, **lex_values}])

    # Trích xuất đặc trưng 5.005 chiều qua transform_hybrid
    features = extractor.transform_hybrid(row_df, text_column="clean_advance_text")
    expected_width = getattr(model, "n_features_in_", None)
    if expected_width is not None and int(expected_width) != features.shape[1]:
        raise ValueError(
            f"Model ({expected_width} chiều) và extractor ({features.shape[1]} chiều) không khớp. "
            "Hãy chạy lại scripts/build_text_lexicon_artifacts.py."
        )

    # 1. Dự đoán từ mô hình học máy cơ sở
    raw_label = str(model.predict(features)[0])
    prob_dict: dict[str, float] = {}
    classes = [str(v) for v in getattr(model, "classes_", [])]
    if hasattr(model, "predict_proba"):
        probabilities = np.asarray(model.predict_proba(features))[0]
        prob_dict = {cls: float(p) for cls, p in zip(classes, probabilities)}
    raw_ml_probabilities = dict(prob_dict) if prob_dict else None

    # 2. Hybrid Decision Gate (đồng bộ logic với predict_review)
    pos_w = lex_stats.get("pos_w", 0)
    neg_w = lex_stats.get("neg_w", 0)
    ratio = lex_stats.get("sentiment_ratio", 0.0)

    final_label = raw_label
    decision_type = "ml"
    explanation = (
        f"Dự đoán dựa trên mô hình Text + Lexicon ({SENTIMENT_LABELS.get(raw_label, raw_label)})."
    )

    neg_prob = prob_dict.get("Negative", 0.0)
    neu_prob = prob_dict.get("Neutral", 0.0)
    pos_prob = prob_dict.get("Positive", 0.0)

    # Trường hợp A: Tín hiệu tiêu cực từ vựng rất rõ ràng
    if neg_w >= 2 and ratio <= -0.4:
        if raw_label != "Negative":
            final_label = "Negative"
            decision_type = "hybrid"
            phrases_str = ", ".join(f"'{p}'" for p in lex_stats.get("neg_phrases", [])[:3])
            explanation = (
                f"Hiệu chỉnh Hybrid: Phát hiện {neg_w} cụm từ tiêu cực/phủ định ({phrases_str}) "
                f"với tỷ lệ sắc thái {ratio:.2f}, khắc phục độ lệch lớp của mô hình ML."
            )
            if prob_dict:
                prob_dict["Negative"] = max(0.65, neg_prob + 0.35)
                remaining = 1.0 - prob_dict["Negative"]
                tot_other = neu_prob + pos_prob
                if tot_other > 0:
                    prob_dict["Neutral"] = remaining * (neu_prob / tot_other)
                    prob_dict["Positive"] = remaining * (pos_prob / tot_other)
                else:
                    prob_dict["Neutral"] = remaining * 0.5
                    prob_dict["Positive"] = remaining * 0.5
    # Trường hợp B: ML phân vân vùng ranh giới
    elif neg_w > pos_w and ratio <= -0.2 and (
        raw_label == "Neutral" or (neu_prob > 0 and abs(neu_prob - neg_prob) < 0.15)
    ):
        final_label = "Negative"
        decision_type = "hybrid"
        phrases_str = ", ".join(f"'{p}'" for p in lex_stats.get("neg_phrases", [])[:3])
        explanation = (
            f"Hiệu chỉnh Hybrid: Mô hình ML phân vân vùng ranh giới; từ điển ngữ nghĩa xác nhận "
            f"{neg_w} cụm tiêu cực ({phrases_str})."
        )
        if prob_dict:
            prob_dict["Negative"] = max(0.55, neg_prob + 0.20)
            remaining = 1.0 - prob_dict["Negative"]
            tot_other = neu_prob + pos_prob
            if tot_other > 0:
                prob_dict["Neutral"] = remaining * (neu_prob / tot_other)
                prob_dict["Positive"] = remaining * (pos_prob / tot_other)
    # Trường hợp C: Tín hiệu tích cực áp đảo nhưng ML rơi vào Neutral
    elif pos_w >= 2 and ratio >= 0.5 and raw_label == "Neutral":
        final_label = "Positive"
        decision_type = "hybrid"
        phrases_str = ", ".join(f"'{p}'" for p in lex_stats.get("pos_phrases", [])[:3])
        explanation = (
            f"Hiệu chỉnh Hybrid: Xác nhận {pos_w} cụm từ khen ngợi ({phrases_str}) "
            f"với tỷ lệ sắc thái +{ratio:.2f}."
        )
        if prob_dict:
            prob_dict["Positive"] = max(0.60, pos_prob + 0.25)
            remaining = 1.0 - prob_dict["Positive"]
            tot_other = neu_prob + neg_prob
            if tot_other > 0:
                prob_dict["Neutral"] = remaining * (neu_prob / tot_other)
                prob_dict["Negative"] = remaining * (neg_prob / tot_other)

    confidence: float | None = prob_dict.get(final_label) if prob_dict else None

    return PredictionResult(
        label=final_label,
        processed_text=processed,
        confidence=confidence,
        probabilities=prob_dict if prob_dict else None,
        lexicon_stats=lex_stats,
        decision_type=decision_type,
        explanation=explanation,
        raw_ml_label=raw_label,
        raw_ml_probabilities=raw_ml_probabilities,
    )
