"""
main.py
-------
Runs the whole Expense Tracker pipeline end to end:

    generate data -> clean -> feature engineering -> analysis
    -> charts -> insights report -> CSV outputs

Usage:
    python main.py              # full pipeline with a fresh synthetic dataset
    python main.py --use-existing   # reuse data/raw/expenses_raw.csv (e.g. your own data)
"""

import argparse
import sys

import pandas as pd

from src import analysis, config, insights, visualization
from src.cleaning import add_features, clean_expenses, save_clean
from src.data_generator import generate_dataset

# Windows terminals sometimes can't print ₹ -> force UTF-8 output
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def banner(text):
    print("\n" + "=" * 60 + f"\n{text}\n" + "=" * 60)


def main(use_existing: bool = False):
    # Phase 2: data creation
    banner("STEP 1/6  Data creation")
    if use_existing and config.RAW_DATA_PATH.exists():
        raw = pd.read_csv(config.RAW_DATA_PATH)
        print(f"Loaded existing raw data: {len(raw)} rows")
    else:
        raw = generate_dataset()
        print(f"Generated synthetic data: {len(raw)} rows -> {config.RAW_DATA_PATH.relative_to(config.ROOT_DIR)}")
    print(raw.head())

    # Phase 3: cleaning
    banner("STEP 2/6  Data cleaning")
    clean, cleaning_report = clean_expenses(raw)

    # Phase 5: feature engineering
    banner("STEP 3/6  Feature engineering")
    df = add_features(clean)
    save_clean(df)
    print(f"Added columns: {[c for c in df.columns if c not in clean.columns]}")
    print(f"Saved clean data -> {config.CLEAN_DATA_PATH.relative_to(config.ROOT_DIR)}")

    # Phase 6: analysis
    banner("STEP 4/6  Analysis")
    tables = {
        "category_summary": analysis.category_summary(df),
        "monthly_trend": analysis.monthly_trend(df),
        "category_by_month": analysis.category_by_month(df),
        "payment_method_summary": analysis.payment_method_summary(df),
        "weekday_pattern": analysis.weekday_pattern(df),
        "budget_vs_actual": analysis.budget_vs_actual(df),
        "overspending_report": analysis.overspending_report(analysis.budget_vs_actual(df)),
        "anomalies": analysis.detect_anomalies(df),
    }
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, table in tables.items():
        table.to_csv(config.OUTPUT_DIR / f"{name}.csv", encoding="utf-8")
    print("Category summary:\n", tables["category_summary"])
    print("\nMonthly trend:\n", tables["monthly_trend"][["total", "mom_change_pct", "savings_rate_pct"]])

    # Phase 7: visualization
    banner("STEP 5/6  Visualization")
    visualization.generate_all_charts(df)

    # Phase 8: insights
    banner("STEP 6/6  Insights")
    insights.write_report(df, cleaning_report)
    for i, line in enumerate(insights.generate_insights(df), 1):
        print(f"{i:>2}. {line}")
    print("\nRecommendations:")
    for r in insights.generate_recommendations(df):
        print(" -", r.replace("**", ""))

    banner("DONE")
    print("Charts  -> images/")
    print("Tables  -> outputs/*.csv")
    print("Report  -> outputs/insights_report.md")
    print("Dashboard: streamlit run app.py")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Expense Tracker data science pipeline")
    parser.add_argument("--use-existing", action="store_true", help="reuse data/raw/expenses_raw.csv")
    main(parser.parse_args().use_existing)
