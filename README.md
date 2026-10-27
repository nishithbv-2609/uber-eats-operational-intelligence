# Uber Eats Operational & Customer Intelligence System

## Project Overview

This project uses synthetic food-delivery data to explore customer behaviour, restaurant performance, customer review sentiment, delivery-time prediction, and hourly order demand forecasting.

The project is developed in stages, covering data generation and validation, feature engineering, customer and restaurant segmentation, and further analytics and machine-learning tasks.

## Objectives

1. Segment customers and restaurants using clustering.
2. Analyse customer review sentiment using NLP.
3. Predict delivery time using regression models.
4. Forecast hourly order demand using time-series methods.
5. Develop data-driven operational recommendations.

## Project Structure

- `data/raw/` — Generated synthetic CSV datasets.
- `data/processed/` — Engineered, transformed, and segmented datasets.
- `notebooks/` — Analysis and modelling notebooks.
- `src/` — Python scripts for data generation, validation, and feature engineering.
- `models/` — Saved machine-learning models.
- `reports/figures/` — Visualisations and report figures.
- `docs/` — Data dictionary and project documentation.
- `tests/` — Data and pipeline tests.

## Data

Seven synthetic datasets are generated:

| Dataset | Description |
|---|---|
| `customers.csv` | Customer information |
| `restaurants.csv` | Restaurant information |
| `drivers.csv` | Driver information |
| `orders.csv` | Food order records |
| `deliveries.csv` | Delivery details and delivery times |
| `reviews.csv` | Customer ratings and review text |
| `payments.csv` | Payment records |

The datasets are generated for educational and analytical purposes.

## Day 1: Data Generation and Validation

The initial stage established the project datasets and validated their basic data quality.

- Generated seven synthetic CSV datasets.
- Checked for missing values and duplicate primary identifiers.
- Validated relationships between datasets.
- Checked that deliveries and reviews were associated with completed orders.

## Day 2: Customer and Restaurant Segmentation

**Objective:** Identify groups of customers with similar ordering behaviour and restaurants with similar business and operational characteristics.

### Feature Engineering

Customer features:
- Total orders
- Average order value
- Total spending
- Ordering frequency
- Weekend orders
- Late-night orders
- Average rating given

Restaurant features:
- Total orders
- Revenue
- Average rating
- Average preparation time
- Cancellation rate
- Average delivery time

### Data Preprocessing

- Loaded the engineered customer and restaurant datasets.
- Checked for missing values and applied median imputation where necessary.
- Removed customer and restaurant identifiers from the modelling features.
- Standardised numerical features using `StandardScaler`.

### Clustering Methods

**K-Means**

The Elbow Method and silhouette scores were used to assess potential cluster counts.

- Customers: 3 clusters.
- Restaurants: 5 clusters.

**DBSCAN**

DBSCAN was applied to identify dense groups and potential noise points.

- Customers: 450 points in one main cluster and 50 noise points.
- Restaurants: 73 points in one main cluster and 27 noise points.

With the selected parameters (`eps=1.5`, `min_samples=5`), DBSCAN did not identify multiple non-noise clusters in either dataset.

### Evaluation Results

| Dataset | K-Means clusters | Silhouette score | PCA variance explained by two components |
|---|---:|---:|---:|
| Customers | 3 | 0.215 | 55.62% |
| Restaurants | 5 | 0.220 | 64.82% |

The silhouette scores indicate limited separation between some clusters. Cluster profiles and business interpretations were therefore considered alongside the numerical evaluation.

PCA was used to reduce the feature dimensions to two components for visualising the K-Means clusters.

### Business Insights

Customer segmentation identified groups with different spending levels, order frequencies, and ordering patterns. These segments can support targeted promotions and customer-retention strategies.

Restaurant segmentation highlighted differences in order volume, revenue, ratings, cancellation rates, preparation times, and delivery times. These profiles can help identify operational strengths and areas for improvement.

The business labels are based on cluster averages and should be treated as initial interpretations.

### Day 2 Output Files

Engineered datasets:
- `data/processed/customer_features.csv`
- `data/processed/restaurant_features.csv`

Standardised datasets:
- `data/processed/customer_scaled.csv`
- `data/processed/restaurant_scaled.csv`

Final segmentation results:
- `data/processed/customer_segmentation_results.csv`
- `data/processed/restaurant_segmentation_results.csv`

The final segmentation files contain the engineered features, K-Means cluster assignments, business segment labels, and DBSCAN cluster assignments.

### Notebook

Day 2 analysis is available in:

`notebooks/day2_customer_restaurant_segmentation.ipynb`

## Environment Setup

Create and activate a Python virtual environment, then install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## Generate and Validate Data

To generate the synthetic datasets and validate them, run:

```bash
python src/data_generation.py
python src/validate_data.py
```

## Technologies Used

- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- Seaborn
- Jupyter Notebook

## Disclaimer

This is an educational project using synthetic data. It is not affiliated with or based on private Uber Eats customer or operational records.