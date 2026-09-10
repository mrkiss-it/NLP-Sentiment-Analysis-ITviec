"""Overview page for the ITviec sentiment analysis project."""

from pathlib import Path
import sys

import altair as alt
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app_cache import get_reviews
from src.app_services import get_model_status, sentiment_summary
from src.app_theme import page_header, style_chart


page_header(
    "TỔNG QUAN",
    "Hiểu tiếng nói nhân sự qua từng review",
    "Khám phá cảm xúc từ review ngành công nghệ. Từ bức tranh tổng thể "
    "đến câu chuyện của từng doanh nghiệp.",
)

status = get_model_status()
with st.container(horizontal=True, vertical_alignment="center"):
    st.badge("Dashboard sẵn sàng", icon=":material/check_circle:", color="green")
    if status.ready:
        st.badge("Model sẵn sàng", icon=":material/model_training:", color="green")
    else:
        st.badge("Model đang chờ", icon=":material/schedule:", color="orange")

try:
    reviews = get_reviews()
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc), icon=":material/error:")
    st.stop()

summary = sentiment_summary(reviews)
positive_share = float(summary.loc[summary["sentiment"] == "Positive", "share"].iloc[0])
negative_share = float(summary.loc[summary["sentiment"] == "Negative", "share"].iloc[0])
average_rating = float(reviews["Rating"].mean())

with st.container(horizontal=True, gap="small", key="overview_metrics"):
    with st.container(key="kpi_reviews"):
        st.metric(
            "Tổng review",
            f"{len(reviews):,}",
            icon=":material/rate_review:",
            border=True,
        )
    with st.container(key="kpi_companies"):
        st.metric(
            "Doanh nghiệp",
            f"{reviews['Company Name'].nunique():,}",
            icon=":material/domain:",
            border=True,
        )
    with st.container(key="kpi_positive"):
        st.metric(
            "Tỷ lệ tích cực",
            f"{positive_share:.1f}%",
            icon=":material/sentiment_satisfied:",
            border=True,
        )
    with st.container(key="kpi_rating"):
        st.metric(
            "Điểm trung bình",
            f"{average_rating:.2f}/5",
            icon=":material/star:",
            border=True,
        )

with st.container(key="overview_chart_row"):
    left, right = st.columns([1.5, 1], gap="medium")
with left:
    with st.container(border=True, height="stretch", key="overview_sentiment_panel"):
        st.subheader(":material/donut_large: Bức tranh cảm xúc")
        st.caption("Nhãn yếu được suy ra từ rating do người viết review cung cấp.")
        chart = (
            alt.Chart(summary)
            .mark_bar(cornerRadiusTopLeft=7, cornerRadiusTopRight=7)
            .encode(
                x=alt.X("label:N", title=None, sort=["Tích cực", "Trung tính", "Tiêu cực"], axis=alt.Axis(labelAngle=0)),
                y=alt.Y("reviews:Q", title="Số review"),
                color=alt.Color(
                    "sentiment:N",
                    scale=alt.Scale(domain=["Positive", "Neutral", "Negative"], range=["#50e3a4", "#f4d35e", "#ff6677"]),
                    legend=None,
                ),
                tooltip=[
                    alt.Tooltip("label:N", title="Cảm xúc"),
                    alt.Tooltip("reviews:Q", title="Review", format=","),
                    alt.Tooltip("share:Q", title="Tỷ lệ", format=".1f"),
                ],
            )
            .properties(height=310)
        )
        labels = chart.mark_text(dy=-12, color="#e2e8f0", font="JetBrains Mono", fontSize=13).encode(
            text=alt.Text("reviews:Q", format=","), color=alt.value("#e2e8f0")
        )
        st.altair_chart(style_chart(chart + labels), width="stretch", theme=None)

with right:
    with st.container(border=True, height="stretch", key="overview_journey_panel"):
        st.subheader(":material/manage_search: Điểm cần chú ý")
        st.caption("Bắt đầu từ những phản hồi cần được lắng nghe.")
        with st.container(key="kpi_negative"):
            st.metric(
                "Tỷ lệ review tiêu cực",
                f"{negative_share:.1f}%",
                icon=":material/priority_high:",
                border=True,
            )
        negative_count = int(summary.loc[summary["sentiment"] == "Negative", "reviews"].iloc[0])
        st.write(
            f"**{negative_count:,} review tiêu cực** trong tập dữ liệu. "
            "Đọc nội dung cụ thể để tìm hiểu vấn đề về môi trường, quản lý và phúc lợi."
        )
        st.caption("Tỷ lệ phản ánh mẫu review hiện có, không phải toàn bộ nhân sự doanh nghiệp.")
        st.page_link("app_pages/insights.py", label="Khám phá insight doanh nghiệp", icon=":material/arrow_forward:")

st.subheader("Bạn muốn khám phá điều gì?")
with st.container(horizontal=True, key="product_actions"):
    with st.container(border=True, height="stretch", key="product_insight_card"):
        st.markdown("#### :material/domain: Thấu hiểu doanh nghiệp")
        st.write("Chọn công ty, xem tỷ lệ cảm xúc, khám phá WordCloud và đọc review thực tế.")
        st.page_link("app_pages/insights.py", label="Mở dashboard insight", icon=":material/arrow_forward:")
    with st.container(border=True, height="stretch", key="product_model_card"):
        st.markdown("#### :material/auto_awesome: Phân tích một review")
        st.write("Nhập phản hồi của bạn và xem mô hình nhận diện cảm xúc từ nội dung văn bản.")
        st.page_link("app_pages/predict.py", label="Thử phân tích cảm xúc", icon=":material/arrow_forward:")
    with st.container(border=True, height="stretch", key="product_evaluation_card"):
        st.markdown("#### :material/science: Kiểm chứng mô hình")
        st.write("Đọc ma trận nhầm lẫn, khám phá ngưỡng và phân tích những review model còn nhầm.")
        st.page_link("app_pages/evaluation.py", label="Xem kết quả thực nghiệm", icon=":material/arrow_forward:")

if not status.ready:
    st.info(status.message, icon=":material/info:")
