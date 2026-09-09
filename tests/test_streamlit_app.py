from pathlib import Path
import sys

import pytest
try:
    import tomllib
except ModuleNotFoundError:
    import toml as tomllib

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from streamlit.testing.v1 import AppTest

from src.app_services import get_model_status



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
        PROJECT_ROOT / "app_pages" / "predict.py", default_timeout=90
    ).run()
    app.text_area[0].set_value("Môi trường tốt nhưng thường xuyên OT không lương")
    app.button[0].click().run()

    assert not app.exception
    if not get_model_status().ready:
        assert any("model chưa được bàn giao" in item.value for item in app.warning)
        assert app.code


def test_company_insights_page_renders_real_dataset():
    app = AppTest.from_file(
        PROJECT_ROOT / "app_pages" / "insights.py", default_timeout=90
    ).run()

    assert not app.exception
    assert any("Insight cảm xúc" in title.value for title in app.title)
    assert app.metric
    assert any(
        "WordCloud chỉ được tạo" in caption.value for caption in app.caption
    )


def test_lexicon_model_status_dataclass_fields():
    """Kiểm tra LexiconModelStatus trả về đúng cấu trúc dataclass cho Hướng 2."""
    from src.app_services import LexiconModelStatus, get_lexicon_model_status

    status = get_lexicon_model_status()

    # Luôn trả về LexiconModelStatus dù artifact có sẵn hay chưa
    assert isinstance(status, LexiconModelStatus)
    assert isinstance(status.ready, bool)
    assert isinstance(status.message, str)
    assert len(status.message) > 0
    # extractor_path phải là đường dẫn hợp lệ trỏ vào thư mục models/
    assert "text_lexicon_feature_extractor" in str(status.extractor_path)
    if status.model_path is not None:
        assert "best_text_lexicon_model" in str(status.model_path)


def test_predict_review_lexicon_returns_valid_prediction():
    """Kiểm tra predict_review_lexicon trả về PredictionResult hợp lệ trên câu phủ định phức tạp.

    Bỏ qua nếu artifact Hướng 2 chưa sẵn sàng (chưa chạy build_text_lexicon_artifacts.py).
    """
    from src.app_services import (
        PredictionResult,
        get_lexicon_model_status,
        load_lexicon_inference_bundle,
        predict_review_lexicon,
    )
    from src.preprocessing import TextPreprocessor

    status = get_lexicon_model_status()
    if not status.ready:
        pytest.skip("Artifact Hướng 2 chưa sẵn sàng. Chạy scripts/build_text_lexicon_artifacts.py.")

    model, extractor = load_lexicon_inference_bundle(status)
    preprocessor = TextPreprocessor()
    text = "Môi trường làm việc không được thân thiện, đồng nghiệp không hỗ trợ và ít cơ hội học hỏi."

    result = predict_review_lexicon(text, model, extractor, preprocessor)

    assert isinstance(result, PredictionResult)
    assert result.label in {"Positive", "Neutral", "Negative"}
    assert result.confidence is not None
    assert 0.0 <= result.confidence <= 1.0
    assert result.decision_type in {"ml", "hybrid"}
    assert result.probabilities is not None
    # Câu phủ định tiêu cực rõ ràng — Negative phải cao hơn Positive
    assert result.probabilities.get("Negative", 0) > result.probabilities.get("Positive", 0)
    assert result.label == "Negative"

def test_benchmark_page_renders_leaderboard_and_metrics():
    """Kiểm tra trang app_pages/benchmark.py render thành công leaderboard và các thẻ KPI."""
    app = AppTest.from_file(
        PROJECT_ROOT / "app_pages" / "benchmark.py", default_timeout=90
    ).run()

    assert not app.exception
    assert any("Hiệu năng Mô hình" in title.value for title in app.title)
    assert len(app.metric) >= 4
    assert any("Stacking" in m.value for m in app.metric)
    assert any("0.5507" in m.value for m in app.metric)
