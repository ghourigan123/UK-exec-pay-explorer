"""Chart functions for UK Exec Pay Explorer."""

import pandas as pd
import plotly.graph_objects as go

from src.transforms import pay_composition_pct

_COMPONENT_COLORS: dict[str, str] = {
    "Base Salary": "#2563EB",
    "Annual Bonus": "#7C3AED",
    "LTIP Vested": "#059669",
    "Pension": "#D97706",
    "Other": "#9CA3AF",
}

_ABS_COLS: dict[str, str] = {
    "Base Salary": "base_salary_gbp",
    "Annual Bonus": "annual_bonus_gbp",
    "LTIP Vested": "ltip_vested_gbp",
    "Pension": "pension_benefits_gbp",
    "Other": "other_gbp",
}


def sector_comparison_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of median total single figure by sector.

    Args:
        df: Source DataFrame.

    Returns:
        Plotly Figure sorted ascending (largest at top).
    """
    sector_counts = df.groupby("sector").size().to_dict()
    sector_median = (
        df.groupby("sector")["total_single_figure_gbp"]
        .median()
        .sort_values(ascending=True)
        .reset_index()
    )
    sector_median.columns = ["sector", "median_total"]
    sector_median["label"] = sector_median["sector"].apply(
        lambda s: f"{s}  (n={sector_counts.get(s, 1)})"
    )

    fig = go.Figure(
        go.Bar(
            x=sector_median["median_total"],
            y=sector_median["label"],
            orientation="h",
            marker_color="#2563EB",
            text=[f"£{v / 1_000_000:.1f}M" for v in sector_median["median_total"]],
            textposition="outside",
            hovertemplate="Median: £%{x:,.0f}<extra></extra>",
        )
    )
    fig.update_layout(
        xaxis_title="Median total single figure",
        yaxis_title=None,
        plot_bgcolor="white",
        margin=dict(l=20, r=100, t=20, b=40),
        xaxis=dict(
            showgrid=False,
            tickprefix="£",
            tickformat=".2s",
        ),
    )
    return fig


def pay_composition_chart(
    df: pd.DataFrame,
    ceo_a: str,
    ceo_b: str,
) -> go.Figure:
    """Stacked 100% bar chart comparing pay composition for two CEOs.

    Args:
        df: Source DataFrame.
        ceo_a: Name of the first CEO.
        ceo_b: Name of the second CEO.

    Returns:
        Plotly Figure with one stacked bar per CEO.
    """
    pct_a = pay_composition_pct(df, ceo_a)
    pct_b = pay_composition_pct(df, ceo_b)

    row_a = df[df["ceo_name"] == ceo_a].iloc[0]
    row_b = df[df["ceo_name"] == ceo_b].iloc[0]

    x_labels = [
        f"{ceo_a} ({row_a['company_name']}) | £{row_a['total_single_figure_gbp']:,.0f}",
        f"{ceo_b} ({row_b['company_name']}) | £{row_b['total_single_figure_gbp']:,.0f}",
    ]

    fig = go.Figure()
    for component, color in _COMPONENT_COLORS.items():
        abs_col = _ABS_COLS[component]
        fig.add_trace(
            go.Bar(
                x=x_labels,
                y=[pct_a[component], pct_b[component]],
                name=component,
                marker_color=color,
                text=[f"{pct_a[component]:.1f}%", f"{pct_b[component]:.1f}%"],
                textposition="inside",
                insidetextanchor="middle",
                customdata=[[row_a[abs_col]], [row_b[abs_col]]],
                hovertemplate=(
                    "%{x}<br>"
                    + component
                    + ": £%{customdata[0]:,.0f} (%{y:.1f}%)<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        barmode="stack",
        yaxis=dict(
            title="Percentage of total (%)",
            range=[0, 105],
            showgrid=False,
        ),
        plot_bgcolor="white",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5,
        ),
        margin=dict(t=20, b=120),
    )
    return fig
