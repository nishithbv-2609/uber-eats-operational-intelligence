# Uber Eats Operational & Customer Intelligence System

## Project Overview

This project builds a synthetic data analytics and machine learning pipeline for an Uber Eats-style food delivery platform. It explores customer behavior, restaurant performance, customer reviews, delivery time prediction, and hourly order demand.

The project covers data generation, data validation, exploratory data analysis, clustering, natural language processing, regression, and time series forecasting.

**Note:** This project uses synthetic data for educational purposes. It does not use private Uber Eats customer or operational records.

---

## Project Objectives

- Generate and validate realistic food delivery datasets.
- Segment customers and restaurants using clustering algorithms.
- Analyze customer reviews using Natural Language Processing (NLP).
- Predict delivery times using regression models.
- Analyze hourly order demand and compare forecasting models.
- Translate analytical findings into potential business insights.

---

## Project Structure

```text
uber-eats-operational-intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   ├── day2_customer_restaurant_segmentation.ipynb
│   ├── day3.ipynb
│   ├── day4_delivery_time_prediction.ipynb
│   └── day5_hourly_demand_forecasting.ipynb
│
├── src/
│   ├── data_generation.py
│   └── validate_data.py
│
├── models/
├── reports/
│   └── figures/
├── docs/
├── tests/
├── requirements.txt
└── README.md
```

---

## Datasets

The project uses seven synthetic datasets:

| Dataset | Description |
|---|---|
| `customers.csv` | Customer details and attributes |
| `restaurants.csv` | Restaurant details and attributes |
| `drivers.csv` | Delivery driver information |
| `orders.csv` | Order details and timestamps |
| `deliveries.csv` | Delivery information and delivery times |
| `reviews.csv` | Customer ratings and review text |
| `payments.csv` | Payment transaction details |

---

# Project Progress

## Day 1: Data Generation and Validation

### Work Completed
- Generated synthetic datasets for the food delivery platform.
- Organized datasets into raw and processed data directories.
- Validated the generated data for basic quality and consistency.
- Prepared the datasets for further analysis.

### Scripts
- `src/data_generation.py`
- `src/validate_data.py`

---

## Day 2: Customer and Restaurant Segmentation

### Work Completed
- Performed exploratory analysis on customer and restaurant data.
- Created features for clustering.
- Scaled numerical features.
- Applied K-Means and DBSCAN clustering.
- Used PCA to explore the data in two dimensions.
- Evaluated clustering performance using silhouette scores.

### Results

| Analysis | Result |
|---|---|
| Customer K-Means clusters | 3 |
| Customer silhouette score | 0.215 |
| Customer PCA variance explained | 55.62% |
| Restaurant K-Means clusters | 5 |
| Restaurant silhouette score | 0.220 |
| Restaurant PCA variance explained | 64.82% |

DBSCAN identified one main cluster and noise points in both datasets. It did not identify multiple non-noise clusters with the tested settings.

| Dataset | Main cluster | Noise points |
|---|---:|---:|
| Customers | 450 | 50 |
| Restaurants | 73 | 27 |

### Output Files
- `data/processed/customer_features.csv`
- `data/processed/restaurant_features.csv`
- `data/processed/customer_scaled.csv`
- `data/processed/restaurant_scaled.csv`
- `data/processed/customer_segmentation_results.csv`
- `data/processed/restaurant_segmentation_results.csv`

### Notebook
`notebooks/day2_customer_restaurant_segmentation.ipynb`

---

## Day 3: Customer Review Sentiment Analysis

### Work Completed
- Loaded and explored customer review data.
- Cleaned review text by converting it to lowercase, removing punctuation, and processing tokens.
- Removed stopwords while preserving negations.
- Applied lemmatization.
- Converted review text into TF-IDF features.
- Analyzed sentiment using VADER.
- Compared VADER predictions with manually assigned sentiment labels.
- Built a Multinomial Naive Bayes text classification model.

### Dataset and Results

The review dataset contained **5,853 rows** and four columns: `review_id`, `order_id`, `review_rating`, and `review_text`.

After TF-IDF transformation, the feature matrix contained **5,853 rows and 32 features**.

#### VADER Sentiment Distribution

| Sentiment | Reviews | Percentage |
|---|---:|---:|
| Positive | 3,467 | 59.23% |
| Negative | 1,838 | 31.40% |
| Neutral | 548 | 9.36% |

The agreement between VADER sentiment and manually assigned labels was **80.33%**.

### Key Findings
- Positive sentiment was the largest category.
- Negative reviews highlighted possible issues such as late deliveries and cold food.
- Some reviews received different labels from VADER and the manual classification, showing that sentiment tools may interpret context differently.

### Limitation
The dataset contains only 10 unique review text templates. The Naive Bayes model reported 100% test accuracy, but this result is not reliable evidence of generalization because the text patterns are highly repetitive and the TF-IDF vectorizer was fitted before the train-test split. A stricter evaluation would fit the vectorizer only on the training data.

### Notebook
`notebooks/day3.ipynb`

---

## Day 4: Delivery Time Prediction

### Work Completed
- Explored delivery-related data.
- Prepared the target variable and engineered features for prediction.
- Built a regression workflow to estimate delivery time.
- Compared a baseline model with Ridge, Lasso, and Random Forest regression models.
- Evaluated model performance using MAE, RMSE, and R².
- Used cross-validation to assess model performance.
- Examined feature importance and visualized results.

### Output Files
- `data/processed/delivery_time_feature_engineered.csv`
- `data/processed/delivery_time_model_comparison.csv`

### Notebook
`notebooks/day4_delivery_time_prediction.ipynb`

### Objective
The goal was to investigate which features help explain delivery time and compare different regression approaches. Model performance should be judged using the evaluation results rather than assuming that a more complex model will always perform better.

---

## Day 5: Hourly Demand Forecasting

### Work Completed
- Converted order timestamps into hourly order counts.
- Analyzed hourly, daily, and weekday demand patterns.
- Examined the time series using seasonal decomposition.
- Tested stationarity using the Augmented Dickey-Fuller (ADF) test.
- Split the data chronologically into training and testing periods.
- Compared a baseline forecast, ARIMA, and Prophet.
- Evaluated forecasts using MAE and RMSE.
- Visualized actual demand against predicted demand.

### Dataset Summary

The order dataset contained **10,000 records**. Hourly resampling produced **35,063 hourly observations**, including hours with no orders.

| Metric | Result |
|---|---:|
| Average orders per hour | 0.285 |
| Maximum orders in an hour | 5 |
| Hours with orders | 8,744 |
| Hours with zero orders | 26,319 |
| Zero-order hours | Approximately 75% |

### Demand Pattern Findings
- Saturday had the highest total order count among the days of the week.
- Monday had the lowest total order count.
- Average hourly demand was similar on weekdays and weekends.
- Demand was sparse, with approximately three out of every four hourly observations containing zero orders.

### Stationarity Test

The ADF test returned a test statistic of approximately **-187.65** and a p-value of **0.0**. This provides strong evidence against the null hypothesis of a unit root for the tested series.

Stationarity is one part of time series analysis; it does not, by itself, establish the presence or absence of daily or weekly seasonal patterns.

### Forecasting Results

| Model | MAE | RMSE |
|---|---:|---:|
| Baseline Mean | 0.4232 | 0.5224 |
| ARIMA(2,0,2) | 0.4232 | 0.5224 |
| Prophet | 0.4188 | 0.5224 |

Prophet achieved a slightly lower MAE than the baseline and ARIMA models. However, the RMSE was the same to four decimal places for all three models.

### Key Findings
- The forecasts remained close to the average hourly demand.
- The models struggled to capture short-term demand spikes.
- ARIMA did not improve on the baseline in the reported evaluation.
- Prophet provided only a small improvement in MAE.
- MAPE was not used because many actual hourly values were zero, making percentage errors unsuitable for this dataset.

### Business Insight
The tested models did not substantially improve demand forecasts over the baseline. Since hourly demand is sparse and includes many zero-order periods, future work could explore count-based or intermittent-demand forecasting methods, additional calendar features, and more informative data.

### Output Files
- `data/processed/hourly_demand.csv`
- `data/processed/adf_test_results.csv`
- `data/processed/demand_forecast_model_comparison.csv`
- `data/processed/final_hourly_demand_forecast.csv`

### Notebook
`notebooks/day5_hourly_demand_forecasting.ipynb`

---

## Technologies Used

- Python
- pandas
- NumPy
- scikit-learn
- Matplotlib
- Seaborn
- NLTK / VADER
- Statsmodels
- Prophet
- Jupyter Notebook
- Git and GitHub

---

## Environment Setup

### 1. Create a Virtual Environment

```bash
python3 -m venv .venv
```

### 2. Activate the Environment

On Linux or macOS:

```bash
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Generate the Datasets

```bash
python src/data_generation.py
```

### 5. Validate the Datasets

```bash
python src/validate_data.py
```

---

## Conclusion

By Day 5, the project has covered synthetic data generation, data validation, customer and restaurant segmentation, customer review sentiment analysis, delivery time prediction, and hourly demand forecasting.

The results demonstrate how analytics and machine learning can support operational decisions in a food delivery platform. They also highlight the importance of data quality, suitable evaluation methods, and understanding the limitations of synthetic and repetitive datasets.