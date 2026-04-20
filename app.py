"""UK Exec Pay Explorer - main Streamlit entry point."""

from pathlib import Path

import pandas as pd
import streamlit as st

from src.charts import pay_composition_chart, sector_comparison_chart
from src.data_loader import load_data
from src.transforms import filter_data

DATA_PATH = Path(__file__).parent / "data" / "ceo_pay_2024.csv"


def render_header() -> None:
    """Render app title, subtitle, and methodology expander."""
    st.title("UK Exec Pay Explorer")
    st.caption("Explore CEO compensation data from FTSE 100 annual remuneration reports.")
    with st.expander("Methodology and caveats"):
        st.markdown(
            "**Total single figure** is the sum of base salary, annual bonus, "
            "LTIP vested, pension benefits, and other benefits. "
            "This follows the Companies Act 2006 (Schedule 8) standard used by all "
            "UK-listed companies in their Directors' Remuneration Reports.\n\n"
            "All figures are sourced manually from publicly available annual reports. "
            "LTIP values reflect the market value of shares that vested during the year. "
            "Pay ratios compare the CEO total single figure to median UK employee pay "
            "as disclosed in each company's annual remuneration report.\n\n"
            "**Note:** the five sample rows in this MVP use illustrative figures "
            "for template purposes. Replace with verified data from published reports "
            "before sharing findings."
        )


def render_overview(df: pd.DataFrame) -> None:
    """Render the filterable overview table with summary metrics."""
    st.subheader("All companies")

    col1, col2 = st.columns(2)
    with col1:
        sectors = ["All"] + sorted(df["sector"].unique().tolist())
        sector = st.selectbox("Sector", sectors)
    with col2:
        max_comp = int(df["total_single_figure_gbp"].max())
        comp_range = st.slider(
            "Total compensation range (GBP)",
            min_value=0,
            max_value=max_comp,
            value=(0, max_comp),
            step=500_000,
        )

    filtered = filter_data(df, sector, comp_range)

    if filtered.empty:
        st.info("No companies match the current filters.")
        return

    c1, c2, c3 = st.columns(3)
    c1.metric("Companies shown", len(filtered))
    c2.metric(
        "Median total comp",
        f"£{int(filtered['total_single_figure_gbp'].median()):,}",
    )
    c3.metric(
        "Median pay ratio",
        f"{int(filtered['pay_ratio_median'].median())}:1",
    )

    st.dataframe(
        filtered[
            [
                "company_name", "ceo_name", "sector", "financial_year",
                "base_salary_gbp", "annual_bonus_gbp", "ltip_vested_gbp",
                "total_single_figure_gbp", "pay_ratio_median",
            ]
        ].rename(
            columns={
                "company_name": "Company",
                "ceo_name": "CEO",
                "sector": "Sector",
                "financial_year": "Year",
                "base_salary_gbp": "Base Salary",
                "annual_bonus_gbp": "Annual Bonus",
                "ltip_vested_gbp": "LTIP Vested",
                "total_single_figure_gbp": "Total (Single Figure)",
                "pay_ratio_median": "Pay Ratio",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )


def render_sector_comparison(df: pd.DataFrame) -> None:
    """Render median total comp by sector as a horizontal bar chart."""
    st.subheader("Median total compensation by sector")
    st.plotly_chart(sector_comparison_chart(df), use_container_width=True)


def render_pay_composition(df: pd.DataFrame) -> None:
    """Render stacked bar pay composition for two selected CEOs."""
    st.subheader("Pay composition breakdown")
    ceo_names = sorted(df["ceo_name"].tolist())
    col1, col2 = st.columns(2)
    with col1:
        ceo_a = st.selectbox("CEO (left)", ceo_names, index=0)
    with col2:
        ceo_b = st.selectbox("CEO (right)", ceo_names, index=min(1, len(ceo_names) - 1))

    if ceo_a == ceo_b:
        st.info("Select two different CEOs to compare.")
    else:
        st.plotly_chart(pay_composition_chart(df, ceo_a, ceo_b), use_container_width=True)


def render_footer() -> None:
    """Render data source attribution and GitHub link."""
    st.divider()
    st.caption(
        "Data sourced from publicly available FTSE 100 Annual Remuneration Reports. "
        "Built by [Glenn Hourigan](https://github.com/ghourigan123/UK-exec-pay-explorer) as a portfolio project."
    )


def main() -> None:
    """Entry point for the Streamlit app."""
    st.set_page_config(page_title="UK Exec Pay Explorer", layout="wide")
    render_header()

    df = load_data(DATA_PATH)

    view = st.sidebar.radio(
        "View",
        ["Overview table", "Sector comparison", "Pay composition breakdown"],
    )
    st.sidebar.divider()
    st.sidebar.caption(f"**{len(df)} companies** in dataset")
    st.sidebar.caption(f"Financial year: {df['financial_year'].iloc[0]}")

    if view == "Overview table":
        render_overview(df)
    elif view == "Sector comparison":
        render_sector_comparison(df)
    else:
        render_pay_composition(df)

    render_footer()


if __name__ == "__main__":
    main()
