import pandas as pd

# Load the raw datasets
customers = pd.read_csv("data/raw/customers.csv")
orders = pd.read_csv("data/raw/orders.csv")
deliveries = pd.read_csv("data/raw/deliveries.csv")
reviews = pd.read_csv("data/raw/reviews.csv")
restaurants = pd.read_csv("data/raw/restaurants.csv")

# Check dataset dimensions
print("Customers:", customers.shape)
print("Orders:", orders.shape)
print("Deliveries:", deliveries.shape)
print("Reviews:", reviews.shape)
print("Restaurants:", restaurants.shape)

# Check column names
print("\nOrders columns:", orders.columns.tolist())
print("Deliveries columns:", deliveries.columns.tolist())
print("Reviews columns:", reviews.columns.tolist())
print("Customers columns:", customers.columns.tolist())




# Convert timestamps to datetime
orders["order_timestamp"] = pd.to_datetime(orders["order_timestamp"])
customers["signup_date"] = pd.to_datetime(customers["signup_date"])

# 1. Total orders, average order value, and total spending
customer_order_features = orders.groupby("customer_id").agg(
    total_orders=("order_id", "count"),
    avg_order_value=("order_amount", "mean"),
    total_spending=("order_amount", "sum")
).reset_index()

# 2. Ordering frequency: orders per month since signup
reference_date = orders["order_timestamp"].max()

customer_order_features = customer_order_features.merge(
    customers[["customer_id", "signup_date"]],
    on="customer_id",
    how="right"
)

customer_order_features["months_since_signup"] = (
    (reference_date - customer_order_features["signup_date"]).dt.days / 30.44
).clip(lower=1)

customer_order_features["total_orders"] = (
    customer_order_features["total_orders"].fillna(0)
)

customer_order_features["ordering_frequency"] = (
    customer_order_features["total_orders"]
    / customer_order_features["months_since_signup"]
)

# 3. Weekend orders: Saturday=5, Sunday=6
orders["day_of_week"] = orders["order_timestamp"].dt.dayofweek
weekend_orders = (
    orders[orders["day_of_week"].isin([5, 6])]
    .groupby("customer_id")
    .size()
    .rename("weekend_orders")
)

# 4. Late-night orders: 10 PM to 4:59 AM
late_night_orders = (
    orders[orders["order_hour"].isin([22, 23, 0, 1, 2, 3, 4])]
    .groupby("customer_id")
    .size()
    .rename("late_night_orders")
)

# 5. Average rating given by each customer
customer_ratings = orders[["order_id", "customer_id"]].merge(
    reviews[["order_id", "review_rating"]],
    on="order_id",
    how="inner"
)

avg_rating = (
    customer_ratings.groupby("customer_id")["review_rating"]
    .mean()
    .rename("avg_rating_given")
)

# 6. Combine all customer features
customer_features = customer_order_features[
    ["customer_id", "total_orders", "avg_order_value",
     "total_spending", "ordering_frequency"]
].set_index("customer_id")

customer_features = customer_features.join(weekend_orders)
customer_features = customer_features.join(late_night_orders)
customer_features = customer_features.join(avg_rating)

# Fill missing counts and ratings
customer_features[["weekend_orders", "late_night_orders"]] = (
    customer_features[["weekend_orders", "late_night_orders"]].fillna(0)
)

# Display the final customer feature dataset
customer_features = customer_features.reset_index()

print("\nCustomer feature dataset:")
print(customer_features.head())

print("\nCustomer feature shape:", customer_features.shape)
print("\nMissing values:")
print(customer_features.isnull().sum())


# ==========================================
# RESTAURANT FEATURE ENGINEERING
# ==========================================

# 1. Total orders and revenue per restaurant
restaurant_order_features = orders.groupby("restaurant_id").agg(
    total_orders=("order_id", "count"),
    revenue=("order_amount", "sum")
).reset_index()

# 2. Average customer rating per restaurant
restaurant_ratings = orders[["order_id", "restaurant_id"]].merge(
    reviews[["order_id", "review_rating"]],
    on="order_id",
    how="inner"
)

avg_rating = (
    restaurant_ratings.groupby("restaurant_id")["review_rating"]
    .mean()
    .rename("avg_rating")
)

# 3. Cancellation rate per restaurant
orders["is_cancelled"] = (
    orders["order_status"].astype(str).str.lower() == "cancelled"
)

cancellation_rate = (
    orders.groupby("restaurant_id")["is_cancelled"]
    .mean()
    .mul(100)
    .rename("cancellation_rate")
)

# 4. Average delivery time per restaurant
restaurant_deliveries = orders[["order_id", "restaurant_id"]].merge(
    deliveries[["order_id", "delivery_time_minutes"]],
    on="order_id",
    how="inner"
)

avg_delivery_time = (
    restaurant_deliveries.groupby("restaurant_id")["delivery_time_minutes"]
    .mean()
    .rename("avg_delivery_time")
)

# 5. Average preparation time
# Check whether preparation time is available in the datasets
prep_columns = [
    column for column in restaurants.columns
    if "prep" in column.lower() and "time" in column.lower()
]

if prep_columns:
    prep_column = prep_columns[0]

    avg_prep_time = (
        restaurants.set_index("restaurant_id")[prep_column]
        .rename("avg_prep_time")
    )
else:
    avg_prep_time = pd.Series(
        dtype="float64",
        name="avg_prep_time"
    )

# 6. Combine restaurant features
restaurant_features = restaurant_order_features.set_index("restaurant_id")

restaurant_features = restaurant_features.join(avg_rating)
restaurant_features = restaurant_features.join(cancellation_rate)
restaurant_features = restaurant_features.join(avg_delivery_time)
restaurant_features = restaurant_features.join(avg_prep_time)

# Include restaurants that have no orders
restaurant_features = restaurants[["restaurant_id"]].merge(
    restaurant_features.reset_index(),
    on="restaurant_id",
    how="left"
)

# Display results
print("\nRestaurant feature dataset:")
print(restaurant_features.head())

print("\nRestaurant feature shape:", restaurant_features.shape)

print("\nMissing values:")
print(restaurant_features.isnull().sum())



# Save feature-engineered datasets
customer_features.to_csv(
    "data/processed/customer_features.csv",
    index=False
)

restaurant_features.to_csv(
    "data/processed/restaurant_features.csv",
    index=False
)

print("\nFeature-engineered datasets saved successfully!")
