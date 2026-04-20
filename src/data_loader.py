"""Data loading for UK Exec Pay Explorer."""

from pathlib import Path

import pandas as pd
import streamlit as st


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
