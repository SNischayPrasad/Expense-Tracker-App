"""
analysis.py
-----------
All the number-crunching: aggregations, trends, budgets, and anomaly detection.
Each function returns a DataFrame so it can be printed, plotted, or saved.
"""

import pandas as pd

from src import config


def category_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Total, average, count and share (%) of spending per category."""
    out = (
        df.groupby("category")["amount"]
        .agg(total="sum", average="mean", transactions="count", largest="max")
        .sort_values("total", ascending=False)
    )
    out["share_pct"] = 100 * out["total"] / out["total"].sum()
    return out.round(2)


def monthly_trend(df: pd.DataFrame) -> pd.DataFrame:
    """Total spending per month + month-over-month (MoM) change."""
    out = df.groupby("year_month")["amount"].agg(total="sum", transactions="count")
    out["mom_change_pct"] = out["total"].pct_change() * 100
    out["rolling_3m_avg"] = out["total"].rolling(3, min_periods=1).mean()
    out["savings"] = config.MONTHLY_INCOME - out["total"]
    out["savings_rate_pct"] = 100 * out["savings"] / config.MONTHLY_INCOME
    return out.round(2)


def category_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """Pivot table: rows = month, columns = category, values = spend."""
    return df.pivot_table(index="year_month", columns="category", values="amount",
                          aggfunc="sum", fill_value=0).round(2)


def payment_method_summary(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby("payment_method")["amount"].agg(total="sum", transactions="count")
    out["share_pct"] = 100 * out["total"] / out["total"].sum()
    return out.sort_values("total", ascending=False).round(2)


def weekday_pattern(df: pd.DataFrame) -> pd.DataFrame:
    """Average daily spend per weekday (excluding rent, which is fixed)."""
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    variable = df[df["category"] != "Rent"]
    daily = variable.groupby(["date", "weekday"])["amount"].sum().reset_index()
    out = daily.groupby("weekday")["amount"].mean().reindex(order).to_frame("avg_daily_spend")
    return out.round(2)


def expense_type_summary(df: pd.DataFrame) -> pd.DataFrame:
    out = df.groupby("expense_type")["amount"].sum().to_frame("total")
    out["share_pct"] = 100 * out["total"] / out["total"].sum()
    return out.round(2)


def budget_vs_actual(df: pd.DataFrame) -> pd.DataFrame:
    """Compare every month's spend per category with its budget.
    Overspending = actual > budget."""
    pivot = category_by_month(df)
    rows = []
    for month, row in pivot.iterrows():
        for category, actual in row.items():
            budget = config.MONTHLY_BUDGET.get(category, 0)
            rows.append({
                "year_month": month,
                "category": category,
                "budget": budget,
                "actual": round(actual, 2),
                "variance": round(actual - budget, 2),
                "utilisation_pct": round(100 * actual / budget, 1) if budget else None,
                "overspent": actual > budget,
            })
    return pd.DataFrame(rows)


def overspending_report(budget_df: pd.DataFrame) -> pd.DataFrame:
    """Only the month/category combinations that went over budget."""
    over = budget_df[budget_df["overspent"]].sort_values("variance", ascending=False)
    return over.reset_index(drop=True)


def detect_anomalies(df: pd.DataFrame, z: float = config.ANOMALY_Z_THRESHOLD) -> pd.DataFrame:
    """Flag single transactions that are unusually large FOR THEIR CATEGORY.
    Uses z-score: (amount - category mean) / category std."""
    variable = df[df["category"] != "Rent"].copy()
    grp = variable.groupby("category")["amount"]
    variable["z_score"] = (variable["amount"] - grp.transform("mean")) / grp.transform("std")
    variable["z_score"] = variable["z_score"].round(2)
    out = variable[variable["z_score"] > z]
    cols = ["transaction_id", "date", "category", "description", "amount", "payment_method", "z_score"]
    return out[cols].sort_values("z_score", ascending=False).reset_index(drop=True)


def kpis(df: pd.DataFrame) -> dict:
    """Headline numbers for the report and dashboard."""
    monthly = monthly_trend(df)
    cats = category_summary(df)
    return {
        "total_spend": round(df["amount"].sum(), 2),
        "transactions": int(len(df)),
        "avg_monthly_spend": round(monthly["total"].mean(), 2),
        "avg_transaction": round(df["amount"].mean(), 2),
        "highest_month": monthly["total"].idxmax(),
        "highest_month_spend": round(monthly["total"].max(), 2),
        "lowest_month": monthly["total"].idxmin(),
        "lowest_month_spend": round(monthly["total"].min(), 2),
        "top_category": cats.index[0],
        "top_category_share": round(cats["share_pct"].iloc[0], 1),
        "avg_savings_rate": round(monthly["savings_rate_pct"].mean(), 1),
    }
