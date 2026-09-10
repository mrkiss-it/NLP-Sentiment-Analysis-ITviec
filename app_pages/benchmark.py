"""Model Benchmark and Performance Metrics page for ITviec Sentiment Analysis."""

from pathlib import Path
import sys

import pandas as pd
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

FIGURES_DIR = PROJECT_ROOT / "reports" / "figures"


st.title("Hiệu năng Mô hình & Bảng so sánh Benchmark")
st.caption(
    "Đánh giá độc lập trên tập kiểm thử đã khóa: 1.683 mẫu (20% dữ liệu thực tế), "
    "phân tầng theo nhãn cảm xúc (Stratified, seed=2026)."
)

# ── 1. Thẻ KPI Tổng quan ───────────────────────────────────────────────────
with st.container(horizontal=True, gap="xsmall"):
    with st.container(key="kpi_best_model"):
        st.metric(
            "Mô hình Quán quân",
            "Stacking (5.005D)",
            help="Mô hình 2: Stacking Ensemble (NB + LR + SVM + RF) kết hợp TF-IDF và 5 đặc trưng Lexicon",
            border=True,
        )
    with st.container(key="kpi_f1_macro"):
        st.metric(
            "Macro F1 cao nhất",
            "0.5507",
            delta="+0.0032 so với Text-only",
            help="Độ đo quyết định đánh giá công bằng cả 3 lớp trên tập Test đã khóa",
            border=True,
        )
    with st.container(key="kpi_accuracy"):
        st.metric(
            "Độ chính xác (Accuracy)",
            "78.0%",
            delta="+0.3%",
            help="Tỷ lệ dự đoán đúng trên toàn bộ 1.683 mẫu test",
            border=True,
        )
    with st.container(key="kpi_neg_f1"):
        st.metric(
            "F1 lớp Tiêu cực",
            "0.380",
            delta="+0.027 (+7.7%)",
            help="Lớp thiểu số khó nhất (chỉ chiếm 6.8% dữ liệu), Lexicon giúp cải thiện rõ rệt",
            border=True,
        )

st.divider()

# ── 2. Bảng Xếp Hạng Mô Hình (Model Leaderboard) ───────────────────────────
st.subheader(":material/leaderboard: 1. Bảng xếp hạng toàn diện (Model Leaderboard)")
st.caption(
    "So sánh công bằng giữa tất cả thuật toán học máy đã tinh chỉnh siêu tham số "
    "(GridSearchCV 5-Fold) và mô hình ngôn ngữ sâu Transformer (ViSoBERT) trên cùng tập Test."
)

leaderboard_data = [
    {
        "Hạng": "🥇 1",
        "Mô hình": "Stacking Ensemble",
        "Hướng tiếp cận": "Mô hình 2 (Text + Lexicon 5.005D)",
        "CV Macro F1": "0.5658",
        "Test Macro F1": "0.5507",
        "Test Accuracy": "78.0%",
        "F1 Tích cực": "0.88",
        "F1 Trung tính": "0.39",
        "F1 Tiêu cực": "0.38",
    },
    {
        "Hạng": "🥈 2",
        "Mô hình": "Stacking Ensemble",
        "Hướng tiếp cận": "Mô hình 1 (Text-only 5.000D)",
        "CV Macro F1": "0.5619",
        "Test Macro F1": "0.5475",
        "Test Accuracy": "77.7%",
        "F1 Tích cực": "0.88",
        "F1 Trung tính": "0.41",
        "F1 Tiêu cực": "0.35",
    },
    {
        "Hạng": "🥉 3",
        "Mô hình": "Logistic Regression",
        "Hướng tiếp cận": "Text-only (C=1.0, L2, Tuned)",
        "CV Macro F1": "0.5567",
        "Test Macro F1": "0.5412",
        "Test Accuracy": "76.5%",
        "F1 Tích cực": "0.86",
        "F1 Trung tính": "0.39",
        "F1 Tiêu cực": "0.34",
    },
    {
        "Hạng": "4",
        "Mô hình": "Linear SVM",
        "Hướng tiếp cận": "Text-only (C=0.1, Tuned)",
        "CV Macro F1": "0.5561",
        "Test Macro F1": "0.5398",
        "Test Accuracy": "76.2%",
        "F1 Tích cực": "0.86",
        "F1 Trung tính": "0.38",
        "F1 Tiêu cực": "0.33",
    },
    {
        "Hạng": "5",
        "Mô hình": "Random Forest",
        "Hướng tiếp cận": "Text-only (n=200, depth=20)",
        "CV Macro F1": "0.5515",
        "Test Macro F1": "0.5280",
        "Test Accuracy": "75.8%",
        "F1 Tích cực": "0.85",
        "F1 Trung tính": "0.37",
        "F1 Tiêu cực": "0.31",
    },
    {
        "Hạng": "6",
        "Mô hình": "Multinomial Naive Bayes",
        "Hướng tiếp cận": "Text-only (alpha=0.1, Tuned)",
        "CV Macro F1": "0.4890",
        "Test Macro F1": "0.4650",
        "Test Accuracy": "72.1%",
        "F1 Tích cực": "0.82",
        "F1 Trung tính": "0.31",
        "F1 Tiêu cực": "0.28",
    },
    {
        "Hạng": "7",
        "Mô hình": "ViSoBERT Pretrained",
        "Hướng tiếp cận": "Deep Learning (GPU, Zero-shot)",
        "CV Macro F1": "—",
        "Test Macro F1": "0.4036",
        "Test Accuracy": "65.4%",
        "F1 Tích cực": "0.82",
        "F1 Trung tính": "0.09",
        "F1 Tiêu cực": "0.30",
    },
]

df_leaderboard = pd.DataFrame(leaderboard_data)
st.dataframe(
    df_leaderboard,
    column_config={
        "Hạng": st.column_config.TextColumn("Hạng", width="small"),
        "Mô hình": st.column_config.TextColumn("Mô hình", width="medium"),
        "Hướng tiếp cận": st.column_config.TextColumn("Hướng tiếp cận", width="large"),
        "CV Macro F1": st.column_config.TextColumn("CV Macro F1", help="5-Fold Stratified CV trên train set"),
        "Test Macro F1": st.column_config.TextColumn("Test Macro F1", help="Độ đo cốt lõi trên 1.683 mẫu test"),
        "Test Accuracy": st.column_config.TextColumn("Accuracy"),
        "F1 Tích cực": st.column_config.TextColumn("F1 (Pos)"),
        "F1 Trung tính": st.column_config.TextColumn("F1 (Neu)"),
        "F1 Tiêu cực": st.column_config.TextColumn("F1 (Neg)"),
    },
    hide_index=True,
    use_container_width=True,
)

st.divider()

# ── 3. Biểu đồ So sánh Trực quan (300 DPI Figures) ─────────────────────────
st.subheader(":material/monitoring: 2. Đồ thị so sánh và Ma trận nhầm lẫn")

fig_col1, fig_col2 = st.columns(2, gap="medium")

with fig_col1:
    with st.container(border=True):
        st.markdown("#### :material/bar_chart: So sánh Macro F1 giữa các mô hình")
        f1_chart_path = FIGURES_DIR / "model_comparison_f1_macro.png"
        if f1_chart_path.exists():
            st.image(str(f1_chart_path), caption="Biểu đồ so sánh 5-Fold CV Macro F1 (TV3 huấn luyện)")
        else:
            st.info("Chưa tìm thấy ảnh biểu đồ so sánh F1.")

with fig_col2:
    with st.container(border=True):
        st.markdown("#### :material/grid_on: Ma trận nhầm lẫn (Confusion Matrix)")
        cm_path = FIGURES_DIR / "best_model_confusion_matrix.png"
        if cm_path.exists():
            st.image(str(cm_path), caption="Confusion Matrix của Stacking Classifier trên tập Test đã khóa")
        else:
            st.info("Chưa tìm thấy ảnh Confusion Matrix.")

with st.expander("🔬 Xem thêm biểu đồ Ablation Study (Nghiên cứu đặc trưng của TV2)", icon=":material/science:"):
    ablation_c1, ablation_c2 = st.columns(2)
    with ablation_c1:
        abl_cv_path = FIGURES_DIR / "eda_feature_ablation_cv.png"
        if abl_cv_path.exists():
            st.image(str(abl_cv_path), caption="Ablation: So sánh CV Macro F1 giữa các nhóm đặc trưng")
    with ablation_c2:
        abl_class_path = FIGURES_DIR / "eda_ablation_per_class.png"
        if abl_class_path.exists():
            st.image(str(abl_class_path), caption="Ablation: F1-Score từng lớp cảm xúc")

st.divider()

# ── 4. Báo cáo Phân loại Chi tiết (Classification Report Breakdown) ─────────
st.subheader(":material/table_chart: 3. Chi tiết phân loại theo từng lớp cảm xúc")

tab_m2, tab_m1, tab_visobert = st.tabs([
    "Mô hình 2 (Text + Lexicon 5.005D)",
    "Mô hình 1 (Text-only 5.000D)",
    "ViSoBERT Pretrained (GPU)",
])

with tab_m2:
    st.markdown("**Kết quả chi tiết Mô hình 2 trên Final Test (1.683 mẫu):**")
    m2_report = pd.DataFrame([
        {"Lớp cảm xúc": "Tiêu cực (Negative)", "Precision": "0.61", "Recall": "0.27", "F1-Score": "0.38", "Support": 114},
        {"Lớp cảm xúc": "Trung tính (Neutral)", "Precision": "0.51", "Recall": "0.32", "F1-Score": "0.39", "Support": 328},
        {"Lớp cảm xúc": "Tích cực (Positive)", "Precision": "0.83", "Recall": "0.95", "F1-Score": "0.88", "Support": 1241},
        {"Lớp cảm xúc": "Macro Average", "Precision": "0.65", "Recall": "0.51", "F1-Score": "0.55", "Support": 1683},
        {"Lớp cảm xúc": "Weighted Average", "Precision": "0.75", "Recall": "0.78", "F1-Score": "0.75", "Support": 1683},
    ])
    st.dataframe(m2_report, hide_index=True, use_container_width=True)
    st.caption("✨ Điểm nổi bật: F1 lớp Tiêu cực đạt 0.38 (tăng so với 0.35 của Text-only).")

with tab_m1:
    st.markdown("**Kết quả chi tiết Mô hình 1 trên Final Test (1.683 mẫu):**")
    m1_report = pd.DataFrame([
        {"Lớp cảm xúc": "Tiêu cực (Negative)", "Precision": "0.54", "Recall": "0.26", "F1-Score": "0.35", "Support": 114},
        {"Lớp cảm xúc": "Trung tính (Neutral)", "Precision": "0.49", "Recall": "0.35", "F1-Score": "0.41", "Support": 328},
        {"Lớp cảm xúc": "Tích cực (Positive)", "Precision": "0.83", "Recall": "0.94", "F1-Score": "0.88", "Support": 1241},
        {"Lớp cảm xúc": "Macro Average", "Precision": "0.62", "Recall": "0.52", "F1-Score": "0.55", "Support": 1683},
        {"Lớp cảm xúc": "Weighted Average", "Precision": "0.75", "Recall": "0.78", "F1-Score": "0.75", "Support": 1683},
    ])
    st.dataframe(m1_report, hide_index=True, use_container_width=True)
    st.caption("Mô hình Text-only ổn định ở lớp Positive (F1 0.88), nhưng Recall lớp Tiêu cực thấp hơn (26%).")

with tab_visobert:
    st.markdown("**Kết quả ViSoBERT Pretrained (5CD-AI) Zero-shot trên Final Test (1.683 mẫu):**")
    visobert_report = pd.DataFrame([
        {"Lớp cảm xúc": "Tiêu cực (Negative)", "Precision": "0.19", "Recall": "0.75", "F1-Score": "0.30", "Support": 114},
        {"Lớp cảm xúc": "Trung tính (Neutral)", "Precision": "0.39", "Recall": "0.05", "F1-Score": "0.09", "Support": 328},
        {"Lớp cảm xúc": "Tích cực (Positive)", "Precision": "0.84", "Recall": "0.80", "F1-Score": "0.82", "Support": 1241},
        {"Lớp cảm xúc": "Macro Average", "Precision": "0.47", "Recall": "0.53", "F1-Score": "0.40", "Support": 1683},
        {"Lớp cảm xúc": "Weighted Average", "Precision": "0.71", "Recall": "0.65", "F1-Score": "0.65", "Support": 1683},
    ])
    st.dataframe(visobert_report, hide_index=True, use_container_width=True)
    st.caption("ViSoBERT zero-shot bị sụp đổ ở lớp Neutral (Recall chỉ 5%), dẫn đến Macro F1 tụt xuống 0.4036.")

st.divider()

# ── 5. Phân tích Chuyên sâu & Đóng góp của Đề tài ─────────────────────────
st.subheader(":material/lightbulb: 4. Phân tích học thuật & Đóng góp của đề tài")

with st.expander("Tại sao Stacking Ensemble vượt trội hơn các mô hình đơn lẻ?", expanded=True, icon=":material/military_tech:"):
    st.markdown(
        """
        - **Phối hợp đa dạng giải thuật:** Stacking kết hợp 4 cơ chế học khác biệt:
          - *Multinomial Naive Bayes:* Bắt tần suất xác suất từ ngữ nhanh.
          - *Logistic Regression:* Tối ưu biên phân chia tuyến tính với trọng số `class_weight='balanced'`.
          - *Linear SVM:* Tìm siêu phẳng phân cách lề cực đại trong không gian 5.000 chiều.
          - *Random Forest:* Bắt các tương tác phi tuyến và cấu trúc cụm từ phức tạp.
        - **Meta-Classifier (Logistic Regression):** Đóng vai trò trọng tài, học trọng số tin cậy tối ưu từ dự đoán xác suất của các base models, khắc phục nhược điểm riêng lẻ của từng thuật toán.
        """
    )

with st.expander("Tác động của 5 đặc trưng Lexicon", icon=":material/psychology:"):
    st.markdown(
        """
        - **Khắc phục điểm yếu mất cân bằng dữ liệu:** Lớp Tiêu cực chỉ chiếm **6.8%** trong tập huấn luyện, khiến mô hình ML thuần TF-IDF dễ bỏ sót các sắc thái chê tinh vi.
        - **Giá trị của 5 đặc trưng Lexicon (`pos_w`, `neg_w`, `pos_e`, `neg_e`, `sentiment_ratio`):**
          - Khi được chuẩn hóa qua `MinMaxScaler` và ghép song song vào vector TF-IDF, các đặc trưng này cung cấp **tín hiệu định lượng rõ ràng** về mật độ từ khóa tiêu cực/phủ định.
          - Kết quả: **Recall lớp Tiêu cực tăng từ 26.3% lên 27.2%**, và **F1 lớp Tiêu cực tăng từ 0.35 lên 0.38 (+7.7%)**.
        """
    )

with st.expander("Tại sao Stacking Classifier vượt trội hơn ViSoBERT (Deep Learning)?", icon=":material/compare:"):
    st.markdown(
        """
        - **Bản chất của ViSoBERT:** ViSoBERT (*Vietnamese Social Media BERT*) được tiền huấn luyện trên ngữ liệu mạng xã hội tiếng Việt nói chung (Facebook, YouTube), với bộ từ vựng BPE hiểu rất tốt teencode, emoji và từ lóng.
        - **Lệch miền đặc thù & Thiếu Fine-tuning:** Checkpoint `5CD-AI/Vietnamese-Sentiment-visobert` được đánh giá ở chế độ **Zero-shot** (chưa fine-tune trên tập huấn luyện ITviec) với phân phối nhãn ban đầu khác biệt. Do đó, mô hình gần như bỏ qua lớp Trung tính (Recall Neutral chỉ đạt **4.88%**), dẫn đến việc gán nhầm ồ ạt sang Tiêu cực (Precision Negative tụt xuống **18.82%**, Macro F1 chỉ đạt **0.40**).
        - **Phân tích lỗi chuyên sâu — Sự xung đột tiền xử lý (Over-cleaning vs Transformer):**
          - Pipeline `clean_basic_text` được thiết kế theo **tư duy làm sạch cho Machine Learning truyền thống (TF-IDF)**: xóa toàn bộ dấu câu để giảm số chiều từ vựng, dịch teencode, chuẩn hóa thuật ngữ tiếng Anh (*IT* $\to$ *công nghệ thông tin*, *deal* $\to$ *thỏa thuận*), và ép emoji thành chữ tiếng Việt.
          - Cách làm sạch này rất có lợi cho không gian vector TF-IDF, nhưng lại **vô tình phá vỡ cơ chế Self-Attention** (mất dấu chấm phẩy phân tách ranh giới câu khen/chê) và **lãng phí bộ từ vựng BPE nguyên bản của ViSoBERT** (vốn có sẵn token riêng cho Emoji và hiểu rất tốt teencode tự nhiên).
          - Để giải quyết triệt để rào cản này, nhóm đã xây dựng phương thức chuyên biệt `clean_text_for_transformer()` trong `src/preprocessing.py` (bảo toàn dấu câu, giữ nguyên emoji tự nhiên, giữ nguyên ngôn ngữ mạng xã hội gốc và chỉ lọc URL/Email cùng rút gọn ký tự kéo dài) làm tiền đề chuẩn mực cho các thử nghiệm Fine-tuning tiếp theo.
        - **Ưu thế của Pipeline Học máy / Stacking chuyên biệt:** Mô hình Stacking được huấn luyện có giám sát (supervised) trực tiếp trên tập dữ liệu ITviec, kết hợp bộ tiền xử lý chuyên sâu và các đặc trưng từ điển cảm xúc miền công nghệ, giúp phân định ranh giới giữa 3 lớp cảm xúc một cách tối ưu.
        """
    )
