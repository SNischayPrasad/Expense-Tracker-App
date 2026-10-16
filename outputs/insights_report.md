# Expense Analysis Report
_Generated on 2026-10-16 from synthetic data (2025-01-01 to 2025-12-31)._

## Key metrics
| Metric | Value |
|---|---|
| Total spend | ₹728,338 |
| Transactions | 920 |
| Avg monthly spend | ₹60,695 |
| Avg transaction | ₹792 |
| Highest month | 2025-11 (₹94,959) |
| Top category | Rent (24.7%) |
| Avg savings rate | 19.1% |

## Data cleaning summary
| Step | Count |
|---|---|
| rows before | 943 |
| duplicates removed | 15 |
| unparseable dates dropped | 0 |
| missing amount dropped | 8 |
| negative amounts fixed | 6 |
| missing payment filled | 27 |
| missing description filled | 18 |
| invalid category dropped | 0 |
| rows after | 920 |

## Key insights
1. Total spending for the year was ₹728,338 across 920 transactions (average ₹60,695 per month).
2. 'Rent' is the largest category at 24.7% of all spending; the top 3 categories (Rent, Food, Shopping) make up 56.7%.
3. Highest spending month was 2025-11 (₹94,959); lowest was 2025-06 (₹45,261) — a gap of 110%.
4. Festive season (Oct–Dec) spending averaged ₹84,526/month, 60% higher than the rest of the year.
5. Average weekend daily spend (₹1,885) is 22% higher than weekdays (₹1,540) — mostly food, shopping and entertainment.
6. Discretionary (non-essential) spending is 42.1% of the total.
7. Average savings rate is 19.1% of a ₹75,000 monthly income; 3 month(s) had spending above income.
8. Budget was exceeded 53 times. Most frequent: Food (9 months), Utilities (8 months), Entertainment (8 months).
9. UPI is the most used payment method (36.0% of value).
10. 15 unusually large transactions were flagged (z-score > 3.0).

## Recommendations
- Reduce **Shopping** — it went ₹48,790 over budget in total this year. Set a weekly cap of ₹1,395.
- Reduce **Food** — it went ₹33,179 over budget in total this year. Set a weekly cap of ₹1,744.
- Reduce **Groceries** — it went ₹29,180 over budget in total this year. Set a weekly cap of ₹2,093.
- Create a separate 'festival fund' — save ~10% of income from Jan–Sep to absorb the Oct–Dec spike.
- Plan weekend meals/outings in advance; weekend spending is noticeably higher.
- Review flagged large transactions monthly to catch impulse buys or billing errors.
- Follow the 50/30/20 rule: 50% needs, 30% wants, 20% savings.

## Spending by category
| category      |    total |   average |   transactions |   largest |   share_pct |
|:--------------|---------:|----------:|---------------:|----------:|------------:|
| Rent          | 180000   |  15000    |             12 |  15000    |       24.71 |
| Food          | 120854   |    313.09 |            386 |   2212.56 |       16.59 |
| Shopping      | 112380   |   1971.57 |             57 |   9474.97 |       15.43 |
| Groceries     | 112271   |   1290.47 |             87 |   2995.37 |       15.41 |
| Utilities     |  54339.7 |   1358.49 |             40 |   3361.19 |        7.46 |
| Transport     |  44381.2 |    180.41 |            246 |    902.9  |        6.09 |
| Entertainment |  43255.9 |    831.84 |             52 |   3113.58 |        5.94 |
| Travel        |  30423.4 |   2765.76 |             11 |   8887.3  |        4.18 |
| Health        |  16197.1 |    809.86 |             20 |   2263.14 |        2.22 |
| Education     |  14235.9 |   1581.77 |              9 |   3249.62 |        1.95 |

## Monthly trend
| year_month   |   total |   transactions |   mom_change_pct |   rolling_3m_avg |   savings |   savings_rate_pct |
|:-------------|--------:|---------------:|-----------------:|-----------------:|----------:|-------------------:|
| 2025-01      | 54660.6 |             85 |           nan    |          54660.6 |  20339.4  |              27.12 |
| 2025-02      | 66811.2 |             80 |            22.23 |          60735.9 |   8188.75 |              10.92 |
| 2025-03      | 49280.3 |             74 |           -26.24 |          56917.4 |  25719.7  |              34.29 |
| 2025-04      | 49986.9 |             66 |             1.43 |          55359.5 |  25013.1  |              33.35 |
| 2025-05      | 50815.2 |             71 |             1.66 |          50027.4 |  24184.8  |              32.25 |
| 2025-06      | 45261.4 |             60 |           -10.93 |          48687.8 |  29738.6  |              39.65 |
| 2025-07      | 57924.4 |             79 |            27.98 |          51333.7 |  17075.6  |              22.77 |
| 2025-08      | 48658.7 |             69 |           -16    |          50614.8 |  26341.3  |              35.12 |
| 2025-09      | 51361.6 |             61 |             5.55 |          52648.2 |  23638.4  |              31.52 |
| 2025-10      | 80168.6 |             81 |            56.09 |          60062.9 |  -5168.56 |              -6.89 |
| 2025-11      | 94958.9 |             99 |            18.45 |          75496.4 | -19959    |             -26.61 |
| 2025-12      | 78449.9 |             95 |           -17.39 |          84525.8 |  -3449.88 |              -4.6  |

## Top 10 overspending events
| year_month   | category   |   budget |   actual |   variance |   utilisation_pct | overspent   |
|:-------------|:-----------|---------:|---------:|-----------:|------------------:|:------------|
| 2025-10      | Shopping   |     6000 |  21265.6 |   15265.6  |             354.4 | True        |
| 2025-11      | Food       |     7500 |  19974.8 |   12474.8  |             266.3 | True        |
| 2025-09      | Shopping   |     6000 |  16990.7 |   10990.7  |             283.2 | True        |
| 2025-11      | Travel     |     4000 |  14656.8 |   10656.8  |             366.4 | True        |
| 2025-12      | Groceries  |     9000 |  17916.8 |    8916.78 |             199.1 | True        |
| 2025-02      | Shopping   |     6000 |  12747.5 |    6747.5  |             212.5 | True        |
| 2025-08      | Groceries  |     9000 |  15292.7 |    6292.69 |             169.9 | True        |
| 2025-12      | Food       |     7500 |  13354.3 |    5854.28 |             178.1 | True        |
| 2025-01      | Shopping   |     6000 |  11767.9 |    5767.85 |             196.1 | True        |
| 2025-10      | Food       |     7500 |  13257.9 |    5757.94 |             176.8 | True        |

## Top 10 unusual transactions
| transaction_id   | date                | category   | description     |   amount | payment_method   |   z_score |
|:-----------------|:--------------------|:-----------|:----------------|---------:|:-----------------|----------:|
| TXN100429        | 2025-12-13 00:00:00 | Food       | Lunch           |  2212.56 | Credit Card      |      8.24 |
| TXN100012        | 2025-04-19 00:00:00 | Food       | Zomato order    |  1828.29 | Credit Card      |      6.57 |
| TXN100664        | 2025-07-16 00:00:00 | Transport  | Metro card      |   902.9  | Cash             |      5.2  |
| TXN100733        | 2025-05-24 00:00:00 | Transport  | Metro card      |   819.72 | Debit Card       |      4.6  |
| TXN100765        | 2025-10-01 00:00:00 | Food       | Swiggy order    |  1319.58 | Cash             |      4.37 |
| TXN100209        | 2025-12-21 00:00:00 | Transport  | Uber            |   780.33 | UPI              |      4.32 |
| TXN100251        | 2025-12-22 00:00:00 | Transport  | Fuel            |   763.39 | Cash             |      4.19 |
| TXN100475        | 2025-11-15 00:00:00 | Utilities  | Mobile recharge |  3361.19 | UPI              |      4.12 |
| TXN100151        | 2025-09-05 00:00:00 | Shopping   | Electronics     |  9474.97 | Credit Card      |      4.04 |
| TXN100651        | 2025-09-17 00:00:00 | Food       | Swiggy order    |  1159.71 | Debit Card       |      3.67 |
