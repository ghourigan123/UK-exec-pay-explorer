"""Data loading for UK Exec Pay Explorer."""

from pathlib import Path

import pandas as pd
import streamlit as st

_COMP_COLS: list[str] = [
    "base_salary_gbp",
    "annual_bonus_gbp",
    "ltip_vested_gbp",
    "pension_benefits_gbp",
    "other_gbp",
]


@st.cache_data
def load_data(path: Path) -> pd.DataFrame:
    """Load CEO pay data from CSV.

    Args:
        path: Absolute path to the CSV file.

    Returns:
        DataFrame with financial_year cast to str.
    """
    df = pd.read_csv(path)
    df["financial_year"] = df["financial_year"].astype(str)
    return df


def validate_data(df: pd.DataFrame) -> list[str]:
    """Check data integrity and return a list of human-readable issue strings.

    Checks per row:
    - total_single_figure_gbp is within £10,000 of the sum of components
    - No negative values in any compensation column
    - financial_year is a valid 4-digit year between 1990 and 2100

    Args:
        df: Source DataFrame.

    Returns:
        List of issue strings. Empty list means data passed all checks.
    """
    issues: list[str] = []
    for _, row in df.iterrows():
        label = f"{row['company_name']} ({row['ceo_name']})"

        computed = sum(row[c] for c in _COMP_COLS)
        if abs(computed - row["total_single_figure_gbp"]) > 10_000:
            issues.append(
                f"{label}: total (£{row['total_single_figure_gbp']:,.0f}) "
                f"does not match component sum (£{computed:,.0f})."
            )

        for col in _COMP_COLS + ["total_single_figure_gbp"]:
            if row[col] < 0:
                issues.append(f"{label}: negative value in column '{col}'.")

        try:
            year = int(row["financial_year"])
            if not (1990 <= year <= 2100):
                issues.append(
                    f"{label}: financial_year '{row['financial_year']}' is outside expected range (1990-2100)."
                )
        except (ValueError, TypeError):
            issues.append(
                f"{label}: financial_year '{row['financial_year']}' is not a valid 4-digit year."
            )

    return issues
