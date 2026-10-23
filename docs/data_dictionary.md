# Uber Eats Operational & Customer Intelligence System
## Data Dictionary

This document describes the seven synthetic datasets generated for the project.

### 1. customers.csv

| Column | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `age` | Customer age in years |
| `gender` | Customer's recorded gender category |
| `city` | Customer's city |
| `signup_date` | Date the customer signed up |

### 2. restaurants.csv

| Column | Description |
|---|---|
| `restaurant_id` | Unique restaurant identifier |
| `restaurant_name` | Restaurant name |
| `cuisine` | Restaurant cuisine category |
| `city` | Restaurant's city |
| `restaurant_rating` | Restaurant rating from 2.5 to 5.0 |
| `average_prep_time_minutes` | Average food preparation time in minutes |

### 3. drivers.csv

| Column | Description |
|---|---|
| `driver_id` | Unique driver identifier |
| `vehicle_type` | Driver's vehicle type |
| `driver_rating` | Driver rating from 2.5 to 5.0 |
| `experience_months` | Driver experience in months |
| `city` | Driver's city |

### 4. orders.csv

| Column | Description |
|---|---|
| `order_id` | Unique order identifier |
| `customer_id` | Customer who placed the order |
| `restaurant_id` | Restaurant receiving the order |
| `order_timestamp` | Date and time the order was placed |
| `order_amount` | Total order amount |
| `num_items` | Number of items in the order |
| `order_status` | Order outcome: completed, cancelled, or failed |
| `order_hour` | Hour of the day when the order was placed |
| `order_date` | Calendar date of the order |

### 5. deliveries.csv

| Column | Description |
|---|---|
| `delivery_id` | Unique delivery identifier |
| `order_id` | Associated order identifier |
| `driver_id` | Driver assigned to the delivery |
| `distance_km` | Delivery distance in kilometres |
| `traffic_level` | Traffic category |
| `weather` | Weather category |
| `delivery_time_minutes` | Delivery duration in minutes |

### 6. reviews.csv

| Column | Description |
|---|---|
| `review_id` | Unique review identifier |
| `order_id` | Order being reviewed |
| `review_rating` | Customer review rating from 1 to 5 |
| `review_text` | Synthetic written customer feedback |

### 7. payments.csv

| Column | Description |
|---|---|
| `payment_id` | Unique payment record identifier |
| `order_id` | Associated order identifier |
| `payment_amount` | Amount associated with the order |
| `payment_method` | Payment method |
| `payment_status` | Payment outcome or processing status |

## Dataset Relationships

- `orders.customer_id` → `customers.customer_id`
- `orders.restaurant_id` → `restaurants.restaurant_id`
- `deliveries.order_id` → `orders.order_id`
- `deliveries.driver_id` → `drivers.driver_id`
- `reviews.order_id` → `orders.order_id`
- `payments.order_id` → `orders.order_id`

## Data Notes

- All datasets are synthetically generated for learning and demonstration.
- IDs are used to connect records across datasets.
- Deliveries and reviews are associated with completed orders.
- The validation script checks missing values, duplicate primary IDs, and selected relationships.
- Synthetic data may not reflect real-world Uber Eats distributions or performance.
