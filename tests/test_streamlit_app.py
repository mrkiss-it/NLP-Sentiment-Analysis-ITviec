from pathlib import Path
import sys

import pytest

try:
    import tomllib
except ModuleNotFoundError:
    import toml as tomllib

from streamlit.testing.v1 import AppTest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app_services import get_model_status


def test_theme_config_locks_the_app_to_developer_dark_mode():
    config = tomllib.loads((PROJECT_ROOT / ".streamlit" / "config.toml").read_text(encoding="utf-8"))
    theme = config["theme"]

    assert theme["base"] == "dark"
    assert theme["primaryColor"] == "#7AA7FF"
    assert theme["backgroundColor"] == "#080B10"
    assert theme["sidebar"]["backgroundColor"] == "#0C1017"
    assert "DM Sans" in theme["font"]
    assert "JetBrains Mono" in theme["codeFont"]
    assert "light" not in theme
    assert "dark" not in theme


def test_dark_style_has_an_ultrawide_content_limit():
    source = (PROJECT_ROOT / "src" / "app_theme.py").read_text(encoding="utf-8")

    assert '[data-testid="stMainBlockContainer"]' in source
    assert "max-width: 1920px" in source
    assert "padding-inline: clamp(1rem, 3vw, 4rem)" in source
    assert "--it-bg: #080b10" in source
    assert "--it-blue: #7aa7ff" in source
    assert 'background: var(--it-blue)' in source
    assert '"JetBrains Mono"' in source
    assert "render_theme_picker" not in source
    assert '[data-testid="stToolbar"] > div > div:last-child' not in source


def test_streamlit_entrypoint_renders_default_page():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=90).run()
    source = (PROJECT_ROOT / "app.py").read_text(encoding="utf-8")

    assert not app.exception
    assert any("Khám phá góc nhìn nhân sự" in title.value for title in app.title)
    assert "st.logo(" in source
    assert "TV4 · Phạm Thành Trung" not in source
    assert (PROJECT_ROOT / "assets" / "sentiment-lab-logo.svg").is_file()
    assert (PROJECT_ROOT / "assets" / "sentiment-lab-mark.svg").is_file()
    assert "render_theme_picker" not in source


def test_prediction_page_handles_model_handoff_state():
    app = AppTest.from_file(
        PROJECT_ROOT / "app.py", default_timeout=90
    ).run().switch_page("app_pages/predict.py").run()
    app.text_area[0].set_value("Môi trường tốt nhưng thường xuyên OT không lương")
    app.button[0].click().run()

    assert not app.exception
    pipeline_text = [item.value for item in app.markdown]
    assert any("Tiền xử lý văn bản" in value for value in pipeline_text)
    assert any("Biểu diễn & dự đoán" in value for value in pipeline_text)
    assert any("Ra quyết định" in value for value in pipeline_text)
    if not get_model_status().ready:
        assert any("model chưa được bàn giao" in item.value for item in app.warning)
        assert app.code


def test_prediction_result_survives_rerun_but_clears_when_input_changes():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=90).run()
    app.switch_page("app_pages/predict.py").run()
    app.text_area[0].set_value("Môi trường tốt và đồng nghiệp thân thiện").run()
    app.button(key="analyze_review").click().run()
    assert not app.exception
    if get_model_status().ready:
        result = app.session_state["analysis_result"]
        app.run()
        assert app.session_state["analysis_result"] == result
        app.text_area[0].set_value("Một nội dung khác chưa được phân tích").run()
        assert "analysis_result" not in app.session_state


def test_unified_evaluation_view_loads_saved_evidence_without_model_inference():
    app = AppTest.from_file(
        PROJECT_ROOT / "app_pages" / "benchmark.py", default_timeout=90
    ).run()
    app.segmented_control(key="model_evaluation_view").set_value(
        "Chất lượng mô hình"
    ).run()
    assert not app.exception
    assert any("Hiệu năng và chất lượng mô hình" in item.value for item in app.title)
    assert any(metric.label == "Macro F1" for metric in app.metric)


def test_unified_error_analysis_view_renders_saved_review_errors():
    app = AppTest.from_file(
        PROJECT_ROOT / "app_pages" / "benchmark.py", default_timeout=90
    ).run()
    app.segmented_control(key="model_evaluation_view").set_value(
        "Lỗi & ngưỡng"
    ).run()

    assert not app.exception
    assert app.select_slider(key="evaluation_threshold").value == 0.30
    metric_values = {metric.label: metric.value for metric in app.metric}
    assert metric_values["Ngưỡng đang xem"] == "30%"
    assert metric_values["Recall Tiêu cực"] == "35.1%"
    app.select_slider(key="evaluation_threshold").set_value(0.10).run()
    metric_values = {metric.label: metric.value for metric in app.metric}
    assert metric_values["Ngưỡng đang xem"] == "10%"
    assert metric_values["Recall Tiêu cực"] == "77.2%"
    assert app.selectbox(key="error_pair").value
    assert app.selectbox(key="error_review").value is not None


def test_company_insights_page_renders_real_dataset():
    app = AppTest.from_file(
        PROJECT_ROOT / "app_pages" / "insights.py", default_timeout=90
    ).run()

    assert not app.exception
    assert any(title.value == "Insight doanh nghiệp" for title in app.title)
    assert app.metric
    metric_labels = {metric.label for metric in app.metric}
    assert {
        "Review được phân tích",
        "Lượt xuất hiện từ",
        "Từ khóa dẫn đầu",
    } <= metric_labels
    assert any(
        "Từ xuất hiện nhiều hơn" in caption.value
        for caption in app.caption
    )
    assert any(title.value == "Góc nhìn review" for title in app.subheader)
    assert not any(expander.label == "Khám phá review chi tiết" for expander in app.expander)
    assert len(app.radio(key="review_selection").options) == 8
    assert app.text_input(key="review_query").value == ""


def test_lexicon_model_status_dataclass_fields():
    from src.app_services import LexiconModelStatus, get_lexicon_model_status

    status = get_lexicon_model_status()
    assert isinstance(status, LexiconModelStatus)
    assert isinstance(status.ready, bool)
    assert isinstance(status.message, str) and status.message
    assert "text_lexicon_feature_extractor" in str(status.extractor_path)
    if status.model_path is not None:
        assert "best_text_lexicon_model" in str(status.model_path)


def test_predict_review_lexicon_returns_valid_prediction():
    from src.app_services import (
        PredictionResult,
        get_lexicon_model_status,
        load_lexicon_inference_bundle,
        predict_review_lexicon,
    )
    from src.preprocessing import TextPreprocessor

    status = get_lexicon_model_status()
    if not status.ready:
        pytest.skip("Artifact Text + Lexicon chưa sẵn sàng.")

    model, extractor = load_lexicon_inference_bundle(status)
    result = predict_review_lexicon(
        "Môi trường làm việc không được thân thiện, đồng nghiệp không hỗ trợ và ít cơ hội học hỏi.",
        model,
        extractor,
        TextPreprocessor(),
    )
    assert isinstance(result, PredictionResult)
    assert result.label == "Negative"
    assert result.confidence is not None and 0.0 <= result.confidence <= 1.0
    assert result.decision_type in {"ml", "threshold", "hybrid"}
    assert result.probabilities is not None
    assert result.probabilities.get("Negative", 0) > result.probabilities.get("Positive", 0)


def test_benchmark_page_renders_leaderboard_and_metrics():
    app = AppTest.from_file(
        PROJECT_ROOT / "app_pages" / "benchmark.py", default_timeout=90
    ).run()

    assert not app.exception
    assert any(title.value == "Hiệu năng và chất lượng mô hình" for title in app.title)
    assert len(app.metric) >= 4
    assert any("Stacking" in metric.value for metric in app.metric)
    assert any("0.5475" in metric.value for metric in app.metric)
    assert any("Bảng xếp hạng mô hình" in item.value for item in app.markdown)
    assert len(app.dataframe) >= 1
    leaderboard = app.dataframe[0].value
    assert leaderboard["Hạng"].tolist() == [1, 2, 3, 4, 5]
    assert leaderboard.iloc[0]["Mô hình"] == "Stacking Ensemble"

    navigation_source = (PROJECT_ROOT / "app.py").read_text(encoding="utf-8")
    assert 'title="Mô hình & đánh giá"' in navigation_source
    assert 'st.Page("app_pages/evaluation.py"' not in navigation_source
