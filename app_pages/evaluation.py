"""Read-only experimental evidence; the threshold explorer never changes inference."""

import hashlib
import json
from pathlib import Path
import sys

import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app_services import NEGATIVE_THRESHOLD, SENTIMENT_LABELS
from src.app_theme import page_header, style_chart

ARTIFACTS = PROJECT_ROOT / "reports" / "evaluation"


@st.cache_data(max_entries=2, show_spinner=False)
def load_evidence(signature):
    snapshot = json.loads((ARTIFACTS / "evaluation_snapshot.json").read_text(encoding="utf-8"))
    comparison = pd.read_csv(ARTIFACTS / "baseline_vs_negative_threshold.csv")
    sensitivity = pd.read_csv(ARTIFACTS / "negative_threshold_sensitivity.csv")
    errors = pd.read_csv(ARTIFACTS / "error_analysis_15_samples.csv")
    model = PROJECT_ROOT / "models" / "best_sentiment_model.joblib"
    matches = model.exists() and hashlib.sha256(model.read_bytes()).hexdigest() == snapshot["model_sha256"]
    return snapshot, comparison, sensitivity, errors, matches


page_header(
    "BẰNG CHỨNG THỰC NGHIỆM", "Mô hình tốt đến đâu?",
    "Đi từ số liệu tổng thể đến từng lỗi dự đoán. Hiểu được đánh đổi cũng là một phần của hiểu mô hình.",
)
try:
    sources = [
        ARTIFACTS / name for name in [
            "evaluation_snapshot.json", "baseline_vs_negative_threshold.csv",
            "negative_threshold_sensitivity.csv", "error_analysis_15_samples.csv",
        ]
    ]
    sources.append(PROJECT_ROOT / "models" / "best_sentiment_model.joblib")
    signature = tuple((str(p), p.stat().st_mtime_ns, p.stat().st_size) for p in sources)
    snapshot, comparison, sensitivity, errors, model_matches = load_evidence(signature)
except (OSError, ValueError, KeyError) as exc:
    st.warning("Chưa có đủ kết quả thực nghiệm. Chạy notebook 06 để tạo bộ dữ liệu evaluation.")
    st.caption(str(exc))
    st.stop()

baseline, policy = comparison.iloc[0], comparison.iloc[1]
with st.container(horizontal=True, gap="small"):
    st.badge("Stacking · bộ test đã khóa", color="blue", icon=":material/science:")
    st.badge(f"{snapshot['test_count']:,} mẫu", color="gray")
    st.badge("Kết quả từ notebook 06", color="gray", icon=":material/book:")
if not model_matches or not np.isclose(snapshot["threshold"], NEGATIVE_THRESHOLD):
    st.warning("Model hoặc policy hiện tại khác bản đã đánh giá. Các số liệu dưới đây thuộc snapshot notebook 06.")

with st.container(horizontal=True, key="evaluation_metrics", gap="small"):
    for title, column, fmt in [
        ("Macro F1", "Macro F1", ".4f"), ("Accuracy", "Accuracy", ".1%"),
        ("Recall tiêu cực", "Negative Recall", ".1%"), ("Precision tiêu cực", "Negative Precision", ".1%"),
    ]:
        change = float(policy[column] - baseline[column])
        st.metric(title, format(policy[column], fmt),
                  delta=f"{change:+.4f}" if fmt == ".4f" else f"{change * 100:+.2f} điểm %",
                  border=True, help="Policy 30%, thay đổi so với dự đoán mặc định của model.")
st.caption("Số liệu trên là policy 30% so với baseline. Đây là phân tích bổ sung trên final test đã được xem trước, chưa phải xác nhận độc lập cho ngưỡng mới.")

with st.container(key="evaluation_chart_row"):
    matrix_col, tradeoff_col = st.columns([1.1, 1], gap="medium")
with matrix_col.container(border=True, height="stretch", key="evaluation_matrix"):
    st.caption("01 / MA TRẬN NHẦM LẪN")
    st.subheader("Model thường nhầm ở đâu?")
    mode = st.segmented_control("Kết quả hiển thị", ["Baseline", "Ngưỡng 30%"], default="Ngưỡng 30%", key="matrix_mode")
    matrix = np.asarray(snapshot["baseline_matrix"] if mode == "Baseline" else snapshot["policy_matrix"])
    labels = snapshot["labels"]
    rows = [
        {"actual": SENTIMENT_LABELS[a], "predicted": SENTIMENT_LABELS[b],
         "count": int(matrix[i, j]), "share": float(matrix[i, j] / matrix[i].sum())}
        for i, a in enumerate(labels) for j, b in enumerate(labels)
    ]
    order = [SENTIMENT_LABELS[label] for label in labels]
    heat = alt.Chart(pd.DataFrame(rows)).encode(
        x=alt.X("predicted:N", title="Dự đoán", sort=order, axis=alt.Axis(labelAngle=0)),
        y=alt.Y("actual:N", title="Nhãn từ rating", sort=order),
        tooltip=[alt.Tooltip("actual:N", title="Nhãn từ rating"),
                 alt.Tooltip("predicted:N", title="Dự đoán"), alt.Tooltip("count:Q", title="Số review"),
                 alt.Tooltip("share:Q", title="Tỷ lệ trong lớp thật", format=".1%")],
    )
    tiles = heat.mark_rect(cornerRadius=7, stroke="#0c1119", strokeWidth=5).encode(
        color=alt.Color("share:Q", scale=alt.Scale(domain=[0, 1], range=["#141f32", "#527bd1"]), legend=None))
    values = heat.mark_text(color="#f1f5f9", font="JetBrains Mono", fontSize=18).encode(text="count:Q")
    st.altair_chart(style_chart((tiles + values).properties(height=245)), width="stretch", theme=None)
    st.caption("Mỗi hàng là một lớp thật. Màu theo tỷ lệ trong hàng giúp thấy lỗi lớp ít mẫu; số trong ô là số review.")

with tradeoff_col.container(border=True, height="stretch", key="evaluation_tradeoff"):
    st.caption("02 / ĐÁNH ĐỔI KHI HẠ NGƯỠNG")
    st.subheader("Bắt được nhiều hơn, báo nhầm nhiều hơn")
    base_matrix = np.asarray(snapshot["baseline_matrix"])
    policy_matrix = np.asarray(snapshot["policy_matrix"])
    ni = snapshot["labels"].index("Negative")
    recovered = int(policy_matrix[ni, ni] - base_matrix[ni, ni])
    added_fp = int((policy_matrix[:, ni].sum() - policy_matrix[ni, ni]) - (base_matrix[:, ni].sum() - base_matrix[ni, ni]))
    with st.container(horizontal=True, key="tradeoff_metrics"):
        st.metric("Tiêu cực nhận đúng thêm", f"+{recovered}")
        st.metric("Báo nhầm tiêu cực thêm", f"+{added_fp}")
    st.write(f"Ở ngưỡng **30%**, Recall tiêu cực đạt **{policy['Negative Recall']:.1%}**; Precision còn **{policy['Negative Precision']:.1%}**.")
    st.caption("Recall: tìm được bao nhiêu review tiêu cực thực sự. Precision: trong các review bị gắn nhãn tiêu cực, bao nhiêu review đúng theo nhãn rating.")
    st.badge("Chưa đạt mục tiêu Recall 55–60%", color="orange", icon=":material/info:")
    st.caption("Threshold là quy tắc chọn nhãn sau model. Trọng số mô hình và TF-IDF được giữ nguyên.")

with st.container(border=True, key="evaluation_sensitivity"):
    st.caption("03 / KHÁM PHÁ NGƯỠNG")
    st.subheader("Điều gì xảy ra khi thay đổi ngưỡng?")
    threshold = st.select_slider("Ngưỡng đang khảo sát", options=sensitivity["Threshold"].tolist(),
                                 value=0.30, key="evaluation_threshold")
    selected = sensitivity.loc[np.isclose(sensitivity["Threshold"], threshold)].iloc[0]
    chart_data = sensitivity.rename(columns={"Negative Recall": "Recall tiêu cực", "Negative Precision": "Precision tiêu cực", "Macro F1": "Macro F1"}).melt(
        id_vars=["Threshold"], value_vars=["Recall tiêu cực", "Precision tiêu cực", "Macro F1"],
        var_name="metric", value_name="value")
    lines = alt.Chart(chart_data).mark_line(point=True, strokeWidth=2).encode(
        x=alt.X("Threshold:Q", title="Ngưỡng tiêu cực", axis=alt.Axis(format=".0%")),
        y=alt.Y("value:Q", title=None, scale=alt.Scale(domain=[0, 1]), axis=alt.Axis(format=".0%")),
        color=alt.Color("metric:N", title=None, scale=alt.Scale(
            domain=["Recall tiêu cực", "Precision tiêu cực", "Macro F1"],
            range=["#50e3a4", "#ff994f", "#7aa7ff"]), legend=alt.Legend(orient="bottom")),
        tooltip=[alt.Tooltip("Threshold:Q", title="Ngưỡng", format=".0%"),
                 alt.Tooltip("metric:N", title="Chỉ số"), alt.Tooltip("value:Q", title="Giá trị", format=".2%")])
    marker = alt.Chart(pd.DataFrame({"Threshold": [threshold]})).mark_rule(
        strokeDash=[4, 4], color="#cdd8e8").encode(x="Threshold:Q")
    st.altair_chart(style_chart((lines + marker).properties(height=240)), width="stretch", theme=None)
    st.caption(f"Ngưỡng {threshold:.0%} · Recall {selected['Negative Recall']:.2%} · Precision {selected['Negative Precision']:.2%} · Macro F1 {selected['Macro F1']:.4f}")
    st.caption("Chỉ khám phá số liệu đã xuất; thao tác này không thay đổi policy Web Demo. Chọn ngưỡng chính thức cần validation/OOF riêng.")

with st.container(border=True, key="evaluation_errors"):
    st.caption("04 / ERROR ANALYSIS")
    st.subheader("Đọc một lỗi thật, hiểu một giới hạn")
    pairs = errors["Cặp nhầm"].unique().tolist()
    pair = st.selectbox("Kiểu nhầm lẫn", pairs,
        format_func=lambda value: " → ".join(SENTIMENT_LABELS.get(part, part) for part in value.split(" → ")))
    subset = errors[errors["Cặp nhầm"] == pair]
    index = st.selectbox("Review cần xem", subset.index.tolist(),
        format_func=lambda i: f"#{int(errors.loc[i, 'source_index'])} · {errors.loc[i, 'Company Name']} · {int(errors.loc[i, 'Rating'])} sao")
    row = errors.loc[index]
    with st.container(horizontal=True):
        st.badge(f"Nhãn từ rating: {SENTIMENT_LABELS[row['Nhãn thật']]}", color="gray")
        st.badge(f"Model: {SENTIMENT_LABELS[row['Threshold 0.30']]}", color="orange")
        st.badge(f"P(Tiêu cực): {row['P(Negative)']:.1%}", color="gray")
    with st.container(height=190, border=True):
        st.text(row["raw_review_text"])
    st.caption(f"Tín hiệu gợi ý để đọc lỗi: {row['Nhóm tín hiệu']}. Đây là heuristic, chưa phải nguyên nhân đã được kiểm chứng.")
    st.caption("15 ví dụ được chọn để thảo luận lỗi, không đại diện cho tần suất lỗi toàn bộ test. Review có nhiều chủ đề; nhãn từ rating có thể khác sắc thái văn bản.")

with st.expander("Nguồn kết quả và cách tái lập", icon=":material/verified:"):
    st.write("Nguồn: notebook 06, feature split đã khóa và các CSV trong reports/evaluation/.")
    st.code(".venv311/Scripts/jupyter nbconvert --to notebook --execute --inplace notebooks/06_model_evaluation_error_analysis.ipynb", language="text", wrap_lines=True)
    st.caption(f"SHA-256 model được đánh giá: {snapshot['model_sha256']}")
    st.caption("Đánh giá dùng X_test đã lưu; demo nhập review chạy preprocessing hiện tại. Hai đường vào cần được kiểm chứng tương đương trước khi khẳng định metric trên test áp dụng trực tiếp cho mọi input web.")
