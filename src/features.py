import os
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence, Tuple

import joblib
import numpy as np
import pandas as pd
from imblearn.over_sampling import SMOTE
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler


LEXICON_FEATURES = (
    "pos_w",
    "neg_w",
    "pos_e",
    "neg_e",
    "sentiment_ratio",
)

ASPECT_RATING_FEATURES = (
    "Salary & benefits",
    "Training & learning",
    "Management cares about me",
    "Culture & fun",
    "Office & workspace",
)

STRUCTURED_FEATURES = LEXICON_FEATURES + ASPECT_RATING_FEATURES

# Text-only is the deployable NLP default. Structured ratings are opt-in diagnostics.
DEFAULT_NUMERIC_FEATURES: tuple[str, ...] = ()


@dataclass(frozen=True)
class FeatureSplit:
    """Các ma trận và nhãn đã chia theo tỷ lệ train/test."""

    X_train: sparse.csr_matrix
    X_test: sparse.csr_matrix
    y_train: pd.Series
    y_test: pd.Series
    train_indices: np.ndarray
    test_indices: np.ndarray


class FeatureExtractor:
    """Vector hóa văn bản và ghép các đặc trưng số đã chuẩn hóa."""

    def __init__(
        self,
        method: str = "tfidf",
        max_features: int = 5000,
        ngram_range: Tuple[int, int] = (1, 2),
        min_df: int = 2,
        numeric_features: Sequence[str] = DEFAULT_NUMERIC_FEATURES,
    ):
        self.method = method
        self.max_features = max_features
        self.ngram_range = ngram_range
        self.min_df = min_df
        self.numeric_features = tuple(numeric_features)
        self.scaler = (
            MinMaxScaler(feature_range=(0, 1)) if self.numeric_features else None
        )

        vectorizer_options = {
            "max_features": max_features,
            "ngram_range": ngram_range,
            "min_df": min_df,
        }
        if method == "tfidf":
            self.vectorizer = TfidfVectorizer(
                **vectorizer_options,
                sublinear_tf=True,
            )
        elif method == "bow":
            self.vectorizer = CountVectorizer(**vectorizer_options)
        else:
            raise ValueError(
                f"Phương thức '{method}' không được hỗ trợ. Dùng 'tfidf' hoặc 'bow'."
            )

    @staticmethod
    def _prepare_corpus(corpus: Iterable[str]) -> pd.Series:
        return pd.Series(corpus, dtype="string").fillna("").astype(str)

    def _prepare_numeric(self, data: pd.DataFrame) -> np.ndarray:
        if not self.numeric_features:
            return np.empty((len(data), 0), dtype=float)
        missing_columns = [
            column for column in self.numeric_features if column not in data.columns
        ]
        if missing_columns:
            raise ValueError(
                "Thiếu cột đặc trưng số: " + ", ".join(missing_columns)
            )
        return (
            data.loc[:, self.numeric_features]
            .apply(pd.to_numeric, errors="coerce")
            .fillna(0.0)
            .to_numpy(dtype=float)
        )

    def fit_transform(self, corpus: Iterable[str]) -> sparse.csr_matrix:
        """Học từ điển trên tập train và vector hóa văn bản."""
        return self.vectorizer.fit_transform(self._prepare_corpus(corpus)).tocsr()

    def transform(self, corpus: Iterable[str]) -> sparse.csr_matrix:
        """Vector hóa văn bản bằng từ điển đã học."""
        return self.vectorizer.transform(self._prepare_corpus(corpus)).tocsr()

    def fit_transform_hybrid(
        self,
        data: pd.DataFrame,
        text_column: str = "clean_advance_text",
        numeric_columns: Sequence[str] | None = None,
    ) -> sparse.csr_matrix:
        """Fit trên tập train rồi ghép TF-IDF với đặc trưng số."""
        if text_column not in data.columns:
            raise ValueError(f"Không tìm thấy cột văn bản '{text_column}'.")
        if numeric_columns is not None:
            self.numeric_features = tuple(numeric_columns)
            self.scaler = (
                MinMaxScaler(feature_range=(0, 1))
                if self.numeric_features
                else None
            )

        text_features = self.fit_transform(data[text_column])
        if not self.numeric_features:
            return text_features
        numeric_values = self._prepare_numeric(data)
        if self.scaler is None:
            raise RuntimeError("Scaler chưa được khởi tạo cho đặc trưng số.")
        numeric_features = sparse.csr_matrix(self.scaler.fit_transform(numeric_values))
        return sparse.hstack([text_features, numeric_features], format="csr")

    def transform_hybrid(
        self,
        data: pd.DataFrame,
        text_column: str = "clean_advance_text",
    ) -> sparse.csr_matrix:
        """Biến đổi dữ liệu mới bằng vectorizer và scaler đã fit."""
        if text_column not in data.columns:
            raise ValueError(f"Không tìm thấy cột văn bản '{text_column}'.")

        text_features = self.transform(data[text_column])
        if not self.numeric_features:
            return text_features
        numeric_values = self._prepare_numeric(data)
        if self.scaler is None:
            raise RuntimeError("Scaler chưa được fit cho đặc trưng số.")
        numeric_features = sparse.csr_matrix(self.scaler.transform(numeric_values))
        return sparse.hstack([text_features, numeric_features], format="csr")

    def get_feature_names_out(self) -> np.ndarray:
        """Trả tên đặc trưng text và số theo đúng thứ tự cột ma trận."""
        text_names = self.vectorizer.get_feature_names_out()
        numeric_names = np.asarray(
            [f"num__{column}" for column in self.numeric_features], dtype=object
        )
        return np.concatenate([text_names, numeric_names])

    def save_vectorizer(self, filepath: str | os.PathLike[str]) -> None:
        """Lưu riêng vectorizer cho pipeline text-only."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.vectorizer, path)
        print(f"Đã lưu vectorizer tại: {path}")

    @classmethod
    def load_vectorizer(cls, filepath: str | os.PathLike[str]):
        """Tải riêng vectorizer vào extractor text-only."""
        instance = cls(numeric_features=())
        instance.vectorizer = joblib.load(filepath)
        return instance

    def save(self, filepath: str | os.PathLike[str]) -> None:
        """Alias tương thích ngược của :meth:`save_vectorizer`."""
        self.save_vectorizer(filepath)

    @classmethod
    def load(cls, filepath: str | os.PathLike[str]):
        """Alias tương thích ngược; chỉ tải vectorizer text-only."""
        return cls.load_vectorizer(filepath)

    def save_bundle(self, filepath: str | os.PathLike[str]) -> None:
        """Lưu cả vectorizer, scaler và cấu hình đặc trưng số."""
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self, path)
        print(f"Đã lưu feature extractor tại: {path}")

    @classmethod
    def load_bundle(cls, filepath: str | os.PathLike[str]):
        """Tải feature extractor đầy đủ đã fit."""
        instance = joblib.load(filepath)
        if not isinstance(instance, cls):
            raise TypeError("File không chứa FeatureExtractor hợp lệ.")
        return instance


def prepare_feature_split(
    data: pd.DataFrame,
    extractor: FeatureExtractor | None = None,
    text_column: str = "clean_advance_text",
    label_column: str = "sentiment",
    numeric_columns: Sequence[str] | None = None,
    test_size: float = 0.2,
    random_state: int = 2026,
) -> FeatureSplit:
    """Chia phân tầng trước khi fit để tránh rò rỉ dữ liệu từ tập test."""
    if label_column not in data.columns:
        raise ValueError(f"Không tìm thấy cột nhãn '{label_column}'.")

    train_indices, test_indices = train_test_split(
        data.index.to_numpy(),
        test_size=test_size,
        random_state=random_state,
        stratify=data[label_column],
    )
    train_data = data.loc[train_indices]
    test_data = data.loc[test_indices]
    resolved_numeric_columns = (
        tuple(numeric_columns)
        if numeric_columns is not None
        else tuple(extractor.numeric_features if extractor else ())
    )
    feature_extractor = extractor or FeatureExtractor(
        numeric_features=resolved_numeric_columns
    )
    X_train = feature_extractor.fit_transform_hybrid(
        train_data,
        text_column=text_column,
        numeric_columns=resolved_numeric_columns,
    )
    X_test = feature_extractor.transform_hybrid(
        test_data,
        text_column=text_column,
    )
    return FeatureSplit(
        X_train=X_train,
        X_test=X_test,
        y_train=train_data[label_column].copy(),
        y_test=test_data[label_column].copy(),
        train_indices=train_indices,
        test_indices=test_indices,
    )


def deduplicate_modeling_rows(
    data: pd.DataFrame,
    text_column: str = "clean_advance_text",
    label_column: str = "sentiment",
) -> tuple[pd.DataFrame, dict[str, int]]:
    """Loại text trùng và bỏ toàn bộ nhóm có cùng text nhưng khác nhãn."""
    required = {text_column, label_column}
    missing = required.difference(data.columns)
    if missing:
        raise ValueError("Thiếu cột để xử lý trùng lặp: " + ", ".join(sorted(missing)))

    label_counts = data.groupby(text_column, dropna=False)[label_column].nunique()
    conflicting_texts = set(label_counts[label_counts > 1].index)
    without_conflicts = data.loc[~data[text_column].isin(conflicting_texts)]
    deduplicated = without_conflicts.drop_duplicates(
        subset=[text_column], keep="first"
    ).copy()
    audit = {
        "input_rows": int(len(data)),
        "output_rows": int(len(deduplicated)),
        "duplicate_rows_removed": int(len(data) - len(deduplicated)),
        "conflicting_groups_removed": int(len(conflicting_texts)),
    }
    return deduplicated, audit


def apply_smote(
    X_train: sparse.spmatrix,
    y_train: Sequence[str],
    random_state: int = 2026,
    k_neighbors: int = 5,
) -> tuple[sparse.csr_matrix, np.ndarray]:
    """Cân bằng riêng tập train bằng SMOTE."""
    sampler = SMOTE(random_state=random_state, k_neighbors=k_neighbors)
    X_resampled, y_resampled = sampler.fit_resample(X_train, y_train)
    return sparse.csr_matrix(X_resampled), np.asarray(y_resampled)


def save_feature_split(
    split: FeatureSplit,
    filepath: str | os.PathLike[str],
    extractor: FeatureExtractor,
    metadata: dict | None = None,
) -> None:
    """Lưu split kèm feature contract để bàn giao an toàn cho modeling."""
    path = Path(filepath)
    path.parent.mkdir(parents=True, exist_ok=True)
    feature_names = extractor.get_feature_names_out()
    if len(feature_names) != split.X_train.shape[1]:
        raise ValueError("Số tên đặc trưng không khớp chiều X_train.")
    joblib.dump(
        {
            "schema_version": 2,
            "X_train": split.X_train,
            "X_test": split.X_test,
            "y_train": split.y_train,
            "y_test": split.y_test,
            "train_indices": split.train_indices,
            "test_indices": split.test_indices,
            "feature_names": feature_names,
            "metadata": dict(metadata or {}),
        },
        path,
    )
    print(f"Đã lưu train/test features tại: {path}")


def load_feature_split(filepath: str | os.PathLike[str]) -> dict:
    """Tải và kiểm tra tính nhất quán của artifact train/test schema v2."""
    try:
        from pandas.core.arrays.string_ import StringArray

        if not getattr(StringArray, "_compat_patched", False):
            def _compat_setstate(self, state):
                if isinstance(state, tuple) and len(state) == 2:
                    state = (state[0], state[1], {})
                super(StringArray, self).__setstate__(state)

            StringArray.__setstate__ = _compat_setstate
            StringArray._compat_patched = True
    except Exception:
        pass

    artifact = joblib.load(filepath)
    required = {
        "schema_version",
        "X_train",
        "X_test",
        "y_train",
        "y_test",
        "train_indices",
        "test_indices",
        "feature_names",
        "metadata",
    }
    if not isinstance(artifact, dict) or not required.issubset(artifact):
        raise ValueError("Artifact feature split thiếu trường bắt buộc.")
    if artifact["schema_version"] != 2:
        raise ValueError("Artifact feature split không đúng schema version 2.")
    train_width = artifact["X_train"].shape[1]
    test_width = artifact["X_test"].shape[1]
    if train_width != test_width or train_width != len(artifact["feature_names"]):
        raise ValueError("Chiều ma trận không khớp feature contract.")
    if len(artifact["y_train"]) != artifact["X_train"].shape[0]:
        raise ValueError("Số nhãn train không khớp X_train.")
    if len(artifact["y_test"]) != artifact["X_test"].shape[0]:
        raise ValueError("Số nhãn test không khớp X_test.")
    return artifact
