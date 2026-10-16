"""
data_generator.py
-----------------
Creates a realistic SYNTHETIC expense dataset (no real financial data needed).

How the simulation works:
1. For every month, each category gets a random number of transactions
   (Poisson distribution around its average).
2. Each transaction gets a random day, amount (log-normal), and payment method.
3. Festive months get a spending multiplier -> visible seasonal trends.
4. Weekends get slightly higher Food/Entertainment spending.
5. Rent is added on the 1st of every month (fixed cost).
6. We deliberately add "dirty data" (duplicates, missing values, typos,
   negative amounts) so the cleaning step has real work to do --
   just like data from real apps.
"""

import numpy as np
import pandas as pd

from src import config

DESCRIPTIONS = {
    "Food": ["Swiggy order", "Zomato order", "Cafe", "Lunch", "Street food", "Dinner out"],
    "Groceries": ["BigBasket", "Local kirana", "DMart", "Blinkit", "Vegetables"],
    "Transport": ["Uber", "Ola", "Metro card", "Auto", "Fuel"],
    "Shopping": ["Amazon", "Flipkart", "Myntra", "Clothes", "Electronics"],
    "Entertainment": ["Movie", "Netflix", "Spotify", "Concert", "Gaming"],
    "Utilities": ["Electricity bill", "Mobile recharge", "Internet bill", "Water bill"],
    "Health": ["Pharmacy", "Doctor visit", "Gym", "Lab test"],
    "Education": ["Online course", "Books", "Certification exam"],
    "Travel": ["Train ticket", "Flight", "Hotel", "Bus ticket"],
    "Rent": ["Monthly rent"],
}


def _random_amount(rng, mean, sigma):
    """Log-normal amount whose average is roughly `mean`."""
    mu = np.log(mean) - sigma**2 / 2
    return round(float(rng.lognormal(mu, sigma)), 2)


def generate_clean_expenses(seed: int = config.RANDOM_SEED) -> pd.DataFrame:
    """Generate the 'true' expense records before any dirt is added."""
    rng = np.random.default_rng(seed)
    months = pd.date_range(config.START_DATE, config.END_DATE, freq="MS")
    rows = []

    for month_start in months:
        days_in_month = month_start.days_in_month
        season = config.SEASONAL_MULTIPLIER.get(month_start.month, 1.0)

        # Fixed rent on the 1st
        rows.append({
            "date": month_start,
            "category": "Rent",
            "description": "Monthly rent",
            "amount": float(config.RENT_AMOUNT),
            "payment_method": "Net Banking",
        })

        for category, p in config.CATEGORY_PROFILE.items():
            # Festive months -> more transactions for discretionary categories
            lam = p["tx_per_month"] * (season if category in {"Shopping", "Food", "Entertainment", "Travel"} else 1)
            n_tx = rng.poisson(lam)
            for _ in range(n_tx):
                day = int(rng.integers(1, days_in_month + 1))
                date = month_start + pd.Timedelta(days=day - 1)
                amount = _random_amount(rng, p["mean"], p["sigma"]) * season
                # Weekend effect for fun spending
                if date.dayofweek >= 5 and category in {"Food", "Entertainment", "Shopping"}:
                    amount *= 1.3
                rows.append({
                    "date": date,
                    "category": category,
                    "description": rng.choice(DESCRIPTIONS[category]),
                    "amount": round(amount, 2),
                    "payment_method": rng.choice(config.PAYMENT_METHODS, p=config.PAYMENT_WEIGHTS),
                })

    df = pd.DataFrame(rows).sort_values("date").reset_index(drop=True)
    return df


def add_dirty_data(df: pd.DataFrame, seed: int = config.RANDOM_SEED) -> pd.DataFrame:
    """Inject realistic data-quality problems for the cleaning phase."""
    rng = np.random.default_rng(seed + 1)
    dirty = df.copy()
    dirty["date"] = dirty["date"].dt.strftime("%Y-%m-%d")
    n = len(dirty)

    # 1) Inconsistent category text (lowercase / extra spaces)
    idx = rng.choice(n, size=int(n * 0.05), replace=False)
    dirty.loc[idx, "category"] = dirty.loc[idx, "category"].str.lower() + "  "

    # 2) Missing payment methods and descriptions
    idx = rng.choice(n, size=int(n * 0.03), replace=False)
    dirty.loc[idx, "payment_method"] = np.nan
    idx = rng.choice(n, size=int(n * 0.02), replace=False)
    dirty.loc[idx, "description"] = np.nan

    # 3) A few missing amounts (cannot be recovered -> will be dropped)
    idx = rng.choice(n, size=8, replace=False)
    dirty.loc[idx, "amount"] = np.nan

    # 4) Negative amounts (data-entry errors / refunds entered wrongly)
    idx = rng.choice(n, size=6, replace=False)
    dirty.loc[idx, "amount"] = -dirty.loc[idx, "amount"]

    # 5) Amounts stored as text with currency symbol
    idx = rng.choice(n, size=10, replace=False)
    dirty["amount"] = dirty["amount"].astype(object)
    dirty.loc[idx, "amount"] = dirty.loc[idx, "amount"].apply(lambda v: f"₹{v}" if pd.notna(v) else v)

    # 6) Duplicate rows (same transaction saved twice)
    dupes = dirty.sample(15, random_state=seed)
    dirty = pd.concat([dirty, dupes], ignore_index=True)

    # 7) A different date format for some rows
    idx = rng.choice(len(dirty), size=12, replace=False)
    dirty.loc[idx, "date"] = pd.to_datetime(dirty.loc[idx, "date"]).dt.strftime("%d/%m/%Y")

    # Shuffle so problems are scattered, then add a transaction id
    dirty = dirty.sample(frac=1, random_state=seed).reset_index(drop=True)
    dirty.insert(0, "transaction_id", [f"TXN{100000 + i}" for i in range(len(dirty))])
    return dirty


def generate_dataset(save: bool = True) -> pd.DataFrame:
    """Full pipeline: clean simulation -> add dirt -> save CSV."""
    df = add_dirty_data(generate_clean_expenses())
    if save:
        config.RAW_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
        df.to_csv(config.RAW_DATA_PATH, index=False, encoding="utf-8")
    return df


if __name__ == "__main__":
    data = generate_dataset()
    print(data.head(10))
    print(f"\nGenerated {len(data)} rows -> {config.RAW_DATA_PATH}")
