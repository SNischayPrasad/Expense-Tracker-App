"""
config.py
---------
One place for every setting the project uses.
Change values here instead of editing code in many files.
"""

from pathlib import Path

# ---------- Paths ----------
ROOT_DIR = Path(__file__).resolve().parent.parent
RAW_DATA_PATH = ROOT_DIR / "data" / "raw" / "expenses_raw.csv"
CLEAN_DATA_PATH = ROOT_DIR / "data" / "processed" / "expenses_clean.csv"
OUTPUT_DIR = ROOT_DIR / "outputs"
IMAGE_DIR = ROOT_DIR / "images"

# ---------- Simulation settings ----------
RANDOM_SEED = 42            # same seed -> same dataset every run (reproducible)
START_DATE = "2025-01-01"
END_DATE = "2025-12-31"
CURRENCY = "₹"
MONTHLY_INCOME = 75000      # used for savings-rate insights

# Category -> (average transactions per month, typical amount, amount spread)
# Amounts follow a log-normal distribution: most purchases are small,
# a few are large -- exactly like real spending.
CATEGORY_PROFILE = {
    "Food":          {"tx_per_month": 30, "mean": 250,  "sigma": 0.6},
    "Groceries":     {"tx_per_month": 8,  "mean": 1200, "sigma": 0.4},
    "Transport":     {"tx_per_month": 20, "mean": 150,  "sigma": 0.7},
    "Shopping":      {"tx_per_month": 4,  "mean": 1500, "sigma": 0.8},
    "Entertainment": {"tx_per_month": 4,  "mean": 600,  "sigma": 0.6},
    "Utilities":     {"tx_per_month": 3,  "mean": 1100, "sigma": 0.3},
    "Health":        {"tx_per_month": 2,  "mean": 800,  "sigma": 0.7},
    "Education":     {"tx_per_month": 1,  "mean": 2000, "sigma": 0.5},
    "Travel":        {"tx_per_month": 1,  "mean": 3500, "sigma": 0.8},
}

# Rent is a fixed monthly cost, generated separately on the 1st of each month
RENT_AMOUNT = 15000

# Festive / seasonal multipliers (month number -> spending multiplier)
# Oct-Nov = festival season (Diwali), Dec = holidays, May = summer trip
SEASONAL_MULTIPLIER = {5: 1.25, 10: 1.35, 11: 1.45, 12: 1.30}

PAYMENT_METHODS = ["UPI", "Credit Card", "Debit Card", "Cash", "Net Banking"]
PAYMENT_WEIGHTS = [0.50, 0.20, 0.12, 0.13, 0.05]

# ---------- Budgets (per month) ----------
MONTHLY_BUDGET = {
    "Rent": 15000,
    "Food": 7500,
    "Groceries": 9000,
    "Transport": 3500,
    "Shopping": 6000,
    "Entertainment": 2500,
    "Utilities": 3500,
    "Health": 2000,
    "Education": 2500,
    "Travel": 4000,
}

# Essential vs discretionary (want vs need) -- useful business insight
ESSENTIAL_CATEGORIES = {"Rent", "Groceries", "Utilities", "Health", "Education", "Transport"}

# z-score above which a single transaction is flagged as unusual
ANOMALY_Z_THRESHOLD = 3.0
