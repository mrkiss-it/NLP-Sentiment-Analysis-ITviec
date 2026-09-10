"""Entrypoint for the ITviec sentiment analysis Streamlit application."""

import streamlit as st

from src.app_cache import get_reviews
from src.app_services import get_model_status
from src.app_theme import apply_app_style


st.set_page_config(
    page_title="ITviec Sentiment Lab",
    page_icon="assets/sentiment-lab-mark.svg",
    layout="wide",
    initial_sidebar_state="auto",
)
st.logo(
    "assets/sentiment-lab-logo.svg",
    icon_image="assets/sentiment-lab-mark.svg",
    size="large",
)
apply_app_style()

pages = {
    "Khám phá": [
        st.Page(
            "app_pages/overview.py",
            title="Tổng quan",
            icon=":material/home:",
            default=True,
        ),
        st.Page(
            "app_pages/insights.py",
            title="Insight doanh nghiệp",
            icon=":material/domain:",
        ),
        st.Page(
            "app_pages/benchmark.py",
            title="Hiệu năng & Benchmark",
            icon=":material/leaderboard:",
        ),
    ],
    "Phòng lab NLP": [
        st.Page(
            "app_pages/predict.py",
            title="Phân tích review",
            icon=":material/chat:",
        ),
        st.Page("app_pages/evaluation.py", title="Đánh giá mô hình", icon=":material/science:"),
    ],
}

current_page = st.navigation(pages, position="sidebar", expanded=True)

with st.sidebar:
    try:
        sidebar_reviews = get_reviews()
        review_count = len(sidebar_reviews)
        company_count = sidebar_reviews["Company Name"].nunique()
    except (FileNotFoundError, ValueError):
        review_count = 0
        company_count = 0

    model_status = get_model_status()
    with st.container(border=True, key="sidebar_status_card", gap="small"):
        st.caption("WORKSPACE / IT REVIEWS")
        st.markdown("**Dữ liệu phân tích**")
        stat_left, stat_right = st.columns(2, gap="small")
        stat_left.metric("Review", f"{review_count:,}" if review_count else "—")
        stat_right.metric("Công ty", f"{company_count:,}" if company_count else "—")
        with st.container(horizontal=True, gap="small", key="sidebar_badges"):
            st.badge("Dữ liệu thật", icon=":material/database:", color="green")
            st.badge(
                "Model cục bộ" if model_status.ready else "Model đang chờ",
                icon=":material/model_training:",
                color="green" if model_status.ready else "orange",
            )

    st.caption("NLP Sentiment Analysis · ITviec")

current_page.run()
