"""Data transformation helpers for UK Exec Pay Explorer."""

from typing import Tuple

import pandas as pd


def format_gbp(value: float) -> str:
    """Format a GBP value with pound sign and thousands separators."""
    return f"£{int(value):,}"


def format_ratio(value: float) -> str:
    """Format a pay ratio as N:1."""
    return f"{int(value)}:1"


def filter_data(
    df: pd.DataFrame,
    sector: str,
    comp_range: Tuple[int, int],
) -> pd.DataFrame:
    """Filter by sector and total compensation range.

    Args:
        df: Source DataFrame.
        sector: ICB sector name, or "All" to skip sector filtering.
        comp_range: (min, max) bounds for total_single_figure_gbp.

    Returns:
        Filtered copy of df.
    """
    result = df.copy()
    if sector != "All":
        result = result[result["sector"] == sector]
    result = result[
        (result["total_single_figure_gbp"] >= comp_range[0])
        & (result["total_single_figure_gbp"] <= comp_range[1])
    ]
    return result


def pay_composition_pct(df: pd.DataFrame, ceo_name: str) -> pd.Series:
    """Return each pay component as a percentage of total for one CEO.

    Args:
        df: Source DataFrame.
        ceo_name: Full name of the CEO.

    Returns:
        Series keyed by component label with float percentage values.
    """
    row = df[df["ceo_name"] == ceo_name].iloc[0]
    total = row["total_single_figure_gbp"]
    return pd.Series(
        {
            "Base Salary": row["base_salary_gbp"] / total * 100,
            "Annual Bonus": row["annual_bonus_gbp"] / total * 100,
            "LTIP Vested": row["ltip_vested_gbp"] / total * 100,
            "Pension": row["pension_benefits_gbp"] / total * 100,
            "Other": row["other_gbp"] / total * 100,
        }
    )
