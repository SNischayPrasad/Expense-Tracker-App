"""
insights.py
-----------
Converts numbers into plain-English insights and recommendations,
then writes a Markdown report to outputs/insights_report.md.
This is the "so what?" step that business stakeholders care about.
"""

from datetime import date

from src import analysis, config

C = config.CURRENCY


def generate_insights(df) -> list[str]:
    k = analysis.kpis(df)
    cats = analysis.category_summary(df)
    monthly = analysis.monthly_trend(df)
    weekday = analysis.weekday_pattern(df)["avg_daily_spend"]
    etype = analysis.expense_type_summary(df)
    over = analysis.overspending_report(analysis.budget_vs_actual(df))
    anomalies = analysis.detect_anomalies(df)
    pay = analysis.payment_method_summary(df)

    insights = []
    insights.append(
        f"Total spending for the year was {C}{k['total_spend']:,.0f} across {k['transactions']} transactions "
        f"(average {C}{k['avg_monthly_spend']:,.0f} per month)."
    )
    insights.append(
        f"'{k['top_category']}' is the largest category at {k['top_category_share']}% of all spending; "
        f"the top 3 categories ({', '.join(cats.index[:3])}) make up {cats['share_pct'].iloc[:3].sum():.1f}%."
    )
    insights.append(
        f"Highest spending month was {k['highest_month']} ({C}{k['highest_month_spend']:,.0f}); "
        f"lowest was {k['lowest_month']} ({C}{k['lowest_month_spend']:,.0f}) — a gap of "
        f"{100 * (k['highest_month_spend'] / k['lowest_month_spend'] - 1):.0f}%."
    )
    festive = monthly.loc[monthly.index.str[-2:].isin(["10", "11", "12"]), "total"].mean()
    normal = monthly.loc[~monthly.index.str[-2:].isin(["10", "11", "12"]), "total"].mean()
    insights.append(
        f"Festive season (Oct–Dec) spending averaged {C}{festive:,.0f}/month, "
        f"{100 * (festive / normal - 1):.0f}% higher than the rest of the year."
    )
    weekend = weekday[["Saturday", "Sunday"]].mean()
    weekdays = weekday.drop(["Saturday", "Sunday"]).mean()
    insights.append(
        f"Average weekend daily spend ({C}{weekend:,.0f}) is {100 * (weekend / weekdays - 1):.0f}% "
        f"higher than weekdays ({C}{weekdays:,.0f}) — mostly food, shopping and entertainment."
    )
    disc = etype.loc["Discretionary", "share_pct"] if "Discretionary" in etype.index else 0
    insights.append(f"Discretionary (non-essential) spending is {disc:.1f}% of the total.")
    insights.append(
        f"Average savings rate is {k['avg_savings_rate']}% of a {C}{config.MONTHLY_INCOME:,} monthly income; "
        f"{int((monthly['savings'] < 0).sum())} month(s) had spending above income."
    )
    if len(over):
        worst = over.groupby("category")["overspent"].count().sort_values(ascending=False)
        insights.append(
            f"Budget was exceeded {len(over)} times. Most frequent: "
            + ", ".join(f"{c} ({n} months)" for c, n in worst.head(3).items()) + "."
        )
    insights.append(
        f"{pay.index[0]} is the most used payment method ({pay['share_pct'].iloc[0]:.1f}% of value)."
    )
    insights.append(f"{len(anomalies)} unusually large transactions were flagged (z-score > {config.ANOMALY_Z_THRESHOLD}).")
    return insights


def generate_recommendations(df) -> list[str]:
    over = analysis.overspending_report(analysis.budget_vs_actual(df))
    recs = []
    if len(over):
        top = over.groupby("category")["variance"].sum().sort_values(ascending=False)
        for cat, extra in top.head(3).items():
            recs.append(f"Reduce **{cat}** — it went {C}{extra:,.0f} over budget in total this year. "
                        f"Set a weekly cap of {C}{config.MONTHLY_BUDGET[cat] / 4.3:,.0f}.")
    recs.append("Create a separate 'festival fund' — save ~10% of income from Jan–Sep to absorb the Oct–Dec spike.")
    recs.append("Plan weekend meals/outings in advance; weekend spending is noticeably higher.")
    recs.append("Review flagged large transactions monthly to catch impulse buys or billing errors.")
    recs.append("Follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings.")
    return recs


def write_report(df, cleaning_report: dict | None = None) -> str:
    k = analysis.kpis(df)
    cats = analysis.category_summary(df)
    monthly = analysis.monthly_trend(df)
    over = analysis.overspending_report(analysis.budget_vs_actual(df))
    anomalies = analysis.detect_anomalies(df)

    lines = [
        "# Expense Analysis Report",
        f"_Generated on {date.today().isoformat()} from synthetic data ({config.START_DATE} to {config.END_DATE})._",
        "",
        "## Key metrics",
        "| Metric | Value |", "|---|---|",
        f"| Total spend | {C}{k['total_spend']:,.0f} |",
        f"| Transactions | {k['transactions']} |",
        f"| Avg monthly spend | {C}{k['avg_monthly_spend']:,.0f} |",
        f"| Avg transaction | {C}{k['avg_transaction']:,.0f} |",
        f"| Highest month | {k['highest_month']} ({C}{k['highest_month_spend']:,.0f}) |",
        f"| Top category | {k['top_category']} ({k['top_category_share']}%) |",
        f"| Avg savings rate | {k['avg_savings_rate']}% |",
        "",
    ]
    if cleaning_report:
        lines += ["## Data cleaning summary", "| Step | Count |", "|---|---|"]
        lines += [f"| {key.replace('_', ' ')} | {val} |" for key, val in cleaning_report.items()]
        lines.append("")
    lines += ["## Key insights"] + [f"{i}. {t}" for i, t in enumerate(generate_insights(df), 1)] + [""]
    lines += ["## Recommendations"] + [f"- {r}" for r in generate_recommendations(df)] + [""]
    lines += ["## Spending by category", cats.to_markdown(), ""]
    lines += ["## Monthly trend", monthly.to_markdown(), ""]
    lines += ["## Top 10 overspending events", over.head(10).to_markdown(index=False), ""]
    lines += ["## Top 10 unusual transactions", anomalies.head(10).to_markdown(index=False), ""]

    text = "\n".join(lines)
    config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    (config.OUTPUT_DIR / "insights_report.md").write_text(text, encoding="utf-8")
    return text
