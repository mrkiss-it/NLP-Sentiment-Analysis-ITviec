from pathlib import Path
import tomllib

from streamlit.testing.v1 import AppTest

from src.app_services import get_model_status


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_theme_config_locks_the_app_to_developer_dark_mode():
    config = tomllib.loads((PROJECT_ROOT / ".streamlit" / "config.toml").read_text())
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
    source = (PROJECT_ROOT / "src" / "app_theme.py").read_text()

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
    source = (PROJECT_ROOT / "app.py").read_text()

    assert not app.exception
    assert any("Hiểu tiếng nói" in title.value for title in app.title)
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


def test_evaluation_page_loads_saved_evidence_without_model_inference():
    app = AppTest.from_file(PROJECT_ROOT / "app.py", default_timeout=90).run()
    app.switch_page("app_pages/evaluation.py").run()
    assert not app.exception
    assert any("Mô hình tốt đến đâu" in item.value for item in app.title)
    assert any(metric.label == "Macro F1" for metric in app.metric)


def test_company_insights_page_renders_real_dataset():
    app = AppTest.from_file(
        PROJECT_ROOT / "app_pages" / "insights.py", default_timeout=90
    ).run()

    assert not app.exception
    assert any("Insight cảm xúc" in title.value for title in app.title)
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
    assert any(title.value == "Tiếng nói từ review" for title in app.subheader)
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
    assert any("Hiệu năng Mô hình" in title.value for title in app.title)
    assert len(app.metric) >= 4
    assert any("Stacking" in metric.value for metric in app.metric)
    assert any("0.5507" in metric.value for metric in app.metric)
