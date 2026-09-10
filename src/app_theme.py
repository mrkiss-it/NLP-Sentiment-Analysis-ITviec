"""Shared dark developer-tool styling for the Streamlit application."""

from __future__ import annotations

import streamlit as st


def apply_app_style() -> None:
    """Apply the compact glass surface system around native Streamlit widgets."""
    st.html(
        """
        <style>
        :root {
          --it-bg: #080b10;
          --it-surface: rgba(18, 23, 32, .78);
          --it-surface-strong: #141a24;
          --it-surface-soft: rgba(255, 255, 255, .035);
          --it-border: rgba(255, 255, 255, .085);
          --it-border-hover: rgba(255, 255, 255, .16);
          --it-text: #f1f5f9;
          --it-muted: #a0adbf;
          --it-muted-2: #5d6776;
          --it-blue: #7aa7ff;
          --it-mint: #50e3a4;
          --it-warning: #f4d35e;
          --it-orange: #ff994f;
          --it-error: #ff6677;
          --it-radius-sm: 11px;
          --it-radius-md: 15px;
          --it-radius-lg: 18px;
          --it-font: "DM Sans", system-ui, sans-serif;
          --it-mono: "JetBrains Mono", ui-monospace, monospace;
        }

        html, body, [data-testid="stAppViewContainer"] {
          font-family: var(--it-font);
        }

        /* A readable dashboard canvas for laptops and 34-inch ultrawide screens. */
        [data-testid="stMainBlockContainer"] {
          width: 100%;
          max-width: 1920px;
          margin-inline: auto;
          padding-inline: clamp(1rem, 3vw, 4rem);
          padding-top: 3.5rem;
          padding-bottom: 3rem;
        }
        [data-testid="stAppViewContainer"] {
          background:
            radial-gradient(circle at 78% -12%, rgba(122, 167, 255, .10) 0, transparent 31rem),
            radial-gradient(circle at 8% 105%, rgba(80, 227, 164, .055) 0, transparent 28rem),
            var(--it-bg);
        }
        header[data-testid="stHeader"] {
          background: rgba(8, 11, 16, .74);
          backdrop-filter: blur(10px);
        }
        [data-testid="stMainMenuPopover"] {
          opacity: 0 !important;
          pointer-events: none !important;
        }

        /* Sidebar remains calm, compact, and fully collapsible. */
        section[data-testid="stSidebar"] {
          background:
            radial-gradient(circle at 15% 2%, rgba(122, 167, 255, .10), transparent 13rem),
            radial-gradient(circle at 80% 96%, rgba(80, 227, 164, .055), transparent 14rem),
            #0c1017;
          border-right: 1px solid var(--it-border);
          box-shadow: 10px 0 32px rgba(0, 0, 0, .14);
        }
        [data-testid="stSidebarContent"] {
          padding-top: .65rem;
        }
        [data-testid="stSidebarHeader"] {
          min-height: 72px;
          padding-inline: 1.2rem;
          border-bottom: 1px solid rgba(255, 255, 255, .055);
        }
        [data-testid="stSidebarLogo"] {
          max-height: 34px;
        }
        [data-testid="stSidebarNav"] {
          padding: .8rem 1rem .4rem;
        }
        [data-testid="stNavSectionHeader"] {
          margin: .75rem .45rem .35rem;
          color: #778397;
          font-family: var(--it-mono);
          font-size: .68rem;
          font-weight: 600;
          letter-spacing: .09em;
          text-transform: uppercase;
        }
        [data-testid="stSidebarNavLink"] {
          min-height: 42px;
          margin-block: 3px;
          padding-inline: .75rem;
          border: 1px solid transparent;
          border-radius: var(--it-radius-sm);
          color: #a9b4c5;
          transition: background 140ms ease, border-color 140ms ease, transform 140ms ease;
        }
        [data-testid="stSidebarNavLink"] p {
          font-size: .9rem;
          font-weight: 500;
        }
        [data-testid="stSidebarNavLink"] [data-testid="stIconMaterial"] {
          color: #758297;
          font-size: 1.05rem;
        }
        [data-testid="stSidebarNavLink"]:hover {
          transform: translateX(2px);
          color: var(--it-text);
          background: rgba(122, 167, 255, .06);
          border-color: var(--it-border);
        }
        [data-testid="stSidebarNavLink"][aria-current="page"] {
          color: var(--it-text);
          background: rgba(122, 167, 255, .12);
          border-color: rgba(122, 167, 255, .27);
          box-shadow: inset 3px 0 0 var(--it-blue), 0 7px 18px rgba(0, 0, 0, .12);
        }
        [data-testid="stSidebarNavLink"][aria-current="page"] p {
          font-weight: 700;
        }
        [data-testid="stSidebarNavLink"][aria-current="page"] [data-testid="stIconMaterial"] {
          color: var(--it-blue);
        }
        [data-testid="stSidebarNavSeparator"] {
          margin: .8rem .45rem;
          border-color: rgba(255, 255, 255, .065);
        }
        [data-testid="stSidebarUserContent"] {
          margin-top: auto;
          padding: .55rem 1rem 1rem;
        }
        .st-key-sidebar_status_card {
          overflow: hidden;
          padding: .25rem;
          border-color: rgba(122, 167, 255, .14) !important;
          background: rgba(16, 22, 31, .82) !important;
          box-shadow: inset 0 1px 0 rgba(255, 255, 255, .035), 0 12px 28px rgba(0, 0, 0, .15) !important;
        }
        .st-key-sidebar_status_card::before {
          width: 46px !important;
          background: linear-gradient(90deg, var(--it-blue), var(--it-mint)) !important;
        }
        .st-key-sidebar_status_card [data-testid="stCaptionContainer"] p {
          color: #7d9fdc;
          font-family: var(--it-mono);
          font-size: .64rem;
          letter-spacing: .075em;
        }
        .st-key-sidebar_status_card [data-testid="stMetric"] {
          min-height: 76px;
          padding: .65rem .7rem;
          border-radius: 10px;
          background: rgba(7, 11, 17, .58);
          box-shadow: none;
        }
        .st-key-sidebar_status_card [data-testid="stMetricLabel"] {
          font-size: .72rem;
        }
        .st-key-sidebar_status_card [data-testid="stMetricValue"] {
          color: #dce8fb;
          font-size: 1.25rem;
        }
        .st-key-sidebar_badges [data-testid="stBadge"] {
          white-space: nowrap;
        }

        /* Shared restrained glass surfaces. */
        [data-testid="stMetric"],
        [data-testid="stVerticalBlockBorderWrapper"] {
          border: 1px solid var(--it-border);
          background: var(--it-surface);
          box-shadow: 0 12px 32px rgba(0, 0, 0, .16);
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
          border-radius: var(--it-radius-lg);
          transition: border-color 150ms ease, box-shadow 150ms ease;
        }
        [data-testid="stVerticalBlockBorderWrapper"]:hover {
          border-color: var(--it-border-hover);
          box-shadow: 0 14px 36px rgba(0, 0, 0, .19);
        }
        [data-testid="stMetric"] {
          min-height: 132px;
          padding: 1.15rem 1.25rem;
          border-radius: var(--it-radius-md);
          transition: border-color 150ms ease, transform 150ms ease;
        }
        [data-testid="stMetric"]:hover {
          transform: translateY(-2px);
          border-color: rgba(122, 167, 255, .26);
        }
        :is(
          .st-key-kpi_reviews,
          .st-key-kpi_companies,
          .st-key-kpi_positive,
          .st-key-kpi_neutral,
          .st-key-kpi_negative,
          .st-key-kpi_rating
        ) {
          --metric-accent: var(--it-blue);
        }
        .st-key-kpi_positive { --metric-accent: var(--it-mint); }
        .st-key-kpi_neutral { --metric-accent: var(--it-warning); }
        .st-key-kpi_negative { --metric-accent: var(--it-error); }
        .st-key-kpi_rating { --metric-accent: var(--it-orange); }
        :is(
          .st-key-kpi_reviews,
          .st-key-kpi_companies,
          .st-key-kpi_positive,
          .st-key-kpi_neutral,
          .st-key-kpi_negative,
          .st-key-kpi_rating
        ) [data-testid="stMetric"] {
          position: relative;
          overflow: hidden;
        }
        :is(
          .st-key-kpi_reviews,
          .st-key-kpi_companies,
          .st-key-kpi_positive,
          .st-key-kpi_neutral,
          .st-key-kpi_negative,
          .st-key-kpi_rating
        ) [data-testid="stMetric"]::before {
          content: "";
          position: absolute;
          inset: 0 auto 0 0;
          width: 2px;
          background: var(--metric-accent);
          opacity: .78;
        }
        :is(
          .st-key-kpi_reviews,
          .st-key-kpi_companies,
          .st-key-kpi_positive,
          .st-key-kpi_neutral,
          .st-key-kpi_negative,
          .st-key-kpi_rating
        ) :is([data-testid="stMetricValue"], [data-testid="stMetricLabel"] [data-testid="stIconMaterial"]) {
          color: var(--metric-accent);
        }
        [data-testid="stMetricValue"],
        [data-testid="stMetricDelta"] {
          font-family: var(--it-mono);
        }
        [data-testid="stMetricLabel"] {
          color: var(--it-muted);
          font-family: var(--it-font);
          font-size: .875rem;
          letter-spacing: 0;
        }
        [data-testid="stMetricValue"] {
          color: var(--it-blue);
          font-size: clamp(1.75rem, 2.1vw, 2.5rem);
          letter-spacing: -.045em;
        }

        /* Inputs and compact selectors. */
        [data-testid="stBadge"],
        code, pre, kbd {
          font-family: var(--it-mono);
        }
        [data-testid="stWidgetLabel"] {
          color: #aab5c6;
          font-family: var(--it-font);
          font-size: .875rem;
          letter-spacing: 0;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] > div,
        [data-testid="stTextArea"] textarea,
        [data-testid="stTextInput"] input {
          border-color: var(--it-border);
          border-radius: var(--it-radius-sm);
          background: rgba(6, 9, 14, .66);
          transition: border-color 140ms ease, box-shadow 140ms ease;
        }
        [data-testid="stSelectbox"] [data-baseweb="select"] > div:focus-within,
        [data-testid="stTextArea"] textarea:focus,
        [data-testid="stTextInput"] input:focus {
          border-color: rgba(122, 167, 255, .52);
          box-shadow: 0 0 0 3px rgba(122, 167, 255, .08);
        }
        [data-testid="stButtonGroup"] [role="toolbar"],
        [data-testid="stButtonGroup"] [role="radiogroup"] {
          gap: .24rem;
          padding: .25rem;
          border: 1px solid var(--it-border);
          border-radius: var(--it-radius-sm);
          background: rgba(5, 8, 13, .62);
          box-shadow: inset 0 1px 0 rgba(255, 255, 255, .025);
        }
        [data-testid="stButtonGroup"] button[data-variant="segmented_control"],
        [data-testid="stButtonGroup"] button[data-variant="pills"] {
          min-height: 42px;
          margin: 0;
          border: 1px solid transparent;
          border-radius: 8px !important;
          color: var(--it-muted);
          font-family: var(--it-font);
          font-size: .875rem;
          transition: color 140ms ease, background 140ms ease, border-color 140ms ease;
        }
        [data-testid="stButtonGroup"] button:hover {
          color: var(--it-text);
          background: rgba(255, 255, 255, .045);
        }
        [data-testid="stButtonGroup"] button[data-selected="true"] {
          color: #e9f2ff;
          border-color: rgba(122, 167, 255, .20);
          background: rgba(122, 167, 255, .12);
          box-shadow: 0 3px 10px rgba(20, 45, 82, .14);
        }

        /* Actions use solid color rather than bright gradients. */
        [data-testid="stBaseButton-primary"],
        [data-testid="stFormSubmitButton"] button[kind="primaryFormSubmit"] {
          min-height: 40px;
          padding-inline: 1.1rem;
          border: 1px solid rgba(122, 167, 255, .34);
          border-radius: var(--it-radius-sm);
          color: #08101d;
          background: var(--it-blue);
          box-shadow: 0 7px 18px rgba(56, 92, 154, .16);
          font-weight: 700;
          transition: transform 140ms ease, filter 140ms ease, box-shadow 140ms ease;
        }
        [data-testid="stBaseButton-primary"]:hover,
        [data-testid="stFormSubmitButton"] button[kind="primaryFormSubmit"]:hover {
          transform: translateY(-1px);
          filter: brightness(1.05);
          box-shadow: 0 9px 22px rgba(56, 92, 154, .20);
        }
        [data-testid="stBaseButton-secondary"],
        [data-testid="stPopoverButton"] > button {
          min-height: 40px;
          border-color: var(--it-border);
          border-radius: var(--it-radius-sm);
          color: var(--it-text);
          background: rgba(255, 255, 255, .045);
          box-shadow: none;
          transition: transform 140ms ease, background 140ms ease, border-color 140ms ease;
        }
        [data-testid="stBaseButton-secondary"]:hover,
        [data-testid="stPopoverButton"] > button:hover {
          transform: translateY(-1px);
          border-color: var(--it-border-hover);
          background: rgba(255, 255, 255, .07);
        }

        /* Tabs, expanders, alerts, tables, and status elements. */
        [data-testid="stTabs"] [role="tablist"] {
          gap: .25rem;
          padding: .25rem;
          border: 1px solid var(--it-border);
          border-radius: var(--it-radius-sm);
          background: rgba(5, 8, 13, .58);
        }
        [data-testid="stTabs"] [role="tab"] {
          min-height: 38px;
          padding-inline: .9rem;
          border-radius: 8px;
          color: var(--it-muted);
          transition: background 140ms ease, color 140ms ease;
        }
        [data-testid="stTabs"] [role="tab"][aria-selected="true"] {
          color: var(--it-text);
          background: rgba(122, 167, 255, .11);
        }
        [data-testid="stTabs"] [data-baseweb="tab-highlight"],
        [data-testid="stTabs"] [data-baseweb="tab-border"] {
          display: none;
        }
        [data-testid="stExpander"] details {
          border-color: var(--it-border);
          border-radius: var(--it-radius-md);
          background: var(--it-surface);
        }
        [data-testid="stExpander"] summary {
          min-height: 50px;
          font-weight: 600;
          transition: color 140ms ease, background 140ms ease;
        }
        [data-testid="stExpander"] summary:hover {
          color: var(--it-blue);
          background: rgba(122, 167, 255, .045);
        }
        [data-testid="stAlert"] {
          border-radius: var(--it-radius-sm);
          border-color: var(--it-border);
          background: rgba(18, 23, 32, .72);
        }
        [data-testid="stDataFrame"] {
          overflow: hidden;
          border: 1px solid var(--it-border);
          border-radius: var(--it-radius-md);
        }
        [data-testid="stBadge"] {
          font-size: .75rem;
          letter-spacing: 0;
        }
        [data-testid="stCaptionContainer"] {
          color: var(--it-muted);
          opacity: 1;
        }
        [data-testid="stCaptionContainer"] p { color: var(--it-muted); }

        /* Named sections create a clearer hierarchy without heavier glass. */
        :is(
          .st-key-overview_sentiment_panel,
          .st-key-overview_journey_panel,
          .st-key-insight_filter_panel,
          .st-key-insight_donut_panel,
          .st-key-insight_trend_panel,
          .st-key-wordcloud_panel,
          .st-key-terms_panel,
          .st-key-company_table_panel,
          .st-key-model_status_panel,
          .st-key-sentiment_form,
          .st-key-product_data_card,
          .st-key-product_insight_card,
          .st-key-product_model_card,
          .st-key-pipeline_review_card,
          .st-key-pipeline_clean_card,
          .st-key-pipeline_vector_card,
          .st-key-pipeline_result_card
        ) {
          position: relative;
          overflow: hidden;
          border-color: var(--it-border) !important;
          background: var(--it-surface);
          box-shadow: 0 12px 32px rgba(0, 0, 0, .15);
        }
        :is(
          .st-key-overview_sentiment_panel,
          .st-key-overview_journey_panel,
          .st-key-insight_filter_panel,
          .st-key-insight_donut_panel,
          .st-key-insight_trend_panel,
          .st-key-wordcloud_panel,
          .st-key-terms_panel,
          .st-key-company_table_panel,
          .st-key-model_status_panel,
          .st-key-sentiment_form,
          .st-key-product_data_card,
          .st-key-product_insight_card,
          .st-key-product_model_card,
          .st-key-pipeline_review_card,
          .st-key-pipeline_clean_card,
          .st-key-pipeline_vector_card,
          .st-key-pipeline_result_card
        )::before {
          content: "";
          position: absolute;
          z-index: 1;
          top: 0;
          left: 18px;
          width: 42px;
          height: 2px;
          border-radius: 0 0 2px 2px;
          background: var(--card-accent, var(--it-blue));
          opacity: .72;
        }
        .st-key-product_data_card,
        .st-key-pipeline_clean_card { --card-accent: var(--it-mint); }
        .st-key-product_insight_card,
        .st-key-pipeline_vector_card { --card-accent: var(--it-blue); }
        .st-key-product_model_card,
        .st-key-pipeline_result_card { --card-accent: var(--it-warning); }
        .st-key-pipeline_review_card { --card-accent: var(--it-orange); }
        :is(
          .st-key-product_data_card,
          .st-key-product_insight_card,
          .st-key-product_model_card,
          .st-key-pipeline_review_card,
          .st-key-pipeline_clean_card,
          .st-key-pipeline_vector_card,
          .st-key-pipeline_result_card
        ) {
          min-height: 138px;
          transition: transform 150ms ease, border-color 150ms ease, box-shadow 150ms ease;
        }
        :is(
          .st-key-product_data_card,
          .st-key-product_insight_card,
          .st-key-product_model_card,
          .st-key-pipeline_review_card,
          .st-key-pipeline_clean_card,
          .st-key-pipeline_vector_card,
          .st-key-pipeline_result_card
        ):hover {
          transform: translateY(-2px);
          border-color: color-mix(in srgb, var(--card-accent) 28%, transparent) !important;
          box-shadow: 0 15px 36px rgba(0, 0, 0, .19);
        }
        :is(
          .st-key-product_data_card,
          .st-key-product_insight_card,
          .st-key-product_model_card,
          .st-key-pipeline_review_card,
          .st-key-pipeline_clean_card,
          .st-key-pipeline_vector_card,
          .st-key-pipeline_result_card
        ) [data-testid="stIconMaterial"] {
          color: var(--card-accent);
        }

        h1, h2, h3 {
          color: var(--it-text);
          letter-spacing: -.03em;
        }
        :is(h2, h3, h4) [data-testid="stIconMaterial"] {
          color: var(--it-blue);
        }
        h1 { font-size: clamp(1.85rem, 2.5vw, 2.65rem); text-wrap: balance; }
        h2 { font-size: 1.55rem; }
        h3 { font-size: 1.22rem; }
        p { line-height: 1.55; }

        /* Explicit responsive groups: cards retain a readable minimum width. */
        :is(.st-key-overview_metrics, .st-key-insight_metrics)[data-testid="stHorizontalBlock"] {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(min(100%, 200px), 1fr));
          gap: 1rem;
        }
        :is(.st-key-overview_metrics, .st-key-insight_metrics)[data-testid="stHorizontalBlock"] > * {
          width: 100%; min-width: 0;
        }
        @media (min-width: 1200px) {
          .st-key-insight_metrics[data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(5, minmax(0, 1fr));
          }
        }
        .st-key-page_header { margin-bottom: .5rem; }
        .st-key-page_header [data-testid="stCaptionContainer"] p {
          font-family: var(--it-mono);
          font-size: .75rem;
          color: var(--it-blue);
          letter-spacing: .1em;
        }
        .st-key-page_header h1 { padding-top: .2rem; padding-bottom: .45rem; }
        .st-key-page_header p { max-width: 75ch; }
        .st-key-page_header [data-testid="stMarkdownContainer"] p {
          color: #b3bfd0;
          font-family: var(--it-font);
        }
        .st-key-prediction_result {
          min-height: 360px;
          background: rgba(122, 167, 255, .045);
          border: 1px solid rgba(122, 167, 255, .18);
          border-radius: var(--it-radius-lg);
        }
        .st-key-language_workspace {
          position: relative;
          overflow: hidden;
          border-color: rgba(122, 167, 255, .2) !important;
          background:
            radial-gradient(circle at 92% 4%, rgba(80, 227, 164, .06), transparent 30%),
            rgba(12, 17, 25, .82);
          box-shadow: 0 18px 44px rgba(0, 0, 0, .18);
        }
        .st-key-language_workspace h4 {
          letter-spacing: -.015em;
        }
        .st-key-wordcloud_metrics[data-testid="stHorizontalBlock"] {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: .75rem;
        }
        .st-key-wordcloud_metrics [data-testid="stMetric"] {
          min-height: 92px;
          padding: .75rem .9rem;
          box-shadow: none;
          border-color: rgba(122, 167, 255, .13);
          background: rgba(7, 11, 17, .62);
        }
        .st-key-wordcloud_metrics [data-testid="stMetricLabel"] p {
          color: #8997aa;
          font-family: var(--it-mono);
          font-size: .76rem;
        }
        .st-key-wordcloud_metrics [data-testid="stMetricValue"] {
          font-size: 1.3rem;
          color: #dce8fb;
        }
        .st-key-wordcloud_panel [data-testid="stImage"] {
          overflow: hidden;
          border: 1px solid rgba(255, 255, 255, .07);
          border-radius: 12px;
          background: #0b1018;
        }
        .st-key-wordcloud_panel,
        .st-key-terms_panel {
          background: rgba(9, 14, 21, .82);
        }
        [data-testid="stPageLink"] a {
          padding: .65rem .85rem;
          border-radius: var(--it-radius-sm);
          border: 1px solid var(--it-border);
          background: rgba(122, 167, 255, .07);
        }
        [data-testid="stPageLink"] a:hover { border-color: var(--it-blue); }
        :is(button, a, input, textarea):focus-visible {
          outline: 2px solid var(--it-blue);
          outline-offset: 3px;
        }
        @media (max-width: 1100px) {
          :is(.st-key-overview_chart_row, .st-key-insight_chart_row, .st-key-prediction_workspace) > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap;
          }
          :is(.st-key-overview_chart_row, .st-key-insight_chart_row, .st-key-prediction_workspace) > [data-testid="stLayoutWrapper"] > [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
            min-width: min(100%, 380px);
            flex: 1 1 380px;
          }
        }
        @media (max-width: 600px) {
          :is(.st-key-overview_metrics, .st-key-insight_metrics)[data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(2, minmax(0, 1fr)); gap: .65rem;
          }
          [data-testid="stMetric"] { padding: .85rem; }
          [data-testid="stMetricValue"] { font-size: 1.6rem; }
          .st-key-insight_metrics > [data-testid="stLayoutWrapper"]:last-child {
            grid-column: 1 / -1;
          }
          .st-key-prediction_result { min-height: 220px; }
          .st-key-wordcloud_metrics[data-testid="stHorizontalBlock"] {
            grid-template-columns: repeat(2, minmax(0, 1fr));
          }
          .st-key-wordcloud_metrics [data-testid="stMetric"] { min-height: 78px; }
          .st-key-wordcloud_metrics > [data-testid="stElementContainer"]:last-child {
            grid-column: 1 / -1;
          }
        }
        @media (max-width: 360px) {
          :is(.st-key-overview_metrics, .st-key-insight_metrics, .st-key-wordcloud_metrics)[data-testid="stHorizontalBlock"] {
            grid-template-columns: 1fr;
          }
        }

        @media (max-width: 900px) {
          [data-testid="stMainBlockContainer"] {
            padding-top: 3.5rem;
            padding-inline: 1rem;
          }
          [data-testid="stMetric"] { min-height: 102px; }
        }
        @media (prefers-reduced-motion: reduce) {
          [data-testid="stSidebarNavLink"],
          [data-testid="stBaseButton-primary"],
          [data-testid="stBaseButton-secondary"],
          [data-testid="stButtonGroup"] button,
          [data-testid="stMetric"],
          [data-testid="stVerticalBlockBorderWrapper"],
          [class*="st-key-product_"],
          [class*="st-key-pipeline_"] { transition: none; }
        }

        /* NLP workspace: evidence-first hierarchy, compact readable controls. */
        :is(.st-key-review_editor, .st-key-nlp_evidence, .st-key-evaluation_matrix,
            .st-key-evaluation_tradeoff, .st-key-evaluation_sensitivity,
            .st-key-evaluation_errors, .st-key-product_evaluation_card) {
          background: rgba(16, 22, 32, .8);
          border: 1px solid rgba(122, 167, 255, .14);
          border-radius: 18px;
          box-shadow: 0 8px 24px rgba(0, 0, 0, .12);
        }
        .st-key-prediction_result {
          min-height: 465px;
          background: radial-gradient(ellipse at 90% 0%, rgba(122,167,255,.09), transparent 65%), #0d131d;
          border-color: rgba(122,167,255,.26);
        }
        .st-key-prediction_empty { padding: 1rem .25rem; }
        .st-key-prediction_empty h2 { color: var(--it-blue); }
        .st-key-lab_status { margin-bottom: .15rem; }
        .stMarkdownBadge {
          font-family: var(--it-mono);
          font-size: .75rem !important;
          padding: .22rem .45rem;
          border-radius: 7px;
          line-height: 1.65;
        }
        .st-key-sidebar_badges .stMarkdownBadge { font-size: .72rem !important; }
        .st-key-product_actions {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 1rem;
        }
        .st-key-product_actions > * { min-width: 0; }
        .st-key-product_actions [class*="st-key-product_"] > [data-testid="stElementContainer"]:last-child {
          margin-top: auto;
        }
        :is(.st-key-product_insight_card, .st-key-product_model_card, .st-key-product_evaluation_card) {
          position: relative;
          background: var(--it-surface);
          border-color: var(--it-border);
          --card-accent: var(--it-blue);
        }
        .st-key-product_model_card { --card-accent: var(--it-mint); }
        .st-key-product_evaluation_card { --card-accent: var(--it-warning); }
        .st-key-product_evaluation_card::before {
          content: "";
          position: absolute;
          top: 0; left: 18px; width: 42px; height: 2px;
          border-radius: 0 0 2px 2px;
          background: var(--card-accent);
          opacity: .72;
        }
        .st-key-product_actions [data-testid="stMarkdownContainer"] [role="img"] { color: var(--card-accent); }
        :is(.st-key-review_editor, .st-key-prediction_result, .st-key-nlp_evidence,
            .st-key-evaluation_matrix, .st-key-evaluation_tradeoff,
            .st-key-evaluation_sensitivity, .st-key-evaluation_errors) h3 {
          font-size: clamp(1.1rem, 1.5vw, 1.35rem);
          line-height: 1.4;
        }
        .st-key-review_editor [data-testid="stButtonGroup"] [role="radiogroup"] {
          flex-wrap: wrap;
        }
        .st-key-review_editor [data-testid="stButtonGroup"] button { min-height: 38px; }
        :is(.st-key-probability_positive, .st-key-probability_neutral, .st-key-probability_negative) {
          padding-block: .1rem;
        }
        :is(.st-key-probability_positive, .st-key-probability_neutral, .st-key-probability_negative) p {
          display: flex;
          justify-content: space-between;
          gap: .8rem;
          font-size: .9rem;
        }
        :is(.st-key-probability_positive, .st-key-probability_neutral, .st-key-probability_negative) strong {
          font-family: var(--it-mono);
          font-weight: 500;
        }
        .st-key-probability_positive [role="progressbar"] > div > div { background: var(--it-mint); }
        .st-key-probability_neutral [role="progressbar"] > div > div { background: var(--it-warning); }
        .st-key-probability_negative [role="progressbar"] > div > div { background: var(--it-error); }
        :is(.st-key-nlp_metrics, .st-key-evaluation_metrics, .st-key-tradeoff_metrics) {
          display: grid;
          gap: .75rem;
        }
        .st-key-nlp_metrics { grid-template-columns: repeat(3, minmax(0, 1fr)); }
        .st-key-evaluation_metrics { grid-template-columns: repeat(4, minmax(0, 1fr)); }
        .st-key-tradeoff_metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        :is(.st-key-nlp_metrics, .st-key-tradeoff_metrics) [data-testid="stMetric"] {
          min-height: 80px;
          padding: .45rem .65rem;
          box-shadow: none;
        }
        :is(.st-key-nlp_metrics, .st-key-tradeoff_metrics) [data-testid="stMetricValue"] {
          font-size: clamp(1.35rem, 1.8vw, 1.8rem);
        }
        .st-key-evaluation_metrics [data-testid="stMetricValue"] { font-size: 1.8rem; }
        .st-key-pipeline_steps { display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); }
        :is(.st-key-evaluation_chart_row, .st-key-language_charts) [data-testid="stColumn"] {
          min-width: min(100%, 320px);
        }
        @media (max-width: 1100px) {
          .st-key-product_actions { grid-template-columns: 1fr; }
          :is(.st-key-evaluation_chart_row, .st-key-language_charts) [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap;
          }
          :is(.st-key-evaluation_chart_row, .st-key-language_charts) [data-testid="stColumn"] {
            flex: 1 1 380px;
          }
          .st-key-pipeline_steps { grid-template-columns: repeat(2, minmax(0, 1fr)); }
          .st-key-evaluation_metrics { grid-template-columns: repeat(2, minmax(0, 1fr)); }
        }
        @media (max-width: 640px) {
          .st-key-prediction_result { min-height: 300px; }
          .st-key-nlp_metrics { grid-template-columns: 1fr; }
          .st-key-evaluation_metrics [data-testid="stMetric"] { padding: .55rem; }
          .st-key-evaluation_metrics [data-testid="stMetricValue"] { font-size: 1.3rem; }
          .st-key-evaluation_metrics [data-testid="stMetricDelta"] { font-size: .68rem; }
          .st-key-insight_metrics > :last-child { grid-column: 1 / -1; }
          .st-key-language_workspace { border: 0; padding: 0; background: transparent; box-shadow: none; }
        }
        /* Review reader: native selectable cards, a calm long-form reading pane. */
        .st-key-review_explorer { margin-block: 1.25rem 1.5rem; }
        .st-key-review_explorer_heading [data-testid="stCaptionContainer"] p {
          color: var(--it-blue);
          font-family: var(--it-mono);
          font-size: .72rem;
          letter-spacing: .08em;
        }
        .st-key-review_explorer_heading h3 { font-size: 1.55rem; padding-block: .15rem; }
        .st-key-review_explorer_heading [data-testid="stMarkdownContainer"] p { color: var(--it-muted); }
        :is(.st-key-review_toolbar, .st-key-review_list_panel, .st-key-review_reader, .st-key-review_empty) {
          background: rgba(16, 22, 32, .78);
          border: 1px solid var(--it-border);
          border-radius: var(--it-radius-lg);
          box-shadow: 0 8px 24px rgba(0,0,0,.12);
        }
        .st-key-review_toolbar { padding: 1rem 1.15rem; }
        .st-key-review_query input,
        .st-key-review_query input:focus {
          border: 0;
          border-radius: 0;
          background: transparent;
          outline: none;
          box-shadow: none;
        }
        .st-key-review_query [data-testid="stTextInputRootElement"]:focus-within {
          border-color: var(--it-blue);
          box-shadow: 0 0 0 3px rgba(122,167,255,.1);
        }
        .st-key-review_context { align-items: center; }
        .st-key-review_context [data-testid="stCaptionContainer"] { font-size: .8rem; }
        .st-key-review_list_panel { padding: .85rem; background: rgba(11,16,24,.9); }
        .st-key-review_list_panel > [data-testid="stElementContainer"]:first-child p,
        .st-key-review_reader > [data-testid="stElementContainer"]:first-child p {
          font-family: var(--it-mono);
          font-size: .68rem;
          letter-spacing: .075em;
          color: #91a2ba;
        }
        .st-key-review_selection [role="radiogroup"] { gap: .5rem; }
        .st-key-review_selection :is(label:has(input[type="radio"]), [role="radio"]) {
          width: 100%;
          margin: 0;
          padding: .7rem .8rem;
          border: 1px solid rgba(255,255,255,.065);
          border-radius: 12px;
          background: rgba(18,25,36,.7);
          align-items: flex-start;
          transition: background 120ms ease, border-color 120ms ease;
        }
        .st-key-review_selection :is(label:has(input[type="radio"]), [role="radio"]):hover {
          background: rgba(122,167,255,.055);
          border-color: rgba(122,167,255,.22);
        }
        .st-key-review_selection :is(label:has(input:checked), [role="radio"][aria-checked="true"]) {
          border-color: rgba(122,167,255,.4);
          background: rgba(122,167,255,.11);
          box-shadow: inset 3px 0 0 var(--it-blue);
        }
        .st-key-review_selection :is(label:focus-within, [role="radio"]:focus-visible) {
          outline: 2px solid var(--it-blue);
          outline-offset: 2px;
        }
        .st-key-review_selection [data-testid="stMarkdownContainer"] p {
          font-size: .9rem; line-height: 1.4; font-weight: 500;
        }
        .st-key-review_selection [data-testid="stCaptionContainer"] p {
          color: #a7b4c7; font-size: .76rem; line-height: 1.65;
        }
        .st-key-review_selection .stMarkdownBadge { font-size: .65rem !important; padding: .06rem .3rem; }
        .st-key-review_reader {
          padding: 1.4rem 1.5rem;
          border-color: rgba(122,167,255,.18);
          background: radial-gradient(ellipse at 95% 0%, rgba(122,167,255,.04), transparent 50%), #0e151f;
        }
        .st-key-review_reader h3 {
          font-size: clamp(1.25rem, 1.5vw, 1.65rem); line-height: 1.4;
          padding-block: .15rem .35rem;
        }
        :is(.st-key-review_list_panel, .st-key-review_reader) {
          scrollbar-color: #3a475d transparent;
          scrollbar-width: thin;
        }
        .st-key-review_reading_body { margin-block: .15rem; }
        :is(.st-key-review_liked, .st-key-review_improve) {
          background: rgba(7,12,19,.48);
          border-color: rgba(255,255,255,.07);
          border-radius: 13px;
          padding: 1rem 1.15rem;
        }
        .st-key-review_liked h4 [role="img"] { color: var(--it-mint); }
        .st-key-review_improve h4 [role="img"] { color: var(--it-warning); }
        .st-key-review_reading_body :is([data-testid="stText"], pre) {
          font-family: var(--it-font);
          font-size: 1rem;
          line-height: 1.8;
          white-space: pre-wrap;
          overflow-wrap: anywhere;
          color: #d9e2ef;
        }
        .st-key-review_pager { justify-content: space-between; padding-inline: .1rem; }
        .st-key-review_pager [data-testid="stCaptionContainer"] {
          font-family: var(--it-mono); font-size: .75rem;
        }
        @media (prefers-reduced-motion: reduce) {
          .st-key-review_selection label { transition: none; }
        }
        </style>
        """
    )


def page_header(section: str, title: str, description: str) -> None:
    """Shared page hierarchy rendered with native text elements."""
    with st.container(key="page_header", gap="xsmall"):
        st.caption(f"SENTIMENT LAB / {section}")
        st.title(title)
        st.write(description)


def style_chart(chart):
    """Use readable labels and a consistent, quiet plotting surface."""
    return (
        chart.configure(font="DM Sans", background="transparent")
        .configure_view(strokeWidth=0)
        .configure_axis(
            labelColor="#a0adbf", titleColor="#a0adbf", labelFontSize=13,
            titleFontSize=12, titleFontWeight=400, labelPadding=8, titlePadding=14,
            domain=False, ticks=False, gridColor="#252e3c", gridOpacity=0.55,
        )
        .configure_legend(labelColor="#cbd5e1", titleColor="#a0adbf", labelFontSize=13)
        .configure_range(category=["#50e3a4", "#f4d35e", "#ff6677", "#7aa7ff"])
    )
