"""Interactive company sentiment dashboard backed by cleaned ITviec reviews."""

from io import BytesIO
from pathlib import Path
import sys

import altair as alt
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.app_cache import get_reviews
from src.app_review_explorer import render_review_explorer
from src.app_theme import page_header, style_chart
from src.app_services import (
    SENTIMENT_LABELS,
    SENTIMENT_ORDER,
    company_summary,
    monthly_sentiment,
    sentiment_summary,
    top_terms,
)


@st.cache_data(max_entries=48, show_spinner="Đang tạo bản đồ từ khóa...")
def make_wordcloud(text: str, sentiment: str) -> bytes:
    from wordcloud import WordCloud
    from matplotlib.colors import LinearSegmentedColormap

    background_color = "#0b1018"
    palette = ["#55bfa4", "#50e3a4", "#a7eedb"] if sentiment == "Positive" else ["#dd7585", "#ff6677", "#ffc0a5"]
    color_map = LinearSegmentedColormap.from_list("sentiment_lab", palette)
    image = WordCloud(
        width=1200,
        height=600,
        background_color=background_color,
        max_words=80,
        colormap=color_map,
        collocations=False,
        random_state=2026,
        prefer_horizontal=1.0,
        relative_scaling=0.25,
        margin=10,
    ).generate(text)
    buffer = BytesIO()
    image.to_image().save(buffer, format="PNG")
    return buffer.getvalue()


page_header("DOANH NGHIỆP", "Insight cảm xúc doanh nghiệp",
    "Khám phá xu hướng, từ khóa và review thật. Bộ lọc ngưỡng mẫu giúp tránh "
    "so sánh doanh nghiệp có quá ít dữ liệu."
)

try:
    reviews = get_reviews()
except (FileNotFoundError, ValueError) as exc:
    st.error(str(exc), icon=":material/error:")
    st.stop()

with st.container(border=True, key="insight_filter_panel"):
    st.markdown("**:material/tune: Bộ lọc phân tích**")
    company_filter, sample_filter = st.columns([1.4, 1], gap="medium", vertical_alignment="bottom")
    min_reviews = sample_filter.segmented_control(
        "Ngưỡng mẫu tối thiểu",
        options=[30, 50, 100, 200],
        default=50,
        format_func=lambda value: f"{value}+",
        key="minimum_reviews",
    )
    threshold = int(min_reviews or 50)
    companies = company_summary(reviews, min_reviews=threshold)
    company_options = ["Toàn bộ dữ liệu", *companies["Company Name"].tolist()]
    selected_company = company_filter.selectbox(
        "Doanh nghiệp",
        options=company_options,
        key="selected_company",
        help="Chỉ các doanh nghiệp đạt ngưỡng mẫu mới xuất hiện.",
    )

selected_reviews = (
    reviews
    if selected_company == "Toàn bộ dữ liệu"
    else reviews[reviews["Company Name"] == selected_company]
)
summary = sentiment_summary(selected_reviews)
positive_share = float(summary.loc[summary["sentiment"] == "Positive", "share"].iloc[0])
neutral_share = float(summary.loc[summary["sentiment"] == "Neutral", "share"].iloc[0])
negative_share = float(summary.loc[summary["sentiment"] == "Negative", "share"].iloc[0])

st.caption(f"Đang xem: {selected_company} · {len(selected_reviews):,} review")
with st.container(horizontal=True, gap="small", key="insight_metrics"):
    with st.container(key="kpi_reviews"):
        st.metric("Review", f"{len(selected_reviews):,}", icon=":material/rate_review:", border=True)
    with st.container(key="kpi_positive"):
        st.metric("Tích cực", f"{positive_share:.1f}%", icon=":material/sentiment_satisfied:", border=True)
    with st.container(key="kpi_neutral"):
        st.metric("Trung tính", f"{neutral_share:.1f}%", icon=":material/sentiment_neutral:", border=True)
    with st.container(key="kpi_negative"):
        st.metric("Tiêu cực", f"{negative_share:.1f}%", icon=":material/sentiment_dissatisfied:", border=True)
    with st.container(key="kpi_rating"):
        st.metric("Rating TB", f"{selected_reviews['Rating'].mean():.2f}/5", icon=":material/star:", border=True)

with st.container(key="insight_chart_row"):
    left, right = st.columns([0.9, 1.4], gap="medium")
with left:
    with st.container(border=True, height="stretch", key="insight_donut_panel"):
        st.subheader(":material/donut_large: Cơ cấu cảm xúc")
        donut = (
            alt.Chart(summary)
            .mark_arc(innerRadius=68, outerRadius=118, cornerRadius=5)
            .encode(
                theta=alt.Theta("reviews:Q"),
                color=alt.Color(
                    "label:N",
                    scale=alt.Scale(domain=[SENTIMENT_LABELS[s] for s in SENTIMENT_ORDER], range=["#50e3a4", "#f4d35e", "#ff6677"]),
                    legend=alt.Legend(title=None, orient="bottom"),
                ),
                tooltip=[
                    alt.Tooltip("label:N", title="Cảm xúc"),
                    alt.Tooltip("reviews:Q", title="Review", format=","),
                    alt.Tooltip("share:Q", title="Tỷ lệ", format=".1f"),
                ],
            )
            .properties(height=330)
        )
        center = alt.Chart(alt.Data(values=[{"reviews": len(selected_reviews)}]))
        count_label = center.mark_text(
            font="JetBrains Mono", fontSize=26, fontWeight=500,
            color="#f1f5f9", dy=-8,
        ).encode(text=alt.Text("reviews:Q", format=","))
        unit_label = center.mark_text(
            font="DM Sans", fontSize=13, color="#a0adbf", dy=19,
        ).encode(text=alt.value("review"))
        st.altair_chart(style_chart(donut + count_label + unit_label), width="stretch", theme=None)

with right:
    with st.container(border=True, height="stretch", key="insight_trend_panel"):
        st.subheader(":material/timeline: Xu hướng theo thời gian")
        trend = monthly_sentiment(selected_reviews)
        trend["label"] = trend["sentiment"].map(SENTIMENT_LABELS) if "sentiment" in trend else None
        if trend.empty:
            st.info("Không đủ dữ liệu thời gian để vẽ xu hướng.", icon=":material/info:")
        else:
            line = (
                alt.Chart(trend)
                .mark_line(point=True, strokeWidth=2.5)
                .encode(
                    x=alt.X("review_month:T", title=None, axis=alt.Axis(format="%m/%Y")),
                    y=alt.Y("reviews:Q", title="Số review"),
                    color=alt.Color(
                        "label:N",
                        scale=alt.Scale(domain=[SENTIMENT_LABELS[s] for s in SENTIMENT_ORDER], range=["#50e3a4", "#f4d35e", "#ff6677"]),
                        legend=alt.Legend(title="Cảm xúc", orient="bottom"),
                    ),
                    tooltip=[
                        alt.Tooltip("yearmonth(review_month):T", title="Tháng"),
                        alt.Tooltip("label:N", title="Cảm xúc"),
                        alt.Tooltip("reviews:Q", title="Review"),
                    ],
                )
                .properties(height=330)
                .interactive()
            )
            st.altair_chart(style_chart(line), width="stretch", theme=None)

st.subheader("Bản đồ từ khóa")
st.caption(
    "Nhìn nhanh những chủ đề xuất hiện thường xuyên trong nhóm review đang chọn. "
    "Kích thước thể hiện tần suất, không đại diện cho mức độ quan trọng."
)
with st.container(border=True, key="language_workspace"):
    context_col, control_col = st.columns(
        [1.5, 0.8], gap="medium", vertical_alignment="bottom"
    )
    tone = control_col.segmented_control(
        "Góc nhìn cảm xúc",
        options=["Positive", "Negative"],
        default="Positive",
        format_func=lambda value: "Tích cực" if value == "Positive" else "Tiêu cực",
        key="wordcloud_tone",
        width="stretch",
    )
    selected_tone = tone or "Positive"
    tone_reviews = selected_reviews[
        selected_reviews["sentiment"] == selected_tone
    ]
    tone_label = "Tích cực" if selected_tone == "Positive" else "Tiêu cực"
    tone_share = len(tone_reviews) / len(selected_reviews) * 100 if len(selected_reviews) else 0
    context_col.caption("PHẠM VI PHÂN TÍCH")
    context_col.markdown(
        f"#### :material/domain: {selected_company}"
    )
    context_col.caption(
        f"{len(tone_reviews):,} review {tone_label.lower()} · "
        f"{tone_share:.1f}% dữ liệu đang xem"
    )
    clean_text = " ".join(
        tone_reviews["clean_advance_text"].dropna().astype(str)
    )
    terms = top_terms(tone_reviews["clean_advance_text"], limit=15)
    top_term = terms.iloc[0]["term"] if not terms.empty else "—"
    top_term_label = str(top_term).replace("_", " ")
    token_count = sum(
        len(str(text).split())
        for text in tone_reviews["clean_advance_text"].dropna()
    )

    with st.container(horizontal=True, gap="small", key="wordcloud_metrics"):
        st.metric("Review được phân tích", f"{len(tone_reviews):,}", border=True)
        st.metric("Lượt xuất hiện từ", f"{token_count:,}", border=True)
        st.metric("Từ khóa dẫn đầu", top_term_label, border=True)

    with st.container(key="language_charts"):
        cloud_col, terms_col = st.columns([1.55, 0.8], gap="medium")
    with cloud_col:
        with st.container(border=True, height="stretch", key="wordcloud_panel"):
            st.markdown(f"#### :material/cloud: WordCloud {tone_label.lower()}")
            st.caption("Từ xuất hiện nhiều hơn sẽ có kích thước lớn hơn.")
            if clean_text.strip():
                cloud_bytes = make_wordcloud(clean_text, selected_tone)
                st.image(
                    cloud_bytes,
                    width="stretch",
                )
                st.caption(
                    "Dấu _ giúp giữ nguyên ý nghĩa của các cụm từ ghép trong ảnh."
                )
            else:
                st.info(
                    "Không có nội dung phù hợp để tạo WordCloud.",
                    icon=":material/info:",
                )

    with terms_col:
        with st.container(border=True, height="stretch", key="terms_panel"):
            st.markdown("#### :material/leaderboard: Từ khóa thường gặp")
            st.caption("15 cụm từ có tần suất xuất hiện cao nhất.")
            if terms.empty:
                st.caption("Chưa có từ khóa.")
            else:
                terms = terms.assign(
                    sentiment=selected_tone,
                    term_label=terms["term"].astype(str).str.replace(
                        "_", " ", regex=False
                    ),
                )
                term_chart = (
                    alt.Chart(terms)
                    .mark_bar(cornerRadiusEnd=7)
                    .encode(
                        x=alt.X(
                            "count:Q", title="Lượt xuất hiện",
                            scale=alt.Scale(domain=[0, float(terms["count"].max()) * 1.24]),
                            axis=alt.Axis(tickCount=4, format="~s"),
                        ),
                        y=alt.Y(
                            "term_label:N", title=None, sort=terms["term_label"].tolist(),
                            scale=alt.Scale(paddingInner=0.35, paddingOuter=0.18),
                        ),
                        color=alt.Color(
                            "sentiment:N",
                            scale=alt.Scale(
                                domain=list(SENTIMENT_ORDER),
                                range=["#50e3a4", "#f4d35e", "#ff6677"],
                            ),
                            legend=None,
                        ),
                        tooltip=[
                            alt.Tooltip("term_label:N", title="Từ khóa"),
                            alt.Tooltip("count:Q", title="Số lần", format=","),
                        ],
                    )
                    .properties(height=360)
                )
                term_counts = term_chart.mark_text(
                    align="left", dx=6, font="JetBrains Mono", fontSize=11,
                ).encode(text=alt.Text("count:Q", format=","), color=alt.value("#cbd5e1"))
                st.altair_chart(
                    style_chart(term_chart + term_counts),
                    width="stretch", height="stretch", theme=None, key="terms_chart",
                )

render_review_explorer(selected_reviews, selected_company)

st.subheader("So sánh doanh nghiệp đủ ngưỡng mẫu")
with st.container(border=True, key="company_table_panel"):
    st.caption(
        f"Có {len(companies)} doanh nghiệp đạt ngưỡng {threshold}+ review. "
        "Bảng được sắp xếp theo quy mô mẫu, không phải bảng xếp hạng nơi làm việc."
    )
    display_companies = companies.rename(
        columns={
            "Company Name": "Doanh nghiệp",
            "reviews": "Số review",
            "average_rating": "Rating TB",
            "positive_share": "Tích cực",
            "neutral_share": "Trung tính",
            "negative_share": "Tiêu cực",
        }
    )[
        [
            "Doanh nghiệp",
            "Số review",
            "Rating TB",
            "Tích cực",
            "Trung tính",
            "Tiêu cực",
        ]
    ]
    st.dataframe(
        display_companies,
        hide_index=True,
        column_config={
            "Doanh nghiệp": st.column_config.TextColumn(pinned=True),
            "Số review": st.column_config.NumberColumn(format="%d"),
            "Rating TB": st.column_config.NumberColumn(format="%.2f"),
            "Tích cực": st.column_config.ProgressColumn(
                format="%.1f%%", min_value=0, max_value=100
            ),
            "Trung tính": st.column_config.ProgressColumn(
                format="%.1f%%", min_value=0, max_value=100
            ),
            "Tiêu cực": st.column_config.ProgressColumn(
                format="%.1f%%", min_value=0, max_value=100
            ),
        },
        height=360,
    )


st.caption(
    "Lưu ý: sentiment trong dashboard là weak label suy ra từ rating; phân tích này mô tả dữ liệu, "
    "không khẳng định quan hệ nhân quả."
)
