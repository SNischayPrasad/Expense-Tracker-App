"""
app.py — Interactive Streamlit dashboard
Run:  streamlit run app.py

Features:
- KPI cards, filters (month, category, payment method)
- Category, monthly, weekday and budget charts
- Overspending alerts and unusual transactions
- "Add expense" form (simple user input) saved to data/raw/user_expenses.csv
"""

from datetime import date

import pandas as pd
import plotly.express as px
import streamlit as st

from src import analysis, config, insights
from src.cleaning import add_features, clean_expenses
from src.data_generator import generate_dataset

USER_FILE = config.ROOT_DIR / "data" / "raw" / "user_expenses.csv"

st.set_page_config(page_title="Expense Tracker", page_icon="💰", layout="wide")


@st.cache_data
def load_data(user_file_mtime: float) -> pd.DataFrame:
    raw = pd.read_csv(config.RAW_DATA_PATH) if config.RAW_DATA_PATH.exists() else generate_dataset()
    if USER_FILE.exists():
        raw = pd.concat([raw, pd.read_csv(USER_FILE)], ignore_index=True)
    clean, _ = clean_expenses(raw, verbose=False)
    return add_features(clean)


mtime = USER_FILE.stat().st_mtime if USER_FILE.exists() else 0.0
data = load_data(mtime)

# ---------------- Sidebar ----------------
st.sidebar.title("💰 Expense Tracker")
months = sorted(data["year_month"].unique())
month_range = st.sidebar.select_slider("Month range", options=months, value=(months[0], months[-1]))
cats = st.sidebar.multiselect("Categories", sorted(data["category"].unique()), default=sorted(data["category"].unique()))
pays = st.sidebar.multiselect("Payment methods", sorted(data["payment_method"].unique()),
                              default=sorted(data["payment_method"].unique()))

df = data[(data["year_month"] >= month_range[0]) & (data["year_month"] <= month_range[1])
          & data["category"].isin(cats) & data["payment_method"].isin(pays)]

with st.sidebar.expander("➕ Add an expense"):
    with st.form("add_expense", clear_on_submit=True):
        d = st.date_input("Date", value=date(2025, 12, 31))
        c = st.selectbox("Category", list(config.MONTHLY_BUDGET))
        desc = st.text_input("Description", "Manual entry")
        amt = st.number_input("Amount (₹)", min_value=1.0, value=500.0, step=50.0)
        pm = st.selectbox("Payment method", config.PAYMENT_METHODS)
        if st.form_submit_button("Save"):
            row = pd.DataFrame([{"transaction_id": f"USR{pd.Timestamp.now():%Y%m%d%H%M%S}",
                                 "date": d.strftime("%Y-%m-%d"), "category": c, "description": desc,
                                 "amount": amt, "payment_method": pm}])
            row.to_csv(USER_FILE, mode="a", header=not USER_FILE.exists(), index=False)
            st.success("Saved! Dashboard refreshed.")
            st.rerun()

if df.empty:
    st.warning("No data for these filters.")
    st.stop()

# ---------------- KPIs ----------------
st.title("Personal Expense Analytics Dashboard")
st.caption("Synthetic data · Python · Pandas · Plotly · Streamlit")
k = analysis.kpis(df)
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Total spend", f"₹{k['total_spend']:,.0f}")
c2.metric("Transactions", f"{k['transactions']:,}")
c3.metric("Avg / month", f"₹{k['avg_monthly_spend']:,.0f}")
c4.metric("Top category", k["top_category"], f"{k['top_category_share']}% of spend", delta_color="off")
c5.metric("Avg savings rate", f"{k['avg_savings_rate']}%")

# ---------------- Charts ----------------
tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "📅 Trends", "🎯 Budget", "🚨 Alerts"])

with tab1:
    left, right = st.columns(2)
    cs = analysis.category_summary(df).reset_index()
    left.plotly_chart(px.bar(cs, x="total", y="category", orientation="h", title="Spending by category",
                             labels={"total": "₹"}).update_yaxes(categoryorder="total ascending"),
                      width="stretch")
    right.plotly_chart(px.pie(cs, values="total", names="category", hole=0.45, title="Category share"),
                       width="stretch")
    left, right = st.columns(2)
    pm = analysis.payment_method_summary(df).reset_index()
    left.plotly_chart(px.bar(pm, x="payment_method", y="transactions", title="Payment methods"),
                      width="stretch")
    et = analysis.expense_type_summary(df).reset_index()
    right.plotly_chart(px.pie(et, values="total", names="expense_type", title="Essential vs discretionary"),
                       width="stretch")

with tab2:
    mt = analysis.monthly_trend(df).reset_index()
    fig = px.line(mt, x="year_month", y=["total", "rolling_3m_avg"], markers=True, title="Monthly spending trend")
    fig.add_hline(y=config.MONTHLY_INCOME, line_dash="dot", line_color="green", annotation_text="Income")
    st.plotly_chart(fig, width="stretch")
    cbm = analysis.category_by_month(df).reset_index().melt(id_vars="year_month", var_name="category", value_name="amount")
    st.plotly_chart(px.bar(cbm, x="year_month", y="amount", color="category", title="Monthly breakdown"),
                    width="stretch")
    wd = analysis.weekday_pattern(df).reset_index()
    st.plotly_chart(px.bar(wd, x="weekday", y="avg_daily_spend", title="Average daily spend by weekday"),
                    width="stretch")

with tab3:
    bva = analysis.budget_vs_actual(df)
    avg = bva.groupby("category")[["budget", "actual"]].mean().reset_index()
    st.plotly_chart(px.bar(avg.melt(id_vars="category"), x="category", y="value", color="variable",
                           barmode="group", title="Average monthly budget vs actual"), width="stretch")
    heat = bva.pivot(index="category", columns="year_month", values="utilisation_pct")
    st.plotly_chart(px.imshow(heat, color_continuous_scale="RdYlGn_r", color_continuous_midpoint=100,
                              text_auto=".0f", aspect="auto", title="Budget utilisation % (>100 = overspent)"),
                    width="stretch")

with tab4:
    over = analysis.overspending_report(analysis.budget_vs_actual(df))
    st.subheader(f"⚠️ Overspending events: {len(over)}")
    st.dataframe(over, width="stretch", hide_index=True)
    st.subheader("🔍 Unusually large transactions")
    st.dataframe(analysis.detect_anomalies(df), width="stretch", hide_index=True)

st.divider()
st.subheader("💡 Insights")
for line in insights.generate_insights(df):
    st.markdown(f"- {line}")
st.subheader("✅ Recommendations")
for r in insights.generate_recommendations(df):
    st.markdown(f"- {r}")

with st.expander("View filtered data"):
    st.dataframe(df, width="stretch", hide_index=True)
    st.download_button("Download CSV", df.to_csv(index=False).encode("utf-8"), "filtered_expenses.csv")
