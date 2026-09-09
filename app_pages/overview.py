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


st.title("Hiểu tiếng nói nhân sự qua từng review")
st.caption(
    "Không gian trực quan để khám phá cảm xúc, tìm insight doanh nghiệp "
    "và trải nghiệm mô hình NLP text-only."
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

with st.container(horizontal=True, gap="xsmall"):
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

left, right = st.columns([1.35, 1], gap="large")
with left:
    with st.container(border=True, height="stretch", key="overview_sentiment_panel"):
        st.subheader(":material/donut_large: Bức tranh cảm xúc")
        st.caption("Nhãn yếu được suy ra từ rating do người viết review cung cấp.")
        chart = (
            alt.Chart(summary)
            .mark_bar(cornerRadiusTopLeft=7, cornerRadiusTopRight=7)
            .encode(
                x=alt.X("label:N", title=None, sort=["Tích cực", "Trung tính", "Tiêu cực"]),
                y=alt.Y("reviews:Q", title="Số review"),
                color=alt.Color(
                    "sentiment:N",
                    scale=alt.Scale(domain=["Positive", "Neutral", "Negative"]),
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
        st.altair_chart(chart, width="stretch")

with right:
    with st.container(border=True, height="stretch", key="overview_journey_panel"):
        st.subheader(":material/route: Từ dữ liệu đến quyết định")
        st.markdown(
            """
            **01 · Khám phá**

            Lọc theo doanh nghiệp, so sánh tỷ lệ cảm xúc và từ khóa nổi bật.

            **02 · Thấu hiểu**

            Đọc review thật để nhận diện điểm mạnh và vấn đề cần cải thiện.

            **03 · Trải nghiệm**

            Nhập review mới để mô hình Stacking Ensemble kết hợp Hybrid Lexicon phân tích thời gian thực.
            """
        )
        with st.container(key="kpi_negative"):
            st.metric(
                "Review tiêu cực cần ưu tiên phân tích",
                f"{negative_share:.1f}%",
                icon=":material/priority_high:",
                border=True,
            )

st.subheader("Ba lớp của sản phẩm")
with st.container(horizontal=True):
    with st.container(border=True, key="product_data_card"):
        st.markdown("#### :material/database: Dữ liệu thật")
        st.write("Review đã làm sạch, gán nhãn và giữ nguyên ngữ cảnh doanh nghiệp.")
    with st.container(border=True, key="product_insight_card"):
        st.markdown("#### :material/monitoring: Insight trực quan")
        st.write("KPI, xu hướng theo thời gian, từ khóa và review chi tiết trong một dashboard.")
    with st.container(border=True, key="product_model_card"):
        st.markdown("#### :material/model_training: NLP text-only")
        st.write("Pipeline được thiết kế để chỉ dùng nội dung review khi suy luận.")

st.info(
    status.message
    if not status.ready
    else f"Model đang sẵn sàng: {status.model_path.name}",
    icon=":material/info:",
)
