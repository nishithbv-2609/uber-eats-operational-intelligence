
import pandas as pd
from pathlib import Path

# Locate the raw data folder
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = PROJECT_ROOT / "data" / "raw"

# Load all datasets
customers = pd.read_csv(DATA_DIR / "customers.csv")
restaurants = pd.read_csv(DATA_DIR / "restaurants.csv")
drivers = pd.read_csv(DATA_DIR / "drivers.csv")
orders = pd.read_csv(DATA_DIR / "orders.csv")
deliveries = pd.read_csv(DATA_DIR / "deliveries.csv")
reviews = pd.read_csv(DATA_DIR / "reviews.csv")
payments = pd.read_csv(DATA_DIR / "payments.csv")

datasets = {
    "customers": (customers, "customer_id"),
    "restaurants": (restaurants, "restaurant_id"),
    "drivers": (drivers, "driver_id"),
    "orders": (orders, "order_id"),
    "deliveries": (deliveries, "delivery_id"),
    "reviews": (reviews, "review_id"),
    "payments": (payments, "payment_id"),
}

print("=" * 50)
print("DATASET SUMMARY")
print("=" * 50)

for name, (df, id_column) in datasets.items():
    print(f"\n{name.upper()}")
    print(f"Rows: {len(df):,}")
    print(f"Columns: {len(df.columns)}")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Duplicate IDs: {df[id_column].duplicated().sum()}")

# Check relationships between datasets
checks = {
    "Orders -> Customers": orders["customer_id"].isin(
        customers["customer_id"]
    ).all(),

    "Orders -> Restaurants": orders["restaurant_id"].isin(
        restaurants["restaurant_id"]
    ).all(),

    "Deliveries -> Orders": deliveries["order_id"].isin(
        orders["order_id"]
    ).all(),

    "Deliveries -> Drivers": deliveries["driver_id"].isin(
        drivers["driver_id"]
    ).all(),

    "Reviews -> Orders": reviews["order_id"].isin(
        orders["order_id"]
    ).all(),

    "Payments -> Orders": payments["order_id"].isin(
        orders["order_id"]
    ).all(),
}

# Ensure only completed orders have deliveries and reviews
completed_order_ids = set(
    orders.loc[orders["order_status"] == "Completed", "order_id"]
)

checks["Deliveries belong to completed orders"] = (
    deliveries["order_id"].isin(completed_order_ids).all()
)

checks["Reviews belong to completed orders"] = (
    reviews["order_id"].isin(completed_order_ids).all()
)

print("\n" + "=" * 50)
print("RELATIONSHIP VALIDATION")
print("=" * 50)

for check_name, passed in checks.items():
    print(f"{check_name}: {'PASS' if passed else 'FAIL'}")

# Overall validation result
no_missing_values = all(
    df.isnull().sum().sum() == 0
    for df, _ in datasets.values()
)

no_duplicate_ids = all(
    df[id_column].duplicated().sum() == 0
    for df, id_column in datasets.values()
)

all_relationships_valid = all(checks.values())

print("\n" + "=" * 50)

if no_missing_values and no_duplicate_ids and all_relationships_valid:
    print("OVERALL RESULT: PASS")
else:
    print("OVERALL RESULT: CHECK REQUIRED")

print("=" * 50)
