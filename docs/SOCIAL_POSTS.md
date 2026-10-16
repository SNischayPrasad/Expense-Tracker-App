# 📣 Social Media Posts — Expense Tracker App

**GitHub URL:** https://github.com/SNischayPrasad/Expense-Tracker-App
_(This link only works after the repo has been created and pushed. See the end of this file.)_

**Images:** `images/social/`
| File | Size | Use |
|---|---|---|
| `slide_01_cover.png` … `slide_08_cta.png` | 1080×1080 | Instagram carousel · LinkedIn multi-image post |
| `linkedin_banner.png` | 1200×627 | LinkedIn single-image post |
| `images/11_dashboard_preview.jpg` | — | Instagram story / extra slide |

> Regenerate the images after changing data/config: `python main.py` then `python -m src.social_cards`

---

## 💼 LinkedIn — Version 1 (detailed, recommended)
Attach: all 8 slides (as a multi-image post), or `linkedin_banner.png`.

```
Where does my money actually go? 💸 I built a data science project to find out.

📊 Project: Expense Tracker App using Data Science

Real bank data is private, so I built a simulator that generates a year of realistic spending. It uses log-normal purchase amounts, fixed rent, festival-season spikes, and higher weekend spending. I also added messy records on purpose (duplicates, "₹1,200" text amounts, mixed date formats, missing values) so the cleaning step would be realistic.

🔧 What I built:
→ A data cleaning pipeline that fixes 6 types of data-quality issues and logs every fix (943 → 920 clean records)
→ Feature engineering: month, weekday, weekend flag, essential vs discretionary
→ Analysis: category share, month-over-month trend, savings rate, budget vs actual
→ Overspending alerts + z-score anomaly detection within each category
→ 10 charts + an auto-generated insights report
→ An interactive Streamlit dashboard with filters, alerts and an add-expense form

💡 Key findings:
• Spending jumped 60% in the festive season (Oct–Dec), and November went above income
• Daily spending is 22% higher on weekends
• Food went over budget in 9 of the 12 months
• 15 unusually large transactions were flagged automatically

📚 What I learned:
1️⃣ Data cleaning took more effort than the charts, and it mattered more
2️⃣ A number is only useful when it leads to a decision ("build a festival fund")
3️⃣ Grouping data before detecting outliers avoids false alarms

🛠 Tech: Python | Pandas | NumPy | Matplotlib | Seaborn | Plotly | Streamlit | Jupyter

🔗 Code, notebook & dashboard: https://github.com/SNischayPrasad/Expense-Tracker-App

I'd love feedback from data and finance folks. What would you add next: ML spending forecasts or auto-categorising bank SMS? 👇

#DataScience #DataAnalytics #Python #Pandas #Streamlit #DataVisualization #BusinessAnalytics #FinancialAnalysis #PersonalFinance #StudentProjects #OpenToWork #LearningInPublic
```

---

## 💼 LinkedIn — Version 2 (short)
Attach: `linkedin_banner.png`

```
New project: an Expense Tracker built with Data Science 💰

I simulated a year of spending (920 transactions), cleaned the messy data, and analysed it with Python:

📈 Festive-season spending was 60% higher than normal months
🗓 Weekend daily spending was 22% higher
🚨 53 budget breaches + 15 unusual transactions caught automatically

All of it is in an interactive Streamlit dashboard with filters and budget alerts.

Tech: Python · Pandas · Seaborn · Plotly · Streamlit
Code 👉 https://github.com/SNischayPrasad/Expense-Tracker-App

#DataAnalytics #Python #Streamlit #DataScience #StudentProjects
```

---

## 💼 LinkedIn — "Projects" section entry (profile)
- **Name:** Expense Tracker App using Data Science
- **Skills:** Python, Pandas, Data Cleaning, Exploratory Data Analysis, Data Visualization, Streamlit
- **Description:**
```
End-to-end personal finance analytics project. Simulated 12 months of realistic expense data, built a cleaning pipeline (duplicates, mixed formats, nulls), engineered time-based features, and analysed category share, monthly trends, savings rate and budget vs actual variance. Added z-score anomaly detection and an interactive Streamlit dashboard. Findings: 60% festive-season spending spike, 22% higher weekend spending, 53 budget breaches.
```
- **Link:** https://github.com/SNischayPrasad/Expense-Tracker-App

---

## 📸 Instagram — Carousel caption
Post: all 8 slides in order (`slide_01` → `slide_08`).

```
Where does your money actually go? 💸👀

I built an Expense Tracker using Data Science to find out 📊

Swipe to see what a year of spending data revealed ➡️

✨ Festive season = 60% more spending 🎆
✨ Weekends cost 22% more 🍕🎬
✨ Food went over budget in 9 of 12 months 😅
✨ Unusual transactions were flagged automatically 🚨

Built with Python 🐍 Pandas, Seaborn, Plotly & Streamlit, with a full interactive dashboard 💻

Code is on my GitHub 🔗 (link in bio)

Would you track your own spending like this? Tell me in the comments 👇

.
.
.
#datascience #python #dataanalytics #coding #programming #codinglife #studentlife #engineeringstudent #pythonprojects #datavisualization #personalfinance #moneytips #budgeting #streamlit #pandas #techstudent #learntocode #100daysofcode #developer #indianstudent
```

**Bio link:** set your Instagram bio/link to `https://github.com/SNischayPrasad/Expense-Tracker-App` (Instagram doesn't make links in captions clickable).

## 📸 Instagram — Story / Reel text
Story 1 (dashboard screenshot): `Built my own expense analytics dashboard 💻📊`
Story 2 (slide_03_kpis): `Festive season = +60% spending 😳`
Story 3 (slide_08_cta): `Code on GitHub 🔗` + **link sticker** with the GitHub URL

**Reel idea (15–20 s):** screen-record `python main.py` running → charts appearing → clicking through the dashboard tabs. On-screen text: "I analysed a year of spending with Python 🐍" → "+60% in festive season 😳" → "Built a dashboard 💻" → "Code on GitHub 🔗". Use a trending audio.

---

## ✅ Posting checklist
1. Push the code to GitHub first, so the link works.
2. Replace the placeholders in `README.md` (`<your-username>` → `SNischayPrasad`, LinkedIn URL).
3. Post on LinkedIn on a Tuesday–Thursday morning (8–10 AM) for the best reach.
4. Reply to every comment in the first hour.
5. Add the project to your LinkedIn **Projects** and **Featured** sections.
