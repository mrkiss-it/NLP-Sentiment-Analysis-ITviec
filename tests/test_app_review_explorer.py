import pandas as pd
from pandas.testing import assert_frame_equal
from streamlit.testing.v1 import AppTest

from src.app_review_explorer import (
    filter_review_catalog,
    normalize_search,
    plain_markdown,
    prepare_review_catalog,
    review_page,
)
from src.app_services import SENTIMENT_ORDER


def test_review_search_is_literal_accent_insensitive_and_preserves_source():
    source = pd.DataFrame({
        "Company Name": ["Công ty Đẹp", "Beta", "Gamma"],
        "Title": ["Đồng nghiệp hỗ trợ", "Nhiều OT", None],
        "What I liked": ["Phúc lợi tốt", "Dùng C++ và [abc]", None],
        "Suggestions for improvement": ["Cải thiện lương", "Thêm thiết bị", "Nên rõ ràng hơn"],
        "Rating": [4, 1, 3], "sentiment": ["Positive", "Negative", "Neutral"],
        "review_month": pd.to_datetime(["2025-01-01", "2025-02-01", None]),
    }, index=[5, 8, 13])
    original = source.copy(deep=True)
    catalog = prepare_review_catalog(source)
    assert_frame_equal(source, original)
    assert normalize_search("  ĐỒNG  NGHIỆP ") == "dong nghiep"
    for query in ["PHUC LOI", "đồng nghiệp", "cong ty dep", "cai thien luong"]:
        found = filter_review_catalog(catalog, query, list(SENTIMENT_ORDER))
        assert found.index.tolist() == [0]
    assert filter_review_catalog(catalog, "[abc]", ["Negative"]).index.tolist() == [1]
    assert filter_review_catalog(catalog, ".*", list(SENTIMENT_ORDER)).empty
    assert filter_review_catalog(catalog, "", []).empty
    assert catalog.loc[2, "What I liked"] == ""
    assert catalog.loc[0, "Title"] == original.loc[5, "Title"]


def test_review_sorting_and_pagination_do_not_cap_the_search_at_200_rows():
    source = pd.DataFrame({
        "Company Name": ["Demo"] * 205, "Title": [f"Review {i}" for i in range(205)],
        "Rating": [(i % 5) + 1 for i in range(205)], "sentiment": ["Positive"] * 205,
        "review_month": pd.date_range("2000-01-01", periods=205, freq="MS"),
    })
    catalog = prepare_review_catalog(source)
    newest = filter_review_catalog(catalog, "", ["Positive"])
    assert newest.index[0] == 204
    assert filter_review_catalog(catalog, "Review 204", ["Positive"]).index.tolist() == [204]
    assert filter_review_catalog(catalog, "", ["Positive"], "Cũ nhất").index[0] == 0
    lowest = filter_review_catalog(catalog, "", ["Positive"], "Rating thấp nhất")
    assert lowest["Rating"].is_monotonic_increasing
    assert lowest.index[0] == 200
    first, page, count = review_page(newest, 0)
    last, last_page, _ = review_page(newest, 999)
    assert (len(first), page, count) == (8, 1, 26)
    assert (len(last), last_page) == (5, 26)
    assert set(first.index).isdisjoint(last.index)
    empty, page, count = review_page(newest.iloc[:0], 900)
    assert empty.empty and (page, count) == (1, 1)


def test_source_titles_cannot_inject_markdown_into_review_labels():
    escaped = plain_markdown("[link](https://example.com) **bold** :red[text] $x$ <b>")
    assert "\\[link\\]" in escaped
    assert "\\*\\*bold\\*\\*" in escaped
    assert "\\:red\\[text\\]" in escaped
    assert "\\$x\\$" in escaped
    assert "\\<b\\>" in escaped


EXPLORER_APP = '''
import pandas as pd
from src.app_review_explorer import render_review_explorer
reviews = pd.DataFrame({
    "Company Name": ["Alpha", "Beta", "Gamma"],
    "Title": ["Review tích cực", "Review tiêu cực", "Review trung tính"],
    "What I liked": ["Phúc lợi tốt", "Đồng nghiệp hỗ trợ", None],
    "Suggestions for improvement": ["Bớt OT", "Cần tăng lương", None],
    "Rating": [5, 1, 3], "sentiment": ["Positive", "Negative", "Neutral"],
    "review_month": pd.to_datetime(["2025-03-01", "2025-02-01", "2025-01-01"]),
})
render_review_explorer(reviews, "Toàn bộ dữ liệu")
'''


def test_reader_renders_without_expanding_and_selection_survives_view_switch():
    app = AppTest.from_string(EXPLORER_APP, default_timeout=20).run()
    assert not app.exception
    assert not app.expander
    assert app.radio(key="review_selection").value == 0
    app.radio(key="review_selection").set_value(1).run()
    assert not app.exception
    assert any(item.value == "Đồng nghiệp hỗ trợ" for item in app.text)
    app.button_group(key="review_view").set_value("Dạng bảng").run()
    assert not app.exception
    assert app.dataframe[0].value["sentiment"].tolist() == ["Tích cực", "Tiêu cực", "Trung tính"]
    app.button_group(key="review_view").set_value("Đọc review").run()
    assert app.radio(key="review_selection").value == 1


def test_search_empty_state_and_reset_do_not_keep_stale_review():
    app = AppTest.from_string(EXPLORER_APP, default_timeout=20).run()
    app.text_input(key="review_query").set_value("phuc loi").run()
    assert not app.exception
    assert len(app.radio(key="review_selection").options) == 1
    app.text_input(key="review_query").set_value("no-such-review-zzz").run()
    assert not app.exception
    assert not app.radio
    assert any("Không tìm thấy" in item.value for item in app.subheader)
    assert "review_selection" not in app.session_state
    app.button[0].click().run()
    assert not app.exception
    assert len(app.radio(key="review_selection").options) == 3
    app.button_group(key="review_tones").set_value([]).run()
    assert not app.radio
    app.button_group(key="review_tones").set_value(["Neutral"]).run()
    assert app.radio(key="review_selection").value == 2
    assert sum("chưa có nội dung" in c.value for c in app.caption) == 2
