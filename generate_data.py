"""
generate_data.py

Generates realistic synthetic e-commerce business data
for the AI Business Intelligence Dashboard project.
"""

import os
import numpy as np
import pandas as pd


# ============================================================
# 1. CONFIGURATION
# ============================================================

START_DATE = "2026-01-01"
END_DATE = "2026-06-30"

RANDOM_SEED = 42

OUTPUT_DIR = "data"
OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "sample_business_data.csv"
)


# ============================================================
# 2. REPRODUCIBILITY
# ============================================================

np.random.seed(RANDOM_SEED)


# ============================================================
# 3. CREATE DATE RANGE
# ============================================================

dates = pd.date_range(
    start=START_DATE,
    end=END_DATE,
    freq="D"
)

df = pd.DataFrame({
    "date": dates
})


# ============================================================
# 4. BASIC TIME FEATURES
# ============================================================

df["day_of_week"] = df["date"].dt.dayofweek
df["day_of_month"] = df["date"].dt.day
df["month"] = df["date"].dt.month


# ============================================================
# 5. BUSINESS GROWTH TREND
# ============================================================

days = np.arange(len(df))

growth_factor = 1 + (days / len(df)) * 0.30


# ============================================================
# 6. WEEKLY SEASONALITY
# ============================================================

weekly_factor = np.where(
    df["day_of_week"].isin([4, 5]),
    1.15,
    np.where(
        df["day_of_week"].isin([0, 1]),
        0.90,
        1.00
    )
)


# ============================================================
# 7. MARKETING SPEND
# ============================================================

base_marketing_spend = 550

marketing_noise = np.random.normal(
    loc=0,
    scale=70,
    size=len(df)
)

df["marketing_spend"] = (
    base_marketing_spend
    * growth_factor
    * weekly_factor
    + marketing_noise
)


df["marketing_spend"] = (
    df["marketing_spend"]
    .clip(lower=300)
    .round(2)
)


# ============================================================
# 8. MARKETING CAMPAIGNS
# ============================================================

campaign_periods = [
    ("2026-02-10", "2026-02-16"),
    ("2026-04-05", "2026-04-12"),
    ("2026-06-15", "2026-06-21")
]

for start, end in campaign_periods:

    mask = (
        (df["date"] >= start)
        & (df["date"] <= end)
    )

    df.loc[mask, "marketing_spend"] *= 1.35


df["marketing_spend"] = df["marketing_spend"].round(2)


# ============================================================
# 9. WEBSITE TRAFFIC
# ============================================================

traffic_base = 1200

traffic_noise = np.random.normal(
    loc=0,
    scale=100,
    size=len(df)
)

df["website_traffic"] = (
    traffic_base
    * growth_factor
    * weekly_factor
    + df["marketing_spend"] * 1.4
    + traffic_noise
)


df["website_traffic"] = (
    df["website_traffic"]
    .clip(lower=500)
    .round()
    .astype(int)
)


# ============================================================
# 10. CONVERSION RATE
# ============================================================

base_conversion_rate = 0.030

conversion_noise = np.random.normal(
    loc=0,
    scale=0.003,
    size=len(df)
)

conversion_rate = (
    base_conversion_rate
    + conversion_noise
    + (growth_factor - 1) * 0.008
)


conversion_rate = np.clip(
    conversion_rate,
    0.018,
    0.055
)


# ============================================================
# 11. ORDERS
# ============================================================

orders = (
    df["website_traffic"]
    * conversion_rate
)

orders_noise = np.random.normal(
    loc=0,
    scale=4,
    size=len(df)
)

df["orders"] = (
    orders
    + orders_noise
).clip(lower=5).round().astype(int)


# ============================================================
# 12. AVERAGE ORDER VALUE
# ============================================================

base_aov = 85

aov_noise = np.random.normal(
    loc=0,
    scale=8,
    size=len(df)
)

average_order_value = (
    base_aov
    + aov_noise
    + (growth_factor - 1) * 15
)

average_order_value = np.clip(
    average_order_value,
    60,
    120
)


# ============================================================
# 13. REVENUE
# ============================================================

df["revenue"] = (
    df["orders"]
    * average_order_value
)

df["revenue"] = (
    df["revenue"]
    .round(2)
)


# ============================================================
# 14. NEW CUSTOMERS
# ============================================================

new_customer_ratio = np.random.uniform(
    0.65,
    0.82,
    len(df)
)

df["new_customers"] = (
    df["orders"]
    * new_customer_ratio
).round().astype(int)


# ============================================================
# 15. RETURNING CUSTOMERS
# ============================================================

df["returning_customers"] = (
    df["orders"]
    - df["new_customers"]
)

df["returning_customers"] = (
    df["returning_customers"]
    .clip(lower=0)
)


# ============================================================
# 16. KEEP ONLY BUSINESS COLUMNS
# ============================================================

df = df[
    [
        "date",
        "orders",
        "revenue",
        "website_traffic",
        "marketing_spend",
        "new_customers",
        "returning_customers"
    ]
]


# ============================================================
# 17. DATA TYPE CLEANUP
# ============================================================

df["date"] = pd.to_datetime(df["date"])

df["orders"] = df["orders"].astype(int)

df["website_traffic"] = (
    df["website_traffic"]
    .astype(int)
)

df["new_customers"] = (
    df["new_customers"]
    .astype(int)
)

df["returning_customers"] = (
    df["returning_customers"]
    .astype(int)
)


# ============================================================
# 18. SAVE DATASET
# ============================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False
)


# ============================================================
# 19. VALIDATION
# ============================================================

print("\n" + "=" * 60)
print("AI BUSINESS INTELLIGENCE DASHBOARD")
print("DATASET GENERATION COMPLETE")
print("=" * 60)

print(f"\nDataset saved to:")
print(OUTPUT_FILE)

print(f"\nRows: {len(df)}")
print(f"Columns: {len(df.columns)}")

print("\nDate range:")
print(f"Start: {df['date'].min().date()}")
print(f"End:   {df['date'].max().date()}")

print("\nMissing values:")
print(df.isnull().sum().sum())

print("\nDuplicate rows:")
print(df.duplicated().sum())

print("\nNegative values:")

numeric_columns = [
    "orders",
    "revenue",
    "website_traffic",
    "marketing_spend",
    "new_customers",
    "returning_customers"
]

for column in numeric_columns:

    negative_count = (
        df[column] < 0
    ).sum()

    print(
        f"{column}: {negative_count}"
    )

print("\nFirst 5 rows:")
print(df.head())

print("\nDataset statistics:")
print(df[numeric_columns].describe())

print("\n" + "=" * 60)