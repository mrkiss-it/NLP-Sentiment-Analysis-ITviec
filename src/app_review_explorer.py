"""A paginated, read-only review reader with fragment-scoped interactions."""

from __future__ import annotations

import hashlib
import re
import unicodedata

import pandas as pd
import streamlit as st

from src.app_services import SENTIMENT_LABELS, SENTIMENT_ORDER

PAGE_SIZE = 8
SORT_OPTIONS = ("Mới nhất", "Cũ nhất", "Rating thấp nhất", "Rating cao nhất")
TEXT_COLUMNS = ("Company Name", "Title", "What I liked", "Suggestions for improvement")
TONE_COLORS = {"Positive": "green", "Neutral": "yellow", "Negative": "red"}


def normalize_search(value: str) -> str:
    """Accent-insensitive literal search, separate from the model's preprocessing."""
    text = unicodedata.normalize("NFKD", value.casefold().replace("đ", "d"))
    return " ".join("".join(c for c in text if not unicodedata.combining(c)).split())


def plain_markdown(value: str) -> str:
    """Keep source text literal in native widget labels and headings."""
    return re.sub(r"([\\`*_{}\[\]()<>#+.!|~:$-])", r"\\\1", value)


@st.cache_data(max_entries=8, show_spinner=False)
def prepare_review_catalog(reviews: pd.DataFrame) -> pd.DataFrame:
    """Build a bounded cached search index without altering source reviews."""
    catalog = reviews.reindex(columns=[*TEXT_COLUMNS, "Rating", "sentiment", "review_month"]).copy()
    catalog = catalog.reset_index(drop=True)
    catalog.index.name = "review_id"  # Stable within this dataset/scope, never a model feature.
    for column in TEXT_COLUMNS:
        catalog[column] = catalog[column].fillna("").astype(str).str.strip()
    catalog["sentiment"] = catalog["sentiment"].fillna("").astype(str)
    catalog["Rating"] = pd.to_numeric(catalog["Rating"], errors="coerce")
    catalog["review_month"] = pd.to_datetime(catalog["review_month"], errors="coerce")
    catalog["_search"] = catalog[list(TEXT_COLUMNS)].agg(" ".join, axis=1).map(normalize_search)
    return catalog


def filter_review_catalog(
    catalog: pd.DataFrame, query: str, sentiments: list[str], order: str = "Mới nhất"
) -> pd.DataFrame:
    """Filter all matching rows before pagination; never interpret search as regex."""
    mask = catalog["sentiment"].isin(sentiments)
    needle = normalize_search(query)
    if needle:
        mask &= catalog["_search"].str.contains(needle, regex=False, na=False)
    result = catalog.loc[mask]
    if order in ("Rating thấp nhất", "Rating cao nhất"):
        return result.sort_values(
            ["Rating", "review_month"], ascending=[order == "Rating thấp nhất", False],
            na_position="last", kind="stable",
        )
    return result.sort_values(
        "review_month", ascending=order == "Cũ nhất", na_position="last", kind="stable"
    )


def review_page(rows: pd.DataFrame, page: int) -> tuple[pd.DataFrame, int, int]:
    """Clamp a one-based page after filtering and return at most eight reviews."""
    total_pages = max(1, (len(rows) + PAGE_SIZE - 1) // PAGE_SIZE)
    current = min(max(1, int(page)), total_pages)
    start = (current - 1) * PAGE_SIZE
    return rows.iloc[start:start + PAGE_SIZE], current, total_pages


def month_label(value) -> str:
    return value.strftime("%m/%Y") if pd.notna(value) else "Chưa có thời gian"


def rating_label(value) -> str:
    return f"{value:g}/5" if pd.notna(value) else "Chưa có rating"


def _reset_filters() -> None:
    st.session_state["review_query"] = ""
    st.session_state["review_tones"] = list(SENTIMENT_ORDER)
    st.session_state["review_sort"] = SORT_OPTIONS[0]
    st.session_state.pop("review_selection", None)
    st.session_state.pop("review_selected_id", None)


def _remember_selection() -> None:
    st.session_state["review_selected_id"] = st.session_state.get("review_selection")


def _reader(row: pd.Series) -> None:
    with st.container(border=True, height=640, key="review_reader", gap="small"):
        st.caption("NỘI DUNG REVIEW")
        st.subheader(plain_markdown(row["Title"] or "Review chưa có tiêu đề"))
        st.caption(f":material/domain: {plain_markdown(row['Company Name'] or 'Chưa có tên công ty')}")
        with st.container(horizontal=True, gap="small", key="review_metadata"):
            st.badge(SENTIMENT_LABELS.get(row["sentiment"], "Chưa có nhãn"),
                     color=TONE_COLORS.get(row["sentiment"], "gray"))
            st.badge(rating_label(row["Rating"]), icon=":material/star:", color="orange")
            st.badge(month_label(row["review_month"]), icon=":material/calendar_month:", color="gray")

        with st.container(key="review_reading_body", gap="small"):
            for column, title, icon, key in [
                ("What I liked", "Điểm thích", "thumb_up", "review_liked"),
                ("Suggestions for improvement", "Gợi ý cải thiện", "tips_and_updates", "review_improve"),
            ]:
                with st.container(border=True, key=key, gap="small"):
                    st.markdown(f"#### :material/{icon}: {title}")
                    if row[column]:
                        st.text(row[column])  # Full source text; no HTML/Markdown interpretation.
                    else:
                        st.caption("Review này chưa có nội dung ở mục này.")
        st.caption(":material/info: Nhãn cảm xúc suy ra từ rating, không phải dự đoán của model. Đọc cả hai phần để hiểu ngữ cảnh.")


@st.fragment
def _review_explorer(catalog: pd.DataFrame, scope: str) -> None:
    with st.container(key="review_explorer", gap="small"):
        with st.container(key="review_explorer_heading", gap="xsmall"):
            st.caption("TỪ DỮ LIỆU ĐẾN CÂU CHUYỆN")
            st.subheader("Tiếng nói từ review")
            st.write("Đọc phản hồi nguyên văn, từ điều được yêu thích đến những điều có thể tốt hơn.")

        with st.container(border=True, key="review_toolbar", gap="small"):
            search_col, sort_col, view_col = st.columns([1.8, 1, 1.1], vertical_alignment="bottom")
            query = search_col.text_input(
                "Tìm trong review", key="review_query", placeholder="Ví dụ: phúc lợi, OT, tên công ty…",
                icon=":material/search:", max_chars=200,
                help="Tìm theo cụm từ trong tiêu đề, công ty và nội dung; có thể gõ không dấu. Nhấn Enter để tìm.",
            )
            order = sort_col.selectbox("Sắp xếp", SORT_OPTIONS, key="review_sort")
            view = view_col.segmented_control(
                "Chế độ xem", ["Đọc review", "Dạng bảng"], default="Đọc review",
                key="review_view", width="stretch",
            )
            tones = st.pills(
                "Lọc cảm xúc", list(SENTIMENT_ORDER), default=list(SENTIMENT_ORDER),
                selection_mode="multi", key="review_tones",
                format_func=lambda tone: f":{TONE_COLORS[tone]}-badge[{SENTIMENT_LABELS[tone]}]",
            )

        signature = (scope, normalize_search(query), tuple(tones or []), order, len(catalog))
        if st.session_state.get("review_filter_signature") != signature:
            previous_pager = st.session_state.get("review_pager_key")
            if previous_pager:
                st.session_state.pop(previous_pager, None)
            st.session_state.pop("review_selection", None)
            st.session_state.pop("review_selected_id", None)
            st.session_state["review_filter_signature"] = signature
        # A new filter gets a fresh native pager, without competing default/state values.
        pager_key = "review_page_" + hashlib.sha256(repr(signature).encode()).hexdigest()[:12]
        st.session_state["review_pager_key"] = pager_key
        filtered = filter_review_catalog(catalog, query, tones or [], order)
        _, _, total_pages = review_page(filtered, 1)

        with st.container(horizontal=True, gap="small", key="review_context"):
            st.badge(f"{len(filtered):,} review phù hợp", color="blue", icon=":material/manage_search:")
            st.caption(f"{plain_markdown(scope)} · Tìm kiếm và lọc chỉ áp dụng cho mục review này")

        if filtered.empty:
            st.session_state.pop("review_selection", None)
            st.session_state.pop("review_selected_id", None)
            with st.container(border=True, key="review_empty"):
                st.subheader(":material/search_off: Không tìm thấy review phù hợp")
                st.write("Thử cụm từ khác hoặc chọn thêm cảm xúc. Phạm vi doanh nghiệp vẫn theo bộ lọc phía trên.")
                st.button("Đặt lại bộ lọc review", icon=":material/restart_alt:", on_click=_reset_filters)
            return

        content = st.container(key="review_content")
        # Reserve content above the native pager; only these eight rows reach the UI.
        with st.container(horizontal=True, vertical_alignment="center", key="review_pager"):
            page = st.pagination(total_pages, key=pager_key, max_visible_pages=5)
            start = (page - 1) * PAGE_SIZE
            st.caption(f"{start + 1:,}–{min(start + PAGE_SIZE, len(filtered)):,} / {len(filtered):,} review · Trang {page:,}/{total_pages:,}")
        visible, _, _ = review_page(filtered, page)

        with content:
            if view == "Dạng bảng":
                display = visible[["Company Name", "Title", "What I liked", "Suggestions for improvement", "Rating", "sentiment", "review_month"]].copy()
                display["sentiment"] = display["sentiment"].map(SENTIMENT_LABELS).fillna("Chưa có nhãn")
                st.dataframe(display, hide_index=True, key="review_table", width="stretch", row_height=56,
                    column_config={
                        "Company Name": st.column_config.TextColumn("Doanh nghiệp", pinned=True),
                        "Title": st.column_config.TextColumn("Tiêu đề", width="medium"),
                        "What I liked": st.column_config.TextColumn("Điểm thích", width="large"),
                        "Suggestions for improvement": st.column_config.TextColumn("Gợi ý cải thiện", width="large"),
                        "Rating": st.column_config.NumberColumn("Rating", format="%d ★"),
                        "sentiment": st.column_config.TextColumn("Cảm xúc từ rating"),
                        "review_month": st.column_config.DateColumn("Thời gian", format="MM/YYYY"),
                    })
                return

            listing, reading = st.columns([1, 1.65], gap="medium")
            ids = visible.index.tolist()
            if st.session_state.get("review_selection") not in ids:
                remembered = st.session_state.get("review_selected_id")
                st.session_state["review_selection"] = remembered if remembered in ids else ids[0]
            with listing.container(border=True, height=640, key="review_list_panel", gap="small"):
                st.caption("CHỌN REVIEW · CUỘN ĐỂ XEM THÊM")
                captions = []
                for _, row in visible.iterrows():
                    color = TONE_COLORS.get(row["sentiment"], "gray")
                    tone = SENTIMENT_LABELS.get(row["sentiment"], "Chưa có nhãn")
                    company = plain_markdown(row["Company Name"] or "Chưa có tên công ty")
                    captions.append(f"{company}  \n:{color}-badge[{tone}] · {rating_label(row['Rating'])} ★ · {month_label(row['review_month'])}")
                selected = st.radio(
                    "Review cần đọc", ids, key="review_selection", width="stretch",
                    label_visibility="collapsed", captions=captions,
                    on_change=_remember_selection,
                    format_func=lambda i: plain_markdown(
                        (visible.loc[i, "Title"] or "Review chưa có tiêu đề")[:110]
                        + ("…" if len(visible.loc[i, "Title"]) > 110 else "")
                    ),
                    persist_state="page",
                )
                st.session_state["review_selected_id"] = selected
            with reading:
                _reader(visible.loc[selected if selected in ids else ids[0]])


def render_review_explorer(reviews: pd.DataFrame, scope: str) -> None:
    """Prepare once on a full page run, then reuse the catalog on fragment reruns."""
    _review_explorer(prepare_review_catalog(reviews), scope)
