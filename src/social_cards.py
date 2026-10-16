"""
social_cards.py
---------------
Builds ready-to-post images for LinkedIn / Instagram from the project's results.
Run after main.py:   python -m src.social_cards

Outputs (images/social/):
  slide_01 ... slide_08.png  -> 1080x1080 carousel (Instagram + LinkedIn document/carousel)
  linkedin_banner.png        -> 1200x627 single image for a LinkedIn post
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.image as mpimg
import matplotlib.pyplot as plt
import pandas as pd
from matplotlib.patches import FancyBboxPatch

from src import analysis, config
from src.cleaning import add_features

GITHUB_URL = "github.com/SNischayPrasad/Expense-Tracker-App"
OUT = config.IMAGE_DIR / "social"

BG, CARD, TEXT, MUTED = "#0F172A", "#1E293B", "#F8FAFC", "#94A3B8"
ACCENT, GREEN, RED, AMBER = "#38BDF8", "#4ADE80", "#F87171", "#FBBF24"


def _canvas(w=10.8, h=10.8):
    fig = plt.figure(figsize=(w, h), dpi=100, facecolor=BG)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
    return fig, ax


def _card(ax, x, y, w, h, color=CARD):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.025",
                                facecolor=color, edgecolor="none"))


def _footer(ax, n, total=8):
    ax.text(0.06, 0.04, "Expense Tracker · Data Science Project", color=MUTED, fontsize=13)
    ax.text(0.94, 0.04, f"{n}/{total}", color=MUTED, fontsize=13, ha="right")


def _title(ax, kicker, title):
    ax.text(0.06, 0.92, kicker.upper(), color=ACCENT, fontsize=16, fontweight="bold")
    ax.text(0.06, 0.855, title, color=TEXT, fontsize=34, fontweight="bold", va="center")


def _image_slide(path, n, kicker, title, caption):
    fig, ax = _canvas()
    _title(ax, kicker, title)
    img = mpimg.imread(path)
    h, w = img.shape[:2]
    box_w, box_h = 0.88, 0.62
    scale = min(box_w / w, box_h / h * 1.0)  # canvas is square so units match
    iw, ih = w * scale, h * scale
    x0, y0 = 0.5 - iw / 2, 0.78 - ih
    _card(ax, x0 - 0.015, y0 - 0.015, iw + 0.03, ih + 0.03, color="#FFFFFF")
    ax.imshow(img, extent=(x0, x0 + iw, y0, y0 + ih), aspect="auto", zorder=3)
    ax.text(0.06, y0 - 0.08, caption, color=TEXT, fontsize=19, va="center")
    _footer(ax, n)
    return fig


def _save(fig, name):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / name, facecolor=BG)
    plt.close(fig)
    print(f"  saved images/social/{name}")


def build(df):
    k = analysis.kpis(df)
    monthly = analysis.monthly_trend(df)
    festive_mask = monthly.index.str[-2:].isin(["10", "11", "12"])
    festive_uplift = 100 * (monthly.loc[festive_mask, "total"].mean() / monthly.loc[~festive_mask, "total"].mean() - 1)
    wd = analysis.weekday_pattern(df)["avg_daily_spend"]
    weekend_uplift = 100 * (wd[["Saturday", "Sunday"]].mean() / wd.drop(["Saturday", "Sunday"]).mean() - 1)
    over = analysis.overspending_report(analysis.budget_vs_actual(df))
    n_anom = len(analysis.detect_anomalies(df))
    raw_rows = len(pd.read_csv(config.RAW_DATA_PATH))

    # ---- Slide 1: cover ----
    fig, ax = _canvas()
    ax.text(0.06, 0.80, "DATA SCIENCE PROJECT", color=ACCENT, fontsize=20, fontweight="bold")
    ax.text(0.06, 0.66, "Where does my\nmoney actually go?", color=TEXT, fontsize=54, fontweight="bold", va="center", linespacing=1.1)
    ax.text(0.06, 0.50, "An end-to-end Expense Tracker built with Python:\nsimulation → cleaning → analysis → dashboard",
            color=MUTED, fontsize=21, va="center", linespacing=1.4)
    stack = ["Python", "Pandas", "NumPy", "Seaborn", "Plotly", "Streamlit"]
    for i, s in enumerate(stack):
        x, y = 0.06 + (i % 3) * 0.2, 0.37 - (i // 3) * 0.08
        _card(ax, x, y, 0.18, 0.06, color=CARD)
        ax.text(x + 0.09, y + 0.03, s, color=TEXT, fontsize=16, ha="center", va="center")
    ax.text(0.06, 0.17, f"₹{k['total_spend']/1e5:.1f}L analysed · {k['transactions']} transactions · 12 months",
            color=GREEN, fontsize=20, fontweight="bold")
    ax.text(0.94, 0.08, "Swipe →", color=ACCENT, fontsize=22, ha="right", fontweight="bold")
    _save(fig, "slide_01_cover.png")

    # ---- Slide 2: pipeline ----
    fig, ax = _canvas()
    _title(ax, "How it works", "The pipeline")
    steps = [
        ("1  Simulate", f"{raw_rows} realistic transactions with festive & weekend patterns"),
        ("2  Clean", "Duplicates, ₹ strings, mixed dates, nulls, negatives fixed"),
        ("3  Engineer", "Month, weekday, weekend, essential vs discretionary"),
        ("4  Analyse", "Category share, MoM trend, savings rate, budget vs actual"),
        ("5  Detect", "Overspending + z-score anomaly detection"),
        ("6  Present", "10 charts, auto insights report, Streamlit dashboard"),
    ]
    for i, (head, body) in enumerate(steps):
        y = 0.70 - i * 0.105
        _card(ax, 0.06, y, 0.88, 0.085)
        ax.text(0.09, y + 0.0425, head, color=ACCENT, fontsize=21, fontweight="bold", va="center")
        ax.text(0.33, y + 0.0425, body, color=TEXT, fontsize=16, va="center")
    _footer(ax, 2)
    _save(fig, "slide_02_pipeline.png")

    # ---- Slide 3: KPI cards ----
    fig, ax = _canvas()
    _title(ax, "Results", "The numbers")
    cards = [
        (f"+{festive_uplift:.0f}%", "festive-season (Oct–Dec)\nspending vs normal months", AMBER),
        (f"+{weekend_uplift:.0f}%", "higher daily spend\non weekends", ACCENT),
        (f"{k['avg_savings_rate']:.0f}%", "average savings rate\n(3 months went negative)", GREEN),
        (f"{len(over)}", "budget breaches found\nacross categories × months", RED),
        (f"{k['top_category_share']:.0f}%", f"of spending goes to\n{k['top_category']} (largest category)", ACCENT),
        (f"{n_anom}", "unusually large\ntransactions flagged", AMBER),
    ]
    for i, (big, small, color) in enumerate(cards):
        col, row = i % 2, i // 2
        x, y = 0.06 + col * 0.45, 0.56 - row * 0.2
        _card(ax, x, y, 0.43, 0.18)
        ax.text(x + 0.03, y + 0.12, big, color=color, fontsize=40, fontweight="bold", va="center")
        ax.text(x + 0.03, y + 0.045, small, color=MUTED, fontsize=15, va="center", linespacing=1.3)
    _footer(ax, 3)
    _save(fig, "slide_03_kpis.png")

    # ---- Slides 4-7: charts + dashboard ----
    img = config.IMAGE_DIR
    slides = [
        (img / "03_monthly_trend_line.png", "Trend", "Festive spike is real",
         f"Spending peaked in Nov at ₹{k['highest_month_spend']:,.0f} — above income."),
        (img / "01_category_spending_bar.png", "Categories", "Where the money goes",
         "Rent, Food and Shopping make up more than half of all spending."),
        (img / "09_budget_utilisation_heatmap.png", "Budget", "Overspending heatmap",
         "Red cells = over budget. Food broke its budget in 9 of 12 months."),
        (img / "11_dashboard_preview.jpg", "Dashboard", "Interactive Streamlit app",
         "Filters, KPIs, trends, budget alerts and an add-expense form."),
    ]
    for n, (p, kicker, title, cap) in enumerate(slides, start=4):
        fig = _image_slide(p, n, kicker, title, cap)
        _save(fig, f"slide_{n:02d}_{kicker.lower()}.png")

    # ---- Slide 8: takeaways + CTA ----
    fig, ax = _canvas()
    _title(ax, "Takeaways", "What I learned")
    points = [
        "Cleaning took more effort than charting — and mattered more",
        "Insights need a 'so what': every number → a recommendation",
        "Grouping before outlier detection avoids false alarms",
        "A dashboard makes analysis usable by non-technical people",
    ]
    for i, p in enumerate(points):
        y = 0.72 - i * 0.09
        ax.text(0.07, y, "✓", color=GREEN, fontsize=24, fontweight="bold", va="center")
        ax.text(0.12, y, p, color=TEXT, fontsize=18, va="center")
    _card(ax, 0.06, 0.15, 0.88, 0.17, color=ACCENT)
    ax.text(0.5, 0.265, "Full code, notebook & dashboard", color=BG, fontsize=20, ha="center", va="center")
    ax.text(0.5, 0.20, GITHUB_URL, color=BG, fontsize=23, fontweight="bold", ha="center", va="center")
    _footer(ax, 8)
    _save(fig, "slide_08_cta.png")

    # ---- LinkedIn single image 1200x627 ----
    fig, ax = _canvas(12, 6.27)
    ax.text(0.05, 0.84, "DATA SCIENCE PROJECT", color=ACCENT, fontsize=17, fontweight="bold")
    ax.text(0.05, 0.66, "Expense Tracker App", color=TEXT, fontsize=34, fontweight="bold", va="center")
    ax.text(0.05, 0.50, "Python · Pandas · Seaborn · Plotly · Streamlit", color=MUTED, fontsize=18, va="center")
    stats = [(f"+{festive_uplift:.0f}%", "festive spike", AMBER), (f"+{weekend_uplift:.0f}%", "weekend spend", ACCENT),
             (f"{len(over)}", "budget breaches", RED)]
    for i, (big, small, color) in enumerate(stats):
        x = 0.05 + i * 0.16
        ax.text(x, 0.30, big, color=color, fontsize=30, fontweight="bold", va="center")
        ax.text(x, 0.18, small, color=MUTED, fontsize=14, va="center")
    ax.text(0.05, 0.06, GITHUB_URL, color=TEXT, fontsize=14)
    shot = mpimg.imread(img / "03_monthly_trend_line.png")
    h, w = shot.shape[:2]
    iw = 0.40; ih = iw * (h / w) * (12 / 6.27)
    _card(ax, 0.565, 0.5 - ih / 2 - 0.02, iw + 0.02, ih + 0.04, color="#FFFFFF")
    ax.imshow(shot, extent=(0.575, 0.575 + iw, 0.5 - ih / 2, 0.5 + ih / 2), aspect="auto", zorder=3)
    _save(fig, "linkedin_banner.png")


if __name__ == "__main__":
    clean = pd.read_csv(config.CLEAN_DATA_PATH, parse_dates=["date"])
    build(add_features(clean[["transaction_id", "date", "category", "description", "amount", "payment_method"]]))
