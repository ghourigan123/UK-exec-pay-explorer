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


def sector_comparison_chart(df: pd.DataFrame) -> go.Figure:
    """Horizontal bar chart of median total single figure by sector.

    Args:
        df: Source DataFrame.

    Returns:
        Plotly Figure sorted ascending (largest at top).
    """
    sector_median = (
        df.groupby("sector")["total_single_figure_gbp"]
        .median()
        .sort_values(ascending=True)
        .reset_index()
    )
    sector_median.columns = ["sector", "median_total"]

    fig = go.Figure(
        go.Bar(
            x=sector_median["median_total"],
            y=sector_median["sector"],
            orientation="h",
            marker_color="#2563EB",
            text=[f"£{v:,.0f}" for v in sector_median["median_total"]],
            textposition="outside",
        )
    )
    fig.update_layout(
        xaxis_title="Median total single figure (GBP)",
        yaxis_title=None,
        plot_bgcolor="white",
        margin=dict(l=20, r=120, t=20, b=40),
        xaxis=dict(showgrid=True, gridcolor="#F1F5F9"),
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
        fig.add_trace(
            go.Bar(
                x=x_labels,
                y=[pct_a[component], pct_b[component]],
                name=component,
                marker_color=color,
                text=[f"{pct_a[component]:.1f}%", f"{pct_b[component]:.1f}%"],
                textposition="inside",
                insidetextanchor="middle",
            )
        )

    fig.update_layout(
        barmode="stack",
        yaxis=dict(
            title="Percentage of total (%)",
            range=[0, 105],
            gridcolor="#F1F5F9",
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
