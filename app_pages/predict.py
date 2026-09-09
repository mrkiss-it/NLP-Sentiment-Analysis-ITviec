"""Interactive review prediction page with a fail-closed model handoff."""

from __future__ import annotations

from pathlib import Path
import sys
from typing import TYPE_CHECKING

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app_services import (
    SENTIMENT_LABELS,
    get_lexicon_model_status,
    get_model_status,
    load_inference_bundle,
    load_lexicon_inference_bundle,
    predict_review,
    predict_review_lexicon,
)

if TYPE_CHECKING:
    from src.preprocessing import TextPreprocessor


EXAMPLES = {
    "Tích cực": "Môi trường làm việc thân thiện, đồng nghiệp hỗ trợ và có nhiều cơ hội học hỏi.",
    "Cân bằng": "Công việc ổn, phúc lợi bình thường nhưng quy trình còn khá chậm.",
    "Tiêu cực": "Thường xuyên OT, quản lý thiếu minh bạch và lương chưa tương xứng.",
}


@st.cache_resource
def get_preprocessor() -> TextPreprocessor:
    from src.preprocessing import TextPreprocessor

    return TextPreprocessor()


@st.cache_resource
def get_bundle(model_path: str, extractor_path: str):
    status = get_model_status()
    if not status.ready or str(status.model_path) != model_path:
        raise RuntimeError(status.message)
    if str(status.extractor_path) != extractor_path:
        raise RuntimeError("Feature extractor đã thay đổi trong lúc tải app.")
    return load_inference_bundle(status)


@st.cache_resource
def get_lexicon_bundle(model_path: str, extractor_path: str):
    """Cache bundle Hướng 2 (Text + Lexicon 5.005 chiều) riêng biệt."""
    status = get_lexicon_model_status()
    if not status.ready or str(status.model_path) != model_path:
        raise RuntimeError(status.message)
    if str(status.extractor_path) != extractor_path:
        raise RuntimeError("Lexicon extractor đã thay đổi trong lúc tải app.")
    return load_lexicon_inference_bundle(status)


st.title("Phân tích cảm xúc review")
st.caption("Nhập nội dung tự nhiên; hệ thống chỉ sử dụng văn bản, không dùng rating.")

# ── Bộ chọn mô hình Hướng 1 / Hướng 2 ──────────────────────────────────────
MODEL_OPTION_TEXT_ONLY = "Mô hình 1: Text-only (5.000 chiều)"
MODEL_OPTION_LEXICON = "Mô hình 2: Text + Lexicon (5.005 chiều)"

selected_model_option = st.radio(
    "Chọn mô hình dự đoán",
    options=[MODEL_OPTION_TEXT_ONLY, MODEL_OPTION_LEXICON],
    horizontal=True,
    key="model_selector",
    help=(
        "**Mô hình 1**: TF-IDF 5.000 chiều — pipeline triển khai mặc định.\n\n"
        "**Mô hình 2**: TF-IDF 5.000 + 5 đặc trưng Lexicon (pos_w, neg_w, pos_e, neg_e, sentiment_ratio) "
        "— pipeline nghiên cứu Hướng 2 (Ablation Study)."
    ),
)
use_lexicon_model = selected_model_option == MODEL_OPTION_LEXICON

# ── Trạng thái model tương ứng ───────────────────────────────────────────────
status = get_model_status()
lexicon_status = get_lexicon_model_status()
active_status = lexicon_status if use_lexicon_model else status

with st.container(border=True, key="model_status_panel"):
    with st.container(horizontal=True, vertical_alignment="center"):
        if active_status.ready:
            badge_label = "Text + Lexicon sẵn sàng" if use_lexicon_model else "Model sẵn sàng"
            st.badge(badge_label, icon=":material/check_circle:", color="green")
        else:
            badge_label = "Chờ artifact Text + Lexicon" if use_lexicon_model else "Chưa tải được mô hình"
            st.badge(badge_label, icon=":material/schedule:", color="orange")
        st.caption(active_status.message)

st.subheader("Thử nhanh với review mẫu")
example = st.pills(
    "Review mẫu",
    options=list(EXAMPLES),
    selection_mode="single",
    key="review_example",
    label_visibility="collapsed",
)
if example and st.session_state.get("last_review_example") != example:
    st.session_state["review_input"] = EXAMPLES[example]
    st.session_state["last_review_example"] = example

with st.form("sentiment_form", border=True):
    review_text = st.text_area(
        "Nội dung review",
        key="review_input",
        placeholder="Ví dụ: Môi trường tốt nhưng công ty cần cải thiện chính sách OT...",
        height=170,
        max_chars=3000,
        help="Có thể nhập tiếng Việt, tiếng Anh ngành IT, teencode và emoji.",
    )
    with st.container(horizontal=True, horizontal_alignment="right"):
        submitted = st.form_submit_button(
            "Phân tích cảm xúc",
            type="primary",
            icon=":material/auto_awesome:",
        )

result_slot = st.container()
if submitted:
    if not review_text.strip():
        result_slot.error("Hãy nhập nội dung review trước khi phân tích.", icon=":material/error:")
    else:
        model_name_label = "Mô hình 2 (Text + Lexicon 5.005 chiều)" if use_lexicon_model else "Mô hình 1 (Text-only 5.000 chiều)"
        prediction = None
        with result_slot:
            with st.status("Đang phân tích cảm xúc đánh giá...", expanded=True) as status_box:
                st.write(":material/cleaning_services: 1. Chuẩn hóa Unicode, giải mã emoji và dịch teencode...")
                preprocessor = get_preprocessor()
                processed_preview = preprocessor.clean_advance_text(review_text)

                st.write(":material/psychology: 2. Tách từ tiếng Việt (`underthesea`) và đối soát từ điển sắc thái...")

                st.write(f":material/smart_toy: 3. Đưa vào Stacking Ensemble Classifier ({model_name_label})...")

                if not active_status.ready or active_status.model_path is None:
                    status_box.update(label="Mô hình chưa sẵn sàng", state="error", expanded=True)
                    pending_msg = (
                        "Artifact Hướng 2 chưa sẵn sàng. Chạy scripts/build_text_lexicon_artifacts.py."
                        if use_lexicon_model
                        else "Giao diện đã sẵn sàng nhưng chưa thể dự đoán vì model chưa được bàn giao."
                    )
                    st.warning(pending_msg, icon=":material/pending:")
                    st.markdown("**Văn bản sau tiền xử lý**")
                    st.code(processed_preview or "(không còn token hợp lệ)", language=None)
                    st.caption("Không có nhãn hoặc điểm số giả được sinh ra trong trạng thái này.")
                else:
                    try:
                        if use_lexicon_model:
                            model, extractor = get_lexicon_bundle(
                                str(lexicon_status.model_path), str(lexicon_status.extractor_path)
                            )
                            prediction = predict_review_lexicon(
                                review_text, model, extractor, preprocessor
                            )
                        else:
                            model, extractor = get_bundle(
                                str(status.model_path), str(status.extractor_path)
                            )
                            prediction = predict_review(
                                review_text, model, extractor, preprocessor
                            )
                    except (AttributeError, OSError, RuntimeError, TypeError, ValueError, Exception) as exc:
                        status_box.update(label="Lỗi trong quá trình suy luận!", state="error", expanded=True)
                        st.error(f"Không thể thực hiện dự đoán: {exc}", icon=":material/error:")
                    else:
                        status_box.update(label="Phân tích hoàn tất thành công!", state="complete", expanded=False)

            if prediction is not None:
                label_vi = SENTIMENT_LABELS.get(prediction.label, prediction.label)
                with result_slot.container(border=True):
                    header_col1, header_col2, header_col3 = st.columns([2, 1, 1], vertical_alignment="center")
                    with header_col1:
                        st.subheader(f"Kết quả: {label_vi}")
                    with header_col2:
                        decision_type = getattr(prediction, "decision_type", "ml")
                        if decision_type == "hybrid":
                            st.badge("Hybrid NLP + Lexicon", icon=":material/auto_fix_high:", color="blue")
                        else:
                            st.badge("Mô hình Học máy", icon=":material/smart_toy:", color="green")
                    with header_col3:
                        if use_lexicon_model:
                            st.badge("Mô hình 2 · 5.005 chiều", icon=":material/science:", color="violet")
                        else:
                            st.badge("Mô hình 1 · 5.000 chiều", icon=":material/text_fields:", color="gray")

                    confidence = getattr(prediction, "confidence", None)
                    if confidence is not None:
                        st.metric("Độ tin cậy", f"{confidence:.1%}", border=True)
                    else:
                        st.caption("Model không cung cấp xác suất đã hiệu chỉnh.")

                    probabilities = getattr(prediction, "probabilities", None)
                    if probabilities:
                        st.markdown("**Phân bố xác suất 3 lớp cảm xúc**")
                        p_cols = st.columns(3)
                        p_order = [("Positive", "Tích cực", "green"), ("Neutral", "Trung tính", "orange"), ("Negative", "Tiêu cực", "red")]
                        for (cls_name, cls_label, color), col in zip(p_order, p_cols):
                            val = probabilities.get(cls_name, 0.0)
                            with col:
                                st.caption(f"{cls_label}: **{val:.1%}**")
                                st.progress(min(max(val, 0.0), 1.0))

                    raw_ml_label = getattr(prediction, "raw_ml_label", None)
                    raw_ml_probs = getattr(prediction, "raw_ml_probabilities", None)

                    if decision_type == "hybrid" and raw_ml_label is not None:
                        raw_label_vi = SENTIMENT_LABELS.get(raw_ml_label, raw_ml_label)
                        with st.container(border=True):
                            st.markdown("##### :material/compare_arrows: Cơ chế Hiệu chỉnh Hybrid: So sánh Trước & Sau can thiệp")
                            col_raw, col_calib = st.columns(2)
                            with col_raw:
                                st.markdown("**1. Dự đoán ban đầu của Mô hình ML (Stacking):**")
                                raw_badge_color = "red" if raw_ml_label == "Negative" else ("green" if raw_ml_label == "Positive" else "orange")
                                st.badge(f"Nhãn ML gốc: {raw_label_vi}", color=raw_badge_color)
                                if raw_ml_probs:
                                    st.caption(
                                        f"Xác suất ML gốc: Tích cực **{raw_ml_probs.get('Positive', 0.0):.1%}** · "
                                        f"Trung tính **{raw_ml_probs.get('Neutral', 0.0):.1%}** · "
                                        f"Tiêu cực **{raw_ml_probs.get('Negative', 0.0):.1%}**"
                                    )
                                st.caption("↳ *Mô hình ML dễ bị ảnh hưởng bởi từ đơn lẻ (ví dụ: 'thân thiện', 'hỗ trợ') hoặc lệch do mất cân bằng lớp.*")
                            with col_calib:
                                st.markdown("**2. Sau khi Cổng Hybrid (NLP + Lexicon) can thiệp:**")
                                final_badge_color = "red" if prediction.label == "Negative" else ("green" if prediction.label == "Positive" else "orange")
                                st.badge(f"Kết quả hiệu chỉnh: {label_vi}", color=final_badge_color)
                                if probabilities:
                                    st.caption(
                                        f"Xác suất hiệu chỉnh: Tích cực **{probabilities.get('Positive', 0.0):.1%}** · "
                                        f"Trung tính **{probabilities.get('Neutral', 0.0):.1%}** · "
                                        f"Tiêu cực **{probabilities.get('Negative', 0.0):.1%}**"
                                    )
                                st.caption("↳ *Thuật toán Negation Scope phát hiện cụm phủ định/giảm mức độ để đảo chiều sắc thái chính xác.*")

                    explanation = getattr(prediction, "explanation", "")
                    if explanation:
                        st.info(explanation, icon=":material/info:")

                    with st.expander("Chi tiết bóc tách ngôn ngữ (Explainable AI)", icon=":material/insights:"):
                        tab_ml, tab_transformer = st.tabs([
                            "Tiền xử lý cho Machine Learning (TF-IDF)",
                            "Tiền xử lý cho Pretrained Transformer (ViSoBERT)",
                        ])
                        with tab_ml:
                            st.caption("Tách từ ghép tiếng Việt (`underthesea`), loại bỏ stopwords và dịch thuật ngữ IT để tối ưu không gian vector TF-IDF.")
                            st.code(prediction.processed_text, language=None)
                        with tab_transformer:
                            clean_fn = getattr(preprocessor, "clean_text_for_transformer", None)
                            if clean_fn is not None:
                                transformer_text = clean_fn(review_text)
                            else:
                                from src.preprocessing import TextPreprocessor as _FreshPreprocessor
                                transformer_text = _FreshPreprocessor().clean_text_for_transformer(review_text)
                            st.caption("Bảo toàn dấu câu và ngữ pháp (. , !), giữ nguyên Emoji tự nhiên và teencode cho BPE Tokenizer và cơ chế Self-Attention.")
                            st.code(transformer_text, language=None)

                        lexicon_stats = getattr(prediction, "lexicon_stats", None)
                        if lexicon_stats:
                            pos_phrases = lexicon_stats.get("pos_phrases", [])
                            neg_phrases = lexicon_stats.get("neg_phrases", [])
                            lex_c1, lex_c2 = st.columns(2)
                            with lex_c1:
                                st.markdown(f"**Từ/cụm tích cực ({len(pos_phrases)}):**")
                                if pos_phrases:
                                    st.write(", ".join(f"`{p}`" for p in pos_phrases))
                                else:
                                    st.caption("Không có")
                            with lex_c2:
                                st.markdown(f"**Từ/cụm tiêu cực / phủ định ({len(neg_phrases)}):**")
                                if neg_phrases:
                                    st.write(", ".join(f"`{p}`" for p in neg_phrases))
                                else:
                                    st.caption("Không có")



st.subheader("Pipeline suy luận")
if use_lexicon_model:
    with st.container(horizontal=True):
        with st.container(border=True, key="pipeline_review_card"):
            st.markdown("#### :material/chat: 1. Review")
            st.caption("Nội dung người dùng nhập, không yêu cầu rating hay thông tin công ty.")
        with st.container(border=True, key="pipeline_clean_card"):
            st.markdown("#### :material/cleaning_services: 2. Tiền xử lý")
            st.caption("Chuẩn hóa Unicode, emoji, teencode, tách từ và loại stopword.")
        with st.container(border=True, key="pipeline_vector_card"):
            st.markdown("#### :material/hub: 3. TF-IDF + Lexicon")
            st.caption("TF-IDF 5.000 chiều || MinMaxScaler(pos_w, neg_w, pos_e, neg_e, ratio) → **5.005 chiều**.")
        with st.container(border=True, key="pipeline_result_card"):
            st.markdown("#### :material/label: 4. Cảm xúc")
            st.caption("Trả về Tích cực, Trung tính hoặc Tiêu cực (Hướng 2 — Text + Lexicon).")
else:
    with st.container(horizontal=True):
        with st.container(border=True, key="pipeline_review_card"):
            st.markdown("#### :material/chat: 1. Review")
            st.caption("Nội dung người dùng nhập, không yêu cầu rating hay thông tin công ty.")
        with st.container(border=True, key="pipeline_clean_card"):
            st.markdown("#### :material/cleaning_services: 2. Tiền xử lý")
            st.caption("Chuẩn hóa Unicode, emoji, teencode, tách từ và loại stopword.")
        with st.container(border=True, key="pipeline_vector_card"):
            st.markdown("#### :material/hub: 3. TF-IDF")
            st.caption("Biến văn bản thành vector **5.000 đặc trưng** theo artifact đã khóa.")
        with st.container(border=True, key="pipeline_result_card"):
            st.markdown("#### :material/label: 4. Cảm xúc")
            st.caption("Trả về Tích cực, Trung tính hoặc Tiêu cực khi model sẵn sàng.")

with st.expander("Lưu ý khi diễn giải", icon=":material/info:"):
    st.markdown(
        """
        - Nhãn huấn luyện được suy ra từ rating nên không phải ground truth do con người gán trực tiếp.
        - Confidence chỉ hiển thị khi model có `predict_proba()`; app không tự chế điểm tin cậy.
        - Kết quả phục vụ demo học thuật, không thay thế đánh giá nhân sự chuyên môn.
        """
    )
