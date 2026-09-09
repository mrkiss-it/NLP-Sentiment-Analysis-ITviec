"""Entrypoint for the ITviec sentiment analysis Streamlit application."""

import streamlit as st

from src.app_theme import apply_app_style


st.set_page_config(
    page_title="ITviec Sentiment Lab",
    page_icon="assets/sentiment-lab-mark.svg",
    layout="wide",
    initial_sidebar_state="expanded",
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
    "Trải nghiệm": [
        st.Page(
            "app_pages/predict.py",
            title="Phân tích review",
            icon=":material/chat:",
        ),
    ],
}

with st.sidebar:
    st.caption("Phân tích cảm xúc review ngành công nghệ trên ITviec.")

current_page = st.navigation(pages, position="sidebar", expanded=True)

with st.sidebar:
    st.badge("Dữ liệu thật", icon=":material/database:", color="green")
    st.caption("8.417 review · 180 doanh nghiệp · 3 nhóm cảm xúc")

current_page.run()
