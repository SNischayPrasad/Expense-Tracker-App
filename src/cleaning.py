"""
cleaning.py
-----------
Turns messy raw data into analysis-ready data.
Every step is logged so you can explain exactly what was fixed (great for interviews).
"""

import numpy as np
import pandas as pd

from src import config


def clean_expenses(raw: pd.DataFrame, verbose: bool = True) -> tuple[pd.DataFrame, dict]:
    """Clean the raw expense data. Returns (clean_df, cleaning_report)."""
    df = raw.copy()
    report = {"rows_before": len(df)}

    # 1) Remove exact duplicate transactions (ignore transaction_id, which is unique per row)
    subset = [c for c in df.columns if c != "transaction_id"]
    before = len(df)
    df = df.drop_duplicates(subset=subset, keep="first")
    report["duplicates_removed"] = before - len(df)

    # 2) Standardise category text: strip spaces, Title Case
    df["category"] = df["category"].astype(str).str.strip().str.title()

    # 3) Parse dates that come in two formats (YYYY-MM-DD and DD/MM/YYYY)
    iso = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
    dmy = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
    df["date"] = iso.fillna(dmy)
    report["unparseable_dates_dropped"] = int(df["date"].isna().sum())
    df = df.dropna(subset=["date"])

    # 4) Convert amount to numeric (remove currency symbols / commas)
    df["amount"] = (
        df["amount"].astype(str)
        .str.replace("₹", "", regex=False)
        .str.replace(",", "", regex=False)
        .str.strip()
        .replace({"nan": np.nan, "": np.nan})
        .astype(float)
    )

    # 5) Missing amounts cannot be guessed -> drop them
    report["missing_amount_dropped"] = int(df["amount"].isna().sum())
    df = df.dropna(subset=["amount"])

    # 6) Negative amounts are entry errors -> take absolute value
    report["negative_amounts_fixed"] = int((df["amount"] < 0).sum())
    df["amount"] = df["amount"].abs()

    # 7) Fill missing categorical values with a clear label
    report["missing_payment_filled"] = int(df["payment_method"].isna().sum())
    df["payment_method"] = df["payment_method"].fillna("Unknown")
    report["missing_description_filled"] = int(df["description"].isna().sum())
    df["description"] = df["description"].fillna("Not specified")

    # 8) Keep only known categories
    valid = set(config.CATEGORY_PROFILE) | {"Rent"}
    report["invalid_category_dropped"] = int((~df["category"].isin(valid)).sum())
    df = df[df["category"].isin(valid)]

    df = df.sort_values("date").reset_index(drop=True)
    report["rows_after"] = len(df)

    if verbose:
        print("Cleaning report:")
        for k, v in report.items():
            print(f"  {k:<28}: {v}")
    return df, report


def add_features(df: pd.DataFrame) -> pd.DataFrame:
    """Feature engineering: new columns that make analysis easier."""
    df = df.copy()
    df["year"] = df["date"].dt.year
    df["month"] = df["date"].dt.month
    df["month_name"] = df["date"].dt.strftime("%b")
    df["year_month"] = df["date"].dt.to_period("M").astype(str)
    df["day"] = df["date"].dt.day
    df["weekday"] = df["date"].dt.day_name()
    df["is_weekend"] = df["date"].dt.dayofweek >= 5
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)
    df["expense_type"] = np.where(df["category"].isin(config.ESSENTIAL_CATEGORIES), "Essential", "Discretionary")
    df["amount_bucket"] = pd.cut(
        df["amount"], bins=[0, 200, 1000, 5000, np.inf],
        labels=["Small (<200)", "Medium (200-1k)", "Large (1k-5k)", "Very large (5k+)"],
    )
    return df


def save_clean(df: pd.DataFrame) -> None:
    config.CLEAN_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(config.CLEAN_DATA_PATH, index=False, encoding="utf-8")
