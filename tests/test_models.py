from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd
import pytest

from src.features import FeatureExtractor, prepare_feature_split
from src.models import PARAM_GRIDS, SentimentModelTrainer



def sample_reviews(n_per_class: int = 15) -> pd.DataFrame:
    tone_by_label = {
        "Positive": "môi_trường tốt phúc_lợi tốt sếp tâm_lý",
        "Neutral": "môi_trường bình_thường lương ổn",
        "Negative": "quản_lý tệ áp_lực cao ot nhiều",
    }
    rows = []
    for label, tone in tone_by_label.items():
        for index in range(n_per_class):
            rows.append({"clean_advance_text": f"{tone} mẫu_{label}_{index}", "sentiment": label})
    return pd.DataFrame(rows)


def make_split():
    data = sample_reviews()
    extractor = FeatureExtractor(max_features=200, min_df=1)
    return prepare_feature_split(data, extractor=extractor, random_state=2026)


TINY_PARAM_GRIDS = {
    "Multinomial Naive Bayes": {"alpha": [0.5, 1.0]},
    "Logistic Regression": {"solver": ["lbfgs"], "penalty": ["l2"], "C": [1.0]},
    "Support Vector Machine (Linear)": {"C": [0.5, 1.0]},
    "Random Forest": {"n_estimators": [10], "max_depth": [5]},
}


def test_param_grids_cover_all_four_base_models():
    assert set(PARAM_GRIDS) == {
        "Multinomial Naive Bayes",
        "Logistic Regression",
        "Support Vector Machine (Linear)",
        "Random Forest",
    }


def test_tune_hyperparameters_returns_a_row_per_model_with_best_params():
    split = make_split()
    trainer = SentimentModelTrainer()

    results = trainer.tune_hyperparameters(
        split.X_train,
        split.y_train,
        cv=3,
        n_jobs=1,
        param_grids=TINY_PARAM_GRIDS,
    )

    assert set(results["Model"]) == set(TINY_PARAM_GRIDS)
    assert set(trainer.best_params) == set(TINY_PARAM_GRIDS)
    assert set(trainer.trained_models) == set(TINY_PARAM_GRIDS)


def test_tuned_svm_supports_predict_proba_for_stacking():
    split = make_split()
    trainer = SentimentModelTrainer()

    trainer.tune_hyperparameters(
        split.X_train,
        split.y_train,
        cv=3,
        n_jobs=1,
        param_grids=TINY_PARAM_GRIDS,
    )
    svm = trainer.trained_models["Support Vector Machine (Linear)"]

    proba = svm.predict_proba(split.X_test)

    assert proba.shape[0] == split.X_test.shape[0]


def test_stacking_model_uses_supplied_tuned_base_estimators():
    split = make_split()
    trainer = SentimentModelTrainer()
    trainer.tune_hyperparameters(
        split.X_train,
        split.y_train,
        cv=3,
        n_jobs=1,
        param_grids=TINY_PARAM_GRIDS,
    )

    stack = trainer.get_stacking_model(base_estimators=trainer.trained_models)
    stack.fit(split.X_train, split.y_train)
    predictions = stack.predict(split.X_test)

    assert len(predictions) == split.X_test.shape[0]
    tuned_nb_alpha = trainer.trained_models["Multinomial Naive Bayes"].alpha
    stack_nb_alpha = dict(stack.estimators)["nb"].alpha
    assert stack_nb_alpha == tuned_nb_alpha


def test_get_stacking_model_falls_back_to_defaults_without_base_estimators():
    stack = SentimentModelTrainer().get_stacking_model()

    estimator_names = [name for name, _ in stack.estimators]

    assert estimator_names == ["nb", "lr", "svm"]


def test_save_model_round_trips_a_trained_model(tmp_path):
    split = make_split()
    trainer = SentimentModelTrainer()
    trainer.train_and_evaluate_all(
        split.X_train, split.y_train, split.X_test, split.y_test
    )
    filepath = tmp_path / "best_sentiment_model.joblib"

    trainer.save_model("Logistic Regression", str(filepath))

    assert filepath.exists()


def test_save_model_raises_for_an_untrained_model_name(tmp_path):
    trainer = SentimentModelTrainer()

    with pytest.raises(ValueError):
        trainer.save_model("Not A Model", str(tmp_path / "x.joblib"))
