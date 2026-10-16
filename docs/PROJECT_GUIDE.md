# 📘 Expense Tracker App using Data Science — Complete Project Guide

This guide explains everything in this repo: the concepts, the architecture, every phase, how to run it, how to upload it to GitHub, how to collect proof, and how to talk about it in interviews.

---

## 1️⃣ Project Explanation

### What is an Expense Tracker App?
**Simple explanation:** It is a digital notebook for your money. Every time you spend, you record *when*, *on what*, *how much*, and *how you paid*. The app then tells you where your money goes, whether you're overspending, and how to save more.

**Technical explanation:** It is a data pipeline that ingests transactional records (date, category, amount, payment_method). It validates and cleans them and derives temporal and behavioural features. It aggregates them along several dimensions (category, time, payment channel), compares the totals against budget constraints, detects statistical outliers, and presents the results through static reports and an interactive BI-style dashboard.

### Why is it important?
- **Visibility:** most people underestimate small, frequent spends (food delivery, cabs).
- **Control:** budgets only work if you measure against them.
- **Planning:** past patterns, like festival spikes, help you plan future savings.
- **Early warning:** anomalies can reveal fraud, billing errors, or impulse buys.

### How individuals and companies use it
| User | Use |
|---|---|
| Individuals / students | Track pocket money and salary, cut wasteful spending, save for goals |
| Families | Shared household budget, rent/utility planning |
| Startups / SMEs | Monitor operating expenses, vendor costs, employee reimbursements |
| Corporates | Expense management (SAP Concur, Zoho Expense), policy-violation checks, cost-centre reporting |
| Finance teams | Budget vs actual variance analysis, forecasting, audit trails |

### Real-world use cases
- **Personal finance tracking:** which categories eat the most money each month.
- **Business expense monitoring:** department-wise spend and flagging out-of-policy claims.
- **Budgeting and cost control:** setting a limit for each category and alerting when it's crossed (this project's budget-vs-actual module).
- **Financial planning:** using monthly trends and seasonality to plan savings (e.g. a "festival fund").

### Workflow
```
Data Input ──► Storage ──► Analysis ──► Visualization ──► Insights ──► Decision-making
(generator/    (CSV in      (Pandas     (Matplotlib,      (insights.py  ("cut Shopping by
 user form)     data/)       groupbys)   Seaborn, Plotly)   report)       20%, build festival fund")
```

---

## 2️⃣ Tech Stack Options

| | Option A — Easy | Option B — Intermediate ⭐ | Option C — Advanced |
|---|---|---|---|
| Language | Python | Python | Python + SQL + JS |
| Data | Excel / CSV | CSV, synthetic generator | PostgreSQL / Firebase, bank APIs |
| Libraries | Pandas, Matplotlib | Pandas, NumPy, Matplotlib, Seaborn, Plotly | + Scikit-learn, Prophet, FastAPI |
| Visualization | Matplotlib charts | Static charts + Plotly | Power BI / Tableau / React dashboards |
| App / dashboard | ❌ Jupyter only | ✅ Streamlit dashboard | ✅ Full web/mobile app with login |
| ML | ❌ | Statistical anomaly detection (z-score) | Forecasting, NLP auto-categorisation |
| Difficulty | ⭐ | ⭐⭐ | ⭐⭐⭐⭐ |
| Time | 1–2 days | 4–6 days | 3–6 weeks |

### ✅ Selected: Option B (Intermediate)
It's what this repo implements. It is fast enough to finish in a week and covers every skill analyst recruiters look for (Pandas, cleaning, EDA, visualization, business insights, a dashboard). It's also modular, so you can grow it into Option C later.

---

## 3️⃣ Project Architecture

### Text-based architecture diagram
```
┌──────────────────────────── INPUT LAYER ────────────────────────────┐
│  data_generator.py (synthetic)      app.py "Add expense" form (user) │
│        │                                     │                       │
│        ▼                                     ▼                       │
│  data/raw/expenses_raw.csv          data/raw/user_expenses.csv       │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌────────────────────────── PROCESSING LAYER ─────────────────────────┐
│ cleaning.py                                                          │
│   ├─ remove duplicates      ├─ parse mixed date formats              │
│   ├─ "₹1,200" → 1200.0      ├─ fix negatives, drop missing amounts   │
│   ├─ standardise categories └─ fill missing payment/description      │
│   └─ add_features(): month, weekday, weekend, quarter,               │
│                      essential/discretionary, amount bucket          │
│        ▼                                                             │
│ data/processed/expenses_clean.csv                                    │
│        ▼                                                             │
│ analysis.py                                                          │
│   ├─ category_summary      ├─ monthly_trend (MoM, rolling, savings)  │
│   ├─ category_by_month     ├─ weekday_pattern / payment summary      │
│   ├─ budget_vs_actual  →   overspending_report                       │
│   └─ detect_anomalies (z-score per category), kpis                   │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌──────────────────────────── OUTPUT LAYER ───────────────────────────┐
│ visualization.py → images/*.png (10 charts)                          │
│ insights.py      → outputs/insights_report.md (insights + recs)      │
│ main.py          → outputs/*.csv (8 analysis tables)                 │
│ app.py           → interactive Streamlit dashboard                   │
└─────────────────────────────────────────────────────────────────────┘
```

### Data flow
1. **Input:** each record = `transaction_id, date, category, description, amount, payment_method`.
2. **Cleaning** turns 943 messy rows into 920 valid rows, and every fix is counted in a cleaning report.
3. **Feature engineering** adds 11 columns that make grouping easy (e.g. `year_month`, `is_weekend`).
4. **Aggregation:** `groupby` and `pivot_table` collapse transactions into category, month, and weekday summaries.
5. **Trend analysis:** `pct_change()` for month-over-month change, `rolling(3)` for smoothing, income minus spend for savings.
6. **Budget check:** the actual spend for each category and month is compared with `MONTHLY_BUDGET`, and variance and utilisation % are computed.
7. **Anomaly detection:** z-score of each amount within its category; anything above 3σ is flagged.
8. **Output:** charts, CSVs, a Markdown report, and the dashboard.

---

## 4️⃣ Implementation Plan (Phase-wise)

| Phase | What to do | Why | Expected output | Mistakes to avoid |
|---|---|---|---|---|
| **1. Setup** | Install Python, create the folder structure, venv, `pip install -r requirements.txt`, `git init` | Reproducible, isolated environment | Working venv, empty repo skeleton | Installing libraries globally; forgetting to activate the venv |
| **2. Data creation** | `src/data_generator.py`: simulate 12 months with Poisson counts and log-normal amounts, seasonality, weekend effect; inject dirty data | No real data available; dirt makes cleaning realistic | `data/raw/expenses_raw.csv` (~943 rows) | Uniform random amounts (unrealistic); no random seed (results change every run) |
| **3. Cleaning** | `clean_expenses()`: duplicates, date formats, currency strings, negatives, nulls, label case | Garbage in → garbage out | Cleaning report + 920 clean rows | Silently dropping rows without logging; `fillna(0)` on amounts (fakes data) |
| **4. EDA** | `notebooks/expense_eda.ipynb`: shape, info, nulls, value counts, describe, distributions | Understand the data before modelling | Notebook with observations | Skipping EDA and jumping straight to charts |
| **5. Feature engineering** | `add_features()`: month, weekday, weekend, quarter, essential/discretionary, amount bucket | Enables time and behaviour analysis | 11 new columns, `expenses_clean.csv` | Using string months for sorting (Apr before Jan!) — use `YYYY-MM` |
| **6. Analysis** | `analysis.py`: category, monthly, MoM, savings, weekday, payment, budget, anomalies | Answers the business questions | 8 CSV tables in `outputs/` | Including fixed rent in weekday/anomaly analysis (it distorts the results) |
| **7. Visualization** | `visualization.py`: 10 charts; `app.py`: dashboard | People understand pictures faster than tables | `images/*.png`, live dashboard | Pie charts with 10 tiny slices; no titles/labels; 3D charts |
| **8. Insights** | `insights.py`: turn numbers into sentences and recommendations | Stakeholders want "so what?" | `outputs/insights_report.md` | Stating numbers without meaning or action |
| **9. GitHub upload** | README, screenshots, `.gitignore`, meaningful commits, push | Public proof of work | Polished public repo | Pushing `venv/`; one giant "final" commit; no README images |

---

## 5️⃣ Folder Structure

```
Expense-Tracker-App/
│
├── data/
│   ├── raw/              ← original/messy data (never edit by hand)
│   └── processed/        ← cleaned, analysis-ready data
├── notebooks/            ← Jupyter notebooks for exploration (EDA)
├── src/                  ← reusable Python modules (the "engine")
│   ├── __init__.py       ← makes src an importable package
│   ├── config.py         ← settings: categories, budgets, income, paths
│   ├── data_generator.py ← synthetic data simulation
│   ├── cleaning.py       ← cleaning + feature engineering
│   ├── analysis.py       ← all calculations
│   ├── visualization.py  ← static charts
│   └── insights.py       ← text insights + report
├── outputs/              ← generated tables (CSV) and report (MD)
├── images/               ← charts and screenshots used in README
├── docs/                 ← this guide
├── app.py                ← Streamlit dashboard
├── main.py               ← one command runs the whole pipeline
├── requirements.txt      ← library list for pip
├── .gitignore            ← files Git should ignore (venv, caches)
└── README.md             ← the project's front page on GitHub
```
**Why this layout?** It separates raw data, logic, and results, which is how real data teams organise projects (similar to the "Cookiecutter Data Science" template). Recruiters notice this.

---

## 6️⃣ Installation Guide

### Step 1 — Install Python
- Download Python 3.10 or newer from https://www.python.org/downloads/
- **Windows:** tick ✅ **"Add Python to PATH"** during install.
- Check: `python --version` (Mac: `python3 --version`)

### Step 2 — Get the project
```bash
cd Expense-Tracker-App
```

### Step 3 — Create and activate a virtual environment
| | Windows (PowerShell / CMD) | Mac / Linux |
|---|---|---|
| Create | `python -m venv venv` | `python3 -m venv venv` |
| Activate | `venv\Scripts\activate` | `source venv/bin/activate` |
| Deactivate | `deactivate` | `deactivate` |

When it's active, you'll see `(venv)` at the start of the terminal line.

> PowerShell error *"running scripts is disabled"*? Run once:
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

### Step 4 — Install libraries
```bash
pip install -r requirements.txt
```

### Step 5 — Verify
```bash
python -c "import pandas, seaborn, streamlit, plotly; print('All good!')"
```

---

## 7️⃣ Full Project Code

All the code is in the repo and runs as-is. Here's what each file does and the key ideas in it.

| File | Lines | Role |
|---|---|---|
| `src/config.py` | ~70 | Central settings: categories with average count/amount/spread, rent, seasonal multipliers, payment weights, budgets, income |
| `src/data_generator.py` | ~140 | Simulation + dirty-data injection |
| `src/cleaning.py` | ~100 | 8 cleaning steps + feature engineering |
| `src/analysis.py` | ~120 | 10 analysis functions |
| `src/visualization.py` | ~170 | 10 charts |
| `src/insights.py` | ~130 | Insight sentences, recommendations, Markdown report |
| `main.py` | ~100 | Orchestrates the 6 steps |
| `app.py` | ~140 | Streamlit dashboard |
| `notebooks/expense_eda.ipynb` | — | EDA walkthrough |

### Key code ideas (explained)

**Realistic amounts (log-normal):**
```python
mu = np.log(mean) - sigma**2 / 2      # makes the average ≈ mean
amount = rng.lognormal(mu, sigma)     # many small spends, a few big ones
```

**Number of transactions per month (Poisson):**
```python
n_tx = rng.poisson(tx_per_month * season)   # e.g. Food ≈ 30/month, more in festive months
```

**Cleaning currency strings:**
```python
df["amount"] = df["amount"].astype(str).str.replace("₹", "").str.replace(",", "").astype(float)
```

**Parsing two date formats:**
```python
iso = pd.to_datetime(df["date"], format="%Y-%m-%d", errors="coerce")
dmy = pd.to_datetime(df["date"], format="%d/%m/%Y", errors="coerce")
df["date"] = iso.fillna(dmy)
```

**Month-over-month change and savings:**
```python
out["mom_change_pct"] = out["total"].pct_change() * 100
out["savings_rate_pct"] = 100 * (INCOME - out["total"]) / INCOME
```

**Overspending detection:**
```python
actual > config.MONTHLY_BUDGET[category]   # for every category × month cell
```

**Anomaly detection (z-score within category):**
```python
z = (amount - category_mean) / category_std   # flag if z > 3
```

---

## 8️⃣ Virtual Simulation

### How expenses are generated
| Category | Avg tx / month | Typical amount (₹) | Notes |
|---|---|---|---|
| Rent | 1 (fixed, 1st of month) | 15,000 | Net Banking |
| Food | 30 | 250 | +30% on weekends, festive boost |
| Groceries | 8 | 1,200 | |
| Transport | 20 | 150 | |
| Shopping | 4 | 1,500 | High spread, festive boost |
| Entertainment | 4 | 600 | Weekend + festive boost |
| Utilities | 3 | 1,100 | Low spread (bills are stable) |
| Health | 2 | 800 | |
| Education | 1 | 2,000 | |
| Travel | 1 | 3,500 | Festive boost |

Payment method mix: UPI 50%, Credit Card 20%, Cash 13%, Debit Card 12%, Net Banking 5%.

### How trends appear
- **Seasonality:** `SEASONAL_MULTIPLIER = {5: 1.25, 10: 1.35, 11: 1.45, 12: 1.30}`. Amounts *and* transaction counts rise in May (summer), Oct–Nov (Diwali), and Dec (holidays). The analysis then *rediscovers* this as a festive-season uplift of about 60%.
- **Weekend effect:** Food/Entertainment/Shopping amounts × 1.3 on Sat/Sun → weekend daily spend about 22% higher.
- **Randomness:** Poisson counts and log-normal amounts make each month different, as real life is.

### How overspending is detected
1. Sum the actual spend for each category and month (a pivot table).
2. Compare it with `MONTHLY_BUDGET[category]`.
3. `variance = actual − budget`, `utilisation % = actual / budget × 100`.
4. `overspent = actual > budget` → collected in `overspending_report.csv`, coloured red in the heatmap, listed in the dashboard "Alerts" tab.
5. Single unusually large purchases are caught separately by the z-score anomaly detector.

### Step-by-step simulation
```
Step 1 → Seed the random generator (seed=42) so results are reproducible
Step 2 → For each of the 12 months: add rent on day 1
Step 3 → For each category: draw a Poisson count → for each transaction pick
         a random day, a log-normal amount, a description, and a payment method
Step 4 → Apply the seasonal multiplier and the weekend boost
Step 5 → Inject dirt: 5% lowercase/space categories, 3% missing payment,
         2% missing description, 8 missing amounts, 6 negatives,
         10 "₹123" strings, 15 duplicates, 12 dd/mm/yyyy dates
Step 6 → Shuffle, add transaction IDs, save data/raw/expenses_raw.csv (943 rows)
Step 7 → Clean → 920 rows; engineer features → data/processed/expenses_clean.csv
Step 8 → Analyse → 8 CSV tables in outputs/
Step 9 → Visualise → 10 PNG charts in images/
Step 10 → Generate insights → outputs/insights_report.md
Step 11 → Explore interactively → streamlit run app.py
```

### What to screenshot and save as proof
| Proof | How |
|---|---|
| Terminal output of `python main.py` (cleaning report + insights) | Screenshot the terminal |
| Raw vs clean data preview | Notebook cells `raw.head(10)` and `df.head()` |
| All 10 charts | Already saved in `images/` |
| Dashboard: KPI row, each tab, alerts table | Browser screenshots |
| Add-expense form working | Screenshot before and after adding an entry |
| `insights_report.md` rendered on GitHub | Screenshot |
| GitHub commit history | Screenshot of the commits page |

---

## 9️⃣ How to Run the Project

```bash
# 1. activate venv first (see section 6)
python main.py                     # full pipeline (~10 seconds)
python main.py --use-existing      # reuse existing raw CSV (e.g. your own data)
python -m src.data_generator       # only generate data
streamlit run app.py               # dashboard → http://localhost:8501
jupyter notebook notebooks/expense_eda.ipynb   # EDA notebook
```

### Expected terminal output (abridged)
```
STEP 1/6  Data creation      → Generated synthetic data: 943 rows
STEP 2/6  Data cleaning      → duplicates_removed: 15, missing_amount_dropped: 8,
                               negative_amounts_fixed: 6, missing_payment_filled: 27 ... rows_after: 920
STEP 3/6  Feature engineering→ Added columns: year, month, ..., expense_type, amount_bucket
STEP 4/6  Analysis           → category summary + monthly trend tables
STEP 5/6  Visualization      → saved 01_...png ... 10_...png
STEP 6/6  Insights           → 10 insights + recommendations
```

### Generated files
- `images/01_category_spending_bar.png` … `10_amount_distribution.png`
- `outputs/category_summary.csv, monthly_trend.csv, category_by_month.csv, payment_method_summary.csv, weekday_pattern.csv, budget_vs_actual.csv, overspending_report.csv, anomalies.csv`
- `outputs/insights_report.md`

---

## 🔟 GitHub Upload Steps

### 1. Create the repo on GitHub
- github.com → **New repository**
- **Name:** `Expense-Tracker-App` (or `expense-tracker-data-science`)
- **Description:** `End-to-end expense analytics project in Python: synthetic data simulation, data cleaning, EDA, budget vs actual, anomaly detection, automated insights and an interactive Streamlit dashboard.`
- Public ✅, **do not** add a README (you already have one).

### 2. Connect and push (run inside the project folder)
```bash
git init
git add .
git commit -m "Initial commit: project structure and pipeline"
git branch -M main
git remote add origin https://github.com/<your-username>/Expense-Tracker-App.git
git push -u origin main
```
`venv/` is excluded by `.gitignore`. Check with `git status` before committing.

### 3. Good commit messages (one per milestone)
```
chore: set up project structure, venv and requirements
feat: add synthetic expense data generator with seasonality
feat: add data cleaning pipeline with cleaning report
feat: add feature engineering (time, weekend, expense type)
feat: add category, monthly trend and budget analysis
feat: add z-score anomaly detection
feat: add 10 static charts with matplotlib/seaborn
feat: add automated insights and recommendations report
feat: add interactive Streamlit dashboard
docs: add EDA notebook, README with screenshots and project guide
```

### 4. Topics / tags (repo → ⚙ About → Topics)
`data-science` `data-analysis` `python` `pandas` `numpy` `matplotlib` `seaborn` `plotly` `streamlit` `expense-tracker` `personal-finance` `budgeting` `eda` `data-visualization` `business-analytics` `financial-analysis` `anomaly-detection`

### 5. Extras
- Pin the repo on your GitHub profile.
- Optional: deploy free on **Streamlit Community Cloud** (share.streamlit.io → New app → choose the repo → `app.py`). Put the live link in the README and on your resume.

---

## 1️⃣1️⃣ README.md
The complete README is in the repo root: [`README.md`](../README.md). It covers the overview, problem, solution, features, tech stack, structure, how to run, results, screenshots, future work, and author. Replace `<your-username>` and the LinkedIn placeholders.

---

## 1️⃣2️⃣ Proof-Building Strategy (5 days)

| Day | Work | Commits | Proof to save |
|---|---|---|---|
| **Day 1 — Setup** | Install Python, create venv, folder structure, `config.py`, requirements, `.gitignore`, push an empty skeleton | `chore: set up project structure...` | Screenshot of the folder tree + first commit on GitHub |
| **Day 2 — Dataset** | Write `data_generator.py`, generate raw CSV, explore it in the notebook | `feat: add synthetic expense data generator...` | `raw.head(10)`, `raw.isna().sum()`, value counts showing messy labels |
| **Day 3 — Cleaning + analysis** | `cleaning.py`, `add_features()`, `analysis.py` | `feat: add data cleaning...`, `feat: add feature engineering...`, `feat: add category, monthly...`, `feat: add z-score anomaly...` | Cleaning report in the terminal, `category_summary` and `monthly_trend` tables |
| **Day 4 — Visualization** | `visualization.py`, `app.py` | `feat: add 10 static charts...`, `feat: add interactive Streamlit dashboard` | All PNGs + dashboard screenshots (each tab) |
| **Day 5 — Final upload** | `insights.py`, README with images, guide, final push, LinkedIn post | `feat: add automated insights...`, `docs: add README...` | Repo home page, commit history, insights report, LinkedIn post |

**LinkedIn post idea:** "Built an Expense Tracker with Data Science 💰. Simulated a year of spending, cleaned 943 messy records, and found a 60% festive-season spike and 22% higher weekend spending. Also built a Streamlit dashboard with budget alerts. Code: <link> #DataAnalytics #Python"

---

## 1️⃣3️⃣ Screenshots / Outputs to Capture

| # | Capture | Source | Shows |
|---|---|---|---|
| 1 | Dataset preview (raw) | notebook `raw.head(10)` | Messy data: ₹ strings, lowercase categories, NaNs |
| 2 | Dataset preview (clean) | notebook `df.head()` | Clean data + engineered columns |
| 3 | Cleaning report | terminal after `python main.py` | Data-quality fixes with counts |
| 4 | Category-wise spending (bar) | `images/01_category_spending_bar.png` | Where money goes |
| 5 | Category share (pie) | `images/02_category_share_pie.png` | % split |
| 6 | Monthly trend (line) | `images/03_monthly_trend_line.png` | Festive spike vs income and budget |
| 7 | Monthly stacked bar | `images/04_monthly_category_stacked.png` | Category mix over time |
| 8 | Category × month heatmap | `images/05_category_month_heatmap.png` | Hot spots |
| 9 | Weekday pattern | `images/06_weekday_pattern.png` | Weekend effect |
| 10 | Payment methods | `images/07_payment_methods.png` | UPI dominance |
| 11 | Budget vs actual | `images/08_budget_vs_actual.png` | Overspending categories |
| 12 | Budget utilisation heatmap | `images/09_budget_utilisation_heatmap.png` | Which months/categories broke budget |
| 13 | Amount distribution | `images/10_amount_distribution.png` | Log-normal spending |
| 14 | Final dashboard (all tabs + Alerts) | `streamlit run app.py` | Interactive product |
| 15 | Insights report | `outputs/insights_report.md` on GitHub | Business storytelling |

---

## 1️⃣4️⃣ Interview Preparation

### HR explanation (30 seconds, non-technical)
> "I built an expense tracker that analyses a year of spending data to show where money goes, when people overspend, and how they could save more. I didn't have access to real bank data, so I simulated realistic data with festival spikes and weekend habits. I cleaned it, analysed it in Python, and built an interactive dashboard with budget alerts. For example, it found that spending rises 60% during the festive season. Based on that, it recommends building a festival fund. The project taught me to turn raw data into decisions."

### Technical explanation (2 minutes)
> "It's a modular Python pipeline. `data_generator.py` simulates 12 months of transactions. Counts come from a Poisson distribution and amounts from a log-normal distribution per category, with seasonal and weekend multipliers. I then inject realistic data-quality issues: duplicates, mixed date formats, currency strings, nulls, and negatives. `cleaning.py` fixes these and logs each fix. It then engineers features such as year_month, weekday, is_weekend, quarter, and essential vs discretionary. `analysis.py` uses groupby and pivot tables for category share, MoM growth with `pct_change`, a 3-month rolling average, savings rate, budget-vs-actual variance, and z-score anomaly detection within each category. Outputs are 10 Matplotlib/Seaborn charts, CSV tables, an auto-generated Markdown insights report, and a Streamlit + Plotly dashboard with filters, alerts, and a form to add expenses."

### 10 Interview Questions and Answers

**1. Why synthetic data? Isn't that "fake"?**
Real financial data is private. I designed the generator to copy real patterns (log-normal amounts, seasonality, weekend effect) and messy data quality. The pipeline itself is data-agnostic: `python main.py --use-existing` runs on any CSV with the same columns, such as a real bank export.

**2. Why a log-normal distribution for amounts?**
Spending is always positive and right-skewed: many small purchases and a few large ones. A normal distribution could produce negative values and wouldn't have that long right tail. The histogram (`10_amount_distribution.png`) confirms the shape.

**3. What data-cleaning steps did you do and why?**
I did eight: remove duplicates, standardise category case and spaces, parse two date formats, strip ₹ and commas and convert to float, drop rows with a missing amount (it can't be guessed), take the absolute value of negatives (entry errors), fill missing payment method and description with "Unknown"/"Not specified", and keep only valid categories. 943 rows → 920.

**4. Why not fill missing amounts with the mean?**
The amount is the target metric. Imputing it would invent money that was never spent and bias the totals. Missing categorical fields don't affect the totals, so I labelled them "Unknown" instead of dropping rows.

**5. How do you detect overspending?**
For each category and month, I compare actual spend with the budget and compute variance (actual − budget) and utilisation %. Anything above 100% is flagged. The heatmap shows this visually; for example, Food went over budget in 9 of 12 months.

**6. How does anomaly detection work, and what are its limits?**
It uses a z-score *within each category*: (amount − category mean) / category std > 3. Grouping by category matters because ₹3,000 is normal for Travel but unusual for Food. Limits: the mean and std are themselves affected by outliers, and the data is skewed. Improvements would be IQR or median-based (MAD) scores, z-scores on log-amounts, or Isolation Forest.

**7. What is the difference between essential and discretionary spending, and why track it?**
Essentials are needs (rent, groceries, utilities, health, education, transport). Discretionary spending is wants (food out, shopping, entertainment, travel). Discretionary spending is where cuts are possible. Here it's 42%, above the 30% "wants" share in the 50/30/20 rule, which supports the recommendation to cut it.

**8. What are your key insights?**
- The festive season (Oct–Dec) is 60% above the normal monthly spend.
- Weekend daily spend is 22% higher.
- Rent, Food, and Shopping make up about 57% of spending.
- The average savings rate is 19%, but 3 months were negative.
- Shopping and Food had the biggest budget overruns (₹49K and ₹33K).

**9. How would you make it production-ready / scale it?**
- Store data in SQLite/PostgreSQL instead of CSV.
- Add user authentication.
- Ingest bank statements or SMS and auto-categorise them with NLP.
- Schedule the pipeline (cron/Airflow).
- Add unit tests (pytest) and CI.
- Deploy the dashboard (Streamlit Cloud/Docker).
- Add forecasting (Prophet/ARIMA) and alerting (email/push).

**10. How is this relevant to a Business/Financial Analyst role?**
It's the same workflow analysts use for company expense management. They also clean transactional data, run budget-vs-actual variance analysis, examine cost drivers by category and department, study seasonality for forecasting, detect policy violations or anomalies, and present KPIs on dashboards with recommendations.

### Bonus quick-fire questions
- *groupby vs pivot_table?* groupby is general aggregation. pivot_table reshapes the result into a 2-D matrix (months × categories).
- *Why `YYYY-MM` instead of month names?* It sorts correctly as text and stays unique across years.
- *Why `random_seed`?* Reproducibility: the same results every run, which matters for testing and review.
- *Why Streamlit?* It builds a full interactive dashboard in pure Python with no HTML/JS, so prototypes are fast.

---

## 1️⃣5️⃣ Future Improvements

| Improvement | How |
|---|---|
| 📱 Mobile app | Flutter / React Native front end + FastAPI back end; or a PWA |
| ⚡ Real-time tracking | Parse bank SMS/UPI notifications or use Account Aggregator APIs (India); store in a database; refresh the dashboard live |
| 🤖 AI spending prediction | Forecast next month per category with Prophet/ARIMA/XGBoost on lag features; show confidence intervals |
| 🏷 Auto-categorisation | NLP classifier (TF-IDF + Logistic Regression) on transaction descriptions |
| 🔔 Budgeting alerts | Trigger email/Telegram/push when utilisation passes 80% and 100% mid-month |
| 🎯 Financial goal tracking | Goals (laptop, trip, emergency fund), with progress bars and a projected completion date |
| 👥 Multi-user / business mode | Departments, cost centres, approval workflow, receipt OCR |
| 🧪 Quality | pytest unit tests, GitHub Actions CI, type hints, Docker |

---

## 1️⃣6️⃣ Troubleshooting

| Error / problem | Cause | Solution |
|---|---|---|
| `'python' is not recognized` | Python not on PATH | Reinstall and tick "Add to PATH", or use `py` on Windows / `python3` on Mac |
| `venv\Scripts\activate` — "running scripts is disabled" | PowerShell execution policy | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `ModuleNotFoundError: No module named 'pandas'` | venv not active, or libraries not installed | Activate the venv, then `pip install -r requirements.txt` |
| `ModuleNotFoundError: No module named 'src'` | Running from the wrong folder | `cd Expense-Tracker-App`, then run `python main.py` (not `python src/main.py`) |
| `UnicodeEncodeError ... '₹'` (₹) | Windows console encoding | `main.py` already forces UTF-8; otherwise run `set PYTHONIOENCODING=utf-8` (CMD) or `$env:PYTHONIOENCODING="utf-8"` (PowerShell) |
| `ImportError: Missing optional dependency 'tabulate'` | `to_markdown` needs tabulate | `pip install tabulate` |
| `streamlit: command not found` | venv not active | Activate the venv, or `python -m streamlit run app.py` |
| Port 8501 already in use | Another Streamlit is running | `streamlit run app.py --server.port 8502` |
| Charts not appearing in a window | Script uses the `Agg` backend (saves files) | Open the PNGs in `images/`, or use the notebook/dashboard |
| Notebook: `FileNotFoundError ../data/raw/...` | Pipeline not run yet | Run `python main.py` first |
| `git push` rejected / auth failed | GitHub needs a token, not a password | Use a Personal Access Token or GitHub Desktop; or `gh auth login` |
| `venv/` uploaded to GitHub | `.gitignore` added too late | `git rm -r --cached venv` then commit |
| Different numbers than the README | Changed seed/config | Expected. Results depend on `RANDOM_SEED` and `config.py` |
