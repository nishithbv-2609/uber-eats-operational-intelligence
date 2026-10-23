
import pandas as pd
import numpy as np
from pathlib import Path

# --------------------------------------------------
# 1. Setup
# --------------------------------------------------

SEED = 42
rng = np.random.default_rng(SEED)

# Project root: ML_Assignment/
PROJECT_ROOT = Path(__file__).resolve().parent.parent
RAW_DATA_DIR = PROJECT_ROOT / "data" / "raw"
RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

# --------------------------------------------------
# 2. Customers
# --------------------------------------------------

NUM_CUSTOMERS = 500

customers = pd.DataFrame({
    "customer_id": range(1, NUM_CUSTOMERS + 1),
    "age": rng.integers(18, 66, NUM_CUSTOMERS),
    "gender": rng.choice(
        ["Male", "Female", "Other"], NUM_CUSTOMERS,
        p=[0.48, 0.48, 0.04]
    ),
    "city": rng.choice(
        ["Bengaluru", "Chennai", "Hyderabad", "Mumbai", "Delhi"],
        NUM_CUSTOMERS
    ),
    "signup_date": pd.to_datetime(
        rng.choice(
            pd.date_range("2022-01-01", "2025-12-31"),
            NUM_CUSTOMERS
        )
    ).strftime("%Y-%m-%d")
})

# --------------------------------------------------
# 3. Restaurants
# --------------------------------------------------

NUM_RESTAURANTS = 100

restaurants = pd.DataFrame({
    "restaurant_id": range(1, NUM_RESTAURANTS + 1),
    "restaurant_name": [
        f"Restaurant_{i:03d}" for i in range(1, NUM_RESTAURANTS + 1)
    ],
    "cuisine": rng.choice(
        ["Indian", "Chinese", "Italian", "Mexican", "Fast Food",
         "South Indian", "Desserts"],
        NUM_RESTAURANTS
    ),
    "city": rng.choice(
        ["Bengaluru", "Chennai", "Hyderabad", "Mumbai", "Delhi"],
        NUM_RESTAURANTS
    ),
    "restaurant_rating": np.round(
        rng.uniform(2.5, 5.0, NUM_RESTAURANTS), 1
    ),
    "average_prep_time_minutes": rng.integers(
        10, 41, NUM_RESTAURANTS
    )
})

# --------------------------------------------------
# 4. Drivers
# --------------------------------------------------

NUM_DRIVERS = 150

drivers = pd.DataFrame({
    "driver_id": range(1, NUM_DRIVERS + 1),
    "vehicle_type": rng.choice(
        ["Bike", "Scooter", "Car"], NUM_DRIVERS,
        p=[0.25, 0.65, 0.10]
    ),
    "driver_rating": np.round(
        rng.uniform(2.5, 5.0, NUM_DRIVERS), 1
    ),
    "experience_months": rng.integers(1, 121, NUM_DRIVERS),
    "city": rng.choice(
        ["Bengaluru", "Chennai", "Hyderabad", "Mumbai", "Delhi"],
        NUM_DRIVERS
    )
})

# --------------------------------------------------
# 5. Orders
# --------------------------------------------------

NUM_ORDERS = 10000

order_times = pd.to_datetime(
    rng.integers(
        pd.Timestamp("2022-01-01").value // 10**9,
        pd.Timestamp("2026-01-01").value // 10**9,
        NUM_ORDERS
    ),
    unit="s"
).round("min")

orders = pd.DataFrame({
    "order_id": range(1, NUM_ORDERS + 1),
    "customer_id": rng.integers(1, NUM_CUSTOMERS + 1, NUM_ORDERS),
    "restaurant_id": rng.integers(1, NUM_RESTAURANTS + 1, NUM_ORDERS),
    "order_timestamp": order_times,
    "order_amount": np.round(
        rng.gamma(shape=3.0, scale=250.0, size=NUM_ORDERS), 2
    ),
    "num_items": rng.integers(1, 11, NUM_ORDERS),
    "order_status": rng.choice(
        ["Completed", "Cancelled", "Failed"],
        NUM_ORDERS, p=[0.90, 0.07, 0.03]
    )
})

orders["order_hour"] = orders["order_timestamp"].dt.hour
orders["order_date"] = orders["order_timestamp"].dt.strftime("%Y-%m-%d")

# --------------------------------------------------
# 6. Deliveries
# --------------------------------------------------

delivery_orders = orders.loc[
    orders["order_status"] == "Completed", ["order_id", "restaurant_id"]
].copy()

num_deliveries = len(delivery_orders)

delivery_restaurants = delivery_orders["restaurant_id"].to_numpy() - 1

prep_times = restaurants["average_prep_time_minutes"].to_numpy()[
    delivery_restaurants
]

distance = np.round(rng.uniform(1, 20, num_deliveries), 2)
traffic = rng.choice(
    ["Low", "Medium", "High"], num_deliveries, p=[0.30, 0.45, 0.25]
)
weather = rng.choice(
    ["Clear", "Rainy", "Cloudy", "Stormy"],
    num_deliveries, p=[0.50, 0.20, 0.25, 0.05]
)

traffic_delay = np.select(
    [traffic == "Low", traffic == "Medium", traffic == "High"],
    [2, 8, 16]
)
weather_delay = np.select(
    [weather == "Clear", weather == "Cloudy",
     weather == "Rainy", weather == "Stormy"],
    [0, 3, 8, 15]
)

delivery_time = np.maximum(
    10,
    prep_times + (distance * 2.2) + traffic_delay + weather_delay
    + rng.normal(0, 5, num_deliveries)
).round().astype(int)

deliveries = pd.DataFrame({
    "delivery_id": range(1, num_deliveries + 1),
    "order_id": delivery_orders["order_id"].to_numpy(),
    "driver_id": rng.integers(1, NUM_DRIVERS + 1, num_deliveries),
    "distance_km": distance,
    "traffic_level": traffic,
    "weather": weather,
    "delivery_time_minutes": delivery_time
})

# --------------------------------------------------
# 7. Reviews
# --------------------------------------------------

review_orders = orders.loc[
    orders["order_status"] == "Completed", ["order_id"]
].sample(frac=0.65, random_state=SEED)

num_reviews = len(review_orders)

review_texts = [
    "Food was delicious and delivery was quick.",
    "The food was cold and arrived late.",
    "Great taste and excellent service.",
    "Order was okay but delivery took too long.",
    "Amazing experience, would order again!",
    "Poor packaging and disappointing food.",
    "Good value for money and friendly delivery.",
    "The order was missing items.",
    "Fresh food and fast delivery.",
    "Not satisfied with the overall experience."
]

reviews = pd.DataFrame({
    "review_id": range(1, num_reviews + 1),
    "order_id": review_orders["order_id"].to_numpy(),
    "review_rating": rng.choice(
        [1, 2, 3, 4, 5], num_reviews,
        p=[0.08, 0.10, 0.17, 0.30, 0.35]
    ),
    "review_text": rng.choice(review_texts, num_reviews)
})

# --------------------------------------------------
# 8. Payments
# --------------------------------------------------

payments = orders[["order_id", "order_amount", "order_status"]].copy()
payments = payments.rename(columns={"order_amount": "payment_amount"})
payments["payment_id"] = range(1, len(payments) + 1)
payments["payment_method"] = rng.choice(
    ["UPI", "Credit Card", "Debit Card", "Wallet", "Cash"],
    len(payments)
)
payments["payment_status"] = np.where(
    payments["order_status"] == "Completed",
    rng.choice(
        ["Paid", "Refunded", "Pending"], len(payments),
        p=[0.94, 0.04, 0.02]
    ),
    rng.choice(
        ["Failed", "Cancelled"], len(payments)
    )
)
payments = payments[
    ["payment_id", "order_id", "payment_amount",
     "payment_method", "payment_status"]
]

# --------------------------------------------------
# 9. Save CSV files
# --------------------------------------------------

datasets = {
    "customers.csv": customers,
    "restaurants.csv": restaurants,
    "drivers.csv": drivers,
    "orders.csv": orders,
    "deliveries.csv": deliveries,
    "reviews.csv": reviews,
    "payments.csv": payments
}

for filename, dataframe in datasets.items():
    output_path = RAW_DATA_DIR / filename
    dataframe.to_csv(output_path, index=False)
    print(f"Created {filename}: {len(dataframe):,} rows")

print("\nAll seven datasets generated successfully!")
print(f"Saved to: {RAW_DATA_DIR}")
