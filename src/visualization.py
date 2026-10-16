"""
visualization.py
----------------
Creates every chart and saves it as a PNG inside images/.
These PNGs are your GitHub "proof" screenshots and go into the README.
"""

import matplotlib
matplotlib.use("Agg")  # save files without opening windows (works on any machine)
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns

from src import analysis, config

sns.set_theme(style="whitegrid", palette="deep")
plt.rcParams.update({"figure.dpi": 110, "axes.titleweight": "bold", "axes.titlesize": 13})

RUPEE = mticker.FuncFormatter(lambda x, _: f"{x/1000:.0f}k" if x >= 1000 else f"{x:.0f}")


def _save(fig, name):
    config.IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    path = config.IMAGE_DIR / name
    fig.tight_layout()
    fig.savefig(path, bbox_inches="tight")
    plt.close(fig)
    return path


def plot_category_bar(df):
    cats = analysis.category_summary(df)
    fig, ax = plt.subplots(figsize=(10, 5.5))
    sns.barplot(x=cats["total"], y=cats.index, ax=ax, color="#4C72B0")
    for i, (total, share) in enumerate(zip(cats["total"], cats["share_pct"])):
        ax.text(total, i, f"  ₹{total:,.0f} ({share:.1f}%)", va="center", fontsize=9)
    ax.set_title("Total Spending by Category (2025)")
    ax.set_xlabel("Amount (₹)"); ax.set_ylabel("")
    ax.xaxis.set_major_formatter(RUPEE)
    ax.set_xlim(0, cats["total"].max() * 1.3)
    return _save(fig, "01_category_spending_bar.png")


def plot_category_pie(df):
    cats = analysis.category_summary(df)
    # Group tiny slices into "Other" so the pie stays readable
    main = cats[cats["share_pct"] >= 4]["total"]
    other = cats[cats["share_pct"] < 4]["total"].sum()
    if other > 0:
        main["Other"] = other
    fig, ax = plt.subplots(figsize=(8, 8))
    ax.pie(main, labels=main.index, autopct="%1.1f%%", startangle=90,
           colors=sns.color_palette("Set2", len(main)), wedgeprops={"edgecolor": "white"})
    ax.set_title("Share of Spending by Category")
    return _save(fig, "02_category_share_pie.png")


def plot_monthly_trend(df):
    m = analysis.monthly_trend(df)
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(m.index, m["total"], marker="o", linewidth=2.5, label="Monthly spend")
    ax.plot(m.index, m["rolling_3m_avg"], linestyle="--", label="3-month average")
    ax.axhline(config.MONTHLY_INCOME, color="green", linestyle=":", label=f"Income (₹{config.MONTHLY_INCOME:,})")
    ax.axhline(sum(config.MONTHLY_BUDGET.values()), color="red", linestyle=":", label="Total budget")
    peak = m["total"].idxmax()
    ax.annotate(f"Peak: ₹{m.loc[peak, 'total']:,.0f}", xy=(peak, m.loc[peak, "total"]),
                xytext=(0, 15), textcoords="offset points", ha="center", fontweight="bold")
    ax.set_title("Monthly Spending Trend")
    ax.set_ylabel("Amount (₹)"); ax.set_xlabel("")
    ax.yaxis.set_major_formatter(RUPEE)
    ax.tick_params(axis="x", rotation=45)
    ax.legend(loc="upper left")
    return _save(fig, "03_monthly_trend_line.png")


def plot_stacked_monthly(df):
    pivot = analysis.category_by_month(df)
    pivot = pivot[pivot.sum().sort_values(ascending=False).index]
    fig, ax = plt.subplots(figsize=(12, 6))
    pivot.plot(kind="bar", stacked=True, ax=ax, colormap="tab20", width=0.8)
    ax.set_title("Monthly Spending Breakdown by Category")
    ax.set_ylabel("Amount (₹)"); ax.set_xlabel("")
    ax.yaxis.set_major_formatter(RUPEE)
    ax.legend(bbox_to_anchor=(1.01, 1), loc="upper left", fontsize=9)
    ax.tick_params(axis="x", rotation=45)
    return _save(fig, "04_monthly_category_stacked.png")


def plot_heatmap(df):
    pivot = analysis.category_by_month(df).T
    fig, ax = plt.subplots(figsize=(13, 6))
    sns.heatmap(pivot / 1000, annot=True, fmt=".1f", cmap="YlOrRd", ax=ax, cbar_kws={"label": "₹ thousands"})
    ax.set_title("Spending Heatmap (₹ thousands) — Category × Month")
    ax.set_xlabel(""); ax.set_ylabel("")
    return _save(fig, "05_category_month_heatmap.png")


def plot_weekday(df):
    w = analysis.weekday_pattern(df)
    colors = ["#DD8452" if d in ("Saturday", "Sunday") else "#4C72B0" for d in w.index]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.bar(w.index, w["avg_daily_spend"], color=colors)
    ax.set_title("Average Daily Spend by Weekday (weekends in orange)")
    ax.set_ylabel("Amount (₹)")
    return _save(fig, "06_weekday_pattern.png")


def plot_payment_methods(df):
    p = analysis.payment_method_summary(df)
    fig, ax = plt.subplots(figsize=(8, 4.5))
    sns.barplot(x=p.index, y=p["transactions"], ax=ax, color="#55A868")
    ax.set_title("Transactions by Payment Method")
    ax.set_ylabel("Number of transactions"); ax.set_xlabel("")
    return _save(fig, "07_payment_methods.png")


def plot_budget_vs_actual(df):
    b = analysis.budget_vs_actual(df)
    avg = b.groupby("category")[["budget", "actual"]].mean().sort_values("actual", ascending=False)
    fig, ax = plt.subplots(figsize=(11, 5))
    x = range(len(avg))
    ax.bar([i - 0.2 for i in x], avg["budget"], width=0.4, label="Budget", color="#8C8C8C")
    bar_colors = ["#C44E52" if a > bud else "#55A868" for a, bud in zip(avg["actual"], avg["budget"])]
    ax.bar([i + 0.2 for i in x], avg["actual"], width=0.4, label="Avg actual", color=bar_colors)
    ax.set_xticks(list(x)); ax.set_xticklabels(avg.index, rotation=30)
    ax.set_title("Average Monthly Budget vs Actual (red = over budget)")
    ax.set_ylabel("Amount (₹)")
    ax.yaxis.set_major_formatter(RUPEE)
    ax.legend()
    return _save(fig, "08_budget_vs_actual.png")


def plot_overspending_heatmap(df):
    b = analysis.budget_vs_actual(df)
    pivot = b.pivot(index="category", columns="year_month", values="utilisation_pct")
    fig, ax = plt.subplots(figsize=(13, 6))
    sns.heatmap(pivot, annot=True, fmt=".0f", cmap="RdYlGn_r", center=100, ax=ax,
                cbar_kws={"label": "% of budget used"})
    ax.set_title("Budget Utilisation % (above 100 = overspent)")
    ax.set_xlabel(""); ax.set_ylabel("")
    return _save(fig, "09_budget_utilisation_heatmap.png")


def plot_amount_distribution(df):
    variable = df[df["category"] != "Rent"]
    fig, ax = plt.subplots(figsize=(9, 4.5))
    sns.histplot(variable["amount"], bins=60, log_scale=True, ax=ax, color="#8172B3")
    ax.set_title("Distribution of Transaction Amounts (log scale, excl. rent)")
    ax.set_xlabel("Amount (₹)")
    return _save(fig, "10_amount_distribution.png")


def generate_all_charts(df):
    funcs = [plot_category_bar, plot_category_pie, plot_monthly_trend, plot_stacked_monthly,
             plot_heatmap, plot_weekday, plot_payment_methods, plot_budget_vs_actual,
             plot_overspending_heatmap, plot_amount_distribution]
    paths = [f(df) for f in funcs]
    for p in paths:
        print(f"  saved {p.name}")
    return paths
